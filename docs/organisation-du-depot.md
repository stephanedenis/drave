# Organisation du dépôt — quel dossier pour quoi

> Écrit le **2026-10-10 10:20 HAE** (EDT, UTC−4). Ce document est la **règle** : il dit ce qui va
> dans `docs/`, dans `reports/` et dans `journal/`, comment nommer, et comment horodater. Il
> existe parce que les trois dossiers étaient utilisés **en désordre** : des suivis d'avancement
> et des résultats de campagne dans `docs/`, des rapports de dizaines d'expériences dans un seul
> fichier de 179 Ko, et des **dates dans le futur** (jusqu'au 12 octobre 2026, alors que le travail
> s'est fait du 9 octobre 15 h 30 au 10 octobre 10 h 13).

---

## 0. Les points d'entrée (ce qu'on lit en arrivant)

| fichier | rôle | taille visée |
|---|---|---|
| `README.md` | ce qu'est Drave, trois commandes, **où est quoi** (tableau) | ~60 lignes |
| `REPRISE.md` | la **check-list de démarrage** : quoi lire, quoi vérifier, les pièges, où écrire | ~90 lignes |
| `docs/etat.md` | l'**index des modules** : roadmap → état → prochaine action | ~60 lignes |
| `docs/references-non-regression.md` | les **repères chiffrés** (ce qui ne doit pas bouger) | ~60 lignes |
| `journal/AAAA-MM-JJ.md` | la **journée en cours**, par thème | — |

**Règle** : ces fichiers **renvoient**, ils ne recopient pas. Un détail mesuré va dans
`reports/`, un principe dans `docs/`, un fait daté dans `journal/`. Deux fichiers d'entrée de
709 et 1 828 lignes ont été allégés le 2026-10-10 pour cette raison (versions longues conservées
dans `journal/`, voir `journal/2026-10-10-reprise-historique.md`).

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

## 3. `journal/` — LES ÉVÉNEMENTS, DATÉS, PAR JOUR ET PAR THÈME

**Ce qui y va** : ce qui s'est passé, **quand**, avec des **liens** vers les autres fichiers.
Une journée de ce dépôt ne tient pas dans un fichier — elle touche le moteur, les protocoles,
les mesures, les portes et la documentation — donc **chaque jour est découpé par thème** :

| fichier | rôle |
|---|---|
| `journal/AAAA-MM-JJ.md` | l'**index du jour** : les thèmes, tous les commits, les sessions, et le **récit écrit à la main** (bloc « notes », préservé) |
| `journal/AAAA-MM-JJ_<thème>.md` | les **commits du jour de ce thème**, les titres de tour de session qui s'y rattachent, les mesures touchées |
| `journal/sessions/<id>/` | les rapports de session (automates, `tools/session_report.py`) |
| `journal/AAAA-MM-JJ-<récit>.md` | une pièce longue écrite à la main (ex. le récit du sprint) |
| `journal/README.md` | l'index général : les journées (index + thèmes) et les sessions — **régénéré**, ne pas éditer |

Le nom commence par la **date** et finit par le **thème** : `ls journal/2026-10-1*_attention.md`
suit un thème d'un jour à l'autre.

**C'est automatisé** (`tools/journal_auto.py`, appelé par le `pre-commit`) : les commits du jour
viennent de **git** (heure d'auteur, en HAE), les sessions actives de `journal/README.md`, et les
**étapes du jour** — les lignes `⏵ …` que l'agent écrit dans le journal de session pour dire ce
qu'il fait, tour par tour — sont reprises dans le thème correspondant : c'est le détail riche,
classé, sans recopier la conversation. Titres de tour et liens vers les rapports complets
complètent chaque fichier. Les thèmes sont attribués par mots-clés du sujet et par
chemins touchés (liste dans le script : `tools/journal_auto.py --lister`). **Tout ce qui est
écrit à la main dans le bloc « notes » est conservé** d'une génération à l'autre — le reste est
régénéré, donc on n'écrit pas en dehors du bloc.

**Ce qui n'y va pas** : les résultats (un lien vers `reports/`), l'état consolidé (un lien vers
`docs/etat-*.md`).

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

**Deuxième occurrence, le jour même (2026-10-10).** La règle ci-dessus a été écrite le matin et
**enfreinte l'après-midi** : des fiches ont porté 16:50, 17:55, 18:35, 19:00 alors que l'horloge
disait 15:54 — jusqu'à **3 h 06 d'avance**, parce que les heures étaient **estimées** au fil du
travail au lieu d'être lues. Corrigé en prenant l'heure du **commit** qui a écrit chaque document
(`git log --diff-filter=A --format=%ad`), et la leçon est précisée : **une estampille s'écrit
APRÈS un appel à `date`, ou se prend dans git** ; si l'heure n'est pas disponible, on écrit
« heure inconnue » — c'est toujours mieux qu'une heure plausible.

## 5. Ce que ça change pour la suite

À chaque round : (1) le fait et l'heure réelle dans le `journal/` du jour, avec liens ;
(2) la mesure dans un fichier `reports/` ; (3) la conséquence dans `docs/etat-*.md` ;
(4) `date` — jamais une horloge supposée.
