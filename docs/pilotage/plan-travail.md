# Le plan de travail — plusieurs sessions sur une même machine

> **Ce que ce document est.** Le **pont** entre l'état ([`en-cours.md`](en-cours.md), ce qui se
> passe maintenant) et l'ordre ([`roadmap.md`](roadmap.md), ce qu'il faut faire et dans quel
> ordre) : **qui fait quoi, dans quel territoire, à quelle cadence, et comment on surveille les
> fichiers qui bougent**. Il ne remplace ni l'un ni l'autre : l'état reste la source du présent,
> la roadmap la source de l'ordre.
>
> **Date** : 2026-11-02. **Machine** : une seule — 40 cœurs, 125 Go de RAM, 2 GPU de 16 Go,
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
| **N2 — le natif (session `0733c5bb`)** | entraîner et évaluer le modèle natif sur les corpus D, mesurer longueur, capacité, diversité | N2, N4, le mètre honnête | **GPU** (1 des 2), 8–16 cœurs | **N2.ac** (1 Go, 60 k pas) : **3,49 / 6,03** — production ; **200 k pas** : val_fr **3,16**, littérature **5,61**, anglais **7,28**, wikitext2 **8,00** (**< 2,5 non atteinte**) ; **R1.1/R1.2 mesurées** ; fiche + clôture en cours. |
| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **153/153** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** (POS **0,9415** / syntagmes **0,7539** / acte **1,0**) ; **DRVM/native** règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208)** (négation/modalité sous l'heuristique). Prochaine : **T132/T133**, **gold 200+**. |
| **S — les structures (session `29ad180d`)** | les structures d'interprétation candidates, la validation humaine/LLM, la banque | S, la pragmatique, l'export | **CPU**, 2–4 cœurs | **61/61** types, **144/144** rôles, **56 tests**, gold **60**, corpus **60**, banque **84/67**, **8 verdicts** ; **poursuivre la validation sur `/paragraphes`**, rétro-traduction API. |
| **D/R/A — terminé (02/11)** | les corpus (texte intégral, PDF/OCR, licences, stubs), la préparation de R1.1/R1.2, A2.6/A8.3 | D, R1, A2.6/A8.3 | **CPU/IO**, 4–16 cœurs | **OCR CEGEP 91 scans uniques (60 documents, 1 982 p, 4,41 M car.)** ; clôture le 02/11. Restent R1.1/R1.2 (N2) et A2.6 (A) ; les 8 scans `.PDF` sont une limite nommée. |

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
| **N2** | `data/corpus_propre/`, `data/corpus_litt_propre/`, `data/corpus_repo_propre/`, `data/corpus_*.txt`, `tools/corpus_propre.py`, `tools/eval_n2_propre.py`, `tools/distiller_budget.py`, `reports/n2-*`, `reports/rapport-n2-*`, `reports/corpus-propre.json`, `reports/corpus-litt-propre.json`, `reports/corpus-repo-propre.json`, `reports/corpus-wiki-propre.json`, `reports/corpus-multi-propre.json`, `data/wiki_fr/`, `data/wiki_multi/`, `tools/entrainer_native.py`, `work/n2d/`, `work/n2h/`, `work/n2i/`, `work/n2j/`, `work/n2k/`, `work/n2w/`, `models/` | `data/corpus_wiki_*`, `reports/corpus-wiki-*`, `reports/inventaire-*` |
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
deux mesures sur le même corpus se sérialisent. La passe complète réserve `machine` (§ 10) :
aucune autre réservation lourde ne tourne pendant ce temps.

**Le checkpoint d'intégration** : au moins une fois par jour, le hub relit les plans, met à jour
la roadmap et l'état, vérifie les compteurs et la revue, et note dans le journal ce qui a bougé.

## 5. Les règles de la machine partagée

- **GPU** : N2 seul sur un GPU ; le second GPU reste libre pour une évaluation ou un sous-agent
  (16 Go chacun : le 32 B et le professeur n'y tiennent pas).
- **CPU** : 2 à 3 gros travaux à la fois (un entraînement 8–16 cœurs, un OCR 1–2, une extraction
  PDF 4–8) ; 40 cœurs, mais la contention disque/compression est réelle. Les fils se réservent
  par socket (§ 10) : `cpu0` pour les GPU, `cpu1` pour le CPU seul.
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
| `python3 tools/sessions.py --check --strict` | plans complets, états connus, heartbeats < 45 min (hors `en pause`), **périmètres et fichiers réservés qui se recouvrent**, sessions de l'état sans plan | avant d'ouvrir une session, et au checkpoint |
| `python3 tools/surveille_sessions.py` | les **fichiers en mouvement** (`git status`) rangés par session, les **orphelins** et les **conflits** (un fichier réservé par deux sessions) | à chaque checkpoint, et avant un commit partagé |
| `python3 tools/verifie_etat_a_jour.py` | aucun fait commité sans ligne d'état | à chaque commit |
| `python3 tools/revue_documentation.py` | classement, liens, compteurs, fraîcheur | avant chaque commit de clôture |
| `python3 tools/verifie_journal.py` | les jours, les sessions, les liens | au checkpoint |
| `python3 tools/taille_documents.py` | les budgets de contexte (T0 ≤ 4 000) | avant chaque commit de clôture |
| `python3 tools/ressources.py --check` / `--actual` | le registre des ressources (GPU, CPU, RAM, NVMe, HDD) et les processus non déclarés | à chaque checkpoint et avant une passe |

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

1. **Ouvrir les sessions** : N2 (GPU, à ouvrir), L/B13 (reprise de `e181ce02`), S (structures, à ouvrir), D/R/A (reprise de `fe3c05f0`) ; chacune crée ou reprend son `journal/sessions/<id>/plan.md` (les onze champs), réserve son territoire (§ 3) et met à jour sa section dans `en-cours` **via le hub**.
2. **Vérifier** : `sessions.py --check --strict` (aucun recouvrement), `surveille_sessions.py` (les
   orphelins), `revue_documentation.py` (compteurs).
3. **Premier checkpoint** : le hub intègre les quatre sections, met à jour la roadmap et note le
   journal. Ensuite, chaque session suit la cadence du § 4.

## 9. Reprise après le reboot du 02/11 15 h 06 — ouvrir ou reprendre

**L'état au 03/11 18 h 45.** **N2** a clos sa phase (60 000 pas à 1 024 : **2,9121** ; **2,3911 /
2,3522** au grand corpus) mais un run tourne encore (`kd2-mix512-30k`) ; **S** a repris sur
l'**arbre des référents** ; **L/B13** publie sur l'**API** ; **D/R/A** est close. Le **plan de la
nuit** et les conflits évités sont au **§ 11** ; le hub `536cd5d6` tient l'état.

**Le principe.** Un terminal = une session = un `plan.md` = un territoire. Une seule session écrit
`en-cours` à la fois ; les autres **proposent** leur ligne au hub. Toutes les commandes se lancent
depuis la racine du dépôt.

**Les commandes.**

| besoin | commande |
|---|---|
| ouvrir une **nouvelle** session | `dsh --profile dsh-tui` (ou `dsh dsh-tui`) |
| **reprendre** une session | `dsh --profile dsh-tui --resume <id>` |
| voir les mandats | `python3 tools/sessions.py --status` |
| vérifier les mandats | `python3 tools/sessions.py --check --strict` |
| voir les fichiers en mouvement | `python3 tools/surveille_sessions.py` |

**Les quatre mandats, dans l'ordre de valeur.**

1. **N2 — le natif (GPU).** **Session `0733c5bb` ouverte.** Lire `AGENTS.md`, `en-cours`,
   `backlog/N2-distillation.md`. **200 k pas terminés** : val_fr **3,16**, littérature **5,61**,
   anglais **7,28**, wikitext2 **8,00** (**< 2,5 non atteinte**) ; **R1.1/R1.2 mesurées**.
   Prochaine action : **fiche + état + commit**, puis **clôture**.
2. **S — les structures (CPU).** **Session `29ad180d` ouverte.** Lire `docs/theorie/jeux-symboliques.md`
   et `tools/structures/`. **61/61** types, **144/144** rôles, **56 tests**, gold **60**,
   corpus **60**, banque **84/67**. Prochaine action : **poursuivre la validation sur
   `/paragraphes`**, rétro-traduction API ; le sous-module se commit **dans son dépôt** avant le pointeur.
3. **L/B13 — la langue et la pensée (CPU).** **Session `e181ce02` ouverte.** **153/153** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** qualifié (POS **0,9415**, syntagmes
   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208)** (négation/modalité sous l'heuristique). Prochaine action : **T132/T133**, **gold 200+**.
4. **D/R/A — les données (CPU/IO).** **Close le 02/11 à 18 h 45** : OCR du fonds CEGEP —
   **147 scans détectés** (91 uniques, 2 053 p), **60 documents, 1 982 p, 4,41 M car.**, 8 Ko 0 ;
   fiche [`ocr-cegep`](../../reports/rapport-ocr-cegep.md). Restent **R1.1/R1.2** (N2) et
   **A2.6** (A) ; les 8 scans `.PDF` (58 p) sont une limite nommée.

**Le premier prompt (à coller dans chaque terminal).**

> Tu es la session `<rôle>`. Lis `AGENTS.md`, `docs/pilotage/en-cours.md` et **seulement** le
> document de ta tâche. Crée (ou reprends) `journal/sessions/<id>/plan.md` avec les onze champs,
> réserve ton territoire, puis exécute la prochaine action nommée ci-dessus. Un fait = mesure +
> contrôle négatif + fiche + `en-cours` + commit (`git add` explicite). Ne touche pas à
> `en-cours`, `roadmap`, `chantiers`, `AGENTS` sans le hub. À la fin du cycle, rends ta ligne
> d'état et le hash du commit.

**Les pièges.**

- **Ne pas écrire `en-cours` à deux.** Le hook refuse un fait sans état, pas deux écrivains : c'est
  la discipline (ou le hub) qui évite la course.
- **`git add` explicite**, jamais `-A` : deux sessions sur le même arbre ; l'index alterné
  (`GIT_INDEX_FILE=/tmp/index.<session>`) est la ceinture. **Après un commit à index alterné,
  resynchroniser l'index principal** (`git read-tree HEAD`, sans toucher à l'arbre) : sinon
  l'index principal ignore les fichiers ajoutés et un `git add -A` d'une autre session les
  **supprime** — mesuré cette nuit : `tools/porte-ressources.sh` (82e porte) emporté par un
  commit B13, puis restauré.
- **Committer avant de rebooter** : le reboot du 02/11 a laissé 67 fichiers non committés.
- **Les portes lourdes une à une** ; les GPU sont partagés.
- **Une ressource se réserve** : `python3 tools/ressources.py --claim ...` (§ 10) ; un GPU, un
  NVMe ou une passe globale ne se partagent pas par accident.
- **Le sous-module `docwatch`** se commit dans son dépôt, puis le pointeur dans le superprojet.

**Quand une session finit.** Elle passe `État : terminé`, écrit sa `cloture.md` si le rapport
automatique ne dit pas ce qui est livré, et le hub la sort d'`en-cours` vers
`journal/sessions/`.


## 10. La coordination des ressources — le registre et le protocole

**Pourquoi.** Le pilotage réservait les **fichiers** (`sessions.py`) et surveillait les fichiers
en mouvement (`surveille_sessions.py`), mais pas la **machine** : deux sessions pouvaient lancer
deux entraînements sur le même GPU, ou saturer le même NVMe, sans le voir. Le registre
[`tools/ressources.py`](../../tools/ressources.py) rend les ressources explicites, les réserve
et met en file ce qui ne tient pas.

> **Consigne de nuit (02/11 20 h → 03/11 08 h).** Une session écrit `en-cours` à la fois ; tout
> job lourd **réserve** (`--claim`) et **libère** (`--release`) ; `--actual` à chaque checkpoint
> dénonce les usages non déclarés ; les tâches légères (portes doc, liens, compteurs, journal,
> backlog) remplissent les ressources libres ; la passe complète réserve `machine`. Chaque axe
> garde une **prochaine action** : aucun axe ne s'arrête pendant qu'un autre tourne.

### 10.1 Le modèle

| ressource | capacité | NUMA | règle |
|---|---|---:|---|
| `gpu0` | 1 job exclusif, 16 Gio | 0 | carte du haut (plafonnée 180 W par `hauru-thermal`) |
| `gpu1` | 1 job exclusif, 16 Gio | 0 | carte du bas ; libre pour une éval |
| `cpu0` | 16 fils utiles (20, réserve 4) | 0 | 0-9,20-29 ; **fils des GPU** |
| `cpu1` | 16 fils utiles (20, réserve 4) | 1 | 10-19,30-39 ; **CPU seul, hub** |
| `ram` | 109 Gio utiles (125, réserve 16) | — | un job > 80 Gio est machine-exclusif |
| `nvme_system` | 1 IO lourde, 705 Gio libres | — | `/`, `/home`, `/FastNVMe` (attention : `FastNVMe` est sur le système, pas le RAID) |
| `nvme_raid` | 1 IO lourde, **33 Gio libres** | — | `/home/stephane/IA` (RAID0 4×238 G) — presque plein |
| `hdd_data13tb` | 1 IO lourde, 1,9 Tio | — | `/home/stephane/Data13TB` (corpus, OCR) |
| `machine` | 1 job exclusif | — | passe complète des portes / mesure globale |

### 10.2 La règle NUMA

Les deux GPU sont sur le **node 0** (`nvidia-smi topo -m`) ; le node 1 est libre pour le CPU seul.

```bash
# job GPU : fils et mémoire sur le node 0
numactl --cpunodebind=0 --membind=0 <commande>
CUDA_VISIBLE_DEVICES=0 <commande>        # ou 1, ou 0,1

# job CPU seul : node 1
numactl --cpunodebind=1 --membind=1 <commande>
```

Un job GPU qui réserve `cpu1` est signalé : ses fils doivent aller sur `cpu0`.

### 10.3 Le protocole

Avant une étape lourde (entraînement, OCR, extraction, passe de portes, gros téléchargement) :

```bash
python3 tools/ressources.py --claim --session <id> --job <nom> \
  --res "gpu0=exclusive,cpu0=12,ram=60,nvme_raid=heavy:20" --prio 1 --eta 240
```

- **✅ accordé** : la ressource est libre, le job peut démarrer.
- **⏸ différé** : le claim est **mis en file** ; la session prend une autre tâche (la file est
  admise automatiquement à la libération). C'est la règle « jamais en attente » : on ne bloque
  pas, on change de tâche.
- Après le job : `python3 tools/ressources.py --release --session <id> [--job <nom>]`.
- À chaque checkpoint : `--status` (qui tient quoi), `--check` (cohérence), `--suggest` (ce qui
  est libre), `--actual` (le réel : processus GPU non déclarés, top CPU, espace disque).

### 10.4 L'allocation type

| session | ressources | lancement |
|---|---|---|
| **N2** | `gpu0` excl., `cpu0` 12, `ram` 60, `nvme_raid` heavy:20 | node 0 |
| **L/B13** | `cpu1` 8, `ram` 16 | node 1 |
| **S** | `cpu1` 4, `ram` 8 | node 1 |
| **D/R/A** | `cpu1` 2, `ram` 16, `hdd_data13tb` heavy | node 1 (OCR) |
| **hub** | `cpu1` 2, `ram` 4 | node 1 |
| **passe complète** | `machine` exclusive | — (rendez-vous) |

`cpu1` = 8 + 4 + 2 + 2 = **16 fils** (le maximum utile) ; `ram` = 104 Gio ; `gpu1` reste libre
pour une éval. La passe complète **réserve `machine`** : elle attend que les sessions libèrent
leurs claims ; le hub annonce la fenêtre, les sessions `release`, la file admet `machine`.

### 10.5 Le stockage

- `IA` (RAID) est à **33 Gio** : un claim `nvme_raid=heavy:20` vérifie l'espace ; un claim de
  40 Gio est refusé. Les nouveaux gros corpus/checkpoints vont sur `hdd_data13tb` (1,9 Tio) ou
  `nvme_system` (705 Gio), pas sur `IA`.
- **Une seule IO lourde par dispositif.** Une IO lourde sur `nvme_system` est déconseillée
  (OS, dépôt, bureau) ; l'outil l'avertit.
- `FastNVMe` est un sous-volume du NVMe système, **pas** du RAID : ne pas s'y tromper.

### 10.6 Le registre et la vérification

- Le registre vit dans `work/ressources.json` (ignoré par git) ; la politique est ici ; le code
  est [`tools/ressources.py`](../../tools/ressources.py) (`--autotest` : 9 cas).
- `--actual` compare le registre au réel : un GPU utilisé sans claim est signalé (aujourd'hui
  `llama-server` et les processus N2 sont **non déclarés**).
- **Application dure** (à venir) : `systemd-run` avec `AllowedCPUs`, `IOWeight`, `MemoryMax` et
  `CUDA_VISIBLE_DEVICES`, ou des slices par ressource. Le registre est **consultatif** ; il
  n'empêche pas un job, il rend le conflit visible.
- Une **porte** `porte-ressources.sh` (`--check --strict`) pourra être ajoutée après validation :
  elle ferait passer le compte de 81 à 82 portes, et les compteurs de l'état suivraient.


### 10.7 La nuit du 02/11 → 03/11 (08 h)

**Consigne.** Les quatre sessions actives restent productives jusqu'à 08 h ; aucune n'attend.
Les claims actifs (02/11 20 h) :

| session | claim | remarque |
|---|---|---|
| N2 `0733c5bb` | `gpu0`, `cpu0` 12, `ram` 60 | R1.2-1024 en cours ; node 0 |
| hub `536cd5d6` | `gpu1`, `cpu1` 8, `ram` 8 | passe de portes ; node 1 |
| S `29ad180d` | `cpu1` 4, `ram` 8 | homographes/lexique, h033, gold |
| Pensée `e181ce02` | `cpu1` 4, `ram` 16 | gold 200+, porte mobile |
| D/R/A `fe3c05f0` | close | place `cpu1` 2 libre si on la rouvre |

**La passe complète en cours** (`work/portes/passe-1102-19h32`, lancée 19 h 32 avec
`CUDA_VISIBLE_DEVICES=1,0`) est une **exception** : elle partage GPU0 avec N2 (ralentissement
assumé) et doit finir. Les passes suivantes : partielles sur `gpu1` + `cpu1` ; complètes sur
`machine` exclusive, après libération de N2/S/Pensée. Le hub suit `registre.txt` et `--actual`.

**Le hub** : `--status` / `--actual` / `--check` du registre, `sessions.py --status`,
`surveille_sessions.py`, `git status` ; intégration des fiches B13/N2/S, état/roadmap, INDEX,
références de non-régression ; heartbeat à chaque cycle. **Les sessions** : `--release` en fin
de job, `--claim` du suivant ; si une action attend l'humain (validation S), prendre la ligne
suivante. **Checkpoint 08 h** : registre, sessions, `git log`, verdict de la passe, bilan.

## 11. La nuit du 03/11 → 04/11 — le plan, et les conflits qu'il évite

**L'état au 03/11 18 h 45.** **N2** a clos sa phase (60 000 pas à 1 024 : **2,9121** ; **2,3911 /
2,3522** au grand corpus ; distillation native **+0,10** à budget égal — **erratum 04/11** : pas de gain à parité stricte, le +0,14–0,18 était une repondération) mais **un run tourne
encore** (`kd2-mix512-30k`, les deux GPU à 100 %, fin vers 22 h 40). **S** a repris à 13 h 55 sur
l'**arbre des référents** ; **L/B13** publie (fusion réparée sur l'API, **/35**) ; **D/R/A** est
close. Le **roster** de la nuit : N2 (GPU), S (CPU), L/B13 (CPU + API), le hub (pilotage).

