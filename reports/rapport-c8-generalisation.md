# C8 — la tête réflexe sur des textes JAMAIS VUS : jusqu'à ×5,7 du modèle complet

> Campagne : **cerveau** · expérience : adaptateur entraîné sur des morceaux distincts du corpus,
> testé sur un morceau tenu à l'écart
> Question : la tête entraînée de l'expérience précédente était apprise sur la **première moitié
> d'un texte** et évaluée sur la **seconde**. Alors : **une tête entraînée sur des textes
> sait-elle lire un texte qu'elle n'a JAMAIS vu ?**
> Verdict : **oui, et elle s'en approche beaucoup quand on lui donne des données** — sur un
> morceau tenu à l'écart, la tête empruntée rend **697 572** de perplexité, la tête entraînée sur
> **30 morceaux** rend **84,99**, et le modèle complet vaut **15,02** sur ce même morceau : le
> réflexe n'est plus qu'à **×5,7** du modèle complet (il en était à ×46 000 avec la tête
> empruntée). Avec **7 morceaux seulement**, la même recette donne 202,17 — **les données
> comptent** (÷2,4), et le surapprentissage arrive plus tôt.
> Date réelle : **2026-10-10 14:20 HAE** · **toutes les graines sont fixées** (`--graine 0`).
> Protocole : `tools/c8_corpus.sh` (morceaux de 1 024 jetons pris à des endroits différents du
> corpus) puis `tools/c8_entrainer_tete.py --train … --test …`.

> **Ce que cette fiche remplace.** Un premier passage (même journée, avant la graine fixée et sur
> un découpage différent) annonçait **÷79** avec 2 632,05. Ce chiffre n'était pas reproductible :
> deux entraînements au même protocole donnaient 2 632 puis 9 056, parce que **l'ordre des lots
> n'était pas fixé**. Les chiffres ci-dessous le sont (`--graine 0`), et le protocole est plus
> strict. L'ancien chiffre est conservé ici comme trace.

## 1. Le protocole, et pourquoi il change la question

| | expérience précédente | **celle-ci** |
|---|---|---|
| entraînement | première moitié d'un texte | **7 morceaux distincts** (jetons 0, 10k, 21k, …) |
| test | seconde moitié **du même texte** | **un morceau jamais vu**, pris ailleurs |
| ce que le chiffre mesure | l'adaptation au texte | la **généralisation** |

Les morceaux sont pris à des positions réparties dans tout le corpus (pas des fenêtres voisines),
et **les cibles de chaque morceau sont ses propres jetons** — un seul fichier d'identifiants pour
tous aurait donné des cibles étrangères aux états, c'est-à-dire un apprentissage sur du bruit qui
aurait « mesuré » que la tête ne généralise pas.

## 2. Les chiffres — graine fixée, test tenu à l'écart

Toutes les lignes : entraînement sur des morceaux **qui n'incluent pas** le morceau de test,
évaluation sur les positions du morceau de test, meilleure époque restaurée.

| protocole (`--graine 0`) | tête empruntée | **tête entraînée** | modèle complet |
|---|---|---|---|
| 7 morceaux → test m7 | 697 572,2130 | **202,1726** (époque 6) | 15,0163 |
| **30 morceaux → test m7** | 697 572,2130 | **84,9860** (époque 2) | 15,0163 |
| 39 morceaux → test m39 | 370 205,4060 | **51,4647** (époque 2) | 8,6773 |
| 39 morceaux, tête **non linéaire** (512) → m39 | 370 205 (identité) | 272,1710 (époque 2) | 8,6773 |

**Trois faits :**

1. **la tête entraînée généralise** : sur un texte jamais vu, elle passe de 697 572 (tête
   empruntée) à **85** — et le modèle complet n'est plus qu'à **×5,7** ;
2. **les données comptent** : à texte de test égal (m7), passer de 7 à 30 morceaux fait 202 → 85
   (÷2,4), et le meilleur point arrive **plus tôt** (époque 2 au lieu de 6) : plus de données,
   plus vite surappris ;
