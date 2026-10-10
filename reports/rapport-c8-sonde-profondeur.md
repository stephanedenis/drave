# C8 — le réflexe : l'état intermédiaire CONTIENT le prochain jeton, c'est la TÊTE qui ne sait pas le lire

> Campagne : **cerveau** · expérience : sonde linéaire sur l'état de la couche 16
> Question : un chemin court (s'arrêter à la couche 16, appliquer une tête) ne sait rien — mais
> est-ce l'**état** qui est pauvre, ou la **tête** qui ne sait pas le lire ? Autrement dit :
> **faut-il entraîner une tête par profondeur, ou C8 est-il hors de portée ?**
> Verdict : **l'information est là, et elle est même LINÉAIREMENT accessible** — une sonde ridge
> sur l'état de la couche 16 prédit le prochain jeton (parmi les 256 plus fréquents) avec
> **43,1 %** de justes sur des positions **jamais vues**, contre **4,0 %** pour la classe
> majoritaire et **0,39 %** pour le hasard. La tête empruntée, elle, rend une perplexité de
> **728 388** contre **9,43** pour le modèle complet : **le maillon faible est la tête**, et C8
> a un sens.
> Date réelle : **2026-10-10 11:35 HAE**.
> Protocole : `tools/c8_sonde_lineaire.py` (capture par `drave --couches 0:15 --tete-partielle
> --etat-sortie F --etat-pos 4,5,…,1023`), Qwen2.5-0.5B-Q8_0, `ids_0.5B-Q8.txt`, 1 024 jetons.

## 1. Le fait mesuré, et il est brutal

| chemin | perplexité (1 023 jetons) |
|---|---|
| modèle complet (24 couches) | **9,4341** |
| **réflexe** : couches 0 → 15, puis la tête du modèle (`--tete-partielle`) | **728 388,7546** |

Un facteur **77 000**. C'était la mesure du premier pas de C8, et elle avait été lue comme
« un chemin court ne peut pas lire un état intermédiaire » (cos 0,145 entre l'état et ce que la
tête attend). **Cette lecture attribuait à l'état ce qui appartient à la tête.**

## 2. La sonde : ce que l'état contient vraiment

Protocole : capturer l'état de la couche 16 (896 canaux, juste avant la norme finale) à
1 019 positions ; cible = **le jeton suivant** du corpus ; sonde = régression ridge fermée
`W = (XᵀX + λI)⁻¹ Xᵀ Y` sur les **256 jetons les plus fréquents** ; partage **train/test par
position** (la première moitié entraîne, la seconde évalue : aucune position de test n'est vue).

| mesure | valeur |
|---|---|
| **sonde linéaire, test** | **43,1 %** |
| classe majoritaire (référence) | 4,0 % |
| hasard uniforme sur 256 classes | 0,39 % |
| fréquence du jeton le plus fréquent du corpus | 5,27 % |

**43,1 % là où la référence est à 4 %** : l'information du prochain jeton est **présente** dans
l'état de la couche 16 et elle est **linéairement décodable**. Un réflexe à cette profondeur n'est
donc pas condamné par la pauvreté de l'état.

## 3. Ce que ça change pour C8, et ce que ça ne dit pas

**Ce que ça change** : le chantier n'est pas « trouver une profondeur où l'état serait riche »,
c'est **entraîner la tête** — c'est-à-dire le même travail que C7 vers les poids. La sonde donne
même la marche à suivre : une tête **non linéaire** sur le même état devrait faire mieux que
43,1 %, et la question devient « combien des 9,43 du modèle complet un réflexe de couche 16 peut-il
retrouver ? ».

**Ce que ça ne dit pas** :

- **une seule profondeur** (16 sur 24) et **un seul texte** (1 024 jetons du corpus de campagne) :
  la courbe profondeur → décodabilité n'est pas mesurée, et c'est elle qui dirait où placer le
  réflexe ;
- **256 classes sur 151 936** : la sonde mesure une décision **restreinte**. Le chiffre n'est donc
  pas comparable à la perplexité du modèle complet, et il ne faut pas l'y comparer ;
- **linéaire** : une sonde linéaire qui marche ne dit pas ce qu'une tête entraînée atteindrait
  (elle dit seulement que l'information n'est pas absente) ;
- **la latence du réflexe** n'est pas mesurée : un chemin court n'a d'intérêt que s'il va plus
  vite, et 16 couches sur 24, ce n'est qu'un tiers de calcul en moins.

## 4. Protocole, pour rejouer

```bash
D=./drave-core/target/release/drave; M=models/Qwen2.5-0.5B-Q8_0.gguf
POS=$(seq -s, 4 1023)
$D "$M" --ppl /tmp/campagne24/ids_0.5B-Q8.txt --limit 1024 --ctx 1024 --threads 8 \
   --couches 0:15 --tete-partielle --etat-sortie /tmp/c8/etat --etat-pos "$POS"
python3 tools/c8_sonde_lineaire.py --etats /tmp/c8/etat --ids /tmp/campagne24/ids_0.5B-Q8.txt \
   --limite 1024 --classes 256
```

Deux défauts de harnais attrapés en écrivant la sonde, tous deux du même genre (un instrument qui
ne dit rien au lieu de dire qu'il ne peut rien dire) : les `ids` de la campagne sont un **CSV sur
une ligne**, qu'un découpage sur les blancs lit comme **zéro** jeton ; et une liste d'états vide
rendait « 0 position × 896 canaux » au lieu de s'arrêter. Corrigé : lecture CSV **ou** une par
ligne, et arrêt explicite si les entrées sont vides.
