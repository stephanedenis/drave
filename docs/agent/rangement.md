# Le rangement, et la revue de documentation

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
> **avant de classer un fichier** ou de clore un sous-chantier.

## Les quatre dossiers (règle stricte)

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | l'**état actuel**, la **mission**, la **vision**, l'**architecture**, les **concepts**, les **modes d'emploi** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |

Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/` ; il reste dans `docs/` un
**résumé de l'état** (ce qu'on sait, ce qu'on ne sait pas, et le lien vers la fiche). À chaque cycle,
[`docs/en-cours.md`](../en-cours.md) dit l'état **courant** en quelques lignes, pas l'historique.

## La revue de fin de sous-chantier (obligatoire)

**Quand** : à la **fin de chaque sous-chantier**, et au minimum **une fois par cycle**, avant le commit de clôture.
**Quoi** : `python3 tools/revue_documentation.py` vérifie — et il faut **corriger** avant de continuer :

1. **classement** : un résultat qui traîne dans `docs/` est déplacé dans `reports/` ; une page de `docs/` qui n'a
   plus de « ce qui reste vrai » est supprimée ;
2. **structure** : chaque chantier de `en-cours.md` a son entrée, son état, sa fiche, et ses sous-chantiers ;
3. **annotation** : tous les **liens internes** résolvent (docs ↔ reports ↔ journal), et les **sources externes**
   (Glottolog, Gutenberg, Unicode UDHR, Cellar/EUR-Lex, Panini/Nipada) sont citées avec leur URL ou leur chemin ;
4. **fraîcheur** : la date de `en-cours.md` est l'**heure locale** du dernier commit (jamais une estimation) ;
5. **cohérence** : la synthèse ([`docs/synthese/index.md`](../synthese/index.md)) et le tableau de bord disent la
   même chose ;
6. **vocabulaire** : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) — elle est en
   **unités de sens**, le jeton est l'unité technique du tokeniseur (voir le [glossaire](../glossaire.md)) ✓✓.

Les portes [`porte-tableaux`](../../tools/porte-tableaux.sh) (cellules des tableaux, liens) et
[`porte-registre`](../../tools/porte-registre.sh) complètent la revue.

> *Une documentation qui n'est pas revue à la fin d'un sous-chantier est une documentation qui mentira au cycle
> suivant* ✗✓.

## La synthèse théorique

[`docs/synthese/`](../synthese/) porte la **théorie** (7 chapitres, 7 schémas), et son `index.md` doit refléter les
**sept chantiers** et dire la même chose que `en-cours.md`. Les chiffres y sont cités comme état, jamais comme
tableau de mesure.
