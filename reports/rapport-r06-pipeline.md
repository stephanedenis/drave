# R0.6 — le pipeline de lecture : 12/20 au pilote, 10/10 refusés, 7/8 au modèle

> **Ligne de roadmap** : R0.6 · **Date** : 2026-10-29 · **Verdict** : ✅ **le contrat est tenu** —
> 19/20 réponses acceptées au pilote dont **12 justes** (0,600), **provenance vérifiée 19/19**,
> **refus 10/10** sur des questions hors sujet, **rejeu identique**, et le **modèle** répond
> **7/8** là où l'extractif n'en donne que **3/8** (paraphrases).
>
> **Dispositif** : `tools/lecture.py` (extractif par défaut, modèle sur demande) ; seuil de refus
> **3,8** ; porte `tools/porte-lecture.sh` (6 contrôles) ; JSON brut
> [`r06-pipeline.json`](r06-pipeline.json) ; spec
> [`pipeline-lecture.md`](../docs/implantation/pipeline-lecture.md).

## La question

R0.1 (le document), R0.2 (le contrôleur), R0.3 (le banc) existent séparément. Le pipeline les
**assemble** : un document, une question, un budget → une réponse **avec sa source**, dans une
trace rejouable. La question de la fiche : le contrat tient-il — budget, provenance, refus,
rejeu — et que vaut l'assemblage sur les trois régimes mesurés ?

## Le dispositif

- **une commande** : `python3 tools/lecture.py --document X --question Q [--budget 0.30]
  [--lecteur extractif|modele]` ; sortie JSON ou texte, la source (région, offset, sha) avec
  la réponse ;
- **le refus** : si le meilleur score BM25 est sous **3,8**, la réponse est « insuffisant » —
  le pipeline ne rend pas un passage au hasard ;
- **la porte** : 6 contrôles — réponse connue, budget tenu, provenance, rejeu, refus,
  closed-book — tous verts ;
- **les trois régimes** : pilote (20 questions main), hors sujet (10 questions), paraphrases
  (8 questions du banc durci).

## Ce qui est mesuré

| régime | mesure | chiffre |
|---|---|---|
| **pilote** (20 questions) | réponses acceptées · justes · provenance | **19/20** · **12/20 = 0,600** · **19/19** |
| **hors sujet** (10 questions) | refus | **10/10 = 1,000** |
| **paraphrases** (8 questions) | extractif · modèle | **3/8** · **7/8** |
| **rejeu** | deux exécutions, même JSON | **identique** |
| **porte** | 6 contrôles | **6/6** |

**Le pipeline fait ce qu'il promet** : il lit dans le budget (2 516 octets sur 3 132 pour la
question de référence), cite sa source (région `r00032`, octets 8015–8339), refuse le hors
sujet, et rejoue à l'identique.

**Et il choisit bien ses lecteurs** : sur les paraphrases, l'extractif ne donne que 3/8 (il est
refusé ou trompé), le **modèle en donne 7/8**. C'est la leçon de R0.3 rendue **utilisable** :
le lexique pour les mots, le modèle pour les paraphrases, et le refus comme aiguillage.

## Le seuil, et pourquoi 3,8

Les scores BM25 des **réponses justes** du pilote vont de **3,94 à 11,08** ; le seul **faux
positif** hors sujet (« trois » dans « trois octets ») est à **3,56**. Le seuil **3,8** sépare
les deux, refuse 1 question du pilote (dont la réponse était fausse de toute façon) et laisse
passer les 12 justes. Il est exposé (`--seuil`) : c'est un réglage **calibré sur ce corpus**,
pas une constante universelle.

## Ce qui pourrait le rendre faux

- **le seuil est calibré sur l'échelle BM25 brute** de ce corpus : un autre document, une autre
  longueur de passages, et 3,8 ne sépare plus rien (la leçon du routeur, R0.5) ;
- **les échantillons sont petits** : 20, 10 et 8 questions ; un cas vaut 0,05 à 0,125 ;
- **le modèle n'a ni provenance ni refus** : il répond toujours, et sa réponse ne se cite pas ;
- **le pilote** mesure le lecteur extractif (0,600), pas le pipeline : le pipeline ne fait que
  l'assembler — c'est déjà le plafond de R0.2 ;
- **le budget en octets** ignore le coût CPU réel (découpage, scoring), qui reste négligeable
  ici (0,02 s).

## Ce que ça change

1. **R0 est utilisable** : une commande, un contrat, une porte. Les mesures de R0.1–R0.3 ne
   sont plus des fiches isolées, elles sont un lecteur.
2. **Le refus est une propriété de sûreté** : un pipeline qui répond toujours est un pipeline
   qui devine ; celui-ci dit « insuffisant » quand il ne sait pas, et propose le modèle.
3. **L'aiguillage extractif/modèle est démontré** là où il compte : 3/8 contre 7/8 sur les
   paraphrases.

## Fichiers

- `tools/lecture.py` — le pipeline (extractif, modèle, refus, provenance, trace).
- `tools/porte-lecture.sh` — la porte à 6 contrôles.
- `docs/implantation/pipeline-lecture.md` — le contrat et les limites.
- `reports/r06-pipeline.json` — les mesures brutes (20 + 10 + 8 questions).
