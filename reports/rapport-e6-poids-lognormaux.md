# E6 — poids log-normaux : les chiffres corrigés, et les trois chiffres RÉTRACTÉS

> Campagne : **biologie** · expérience : E6 (`docs/biologie-pour-drave.md` § 3 ter)
> Question : une distribution **multiplicative** des poids (celle du cortex) rend-elle l'élagage
> moins cher que la nôtre, quasi gaussienne — et quel rôle joue la **contrainte de signe**
> (principe de Dale) ?
> Verdict, **après correction de deux défauts du harnais** : **la loi log-normale COÛTE à
> l'élagage, dans les deux conditions de signe** ; la contrainte de signe, elle, **n'a pas d'effet
> cohérent** (elle aide d'un côté du plan, elle nuit de l'autre). Le meilleur point du plan est
> **signes figés + magnitudes libres** : 41,67 à 25 % gardés contre 49,43 au témoin dense (×1,19).
> Date réelle : **2026-10-11 03 h 00 HAE** (heure lue sur la machine).
> Mesures : `tools/entrainer_moteur.py` · occupation : `tools/occupation_poids.py` ·
> invariants : `tools/porte-harnais-invariants.sh`.

## 0. CE QUI EST RÉTRACTÉ, ET POURQUOI

Trois chiffres publiés dans cette fiche le 10 et le 11 octobre sont **faux** et sont **retirés**.
Ils ont été obtenus avec un harnais qui avait deux défauts, tous deux corrigés depuis :

| chiffre retiré | ce qu'il annonçait | pourquoi il est faux |
|---|---|---|
| « signes figés : **7,9467** à 25 % gardés, **×1,09** » | un modèle quasi insensible à l'élagage | l'**attention n'était pas élaguée** pour les variantes reparamétrées : seuls les experts l'étaient (attention à 1,0 % de zéros au lieu de 75 %) |
| « la loi log-normale **nuit**, 2,2× pire » | un effet énorme entre deux variantes | même défaut : les deux variantes étaient élaguées **différemment** |
| « **trois graines** : 7,95 · 7,99 · 8,27 contre 49,43 · 55,45 · 46,61 » | une robustesse spectaculaire | les trois valeurs « signes figés » souffrent du même défaut |

**Ce qui les a trouvés** : l'instrument d'occupation (`tools/occupation_poids.py`, manque **M9**) a
montré une attention à 1,0 % de zéros là où l'annonce disait 75 %. **Ce qui les a rendus
définitivement faux** : le second défaut, plus grave — l'inverse appliqué **deux fois** à
l'installation, qui faisait partir les modèles log-normaux avec des poids de **±12** au lieu de
±0,08 (θ moyen 1,097 au lieu de −2,8 ; validation 3,0713 au lieu de 2,4874 bits/octet). Aucun des
deux n'était visible dans un chiffre de perplexité.

Les deux défauts sont maintenant **rallumables** (`DRAVE_ELAGAGE_SANS_PARAM=1`,
`DRAVE_INSTALL_DOUBLE=1`) et **surveillés** par `tools/porte-harnais-invariants.sh`, qui vérifie que
les invariants tiennent — et qui a été **vue rouge par les deux bouts**.

## 1. Le plan 2×2, refait proprement

Mêmes conditions partout (7,58 M paramètres, 3 000 pas, même graine, mêmes 28 tenseurs élagués,
même export, même texte, **même initialisation** — vérifiée : l'installation laisse le modèle
inchangé à 6e-06 près), et l'occupation **lue dans le fichier** :

| poids gardés | occupation | dense (magnitudes libres, signes libres) | **signes figés, magnitudes libres** | magnitudes log-normales, signes libres | magnitudes log-normales, signes figés |
|---|---:|---:|---:|---:|---:|
| 100 % | 89,2 % | 7,3429 | **7,3003** | 7,2741 | 7,6168 |
| 50 % | 50,6 % | 7,5680 | **7,2241** | 7,4955 | 7,8401 |
| 25 % | 26,0 % | 49,4291 | **41,6677** | 59,1526 | 71,1531 |

*Les quatre variantes ont exactement la même occupation à chaque taux (26,0 % à 25 % gardés) : la
comparaison porte enfin sur le même élagage.*

**Ce que le plan dit, et il ne dit pas ce qu'on croyait.**

