# N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : à recette égale (34,3 M, deux
> étages de 20 000 pas, canal), le corpus de **831 Mo** (600 000 articles, offset 1 M, **0 fuite**)
> donne **3,7025** sur la validation de N2.z (3,5250) et **3,4604** sur la sienne ; N2.z donne
> **3,5250** sur la sienne et **3,7107** sur celle du grand. **Chaque modèle est meilleur sur son
> propre domaine** (écart ~0,2) : à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus
> — il fait apprendre **autre chose**.

## Le dispositif

- **Corpus** : 600 000 articles (page_id à partir de 1 000 000, disjoint du corpus N2.j qui part de
  200 000) ; brut **1 048 Mo** → dédupliqué **924 Mo (88,2 %)** → train **831 Mo**, val 46 Mo, test
  46 Mo ; **0 fuite** sur 4 000 fenêtres (`reports/corpus-wiki-big-propre.json`).
- **Modèle** : 34,3 M (`384/512`), deux étages de 20 000 pas × 8 × 128, positions [0, 384], canal de
  structure — exactement la recette de N2.z.
- **Évaluation croisée** : chaque modèle sur **les deux** validations (la même fenêtre de 4 lots ×
  16 × (L+1) octets, canal fourni), L = 128/256/512.

## Ce qui est mesuré

| modèle | val N2.z (186 Mo) | val grand (831 Mo) |
|---|---:|---:|
| **N2.z** (186 Mo, canal) | **3,5250** | 3,7107 |
| **grand** (831 Mo, canal) | 3,7025 | **3,4604** |
| écart | −0,18 pour N2.z | −0,25 pour le grand |

Courbe du grand sur son val : **3,46 / 3,45 / 3,90** à 128/256/512 (N2.z : 3,53 / 3,49 / 3,66).

## Lecture

**Le corpus ne paie pas à compute constant.** Les deux modèles ont vu **40 Mo** de texte (2 × 20 000
pas × 8 × 128) ; le grand en a vu 5 % et le petit 21 %. Le grand ne peut donc pas « savoir plus » :
il sait **autre chose**. Et chaque modèle est meilleur sur la tranche qu'il a côtoyée — la PPL est
dominée par l'**appariement de domaine** entre l'entraînement et la validation, pas par la taille du
corpus.

**Le signal interne est réel mais non comparable** : sur son propre val, le grand vaut 3,46 (3,45 à
256) contre 3,53 pour N2.z — mais les deux validations n'ont pas la même difficulté (les articles
1 M+ sont plus récents, autre vocabulaire).

**La bonne question n'est donc pas « plus de données ? » mais « plus de pas ? ».** À 40 Mo vus, le
corpus est un changement de domaine ; pour tester la donnée comme levier, il faut **10× le compute**
(200 000 pas) sur les deux corpus, ou un curriculum qui balaie le corpus.

## Ce que ça change pour N2

- La prochaine action n'est pas « un corpus plus gros » mais **plus de pas sur le corpus existant**
  (le contrôle : 200 000 pas sur 186 Mo, puis sur 831 Mo).
- La **validation doit être tirée du même domaine** que l'entraînement, sinon la PPL mesure le
  décalage, pas la qualité — la leçon vaut pour tous les comparatifs de la ligne N.
- La déduplication de 1 Go coûte **~80 Go de mémoire** (version légère : `bytearray` + `set` ; la
  version du dépôt en demande 110+) : au-delà, il faut une passe par blocs avec un état de
  chevauchement.

## Ce qui pourrait le rendre faux

- **Une graine, un seul corpus, une seule paire de validations** ; l'écart de 0,2 est net mais
  l'intervalle n'est pas mesuré.
- **Le décalage temporel** : l'offset 1 M correspond à des articles plus récents que l'offset 200 k
  — une partie de l'écart est un effet de **distribution**, pas de taille.
- **40 Mo vus** : c'est le point le plus limitant ; à 200 000 pas, la conclusion pourrait s'inverser.
- **Le canal** est fourni aux deux, mais le grand corpus a son propre canal (recalculé sur son
  texte) — pas d'asymétrie de ce côté.

## Fichiers

- Corpus : `data/wiki_big/{brut.txt,propre/}` ; manifeste : `reports/corpus-wiki-big-propre.json`.
- Modèles : `work/n2w/base-big.pt`, `base-big-canal.pt` ; outils :
  `work/n2w/{extraire_big,deduit_leger,pipeline_big.sh,eval_croise.py}`.
- Mesures : sorties de `evalue_canal.py` et `eval_croise.py` (3,5250 / 3,7025 / 3,4604 / 3,7107).
