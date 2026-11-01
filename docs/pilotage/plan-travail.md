# Le plan de travail — plusieurs sessions sur une même machine

> **Ce que ce document est.** Le **pont** entre l'état ([`en-cours.md`](en-cours.md), ce qui se
> passe maintenant) et l'ordre ([`roadmap.md`](roadmap.md), ce qu'il faut faire et dans quel
> ordre) : **qui fait quoi, dans quel territoire, à quelle cadence, et comment on surveille les
> fichiers qui bougent**. Il ne remplace ni l'un ni l'autre : l'état reste la source du présent,
> la roadmap la source de l'ordre.
>
> **Date** : 2026-11-01. **Machine** : une seule — 40 cœurs, 125 Go de RAM, 2 GPU de 16 Go,
> 2,0 To libres sur `Data13TB`, 34 Go sur `IA`. **Capacité** : voir
> [`chantiers.md`](chantiers.md) § 8 (4 sessions, 4 à 6 chantiers, 2 à 4 sous-agents par session).
>
> **Chargement** : ce document avant d'ouvrir une session ; puis la fiche du chantier.

## 1. Où ce plan se situe

```
en-cours.md          ce qui se passe maintenant (état court, une section par session active)
plan-travail.md      qui fait quoi, où, à quelle cadence (ce document)
roadmap.md           l'ordre des chantiers et leur état
chantiers.md         les relations entre les chantiers, la vision, la capacité
backlog/             les contrats par fonctionnalité
```

L'état se lit en premier ; le plan dit **comment le travail se répartit** ; la roadmap dit
**dans quel ordre** ; `chantiers.md` dit **pourquoi les morceaux tiennent ensemble**. Un fait ne
se commit qu'avec sa ligne d'état (hook `verifie_etat_a_jour.py`) ; une session ne s'ouvre
qu'avec un plan (`journal/sessions/<id>/plan.md`) et un territoire réservé.

## 2. Les quatre sessions et le rôle d'intégration

Quatre sessions **de mandat** et **un rôle d'intégration** (porté par la session de pilotage ou
tournant à chaque checkpoint). Chaque session a un mandat long, un territoire, et 2 à 4
sous-agents pour les tâches bornées.

| session | mandat | chantiers | charge | prochaine action |
|---|---|---|---|---|
| **N2 — le natif** | entraîner et évaluer le modèle natif sur les corpus D, mesurer longueur, capacité, diversité | N2, N4, le mètre honnête | **GPU** (1 des 2), 8–16 cœurs | N2 sur les corpus wiki fr/en ; le verrou 129→512 ; la capacité |
| **L — la langue et la pensée** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | le contrat/bloc (**398 langues**), AC-3/alpha-bêta, le DRVF et le banc sont faits ; gold/neuronal ; opérateurs B13 |
| **S — les structures** | les structures d'interprétation candidates, la validation humaine/LLM, la banque | S, la pragmatique, l'export | **CPU**, 2–4 cœurs | l'analyseur plus riche (rôles, subordonnées), l'export vers le corpus |
| **D/R/A — les données, le lecteur, le moteur** | les corpus (texte intégral, PDF/OCR, licences, stubs), la préparation de R1.1/R1.2, A2.6/A8.3 | D, R1, A2.6/A8.3 | **CPU/IO**, 4–16 cœurs | le texte intégral des 10 corpus, l'extraction PDF/OCR, la prépa R1 |

**Le rôle d'intégration** (le « hub ») : tient `en-cours`, `roadmap`, `chantiers`, ce plan,
`journal/`, `reports/INDEX.md`, `AGENTS.md`, les compteurs et la revue de documentation. Il ne
code pas un chantier ; il **intègre** les sections des sessions, met à jour les compteurs, vérifie
les portes et commite. Il est **un seul à la fois** (voir § 4).

**Les sous-agents** : 2 à 4 par session, sur des tâches **bornées** (une mesure, un outil, une
fiche, un audit) ; ils ne touchent ni `en-cours`, ni la roadmap, ni `AGENTS.md` ; ils rendent un
diff que la session intègre (AGENTS § 10, `continuite.md` § 2). Le fan-out massif (`workflow`) est
réservé aux **audits en lecture seule**.

## 3. Les territoires — qui écrit quoi

**Un fichier n'a qu'un écrivain à la fois.** Les réservations sont des globs ; elles se déclarent
dans le plan de chaque session et se vérifient par `tools/sessions.py --check`.