1. **La loi log-normale COÛTE**, et c'est le seul effet cohérent du plan : à 25 % gardés elle donne
   **71,15** (signes figés) et **59,15** (signes libres) là où des magnitudes libres donnent
   **41,67** et **49,43**. L'effet est du même signe dans les deux conditions de signe (**×1,71** et
   **×1,20**), donc il ne dépend pas d'elles. La prédiction biologique n'est **pas** vérifiée ;
2. **la contrainte de signe n'a PAS d'effet cohérent** : figer les signes **aide** avec des
   magnitudes libres (49,43 → 41,67, ×1,19) et **nuit** avec des magnitudes log-normales
   (59,15 → 71,15, ×0,83). Il y a **interaction**, donc pas de « mécanisme Dale » à annoncer ;
3. **le meilleur point du plan est `signes figés + magnitudes libres`** aux trois taux (7,3003 ·
   7,2241 · 41,6677) — mais l'avantage sur le témoin dense reste **modeste** : ×1,006 sans élagage,
   ×1,05 à 50 %, **×1,19** à 25 %. On n'a pas trouvé le levier qui rend l'élagage gratuit.

## 2. Ce que la mesure a appris de plus solide que son résultat

**Deux instruments manquaient, et leur absence a produit trois faux résultats publiés.** C'est la
leçon la plus réutilisable de cette expérience :

- **une occupation annoncée n'est pas une occupation faite** : la ligne « élagage à 25 % gardé :
  28 tenseurs · 100 % des poids de projection » était **fausse pour les modèles reparamétrés**
  (l'attention en était exclue). Il a fallu `tools/occupation_poids.py` — qui lit le **fichier** —
  pour le voir ;
- **un modèle reparamétré n'est pas le modèle d'avant** : l'installation appliquait l'inverse deux
  fois, et rien ne le disait. La vérification ajoutée (`# installation : le modèle est INCHANGÉ
  (écart max …)`) l'aurait vu **au premier run** ;
- **aucun des deux n'était visible dans une perplexité** : les deux produisaient des nombres
  parfaitement plausibles. C'est la définition d'un défaut qui coûte cher.

## 3. Ce que cette fiche ne dit PAS

- **pourquoi** la loi log-normale coûte : l'hypothèse la plus simple — `e^θ` ne peut pas atteindre
  zéro (plancher 6,1e-6), donc un poids « élagué » continue de contribuer — n'est **pas** testée
  ici ; le témoin à plancher du 11/10 allait dans ce sens, mais il a été mesuré sous l'ancien
  harnais ;
- **une seule échelle** (7,58 M paramètres), un corpus, une graine pour le tableau principal ;
- **elle ne teste pas d'autres façons de figer les signes** : `tanh(ψ)` et `signe · |θ|` sont deux
  conventions ; la seconde est celle qui gagne ici, et rien ne dit qu'une troisième ne ferait pas
  mieux ;
- **elle ne dit rien du coût réel** : le compteur de paires du moteur ne voit pas l'occupation
  (manque **M9**, seconde moitié) ; le gain de stockage se lit dans le **fichier**, pas dans la
  ligne « paires ».

## 4. Protocole, pour rejouer

```bash
P=/home/stephane/gpu-env/bin/python; D=./drave-core/target/release/drave
BASE="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 \
      --lot 32 --pas 3000 --lr 3e-4 --graine 1 --elagage-tous 500"
# les quatre coins du plan, à 25 % gardés
$P tools/entrainer_moteur.py $BASE                                    --elagage 0.25 --sortie /tmp/b/dense
$P tools/entrainer_moteur.py $BASE --signes-figes                     --elagage 0.25 --sortie /tmp/b/sigfiges
$P tools/entrainer_moteur.py $BASE --poids-lognormaux                 --elagage 0.25 --sortie /tmp/b/logn
$P tools/entrainer_moteur.py $BASE --poids-lognormaux --signes-libres --elagage 0.25 --sortie /tmp/b/libres
for V in dense sigfiges logn libres; do
  $P tools/exporter_gguf.py --hf /tmp/b/$V --sortie /tmp/b/$V.gguf
  $P tools/occupation_poids.py --modele /tmp/b/$V.gguf      # l'occupation, dans le FICHIER
  $D /tmp/b/$V.gguf --ppl /tmp/e6/val.ids --limit 512 --ctx 512 --threads 4 | grep perplexité
done
tools/porte-harnais-invariants.sh                            # les deux invariants du harnais
```
