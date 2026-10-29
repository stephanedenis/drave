# R06 v3 — le déclencheur sans échelle : il classe (0,89–1,00), il faut le calibrer

> **Ligne de roadmap** : R06 (relecture) · **Date** : 2026-10-29 · **Verdict** : ✅ **les signaux
> sans échelle prédisent** — couverture **0,906**, accord **0,848**, dispersion 0,752 (la
> stabilité, 0,500, ne sert à rien) ; le déclencheur combiné **transfère en classement**
> (AUC **1,000** sur le lexical, **0,891** sur les paraphrases) ; ⚠️ **mais un seuil transféré
> à l'aveugle échoue** (0,636 et 0,373, sous les choix fixes) : il se **calibre par corpus**,
> et alors il approche l'oracle (0,915 et 0,422).
>
> **Dispositif** : 330 questions (247 lexicales + 83 paraphrases), quatre signaux, étiquette
> « l'extractif a juste », apprentissage sur un banc / test sur l'autre ; JSON
> [`r06-declencheur.json`](r06-declencheur.json).

## Le verrou

R0.5, R06 et la cascade ont échoué de la même façon : un **seuil absolu** sur un score BM25 ne
transfère pas, parce que l'échelle dépend du document. Le verrou n'est pas la cascade, c'est le
**déclencheur**. On teste donc des signaux **sans échelle** :

| signal | ce qu'il mesure |
|---|---|
| **couverture** | la part des mots de la question présents dans la réponse |
| **accord** | le span du balayage tombe-t-il dans le passage choisi par l'extractif ? |
| **dispersion** | (top1 − top2) / top1 — l'écart **relatif** du meilleur au second |
| **stabilité** | le gagnant survit-il au retrait d'un mot de la question ? |

## Ce qui est mesuré

**AUC pour « l'extractif a juste »** (330 questions) :

| signal | AUC |
|---|---:|
| couverture | **0,906** |
| accord | **0,848** |
| dispersion | 0,752 |
| stabilité | 0,500 |

**Le transfert du déclencheur combiné** (appris sur un banc, testé sur l'autre) :

| testé sur | AUC | seuil transféré | plafond (seuil calibré) | fixe extractif | fixe modèle |
|---|---:|---:|---:|---:|---:|
| lexical (247) | **1,000** | 0,636 | **0,915** | 0,874 | 0,231 |
| paraphrases (83) | **0,891** | 0,373 | **0,422** | 0,265 | 0,373 |

**Le classement transfère parfaitement ; le seuil, non.** Le seuil médian appris sur l'autre
banc allume le modèle 123 fois sur 247 (il coûte plus qu'il ne rapporte). **Calibré sur le
corpus**, le déclencheur atteint **0,915** (oracle 0,915) sur le lexical et **0,422** (oracle
0,458) sur les paraphrases — au-dessus du meilleur choix fixe de **+4** et **+5 points**.

## Ce que ça dit

1. **Le déclencheur existe** : les signaux sans échelle prédisent l'erreur de l'extractif
   (0,85–0,91), là où le score brut ne transférait pas.
2. **La calibration est le prix** : le seuil se règle sur le corpus (un échantillon suffit), pas
   sur un autre corpus. C'est la loi « le corpus décide », mais cette fois avec un outil
   **intra-corpus** : le déclencheur choisit les questions, la calibration choisit le niveau.
3. **La stabilité ne vaut rien** (0,500) : retirer un mot de la question ne change pas le
   gagnant — le classement est robuste, donc insensible. Un signal inutile, mesuré.

## Ce qui pourrait le rendre faux

- **l'AUC 1,000** sur le lexical est parfaite : à vérifier sur un autre corpus, elle peut être
  un artefact de la génération des questions (les golds partagent leurs mots) ;
- **le plafond est un oracle de seuil** : il dit ce que la politique peut rapporter, pas ce
  qu'elle rapportera avec un échantillon de calibration réel ;
- **330 questions**, deux corpus : le transfert est testé une fois, pas dix ;
- **les signaux sont lexicaux** : une paraphrase sans recouvrement n'a pas de couverture — mais
  c'est justement là que le déclencheur s'allume (couverture basse → modèle).

## Ce que ça change

- **La cascade peut être déclenchée** : il reste à brancher le seuil **calibré** (échantillon du
  corpus) dans `lecture.py --cascade` et à mesurer la politique sur les trois jeux ;
- **la fiche R06 a son déclencheur** : couverture + accord, seuil calibré par corpus.

## Fichiers

- `tools/declencheur.py` — les quatre signaux, l'AUC, le transfert, le plafond.
- `reports/r06-declencheur.json` — les mesures.