| session | réservé (écriture) | lit (sans écrire) |
|---|---|---|
| **N2** | `data/corpus_propre/`, `data/corpus_litt_propre/`, `data/corpus_repo_propre/`, `data/corpus_*.txt`, `tools/corpus_propre.py`, `tools/eval_n2_propre.py`, `tools/distiller_budget.py`, `reports/n2-*`, `reports/rapport-n2-*`, `reports/corpus-propre.json`, `reports/corpus-litt-propre.json`, `reports/corpus-repo-propre.json`, `reports/corpus-wiki-propre.json`, `reports/corpus-multi-propre.json`, `data/wiki_fr/`, `data/wiki_multi/`, `tools/entrainer_native.py`, `work/n2d/`, `work/n2h/`, `work/n2i/`, `work/n2j/`, `work/n2k/`, `models/` | `data/corpus_wiki_*`, `reports/corpus-wiki-*`, `reports/inventaire-*` |
| **L** | `docs/theorie/pensee-iterative.md`, `docs/theorie/pre-traitement-linguistique.md`, `docs/implantation/moteur-de-pensee.md`, `docs/implantation/bloc-linguistique.md`, `tools/pensee/`, `reports/pensee-*`, `reports/r44-*`, `docs/schemas/pensee-*.svg`, `docs/schemas/heuristique-*.svg`, `journal/sessions/<id>/` | les corpus D, les fiches S, `reports/r44-*` (clos) |
| **S** | `tools/structures/` (sous-module), ses exports et sa banque (à préciser dans son plan), `journal/sessions/<id>/` | `docs/theorie/pre-traitement-linguistique.md`, les corpus D |
| **D/R/A** | `data/wikipedia/` (lecture seule), `data/corpus_wiki_*`, `tools/corpus_wikipedia.py`, `tools/verifie_contamination.py`, `tools/catalogue_corpus.py`, `reports/corpus-wiki-*`, `reports/corpus-wikipedia-*`, `reports/inventaire-*`, `reports/rapport-corpus-*`, `reports/corpus-wiki-*texte*`, `data/corpus_wiki_*_texte/`, `tools/corpus_wikipedia_texte.py`, `reports/r11-*`, `reports/r12-*`, `reports/a26-*`, `reports/a83-*`, `journal/sessions/<id>/` | `reports/n2-*` (les résultats N2), `reports/pensee-*` |
| **hub** (intégration) | `docs/pilotage/en-cours.md`, `roadmap.md`, `chantiers.md`, `plan-travail.md`, `README.md`, `journal/` (hors `sessions/<id>/`), `reports/INDEX.md`, `AGENTS.md`, `tools/surveille_sessions.py`, `tools/carte_chantiers.py` | tout le reste |

**Les fichiers partagés, et leur règle.** `en-cours.md`, `roadmap.md`, `AGENTS.md`,
`reports/INDEX.md` et `journal/` ne s'écrivent que par **le hub**, à la demande des sessions (leur
section, leur fait, leurs compteurs). Les sessions **proposent** : leur section est déjà dans leur
plan, elles la remettent au hub au checkpoint ; le hub l'intègre et commite. Si une session doit
écrire elle-même sa ligne d'état (parce qu'elle commite un fait), elle le fait **hors de la
fenêtre d'intégration** et le hub relit après — c'est la règle « un écrivain à la fois ».

**Le partage de `data/`** : N2 écrit les corpus préparés qu'il utilise (`corpus_propre`,
`corpus_litt_propre`, `corpus_repo_propre`, `corpus_*.txt`) ; D écrit les **nouveaux** corpus
(`corpus_wiki_*`) et leurs manifestes. N2 **lit** les seconds, ne les modifie pas ; D **lit** les
premiers, ne les modifie pas. Les manifestes `reports/corpus-*` suivent la même règle.

## 4. La cadence et l'écriture de l'état

**Un round** = une session travaille jusqu'à un **checkpoint** : un fait mesuré, une fiche, un
JSON, un commit, la ligne d'état à jour, le heartbeat et la prochaine action dans son plan.

**Le tour d'écriture de l'état.** Une seule session écrit `en-cours`/`roadmap`/les compteurs à la
fois :

1. la session prépare son **bloc** (section, fait, compteurs) et le remet au hub (ou l'écrit si
   elle est le hub) ;
2. le hub relit la revue (`revue_documentation.py`), corrige les compteurs, met à jour la
   roadmap, commite ;
3. les autres sessions ne touchent pas ces fichiers pendant le tour ; elles continuent leur
   chantier et préparent leur bloc.

**Le commit.** Petits et fréquents ; `git add` **explicite** ; pour un commit qui touche des
fichiers partagés, l'**index alterné** (`GIT_INDEX_FILE=/tmp/index.<session> git read-tree HEAD`
puis `git add` des seuls fichiers de la session) évite d'embarquer les modifications des autres ;
en cas de course (`cannot lock ref 'HEAD'`), **relire HEAD, refaire l'index, recommiter** — jamais
de `git reset` sur les fichiers d'une autre session.