**Qui fait quoi, avec quoi, et quand il s'arrête.**

| session | territoire | tâche de la nuit | ressource | livrable | arrêt |
|---|---|---|---|---|---|
| **N2** `0733c5bb` | `reports/n2-*`, `work/n2ac/`, `data/` | finir `kd2`, mesurer et committer ; puis le **contrôle depuis zéro** et la **clôture** ; ensuite **la porte propre (0,29)** | `gpu0`+`gpu1` exclusifs (fin du run), `cpu0` 12, `ram` 60 | fiche + JSON + état + commit | run fini, fiche committée, ou limite nommée |
| **S** `29ad180d` | `tools/structures/`, `docs/schemas/arbre-referents.svg`, `reports/s-*` | **v6** (h050, h053, « si fort que » fermés, gold 60) ; la **validation des paragraphes** sur `/paragraphes` ; la **rétro-traduction** API | `cpu1` 4, `ram` 8 | fiches + tests verts + commit | validation faite ou report nommé |
| **L/B13** `e181ce02` | `tools/pensee/`, `reports/pensee-*`, `docs/theorie/pensee-*` | **porte stochastique/fenêtre** (test faible), **gold 200+**, **T132/T133** ; professeurs par l'**API** | `cpu1` 4, `ram` 16 | fiches + commit | porte franchie ou négatif nommé |
| **hub** `536cd5d6` | `docs/pilotage/`, `journal/` (hors sessions), `reports/README.md`, `reports/INDEX.md`, ``tools/sessions.py`, `tools/ressources.py`, `tools/index_reports.py`, `tools/surveille_sessions.py`` | tenir l'**état** (un écrivain à la fois), intégrer chaque fait, surveiller heartbeats et claims ; **passe complète** quand les GPU sont libres ; **bilan 08 h** | `cpu1` 1, `ram` 1 | état/roadmap/journal à jour ; verdict de passe | bilan de 08 h écrit et committé |

