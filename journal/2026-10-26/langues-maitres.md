# 2026-10-26 — Les langues et les maîtres

<!-- notes -->
**La demande.** « Couvre le plus de langues possibles pour toutes ces connaissances, étudie les livres des grands
maîtres en parallèle. » Deux extensions de B5/B6, menées ensemble : un **lexique multilingue** (les mots des jeux
dans 71 langues) et une **base de principes** tirés des livres, encodée dans la pensée.

**Les langues.** Le lexique est une **donnée** : **35 concepts**, **71 langues**, **1 433 couples** de libellés,
construits depuis **Wikidata** (CC0) — pièces des échecs, rangs et enseignes des cartes, noms des cinq jeux et du
whist, couleurs, notions de maîtres. **32 langues** sont « fortes » (de quoi dire une pièce N/P et une carte). Le
corpus multilingue de **449 surfaces** est lu à **100 %** au niveau 4 ; les **11/11** paires (le même coup dans
toutes les langues) sont invariantes ; la permutation des libellés laisse **12/275** items forts (**4,4 %**), le
sens s'effondre. La **notation** (FEN, SAN, UCI, GTP, SGF, binaire) est le recours indépendant de la langue :
**5 112/5 112** lectures (72 items × 71 langues). Les noms de jeux sont détectés **315/315** ; la langue, **343/449**
(**76,4 %**), les confusions venant des libellés partagés.

Ce que les langues **ne** sont **pas** : de la grammaire. Les libellés Wikidata sont des **lemmes** ; les surfaces
sont des **mots-clés** (pièce + cases, rang + enseigne, nom du jeu + coordonnée). Cinq langues (`ky`, `lo`, `mt`,
`si`, `yo`) n'ont aucun item ; la notation les couvre. `e4`/`E4` restent ambiguës entre échecs et go. C'est écrit
dans la fiche, pas caché.

**Les maîtres.** **17 principes**, **9 sources** (sept ouvrages du domaine public — Lasker 1925, Capablanca 1921, Nimzowitsch 1925,
Tarrasch 1931, Payne 1756, Smith 1908, Cavendish 1884 —, les proverbes du go et le morpion résolu), **3 parties**
(Opéra 1858, Immortelle 1851, Toujours verte 1852) validées jusqu'au mat, **28 positions** de livre.

Ce que les principes **déplacent** : aux échecs, le premier coup passe de **Nc3** à **d4**, le livre tient
**10/10**, les mats restent **3/3** ; aux dames, **10 victoires, 10 nulles, 0 défaite** en 20 parties (la base ne gagne
**aucune** des 20 parties avec les Blancs, **0/20** — biais de couleur nommé) ; au go 9×9, **10/10** coups de 3e/4e ligne avec le prior
contre **3/10** sans. Ce qu'ils **ne déplacent pas** : l'accord avec le coup du maître aux échecs (**42/101** avec,
**41/101** sans — **+1**, non significatif) ; sur 5×5, le bord et la capture sont déjà trouvés par la base
(**10/10** des deux côtés) ; aux cartes, la politique du whist **perd** contre la base (**44,7 %** contre
**51,0 %**), et l'ablation (sans honneur 43,5 %, sans seconde 45,7 %, sans troisième 46,5 %) ne la rattrape pas.
La connaissance des livres est une **entrée**, pas la force.

**Le prix.** La vitesse de lecture est passée de **3 083** à **1 297 parses/s** au niveau 4 : la tokenisation
Unicode et la détection de langue des 71 langues coûtent ce facteur ~2,4. La couche reste sous la milliseconde par
surface ; c'est le prix du multilingue, pas une régression cachée. La mesure complète des maîtres prend **468,8 s**,
les jeux **188,7 s**, les langues **3,1 s**, sur Hauru (Python 3.13, sans GPU).

**La porte.** `tools/porte-jeux.sh` est étendue : **65 tests** (dont 11 nouveaux), la couche multilingue, la
permutation, la notation, les maîtres. Elle est verte. La passe complète des 48 portes reste à lancer avant le
commit de clôture.

**Les fichiers.** [`reports/rapport-langues-maitres.md`](../reports/rapport-langues-maitres.md),
[`reports/jeux-langues-mesures.json`](../reports/jeux-langues-mesures.json),
[`reports/jeux-maitres-mesures.json`](../reports/jeux-maitres-mesures.json), le concept
[`docs/jeux-symboliques.md`](../docs/jeux-symboliques.md), la roadmap **B7/B8**.
<!-- /notes -->
