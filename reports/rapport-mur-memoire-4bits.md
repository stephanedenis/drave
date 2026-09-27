# Le mur mémoire, et ce que les 4 bits achètent vraiment

> Suite de `rapport-croisement-push-pull.md`. Trois bugs de mesure corrigés, une
> mesure de bande passante, et un chemin 4 bits écrit puis mesuré.

## 1. Trois bugs qui faussaient les conclusions

| bug | symptôme | cause |
|---|---|---|
| **drapeau final ignoré** | `--dense` « donnait exactement le même résultat que push » | `while i + 1 < args.len()` : un drapeau en **dernière** position n'était jamais lu |
| **tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26 | chaque worker n'écrivait que sa tranche ; la somme des 16 vecteurs récupérait les restes du travail précédent |
| **parenthesage flottant** | pull et push divergeaient d'un token | `(dot×s)×sx` contre `acc×(sx×s)` — deux arrondis différents sur des sommes entières pourtant exactes |

Le troisième n'était pas un bug mais une occasion : en écrivant les deux chemins
avec **le même ordre d'opérations**, et parce que les sommes entières sont
exactes des deux côtés, on obtient une propriété forte :

> **push, pull int8 et auto donnent des résultats bit à bit identiques.**
> PPL 19,2647 au chiffre près sur 510 jetons, 24 jetons identiques, et 0 contre
> 180,7 G événements — les trois modes empruntent donc bien des chemins
> d'exécution différents tout en calculant la même chose.

Changer de mode d'exécution ne peut plus changer un seul token. C'est ce qu'on
veut pouvoir affirmer d'une architecture : le mode est une décision de
**performance**, pas de **sémantique**.

## 2. Le croisement push/pull, remesuré

Comparaison à arithmétique **identique** (`PushMat` et `DenseQ8` partagent la
même quantification int8, une échelle par sortie). Le banc isole une matrice et
impose la densité d'activation.

`blk.0.ffn_gate.weight` — 4 864 × 896, 4,36 M poids, 16 threads :

| densité | push (ms) | pull (ms) | push/pull |
|---|---|---|---|
| 0 % | 0,004 | 0,167 | 0,03 |
| 1 % | 0,019 | 0,162 | 0,12 |
| 5 % | 0,047 | 0,168 | 0,28 |
| 10 % | 0,078 | 0,163 | **0,48** |
| 25 % | 0,180 | 0,163 | 1,11 |
| 50 % | 0,355 | 0,165 | 2,15 |
| 100 % | 0,801 | 0,171 | **4,69** |

`blk.0.attn_q.weight` — 896 × 896 : croisement à **24 %**.
`blk.0.ffn_down.weight` — 896 × 4864 : croisement vers **33–45 %** (mesure
bruyante : le temps du pull y passe de 0,342 à 0,192 ms entre 25 % et 50 % sans
raison algorithmique — effet de cache/NUMA, signalé et non lissé).

➡️ **Le croisement est à ~22 %, pas à 10 %.** Il se lit directement dans le
rapport à pleine densité : le pull traite 4,7 fois plus de poids par seconde que
le push ne traite d'événements, donc l'égalité tombe vers 1/4,7 = 21 %. Le seuil
de bascule `seuil_push` passe de 0,15 à **0,22**, la valeur mesurée.

À 10 % de densité le push est ×2,1 plus rapide ; à 1 %, ×8,3. L'affirmation
antérieure (« égalité à 10 % ») venait de mesures d'avant la correction de
`dot_chunked` : elle est retirée.

## 3. Le mur mémoire

Question restée ouverte : le noyau dense est-il mal écrit, ou déjà au bout de la
machine ? Le banc mesure maintenant un **repère de bande passante** dans les
mêmes conditions que les mesures (64 Mo lus par 16 threads, mots de 64 bits) :

```
bande passante mémoire mesurée : 19–22 Go/s   (charge de fond : 4–8)
pull : 4,4 Mo lus à 14,1–26,9 Go/s, soit 62–136 % du repère
```

Deux enseignements :

1. **Le noyau dense est au mur.** Il lit ses poids à 14 Go/s quand la mémoire en
   donne 20 : il n'y a plus de facteur 4 caché dans le code. Le confirme une
   expérience involontaire mais nette — la **même** matrice, **même** code, passe
   de 26 Go/s à 14 Go/s selon que le tableau de bord poussif du tour précédent
   l'a chassée du L3 ou non.
2. **Dérouler ne sert à rien ici.** `dot_chunked` avait un seul accumulateur
   (chaîne de dépendance, ~1 multiplication/cycle) ; réécrit avec huit
   accumulateurs indépendants : **gain nul** (21,98 ms contre 21,94). C'est la
   preuve par l'expérience que le poste n'est pas arithmétique.