**La mesure.** Les portes lourdes (`porte-ocr-scans`, `toutes-les-portes`) tournent **une à la
fois** ; les portes légères (doc, état, journal) à chaque commit. Le banc R03 est en lecture ;
deux mesures sur le même corpus se sérialisent.

**Le checkpoint d'intégration** : au moins une fois par jour, le hub relit les plans, met à jour
la roadmap et l'état, vérifie les compteurs et la revue, et note dans le journal ce qui a bougé.

## 5. Les règles de la machine partagée

- **GPU** : N2 seul sur un GPU ; le second GPU reste libre pour une évaluation ou un sous-agent
  (16 Go chacun : le 32 B et le professeur n'y tiennent pas).
- **CPU** : 2 à 3 gros travaux à la fois (un entraînement 8–16 cœurs, un OCR 1–2, une extraction
  PDF 4–8) ; 40 cœurs, mais la contention disque/compression est réelle.
- **Disque** : `Data13TB` a 2,0 To ; `IA` est à **34 Go libres** — **aucun nouveau gros modèle**
  sans supprimer (le DeepSeek 341 Go et les artefacts 122 Go sont les postes à revoir). Les
  `work/` de session restent dans `work/<session>/`, jamais à la racine.
- **Fichiers en mouvement** : chaque session travaille dans son territoire, et **surveille**
  (§ 6) ; un fichier hors territoire est signalé au hub, pas « corrigé » en silence.
- **Le hook** : aucun fait (`reports/`, `tools/`, roadmap, backlog) ne se commit sans sa ligne
  d'état ; la revue de documentation et `taille_documents.py` passent avant chaque commit de
  clôture.

## 6. La surveillance

| outil | ce qu'il vérifie | quand |
|---|---|---|
| `python3 tools/sessions.py --check` | plans complets, états connus, heartbeats < 45 min, **périmètres et fichiers réservés qui se recouvrent**, sessions de l'état sans plan | avant d'ouvrir une session, et au checkpoint |
| `python3 tools/surveille_sessions.py` | les **fichiers en mouvement** (`git status`) rangés par session, les **orphelins** et les **conflits** (un fichier réservé par deux sessions) | à chaque checkpoint, et avant un commit partagé |
| `python3 tools/verifie_etat_a_jour.py` | aucun fait commité sans ligne d'état | à chaque commit |
| `python3 tools/revue_documentation.py` | classement, liens, compteurs, fraîcheur | avant chaque commit de clôture |
| `python3 tools/verifie_journal.py` | les jours, les sessions, les liens | au checkpoint |
| `python3 tools/taille_documents.py` | les budgets de contexte (T0 ≤ 4 000) | avant chaque commit de clôture |

**Ce que « surveiller » veut dire ici** : le dépôt est **un seul arbre de travail** ; deux
sessions qui écrivent le même fichier se marchent dessus sans le voir. Les réservations et
`sessions.py` empêchent le recouvrement **déclaré** ; `surveille_sessions.py` montre le
recouvrement **réel** (les fichiers qui bougent). Un orphelin n'est pas une faute : c'est un
fichier qu'aucune session active ne réclame — le hub décide (l'attribuer, le commiter, le
supprimer).

## 7. La balance, et les bascules

- **La charge** : 1 session GPU, 3 sessions CPU, 2 à 4 sous-agents par session ; l'humain sur S,
  le contrat de L et la pragmatique. C'est la configuration qui maximise le **validé**, pas le
  produit brut.
- **La bascule** : quand une session finit (ou s'arrête), son territoire est repris par le hub ou
  la session la moins chargée ; la roadmap marque l'état ; le plan de la session close reste
  lisible (archive).
- **La file** : si un chantier est bloqué (B10.3, A3.4, A5.4, A6.2, R2/R3/R5), on prend la
  **suivante** de la frontière (§ 6 de `chantiers.md`) — jamais d'attente.
- **Le plafond** : au-delà de 5 sessions ou de 4 sous-agents par session, la coordination
  (état, git, revue, relecture humaine) coûte plus qu'elle ne rapporte.

## 8. La mise en route

1. **Ouvrir les sessions** : N2 (GPU), L (Pensée), S (structures), D/R/A ; chacune crée son
   `journal/sessions/<id>/plan.md` (les onze champs), réserve son territoire (§ 3) et met à jour
   sa section dans `en-cours` **via le hub**.
2. **Vérifier** : `sessions.py --check` (aucun recouvrement), `surveille_sessions.py` (les
   orphelins), `revue_documentation.py` (compteurs).
3. **Premier checkpoint** : le hub intègre les quatre sections, met à jour la roadmap et note le
   journal. Ensuite, chaque session suit la cadence du § 4.
