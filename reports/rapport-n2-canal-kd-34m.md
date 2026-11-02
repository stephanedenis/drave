# N2.y — Le canal et la distillation ne s'additionnent pas, même à 34,3 M

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le 34,3 M **canal + distillation**
> (professeur 30,29 M, 2 graines) vaut **3,5277** en domaine (128), contre **3,5131** pour le canal
> **seul** (N2.z) — **+0,015**, dans le bruit — et **3,7778** à 512 octets contre **3,6558** (+0,12).
> La distillation **n'ajoute rien** au canal et **coûte** en longueur. Le meilleur modèle de la
> nuit reste le **canal seul** (3,51 / 3,66).

## La question

N2.x avait montré qu'à 11,47 M, la distillation **absorbe** le canal (−0,03). N2.z a montré qu'à
34,3 M le canal est le meilleur levier (−0,48). La question : à 34,3 M, le canal et la distillation
**s'additionnent-ils** cette fois ?

## Le dispositif

- Init : `base-34m-canal.pt` (34,3 M avec canal, N2.z), val 3,5131.
- Professeur : 30,29 M (`route-480`, N2.u).
- Distillation : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384], **canal fourni**,
  **2 graines**.

## Ce qui est mesuré

| modèle | 128 | 256 | 512 | mélange « milieu » | mélange « tout » |
|---|---:|---:|---:|---:|---:|
| **canal seul** (N2.z) | **3,5131** | **3,4836** | **3,6558** | ×6,6 | ×11,2 |
| **canal + KD** (Z-g1/g2) | 3,5277 | 3,4984 | 3,7778 | ×6,5 | ×10,7 |
| écart | +0,015 | +0,015 | **+0,12** | = | = |

## Lecture

**La distillation n'ajoute rien au canal** : +0,015 en domaine, c'est du bruit entre graines. Et
elle **coûte en longueur** (+0,12 à 512) : le professeur (30,29 M) n'a pas le canal, et son signal
tire l'élève vers une modélisation sans structure — ce qui dégrade la longueur.

**Le canal est le meilleur levier à 34,3 M** : 3,5131 contre 3,6852 pour la distillation seule
(N2.r) et 3,9973 pour la base (N2.p). C'est le résultat le plus net de la nuit : à capacité égale,
**donner la structure en entrée** bat **distiller un professeur 2× plus petit**.

**Le mélange reste inchangé** (×6,5) : le canal ne change pas la nature du lecteur.

## Ce que ça change pour N2

- La **recette de production française** est : corpus réel 186 Mo, positions aléatoires, base
  34,3 M, **canal de structure**, sans distillation → **3,51 / 3,48 / 3,66**.
- La distillation reste utile pour les petits modèles (11,47 M : −0,51) et pour l'OOD (le
  professeur plus gros gagne 0,3 hors domaine, N2.u) — mais elle n'est pas le levier principal.
- La **fenêtre** (R1) reste la question : même à 3,66 à 512, le modèle ne lit pas au-delà de 256
  octets ; il ne s'effondre plus.

## Ce qui pourrait le rendre faux

- **Deux graines** ; l'écart de +0,015 est dans le bruit, mais l'écart de longueur (+0,12) est
  cohérent sur les deux graines.
- **Un réentraînement depuis la base avec canal**, pas depuis zéro : le canal profite des poids
  déjà appris.
- **Le canal est heuristique** (6 classes) ; un canal plus riche pourrait changer la conclusion.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Élèves : `work/n2j/Z-g{1,2}.pt` ; référence : `work/n2j/base-34m-canal.pt` ; professeur :
  `work/n2j/route-480`.
- Mesures : `work/n2j/eval-34m-canal.json` (canal seul), et les sorties de `evalue_canal.py`.