**Les conflits, et comment ils sont évités.**

- **GPU** : N2 **seul** sur les deux cartes jusqu'à la fin du run ; S, L et le hub n'y touchent
  pas. La **passe** attend que N2 rende les cartes — ou tourne sur `gpu1` seule si N2 n'en tient
  qu'une (dérogation de [`portes.md`](../methode/portes.md)).
- **État** : le hub `536cd5d6` tient le tour d'écriture ; les autres **proposent** leur ligne
  (fait + chiffre + fiche + JSON) et ne touchent pas `en-cours`/`roadmap`/`chantiers`.
- **Fichiers** : S seule sur `docs/schemas/arbre-referents.svg` et `reports/s-*` ; L seule sur
  `tools/pensee/` ; N2 seule sur `reports/n2-*` et `work/n2ac/` ; le hub ne prend que ses
  fichiers réservés. Un fichier hors territoire se **signale**, ne se corrige pas en silence.
- **Professeur** : **API DeepSeek** uniquement (`DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key`) ;
  aucun `llama-server`/`ollama` (règle 11, `hauru-gpu-guard`, `porte-ressources`).
- **Claims** : le hub a **pré-enregistré l'allocation de la nuit** dans le registre — N2
  `nuit-kd2` (`gpu0`+`gpu1` exclusifs, `cpu0` 12, `ram` 60), S `nuit-arbre` (`cpu1` 4, `ram` 8),
  L `nuit-l` (`cpu1` 4, `ram` 16), hub `nuit-hub` (`cpu1` 1, `ram` 1) ; chaque session **ajuste**
  (`--release`/`--claim`) au fil des jobs. Le run `kd2` tournait sans claim : il est désormais
  déclaré sous N2.