➡️ Conséquence : **seul le nombre d'octets par poids peut encore faire gagner.**
D'où le chemin 4 bits.

## 4. Chemin 4 bits : 0,53 octet par poids

Forme `DenseQ4` : nibbles signés biaisés (`w = (nibble−8)·s_bloc`), une échelle
`u16` **relative** par bloc de 32 (précision 1/65535, et non 1/255 — essayé :
PPL 17,09 contre 17,10, donc la précision d'échelle n'était pas le facteur
limitant, mais 16 bits ne coûtent que 0,5 bit/poids).

**4,5 bits/poids effectifs** (4 + 16/32), contre 8 pour l'int8 : ×1,78 moins
d'octets.

Le noyau scalaire était **plus lent** que l'int8 (dépaquetage : masque, décalage,
biais, deux chaînes d'accumulation — ~5 cycles par poids). D'où un noyau **AVX2**
(16 poids par `vpmaddwd`) :

- le bug de la première version : `vpmaddwd` recevait les poids **pairs**
  (nibbles bas) en face de `x[0..16]`. Il faut **réentrelacer** (`_mm_unpacklo/hi_epi8`)
  avant d'élargir. Trouvé par un test unitaire : scalaire 132,331 contre AVX2 −2,495.
- après correction : **bit à bit identique au scalaire** sur les quatre formes de
  matrice testées, et sur `ffn_gate` réelle (4 864 × 896).

## 5. Ce que les 4 bits achètent — balayage de précision mixte

255 jetons, contexte 256, activations int16, 16 threads :

| configuration | PPL | écart | tok/s | projets+MLP (ms/jeton) |
|---|---|---|---|---|
| int8 partout | **17,4092** | — | 28,3 | 22,1 |
| 4 bits **attention** | 18,3503 | +5,4 % | 24,5 | 27,0 |
| 4 bits **FFN** | 21,6082 | +24,1 % | 37,0 | 14,1 |
| 4 bits corps entier | 21,9118 | +25,9 % | **39,2** | 13,1 |

Trois faits, dont deux contre-intuitifs :

1. **Le FFN est la partie sensible**, pas l'attention. C'est l'inverse de ce que
   la campagne de parcimonie avait montré — mais elle portait sur la parcimonie
   des **activations**, celle-ci sur la précision des **poids**. Deux
   perturbations différentes, deux sensibilités différentes : à retenir.
2. **Les 4 bits ne paient que sur les grosses matrices.** L'attention (0,8 M
   poids, 800 Ko en int8) tient dans le cache : on paie le dépaquetage sans
   économiser de mémoire — ×1,22 **plus lent**. Le FFN (4,36 M poids, 4,36 Mo)
   déborde : ×1,57 plus rapide.
3. Le gain de bout en bout est **×1,39** (28,3 → 39,2 tok/s) pour **+26 % de
   perplexité**. Sur un modèle de 0,5 G, c'est le prix connu des petits modèles en
   4 bits.

## 5 bis. Un VRAI modèle 4 bits, et la leçon de la double quantification

`models/Qwen2.5-0.5B-Q4_0.gguf` est un modèle 4 bits qui a fait ses preuves ; le
lecteur GGUF savait déjà décoder Q4_0, mais le moteur le **requantifiait** (f32 →
int8, ou f32 → notre 4 bits), c'est-à-dire ajoutait une seconde couche d'erreur à
une source déjà quantifiée.

D'où l'import **verbatim** : les blocs Q4_0 (échelle f16 + 16 octets de nibbles)
sont recopiés dans la disposition interne, sans jamais repasser par les f32.
510 jetons, contexte 256, activations int16, 16 threads :

| modèle | noyau | PPL | écart | s | tok/s |
|---|---|---|---|---|---|
| Qwen2.5-0.5B **Q8_0** | int8 | **19,2647** | — | 18,0 | 28,3 |
| Qwen2.5-0.5B **Q4_0** | int8 (requantifié) | 21,1971 | +10,0 % | 18,0 | 28,3 |
| Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** |
| Qwen2.5-0.5B **Q4_0** | 4 bits + tête 4 bits | 21,7431 | +12,9 % | 12,0 | **42,5** |

