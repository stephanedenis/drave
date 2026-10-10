# Organisation du dépôt — quel dossier pour quoi

> Écrit le **2026-10-10 10:20 HAE** (EDT, UTC−4). Ce document est la **règle** : il dit ce qui va
> dans `docs/`, dans `reports/` et dans `journal/`, comment nommer, et comment horodater. Il
> existe parce que les trois dossiers étaient utilisés **en désordre** : des suivis d'avancement
> et des résultats de campagne dans `docs/`, des rapports de dizaines d'expériences dans un seul
> fichier de 179 Ko, et des **dates dans le futur** (jusqu'au 12 octobre 2026, alors que le travail
> s'est fait du 9 octobre 15 h 30 au 10 octobre 10 h 13).

---

## 1. `docs/` — le FOND

**Ce qui y va** : les principes, les théories, les hypothèses, les plans et les **roadmaps** de
chaque module, **l'état** d'un projet *par rapport à sa roadmap*, le glossaire, les registres
(manques), les conventions.

**Ce qui n'y va pas** : le récit d'une session, la liste des rounds, les résultats d'une
expérience. Un résultat mesuré est un `reports/`, un événement est un `journal/` ; `docs/` n'en
garde que la **conséquence** (« la capacité C6 est faite », avec le lien).

Nommage :

| préfixe | contenu | exemple |
|---|---|---|
| `plan-*.md` | ce qu'on projette de faire, avec ses portes mesurées | `plan-cerveau-complet.md` |
| `roadmap*.md` | la trajectoire d'un module | `roadmap-drave.md` |
| `etat-*.md` | **où on en est**, capacités faites / restantes, prochaine action | `etat-cerveau.md` |
| `note-*.md` | une idée courte, une piste, une réfutation | `note-cancellation-evenementielle.md` |
| `*-pour-drave.md` | un apport extérieur traduit pour le moteur | `biologie-pour-drave.md` |
| (sans préfixe) | un domaine : architecture, format, glossaire, conventions | `format-flux.md`, `manques.md` |

## 2. `reports/` — UNE EXPÉRIENCE PAR FICHIER

**Ce qui y va** : un fichier par expérience, avec **la question**, **le protocole**, **les
mesures**, **le verdict** (y compris négatif), et la **date réelle** du travail. Un rapport
négatif vaut un rapport positif : c'est ce qui empêche de refaire l'essai.

**Règle de taille** : si un fichier couvre plusieurs expériences, il devient un **dossier** —
`reports/<campagne>/` avec un **index** `reports/<campagne>.md` qui liste les fichiers et relie
chacun en une ligne (question → verdict). Le monolithe part en `reports/archive/`.

Nommage : `rapport-<sujet>.md` (une mesure), ou `reports/<campagne>/<NN>-<sujet>.md` (extrait
d'une campagne). Chaque fichier commence par un en-tête de quatre lignes :

```text
> Campagne : <nom> · expérience <NN>
> Question : ...
> Verdict : ... (une ligne, avec le chiffre)
> Date réelle : AAAA-MM-JJ HH:MM HAE (source : commit <hash>)
```

## 3. `journal/` — LES ÉVÉNEMENTS, DATÉS

**Ce qui y va** : ce qui s'est passé, **quand**, avec des **liens** vers les autres fichiers.
Une entrée par jour : `journal/AAAA-MM-JJ.md`. L'index `journal/README.md` est régénéré par
`tools/session_report.py` (sessions) — il ne se remplace pas à la main.

**Ce qui n'y va pas** : les résultats (un lien vers `reports/`), l'état consolidé (un lien vers
`docs/etat-*.md`). Une entrée de journal est **courte** : le fait, l'heure, le lien, et ce que ça
change pour la suite.

## 4. Le fuseau horaire — et l'erreur à ne pas refaire

**Règle** : tout horodatage est écrit en **heure locale de la machine**, notée **HAE** (heure
avancée de l'Est = `EDT`, `UTC−4`), au format `AAAA-MM-JJ HH:MM HAE`. La machine est en
`America/Montreal` sans `TZ` exporté ; `date` répond en EDT.

**L'erreur commise** : les documents de campagne portaient des estampilles **inventées** (« 10
octobre 18 h », « 11 octobre 6 h 45 », « 12 octobre 3 h ») — écrites en **avançant une horloge
supposée** au fil des rounds, jamais lues sur la machine. Résultat : des heures et des **jours
dans le futur**, et une chronologie qui n'existe pas. Ce n'est pas un décalage de fuseau (UTC
n'expliquerait que quatre heures) : c'est une **horloge fabriquée**.

**La source de vérité est git** : `git log --format='%ad %h %s' --date=format:'%m-%d %H:%M'`.
Le travail du sprint « cerveau » s'est fait du **2026-10-09 15 h 30** au **2026-10-10 10 h 13
HAE**, en 77 commits. Toute date d'un document doit pouvoir être **retrouvée dans git** ; sinon
elle s'écrit « date inconnue » — jamais une date plausible.

## 5. Ce que ça change pour la suite

À chaque round : (1) le fait et l'heure réelle dans le `journal/` du jour, avec liens ;
(2) la mesure dans un fichier `reports/` ; (3) la conséquence dans `docs/etat-*.md` ;
(4) `date` — jamais une horloge supposée.
