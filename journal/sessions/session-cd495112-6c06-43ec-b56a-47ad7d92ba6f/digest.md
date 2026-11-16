# Session DSH — relecture

- identifiant : `session-cd495112-6c06-43ec-b56a-47ad7d92ba6f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 23:43:43
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche U1 (exploitable, suite de T4) : **répare les deux points O(k²)** identifiés par T4 — `_groupes_partition` (toutes les paires de syntagmes) et `_cible_proche` (le tri de tous les GV pour chaque segment) — **sans changer les résultats** (les 612 phrases et le réel 452 : les mêmes F1, attachement, POS, au bit près) ; mesure le **α** de la croissance avant/après sur le bloc contrôlé de T4 (l'objectif : α ≤ 1,15 et le terme quadratique non significatif), le temps sur 10 000 mots, la mémoire ; le **contrôle négatif** : les sorties identiques (un diff du JSON avant/après doit être vide). Fiche `reports/rapport-performance-fix.md` + JSON, tests, commit.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/methode/`](docs/methode/)
> (tableau § 3). L'**état courant** est dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; la **roadmap** dans
> [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; le récit daté dans [`journal/`](journal/).

## 1. La vision (l'essentiel)

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le principe : la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. L'approche par **bus d'événements** rend chaque bloc fonctionnel optimisable, comparable et substituable (neuronal là où l'intuition aide, computationnel là où la fiabilité prime).

Né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de les
**combiner**, de les **décomposer** en couches et grappes exécutables par du matériel divers, voire **distribué
en réseau**, de les **diagnostiquer** en étudiant leurs **flux**, et de **rejouer** des événements.


## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/methode/rangement.md`](docs/methode/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/pilotage/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B… / N… / R…). *Sans contrôle négatif, ce n'est pas un
   résultat.* → [`docs/methode/resultats.md`](docs/methode/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   tolérées : **celles listées dans [`docs/pilotage/references-non-regression.md`](docs/pilotage/references-non-regression.md)** ; toute autre est une régression. →
   [`docs/methode/portes.md`](docs/methode/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/methode/rangement.md`](docs/methode/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/theorie/genealogie-des-langues.md`](docs/theorie/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/methode/miroir.md`](docs/methode/miroir.md)
7. **La roadmap** ([`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)) : chaque chantier a une **prochaine action** ; l'ordre est la **valeur** et les **dépendances**, jamais une date. Un chantier est **fini** quand il est
   mesuré, écrit et committé ; il est **marqué**, et le suivant désigné.
8. **Ne jamais bloquer, ne jamais rester en attente** : une question humaine se **consolide** dans `en-cours` et on **continue** ; si une ligne est bloquée (corpus, compte, matériel), on prend la suivante
   — la **file « jamais en attente »** de la roadmap. → [`docs/methode/ressources.md`](docs/methode/ressources.md)
9. **Les illustrations sont des SVG.** Aucun **ASCII art** dans un bloc de code. Un schéma est un
   **`.svg`** — direct, ou généré par **docwatch** depuis `.mmd`/`.puml` (l'image pointe vers
   `<source>.svg`) — avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
   `docs/schemas/` ou `docs/theorie/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
   → [`docs/methode/illustrations.md`](docs/methode/illustrations.md)
10. **Pilotage : cycles longs, sous-agents, état unique.** Un goal par programme (`max_goal_rounds`
    1 000) ; on s'arrête sur un résultat mesuré, écrit, committé, ou un blocage. Les tâches
    indépendantes : **sous-agents** (2–4), sans toucher `en-cours`/`roadmap`/`AGENTS` ; ils
    rendent un **diff**. **État** : une session écrit `en-cours` à la fois ; aucun fait
    sans sa ligne (hook `verifie_etat_a_jour.py`). Git : `git add` explicite. La clôture met `en-cours` à jour (≤ 2 000 mots).
    → [`docs/methode/continuite.md`](docs/methode/continuite.md)

11. **Les GPU sont exclusivement réservés à Drave** ; les **professeurs** passent par l'**API
    DeepSeek** (`tools/llm/enseignant.py`), jamais par un serveur local (`llama-server`,
    `ollama`). Garde-fous : `hauru-gpu-guard` (timer 30 s), `porte-ressources` (contrôle GPU).
    → [`docs/methode/ressources.md`](docs/methode/ressources.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/theorie/vision.md`](docs/theorie/vision.md) |
| la **roadmap** (A/B/N/R, l'ordre, la file « jamais en attente ») | [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) |
| **la lecture rapide** et son backlog (techniques, couches, fiches) | [`docs/theorie/lecture-rapide.md`](docs/theorie/lecture-rapide.md) · [`docs/pilotage/backlog/index.md`](docs/pilotage/backlog/index.md) |
| comprendre la mission et les priorités | [`docs/methode/mission.md`](docs/methode/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/methode/resultats.md`](docs/methode/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/methode/rangement.md`](docs/methode/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/methode/contexte.md`](docs/methode/contexte.md) |
| **cycles DSH, sous-agents, reprise** | [`docs/methode/continuite.md`](docs/methode/continuite.md) |
| **rapporter à l'humain, un round** | [`docs/methode/relations-humaines.md`](docs/methode/relations-humaines.md) |
| **dessiner un schéma**, convertir un diagramme, améliorer une illustration | [`docs/methode/illustrations.md`](docs/methode/illustrations.md) |
| lancer ou lire les portes | [`docs/methode/portes.md`](docs/methode/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/methode/miroir.md`](docs/methode/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/methode/ressources.md`](docs/methode/ressources.md) |
| **les jeux symboliques** (surface → RSN-jeu → pensée, 71 langues, maîtres) | [`docs/theorie/jeux-symboliques.md`](docs/theorie/jeux-symboliques.md) |
| **le protocole sémantique** (rejouer, convergence, sens → texte, raisonnement gelé) | [`docs/theorie/protocole-semantique.md`](docs/theorie/protocole-semantique.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/theorie/glossaire.md`](docs/theorie/glossaire.md) |
| **trouver un sujet** (un concept, un chantier, une phase) | [`docs/theorie/carte.md`](docs/theorie/carte.md) |
| la carte de la documentation | [`docs/README.md`](docs/README.md) |

> **Chargement facultatif.** Les documents de cette table, `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `reports/` et
> `journal/` ne se lisent **que pour la tâche en cours** : le fichier de tâche suffit. Ne pas les
> charger « pour être complet » : c'est du contexte qui coûte et périme.

> **Le contexte est un budget.** Par défaut : `AGENTS.md` + `docs/pilotage/en-cours.md` + **un** document de
> tâche. Le protocole, les budgets et les cas « ne pas charger » sont dans
> [`docs/methode/contexte.md`](docs/methode/contexte.md) ; la vérification est
> `python3 tools/taille_documents.py`.

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les rouges tolérées listées dans `docs/pilotage/references-non-regression.md`** ;
- la revue de documentation passe, et les liens résolvent.
- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
- l'état est court et reprenable : `python3 tools/verifie_en_cours.py`.
- journal : dossiers/jour, sessions liées → `tools/verifie_journal.py`.
- les schémas sont des SVG valides et référencés : `python3 tools/verifier_schemas.py`.

</system-reminder>

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

- **bash** `{"command": "pwd && git status --short | head -50 && git log --oneline -5", "description": "Check repo state and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PLUS DE SYNTAGMES (1 075 CONTRE 1 006) ET VA PLUS VITE ; LE TEMPS NE SUIT PAS LES MOTS SEULS
7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))
7d114559 T3 — LE DÉMARRAGE EN 5 MINUTES : 
… [134 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"_groupes_partition\\|_cible_proche\" --include=*.py . | head -50", "description": "Locate the two functions"}`

  ```
./tools/bloc_linguistique.py:1274:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
./tools/bloc_linguistique.py:1794:                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
./tools/bloc_linguistique.py:1804:                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
./tools/bloc_linguistique.py:1834:                         or self._cible_proche(texte, s, gvs_s, verbes, cache_gv))
./tools/bloc_linguistique.py:1866:                         or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
./tools/bloc_linguistique.py:2518:def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
./tools/bloc_linguistique.py:2556:    groupes = _groupes_partition(segs)
./tools/banc_performance.py:1110:        "prochaine_action": ("profiler et borner `_groupes_partition` (O(k²) sur les syntagmes) "
./tools/banc_performance.py:1111:                             "et `_cible_proche` (tri de tous les GV par segment) ; mesurer "
  ```

- **bash** `{"command": "ls reports | grep -i \"performance\\|T4\\|t4\" ; echo ---; sed -n '1,120p' reports/rapport-performance.md 2>/dev/null | head -120", "description": "Find T4 performance report"}`

  ```
performance-corpus-10000.txt
performance.json
performance-profil.json
rapport-performance.md
---
# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mots sont exploitables** (4,0 s de
> fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de
> linéarité échoue** — le temps croît en **α = 1,55** sur un bloc contrôlé, et le terme
> quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est
> nommé : `_groupes_partition` (toutes les paires de syntagmes, O(k²)) et `_cible_proche`
> (tri de tous les GV pour chaque segment), pas la tokenisation.
>
> **Les chiffres.** Sur le préfixe exact de **10 000 mots** de
> `data/corpus_fr_litterature.txt` (Alice, français), versionné dans
> [`reports/performance-corpus-10000.txt`](performance-corpus-10000.txt)
> (sha256 `0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871`,
> 57 588 caractères, 814 phrases) : **4,012 s** pour `Heuristique.analyser`, *
… [5718 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1220,1330p' tools/bloc_linguistique.py; echo '======'; sed -n '2480,2600p' tools/bloc_linguistique.py", "description": "Read the two functions"}`

  ```
@staticmethod
    def _tete_texte(texte: str) -> str | None:
        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.

        `« … → Le livre »` → `livre` ; `« … → Les fleurs poussent »` → `poussent` ;
        `« … → est prêt »` → `prêt` (l'auxiliaire n'est pas la tête).
        """
        mots = re.findall(r"\b[ldmtsnLDMTNS]['’](?=\w)|[\wÀ-ÿ]+(?:['’\-][\wÀ-ÿ]+)*", texte)
        if not mots:
            return None
        for m in mots:
            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
                return m
        return mots[-1]

    @staticmethod
    def _tete_nom(texte: str, debut: int, fin: int) -> str | None:
        """La tête nominale d'un span : le dernier mot, **élision séparée** (`L'homme` → `homme`)."""
        mots = re.findall(r"\b[ldmtsnLDMTNS]['’](?=\w)|[\wÀ-ÿ]+(?:['’\-][\wÀ-ÿ]+)*",
                          texte[debut:fin])
        return mots[-1] if mots else None

    @staticmethod
    def _verbe_dans(texte: str, debut: int, fin: int,
                    verbes: list[tuple[int, int, str]] | None = None,
                    strict: bool = False) -> str | None:
        """Le **verbe** du span : le le
… [9868 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"α\\|alpha\\|linéar\\|O(k\\|groupes_partition\\|cible_proche\\|contrôlé\\|controle\" reports/rapport-performance.md | head -60", "description": "Locate linearity section in T4 report"}`

  ```
1:# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)
6:> linéarité échoue** — le temps croît en **α = 1,55** sur un bloc contrôlé, et le terme
8:> nommé : `_groupes_partition` (toutes les paires de syntagmes, O(k²)) et `_cible_proche`
134:## 5. Le contrôle négatif de linéarité — et pourquoi il échoue
153:changent, et le temps ne suit pas les mots. La pente log-log des préfixes vaut **α = 1,13**,
156:### 5.2 Le bloc contrôlé isole la taille
183:| `log t = α·log n + β` | 0,995 | 0,140 | **α = 1,552** |
194:| charge | α mesuré | R² | attendu |
211:| `_cible_proche` | 1 040 | **14,474 s** | 30 % |
214:| `_groupes_partition` | 1 | **11,162 s** | 23 % |
221:1. **`_groupes_partition`** ([`bloc_linguistique.py:2518`](../tools/bloc_linguistique.py))
223:   chevauchement : O(k²) en nombre de syntagmes k. À k = 1 984, cela fait ~2 M de paires ;
225:2. **`_cible_proche`** ([`bloc_linguistique.py:1273`](../tools/bloc_linguistique.py))
227:   les **trie** par distance (`sorted`) : O(k·m log m) par analyse. `_verbes_proches` fait
249:contrôle de linéarité **échoue** : à densité constante, α = **1,55** et le m
… [285 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1000,1160p' tools/banc_performance.py", "description": "Read bank performance next action & linearity"}`

  ```
bloc, bloc_debut, bloc_fin = _bloc_phrases(texte, 250)
    bloc_path = work / "bloc-controle.txt"
    bloc_path.write_text(bloc, encoding="utf-8")
    bloc_mots = _compter_mots(bloc)

    print(f"banc : {mots_reels} mots, {len(phrases)} phrases, "
          f"{len(courtes)} phrases courtes, bloc {bloc_mots} mots", file=sys.stderr)

    # --- 10 000 mots
    print("banc : 10 000 mots (fonction + CLI)…", file=sys.stderr)
    m10_fonction = _run_analyse(texte_path, args.repetitions)
    m10_cli = _run_cli(texte_path, args.repetitions, jsonl=False)
    m10_jsonl = _run_cli(texte_path, 1, jsonl=True)

    # --- 100 phrases courtes
    print("banc : 100 phrases courtes (fonction + CLI)…", file=sys.stderr)
    mc_fonction = _run_100_fonction(courtes, repetitions=max(1, args.repetitions))
    mc_cli = _run_100_cli(courtes)
    mc_lot = _run_cli(lot_path, 1, jsonl=True)

    # --- tagger
    tagger: dict = {"disponible": False, "raison": "--avec-tagger absent"}
    if args.avec_tagger:
        print("banc : tagger sur 100 phrases courtes (réseau froid)…", file=sys.stderr)
        t100 = _run_tagger(lot_path, timeout=7200.0)
        tagger["cent_courtes"] = t100
        if args.tagger_comple
… [6558 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '130,270p' reports/rapport-performance.md", "description": "Read linearity section"}`

  ```
diviserait le temps et les tokens par presque le nombre d'appels. Au taux de W3
(0,031 $ pour 143 870 tokens), 236 215 tokens valent **~0,05 $** — le coût monétaire est
négligeable, le coût **temps** ne l'est pas.

## 5. Le contrôle négatif de linéarité — et pourquoi il échoue

### 5.1 Les préfixes réels sont confondus par le contenu

Les préfixes du même texte ne permettent **pas** de conclure : le nombre de syntagmes n'est
pas proportionnel aux mots, et le temps suit les syntagmes.

| mots | syntagmes | temps (s) | mots/s |
|---:|---:|---:|---:|
| 250 | 126 | 0,047 | 5 300 |
| 500 | 262 | 0,122 | 4 097 |
| 1 000 | 496 | 0,306 | 3 270 |
| 2 000 | 1 006 | 0,981 | 2 039 |
| 4 000 | 1 075 | **0,758** | 5 276 |
| 8 000 | 2 192 | 2,689 | 2 975 |
| 10 000 | 2 726 | 3,994 | 2 504 |

Le point **4 000 mots est plus rapide que le point 2 000** (0,758 s contre 0,981 s) alors
qu'il a **plus** de syntagmes (1 075 contre 1 006) : le contenu et les chevauchements
changent, et le temps ne suit pas les mots. La pente log-log des préfixes vaut **α = 1,13**,
mais elle mélange la taille et le contenu ; ce n'est pas un test de complexité.

### 5.2 Le bloc contrôlé isole la taille

On prend un bloc de 
… [5967 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/performance.json'))\nprint(d.get('parametres'))\nprint(json.dumps(d['corpus'],ensure_ascii=False,indent=1)[:2000])\nprint(json.dumps(d['echelle'],ensure_ascii=False,indent=1)[:6000])\nPY", "description": "Read performance JSON mea … [11 caractères tronqués]`

  ```
{'source': 'data/corpus_fr_litterature.txt', 'mots': 10000, 'phrases_courtes': 100, 'repetitions': 3, 'tailles': [250, 500, 1000, 2000, 4000, 8000, 10000], 'avec_tagger': True, 'tagger_complet': False, 'tagger_seulement': True}
{
 "source": "data/corpus_fr_litterature.txt",
 "source_sha256": "392f6c6274daaedfcb2957aa92b489cd28de6fcd7e92c7ae9eb4d8f14e9ed2df",
 "prefixe_sha256": "0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871",
 "mots": 10000,
 "caracteres": 57588,
 "phrases": 814,
 "bloc_controle": {
  "mots": 247,
  "debut": 0,
  "fin": 1572,
  "sha256": "618e219f2420daa76d7ad52dce15d81ef08dc9a8e1f35826785ce566b695ca41"
 },
 "phrases_courtes": {
  "n": 100,
  "mots": 661,
  "median_mots": 6.0,
  "exemples": [
   "Cette version électronique reproduit dans son intégralité la version originale.",
   "La ponctuation n'a pas été modifiée hormis quelques corrections mineures.",
   "L'orthographe a été conservée.",
   "Seuls quelques mots ont été modifiés.",
   "La liste des modifications se trouve à la fin du texte."
  ]
 }
}
{
 "prefixes_reels": {
  "mesures": [
   {
    "mots": 250,
    "duree_s": 0.04710945510305464,
    "duree_min_s": 0.045476330909878016,
    "dure
… [5852 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests | head -50; echo ---; grep -rln \"612\\|452\" tools/tests tools/*.py reports/*.md | head -40", "description": "Find gold test infrastructure"}`

  ```
cic
code
documents
linguistique
maths
__pycache__
qualifier_politique_drvm.py
qualifier_porte_bouge_drvm.py
qualifier_porte_drvm.py
qualifier_porte_fenetre_drvm.py
qualifier_porte_minute_drvm.py
qualifier_porte_mobile_drvm.py
qualifier_porte_sto_drvm.py
qualifier_porte_sto_graines.py
tableaux
test_banc_performance.py
test_empaquetage.py
test_panini_334.py
test_pensee_politique.py
test_pensee_store.py
test_produit_libre.py
test_produit.py
test_restitution.py
test_restitution_v2.py
test_restitution_v3.py
test_schema_produit.py
test_tagger_api.py
test_verificateur_cic.py
test_verificateur_cic_v2.py
---
tools/tests/documents/pdf/deux-colonnes.pdf
tools/tests/documents/corpus/juridique/A_RES_80_1-en.pdf
tools/tests/documents/corpus/juridique/A_RES_80_1-es.pdf
tools/tests/documents/corpus/juridique/A_RES_80_1-fr.pdf
tools/tests/documents/corpus/juridique/A_RES_80_10-en.pdf
tools/tests/documents/corpus/juridique/A_RES_80_10-es.pdf
tools/tests/documents/corpus/juridique/A_RES_80_10-fr.pdf
tools/tests/documents/corpus/manifeste.json
tools/tests/linguistique/__pycache__/gold_split.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_tagger_612.cpython-313.pyc
tools/tests/linguistiq
… [1148 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | grep -i \"gold\\|612\\|452\\|pensee\" | head -40; echo ---; ls tools/tests/linguistique 2>/dev/null", "description": "Find gold reports and tests"}`

  ```
-rw-r--r--. 1 stephane stephane     702 28 oct 11:21 native-pensee.json
-rw-r--r--. 1 stephane stephane    2079 21 oct 03:50 pas-de-pensee-14b.json
-rw-r--r--. 1 stephane stephane    2075 21 oct 01:53 pas-de-pensee-7b.json
-rw-r--r--. 1 stephane stephane    6848 21 oct 01:58 pas-de-pensee-contracte-3b.json
-rw-r--r--. 1 stephane stephane    6825 21 oct 01:59 pas-de-pensee-contracte-7b.json
-rw-r--r--. 1 stephane stephane    3160 21 oct 23:15 pas-de-pensee-corrige-14b.json
-rw-r--r--. 1 stephane stephane    3154 21 oct 23:15 pas-de-pensee-corrige-3b.json
-rw-r--r--. 1 stephane stephane    3168 21 oct 23:15 pas-de-pensee-corrige-7b.json
-rw-r--r--. 1 stephane stephane    3186 21 oct 23:40 pas-de-pensee-corrige-large.json
-rw-r--r--. 1 stephane stephane    2084 21 oct 01:49 pas-de-pensee.json
-rw-r--r--. 1 stephane stephane      81 21 oct 02:02 pas-de-pensee-mlp-18.json
-rw-r--r--. 1 stephane stephane      83 21 oct 02:03 pas-de-pensee-mlp-6.json
-rw-r--r--. 1 stephane stephane    2707 21 oct 23:15 pas-de-pensee-non-lineaire-3b.json
-rw-r--r--. 1 stephane stephane    2742 21 oct 23:40 pas-de-pensee-non-lineaire-large.json
-rw-r--r--. 1 stephane stephane     892 21 oct 16:10 pas-de-pen
… [2634 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['tools/tests/linguistique/gold_gele.json','tools/tests/linguistique/gold_reel.json']:\n    d=json.load(open(p))\n    print(p, type(d), len(d) if hasattr(d,'__len__') else '')\n    if isinstance(d,dict): print(list(d)[:10])\n    if isinstance(d,li … [102 caractères tronqués]`

  ```
tools/tests/linguistique/gold_gele.json <class 'dict'> 2
['gele', 'phrases']
tools/tests/linguistique/gold_reel.json <class 'dict'> 4
['version', 'source', 'note', 'phrases']
  ```

- **bash** `{"command": "grep -rn \"612\\|452\" tools/tests/linguistique/*.py tools/*.py reports/rapport-performance*.md 2>/dev/null | head -40", "description": "Find references to 612 and 452"}`

  ```
tools/tests/linguistique/gold_reel_50.py:8:donc pas un problème de **nombre** (452 > 200) : c'est un problème de **discrimination**.
tools/tests/linguistique/gold_reel_50.py:64:    """Les 452 phrases réelles : 20 hand + 432 reel, chacune avec sa source."""
tools/tests/linguistique/gold_reel_50.py:268:    """Projection si un **nouveau** lot du même profil était ajouté (452 → 502).
tools/tests/linguistique/gold_reel_50.py:329:        "majoritaire": {"hard_50": majoritaire(choisies), "global_452": majoritaire(rows)},
tools/tests/linguistique/gold_reel_50.py:330:        "uniforme": {"hard_50": uniforme(choisies), "global_452": uniforme(rows)},
tools/tests/linguistique/gold_reel_50.py:427:    mesures = {"global_452": metriques(rows), "hard_50": metriques(choisies),
tools/tests/linguistique/gold_reel_50.py:481:                          "(452 phrases) et ambigu (T15).",
tools/tests/linguistique/gold_reel_50.py:492:            "global": mesures["global_452"],
tools/tests/linguistique/gold_reel_50.py:513:                "attachement": mesures["global_452"]["attachement"],
tools/tests/linguistique/gold_reel_50.py:544:            "projection_502": projeter(mesures["global_452"], mesures["hard
… [3464 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"gold_gele\\|gold_reel\" tools --include=*.py | head -30; echo ---; sed -n '1,120p' tools/tests/test_bloc_linguistique.py", "description": "Find gold evaluation scripts"}`

  ```
tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique/gold_reel.py
tools/tests/linguistique/qualifier_cascade.py
tools/tests/linguistique/qualifier_lien_appris.py
tools/tests/linguistique/qualifier_quatre_modes.py
tools/tests/linguistique/qualifier_tagger_612.py
tools/tests/linguistique/gold_reel_50.py
tools/tests/linguistique/qualifier_tagger_h50.py
tools/tests/linguistique/qualifier_tagger_lot.py
tools/pensee/autotest.py
tools/verifier_faq.py
---
[stderr]
sed: can't read tools/tests/test_bloc_linguistique.py: No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "sed -n '1,130p' tools/tests/linguistique/evaluer_gold.py; echo =====; sed -n '1,80p' tools/tests/linguistique/gold.py", "description": "Read gold evaluation tool"}`

  ```
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_ge
… [9866 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique | grep '^test'; echo ---; sed -n '300,520p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluer_gold CLI and tests"}`

  ```
test_atomes_prediction.py
test_bloc_linguistique.py
---
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-01", **resultats}, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
    return 0 if resultats["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/linguistique/gold_gele.json'))\nprint('gele',len(d['phrases']))\nd2=json.load(open('tools/tests/linguistique/gold.json'))\nprint('hand',len(d2['phrases']))\nd3=json.load(open('tools/tests/linguistique/gold_reel.json'))\nprint( … [176 caractères tronqués]`

  ```
gele 602
hand 20
reel 432
synth 160
  ```

- **bash** `{"command": "sed -n '200,310p' tools/tests/linguistique/evaluer_gold.py", "description": "Read main of evaluer_gold"}`

  ```
"exact_any_taux_span": round(att_exact_any / max(1, att_labels), 4),
                        # exactitude sur les segments au bon span : l'attachement seul
                        "top1_taux_span": round(att_top1 / max(1, att_labels), 4),
                        "topk_taux_span": round(att_topk / max(1, att_labels), 4),
                        "topk_exact": att_topk_exact,
                        "topk_exact_taux": round(att_topk_exact / max(1, att_n), 4),
                        "topk_exact_taux_span": round(att_topk_exact / max(1, att_labels), 4),
                        "exact_taux_span": round(att_exact / max(1, att_labels), 4),
                        "verbe": {"cibles": att_v_n, "justes": att_v_ok,
                                  "taux": round(att_v_ok / max(1, att_v_n), 4)},
                        "nom": {"cibles": att_n_n, "justes": att_n_ok,
                                "taux": round(att_n_ok / max(1, att_n_n), 4)},
                        "couverture": round(att_labels / max(1, att_n), 4),
                        "par_langue": {lg: {"cibles": v["cibles"], "labels": v["labels"],
                                            "exact": v["exact"], "topk": v["topk"],
     
… [5171 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/tests/linguistique/test_bloc_linguistique.py", "description": "Read bloc tests"}`

  ```
"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_relative_zero(self):
        """Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL.

        La règle est **structurelle** : elle ne dépend ni du nom, ni du pronom, ni du verbe,
        ni de la prépositi
… [8291 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1640,1900p' tools/bloc_linguistique.py", "description": "Read _cible_proche call sites"}`

  ```
continue
            _av = etiquettes[pos_idx[_k - 1]]
            if (_av.type == "PRON" and _normaliser(_av.valeur) in SUJETS
                    and not _normaliser(_e.valeur).endswith(_nominales)):
                etiquettes[_i] = Etiquette("pos", "VERB", _e.valeur, _e.debut, _e.fin, self.nom,
                                           0.85, candidats=["verb"], langue=lg, script=script,
                                           meta={"ouvert": True, "contexte": "pron_sujet"})

        # 3 b. un DET **ambigu** sans nom à sa droite n'est pas un DET (« the book that I
        # read », « he speaks to her ») : c'est un PRON, ou un CONJ après un verbe.
        _lexd = POS_FERME.get(lg, POS_FERME["fr"])
        for _k, _i in enumerate(pos_idx):
            _e = etiquettes[_i]
            if _e.type != "DET":
                continue
            if _normaliser(_e.valeur) not in (_lexd.get("PRON", set()) | _lexd.get("CONJ", set())):
                continue
            _suiv = etiquettes[pos_idx[_k + 1]] if _k + 1 < len(pos_idx) else None
            if _suiv is not None and (_suiv.type in ("NOUN", "ADJ", "NUM") or (
                    _suiv.type == "VERB" and _suiv.confiance <= 0.45
… [15585 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _sujet_hors_gv\\|def _est_adverbe_seul\\|def _cible_hors_span\\|def _cibles_s\\|def _syntagmes_simple\" tools/bloc_linguistique.py", "description": "Locate helper functions"}`

  ```
516:def _est_adverbe_seul(g: dict) -> bool:
950:    def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,
1036:    def _cibles_s(self, texte: str) -> dict:
1198:    def _cible_hors_span(texte: str, segment: dict, gvs: list[dict], cible: str | None):
1328:    def _syntagmes_simple(self, texte: str, langue: str,
  ```

- **bash** `{"command": "sed -n '1120,1230p' tools/bloc_linguistique.py; echo =====; grep -n \"_sujet_hors_gv\" tools/bloc_linguistique.py", "description": "Read adverbe helper and subject function"}`

  ```
vus: set[tuple[int, int, str]] = set()

        def ajouter(valeur: str | None) -> None:
            v = (valeur or "").strip()
            if not v:
                return
            debut = texte.find(v)
            if debut < 0:  # repli insensible à la casse, sans décaler les offsets
                trouve = re.search(re.escape(v), texte, re.IGNORECASE)
                debut = trouve.start() if trouve else -1
            if debut < 0:
                return
            fin = debut + len(v)
            cle = (debut, fin, v)
            if cle in vus:
                return
            vus.add(cle)
            objets.append({"span": {"debut": debut, "fin": fin},
                           "cible": v, "source": source})

        ajouter(cible)
        for chaine in candidats or []:
            ajouter(Heuristique._cible_candidat(chaine))
        return objets

    @staticmethod
    def _attachement(texte: str, segment: dict, cible: str | None,
                     candidats: Sequence[str] | None, source: str) -> dict:
        """Le bloc `meta.attachement` : `segment`, `cible` et les candidats structurés."""
        att = {"segment": segment.get("texte", ""), "cible": cible or ""}
… [4279 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '500,540p' tools/bloc_linguistique.py; echo =====; sed -n '930,1045p' tools/bloc_linguistique.py", "description": "Read _est_adverbe_seul and _sujet_hors_gv"}`

  ```
am is are was were be been being have has had having do does did done
would must can could should will shall may might ought cannot
""".split())


# adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
# (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
                  "today", "now", "later", "soon", "tonight"}


ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
                  "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
                  "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}


def _est_adverbe_seul(g: dict) -> bool:
    """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
    return (len((g.get("texte") or "").split()) == 1
            and _normaliser(g.get("texte") or "") in ADVERBES_SEULS)


MODAUX = {"would", "must", "can", "could", "should", "will", "shall", "may", "might", "ought",
          "could", "cannot"}

ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", 
… [6185 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"_cible_proche(\\|_verbes_proches(\" tools/bloc_linguistique.py", "description": "List all call sites"}`

  ```
1274:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
1309:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
1794:                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
1804:                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
1807:                    candidats = list(noms) + self._verbes_proches(
1834:                         or self._cible_proche(texte, s, gvs_s, verbes, cache_gv))
1839:                             + self._verbes_proches(
1866:                         or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
1871:                             + self._verbes_proches(
  ```

- **bash** `{"command": "grep -rn \"_cible_proche(\\|_verbes_proches(\" tools --include=*.py | grep -v \"def \"", "description": "External call sites"}`

  ```
tools/bloc_linguistique.py:1794:                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
tools/bloc_linguistique.py:1804:                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
tools/bloc_linguistique.py:1807:                    candidats = list(noms) + self._verbes_proches(
tools/bloc_linguistique.py:1834:                         or self._cible_proche(texte, s, gvs_s, verbes, cache_gv))
tools/bloc_linguistique.py:1839:                             + self._verbes_proches(
tools/bloc_linguistique.py:1866:                         or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
tools/bloc_linguistique.py:1871:                             + self._verbes_proches(
  ```

- **bash** `{"command": "grep -n \"def json\\|duree_s\\|cout\" tools/bloc_linguistique.py | head -40; echo ---; sed -n '260,420p' tools/bloc_linguistique.py", "description": "Inspect Annotation json output"}`

  ```
69:    def json(self) -> dict:
87:    def json(self) -> dict:
132:    cout: dict = field(default_factory=dict)
149:    def json(self, avec_duree: bool = False) -> dict:
150:        cout = dict(self.cout)
152:            cout.pop("duree_s", None)
161:            "trace": list(self.trace), "cout": cout, "contexte": self.contexte,
365:              "regardes regardons regardez regardent écoute écoutes écoutons écoutez écoutent ouvre "
420:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
467:travailles travaillent travaillait regarder regarde regardes regardent regardait écouter écoute
468:écoutes écoutent écoutait aimer aime aimes aiment aimait finir finis finit finissent finissait
1569:                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
1575:                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})
1926:                          cout={"octets": len(texte.encode("utf-8", "replace")), "caracteres": len(texte),
1927:                                "etiquettes": len(etiquettes), "duree_s": round(time.perf_counter() - t0
… [13066 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,170p' tools/bloc_linguistique.py", "description": "Read Annotation json emitter"}`

  ```
# --------------------------------------------------------------------------- types


@dataclass(frozen=True)
class Span:
    debut: int
    fin: int

    def json(self) -> dict:
        return {"debut": self.debut, "fin": self.fin}


@dataclass
class Etiquette:
    niveau: str
    type: str
    valeur: str
    debut: int
    fin: int
    source: str = "heuristique"
    confiance: float = 0.5
    candidats: list[str] = field(default_factory=list)
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
            "debut": self.debut, "fin": self.fin, "source": self.source,
            "confiance": round(float(self.confiance), 4),
            "candidats": list(self.candidats), "langue": self.langue,
            "script": self.script, "meta": _meta_json(self.meta),
        }


def normaliser_role(role: str, strict: bool = True) -> str:
    """Le rôle canonique (voir `tools/roles_vocabulaire.py`)."""
    return _normaliser_role(role, strict=strict)


def _meta_json(meta: dict) -> dict:
    """`meta` sérialisable : les r
… [2794 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '900,1010p' tools/banc_performance.py; echo =====; sed -n '1,80p' tools/banc_performance.py", "description": "Read bank CLI options"}`

  ```
help="petit passage hors ligne : 3 tailles, 1 répétition, sans tagger")
    ap.add_argument("--interne", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--interne-phrases", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--fichier", default="", help=argparse.SUPPRESS)
    ap.add_argument("--sortie-json", default="", help=argparse.SUPPRESS)
    args = ap.parse_args()

    # --- le mode profil : la cause, pas seulement le chiffre
    if args.profil:
        # ne jamais écraser le JSON de performance par un profil
        sortie_profil = args.sortie
        if sortie_profil == "reports/performance.json":
            sortie_profil = "reports/performance-profil.json"
        return _profil(pathlib.Path(args.profil), pathlib.Path(sortie_profil))

    # --- les deux modes helpers, appelés par le banc lui-même
    if args.interne:
        return _helper_analyse(pathlib.Path(args.fichier), pathlib.Path(args.sortie_json))
    if args.interne_phrases:
        return _helper_phrases(pathlib.Path(args.fichier))

    if args.rapide:
        args.repetitions = 1
        args.tailles = "250,1000,10000"
        args.avec_tagger = False
        args.tagger_complet
… [7427 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1160,1260p' tools/banc_performance.py", "description": "Read bank end and CLI"}`

  ```
"verdict": verdict,
    }

    sortie = pathlib.Path(args.sortie)
    if not sortie.is_absolute():
        sortie = RACINE / sortie
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"banc : JSON → {sortie}", file=sys.stderr)

    if args.rapport:
        chemin_rapport = pathlib.Path(args.rapport)
        if not chemin_rapport.is_absolute():
            chemin_rapport = RACINE / chemin_rapport
        chemin_rapport.parent.mkdir(parents=True, exist_ok=True)
        chemin_rapport.write_text(_markdown(rapport) + "\n", encoding="utf-8")
        print(f"banc : rapport → {chemin_rapport}", file=sys.stderr)

    print(json.dumps({
        "dix_mille_s": m10_fonction["duree_analyse_s"]["mediane"],
        "debit_mots_s": verdict["debit_mots_s"],
        "rss_mio": m10_fonction["rss_kb"]["mediane"] / 1024,
        "json_octets": m10_cli["octets"],
        "cent_ms": mc_fonction["duree_par_appel_s"]["mediane"] * 1000,
        "alpha_bloc": alpha_bloc,
        "controle_lineaire": controle_ok,
        "tagger_disponible": tagger.get("disponible", False),
        "sortie": str(sort
… [113 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '840,910p' tools/banc_performance.py", "description": "Read argument parser"}`

  ```
f"c = {a['quadratique']['c']:.3e} s/mot², RMSE {_fmt(a['quadratique']['rmse'], 3)} s ;",
        f"- contrôle de l'instrument : boucle linéaire α = "
        f"**{_fmt(echelle['instrument']['lineaire']['loglog']['alpha'], 2)}**, "
        f"boucle quadratique α = **{_fmt(echelle['instrument']['quadratique']['loglog']['alpha'], 2)}**.",
        "",
        f"**Verdict** : {'✅ le contrôle passe' if rapport['verdict']['controle_lineaire'] else '❌ le contrôle **échoue**'} — "
        f"α = {_fmt(a['loglog']['alpha'], 2)} sur le bloc répété, "
        f"le terme quadratique ajoute {a['quadratique']['r2'] - a['lineaire']['r2']:+.3f} de R².",
        "",
        "## 6. Ce qui pourrait rendre ces chiffres faux",
        "",
        "- **Un seul texte** : le préfixe de 10 000 mots est un texte littéraire français "
        "(Alice) ; un texte technique, juridique ou multilingue peut changer la densité de "
        "syntagmes, donc le temps.",
        "- **Le bloc répété n'est pas le texte réel** : il mesure la croissance à densité "
        "constante. Le texte réel de 10 000 mots a une densité de syntagmes plus faible ; "
        "c'est pourquoi il est plus rapide que le bloc répété de mêm
… [2823 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p /tmp/u1-before /tmp/u1-after && PYTHONHASHSEED=0 python3 tools/banc_performance.py --sortie /tmp/u1-before/performance-avant.json --repetitions 3 > /tmp/u1-before/banc-avant.log 2>&1; echo EXIT:$?; tail -30 /tmp/u1-before/banc-avant.log", "description": "Run baseline performanc … [35 caractères tronqués]`

  ```
started background job bash-30
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/u1-before/gold-avant.json > /tmp/u1-before/gold-avant.log 2>&1; echo EXIT:$?; tail -20 /tmp/u1-before/gold-avant.log", "description": "Run baseline gold evaluation", "run_in_background": true}`

  ```
started background job bash-31
  ```

- **bash** `{"command": "grep -n \"_expliciter_partition\" tools/bloc_linguistique.py; sed -n '2600,2700p' tools/bloc_linguistique.py", "description": "Read partition explicit function rest"}`

  ```
1917:            _expliciter_partition(etiquettes, filtrer=(
2542:def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
                if autre is e:
                    continue
                vue = {"type": autre.type, "debut": autre.debut, "fin": autre.fin,
                       "source": autre.source,
                       "union": bool((autre.meta or {}).get("union")),
                       "relation": _relation_partition(e, autre),
                       "rang": rangs[id(autre)][1]}
                if filtrer:
                    vue["retire"] = id(autre) in retirees
                att = (autre.meta or {}).get("attachement")
                if att:
                    vue["attachement"] = {"segment": att.get("segment", ""),
                                          "cible": att.get("cible", "")}
                    if att.get("candidats"):
                        vue["attachement"]["candidats"] = copy.deepcopy(att["candidats"])
                role = (autre.meta or {}).get("role")
                if role:
                    vue["role"] = role
                vues.append(vue)
            vues.sort(key=lambda v: (v["rang"], v["debut"], v["fin
… [4427 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1900,1935p' tools/bloc_linguistique.py; grep -n \"filtrer\\b\\|filtrer=\" tools/bloc_linguistique.py | head -20", "description": "Check partition filter mode"}`

  ```
titre = (p.lstrip().startswith("#") or
                     bool(re.match(r"^\s*(?:\d+[.)]|[IVXLC]+[.)])\s+", p)) or
                     (len(p.strip()) < 80 and p.strip().endswith((":", ".")) is False and
                      p.strip() == p.strip().upper()))
            etiquettes.append(Etiquette("document", "titre" if titre else "paragraphe",
                                        p.strip()[:60], d, f, self.nom, 0.7,
                                        langue=lg, script=script))
        if contexte:
            etiquettes.append(Etiquette("pragmatique", "contexte", contexte[:200], 0, len(texte),
                                        "humain", 1.0, langue=lg, script=script))

        # 7. unités sémantiques : ouvertes + syntagmes ambiguës, dédupliquées
        unites = _fusionner(unites)
        longueur = sum(u.fin - u.debut for u in unites)
        fraction = longueur / max(1, len(texte))
        etiquettes.sort(key=lambda e: (e.debut, e.fin, e.niveau))
        if self.partition != "brut":
            _expliciter_partition(etiquettes, filtrer=(
                "" if self.partition == "alternative"
                else "union" if self.partition == "filtrer_union" else "
… [2139 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-31 (bash: PYTHONHASHSEED=0 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/u1-before/gold-avant.json > /tmp/u1-before/gold-avant.log 2>&1; echo EXIT:$?; tail -20 /tmp/u1-before/gold-avant.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cat /tmp/u1-before/gold-avant.log | tail -20; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/u1-before/gold-avant.json'))\nprint(d['gold'])\nfor k in ['all','reel','hand','synthetique']:\n print(k, 'pos', d['heuristique'][k]['pos']['exactitude'], 'seg f1', d['heuristique'][k]['sy … [198 caractères tronqués]`

  ```
"exact": 151,
      "topk": 149,
      "exact_taux_span": 1.0
     },
     "en": {
      "cibles": 88,
      "labels": 87,
      "exact": 87,
      "topk": 87,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 238,
    "labels": 238,
    "top1": 238,
    "topk": 236,
    "top
heuristique all: {"pos": {"exactitude": 0.8625, "exactitude_ferme": 0.9373, "exactitude_ouvert": 0.7918, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 65, "NOUN": 65, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"PRON": 15, "CONJ": 68, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"PONCT": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 429, "?": 30, "CONJ": 2, "DET": 14}, "VERB": {"VERB": 546, "NOUN": 218, "PREP": 2, "ADJ": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.786, "rappel": 0.7944, "f1": 0.7902, "tp": 1480, "fp": 403, "fn": 383, "tete": {"precision": 0.9261, "rappel": 0.8808, "f1": 0.9029, "tp": 1641, "fp": 131, "fn": 222}}, "pragmatique": {"acte": 0.9967, "negation":
… [424 caractères tronqués]
  ```

- **bash** `{"command": "tail -5 /tmp/u1-before/banc-avant.log; ls -la /tmp/u1-before", "description": "Check baseline bank progress"}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
total 56
drwxr-xr-x.   2 stephane stephane   100 15 nov 23:45 .
drwxrwxrwt. 577 root     root     31320 15 nov 23:46 ..
-rw-r--r--.   1 stephane stephane   106 15 nov 23:45 banc-avant.log
-rw-r--r--.   1 stephane stephane 47625 15 nov 23:45 gold-avant.json
-rw-r--r--.   1 stephane stephane  3471 15 nov 23:45 gold-avant.log
  ```

- **bash** `{"command": "grep -n \"def _bloc_phrases\" -A30 tools/banc_performance.py", "description": "Read block construction"}`

  ```
86:def _bloc_phrases(texte: str, cible: int = 250) -> tuple[str, int, int]:
87-    """Un bloc de phrases entières, le plus proche possible de `cible` mots."""
88-    phrases = bl.Heuristique._phrases(texte)
89-    bloc = ""
90-    debut = fin = 0
91-    for d, f, _typ, _ in phrases:
92-        morceau = texte[d:f].strip()
93-        if not morceau:
94-            continue
95-        n = _compter_mots(morceau)
96-        if bloc and _compter_mots(bloc) + n > cible:
97-            break
98-        if not bloc:
99-            debut = d
100-        bloc = (bloc + "\n\n" + morceau).strip()
101-        fin = f
102-    return bloc, debut, fin
103-
104-
105-def _phrases_courtes(texte: str, n: int = 100) -> list[str]:
106-    """`n` phrases réelles de 3 à 12 mots, une seule phrase par entrée.
107-
108-    On garde l'ordre du texte. Si le texte n'en fournit pas assez, on complète avec les
109-    phrases les plus courtes (toujours dans l'ordre du texte) — le critère est consigné.
110-    """
111-    candidates: list[tuple[int, int, str]] = []
112-    for i, (d, f, _typ, _) in enumerate(bl.Heuristique._phrases(texte)):
113-        texte_phrase = " ".join(texte[d:f].split())
114-        if not
… [86 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-30", "wait": true, "timeout_ms": 240000}`

  ```
EXIT:0
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
banc : contrôle de l'instrument…
banc : JSON → /tmp/u1-before/performance-avant.json
{
 "dix_mille_s": 3.990812406176701,
 "debit_mots_s": 2505.7554658602085,
 "rss_mio": 126.890625,
 "json_octets": 14795890,
 "cent_ms": 1.0536418994888663,
 "alpha_bloc": 1.52996378990646,
 "controle_lineaire": false,
 "tagger_disponible": false,
 "sortie": "/tmp/u1-before/performance-avant.json"
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "sed -n '820,870p' tools/bloc_linguistique.py", "description": "Read Heuristique init defaults"}`

  ```
i = j
            continue
        if ch not in ".!?…":
            i += 1
            continue
        j = i + 1
        while j < n and texte[j] in ".!?…":
            j += 1
        if not _dans_zone(zones, i, j) and _est_frontiere(texte, i, j, zones):
            ajouter(_absorber_fermants(texte, j), _type_phrase(texte[i:j]))
        i = j
    ajouter(n, "déclarative")
    return sortie


class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
                 union: bool = True, partition: str = "alternative"):
        self.profils = profils
        self.segmenter_s = segmenter_s
        self.seuil_ouvert = seuil_ouvert
        self.seuil_langue = seuil_langue
        self.union = union
        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
        # "filtrer_union" : on retire le S qui **contient** un segment chunker (
… [1145 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/gen_annotations.py <<'PY'\nimport json, sys, pathlib\nsys.path.insert(0, 'tools')\nimport bloc_linguistique as bl\nimport banc_performance as bp\n\noutdir = pathlib.Path(sys.argv[1])\noutdir.mkdir(parents=True, exist_ok=True)\nsource = pathlib.Path('data/corpus_fr_litterature … [1669 caractères tronqués]`

  ```
started background job bash-38
  ```

- **bash** `{"command": "sed -n '1,55p' tools/bloc_linguistique.py", "description": "Check imports"}`

  ```
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script`
… [1312 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "import os\n\nimport argparse\nimport collections\nimport copy\nimport json", "new_string": "import os\n\nimport argparse\nimport bisect\nimport collections\nimport copy\nimport heapq\nimport js … [4 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 35, "limit": 20}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 500, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
35: import collections
36: import copy
37: import json
38: import pathlib
39: import re
40: import subprocess
41: import sys
42: import threading
43: import time
44: import unicodedata
45: import urllib.request
46: from dataclasses import dataclass, field
47: from typing import Protocol, Sequence
48: 
49: RACINE = pathlib.Path(__file__).resolve().parent.parent
50: try:  # paquet : `tools.bloc_linguistique`
51:     from . import roles_gp as _roles_gp
52:     from .roles_vocabulaire import normaliser_role as _normaliser_role
53: except ImportError:  # script : `python3 tools/bloc_linguistique.py`
54:     import roles_gp as _roles_gp

(Showing lines 35-54 of 3019. Use offset=55 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
500: am is are was were be been being have has had having do does did done
501: would must can could should will shall may might ought cannot
502: """.split())
503: 
504: 
505: # adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
506: # (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
507: ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
508:                   "today", "now", "later", "soon", "tonight"}
509: 
510: 
511: ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
512:                   "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
513:                   "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}
514: 
515: 
516: def _est_adverbe_seul(g: dict) -> bool:
517:     """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
518:     return (len((g.get("texte") or "").split()) == 1
519:             and _normaliser(g.get("texte") or "") in ADVERB
… [486 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 12, "offset": 30}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 90, "offset": 1265}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
30: from __future__ import annotations
31: 
32: import os
33: 
34: import argparse
35: import collections
36: import copy
37: import json
38: import pathlib
39: import re
40: import subprocess
41: import sys

(Showing lines 30-41 of 3019. Use offset=42 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1265:         cle = (g["debut"], g["fin"])
1266:         if cache is not None and cle in cache:
1267:             return cache[cle]
1268:         v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
1269:         if cache is not None:
1270:             cache[cle] = v
1271:         return v
1272: 
1273:     @staticmethod
1274:     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
1275:                       verbes: list[tuple[int, int, str]] | None = None,
1276:                       cache: dict | None = None) -> str | None:
1277:         """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).
1278: 
1279:         Rend `None` si le segment est lui-même un GV ou s'il n'y a pas de GV. Le verbe est le
1280:         dernier token du GV (`a vu` → `vu`, `est mangé` → `mangé`).
1281:         """
1282:         gvs = [g for g in gvs if not _est_adverbe_seul(g)]
1283:         if segment.get("type") == "GV" or not gvs:
1284:             return None
1285:         if segment.get("type") == "GP":
1286:             # un GP n'est pas 
… [3838 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "import os\n\nimport argparse\nimport collections\nimport copy\nimport json", "new_string": "import os\n\nimport argparse\nimport bisect\nimport collections\nimport copy\nimport heapq\nimport js … [4 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "def _est_adverbe_seul(g: dict) -> bool:\n    \"\"\"Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »).\"\"\"\n    return (len((g.get(\"texte\") or \"\").split()) == 1\n       … [5580 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "    @staticmethod\n    def _cible_proche(texte: str, segment: dict, gvs: list[dict],\n                      verbes: list[tuple[int, int, str]] | None = None,\n                      cache: dict  … [5140 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 45, "offset": 2650}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2650:             i = parent[i]
2651:         return i
2652: 
2653:     for i in range(len(segs)):
2654:         for j in range(i + 1, len(segs)):
2655:             if max(segs[i].debut, segs[j].debut) < min(segs[i].fin, segs[j].fin):
2656:                 ri, rj = trouver(i), trouver(j)
2657:                 if ri != rj:
2658:                     parent[rj] = ri
2659:     groupes: dict[int, list[Etiquette]] = {}
2660:     for i, e in enumerate(segs):
2661:         groupes.setdefault(trouver(i), []).append(e)
2662:     return sorted((g for g in groupes.values() if len(g) > 1),
2663:                   key=lambda g: (min(e.debut for e in g), min(e.fin for e in g),
2664:                                  min(e.type for e in g)))
2665: 
2666: 
2667: def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
2668:     """Documente (et, si `filtrer`, linéarise) les chevauchements de syntagmes.
2669: 
2670:     `meta.partition` porte le groupe, le rang et la vue ; `meta.alternative` porte les
2671:     autres segments du groupe, leur relation vue du po
… [1475 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 25, "offset": 2635}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2635:     Mesuré sur le gold 612 : dans 179/207 groupes ambigus qui portent un span du gold, le
2636:     chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.
2637:     La préférence ne supprime rien par défaut : elle **classe**.
2638:     """
2639:     return (0 if (e.meta or {}).get("union") else 1, -(e.fin - e.debut), -e.confiance,
2640:             e.debut, e.fin, e.type)
2641: 
2642: 
2643: def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
2644:     """Les composantes connexes du graphe de chevauchement, ordonnées par position."""
2645:     parent = list(range(len(segs)))
2646: 
2647:     def trouver(i: int) -> int:
2648:         while parent[i] != i:
2649:             parent[i] = parent[parent[i]]
2650:             i = parent[i]
2651:         return i
2652: 
2653:     for i in range(len(segs)):
2654:         for j in range(i + 1, len(segs)):
2655:             if max(segs[i].debut, segs[j].debut) < min(segs[i].fin, segs[j].fin):
2656:                 ri, rj = trouver(i), trouver(j)
2657:          
… [188 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:\n    \"\"\"Les composantes connexes du graphe de chevauchement, ordonnées par position.\n\n    Un **balayage** des interv … [2187 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **job_output** `{"job_id": "bash-38", "wait": true, "timeout_ms": 120000}`

  ```
corpus 10000 56862
bloc 0 1572 247
bloc 1 1407 247
bloc 2 2815 494
bloc 4 5631 988
bloc 8 11263 1976
bloc 16 22527 3952
bloc 32 45055 7904
bloc 40 56319 9880
gold 612 reel 452
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m py_compile tools/bloc_linguistique.py && echo COMPILED; PYTHONHASHSEED=0 python3 -m unittest tools.tests.linguistique.test_bloc_linguistique -v 2>&1 | tail -40", "description": "Compile and run bloc tests"}`

  ```
COMPILED
test_activation_semantique (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_activation_semantique) ... ok
test_adaptateur_neuronal_avec_faux_modele (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_adaptateur_neuronal_avec_faux_modele) ... ok
test_adverbe_final_hors_du_gv (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_adverbe_final_hors_du_gv)
Un circonstant de temps final hors du GV ; la négation et l'adverbe non final restent. ... ok
test_cascade (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_cascade) ... ok
test_compose_pos_et_syntagmes (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_compose_pos_et_syntagmes) ... ok
test_langue_et_script (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_langue_et_script) ... ok
test_niveaux_et_spans (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_niveaux_et_spans) ... ok
test_parallele (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_parallele) ... ok
test_priorite_syntagme_confiance (tools.tests.linguistique.test_bloc_linguisti
… [1824 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/diff_opt.py <<'PY'\nimport sys, random\nsys.path.insert(0, 'tools')\nimport bloc_linguistique as bl\nfrom bloc_linguistique import Etiquette\n\n# --- reference group partition (old)\ndef ref_groupes(segs):\n    parent = list(range(len(segs)))\n    def trouver(i):\n        whi … [4559 caractères tronqués]`

  ```
groupes OK
MISMATCH cible 3669 {'debut': 40, 'fin': 42, 'type': 'GP'} L None [(40, 41, 'L')]
[exit code: 1]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 75, "offset": 525}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
525:     """Les GV d'une analyse, indexés pour rendre les plus proches **sans les trier**.
526: 
527:     L'ordre rendu par `proches` est **exactement** celui de
528:     `sorted(gvs, key=ecart)` : d'abord la distance au segment, puis l'ordre d'origine
529:     (le tri de Python est stable). L'index est bâti **une fois par liste de GV** ; une
530:     requête coûte O(log m + candidats examinés) au lieu de O(m log m).
531: 
532:     Trois flux partitionnent les GV sans recouvrement :
533:       - `gauche` : `fin <= debut` du segment, triés par `fin` décroissante (distance
534:         croissante) puis par ordre d'origine ;
535:       - `droite` : `debut >= fin` du segment, triés par `debut` croissante (distance
536:         croissante) puis par ordre d'origine ;
537:       - `zero`  : `debut < fin` et `fin > debut` du segment (chevauchement), dans l'ordre
538:         d'origine. Un arbre de segments (min `debut`, max `fin`) les rend un par un.
539:     Un tas fusionne les trois flux par `(distance, ordre d'origine)`.
540:     """
541: 
542:     __slots__ = ("gvs", "n",
… [2825 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 50, "offset": 600}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
600:             while ir < self.n:
601:                 i = self.par_debut[ir]
602:                 if self.fins[i] <= debut:
603:                     # segment vide : ce GV est déjà dans le flux gauche (priorité au gauche)
604:                     ir += 1
605:                     continue
606:                 heapq.heappush(tas, (self.debuts[i] - fin, i, 0))
607:                 return
608: 
609:         def pousser_gauche() -> None:
610:             nonlocal il
611:             if il >= 0:
612:                 i = self.par_fin[il]
613:                 heapq.heappush(tas, (debut - self.fins[i], i, 1))
614: 
615:         if iz >= 0:
616:             heapq.heappush(tas, (0, iz, 2))
617:         pousser_droite()
618:         pousser_gauche()
619:         while tas:
620:             distance, i, flux = heapq.heappop(tas)
621:             yield self.gvs[i]
622:             if flux == 0:
623:                 ir += 1
624:                 pousser_droite()
625:             elif flux == 1:
626:                 il -= 1
627:                 pousser_gauche()
628:             els
… [809 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "    __slots__ = (\"gvs\", \"n\", \"debuts\", \"fins\", \"utile\", \"min_debut_utile\",\n                 \"max_fin_utile\", \"par_debut\", \"par_fin\",\n                 \"debuts_tries\", \"fin … [2778 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        while tas:\n            distance, i, flux = heapq.heappop(tas)\n            yield i, self.gvs[i]\n            if flux == 0:", "old_string": "        while tas:\n            distance, i, … [86 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        index = _index_gv(gvs, cache)\n        if not index.n:\n            return None\n        gp = segment.get(\"type\") == \"GP\"\n        # un GP n'est pas gouverné par un mot de son propr … [2327 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        index = _index_gv(gvs, cache)\n        proches: list[str] = []\n        for n, (_i, g) in enumerate(index.proches(segment)):\n            if n >= k:\n                break\n             … [505 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "sed -i 's/got_order = list(bl._index_gv(gvs,None).proches(seg))/got_order = [g for _i, g in bl._index_gv(gvs,None).proches(seg)]/' /tmp/diff_opt.py\nPYTHONHASHSEED=0 python3 /tmp/diff_opt.py", "description": "Rerun differential tests"}`

  ```
groupes OK
cible/verbes OK
cache OK
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/banc_performance.py --sortie /tmp/u1-after/performance-apres.json --repetitions 3 > /tmp/u1-after/banc-apres.log 2>&1; echo EXIT:$?; tail -20 /tmp/u1-after/banc-apres.log", "description": "Run performance bank after optimization", "run_in_background": true … [1 caractères tronqués]`

  ```
started background job bash-43
  ```

- **job_output** `{"job_id": "bash-43", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
banc : contrôle de l'instrument…
banc : JSON → /tmp/u1-after/performance-apres.json
{
 "dix_mille_s": 1.323019509203732,
 "debit_mots_s": 7558.4675285843405,
 "rss_mio": 125.87890625,
 "json_octets": 14795890,
 "cent_ms": 1.1298754252493382,
 "alpha_bloc": 1.3102498216236458,
 "controle_lineaire": false,
 "tagger_disponible": false,
 "sortie": "/tmp/u1-after/performance-apres.json"
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['/tmp/u1-before/performance-avant.json','/tmp/u1-after/performance-apres.json']:\n d=json.load(open(p))\n b=d['echelle']['bloc_repete']\n print('\\n',p)\n for m in b['mesures']:\n  print(f\"{m['mots']:6d} {m['syntagmes']:5d} {m['duree_s']:.3f} rs … [456 caractères tronqués]`

  ```
/tmp/u1-before/performance-avant.json
   247   124 0.050 rss 37860
   494   248 0.113 rss 43108
   988   496 0.300 rss 51948
  1976   992 0.828 rss 70404
  3952  1984 2.461 rss 107564
  7904  3968 8.863 rss 181220
  9880  4960 13.691 rss 218652
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
AttributeError: 'list' object has no attribute 'items'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['/tmp/u1-before/performance-avant.json','/tmp/u1-after/performance-apres.json']:\n d=json.load(open(p))\n b=d['echelle']['bloc_repete']\n print('\\n',p)\n for m in b['mesures']:\n  print(f\"{m['mots']:6d} {m['syntagmes']:5d} {m['duree_s']:.3f} rs … [356 caractères tronqués]`

  ```
/tmp/u1-before/performance-avant.json
   247   124 0.050 rss 37860
   494   248 0.113 rss 43108
   988   496 0.300 rss 51948
  1976   992 0.828 rss 70404
  3952  1984 2.461 rss 107564
  7904  3968 8.863 rss 181220
  9880  4960 13.691 rss 218652
ajustements
  lineaire {'a': -1.23312608, 'b': 0.00137332, 'r2': 0.95855228, 'rmse': 1.01498999}
  quadratique {'a': 0.05448999, 'b': 0.00010075, 'c': 1.3e-07, 'r2': 0.99993354, 'rmse': 0.04064398}
  loglog {'alpha': 1.52996379, 'r2': 0.99474409, 'rmse': 0.14370054}
ajustements_syntagmes
  lineaire {'a': -1.23312608, 'b': 0.00273557, 'r2': 0.95855228, 'rmse': 1.01498999}
  quadratique {'a': 0.05448999, 'b': 0.00020068, 'c': 5.1e-07, 'r2': 0.99993354, 'rmse': 0.04064398}
  loglog {'alpha': 1.52996379, 'r2': 0.99474409, 'rmse': 0.14370054}
verdict {'resume': '10 000 mots exploitables ; contrôle de linéarité **échoue**', 'dix_mille_exploitable': True, 'debit_mots_s': 2505.7554658602085, 'controle_lineaire': False, 'alpha_bloc_repete': 1.52996378990646, 'alpha_prefixes_reels': 1.1224380133250769, 'raison': 'α = 1.53 sur le bloc répété (1 = linéaire, 2 = quadratique) ; le terme quadratique ajoute +0.041 de R².', 'prochaine_action': 'profiler et b
… [1506 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _profil\" -A80 tools/banc_performance.py", "description": "Read profile function"}`

  ```
628:def _profil(chemin: pathlib.Path, sortie: pathlib.Path) -> int:
629-    """cProfile sur `Heuristique.analyser` : les fonctions qui portent le temps."""
630-    import cProfile
631-    import pstats
632-
633-    if not chemin.is_absolute():
634-        chemin = RACINE / chemin
635-    texte = chemin.read_text(encoding="utf-8", errors="replace")
636-    h = bl.Heuristique()
637-    h.analyser("Le chat dort.")
638-    pr = cProfile.Profile()
639-    t0 = time.perf_counter()
640-    pr.enable()
641-    annotation = h.analyser(texte)
642-    pr.disable()
643-    duree = time.perf_counter() - t0
644-    stats = pstats.Stats(pr)
645-    stats.sort_stats("cumulative")
646-    fonctions = []
647-    for (fichier, ligne, nom), (cc, nc, tt, ct, _callers) in stats.stats.items():
648-        fonctions.append({"fonction": nom, "fichier": pathlib.Path(fichier).name,
649-                          "ligne": ligne, "appels": nc,
650-                          "temps_propre_s": round(tt, 3),
651-                          "temps_cumule_s": round(ct, 3)})
652-    fonctions.sort(key=lambda x: x["temps_cumule_s"], reverse=True)
653-    rapport = {
654-        "schema": "drave.performance.profil",
655- 
… [2386 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/banc_performance.py --profil work/banc-performance/bloc-x40.txt --sortie /tmp/u1-after/profil-x40.json 2>&1 | tail -20", "description": "Profile block x40 after fix"}`

  ```
[still running after 60000ms; moved to background job bash-47]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "grep -n \"deepcopy\" tools/bloc_linguistique.py", "description": "Find deepcopy calls"}`

  ```
111:    sortie = copy.deepcopy(meta)
2279:            return copy.deepcopy(self._cache[cle])
2413:            return copy.deepcopy(self._cache[cle])
2583:            return copy.deepcopy(self._cache[cle])
2758:                        vue["attachement"]["candidats"] = copy.deepcopy(att["candidats"])
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 - <<'PY'\nimport sys, time\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nbloc=open('work/banc-performance/bloc-controle.txt').read()\nfor k in (16,32,40):\n t='\\n\\n'.join([bloc]*k)\n t0=time.perf_counter(); a=h.analyser(t); d … [517 caractères tronqués]`

  ```
16 mots 3760 syn 1984 gv 704 time 1.197
 groupes 384 max 8 taille>1 384
32 mots 7520 syn 3968 gv 1408 time 3.825
 groupes 768 max 8 taille>1 768
40 mots 9400 syn 4960 gv 1760 time 5.606
 groupes 960 max 8 taille>1 960
  ```

- **job_output** `{"job_id": "bash-47", "timeout_ms": 240000, "wait": true}`

  ```
87.090 s         1  bloc_linguistique.py:1694  analyser
  38.081 s         1  bloc_linguistique.py:1084  _sujet_hors_gv
  37.093 s      3881  ~:0  <built-in method builtins.any>
  29.319 s   5609520  bloc_linguistique.py:1113  <genexpr>
  18.272 s  12582066  ~:0  <method 'get' of 'dict' objects>
   8.279 s         1  bloc_linguistique.py:2686  _expliciter_partition
   7.796 s    429058  copy.py:119  deepcopy
   7.674 s      6680  copy.py:192  _deepcopy_list
   6.592 s     76796  copy.py:218  _deepcopy_dict
   5.911 s     37360  bloc_linguistique.py:670  _est_verbe
   4.359 s         2  generateur.py:346  _segmente
   3.590 s         1  bloc_linguistique.py:1159  _syntagmes_s
profil → /tmp/u1-after/profil-x40.json  (87.1 s, 9880 mots, 4960 syntagmes)
[status: completed, exit code: 0]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 95, "offset": 1078}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1078:                 sortie.append(("préfixe", 0, len(pre), pre))
1079:                 break
1080:         return sortie
1081: 
1082:     # -- syntagmes ----------------------------------------------------------
1083: 
1084:     def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,
1085:                        pos_verbes: set[int] | None = None) -> list[dict] | None:
1086:         """La convention du gold : le sujet est un **GN**, pas le début du GV.
1087: 
1088:         Le générateur S rend « Il a couru », « Il ne dort pas », « Marie lit » comme un
1089:         seul GV : il inclut le sujet. Le gold sépare le GN agent du GV. On **déplace**
1090:         le sujet (pronom, clitique ou nom propre) hors du GV, sans toucher au générateur
1091:         S. Le GN sujet n'est créé que si un GN ne précède pas déjà immédiatement le GV.
1092:         """
1093:         if not cands:
1094:             return cands
1095:         pos_verbes = pos_verbes or set()
1096:         lex = POS_FERME.get(langue, POS_FERME["fr"])
1097:         _suj = SUJETS if langue =
… [4335 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        for c in cands:\n            segs = c.get(\"segments\") or []\n            # les fins de GN, triées : « un GN précède-t-il immédiatement ce GV ? » se\n            # répond en O(log g) a … [2189 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"gns_s = \\|_repli_cible_gp(texte, s\\|_cible_rel_sujet(\" tools/bloc_linguistique.py", "description": "Find per-loop GN list constructions"}`

  ```
1217:    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
1951:                        gns_s = [x for x in c.get("segments", []) if x.get("type") == "GN"]
1952:                        cible = (self._repli_cible_gp(texte, s, gns_s)
1982:                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
2011:                         or self._cible_rel_sujet(
2014:                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 85, "offset": 1908}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1908:         # S n'est pas modifié (lecture seule).
1909:         cands = self._sujet_hors_gv(texte, lg, cands, pos_verbes)
1910:         cibles_s = self._cibles_s(texte) if cands else {}
1911:         cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
1912:         # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
1913:         # le O(n²) mesuré venait des re-chunkings (A6, A11) — sortie identique (T178).
1914:         simples = self._syntagmes_simple(texte, lg, pos_verbes)
1915:         gvs_simple = [x for x in simples if x["type"] == "GV"]
1916:         if cands:
1917:             for c in cands[:1]:
1918:                 noms = [x.get("nom", "") for x in cands]
1919:                 gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
1920:                 deja = {(x["debut"], x["fin"]) for x in gvs_s}
1921:                 gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
1922:                 for s in c.get("segments", []):
1923:                     # la cible de S **
… [5178 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 55, "offset": 1993}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1993:                 etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
1994:                                             s["fin"], self.nom, 0.35,
1995:                                             candidats=candidats,
1996:                                             langue=lg, script=script, meta=meta))
1997:                 prec = s
1998:         # 5 bis. union : les segments du chunker que le générateur S ne fournit pas
1999:         if cands and self.union:
2000:             deja = {(s.get("type"), s.get("debut"), s.get("fin"))
2001:                     for s in cands[0].get("segments", [])}
2002:             gvs_u = ([x for x in cands[0].get("segments", []) if x.get("type") == "GV"]
2003:                      + gvs_simple)
2004:             prec = None
2005:             for s in simples:
2006:                 if (s["type"], s["debut"], s["fin"]) in deja:
2007:                     prec = s
2008:                     continue
2009:                 meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
2010:                 cible =
… [2547 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        simples = self._syntagmes_simple(texte, lg, pos_verbes)\n        gvs_simple = [x for x in simples if x[\"type\"] == \"GV\"]\n        gns_simple = [x for x in simples if x[\"type\"] == \ … [1105 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                    if not cible:\n                        cible = (self._repli_cible_gp(texte, s, gns_s)\n                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv … [316 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                cible = (self._cible_precedent(texte, s, prec, verbes)\n                         or self._repli_cible_gp(texte, s, gns_simple)\n                         or self._cible_proche(te … [314 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "            gvs_u = ([x for x in cands[0].get(\"segments\", []) if x.get(\"type\") == \"GV\"]\n                     + gvs_simple)\n            tous_u = list(cands[0].get(\"segments\", [])) + li … [1450 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m py_compile tools/bloc_linguistique.py && PYTHONHASHSEED=0 python3 -m unittest tools.tests.linguistique.test_bloc_linguistique 2>&1 | tail -5", "description": "Compile and test after changes"}`

  ```
....................
----------------------------------------------------------------------
Ran 20 tests in 0.082s

OK
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 /tmp/gen_annotations.py /tmp/u1-after", "description": "Generate after annotation JSONs", "run_in_background": true}`

  ```
started background job bash-52
  ```

- **job_output** `{"job_id": "bash-52", "timeout_ms": 120000, "wait": true}`

  ```
corpus 10000 56862
bloc 0 1572 247
bloc 1 1407 247
bloc 2 2815 494
bloc 4 5631 988
bloc 8 11263 1976
bloc 16 22527 3952
bloc 32 45055 7904
bloc 40 56319 9880
gold 612 reel 452
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /tmp && for f in u1-before/*.json; do b=$(basename \"$f\"); if [ -f \"u1-after/$b\" ]; then if cmp -s \"$f\" \"u1-after/$b\"; then echo \"IDENTIQUE $b ($(wc -c < \"$f\") octets)\"; else echo \"DIFF $b\"; cmp \"$f\" \"u1-after/$b\" | head -2; fi; fi; done", "description": "Compare bef … [28 caractères tronqués]`

  ```
IDENTIQUE bloc-x16.json (7263340 octets)
IDENTIQUE bloc-x1.json (449558 octets)
IDENTIQUE bloc-x2.json (901533 octets)
IDENTIQUE bloc-x32.json (14552604 octets)
IDENTIQUE bloc-x40.json (18197238 octets)
IDENTIQUE bloc-x4.json (1805483 octets)
IDENTIQUE bloc-x8.json (3618708 octets)
IDENTIQUE corpus-10000.json (16457228 octets)
IDENTIQUE gold-annotations-452.json (3222340 octets)
IDENTIQUE gold-annotations-612.json (4281465 octets)
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/banc_performance.py --sortie /tmp/u1-after/performance-apres2.json --repetitions 3 > /tmp/u1-after/banc-apres2.log 2>&1; echo EXIT:$?; tail -15 /tmp/u1-after/banc-apres2.log", "description": "Rerun performance bank after subject fix", "run_in_background":  … [5 caractères tronqués]`

  ```
started background job bash-54
  ```

- **job_output** `{"job_id": "bash-54", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
banc : contrôle de l'instrument…
banc : JSON → /tmp/u1-after/performance-apres2.json
{
 "dix_mille_s": 0.8815991671290249,
 "debit_mots_s": 11343.023420230236,
 "rss_mio": 126.44921875,
 "json_octets": 14795890,
 "cent_ms": 1.1687774676829576,
 "alpha_bloc": 1.1632869354314745,
 "controle_lineaire": false,
 "tagger_disponible": false,
 "sortie": "/tmp/u1-after/performance-apres2.json"
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/u1-after/performance-apres2.json'))\nb=d['echelle']['bloc_repete']\nfor m in b['mesures']:\n print(f\"{m['mots']:6d} {m['syntagmes']:5d} {m['duree_s']:.4f} rss {m['rss_kb']}\")\nfor key in ('lineaire','quadratique','loglog'):\n v=b[' … [279 caractères tronqués]`

  ```
247   124 0.0449 rss 37812
   494   248 0.0996 rss 43076
   988   496 0.1958 rss 51108
  1976   992 0.4074 rss 70260
  3952  1984 0.9357 rss 107732
  7904  3968 2.4518 rss 182560
  9880  4960 3.4823 rss 219268
lineaire {'a': -0.17999064, 'b': 0.00034894, 'r2': 0.98414097, 'rmse': 0.1574363}
quadratique {'a': 0.01946621, 'b': 0.00015181, 'c': 2e-08, 'r2': 0.99993229, 'rmse': 0.01028681}
loglog {'alpha': 1.16328694, 'r2': 0.99584033, 'rmse': 0.09714721}
delta R2 0.015791327849435155
{'resume': '10 000 mots exploitables ; contrôle de linéarité **échoue**', 'dix_mille_exploitable': True, 'debit_mots_s': 11343.023420230236, 'controle_lineaire': False, 'alpha_bloc_repete': 1.1632869354314745, 'alpha_prefixes_reels': 0.7150410898651197, 'raison': 'α = 1.16 sur le bloc répété (1 = linéaire, 2 = quadratique) ; le terme quadratique ajoute +0.016 de R².', 'prochaine_action': 'profiler et borner `_groupes_partition` (O(k²) sur les syntagmes) et `_cible_proche` (tri de tous les GV par segment) ; mesurer k = syntagmes, pas seulement les mots.'}
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/banc_performance.py --profil work/banc-performance/bloc-x40.txt --sortie /tmp/u1-after/profil-x40-2.json > /tmp/u1-after/profil2.log 2>&1; echo EXIT:$?; tail -15 /tmp/u1-after/profil2.log", "description": "Profile x40 after subject fix", "run_in_background … [8 caractères tronqués]`

  ```
started background job bash-56
  ```

- **job_output** `{"job_id": "bash-56", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
  46.165 s         1  bloc_linguistique.py:1710  analyser
   8.079 s         1  bloc_linguistique.py:2703  _expliciter_partition
   7.598 s    429058  copy.py:119  deepcopy
   7.479 s      6680  copy.py:192  _deepcopy_list
   7.031 s   4867546  ~:0  <method 'get' of 'dict' objects>
   6.417 s     76796  copy.py:218  _deepcopy_dict
   5.647 s     37360  bloc_linguistique.py:670  _est_verbe
   4.271 s         2  generateur.py:346  _segmente
   3.560 s         1  bloc_linguistique.py:1175  _syntagmes_s
   3.557 s         1  generateur.py:516  analyser
   3.471 s     88867  generateur.py:134  _norm
   3.412 s         1  bloc_linguistique.py:1186  _cibles_s
profil → /tmp/u1-after/profil-x40-2.json  (46.2 s, 9880 mots, 4960 syntagmes)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cat > /tmp/prof_detail.py <<'PY'\nimport sys, cProfile, pstats, io, time\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nbloc=open('work/banc-performance/bloc-controle.txt').read()\nk=int(sys.argv[1]) if len(sys.argv)>1 else 32\ntexte='\\n\\n'.join([bloc]*k)\nh=bl.Heuristiq … [974 caractères tronqués]`

  ```
started background job bash-57
  ```

- **bash** `{"command": "sed -n '1200,1265p' tools/bloc_linguistique.py", "description": "Read _cible_rel_sujet"}`

  ```
except Exception:
            return {}

    @staticmethod
    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
        if not precedent:
            return None
        if segment.get("type") == "REL" and precedent.get("type") == "GN":
            return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
            if _est_adverbe_seul(precedent):
                return None
            return Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"], verbes)
        return None

    @staticmethod
    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
        """REL **suivie d'un GV** : le sujet de ce GV (le GN le plus proche à gauche).

        Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
        sujet du GV `nage`. La règle ne s'applique qu'aux REL sans antécédent dans le
        chemin courant (union S/chunker) et exige un GV à droite **et** un GN à gauche.
        La règle littéra
… [1853 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-57", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
=== cumulatif (filtre) ===
  35.131 cum    3.025 own         1 appels  analyser  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1710)
   6.395 cum    0.152 own         1 appels  _expliciter_partition  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:2703)
   6.017 cum    2.607 own    343242 appels  deepcopy  (/usr/lib64/python3.13/copy.py:119)
   5.921 cum    0.110 own      5344 appels  _deepcopy_list  (/usr/lib64/python3.13/copy.py:192)
   5.138 cum    0.790 own     61436 appels  _deepcopy_dict  (/usr/lib64/python3.13/copy.py:218)
   4.812 cum    4.812 own   3301650 appels  <method 'get' of 'dict' objects>  (~:0)
   4.728 cum    1.874 own     29888 appels  _est_verbe  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:670)
   3.375 cum    0.811 own         2 appels  _segmente  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py:346)
   2.912 cum    0.457 own     71091 appels  _norm  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py:134)
   2.894 cum    0.002 own         1 appels  _syntagmes_s  (/home/stephane/Data13TB/stephane/GitHub/Qtr
… [4484 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 15, "offset": 648}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
648:     entree = index.get(id(gvs))
649:     if entree is None or entree[0] is not gvs:
650:         entree = (gvs, _IndexGV(gvs))
651:         index[id(gvs)] = entree
652:     return entree[1]
653: 
654: 
655: 
656: MODAUX = {"would", "must", "can", "could", "should", "will", "shall", "may", "might", "ought",
657:           "could", "cannot"}
658: 
659: ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")
660: 
661: 
662: def _sans_enclitique(mot: str) -> str:

(Showing lines 648-662 of 3180. Use offset=663 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "    entree = index.get(id(gvs))\n    if entree is None or entree[0] is not gvs:\n        entree = (gvs, _IndexGV(gvs))\n        index[id(gvs)] = entree\n    return entree[1]\n\n\nclass _IndexFi … [1852 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"def _cible_rel_sujet\\|def _repli_cible_gp\" tools/bloc_linguistique.py", "description": "Locate functions"}`

  ```
1260:    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
1369:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 28, "offset": 1260}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 20, "offset": 1369}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1260:     def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
1261:         """REL **suivie d'un GV** : le sujet de ce GV (le GN le plus proche à gauche).
1262: 
1263:         Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
1264:         sujet du GV `nage`. La règle ne s'applique qu'aux REL sans antécédent dans le
1265:         chemin courant (union S/chunker) et exige un GV à droite **et** un GN à gauche.
1266:         La règle littérale « REL après un GV » ne s'applique à aucun segment du gold.
1267:         """
1268:         if segment.get("type") != "REL":
1269:             return None
1270:         droites = [x for x in tous if x.get("type") == "GV"
1271:                    and x.get("debut", 0) >= segment.get("fin", 0)]
1272:         if not droites:
1273:             return None
1274:         gauches = [x for x in tous if x.get("type") == "GN"
1275:                    and x.get("fin", 0) <= segment.get("debut", 0)]
1276:         if not gauches:
1277:             return None
1278:         gn = max(gauc
… [614 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1369:     def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
1370:         """Cible vide d'un GP : génitif → tête du GN à gauche (sinon None, le GV tranchera)."""
1371:         if segment.get("type") != "GP":
1372:             return None
1373:         premier = (segment.get("texte") or "").split()[:1]
1374:         prep = _normaliser(premier[0]) if premier else ""
1375:         if prep not in ("de", "du", "des", "d", "of", "from"):
1376:             return None
1377:         gauche = [g for g in gns if g.get("fin", 0) <= segment.get("debut", 0)]
1378:         if not gauche:
1379:             return None
1380:         g = max(gauche, key=lambda x: x["fin"])
1381:         return Heuristique._tete_nom(texte, g["debut"], g["fin"])
1382: 
1383:     @staticmethod
1384:     def _repli_verbe_propre(texte: str, segment: dict, cible: str | None):
1385:         """Sans gouverneur extérieur, une SUB/REL prend son propre verbe (« qu'il viendra »)."""
1386:         if cible or segment.get("type") not in ("SUB", "REL"):
1387:             return cible
138
… [167 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict],\n                         index: _IndexSegments | None = None) -> str | None:\n        \"\"\"REL **suivie d'un GV** : le su … [1741 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict],\n                        index: _IndexFins | None = None) -> str | None:\n        \"\"\"Cible vide d'un GP : génitif → tête d … [1343 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"_repli_cible_gp(texte, s\\|_cible_rel_sujet(texte, s\" tools/bloc_linguistique.py", "description": "Find calls to update"}`

  ```
1993:                        cible = (self._repli_cible_gp(texte, s, gns_s)
2023:                         or self._repli_cible_gp(texte, s, gns_simple)
2053:                         or self._cible_rel_sujet(texte, s, tous_u)
2054:                         or self._repli_cible_gp(texte, s, gns_simple)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 20, "offset": 1953}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1953:         simples = self._syntagmes_simple(texte, lg, pos_verbes)
1954:         gvs_simple = [x for x in simples if x["type"] == "GV"]
1955:         gns_simple = [x for x in simples if x["type"] == "GN"]
1956:         if cands:
1957:             for c in cands[:1]:
1958:                 noms = [x.get("nom", "") for x in cands]
1959:                 segments_c = c.get("segments", [])
1960:                 gns_s = [x for x in segments_c if x.get("type") == "GN"]
1961:                 gvs_s = [x for x in segments_c if x.get("type") == "GV"]
1962:                 deja = {(x["debut"], x["fin"]) for x in gvs_s}
1963:                 gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
1964:                 for s in segments_c:
1965:                     # la cible de S **convertie en son verbe** : « Les enfants jouent » →
1966:                     # `jouent` (le gold attend le verbe, pas le GN) ; à défaut, le GV le plus
1967:                     # proche. Mesuré : 82 cibles justes dans les candidats, 33 choisies avant.
1968:                     # l
… [406 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        simples = self._syntagmes_simple(texte, lg, pos_verbes)\n        gvs_simple = [x for x in simples if x[\"type\"] == \"GV\"]\n        gns_simple = [x for x in simples if x[\"type\"] == \ … [969 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                        cible = (self._repli_cible_gp(texte, s, gns_s, idx_gns_s)\n                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))", "old_string": "     … [158 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                cible = (self._cible_precedent(texte, s, prec, verbes)\n                         or self._repli_cible_gp(texte, s, gns_simple, idx_gns_simple)\n                         or self. … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "            tous_u = list(cands[0].get(\"segments\", [])) + list(simples)\n            idx_tous_u = _IndexSegments(tous_u)\n            prec = None\n            for s in simples:\n              … [1198 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"deepcopy(att\" tools/bloc_linguistique.py", "description": "Find deepcopy candidates"}`

  ```
2817:                        vue["attachement"]["candidats"] = copy.deepcopy(att["candidats"])
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 14, "offset": 2808}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2808:                        "relation": _relation_partition(e, autre),
2809:                        "rang": rangs[id(autre)][1]}
2810:                 if filtrer:
2811:                     vue["retire"] = id(autre) in retirees
2812:                 att = (autre.meta or {}).get("attachement")
2813:                 if att:
2814:                     vue["attachement"] = {"segment": att.get("segment", ""),
2815:                                           "cible": att.get("cible", "")}
2816:                     if att.get("candidats"):
2817:                         vue["attachement"]["candidats"] = copy.deepcopy(att["candidats"])
2818:                 role = (autre.meta or {}).get("role")
2819:                 if role:
2820:                     vue["role"] = role
2821:                 vues.append(vue)

(Showing lines 2808-2821 of 3222. Use offset=2822 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                    if att.get(\"candidats\"):\n                        # copie **superficielle** : la liste des candidats n'est plus\n                        # modifiée après la partition (le  … [283 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m py_compile tools/bloc_linguistique.py && echo OK && PYTHONHASHSEED=0 python3 -m unittest tools.tests.linguistique.test_bloc_linguistique 2>&1 | tail -4", "description": "Compile and test"}`

  ```
OK
----------------------------------------------------------------------
Ran 20 tests in 0.078s

OK
  ```

- **bash** `{"command": "cat > /tmp/diff_idx.py <<'PY'\nimport sys, random\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\n\nrng=random.Random(1)\ndef ref_gp(texte, seg, gns):\n    if seg.get('type')!='GP': return None\n    premier=(seg.get('texte') or '').split()[:1]\n    prep=bl._normaliser(premi … [2063 caractères tronqués]`

  ```
indices OK
  ```

- **bash** `{"command": "rm -rf /tmp/u1-after3 && PYTHONHASHSEED=0 python3 /tmp/gen_annotations.py /tmp/u1-after3 > /tmp/u1-after3.log 2>&1; echo EXIT:$?; tail -12 /tmp/u1-after3.log; for f in /tmp/u1-before/*.json; do b=$(basename \"$f\"); if [ -f \"/tmp/u1-after3/$b\" ]; then cmp -s \"$f\" \"/tmp/u1-after3/$b … [138 caractères tronqués]`

  ```
started background job bash-64
  ```

- **job_output** `{"job_id": "bash-64", "timeout_ms": 120000, "wait": true}`

  ```
EXIT:0
corpus 10000 56862
bloc 0 1572 247
bloc 1 1407 247
bloc 2 2815 494
bloc 4 5631 988
bloc 8 11263 1976
bloc 16 22527 3952
bloc 32 45055 7904
bloc 40 56319 9880
gold 612 reel 452
IDENTIQUE bloc-x16.json
IDENTIQUE bloc-x1.json
IDENTIQUE bloc-x2.json
IDENTIQUE bloc-x32.json
IDENTIQUE bloc-x40.json
IDENTIQUE bloc-x4.json
IDENTIQUE bloc-x8.json
IDENTIQUE corpus-10000.json
IDENTIQUE gold-annotations-452.json
IDENTIQUE gold-annotations-612.json
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/banc_performance.py --sortie /tmp/u1-after/performance-apres3.json --repetitions 3 > /tmp/u1-after/banc-apres3.log 2>&1; echo EXIT:$?; tail -12 /tmp/u1-after/banc-apres3.log", "description": "Run bank after index optimizations", "run_in_background": true}`

  ```
started background job bash-65
  ```

- **job_output** `{"job_id": "bash-65", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
banc : JSON → /tmp/u1-after/performance-apres3.json
{
 "dix_mille_s": 0.807899242034182,
 "debit_mots_s": 12377.781138674349,
 "rss_mio": 127.15625,
 "json_octets": 14795890,
 "cent_ms": 1.120131928473711,
 "alpha_bloc": 1.194635332178568,
 "controle_lineaire": false,
 "tagger_disponible": false,
 "sortie": "/tmp/u1-after/performance-apres3.json"
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['/tmp/u1-after/performance-apres2.json','/tmp/u1-after/performance-apres3.json']:\n d=json.load(open(p)); b=d['echelle']['bloc_repete']\n print(p)\n for m in b['mesures']: print(f\"  {m['mots']:6d} {m['duree_s']:.4f}\")\n for k in ('lineaire','qu … [284 caractères tronqués]`

  ```
/tmp/u1-after/performance-apres2.json
     247 0.0449
     494 0.0996
     988 0.1958
    1976 0.4074
    3952 0.9357
    7904 2.4518
    9880 3.4823
  lineaire {'r2': 0.98414097, 'rmse': 0.1574363}
  quadratique {'c': 2e-08, 'r2': 0.99993229, 'rmse': 0.01028681}
  loglog {'alpha': 1.16328694, 'r2': 0.99584033, 'rmse': 0.09714721}
 delta 0.015791327849435155
/tmp/u1-after/performance-apres3.json
     247 0.0355
     494 0.0817
     988 0.1677
    1976 0.3533
    3952 0.8167
    7904 2.2676
    9880 3.0310
  lineaire {'r2': 0.98716289, 'rmse': 0.12588312}
  quadratique {'c': 2e-08, 'r2': 0.99923855, 'rmse': 0.03065872}
  loglog {'alpha': 1.19463533, 'r2': 0.99669387, 'rmse': 0.08890445}
 delta 0.012075658567928249
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 /tmp/prof_detail.py 32 > /tmp/u1-after/prof_detail3.txt 2>&1; echo EXIT:$?; sed -n '1,45p' /tmp/u1-after/prof_detail3.txt", "description": "Detailed profile after index/deepcopy fixes", "run_in_background": true}`

  ```
started background job bash-67
  ```

- **bash** `{"command": "sed -n '330,560p' tools/structures/generateur.py", "description": "Read generator segmentation"}`

  ```
elif s.type in ("GV", "GN"):
            s.parent, s.profondeur = racine, 1
        else:
            parent = None
            for t in reversed(segs[:k]):
                if t.type in ("GN", "GP", "GV"):
                    parent = t
                    break
            if parent is None:
                parent = segs[racine]
            s.parent = segs.index(parent)
            s.profondeur = parent.profondeur + 1
    for s in segs:
        s.niveau = s.profondeur


def _segmente(texte: str, toks: list[Token]) -> list[Segment]:
    utiles = [t for t in toks if t.cls != "ESPACE"]
    segs: list[Segment] = []
    i = 0
    while i < len(utiles):
        t = utiles[i]
        if t.cls == "PONCT":
            i += 1
            continue
        marqueur = _marqueur(utiles, i)
        if marqueur:
            # « parce qu'elle est fatiguée », « bien qu'il soit tard » : la subordonnée
            # commence au subordonnant et va jusqu'à la ponctuation ou la coordination.
            j = _fin_clause(utiles, i + 1)
            segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                "SUB", marqueur, 1))
            i = j
       
… [9988 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def construire_arbre\" -A60 tools/structures/generateur.py", "description": "Read construire_arbre"}`

  ```
319:def construire_arbre(segs: list["Segment"]) -> None:
320-    """Le père et la profondeur : le GV principal est la racine, les GN ses enfants, et les
321-    GP/REL/SUB s'accrochent au plus proche segment à gauche (GN, GP ou GV). L'indentation
322-    (`niveau`) devient la profondeur réelle, pas un niveau plat par type."""
323-    if not segs:
324-        return
325-    gv = [k for k, s in enumerate(segs) if s.type == "GV"]
326-    racine = gv[0] if gv else 0
327-    for k, s in enumerate(segs):
328-        if k == racine:
329-            s.parent, s.profondeur = None, 0
330-        elif s.type in ("GV", "GN"):
331-            s.parent, s.profondeur = racine, 1
332-        else:
333-            parent = None
334-            for t in reversed(segs[:k]):
335-                if t.type in ("GN", "GP", "GV"):
336-                    parent = t
337-                    break
338-            if parent is None:
339-                parent = segs[racine]
340-            s.parent = segs.index(parent)
341-            s.profondeur = parent.profondeur + 1
342-    for s in segs:
343-        s.niveau = s.profondeur
344-
345-
346-def _segmente(texte: str, toks: list[Token]) -> list[Segment]:
347-
… [1699 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _role_gp\" -A80 tools/structures/generateur.py", "description": "Read _role_gp"}`

  ```
246:def _role_gp(prep: str, segs: list["Segment"], utiles: list[Token], i: int) -> str:
247-    """Le rôle du GP, par la préposition **et son contexte** (ce qui précède, ce qui suit).
248-
249-    Le contexte est ce qui distingue « de la voisine » (possession, après un GN) de
250-    « de son projet » (thème, après un GV), « à manger » (but, infinitif) de « à Marie »
251-    (destinataire), ou « par Marie » (agent, après un passif) de « par la porte » (moyen).
252-    """
253-    def _proche(types: tuple[str, ...]) -> "Segment | None":
254-        for s in reversed(segs):
255-            if s.type in types:
256-                return s
257-        return None
258-
259-    if prep in {"de", "du", "des", "d"}:
260-        proche = _proche(("GN", "GV"))
261-        return "possession" if proche is not None and proche.type == "GN" else "theme"
262-    if prep in {"a", "au", "aux"}:
263-        if i + 1 < len(utiles) and _infinitif(utiles[i + 1]):
264-            return "but"
265-        gv = _proche(("GV",))
266-        if gv is not None and _dernier_mot(gv.texte) in VERBES_LIEU:
267-            return "lieu"
268-        return "destinataire"
269-    if prep == "avec":
270-        retu
… [2391 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "limit": 28, "offset": 319}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "limit": 22, "offset": 455}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
319: def construire_arbre(segs: list["Segment"]) -> None:
320:     """Le père et la profondeur : le GV principal est la racine, les GN ses enfants, et les
321:     GP/REL/SUB s'accrochent au plus proche segment à gauche (GN, GP ou GV). L'indentation
322:     (`niveau`) devient la profondeur réelle, pas un niveau plat par type."""
323:     if not segs:
324:         return
325:     gv = [k for k, s in enumerate(segs) if s.type == "GV"]
326:     racine = gv[0] if gv else 0
327:     for k, s in enumerate(segs):
328:         if k == racine:
329:             s.parent, s.profondeur = None, 0
330:         elif s.type in ("GV", "GN"):
331:             s.parent, s.profondeur = racine, 1
332:         else:
333:             parent = None
334:             for t in reversed(segs[:k]):
335:                 if t.type in ("GN", "GP", "GV"):
336:                     parent = t
337:                     break
338:             if parent is None:
339:                 parent = segs[racine]
340:             s.parent = segs.index(parent)
341:             s.profondeur = parent.profondeur +
… [215 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
455:                 break
456:             if (j > i and utiles[j].cls == "MOT"
457:                     and _norm(utiles[j].texte) in ADVERBES_TEMPS):
458:                 break
459:             j += 1
460:         if j == i:
461:             j = i + 1
462:         # copule + groupe nominal attribut : « est mon voisin » ne se coupe pas en « est » + GN.
463:         if (j < len(utiles) and utiles[j].cls == "DET"
464:                 and _norm(utiles[j - 1].texte) in COPULES):
465:             k, mots = j + 1, 0
466:             while k < len(utiles) and utiles[k].cls in ("DET", "MOT") and mots < 3:
467:                 if utiles[k].cls == "MOT":
468:                     mots += 1
469:                 k += 1
470:             j = k
471:         segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
472:                             "GV", "predicat", 0))
473:         i = j
474:     # Le passif : « a été écrite par Marie » — le GN sujet est patient, « par » est agent.
475:     for k, s in enumerate(segs):
476:         if s.type == "GV" and l
… [140 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "limit": 30, "offset": 474}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
474:     # Le passif : « a été écrite par Marie » — le GN sujet est patient, « par » est agent.
475:     for k, s in enumerate(segs):
476:         if s.type == "GV" and len(_norm(s.texte).split()) >= 3 and "ete" in _norm(s.texte).split():
477:             for g in reversed(segs[:k]):
478:                 if g.type == "GN":
479:                     g.role = "patient"
480:                     break
481:             for g in segs[k + 1:]:
482:                 if g.type == "GP" and _norm(g.texte).split()[:1] == ["par"]:
483:                     g.role = "agent"
484:                     break
485:     # les cibles d'attachement : GN, tête du GP et GV les plus proches à gauche
486:     def _tete_gp(g):
487:         mots = [m for m in MOTIF.finditer(texte, g.debut, g.fin) if m.group().strip()
488:                 and _norm(m.group()) not in PREP | DET]
489:         return mots[-1].group() if mots else None
490:     for k, s in enumerate(segs):
491:         for g in reversed(segs[:k]):
492:             if g.type == "GN" and s.cible_nom is None:
493:                 s.cibl
… [411 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "new_string": "def construire_arbre(segs: list[\"Segment\"]) -> None:\n    \"\"\"Le père et la profondeur : le GV principal est la racine, les GN ses enfants, et les\n    GP/REL/SUB s'accrochent au plus p … [1990 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

### 👤 Utilisateur

background job bash-67 (bash: PYTHONHASHSEED=0 python3 /tmp/prof_detail.py 32 > /tmp/u1-after/prof_detail3.txt 2>&1; echo EXIT:$?; sed -n '1,45p' /tmp/u1-after/prof_detail3.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "new_string": "    # les cibles d'attachement : GN, tête du GP et GV les plus proches à gauche\n    def _tete_gp(g):\n        mots = [m for m in MOTIF.finditer(texte, g.debut, g.fin) if m.group().strip()\ … [1686 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **bash** `{"command": "sed -n '1,60p' tools/structures/generateur.py", "description": "Check generator imports"}`

  ```
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".split())
SU
… [2719 caractères tronqués]
  ```

- **bash** `{"command": "git show HEAD:tools/structures/generateur.py > /tmp/generateur_old.py\ncat > /tmp/diff_gen.py <<'PY'\nimport sys, json, importlib.util\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/structures')\nimport generateur as new\nspec=importlib.util.spec_from_file_location('gen_old','/tm … [1292 caractères tronqués]`

  ```
started background job bash-72
  ```

- **job_output** `{"job_id": "bash-72", "timeout_ms": 180000, "wait": true}`

  ```
[stderr]
fatal: path 'tools/structures/generateur.py' exists on disk, but not in 'HEAD'
Traceback (most recent call last):
  File "/tmp/diff_gen.py", line 22, in <module>
    a=new.analyser(t); b=old.analyser(t)
                         ^^^^^^^^^^^^
AttributeError: module 'gen_old' has no attribute 'analyser'
[status: completed, exit code: 1]
  ```

- **bash** `{"command": "git ls-files tools/structures | head; ls -la tools/structures/generateur.py; git status --short tools/structures/generateur.py; git check-ignore -v tools/structures/generateur.py; cat .gitmodules 2>/dev/null | head -40", "description": "Check generator tracking"}`

  ```
tools/structures
-rw-r--r--. 1 stephane stephane 31037 16 nov 00:04 tools/structures/generateur.py
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
[stderr]
fatal: Pathspec 'tools/structures/generateur.py' is in submodule 'tools/structures'
  ```

- **bash** `{"command": "git -C tools/structures status --short; git -C tools/structures log --oneline -3; git -C tools/structures show HEAD:generateur.py > /tmp/generateur_old.py && wc -l /tmp/generateur_old.py", "description": "Get old generator from submodule HEAD"}`

  ```
M generateur.py
389b99f S — LES 11 VERDICTS HUMAINS DE /paragraphes (a004–a009) : 19/19 CANDIDATS JUGÉS, 11 ACCEPTÉS, 8 EXCLUS ; DÉCISION DU 14/11 (3B), EXCEPTION AUTORISÉE
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
648 /tmp/generateur_old.py
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 /tmp/diff_gen.py", "description": "Differential test generator", "run_in_background": true}`

  ```
started background job bash-75
  ```

- **job_output** `{"job_id": "bash-75", "timeout_ms": 180000, "wait": true}`

  ```
generateur identique sur 620 textes
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m py_compile tools/bloc_linguistique.py tools/structures/generateur.py && python3 -m unittest tools.tests.linguistique.test_bloc_linguistique 2>&1 | tail -4", "description": "Compile and test after generator fix"}`

  ```
----------------------------------------------------------------------
Ran 20 tests in 0.080s

OK
  ```

- **bash** `{"command": "rm -rf /tmp/u1-after4 && PYTHONHASHSEED=0 python3 /tmp/gen_annotations.py /tmp/u1-after4 > /tmp/u1-after4.log 2>&1; echo EXIT:$?; for f in /tmp/u1-before/*.json; do b=$(basename \"$f\"); cmp -s \"$f\" \"/tmp/u1-after4/$b\" && echo \"IDENTIQUE $b\" || echo \"DIFF $b\"; done", "descriptio … [67 caractères tronqués]`

  ```
started background job bash-77
  ```

- **job_output** `{"job_id": "bash-77", "timeout_ms": 120000, "wait": true}`

  ```
EXIT:0
IDENTIQUE bloc-x16.json
IDENTIQUE bloc-x1.json
IDENTIQUE bloc-x2.json
IDENTIQUE bloc-x32.json
IDENTIQUE bloc-x40.json
IDENTIQUE bloc-x4.json
IDENTIQUE bloc-x8.json
IDENTIQUE corpus-10000.json
IDENTIQUE gold-annotations-452.json
IDENTIQUE gold-annotations-612.json
DIFF gold-avant.json
DIFF performance-avant.json
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/banc_performance.py --sortie /tmp/u1-after/performance-apres4.json --repetitions 3 > /tmp/u1-after/banc-apres4.log 2>&1; echo EXIT:$?; tail -12 /tmp/u1-after/banc-apres4.log", "description": "Run bank after generator fixes", "run_in_background": true}`

  ```
started background job bash-78
  ```

- **job_output** `{"job_id": "bash-78", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
banc : JSON → /tmp/u1-after/performance-apres4.json
{
 "dix_mille_s": 0.8157198431435972,
 "debit_mots_s": 12259.110874957134,
 "rss_mio": 127.39453125,
 "json_octets": 14795890,
 "cent_ms": 1.0933474404737353,
 "alpha_bloc": 1.0759394426955102,
 "controle_lineaire": true,
 "tagger_disponible": false,
 "sortie": "/tmp/u1-after/performance-apres4.json"
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['/tmp/u1-before/performance-avant.json','/tmp/u1-after/performance-apres4.json']:\n d=json.load(open(p)); b=d['echelle']['bloc_repete']\n print('\\n',p)\n for m in b['mesures']: print(f\"  {m['mots']:6d} {m['syntagmes']:5d} {m['duree_s']:.4f} rss … [441 caractères tronqués]`

  ```
/tmp/u1-before/performance-avant.json
     247   124 0.0501 rss 37860
     494   248 0.1134 rss 43108
     988   496 0.2999 rss 51948
    1976   992 0.8278 rss 70404
    3952  1984 2.4613 rss 107564
    7904  3968 8.8631 rss 181220
    9880  4960 13.6912 rss 218652
  lineaire {'a': -1.2331260809, 'b': 0.001373324, 'r2': 0.9585522819, 'rmse': 1.0149899939}
  quadratique {'a': 0.0544899868, 'b': 0.0001007476, 'c': 1.292e-07, 'r2': 0.9999335386, 'rmse': 0.0406439798}
  loglog {'alpha': 1.5299637899, 'r2': 0.9947440864, 'rmse': 0.1437005395}
 deltaR2 0.04138125664523007
 verdict 10 000 mots exploitables ; contrôle de linéarité **échoue** False 1.52996378990646

 /tmp/u1-after/performance-apres4.json
     247   124 0.0323 rss 37724
     494   248 0.0778 rss 42372
     988   496 0.1440 rss 50788
    1976   992 0.3083 rss 67784
    3952  1984 0.6180 rss 101708
    7904  3968 1.4782 rss 170980
    9880  4960 1.7772 rss 205692
  lineaire {'a': -0.0387507812, 'b': 0.0001850193, 'r2': 0.9966161246, 'rmse': 0.0383183284}
  quadratique {'a': -0.0155258326, 'b': 0.0001620656, 'c': 2.3e-09, 'r2': 0.9973873202, 'rmse': 0.0336699493}
  loglog {'alpha': 1.0759394427, 'r2': 0.9985052409, 'rmse': 0.05
… [132 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/u1-after/gold-apres.json > /tmp/u1-after/gold-apres.log 2>&1; echo EXIT:$?; python3 - <<'PY'\nimport json\na=json.load(open('/tmp/u1-before/gold-avant.json')); b=json.load(open('/tmp/u1-after/gold-apres.json') … [762 caractères tronqués]`

  ```
EXIT:0
gold counts {'phrases': 612, 'reel': 452, 'hand': 20, 'reel_new': 432, 'synthetique': 160, 'tokens': 3179} {'phrases': 612, 'reel': 452, 'hand': 20, 'reel_new': 432, 'synthetique': 160, 'tokens': 3179}
all pos 0.8625 0.8625 seg f1 0.7902 0.7902 att topk 0.9874 0.9874 att exact 1.0 1.0
reel pos 0.8891 0.8891 seg f1 0.7906 0.7906 att topk 0.9891 0.9891 att exact 1.0 1.0
hand pos 0.8857 0.8857 seg f1 0.9016 0.9016 att topk 0.9231 0.9231 att exact 1.0 1.0
synthetique pos 0.7682 0.7682 seg f1 0.7888 0.7888 att topk 0.9818 0.9818 att exact 1.0 1.0
verdict identique True ok True True
json complet identique (hors date): True
  ```

- **bash** `{"command": "ls tools/structures | head -40; ls tools/structures/tests 2>/dev/null | head; git -C tools/structures status --short", "description": "Check submodule tests"}`

  ```
arbre_svg.py
candidats_corpus.py
construire_donnees.py
donnees
exporter_corpus.py
generateur.py
llm.py
mesure_analyseur.py
mesure_arbre.py
mesure_corpus.py
__pycache__
README.md
serveur.py
static
tests
verifier_corpus.py
__pycache__
test_arbre_svg.py
test_candidats_corpus.py
test_export.py
test_generateur.py
test_mesure_corpus.py
test_serveur.py
 M generateur.py
  ```

- **bash** `{"command": "ls reports | grep -i \"performance\" ; grep -n \"performance\" docs/pilotage/en-cours.md | head; sed -n '1,80p' reports/INDEX.md | head -20", "description": "Check report index conventions"}`

  ```
performance-corpus-10000.txt
performance.json
performance-profil.json
rapport-performance.md
102:| portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **762 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| 
… [796 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/structures/tests/test_generateur.py", "description": "Read existing generator tests"}`

  ```
"""Tests du générateur de candidats."""
import unittest

import generateur


class TestGenerateur(unittest.TestCase):
    def test_segments_alignes(self):
        for texte in ("Le chat de la voisine qui dort sur le toit se réveille.",
                      "J'ai vu l'homme avec le télescope.",
                      "Il a couru pour attraper le bus.",
                      "Elle a dit qu'elle viendrait hier."):
            for c in generateur.analyser(texte):
                prec = 0
                for s in c["segments"]:
                    self.assertGreaterEqual(s["debut"], prec, texte)
                    self.assertLessEqual(s["fin"], len(texte), texte)
                    self.assertEqual(texte[s["debut"]:s["fin"]], s["texte"], texte)
                    prec = s["fin"]
                self.assertGreaterEqual(len(c["segments"]), 2, texte)

    def test_relative_deux_lectures(self):
        cs = generateur.analyser("Le chat de la voisine qui dort sur le toit se réveille.")
        cibles = {c["attachement"]["cible"] for c in cs if c["attachement"]}
        self.assertIn("voisine", cibles)
        self.assertIn("Le chat", cibles)
        self.assertEqual(len(cs), 2)

    def t
… [4602 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/test_banc_performance.py", "description": "Read bank performance tests"}`

  ```
"""test_banc_performance.py — les fondations du banc : découpage, ajustements, tagger.

Le banc est un outil de mesure : ses **calculs** doivent être justes avant que ses chiffres
servent de résultat. Ces tests ne mesurent pas la performance de la machine ; ils vérifient
que le préfixe est exact, que le bloc est fait de phrases entières, que les ajustements
retrouvent une pente connue et que l'extrapolation du tagger est cohérente.

    python3 tools/tests/test_banc_performance.py
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CHEMIN = RACINE / "tools" / "banc_performance.py"


def _charger():
    spec = importlib.util.spec_from_file_location("banc_performance_test", CHEMIN)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


banc = _charger()


class TestDecoupage(unittest.TestCase):
    def test_prefixe_exact(self) -> None:
        texte = "Un deux trois quatre cinq six sept huit neuf dix."
        prefixe, n = banc._prefixe_mots(texte, 5)
        self.assertEqual(n, 5)
… [3594 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/porte-banc-performance.sh 2>/dev/null || ls tools/porte-*.sh | grep -i performance", "description": "Read performance gate"}`

  ```
#!/usr/bin/env bash
# porte-banc-performance — le banc de performance mesure, et son JSON est complet.
#
# Ce qu'elle vérifie : les 12 tests des fondations (préfixe exact, bloc de phrases entières,
# ajustements linéaire/quadratique/log-log, lecture de la ligne TAGGER, extrapolation), puis
# un passage COURT du banc (1 000 mots, 20 phrases, 3 tailles, bloc ×1/×2/×4) hors ligne.
# Elle ne juge PAS le chiffre de performance (il dépend de la machine) : elle vérifie que le
# banc tourne, que le JSON porte les mesures et que le contrôle de linéarité est calculé.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

if python3 tools/tests/test_banc_performance.py >"$tmp/tests.log" 2>&1; then
  dit ✅ "tests : $(grep -oE 'Ran [0-9]+ tests' "$tmp/tests.log" | head -1)"
else
  dit ❌ "tests en échec (voir ci-dessous)"; tail -20 "$tmp/tests.log"; ko=1
fi

if timeout 300 python3 tools/banc_performance.py \
     --mots 1000 --phrases-courtes 20 --tailles 250,500,1000 \
     --bloc-repetitions 1,2,4 --repetitions 1 \
     --sortie "$tmp/performance.json" >"$tmp/banc.log" 2>&1; then
  dit ✅ "passage court : $(gre
… [1969 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"performance\" tools/registre* tools/*.sh 2>/dev/null | head -20; ls tools | grep registre", "description": "Find gate registry"}`

  ```
tools/porte-banc-performance.sh:2:# porte-banc-performance — le banc de performance mesure, et son JSON est complet.
tools/porte-banc-performance.sh:7:# Elle ne juge PAS le chiffre de performance (il dépend de la machine) : elle vérifie que le
tools/porte-banc-performance.sh:16:if python3 tools/tests/test_banc_performance.py >"$tmp/tests.log" 2>&1; then
tools/porte-banc-performance.sh:22:if timeout 300 python3 tools/banc_performance.py \
tools/porte-banc-performance.sh:25:     --sortie "$tmp/performance.json" >"$tmp/banc.log" 2>&1; then
tools/porte-banc-performance.sh:31:if [ -f "$tmp/performance.json" ] && python3 - "$tmp/performance.json" <<'PY'
tools/porte-banc-performance.sh:34:assert d["schema"] == "drave.performance" and d["version"] == 1, d.get("schema")
tools/porte-banc-performance.sh:61:if timeout 120 python3 tools/banc_performance.py --profil "$tmp/texte.txt" \
tools/porte-banc-performance.sh:69:[ "$ko" -eq 0 ] && { echo "✅ porte banc-performance verte"; exit 0; } || { echo "❌ porte banc-performance rouge"; exit 1; }
porte-registre.sh
registre_parle.py
  ```

- **bash** `{"command": "grep -n \"U1\\|B13\\|performance\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -60", "description": "Find U1 in roadmap and state"}`

  ```
docs/pilotage/en-cours.md:59:- **Plan** : B13.
docs/pilotage/en-cours.md:63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
docs/pilotage/en-cours.md:66:- **Prochaine action** : **U1 — borner `_groupes_partition` et `_cible_proche`** (O(k²)) ; **J4 — l'or de rôles** ; T132/T133.
docs/pilotage/en-cours.md:88:- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md).
docs/pilotage/en-cours.md:102:| portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
docs/pilotage/en-cours.md:116:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6** | **U1 — les deux O(k²)** ; **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
docs/pilotage
… [11333 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/en-cours.md", "description": "Read current state head"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en 
… [4380 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Implémenter les index O(k log k) et le balayage (bloc + générateur S)", "status": "completed"}, {"content": "Vérifier l'identité des sorties avant/après (612, 452, 10 000 mots, blocs)", "status": "completed"}, {"content": "Mesurer α, temps 10 000 mots, mémoire, contrôle quadr … [468 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 3 completed.
  ```

- **bash** `{"command": "grep -n \"def structure\" -A30 tools/structures/generateur.py", "description": "Read structure function"}`

  ```
630:def structure(texte: str, roles: bool = True) -> list[dict]:
631-    """La structure de base, sans variantes d'attachement ; `roles=False` coupe les règles.
632-
633-    C'est ce que mesure `mesure_analyseur.py` : la segmentation et les rôles, pas le choix
634-    d'un candidat. `roles=False` rend les rôles par défaut (le contrôle « règles coupées »).
635-    """
636-    segs = _segmente(texte, _tokens(texte))
637-    sortie = []
638-    for s in segs:
639-        d = s.dict()
640-        if not roles and s.type in ROLES_DEFAUT:
641-            d["role"] = ROLES_DEFAUT[s.type]
642-        sortie.append(d)
643-    return sortie
644-
645-
646-if __name__ == "__main__":
647-    import sys
648-    args = [a for a in sys.argv[1:] if not a.startswith("--")]
649-    texte = args[0] if args else "Le chat de la voisine qui dort sur le toit se réveille."
650-    cs = analyser(texte)
651-    if "--json" in sys.argv:
652-        print(json.dumps(cs, ensure_ascii=False, indent=1))
653-    else:
654-        for c in cs:
655-            print(f"- {c['nom']}")
656-            for s in c["segments"]:
657-                print("   " + "  " * s["niveau"] + f"{s['texte']!r} [{s['type']} · {s['role
… [6 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "limit": 15, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py</path>
<type>file</type>
<content>
1: """Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
2: import json
3: import pathlib
4: import stat
5: import sys
6: import tempfile
7: import unittest
8: 
9: RACINE = pathlib.Path(__file__).resolve().parents[3]
10: sys.path.insert(0, str(RACINE / "tools"))
11: import bloc_linguistique as bl
12: 
13: TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"
14: 
15: 

(Showing lines 1-15 of 280. Use offset=16 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "limit": 40, "offset": 245}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py</path>
<type>file</type>
<content>
245:         a = n.analyser("Viens-tu ?", "fr")
246:         etiquettes = {(e.niveau, e.type): e.valeur for e in a.etiquettes}
247:         self.assertEqual(etiquettes[("pragmatique", "acte")], "question")
248:         self.assertIn(("phrase", "négation"), etiquettes)
249:         self.assertNotIn(("phrase", "modalité"), etiquettes)
250:         self.assertNotIn(("pragmatique", "double_sens"), etiquettes)
251:         self.assertEqual(n.appels, 1)
252:         n.analyser("Viens-tu ?", "fr")
253:         self.assertEqual(n.appels, 1, "le cache doit éviter le second appel")
254: 
255:     def test_priorite_syntagme_confiance(self):
256:         defaut = bl.Parallele([bl.Heuristique(), bl.MockNeuronal()]).analyser(TEXTE, "fr")
257:         confiance = bl.Parallele([bl.Heuristique(), bl.MockNeuronal()],
258:                                  priorite_syntagme="confiance").analyser(TEXTE, "fr")
259:         n_defaut = sum(1 for e in defaut.etiquettes
260:                        if e.niveau == "syntagme" and e.source == "neuronal")
261:         n_conf
… [1065 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "new_string": "import json\nimport pathlib\nimport random\nimport stat\nimport sys\nimport tempfile\nimport unittest", "old_string": "import json\nimport pathlib\nimport stat\nimport s … [38 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "new_string": "class TestIndexSpatial(unittest.TestCase):\n    \"\"\"Les index O(k log k) doivent rendre **exactement** l'ancien tri O(k²).\"\"\"\n\n    @staticmethod\n    def _ecart(g … [5698 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m unittest tools.tests.linguistique.test_bloc_linguistique -v 2>&1 | tail -25", "description": "Run new bloc tests"}`

  ```
'm'

- ['m', 'a']
+ []

======================================================================
FAIL: test_gp_tous_dedans (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_gp_tous_dedans)
Si **tous** les GV sont dans le GP, l'original ne filtre pas : le GV gouverne.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", line 388, in test_gp_tous_dedans
    self.assertEqual(bl.Heuristique._cible_proche("......mange...", segment, gvs),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     "mange")
                     ^^^^^^^^
AssertionError: 'ang' != 'mange'
- ang
+ mange
? +   +


----------------------------------------------------------------------
Ran 25 tests in 0.174s

FAILED (failures=2)
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m unittest tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial -v 2>&1 | head -80", "description": "See failing test details"}`

  ```
test_cible_et_verbes_proches (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_cible_et_verbes_proches) ... FAIL
test_gp_tous_dedans (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_gp_tous_dedans)
Si **tous** les GV sont dans le GP, l'original ne filtre pas : le GV gouverne. ... FAIL
test_groupes_partition_balayage (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_groupes_partition_balayage) ... ok
test_index_fins_tie (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_index_fins_tie) ... ok
test_index_gv_ordre_exact (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_index_gv_ordre_exact) ... ok

======================================================================
FAIL: test_cible_et_verbes_proches (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_cible_et_verbes_proches)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", line 382, in test_cible_et_verbes_proches
    self.assertEqual(attendu, bl.
… [1178 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "new_string": "            attendu = []\n            if segment[\"type\"] != \"GV\" and gvs:\n                for g in sorted(gvs, key=lambda g: self._ecart(g, segment))[:3]:\n         … [1450 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 -m unittest tools.tests.linguistique.test_bloc_linguistique -v 2>&1 | tail -12", "description": "Run bloc tests again"}`

  ```
test_tagger_neuronal_pragmatique (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_tagger_neuronal_pragmatique) ... ok
test_cible_et_verbes_proches (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_cible_et_verbes_proches) ... ok
test_gp_tous_dedans (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_gp_tous_dedans)
Si **tous** les GV sont dans le GP, l'original ne filtre pas : le GV gouverne. ... ok
test_groupes_partition_balayage (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_groupes_partition_balayage) ... ok
test_index_fins_tie (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_index_fins_tie) ... ok
test_index_gv_ordre_exact (tools.tests.linguistique.test_bloc_linguistique.TestIndexSpatial.test_index_gv_ordre_exact) ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.278s

OK
  ```

- **bash** `{"command": "tail -30 tools/structures/tests/test_generateur.py", "description": "Read end of generator tests"}`

  ```
self.assertGreaterEqual(g["couverture_globale"], 0.96)
        self.assertLess(c["baseline_role_constant"]["taux"], g["roles_taux"])
        self.assertLess(c["regles_coupees"]["taux"], g["roles_taux"])
        self.assertLess(c["roles_melanges"]["moyenne"], 0.25)


if __name__ == "__main__":
    unittest.main()


class TestSubordination(unittest.TestCase):
    def test_complement_apres_verbe(self):
        cs = generateur.analyser("Je pense que le chat dort.")
        types = {s["type"] for c in cs for s in c["segments"]}
        self.assertIn("SUB", types)
        self.assertNotIn("REL", types)

    def test_relative_apres_nom(self):
        cs = generateur.analyser("Le livre que j'ai lu est bon.")
        types = [s["type"] for c in cs for s in c["segments"]]
        self.assertIn("REL", types)
        self.assertIn("GV", types)
        # la relative ne doit pas avaler le verbe principal
        rel = [s for c in cs for s in c["segments"] if s["type"] == "REL"][0]
        self.assertNotIn("est", rel["texte"])

    def test_coordination_deux_propositions(self):
        cs = generateur.analyser("Il court et il rit.")
        gv = [s for c in cs for s in c["segments"] if s["type"] 
… [45 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^if __name__\" tools/structures/tests/test_generateur.py; sed -n '100,140p' tools/structures/tests/test_generateur.py", "description": "Locate insertion point"}`

  ```
232:if __name__ == "__main__":
        return [(s["texte"].strip(), s["role"])
                for s in generateur.structure(texte) if s["type"] == "SUB"]

    def test_temps(self):
        self.assertEqual(self._sub("Quand il pleut, je reste à la maison."),
                         [("Quand il pleut", "temps")])
        self.assertEqual(self._sub("Nous partirons dès qu'il arrivera."),
                         [("dès qu'il arrivera", "temps")])

    def test_cause(self):
        self.assertEqual(self._sub("Elle part parce qu'elle est fatiguée."),
                         [("parce qu'elle est fatiguée", "cause")])
        self.assertEqual(self._sub("Puisqu'il pleut, nous restons."),
                         [("Puisqu'il pleut", "cause")])

    def test_concession_et_hypothese(self):
        self.assertEqual(self._sub("Bien qu'il soit tard, il travaille."),
                         [("Bien qu'il soit tard", "concession")])
        self.assertEqual(self._sub("S'il vient, nous partirons."),
                         [("S'il vient", "hypothese")])

    def test_but_et_maniere(self):
        self.assertEqual(self._sub("Il travaille afin qu'elle réussisse."),
                         [("af
… [797 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,8p' tools/structures/tests/test_generateur.py; sed -n '220,245p' tools/structures/tests/test_generateur.py", "description": "Check imports and insertion context"}`

  ```
"""Tests du générateur de candidats."""
import unittest

import generateur


class TestGenerateur(unittest.TestCase):
    def test_segments_alignes(self):
        import mesure_analyseur
        r = mesure_analyseur.mesurer(mesure_analyseur.charger(mesure_analyseur.GOLD))
        g, c = r["global"], r["controles"]
        self.assertEqual(g["phrases"], 61)
        self.assertGreaterEqual(g["types_ok"], 60)          # les 61 types sont attendus
        self.assertGreaterEqual(g["roles_taux"], 0.98)
        self.assertGreaterEqual(g["couverture_globale"], 0.96)
        self.assertLess(c["baseline_role_constant"]["taux"], g["roles_taux"])
        self.assertLess(c["regles_coupees"]["taux"], g["roles_taux"])
        self.assertLess(c["roles_melanges"]["moyenne"], 0.25)


if __name__ == "__main__":
    unittest.main()


class TestSubordination(unittest.TestCase):
    def test_complement_apres_verbe(self):
        cs = generateur.analyser("Je pense que le chat dort.")
        types = {s["type"] for c in cs for s in c["segments"]}
        self.assertIn("SUB", types)
        self.assertNotIn("REL", types)

    def test_relative_apres_nom(self):
        cs = generateur.analyser("Le livre qu
… [83 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py", "new_string": "\"\"\"Tests du générateur de candidats.\"\"\"\nimport random\nimport unittest\n\nimport generateur", "old_string": "\"\"\"Tests du générateur de candidats.\"\"\"\nimport unittest … [23 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py", "limit": 6, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py", "limit": 10, "offset": 226}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py</path>
<type>file</type>
<content>
1: """Tests du générateur de candidats."""
2: import unittest
3: 
4: import generateur
5: 
6: 

(Showing lines 1-6 of 255. Use offset=7 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py</path>
<type>file</type>
<content>
226:         self.assertGreaterEqual(g["couverture_globale"], 0.96)
227:         self.assertLess(c["baseline_role_constant"]["taux"], g["roles_taux"])
228:         self.assertLess(c["regles_coupees"]["taux"], g["roles_taux"])
229:         self.assertLess(c["roles_melanges"]["moyenne"], 0.25)
230: 
231: 
232: if __name__ == "__main__":
233:     unittest.main()
234: 
235: 

(Showing lines 226-235 of 255. Use offset=236 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py", "new_string": "\"\"\"Tests du générateur de candidats.\"\"\"\nimport random\nimport unittest\n\nimport generateur", "old_string": "\"\"\"Tests du générateur de candidats.\"\"\"\nimport unittest … [23 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py", "new_string": "class TestArbreLineaire(unittest.TestCase):\n    \"\"\"`construire_arbre` doit rendre les mêmes pères et profondeurs que le O(k²).\"\"\"\n\n    @staticmethod\n    def _segments(t … [1761 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py has been updated successfully.
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 tests/test_generateur.py 2>&1 | tail -12", "description": "Run generator tests", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures"}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py", line 5, in <module>
    import generateur
ModuleNotFoundError: No module named 'generateur'
  ```

- **bash** `{"command": "PYTHONPATH=. PYTHONHASHSEED=0 python3 tests/test_generateur.py 2>&1 | tail -15", "description": "Run generator tests with path", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures"}`

  ```
...........................
----------------------------------------------------------------------
Ran 27 tests in 0.053s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['/tmp/u1-before/performance-avant.json','/tmp/u1-after/performance-apres4.json']:\n d=json.load(open(p))\n print('\\n',p)\n print('env', {k:d['environnement'].get(k) for k in ('python','machine','cpu','nproc','ram_kb','git_commit')})\n r=d['mesur … [251 caractères tronqués]`

  ```
/tmp/u1-before/performance-avant.json
env {'python': '3.13.16', 'machine': 'x86_64', 'cpu': 'Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz', 'nproc': 40, 'ram_kb': 131886412, 'git_commit': '83adaa2b6f8c6b1f03480375d30170a7613c71f8'}
fonction {"repetitions": 3, "duree_analyse_s": {"n": 3, "mediane": 3.990812406176701, "moyenne": 3.9837561137974262, "min": 3.856404581107199, "max": 4.104051354108378, "p95": 4.104051354108378}, "duree_json_s": {"n": 3, "mediane": 0.6280551138333976, "moyenne": 0.6182192109214762, "min": 0.5918897499796003, "max": 0.6347127689514309, "p95": 0.6347127689514309}, "duree_totale_s": {"n": 3, "mediane": 4.618867520010099, "moyenne": 4.601975324718903, "min": 4.49111735005863, "max": 4.695941104087979, "p95": 4.695941104087979}, "rss_kb": {"n": 3, "mediane": 129936, "moyenne": 129702.66666666667, "min": 128756, "max": 130416, "p95": 130416}, "json_octets": 14795890, "etiquettes": 54522, "syntagmes": 2726, "unites_semantiques": 4701, "phrases": 814, "mots": 10000, "brut": [{"duree_analyse_s": 3.990812406176701, "duree_json_s": 0.6280551138333976, "duree_totale_s": 4.618867520010099, "rss_kb": 129936, "json_octets": 14795890, "etiquettes": 54522, "syntagmes": 272
… [3535 caractères tronqués]
  ```

- **bash** `{"command": "date -u +%Y-%m-%dT%H:%M:%SZ; date +%Y-%m-%d; python3 - <<'PY'\nimport hashlib, pathlib\nfor p in sorted(pathlib.Path('/tmp/u1-before').glob('*.json'))+sorted(pathlib.Path('/tmp/u1-after4').glob('*.json')):\n if 'performance' in p.name or 'gold-' in p.name: continue\n print(p.name, p.sta … [113 caractères tronqués]`

  ```
2026-11-16T05:09:15Z
2026-11-16
bloc-x1.json 449558 137cb8097696e49b52cc49041f96b9cdeb24d121654e4c08a6b13a9d0b268789
bloc-x16.json 7263340 c3c34bfb1cd3b4b5442a14e7a13607ada5bf851fc417dd66728c155212974094
bloc-x2.json 901533 dbbb1699cf09922a2288c721d0f095bd1c99ade7dae04629caf614e8fbe2dd3d
bloc-x32.json 14552604 06675c023dc93768056bce30ccc641e61772e6eb1bee1d2aaae982326e0dcfed
bloc-x4.json 1805483 8eba512f8ad72f6c6bc0b706665d21e27242645c5adfe50daa3368cf9c6e634e
bloc-x40.json 18197238 28a412b9ae7d6a785ddd40cace5f2a652d387289b6955854a7ee99cfe48afe56
bloc-x8.json 3618708 fa3f9e7d637686031c4ac7eeadd37fe23dbbf6fbaad29fe5aaccccd6427d76ca
corpus-10000.json 16457228 16488a95ca0d63f478e971d866a05d90796d24085497641e4677ae6c51ef3094
bloc-x1.json 449558 137cb8097696e49b52cc49041f96b9cdeb24d121654e4c08a6b13a9d0b268789
bloc-x16.json 7263340 c3c34bfb1cd3b4b5442a14e7a13607ada5bf851fc417dd66728c155212974094
bloc-x2.json 901533 dbbb1699cf09922a2288c721d0f095bd1c99ade7dae04629caf614e8fbe2dd3d
bloc-x32.json 14552604 06675c023dc93768056bce30ccc641e61772e6eb1bee1d2aaae982326e0dcfed
bloc-x4.json 1805483 8eba512f8ad72f6c6bc0b706665d21e27242645c5adfe50daa3368cf9c6e634e
bloc-x40.json 18197238 28a412b9ae7d6a785
… [225 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/##' | tr '\\n' ' '; echo; ls tools/porte-*.sh | grep -i 'structure\\|bloc\\|banc'", "description": "List gates"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-banc-performance.sh porte-bloc-code.sh porte-bloc-linguistique.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-cic.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-inventaire.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occu
… [685 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-bloc-linguistique.sh", "description": "Read bloc linguistique gate"}`

  ```
#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
python3 tools/tests/linguistique/gold.py >/dev/null || { echo "❌ gold"; exit 1; }
python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json >/dev/null || { echo "❌ évaluation gold"; exit 1; }
echo "✅ porte bloc linguistique verte"
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, hashlib, pathlib\ndef h(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()\nfor p in ['/tmp/u1-before/gold-annotations-612.json','/tmp/u1-after4/gold-annotations-612.json','/tmp/u1-before/gold-annotations-452.json','/tmp/u1-after4/gold-ann … [752 caractères tronqués]`

  ```
/tmp/u1-before/gold-annotations-612.json b61c1521328bde4261ee42c1a0259d4c61cd05a9f12ec922a9256008c176c3dc
/tmp/u1-after4/gold-annotations-612.json b61c1521328bde4261ee42c1a0259d4c61cd05a9f12ec922a9256008c176c3dc
/tmp/u1-before/gold-annotations-452.json de329b530ddafbca9908622b1869edb024207180b468352905e1678f713d7c87
/tmp/u1-after4/gold-annotations-452.json de329b530ddafbca9908622b1869edb024207180b468352905e1678f713d7c87
/tmp/u1-before/corpus-10000.json 16488a95ca0d63f478e971d866a05d90796d24085497641e4677ae6c51ef3094
/tmp/u1-after4/corpus-10000.json 16488a95ca0d63f478e971d866a05d90796d24085497641e4677ae6c51ef3094
gold JSON canon sha avant/apres 5bca5f760a2514daa96bf5f5eed1c0967e2a6e28d1ac16d821d4797d20bdebd8 5bca5f760a2514daa96bf5f5eed1c0967e2a6e28d1ac16d821d4797d20bdebd8 True
all pos {"exactitude": 0.8625, "exactitude_ferme": 0.9373, "exactitude_ouvert": 0.7918, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 65, "NOUN": 65, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"PRON": 15, "CONJ": 68, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "
… [2434 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/faire_json_fix.py <<'PY'\nimport json, pathlib, hashlib\nracine = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\navant = json.load(open('/tmp/u1-before/performance-avant.json'))\napres = json.load(open('/tmp/u1-after/performance-apres4.json'))\n\ndef bloc(d) … [9101 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/performance-fix.json
  ```

- **bash** `{"command": "grep -n \"class _IndexGV\\|class _IndexFins\\|class _IndexSegments\\|def _groupes_partition\\|def _cible_proche\\|def _verbes_proches\\|def _sujet_hors_gv\\|def _repli_cible_gp\\|def _cible_rel_sujet\\|def _expliciter_partition\" tools/bloc_linguistique.py; grep -n \"def construire_arbr … [104 caractères tronqués]`

  ```
524:class _IndexGV:
655:class _IndexFins:
678:class _IndexSegments:
1127:    def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,
1260:    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict],
1363:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict],
1463:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
1500:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
2710:def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
2745:def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
319:def construire_arbre(segs: list["Segment"]) -> None:
345:def _segmente(texte: str, toks: list[Token]) -> list[Segment]:
  ```

- **bash** `{"command": "cat > tools/verifier_performance_fix.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"verifier_performance_fix.py — le contrôle négatif de U1, rejouable.\n\nU1 a remplacé des boucles O(k²) par des index (bloc linguistique et générateur S) **sans\nchanger les sorties**. Ce script le vérifie de d … [5404 caractères tronqués]`

  ```
COMPILED
identique corpus-10000.json             16457228 octets  16488a95ca0d63f4
identique bloc-x1.json                    449558 octets  137cb8097696e49b
identique bloc-x2.json                    901533 octets  dbbb1699cf09922a
identique bloc-x4.json                   1805483 octets  8eba512f8ad72f6c
identique bloc-x8.json                   3618708 octets  fa3f9e7d63768603
identique bloc-x16.json                  7263340 octets  c3c34bfb1cd3b4b5
identique bloc-x32.json                 14552604 octets  06675c023dc93768
identique bloc-x40.json                 18197238 octets  28a412b9ae7d6a78
identique gold-annotations-612.json      4281465 octets  b61c1521328bde42
identique gold-annotations-452.json      3222340 octets  de329b530ddafbca
10/10 identiques — diff vide
EXIT:0
  ```

- **bash** `{"command": "cat > tools/tests/test_verifier_performance_fix.py <<'PY'\n\"\"\"test_verifier_performance_fix.py — le comparateur du contrôle négatif de U1.\n\nLe comparateur ne mesure rien : il vérifie que deux répertoires d'annotations canoniques\nsont identiques ou non. Ces tests couvrent le vert ( … [2100 caractères tronqués]`

  ```
10/10 identiques — diff vide
identique corpus-10000.json                   27 octets  5cd6b21c47a8582f
identique bloc-x1.json                        22 octets  fcfcb3438537b9c5
identique bloc-x2.json                        22 octets  a60e57dc3b679b42
identique bloc-x4.json                        22 octets  a9479698615b0da1
identique bloc-x8.json                        22 octets  bc31a37791112f02
identique bloc-x16.json                       23 octets  53c6fea9691a9bb0
identique bloc-x32.json                       23 octets  4e50c50f2057dab9
identique bloc-x40.json                       23 octets  072359ebfb96bff7
identique gold-annotations-612.json           35 octets  92a7ef3f84c200fc
DIFF      gold-annotations-452.json           35 octets  beecd002077e6380
9/10 identiques — diff non vide
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_verifier_performance_fix 2>&1 | tail -6", "description": "Check comparator test summary"}`

  ```
identique bloc-x16.json                       23 octets  53c6fea9691a9bb0
identique bloc-x32.json                       23 octets  4e50c50f2057dab9
identique bloc-x40.json                       23 octets  072359ebfb96bff7
identique gold-annotations-612.json           35 octets  92a7ef3f84c200fc
DIFF      gold-annotations-452.json           35 octets  beecd002077e6380
9/10 identiques — diff non vide
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_verifier_performance_fix > /tmp/test_verif.log 2>&1; echo EXIT:$?; grep -E \"Ran |OK|FAILED|Error\" /tmp/test_verif.log | tail -10", "description": "Run comparator tests and grep result"}`

  ```
EXIT:0
Ran 3 tests in 0.009s
OK
  ```

- **bash** `{"command": "cat > reports/rapport-performance-fix.md <<'MD'\n# U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près**\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U1** (exploitable, suite de T4) ·\n> **Da … [12044 caractères tronqués]`

  ```
186 reports/rapport-performance-fix.md
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 python3 /tmp/prof_detail.py 32 > /tmp/u1-after/prof_detail_final_x32.txt 2>&1; echo EXIT:$?; sed -n '1,40p' /tmp/u1-after/prof_detail_final_x32.txt", "description": "Final detailed profile x32", "run_in_background": true}`

  ```
started background job bash-110
  ```

- **job_output** `{"job_id": "bash-110", "timeout_ms": 240000, "wait": true}`

  ```
EXIT:0
=== cumulatif (filtre) ===
  24.465 cum    2.969 own         1 appels  analyser  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1749)
   4.631 cum    1.833 own     29888 appels  _est_verbe  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:713)
   2.573 cum    2.573 own   1757534 appels  <method 'get' of 'dict' objects>  (~:0)
   2.454 cum    1.235 own      7904 appels  _morphemes  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1111)
   2.373 cum    0.375 own     60281 appels  _norm  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py:134)
   2.232 cum    0.049 own      7776 appels  _tete_texte  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1409)
   2.216 cum    2.216 own   1583073 appels  <method 'endswith' of 'str' objects>  (~:0)
   2.078 cum    0.326 own         2 appels  _tokens  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py:175)
   2.049 cum    0.153 own         1 appels  _syntagmes_simple  (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1516)
   2.025 cum    0.001 own
… [2974 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/performance-fix.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nd['source']['commit_avant']='83adaa2b6f8c6b1f03480375d30170a7613c71f8'\nd['source']['sous_module_avant']='389b99f'\nd['source']['commit_mesure']='83adaa2b … [454 caractères tronqués]`

  ```
ok
JSON_OK
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "limit": 18, "offset": 126}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md</path>
<type>file</type>
<content>
126: | [`bloc_linguistique.py:2745`](../tools/bloc_linguistique.py) | `_expliciter_partition` | `deepcopy` des candidats par alternative | copie superficielle (aucune mutation ensuite) |
127: | [`generateur.py:319`](../tools/structures/generateur.py) | `construire_arbre` | `reversed(segs[:k])` + `segs.index(parent)`, O(k²) | dernier segment à gauche entretenu, O(k) |
128: | [`generateur.py:345`](../tools/structures/generateur.py) | `_segmente` (cibles) | `reversed(segs[:k])` par segment, O(k²) | dernier GN / GP / GV entretenu, O(k) |
129: 
130: Les deux premiers points sont ceux de T4 ; les cinq suivants ont été nommés par le profil
131: **après** correction des deux premiers. Le profil du bloc ×32 passe de 48,6 s (×16) à
132: 35,1 s (×32) profilées, et les parts changent : `_expliciter_partition` (6,4 s) et
133: `deepcopy` (6,0 s) disparaissent presque, `_sujet_hors_gv` tombe de 38,1 s à 0,8 s,
134: `_groupes_partition` de 11,2 s à 0,08 s.
135: 
136: ## 6. Tests et portes
137: 
138: | commande | résultat |
139: |---|---|
140: | `python3 -m unittest tools.test
… [542 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "new_string": "Les deux premiers points sont ceux de T4 ; les cinq suivants ont été nommés par le profil\n**après** correction des deux premiers. Le profil final du bloc ×32 (24,5 s profilées) ne\nmon … [913 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md has been updated successfully.
  ```

- **bash** `{"command": "ls journal | tail -20; ls journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc | tail; sed -n '1,60p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null", "description": "Inspect journal structure"}`

  ```
2026-10-25
2026-10-26
2026-10-27
2026-10-28
2026-10-29
2026-10-30
2026-10-31
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
2026-11-15
README.md
sessions
THEMES.md
digest.md
plan.md
rapport.md
session.v4.jsonl.zstd
# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
- **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
  `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
  `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
  `docs/schemas/heuristique-*.svg`
… [5149 caractères tronqués]
  ```

- **bash** `{"command": "tail -80 journal/2026-11-15.md 2>/dev/null || ls journal | grep 2026-11 | tail", "description": "Read latest journal entry"}`

  ```
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
2026-11-15
  ```

- **bash** `{"command": "ls journal/2026-11-15; sed -n '1,60p' journal/2026-11-15/*.md 2>/dev/null | head -80; ls journal/2026-11-15 | tail", "description": "Inspect daily journal format"}`

  ```
distribue.md
docs.md
memoire.md
mesures.md
modele.md
outils.md
portes.md
README.md
# 2026-11-15 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (9)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:27 | `f926b5bc` | C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f) | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
| 03:04 | `c37fed06` | B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE | `en-cours.md`, `README.md`, `distribue.md` (+16) |
| 04:26 | `f1c6b506` | PHASE 3 (C PUIS B) — N2 (--rope --canal-dir), S (page / et 11 VERDICTS), R (GOLD RÉEL 452), PANINI (PROTOCOLE À DATE CONTRÔLÉE, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX, CIC 42/42) ; 6 FICHES, SEPT. 9 DU PLAN | `en-cou
… [4524 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/journal_auto.py --help 2>&1 | head -40; sed -n '1,40p' tools/journal_auto.py", "description": "Read journal auto usage"}`

  ```
usage: journal_auto.py [-h] [--jour JOUR] [--depuis DEPUIS] [--lister]
                       [--dry-run] [--quiet]

options:
  -h, --help       show this help message and exit
  --jour JOUR      AAAA-MM-JJ (défaut : aujourd'hui)
  --depuis DEPUIS  générer chaque jour depuis cette date
  --lister         montrer les thèmes et leurs mots-clés
  --dry-run
  --quiet
#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le découpage **`<AAAA-MM-JJ>_<thème>.md`** : on lit la journée d'un thème,
et on suit un thème **d'un jour à l'autre** (le nom commence par la date, le thème suit —
`ls journal/2026-10-1*/attention.md`).

SOURCES, et rien d'autre :
  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
     fichiers touchés ; c'est la chronologie **fiable** (les horodatages écrits à la main
     s'étaient retrouv
… [1064 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '56,72p' docs/pilotage/en-cours.md; echo ----; sed -n '110,130p' docs/pilotage/en-cours.md; echo ----; sed -n '155,180p' docs/pilotage/roadmap.md", "description": "Read state and roadmap U1 sections"}`

  ```
- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13.
- **Stratégie** : v0.
- **Ambition** : runtime tracé.
- **Objectif final** : moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md). **T6 — le bilan exploitable** : [fiche](../../reports/rapport-bilan-exploitable.md), [JSON](../../reports/rapport-bilan-exploitable.json).
- **Prochaine action** : **U1 — borner `_groupes_partition` et `_cible_proche`** (O(k²)) ; **J4 — l'or de rôles** ; T132/T133.
- **Bloquants** : 7B locales interdites (règle 11) ; **gol
… [5095 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 12, "offset": 62}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 6, "offset": 114}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
62: - **Objectif final** : moteur de pensée v0.
63: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
64: - **Ce que font les autres** : **N2**, **S**, **hub**.
65: - **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md). **T6 — le bilan exploitable** : [fiche](../../reports/rapport-bilan-exploitable.md), [JSON](../../reports/rapport-bilan-exploitable.json).
66: - **Prochaine action** : **U1 — borner `_groupes_partition` et `_cible_proche`** (O(k²)) ; **J4 — l'or de rôles** ; T132/T133.
67: - **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
68: - **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
69: 
70: ### Session `0733c5bb-f90b-4f58
… [336 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
114: |---|---|---|---|
115: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
116: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6** | **U1 — les deux O(k²)** ; **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
117: | **N — le natif** | **N2, N4** | N2 : **1 024 — 2,3911 / 2,3522** ; porte 2,7856 ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; N3 couvert ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
118: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,02177 $ ; W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` opt-in ; W6 : [rapport 
… [791 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../report … [1009 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s** | **U2  … [421 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 5, "offset": 124}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
124: ## Ce qui reste
125: 
126: **T1–T6 — livré** ; reste **U1** (les deux O(k²)), **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.md).
127: 
128: **Pensée** — `g017`, T132/T133, gold de pensée ; **J4 — l'or de rôles** (seconds cadres). **Le gold de S** (61 phrases/144 rôles) n'est pas un or humain indépendant ; **S** — page `/` : décision et recette (106/41), **12/28** référents faux.

(Showing lines 124-128 of 148. Use offset=129 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, sorties identiques) ; reste **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitab … [219 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 5, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

(Showing lines 1-5 of 148. Use offset=6 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-16, 00 h 30 HNE (U1 : les deux O(k²) bornés, α 1,08)**", "old_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 18, "offset": 160}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
160: gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
161: 
162: **T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
163: **14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.
164: **Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;
165: `_groupes_partition`/`_cible_proche` sont **O(k²)**. [Fiche](../../reports/rapport-performance.md) ·
166: [JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.
167: 
168: **T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : **installation éditable**
169: (127 sans install), **quickstart 3/3** (JSON v2 **5 899** octets), **API** (**2 139** objets,
170: **8** rôles), **performance** (10 000 mots **4,01 s**, **2 493 mots/s**, **126 Mio**), **CLI**
171: (**20/20**, codes **0/3/4/5/1**). **Passe non relancée** : **85** portes lues (**81/4**),
172: `sessions` réparée, **86e porte** `porte-banc-performance` verte seule. Trois limites : **clone
173: public** à **88,70 %** d'attachement au lieu de **99,58 %**, cro
… [388 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"U1 — les deux O(k²)\" docs/pilotage/roadmap.md", "description": "Find roadmap U1 mentions"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [2052 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**T1–T6 produit exploitable** ([bilan](../../reports/rapport-bilan-exploitable.md)) ; **U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports … [162 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "`_groupes_partition`/`_cible_proche` sont **O(k²)**. [Fiche](../../reports/rapport-performance.md) ·\n[JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.\n\n**U1 —  … [1045 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "[JSON](../../reports/rapport-bilan-exploitable.json). Prochaine action : **U2 — la roue**,\npuis **U3 — `--profils`** ; **U1** est livré (α **1,08**, [fiche](../../reports/rapport-performance-fix … [272 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"Heartbeat\\|Prochaine action\\|État\\|Reprise\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md | head -20", "description": "Find session plan lines"}`

  ```
18:- **Heartbeat** : 2026-11-15 13:20 EST
19:- **Prochaine action** : le chantier (phase 2, J6-J14) ; la coordination N2/S/R/A est livrée.
23:- **État** : actif
24:- **Reprise** : le 04/11 10 h 14 ; quatre modes, élision 144/144.
35:- **Reprise** : **R4.4** — les trois restes sont des **limites nommées**, pas des tâches ouvertes ;
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "limit": 8, "offset": 17}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
17:   `reports/bloc-*`, `journal/sessions/e181ce02-…/`
18: - **Heartbeat** : 2026-11-15 13:20 EST
19: - **Prochaine action** : le chantier (phase 2, J6-J14) ; la coordination N2/S/R/A est livrée.
20: - **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est
21:   `cascade_pos` (documentée, tolérée).
22: - **Arrêt** : 2026-11-02 15 h 06 (reboot) — reprise à **16 h 16** ; **actif** ; heartbeat rafraîchi.
23: - **État** : actif
24: - **Reprise** : le 04/11 10 h 14 ; quatre modes, élision 144/144.

(Showing lines 17-24 of 69. Use offset=25 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "new_string": "- **Heartbeat** : 2026-11-16 00:30 EST\n- **Prochaine action** : **U2 — la roue**, puis **U3 — `--profils`** ; **U1** est livré (α **1,08**, 10 000 mots **0,8 … [235 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md has been updated successfully.
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 bash tools/porte-bloc-linguistique.sh 2>&1 | tail -20", "description": "Run bloc linguistique gate", "run_in_background": true}`

  ```
started background job bash-119
  ```

- **bash** `{"command": "PYTHONHASHSEED=0 bash tools/porte-banc-performance.sh 2>&1 | tail -20", "description": "Run banc performance gate", "run_in_background": true}`

  ```
started background job bash-120
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo EXIT:${PIPESTATUS[0]}", "description": "Run documentation review"}`

  ```
revue de documentation · 766 fiche(s) · 861 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 3 anomalie(s) :
     · fraîcheur : en-cours.md dit 2026-11-16, le dernier commit date du 2026-11-15
     · compteurs : en-cours.md dit 765 fichiers, le disque en a 766
     · compteurs : en-cours.md dit 860 JSON, le disque en a 861
EXIT:1
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo EXIT2:${PIPESTATUS[0]}", "description": "Run doc size and state checks"}`

  ```
2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2773    232   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4049 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/
… [255 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"765\\|860\\|fichiers\\|JSON\" docs/pilotage/en-cours.md | head -20", "description": "Find counters in en-cours"}`

  ```
52:- **Bloquants** : aucun ; 8765 pris (lancer 9000) ; migration = choix.
65:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md). **T6 — le bilan exploitable** : [fiche](../../reports/rapport-bilan-exploitable.md), [JSON](../../reports/rapport-bilan-exploitable.json). **U1 — les deux O(k²) bornés** : 10 000 mots **4,0 → 0,82 s** (×4,9), α **1,53 → 1,08**, contrôle linéaire **vert**, sorties **identiques** ([fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)).
90:- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md).
104:| fichiers / JSON de résultats | **765** / **860** | `reports/*.md` / `reports/*.json` |
118:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 
… [843 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '162,188p' docs/pilotage/roadmap.md", "description": "Read updated roadmap block"}`

  ```
**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.
**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;
`_groupes_partition`/`_cible_proche` sont **O(k²)**. [Fiche](../../reports/rapport-performance.md) ·
[JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.

**U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
**12 259 mots/s**, **127,4 Mio** (126,9 avant, +0,5 Mio) ; JSON **identique**
(14 795 890 octets). Contrôle de linéarité **vert** : **α = 1,076** (1,530 avant),
le terme quadratique n'ajoute que **+0,00077 de R²** (0,0414 avant). Sorties **identiques au
bit près** : 612/452, 10 000 mots, sept blocs, diff vide. `_groupes_partition` (balayage
O(k log k)), `_cible_proche` (`_IndexGV`), puis `_sujet_hors_gv`, `_repli_cible_gp`,
`_cible_rel_sujet` et deux boucles du générateur S (`construire_arbre`, cibles de
`_segmente`) sont corrigés. [Fiche](../../reports/rapport-performance-fix.md) ·
[JSON](../../reports/performance-fix.json) · [contrôle négatif](../../tools/verifier_performance_fix.py).
Prochai
… [963 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,\n**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.\n[Fiche](../../reports/ … [3498 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

### 👤 Utilisateur

background job bash-120 (bash: PYTHONHASHSEED=0 bash tools/porte-banc-performance.sh 2>&1 | tail -20) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-119 (bash: PYTHONHASHSEED=0 bash tools/porte-bloc-linguistique.sh 2>&1 | tail -20) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-119"}`

  ```
"ponctuation_refus": "vide",
  "langue_inconnue": "und",
  "indice_faux": "und",
  "rejeu_identique": true
 },
 "verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
  "niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-120"}`

  ```
✅ tests : Ran 12 tests
  ✅ passage court : 7 étapes
JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé
  ✅ JSON : contrat et mesures présents
  ✅ mode profil : fonctions dominantes exportées
✅ porte banc-performance verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "grep -n \"fichiers / JSON\" docs/pilotage/en-cours.md", "description": "Locate counters line"}`

  ```
104:| fichiers / JSON de résultats | **765** / **860** | `reports/*.md` / `reports/*.json` |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 3, "offset": 103}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
103: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
104: | fichiers / JSON de résultats | **765** / **860** | `reports/*.md` / `reports/*.json` |
105: | documents de `docs/` | **125** (hors archive et README) | `docs/**/*.md` |

(Showing lines 103-105 of 148. Use offset=106 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **766** / **861** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **765** / **860** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo EXIT:${PIPESTATUS[0]}", "description": "Recheck document budgets"}`

  ```
T0 max : 4049 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9029 mots > budget 9000 (T1)
     · T0 : 4049 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT:1
  ```

- **bash** `{"command": "wc -w docs/pilotage/en-cours.md; sed -n '60,68p' docs/pilotage/en-cours.md", "description": "Word count and session lines"}`

  ```
1679 docs/pilotage/en-cours.md
- **Stratégie** : v0.
- **Ambition** : runtime tracé.
- **Objectif final** : moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md). **T6 — le bilan exploitable** : [fiche](../../reports/rapport-bilan-exploitable.md), [JSON](../../reports/rapport-bilan-exploitable.json). **U1 — les deux O(k²) bornés** : 10 000 mots **4,0 → 0,82 s** (×4,9), α **1,53 → 1,08**, contrôle linéaire **vert**, sorties **identiques** ([fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)).
- **Prochaine action** : **U2 — la roue** ; **U3 — `--profils`** ; **J4 — l'or de rôles** ; T132/T133.
- **Bloquants** : 7B locales interdites (règle 11)
… [114 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../rep … [1489 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -6; echo EXIT:${PIPESTATUS[0]}", "description": "Recheck budgets"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9029 mots > budget 9000 (T1)
     · T0 : 4015 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT:1
  ```

- **bash** `{"command": "sed -n '162,190p' docs/pilotage/roadmap.md; wc -w docs/pilotage/roadmap.md", "description": "Check roadmap block after edit"}`

  ```
**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.
[Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/performance.json).

**U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
**12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), le
quadratique n'ajoute que **+0,00077 de R²** ; sorties identiques (612/452, sept blocs,
diff vide). `_groupes_partition`, `_cible_proche`, `_sujet_hors_gv`, deux index de GN et deux
boucles du générateur S sont corrigés. [Fiche](../../reports/rapport-performance-fix.md) ·
[JSON](../../reports/performance-fix.json) · [contrôle](../../tools/verifier_performance_fix.py).
**Prochaine action : U2 — la roue, puis U3 — `--profils`.**

**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : installation éditable (127
sans install), quickstart 3/3, API (2 139 objets, 8 rôles), performance (10 000 mots 4,01 s,
126 Mio), CLI 20/20 (codes 0/3/4/5/1). Passe non relancée : 85 portes lues (81/4), `sessions`
réparée, 86e porte `porte-banc-performance` verte. Trois limites : cl
… [713 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '56,68p' docs/pilotage/en-cours.md", "description": "Read session lines after trim"}`

  ```
- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13.
- **Stratégie** : v0.
- **Ambition** : runtime tracé.
- **Objectif final** : moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)).
- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **W6** clôture semaine 2 ; **T6** bilan exploitable ; **U1** O(k²) bornés (10 000 mots **4,0 → 0,82 s**, α **1,53 → 1,08**, sorties identiques ; [fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)).
- **Prochaine action** : **U2 — la roue** ; **U3 — `--profils`** ; **J4** ; T132/T133.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.\n- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/ … [1192 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),\n**12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), le\nquadratique n'ajoute que **+0, … [2080 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -6; echo EXIT:${PIPESTATUS[0]}", "description": "Recheck budgets after trim"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9002 mots > budget 9000 (T1)
EXIT:1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**Prochaine action : U2 — la roue, puis U3 — `--profils`.**','**Prochaine action : U2 — la roue, U3 — `--profils`.**')\ns=s.replace('**U1 est livré** ; restent **J … [198 caractères tronqués]`

  ```
· 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT:0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}", "description": "Re-run doc review"}`

  ```
revue de documentation · 766 fiche(s) · 861 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · fraîcheur : en-cours.md dit 2026-11-16, le dernier commit date du 2026-11-15
EXIT:1
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_journal.py 2>&1 | tail -10; echo EXIT2:${PIPESTATUS[0]}", "description": "Check state and journal"}`

  ```
· session « Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)* » ne dit pas « **Plan** »
     · session « Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)* » ne dit pas « **Ambition** »
     · session « Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)* » ne dit pas « **Stratégie** »
     · session « Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)* » ne dit pas « **Objectif final** »
     · session « Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)* » ne dit pas « **Ce que font les autres** »
EXIT:1
  journal · 47 jour(s) · 222 session(s) · 2686 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT2:0
  ```

- **bash** `{"command": "sed -n '1,200p' tools/verifie_en_cours.py", "description": "Read state checker requirements"}`

  ```
#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **sept sections** du template ;
  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
     **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
     **Ce qu'elle fait**, **Ce que font les autres**, **Prochaine action**, **Bloquants** et
     **Journal** ;
  4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
  5. « Les chantiers et leurs bloquants » : une ligne **A**, **B**, **N**, **R** avec un bloquant
     **non vide** (le mot « aucun » est une information, une cellule vide est un oubli) ;
  6. **5 questions ouvertes au plus**, chacune avec ce qui la débloque (`→`) ;
  7. une **prochaine action nommée** dans « Ce qui reste » (A/B/C/N/R) ;
  8. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).

Usage : python3 tools/verifie_en_cours.py   (code 0 = l'état est reprenable)
"""
from __future__ import anno
… [4812 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -i \"T0\\|budget\" | head", "description": "Check T0 exact word count"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
  T0 max : 3991 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.\n- **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.\n- **Fait** :  … [1024 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo EXIT:${PIPESTATUS[0]}", "description": "Check state format"}`

  ```
en-cours · 1642 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT:0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅\" | tail -5; echo EXIT:${PIPESTATUS[0]}", "description": "Check budgets"}`

  ```
T0 max : 4012 mots (budget 4 000)
  ❌ 1 violation(s) :
EXIT:1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.\n- **Ce que font les autres** : N2.\n- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²)  … [562 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅\" | tail -5; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo EXIT2:${PIPESTATUS[0]}", "description": "Recheck budgets and state"}`

  ```
T0 max : 3998 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT:0
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT2:0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo EXIT:${PIPESTATUS[0]}", "description": "Doc review after counters"}`

  ```
revue de documentation · 766 fiche(s) · 861 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · fraîcheur : en-cours.md dit 2026-11-16, le dernier commit date du 2026-11-15
EXIT:1
  ```

- **bash** `{"command": "sed -n '1,120p' tools/toutes-les-portes.sh", "description": "Read all gates script"}`

  ```
#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
# personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
# on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
# exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
# ici, appliqué aux instruments eux-mêmes.
#
# Ce que fait ce script, et ce qu'aucun autre ne faisait :
#   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
#   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
#   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
#      est une porte ROUGE, pas une porte qu'on attend ;
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affiche qu'une ligne par porte ;
#   5. il sort en 1 s'il y a la moindre rouge, en
… [3112 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/references-non-regression.md | sed -n '1,160p'", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
> **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
> Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
> `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-1311-23h15.log`.
>
> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
> `work/portes/verif-cloture/`.

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durabl
… [12356 caractères tronqués]
  ```

- **bash** `{"command": "PORTES=\"porte-etat porte-registre porte-budget porte-produit porte-sessions porte-bloc-linguistique porte-banc-performance porte-bloc-code porte-bloc-maths porte-bloc-tableaux porte-miroir-blocs porte-document porte-lecture porte-lecteur porte-ressources\" bash tools/toutes-les-portes. … [171 caractères tronqués]`

  ```
started background job bash-143
  ```

- **bash** `{"command": "git status --short | head -40; echo ---SUBMODULE---; git -C tools/structures status --short; echo ---DIFFSTAT---; git diff --stat | tail -20; git -C tools/structures diff --stat", "description": "Review git status before commit"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/bloc_linguistique.py
 M tools/chantier/plan.json
 m tools/structures
 M tools/tests/linguistique/test_bloc_linguistique.py
?? reports/performance-fix.json
?? reports/rapport-performance-fix.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/test_verifier_performance_fix.py
?? tools/verifier_performance_fix.py
---SUBMODULE---
 M generateur.py
 M tests/test_generateur.py
---DIFFSTAT---
 docs/pilotage/en-cours.md                          |  21 +-
 docs/pilotage/roadmap.md                           |  31 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |   4 +-
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json       
… [856 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-143", "timeout_ms": 600000, "wait": true}`

  ```
EXIT:0
=== PASSE COMPLÈTE DES PORTES (15 portes, borne 1800 s) ===
    journaux : work/portes-1116-00h14
  porte-banc-performance ✅                          16 s  ✅ porte banc-performance verte
  porte-bloc-code        ✅                          17 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-document         ✅                           7 s  ✅ porte document verte
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-lecteur          ✅                           0 s  ✅ porte lecteur verte
  porte-lecture          ✅                           2 s  ✅ porte lecture verte
  porte-miroir-blocs     ✅                          12 s  ✅ porte miroir verte
  porte-produit          ✅                         171 s  ✅ porte produit vert
… [605 caractères tronqués]
  ```

- **bash** `{"command": "git add generateur.py tests/test_generateur.py && git commit -m \"U1 — générateur S : construire_arbre et cibles en O(k), sorties identiques (620 textes)\" && git log --oneline -1", "description": "Commit submodule changes", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/to … [16 caractères tronqués]`

  ```
[master 648adce] U1 — générateur S : construire_arbre et cibles en O(k), sorties identiques (620 textes)
 2 files changed, 71 insertions(+), 16 deletions(-)
648adce U1 — générateur S : construire_arbre et cibles en O(k), sorties identiques (620 textes)
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -10; git status --short reports/INDEX.md reports/README.md", "description": "Regenerate reports index"}`

  ```
763 fiches → reports/INDEX.md
 M reports/INDEX.md
  ```

- **bash** `{"command": "git diff reports/INDEX.md | head -60", "description": "Check index diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 3d18d19e..c76c747a 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **762 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **763 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -634,6 +634,7 @@
 | [rapport-pensee-votante3.md](rapport-pensee-votante3.md) | B13 — l'observation à trois looks : 20/20, mais 4000 épisodes |
 | [rapport-pensee-vote.md](rapport-pensee-vote.md) | B13 — le vote de signaux : 5 looks, toujours 0/20 |
 | [rapport-pensee-vrais-absents.md](rapport-pensee-vrais-absents.md) | B13 — les vrais absents : 5 phrases sans antécédent, 0 lien |
+| [rapport-performance-fix.md](rapport-performance-fix.md) | U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près** |
 | [rapport-performance.md](rapport-performance.md) | T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSO
… [265 caractères tronqués]
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md reports/INDEX.md reports/performance-fix.json reports/rapport-performance-fix.md tools/bloc_linguistique.py tools/tests/linguistique/test_bloc_linguistique.py tools/t … [171 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
M  reports/INDEX.md
A  reports/performance-fix.json
A  reports/rapport-performance-fix.md
M  tools/bloc_linguistique.py
M  tools/structures
M  tools/tests/linguistique/test_bloc_linguistique.py
A  tools/tests/test_verifier_performance_fix.py
A  tools/verifier_performance_fix.py
  ```

- **bash** `{"command": "git commit -m \"U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO\" && git log --oneline -1", "description": "Commit U1 main repo"}`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-149]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-149", "timeout_ms": 600000, "wait": true}`

  ```
[s/v7 d19f0fc7] U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
 20 files changed, 6075 insertions(+), 120 deletions(-)
 create mode 100644 journal/2026-11-16/README.md
 create mode 100644 journal/sessions/session-cd495112-6c06-43ec-b56a-47ad7d92ba6f/digest.md
 create mode 100644 journal/sessions/session-cd495112-6c06-43ec-b56a-47ad7d92ba6f/rapport.md
 create mode 100644 reports/performance-fix.json
 create mode 100644 reports/rapport-performance-fix.md
 create mode 100644 tools/tests/test_verifier_performance_fix.py
 create mode 100755 tools/verifier_performance_fix.py
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | head -40; echo ---; git status --short | head -30", "description": "Inspect commit contents and status"}`

  ```
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
 docs/pilotage/en-cours.md                          |   21 +-
 docs/pilotage/roadmap.md                           |   31 +-
 journal/2026-11-16/README.md                       |   25 +
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   52 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |    4 +-
 .../rapport.md                                     |   14 +-
 .../digest.md                                      |  104 +
 .../rapport.md                                     |   46 +-
 .../digest.md                                      | 4299 ++++++++++++++++++++
 .../rapport.md                                     |  201 +
 reports/INDEX.md                                   |    3 +-
 reports/performance-fix.json                       |  542 +++
 reports/rapport-performance-fix.md                 |  189 +
 tools/bloc_linguistique.py                         |  345 +-
 tools/struct
… [691 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo EXIT:${PIPESTATUS[0]}", "description": "Doc review after commit"}`

  ```
revue de documentation · 766 fiche(s) · 861 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT:0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_journal.py 2>&1 | tail -4; echo EXIT2:${PIPESTATUS[0]}; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|✅|violation\" | tail -3; echo EXIT3:${PIPESTATUS[0]}", "description": "St … [29 caractères tronqués]`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT:0
  journal · 48 jour(s) · 223 session(s) · 2695 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT2:0
  T0 max : 3998 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT3:0
  ```

- **bash** `{"command": "PORTES=\"porte-etat porte-sessions porte-budget porte-registre\" bash tools/toutes-les-portes.sh 2>&1 | tail -12; echo EXIT:${PIPESTATUS[0]}", "description": "Re-run state gates after commit"}`

  ```
[still running after 60000ms; moved to background job bash-153]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-153", "timeout_ms": 300000, "wait": true}`

  ```
=== PASSE COMPLÈTE DES PORTES (4 portes, borne 1800 s) ===
    journaux : work/portes-1116-00h22
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-registre         ✅                          17 s    ✅ région absente : refusée en la nommant (code 2), rien n'est calculé
  porte-sessions         ✅                           0 s  PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
--- 4 vertes, 0 rouges ---
TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant.
Journaux : work/portes-1116-00h22
EXIT:0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git ls-tree HEAD tools/structures; git -C tools/structures log --oneline -1; git log --oneline -3", "description": "Verify submodule pointer"}`

  ```
160000 commit 648adce3ea18ef4d142778fd67d42413aae5ae64	tools/structures
648adce U1 — générateur S : construire_arbre et cibles en O(k), sorties identiques (620 textes)
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
  ```

- **bash** `{"command": "grep -n \"ce commit\\|83adaa2b\\|389b99f\" reports/rapport-performance-fix.md reports/performance-fix.json | head -20", "description": "Find commit references"}`

  ```
reports/rapport-performance-fix.md:26:> `/usr/bin/time -f %M`. Avant = commit **`83adaa2b`** (sous-module `389b99f`), après = ce
reports/rapport-performance-fix.md:184:Pour l'« avant », se placer sur `83adaa2b` avec le sous-module `389b99f` ; pour l'« après »,
reports/rapport-performance-fix.md:185:sur ce commit. Le JSON brut de la fiche est [`reports/performance-fix.json`](performance-fix.json).
reports/performance-fix.json:35:  "commit_avant": "83adaa2b6f8c6b1f03480375d30170a7613c71f8",
reports/performance-fix.json:36:  "sous_module_avant": "389b99f",
reports/performance-fix.json:37:  "commit_mesure": "83adaa2b + patch U1 (mesure faite avant le commit)"
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "limit": 5, "offset": 24}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "limit": 5, "offset": 182}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md</path>
<type>file</type>
<content>
24: > contrôle négatif. Machine à 40 cœurs (Xeon E5-2687W v3, 125 Go), Python 3.13.16,
25: > `PYTHONHASHSEED=0`, mesures froides répétées 3 fois (médiane), mémoire par
26: > `/usr/bin/time -f %M`. Avant = commit **`83adaa2b`** (sous-module `389b99f`), après = ce
27: > commit.
28: 

(Showing lines 24-28 of 189. Use offset=29 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md</path>
<type>file</type>
<content>
182: ```
183: 
184: Pour l'« avant », se placer sur `83adaa2b` avec le sous-module `389b99f` ; pour l'« après »,
185: sur ce commit. Le JSON brut de la fiche est [`reports/performance-fix.json`](performance-fix.json).
186: 

(Showing lines 182-186 of 189. Use offset=187 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "new_string": "> `/usr/bin/time -f %M`. Avant = commit **`83adaa2b`** (sous-module `389b99f`), après = commit\n> **`d19f0fc7`** (sous-module `648adce`).", "old_string": "> `/usr/bin/time -f %M`. Avant … [73 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "new_string": "Pour l'« avant », se placer sur `83adaa2b` avec le sous-module `389b99f` ; pour l'« après »,\nsur `d19f0fc7` (sous-module `648adce`). Le JSON brut de la fiche est\n[`reports/performance … [247 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/performance-fix.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nd['source']['commit_apres']='d19f0fc7'\nd['source']['sous_module_apres']='648adce'\nd['source']['commit_mesure']='83adaa2b + patch U1 (mesure faite avant  … [244 caractères tronqués]`

  ```
ok
JSON_OK
  ```

- **bash** `{"command": "git add reports/performance-fix.json reports/rapport-performance-fix.md && git commit -m \"U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)\" 2>&1 | tail -20", "description": "Commit report commit pointers", "run_in_background": true}`

  ```
started background job bash-157
  ```

- **job_output** `{"job_id": "bash-157", "timeout_ms": 300000, "wait": true}`

  ```
❌ commit refusé : 2 fait(s) stagé(s) sans docs/pilotage/en-cours.md
     · reports/performance-fix.json
     · reports/rapport-performance-fix.md
     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`
  ⛔ commit refusé : un fait sans ligne d'état.
     mets docs/pilotage/en-cours.md à jour, puis :
     git add docs/pilotage/en-cours.md
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-157 (bash: git add reports/performance-fix.json reports/rapport-performance-fix.md && git commit -m "U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)" 2>&1 | tail -20) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "grep -n \"U1.*O(k²)\" docs/pilotage/en-cours.md", "description": "Find U1 line in state"}`

  ```
3:**Mis à jour : 2026-11-16, 00 h 30 HNE (U1 : les deux O(k²) bornés, α 1,08)**
62:- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)).
123:**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, sorties identiques) ; reste **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performance-fix.md).
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 2, "offset": 62}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
62: - **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)).
63: - **Prochaine action** : **U2 — la roue** ; **U3 — `--profils`** ; **J4** ; T132/T133.

(Showing lines 62-63 of 145. Use offset=64 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** (`d19f0fc7` ; [fiche](../../reports/rapport-performance-fix. … [299 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅\" | tail -3; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -2", "description": "Check budget after hash addition"}`

  ```
T0 max : 4000 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT:0
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md reports/performance-fix.json reports/rapport-performance-fix.md && git commit -m \"U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)\" 2>&1 | tail -25", "description": "Commit report pointers with state", "run_in_ba … [16 caractères tronqués]`

  ```
started background job bash-160
  ```

- **job_output** `{"job_id": "bash-160", "timeout_ms": 300000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 75a56c05] U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
 12 files changed, 317 insertions(+), 29 deletions(-)
 create mode 100644 journal/2026-11-16/mesures.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo EXIT:${PIPESTATUS[0]}; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|✅|violation\" | tail -2; echo EXIT2:${PIPESTATUS[0]}", "description": "Final doc and budget checks"}`

  ```
revue de documentation · 766 fiche(s) · 861 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT:0
  T0 max : 4000 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT2:0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -2; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_journal.py 2>&1 | tail -2; echo EXIT2:${PIPESTATUS[0]}", "description": "Final state and journal checks"}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT:0
  journal · 48 jour(s) · 223 session(s) · 2698 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT2:0
  ```

- **bash** `{"command": "PORTES=\"porte-etat porte-sessions\" bash tools/toutes-les-portes.sh 2>&1 | tail -8; echo EXIT:${PIPESTATUS[0]}", "description": "Final state gates"}`

  ```
=== PASSE COMPLÈTE DES PORTES (2 portes, borne 1800 s) ===
    journaux : work/portes-1116-00h27
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-sessions         ✅                           0 s  PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
--- 2 vertes, 0 rouges ---
TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant.
Journaux : work/portes-1116-00h27
EXIT:0
  ```

- **bash** `{"command": "git status --short | head -30; echo ---; git log --oneline -3; echo ---; git -C tools/structures status --short", "description": "Final git status"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
75a56c05 U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
---
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/u1-after/performance-apres4.json'))\nprint(d['echelle']['instrument'])\nPY", "description": "Check instrument control values after"}`

  ```
{'lineaire': {'mesures': [{'n': 250, 'duree_s': 0.012460159952752292, 'repetitions': 2}, {'n': 500, 'duree_s': 0.016452351468615234, 'repetitions': 2}, {'n': 1000, 'duree_s': 0.018104088958352804, 'repetitions': 2}, {'n': 2000, 'duree_s': 0.03349860664457083, 'repetitions': 2}, {'n': 4000, 'duree_s': 0.06254448147956282, 'repetitions': 2}, {'n': 8000, 'duree_s': 0.128169885603711, 'repetitions': 2}, {'n': 10000, 'duree_s': 0.15085095493122935, 'repetitions': 2}], 'loglog': {'alpha': 0.7068492410791721, 'beta': -8.556390977118182, 'r2': 0.9531690413362014, 'rmse': 0.20244971783321805, 'n': 7}, 'lineaire': {'a': 0.0063776136853512105, 'b': 1.465775663073149e-05, 'r2': 0.9970381484010841, 'rmse': 0.0028739728686698715, 'n': 7}, 'quadratique': {'a': 0.007036259274941748, 'b': 1.4014615622721764e-05, 'c': 6.448761863941637e-11, 'r2': 0.997134654628743, 'rmse': 0.002826763694808254, 'n': 7}, 'pente_attendue': 1.0}, 'quadratique': {'mesures': [{'n': 250, 'duree_s': 0.0026274354895576835, 'repetitions': 2}, {'n': 500, 'duree_s': 0.01373206009157002, 'repetitions': 2}, {'n': 1000, 'duree_s': 0.06538392452057451, 'repetitions': 2}, {'n': 2000, 'duree_s': 0.25916838843841106, 'repetitions': 2
… [638 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['/tmp/u1-before/performance-avant.json','/tmp/u1-after/performance-apres.json','/tmp/u1-after/performance-apres2.json','/tmp/u1-after/performance-apres3.json','/tmp/u1-after/performance-apres4.json']:\n try:\n  d=json.load(open(p)); i=d['echelle' … [226 caractères tronqués]`

  ```
/tmp/u1-before/performance-avant.json lin 0.7823 quad 2.1333
/tmp/u1-after/performance-apres.json lin 0.7491 quad 2.1162
/tmp/u1-after/performance-apres2.json lin 0.7048 quad 2.1244
/tmp/u1-after/performance-apres3.json lin 0.7818 quad 2.1206
/tmp/u1-after/performance-apres4.json lin 0.7068 quad 2.1131
  ```

- **bash** `{"command": "grep -n \"instrument\" reports/rapport-performance-fix.md", "description": "Find instrument sentence"}`

  ```
55:**1,15**. Le contrôle de l'instrument n'a pas bougé : la boucle volontairement linéaire
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "limit": 6, "offset": 53}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md</path>
<type>file</type>
<content>
53: Le terme quadratique n'apporte plus que **+0,00077 de R²** (contre **+0,0414** avant) : il
54: n'est **pas significatif** au critère du banc (< 0,02), et α = **1,076** est sous le seuil
55: **1,15**. Le contrôle de l'instrument n'a pas bougé : la boucle volontairement linéaire
56: donne α = 0,9998, la boucle volontairement quadratique α = 2,0045.
57: 
58: ## 2. Les 10 000 mots

(Showing lines 53-58 of 190. Use offset=59 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md", "new_string": "**1,15**. Le contrôle de l'instrument, dans la même passe : la boucle volontairement\nlinéaire donne α = **0,71** (0,78 avant), la boucle volontairement quadratique α = **2,11**\n(2,13  … [285 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/performance-fix.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nav=json.load(open('/tmp/u1-before/performance-avant.json'))['echelle']['instrument']\nap=json.load(open('/tmp/u1-after/performance-apres4.json'))['echelle … [684 caractères tronqués]`

  ```
ok
JSON_OK
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 2, "offset": 123}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
123: **T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, sorties identiques) ; reste **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performance-fix.md).
124: 

(Showing lines 123-124 of 145. Use offset=125 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, instrument 0,71/2,11) ; reste **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploit … [326 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅\" | tail -2; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -2", "description": "Check budget after instrument change"}`

  ```
T0 max : 4000 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT:0
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md reports/performance-fix.json reports/rapport-performance-fix.md && git commit -m \"U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)\" 2>&1 | tail -20", "description": "Commit instrument  … [39 caractères tronqués]`

  ```
started background job bash-170
  ```

- **job_output** `{"job_id": "bash-170", "timeout_ms": 300000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 04894aea] U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
 10 files changed, 210 insertions(+), 16 deletions(-)
 create mode 100644 journal/2026-11-16/memoire.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3; echo EXIT:${PIPESTATUS[0]}; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|✅|violation\" | tail -2; echo EXIT2:${PIPESTATUS[0]}", "description": "Final doc review"}`

  ```
revue de documentation · 766 fiche(s) · 861 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT:0
  T0 max : 4000 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT2:0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -2; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_journal.py 2>&1 | tail -2; echo EXIT2:${PIPESTATUS[0]}", "description": "Final state/journal"}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT:0
  journal · 48 jour(s) · 223 session(s) · 2701 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT2:0
  ```

- **bash** `{"command": "PORTES=\"porte-etat porte-sessions\" bash tools/toutes-les-portes.sh 2>&1 | tail -6; echo EXIT:${PIPESTATUS[0]}", "description": "Final state gates after correction"}`

  ```
journaux : work/portes-1116-00h30
  porte-etat             ✅                           1 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-sessions         ✅                           0 s  PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
--- 2 vertes, 0 rouges ---
TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant.
Journaux : work/portes-1116-00h30
EXIT:0
  ```

- **bash** `{"command": "python3 tools/verifier_performance_fix.py --comparer /tmp/u1-before /tmp/u1-after4 2>&1 | tail -4; echo EXIT:${PIPESTATUS[0]}", "description": "Final negative control"}`

  ```
identique bloc-x40.json                 18197238 octets  28a412b9ae7d6a78
identique gold-annotations-612.json      4281465 octets  b61c1521328bde42
identique gold-annotations-452.json      3222340 octets  de329b530ddafbca
10/10 identiques — diff vide
EXIT:0
  ```

- **bash** `{"command": "git status --short | head -20; echo ---; git log --oneline -4", "description": "Final git status"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
04894aea U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
75a56c05 U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
  ```

- **todo_write** `{"todos": [{"content": "Implémenter les index O(k log k) et le balayage (bloc + générateur S)", "status": "completed"}, {"content": "Vérifier l'identité des sorties avant/après (612, 452, 10 000 mots, blocs)", "status": "completed"}, {"content": "Mesurer α, temps 10 000 mots, mémoire, contrôle quadr … [474 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 8 completed.
  ```

### 🤖 Assistant

## U1 — les deux O(k²) sont bornés, sorties identiques

**Résultat mesuré** (même bloc contrôlé T4, 247 mots ×1…×40 ; médianes de 3 répétitions) :

| mesure | avant | après |
|---|---:|---:|
| 10 000 mots — fonction | **3,991 s** | **0,816 s** (×4,89) |
| débit | 2 506 mots/s | **12 259 mots/s** |
| CLI `--json` | 5,011 s | **1,668 s** |
| pic RSS fonction | 126,9 Mio | **127,4 Mio** (+0,5 Mio) |
| JSON indenté | 14 795 890 o | **14 795 890 o** (identique) |
| **α** bloc contrôlé | **1,530** | **1,076** |
| ΔR² quadratique − linéaire | +0,0414 | **+0,00077** |
| contrôle linéaire | ❌ | ✅ |

**Objectif atteint** : α = 1,076 ≤ 1,15, terme quadratique non significatif.

### Ce qui a été corrigé

- `_groupes_partition` : toutes les paires O(k²) → **balayage O(k log k)**.
- `_cible_proche` / `_verbes_proches` : tri de tous les GV à chaque segment → **`_IndexGV`** (gauche/droite/chevauchement + tas), O(log m + candidats).
- Le profil a ensuite nommé trois autres boucles quadratiques, corrigées sans changer les résultats :
  - `_sujet_hors_gv` (`any()` sur tous les segments par GV) → fins de GN triées + `bisect` ;
  - `_repli_cible_gp` / `_cible_rel_sujet` → `_IndexFins` / `_IndexSegments` ;
  - `construire_arbre` et les cibles de `_segmente` dans le générateur S → balayage O(k).
- `_expliciter_partition` : `deepcopy` des candidats → copie superficielle.

### Contrôle négatif — diff vide

`python3 tools/verifier_performance_fix.py --comparer /tmp/u1-before /tmp/u1-after4` :

```
10/10 identiques — diff vide
```

Sont identiques **octet pour octet** : 10 000 mots, blocs ×1…×40, annotations des 612 phrases et des 452 réelles. Le générateur S a aussi été comparé directement sur **620 textes** : identique. Les métriques gold sont inchangées : POS **0,8625**, F1 syntagmes **0,7902**, attachement top-k **0,9874** sur 612 ; POS **0,8891**, F1 **0,7906**, top-k **0,9891** sur 452.

### Tests et portes

- `tools/tests/linguistique/test_bloc_linguistique.py` : **25 tests OK** (dont 5 différentiels ancien/nouveau).
- `tools/structures/tests/test_generateur.py` : **27 tests OK**.
- `tools/tests/test_verifier_performance_fix.py` : **3 tests OK**.
- Portes ciblées U1 : **15/15 vertes** (`banc-performance`, `bloc-linguistique`, `produit`, `budget`, `état`, `sessions`, `registre`, etc.), puis **2/2** après commit.
- Revue de documentation, `verifie_en_cours`, `verifie_journal`, budget : **verts**.
- La passe complète des 86 portes n’a pas été relancée (précédent T6) ; les rouges structurelles connues restent `indice` et `melange`.

### Livrables et commits

- Fiche : [`reports/rapport-performance-fix.md`](reports/rapport-performance-fix.md)
- JSON : [`reports/performance-fix.json`](reports/performance-fix.json)
- Contrôle négatif rejouable : [`tools/verifier_performance_fix.py`](tools/verifier_performance_fix.py)
- Sous-module `tools/structures` : commit **`648adce`**
- Dépôt principal : **`d19f0fc7`** (résultat), **`75a56c05`** (pointeurs de commits), **`04894aea`** (correction du contrôle de l’instrument — linéaire 0,71, quadratique 2,11, et non les valeurs de T4).

Les modifications antérieures non liées (`reports/pensee-*`, `tools/chantier/plan.json`, etc.) sont restées hors commit.