3. **la non-linéarité n'aide pas ici** : une tête 896→512→896 (GELU) rend **272** là où
   l'adaptateur linéaire rend **51** sur le même test. Avec 39 000 exemples, la capacité
   supplémentaire se paie — ce n'est pas une preuve que la non-linéarité est inutile, c'est une
   preuve qu'**elle ne suffit pas** : il faudrait régulariser et régler le taux d'apprentissage.

**Ce que le chiffre ne dit pas** : ces textes viennent tous du **même corpus** (donc du même
domaine, du même style, souvent du même vocabulaire). La question « une tête entraînée sur un
corpus lit-elle un corpus DIFFÉRENT ? » reste ouverte, et c'est la vraie question d'un réflexe
utilisable.

## 3. Le surapprentissage fixe encore le chiffre, et deux pièges l'ont faussé

L'adaptateur apprend vite le texte d'entraînement et se dégrade ensuite sur le texte neuf : avec
30 morceaux, le meilleur test est à l'**époque 2** (84,99) et l'entraînement continue de
descendre. C'est le script qui garde la meilleure époque et qui la restaure — sans quoi le
tableau aurait affiché la dernière (bien pire).

**Deux pièges attrapés dans cette campagne, et ils se ressemblent :**

1. **l'entraînement n'était pas graine-fixé** : deux exécutions identiques donnaient **2 632**
   puis **9 056** sur le même test. Aucune comparaison (7 morceaux contre 30, linéaire contre non
   linéaire) n'était concluante. Corrigé : `--graine 0` par défaut ;
2. **le morceau de test était DANS la liste d'entraînement** : pour isoler l'effet « plus de
   données » j'ai lancé « morceaux 0..30 → test m7 »… or **m7 ∈ 0..30**. La tête rendait
   **1,5978** — mieux que le modèle complet (15,02) ! Le chiffre était trop beau : c'était de la
   **mémorisation**. Refait avec la liste **0..30 privée de 7**, il donne **84,99**. Un test qui
   appartient à l'entraînement ne teste rien, et il ne le dit pas : c'est la même famille que la
   porte qui compare zéro jeton.

## 4. Ce que ça change pour C8

**Acquis** : le maillon faible était la tête, pas la profondeur. Une tête **ajustée pour sa
couche** rend le réflexe utilisable sur un texte jamais vu (**85** contre **697 572**), à **×5,7**
du modèle complet — et le chemin court va **×1,54 plus vite** en génération
(`rapport-c8-tete-entrainee.md` § 3 bis). Le compromis devient intéressant : **1,5× plus vite pour
5,7× de perplexité**, au lieu de 46 000×.

**Ce qui reste ouvert** :
- **un autre corpus** : tous ces morceaux viennent du même document. C'est la question qui décide
  si un réflexe est utilisable en pratique ;
- **régularisation et taux d'apprentissage** : la non-linéarité a échoué ici faute de réglage,
  pas par nature ;
- **la profondeur** : le point de fonctionnement (qualité × vitesse) n'est mesuré qu'à 16 couches ;
- **l'échelle des données** : 30 morceaux de 1 024 jetons, c'est 30 000 exemples — un vrai
  entraînement se compte en millions, et c'est un autre chantier que cette sonde.

## 5. Protocole, pour rejouer

```bash
tools/c8_corpus.sh 40 1024 16           # 40 morceaux pris à des endroits différents
PY=/home/stephane/gpu-env/bin/python
# LA LISTE D'ENTRAÎNEMENT EXCLUT LE MORCEAU DE TEST — construit comme ceci, jamais à la main :
TRAIN=$(python3 -c "print(','.join(f'/tmp/c8-corpus/etat-m{i}' for i in range(0,31) if i != 7))")
CUDA_VISIBLE_DEVICES=0 $PY tools/c8_entrainer_tete.py --train "$TRAIN" \
   --test /tmp/c8-corpus/etat-m7 --ids /tmp/c8-corpus/morceau-7.txt \
   --modele models/Qwen2.5-0.5B-Q8_0.gguf --limite 1024 --epoques 20 --graine 0
```

**Les deux règles de lecture de cette fiche** : la graine est **fixée** (sinon deux chiffres du
même protocole diffèrent du simple au triple), et le morceau de test est **exclu de la liste
d'entraînement** — vérifié en comptant, comme pour les jetons dans les portes.