- **Disque** : `IA` à **33 Gio** — aucun nouveau gros modèle ; corpus et checkpoints sur `Data13TB`.

**La cadence.** Un cycle = un fait mesuré + fiche + JSON + ligne d'état **proposée** + commit.
Checkpoints du hub : **22 h**, **00 h**, **04 h**, **08 h** (bilan). Une session qui attend
l'humain prend la ligne suivante : on ne bloque jamais. **Le bilan de 08 h** tient en quatre
lignes : ce que chaque session a livré (fiche + commit), le verdict de la passe si elle a tourné,
les claims réels, et ce qui attend l'humain (validation S, clé API déjà fournie).

## 12. La reprise du 04/11 — le suivi documentaire

La nuit du 03/11 a été interrompue par le reboot de 19 h 33 (deux runs sans checkpoint). Le
04/11, le hub `1e7ef596` a rouvert l'état, relancé `kd2`/`rope2048` (09 h 30) et trois sessions
ont repris (N2 09 h 41, S 09 h 46, L/B13 10 h 14) ; **N3** a clos sa ligne en session courte
(11 h 30–11 h 38). Le suivi docs tourne à chaque cycle : `revue_documentation.py`,
`verifie_en_cours.py`, `taille_documents.py`, `verifie_journal.py`, `verifier_liens.py`,
`porte-tableaux.sh` ; la **passe complète** attend la fin des runs (règle § 11).