(255 jetons donnaient 19,86 / 19,67 / 19,88 : l'écart de la tête 4 bits n'apparaît
qu'à 510 jetons — leçon de méthode habituelle, ne pas conclure sur 255.)

Deux résultats :

1. **Le prix réel des 4 bits sur ce modèle est +9,1 % de perplexité** — pas les
   +26 % mesurés en requantifiant depuis Q8_0. La double quantification était le
   vrai coupable : elle coûtait 12 % de perplexité *en plus* du format.
2. **Le noyau 4 bits est plus fidèle ET plus rapide que l'int8 sur les mêmes
   poids** : 21,01 contre 21,20 de perplexité (il ne requantifie pas) et 13,2
   contre 18,2 s. Un noyau 4 bits n'est pas un compromis ; c'est la
   représentation **native** de ces poids.

Un détail qui a coûté une mesure : en Q4_0 l'échelle de bloc est **signée**
(`d = max/−8`, où `max` est la valeur *signée* de plus grande amplitude), donc
`d < 0` dès que le poids extrême du bloc est positif. Stocker sa valeur absolue
a donné PPL 3 550 569 avant correction.

## 5 ter. L'attention : mesurer avant d'optimiser

Le découpage par poste montrait 3,1 ms/jeton pour l'attention à contexte 256,
pour seulement ~0,5 M de multiplications. Premier réflexe : c'est la relecture du
cache KV (14 têtes de requête pour 2 têtes KV, donc les mêmes clés lues 7 fois).
**Hypothèse fausse** — un chemin groupé par tête KV, qui lit les clés une fois par
groupe, n'a rien changé (3,20 → 3,27 ms), tout en restant bit à bit identique.

L'instrumentation des trois phases a tranché :

| phase | avant | après |
|---|---|---|
| scores `q·k` | **2,10 ms** | **0,65 ms** |
| softmax | 0,28 | 0,27 |
| somme pondérée + écriture KV | 0,71 | 0,65 |
| **total** | **3,09** | **1,57** |

Les scores étaient du **calcul scalaire pur** : un `zip().map().sum()` est une
chaîne d'additions que LLVM n'a pas le droit de réassocier, et le code tenait
3,3 opérations par cycle — soit la largeur d'émission du processeur. Huit
accumulateurs indépendants n'ont rien donné non plus (2,10 → 2,16 ms) : il ne
restait que le SIMD. En AVX2 + FMA, 32 éléments par tour : **×3,3**.

Ni le cache KV, ni la latence d'addition, ni le `exp()` n'étaient le goulot —
c'était l'absence de vectorisation, et seule l'instrumentation par phase l'a
montré. La perplexité bouge au 4ᵉ chiffre (21,0116 → 21,0131) : la somme n'est
plus « dans l'ordre », c'est le prix assumé.

## 6. Conclusion honnête

- Le défaut reste **int8 dense** : c'est le meilleur rapport qualité/débit, et
  c'est désormais le même résultat qu'en mode événementiel, au bit près.
- **Pour un modèle 4 bits qui existe déjà** (Q4_0), le chemin `--q4` est le bon
  choix sans hésitation : ×1,34 de débit **et** une perplexité légèrement
  meilleure que l'int8, parce qu'il ne requantifie pas.
- **Pour un modèle 8 bits**, requantifier en 4 bits coûte +26 % de perplexité :
  à ne faire que si le débit est la contrainte, jamais par défaut. Le levier
  reste réel — c'est le seul qui subsiste quand la mémoire plafonne à 20 Go/s —
  et il se paiera mieux sur un modèle où le FFN domine davantage, ou avec un
  noyau AVX-512.
- `--q4-attn` et `--q4-tout` sont conservés comme **résultats négatifs** : ils
  sont lents et/ou dégradent sans rien acheter.

## 7. Reproductible

```bash
cd qtrinet-core && cargo build --release
cargo test --release            # noyau AVX2 vs scalaire
B=../models/Qwen2.5-0.5B-Q8_0.gguf

# bande passante + croisement push/pull sur une matrice
./target/release/qtrinet-core $B --matrix blk.0.ffn_gate.weight --threads 16

# équivalence bit à bit des trois modes
for f in "" --dense --auto; do
  ./target/release/qtrinet-core $B --ppl /tmp/wt2_ids.txt --ctx 256 --abits 16 \
     --threads 16 --limit 512 $f | grep "perplexité"
done

# balayage de précision
for f in --dense --q4-attn --q4-ffn --q4; do
  ./target/release/qtrinet-core $B --ppl /tmp/wt2_ids.txt --ctx 256 --abits 16 \
     --threads 16 --limit 256 $f | grep "perplexité"
done
```

Et sur le modèle 4 bits lui-même :

```bash
Q=../models/Qwen2.5-0.5B-Q4_0.gguf
./target/release/qtrinet-core $Q --ppl /tmp/wt2_ids.txt --ctx 256 --abits 16 --threads 16 --limit 512 --dense
./target/release/qtrinet-core $Q --ppl /tmp/wt2_ids.txt --ctx 256 --abits 16 --threads 16 --limit 512 --q4
```
