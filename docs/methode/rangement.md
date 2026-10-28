# Le rangement, et la revue de documentation

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
> **avant de classer un fichier** ou de clore un sous-chantier.

## Les quatre dossiers (règle stricte)

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | quatre familles : **méthode**, **pilotage**, **théorie**, **implantation** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |

Dans `docs/`, les quatre familles sont **séparées** : `methode/` (comment on travaille), `pilotage/` (où l'on en
est), `theorie/` (ce qui reste vrai), `implantation/` (comment c'est construit). Une page de `docs/` qui se remplit
de tableaux de mesures **déménage** dans `reports/` ; il reste dans `docs/` un **résumé de l'état** (ce qu'on sait,
ce qu'on ne sait pas, et le lien vers la fiche). À chaque cycle,
[`docs/pilotage/en-cours.md`](../pilotage/en-cours.md) dit l'état **courant** en quelques lignes, pas l'historique.

## La revue de fin de sous-chantier (obligatoire)

**Quand** : à la **fin de chaque sous-chantier**, et au minimum **une fois par cycle**, avant le commit de clôture.
**Quoi** : `python3 tools/revue_documentation.py` vérifie — et il faut **corriger** avant de continuer :

1. **classement** : un résultat qui traîne dans `docs/` est déplacé dans `reports/` ; une page de `docs/` qui n'a
   plus de « ce qui reste vrai » est supprimée ;
2. **structure** : chaque chantier de `en-cours.md` a son entrée, son état, sa fiche, et ses sous-chantiers ;
3. **annotation** : tous les **liens internes** résolvent (docs ↔ reports ↔ journal), **leur libellé ne ment pas
   sur la cible** (un lien qui annonce `docs/x` ne doit pas pointer `docs/archive/x`), et les **sources externes**
   (Glottolog, Gutenberg, Unicode UDHR, Cellar/EUR-Lex, Panini/Nipada) sont citées avec leur URL ou leur chemin ;
4. **fraîcheur** : la date de `en-cours.md` est celle du **dernier commit** (comparaison réelle ; l'heure est
   informative) ;
5. **compteurs** : la page d'état est la **source unique** — **49 portes, 8 chapitres, 215 fichiers / 282 JSON,
   55 documents** — et la revue les compare au disque (fichiers de `reports/`, `docs/`, `tools/porte-*.sh`) ;
6. **cohérence** : la synthèse ([`docs/theorie/synthese/index.md`](../theorie/synthese/index.md)) et le tableau de bord disent la
   même chose, et l'index liste **B10–B12** ;
7. **navigation** : aucun document vivant n'est **orphelin**, et aucun **chemin en code inline** ne pointe vers un
   fichier absent (hors gabarits `AAAA`, `<...>`, `*`) ;
8. **vocabulaire** : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) — elle est en
   **unités de sens**, le jeton est l'unité technique du tokeniseur (voir le [glossaire](../theorie/glossaire.md)) ✓✓.

Les portes [`porte-tableaux`](../../tools/porte-tableaux.sh) (cellules des tableaux, liens) et
[`porte-registre`](../../tools/porte-registre.sh) complètent la revue.

Les **schémas** sont vérifiés par `python3 tools/verifier_schemas.py` : SVG valides, `viewBox`,
`title`/`desc`, liens relatifs, absence d'ASCII art. Les sources `.mmd`/`.puml` sont acceptées :
l'image pointe vers `<source>.svg`, que docwatch génère même s'il n'est pas versionné. L'**index exhaustif** des fiches est
régénéré par `python3 tools/index_reports.py` (→ [`reports/INDEX.md`](../../reports/INDEX.md)).

> *Une documentation qui n'est pas revue à la fin d'un sous-chantier est une documentation qui mentira au cycle
> suivant* ✗✓.

## Les documents datés

Un plan, une note ou un état **daté** porte en tête :

```text
> **Document daté — dernière vérification : AAAA-MM-JJ.**
```

La revue signale les documents datés de **plus de 90 jours** ; `docs/archive/` en est exclu. Un document qui
reste vrai n'est **pas** daté : il reste dans `docs/`.

## La taille et la cohésion

Un document **chargeable** a un **budget** (en mots) et une **cohésion** minimale : un sujet, un
titre, un résumé de 3 à 6 lignes, une consigne de chargement. Le protocole et les budgets sont dans
[`contexte.md`](contexte.md) ; `python3 tools/taille_documents.py` vérifie les budgets et les
résumés, et signale les fiches de résultats de plus de 300 lignes (à lire par verdict + section).

## La synthèse théorique

[`docs/theorie/synthese/`](../theorie/synthese/) porte la **théorie** (8 chapitres, 14 schémas), et son `index.md` doit refléter les
**sept chantiers** et dire la même chose que `en-cours.md`. Les chiffres y sont cités comme état, jamais comme
tableau de mesure.
