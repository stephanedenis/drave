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

## 6. Conclusion honnête

- Le défaut reste **int8 dense** : c'est le meilleur rapport qualité/débit, et
  c'est désormais le même résultat qu'en mode événementiel, au bit près.
- `--q4` (corps en 4 bits) est **le seul levier qui reste** une fois le noyau au
  mur mémoire : ×1,39 sur un CPU dont la mémoire plafonne à 20 Go/s. Il se
  paiera sur un modèle où le FFN domine davantage, ou avec un noyau AVX-512.
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
