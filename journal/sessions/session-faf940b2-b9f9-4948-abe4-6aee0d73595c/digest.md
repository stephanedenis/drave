# Session DSH — relecture

- identifiant : `session-faf940b2-b9f9-4948-abe4-6aee0d73595c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 23:16:47
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche T5 (exploitable, 5/5) : la **robustesse de la CLI** — (1) `--duree` dans le JSON (le temps de l'analyse) ; (2) le **tableau des codes de sortie** (0 succès, 3 refus, 4 clé/dépendance, 5 usage) dans `docs/produit/README.md` et le `--aide` ; (3) `--aide`/`--help` vérifiés sur les quatre sous-commandes ; (4) un `--fichier` sur un chemin **inexistant** et un **répertoire** : le message et le code attendus, pas de trace. Fiche `reports/rapport-cli-robuste.md` + JSON, un test par cas dans `tools/tests/test_produit.py`.

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

- **bash** `{"command": "git status --short && git log --oneline -5 && ls", "description": "Check git status and list files"}`

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
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PLUS DE SYNTAGMES (1 075 CONTRE 1 006) ET VA PLUS VITE ; LE TEMPS NE SUIT PAS LES MOTS SEULS
7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))
7d114559 T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
AGENTS.md
bench
colab
data
… [321 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ docs/produit/ reports/ 2>/dev/null | head -100", "description": "List key directories"}`

  ```
docs/produit/:
demarrage.md
exemples.md
README.md

reports/:
07
07-mesures-couche-commune.md
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a80-indice-qualifie.json
a80-melange-qualifie.json
a80-pannes-ppl.json
a80-porte-adaptateur.json
a80-porte-budget.json
a80-porte-bus.json
a80-porte-bus-socket.json
a80-porte-c4-retard.json
a80-porte-consolidation.json
a80-porte-cycle-c2.json
a80-porte-delais.json
a80-porte-flux.json
a80-porte-fusion.json
a80-porte-gain.json
a80-porte-pont.json
a80-porte-profondeur.json
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
analyse-litteraire.json
archive
atomes-niveaux.json
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
b1110b-hybride.json
b1110-cartes.json
b1110c-case.json
b
… [920 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/produit/README.md", "description": "Read product README"}`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
> existent, et la
> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
> Le format
> est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
> § 3.5 ont été relanc
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "cat pyproject.toml && echo ==== && grep -rn \"argparse\\|--aide\\|--help\" src/ tools/ --include=*.py | head -60", "description": "Find CLI implementation"}`

  ```
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "drave"
version = "0.1.0"
description = "Le point d'entrée produit du bloc linguistique de Drave."
requires-python = ">=3.10"
dependencies = []

[project.scripts]
drave = "tools.drave:main"

[tool.setuptools]
packages = ["tools"]
====
tools/make_patch.py:15:import argparse, struct, sys
tools/make_patch.py:23:    ap = argparse.ArgumentParser()
tools/aiguille.py:34:import argparse
tools/aiguille.py:126:    ap = argparse.ArgumentParser()
tools/mla_synthetique.py:18:import argparse
tools/mla_synthetique.py:225:    ap = argparse.ArgumentParser()
tools/trace_compacite.py:43:import argparse
tools/trace_compacite.py:284:    p = argparse.ArgumentParser(
tools/trace_compacite.py:285:        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
tools/telecharger_modeles.py:17:import argparse
tools/telecharger_modeles.py:126:    ap = argparse.ArgumentParser()
tools/clusters_moe.py:26:import argparse
tools/clusters_moe.py:143:    ap = argparse.ArgumentParser()
tools/convertir_clusters.py:32:import argparse
tools/convertir_clusters.py:403:    ap = argparse.ArgumentParser()

… [2704 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/drave.py tools/tests/test_produit.py && sed -n '1,200p' tools/drave.py", "description": "Read CLI head"}`

  ```
1254 tools/drave.py
  354 tools/tests/test_produit.py
 1608 total
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement,
… [7302 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"duree\\|--fichier\\|--aide\\|--help\\|exit\\|SystemExit\\|return [0-9]\" tools/drave.py | head -120", "description": "Find durations, file, exits in CLI"}`

  ```
502:    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
530:        return 3
538:    return 0
580:            return 4
601:                return 3
607:                return 1
617:            return 3
628:    return 0
656:        return 0.0
762:        return 2
775:            return 4
869:    return 0
879:        return 1
893:        return 1
894:    return 0
914:        return 2
918:        return 2
922:        return 2
926:        return 2
929:            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
931:            return 2
937:            return 1
946:                return 1
968:        return 0
972:        print(f"{NOM}: erreur d'usage : TEXTE ou --fichier requis", file=sys.stderr)
973:        return 2
978:        return 3
989:        return 0
1000:        return 0
1011:        return 0
1021:    return 0
1028:    """Un parseur francophone : `-h`, `--help` et `--aide` partout, sans doublon."""
1035:        self.add_argument("-h", "--help", "--aide", action="help",
1040:        self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")
1118:                          help="texte à analyser (entre guillemets) ou --fichier")
1122:    a
… [354 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '470,660p' tools/drave.py", "description": "Read text/file and analyser"}`

  ```
ici = par_span.get((p.debut, p.fin), [])
            acte = next((e.valeur for e in ici if e.type == "acte"), "—")
            negation = "oui" if any(e.type == "négation" for e in ici) else "non"
            modalite = "oui" if any(e.type == "modalité" for e in ici) else "non"
            double_sens = "oui" if any(e.type == "double_sens" for e in ici) else "non"
            lignes.append(
                f"  phrase [{p.debut}:{p.fin}] {p.valeur} · acte={acte} "
                f"· négation={negation} · modalité={modalite} · double sens={double_sens}"
            )
    else:
        lignes.append("PRAGMATIQUE —")

    couverture = a.couverture()
    if couverture:
        ordre = [n for n in bl.NIVEAUX if n in couverture]
        ordre += sorted(n for n in couverture if n not in bl.NIVEAUX)
        lignes.extend(_envelopper(
            "COUVERTURE  ",
            "(confiance max par niveau)  "
            + " · ".join(f"{n}={couverture[n]:.2f}" for n in ordre),
        ))
    if tagger and a.refus:
        lignes.extend(_envelopper("REFUS TAGGER  ", a.refus))
    if stats is not None:
        lignes.extend(_envelopper("TAGGER API  ", _ligne_tagger(stats)))
    return "\n".join(li
… [7258 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '860,1254p' tools/drave.py", "description": "Read main and parser"}`

  ```
}
            par_langue[langue] = m
        rapport["par_langue"] = par_langue
    if args.json:
        sys.stdout.write(_dumps(rapport))
        if stats is not None:
            print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
    else:
        print(_formater_evaluation(rapport))
    return 0


def cmd_rejouer(args: argparse.Namespace) -> int:
    premiere = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    seconde = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    if premiere.refus or seconde.refus:
        refus = premiere.refus or seconde.refus
        print(f"{NOM}: refus d'analyse : {refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 1
    canonique_1 = _canonique(premiere)
    canonique_2 = _canonique(seconde)
    identique = canonique_1 == canonique_2
    empreinte = hashlib.sha256(canonique_1.encode("utf-8")).hexdigest()[:16]
    print(f"rejeu identique : {'oui' if identique else 'non'}")
    print(f"  texte      : {args.texte!r}")
    print(f"  langue     : {premiere.langue}")
    print(f"  étiquettes : {len(premiere.etiquet
… [19095 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"T5\\|code 5\\|code de sortie 5\\|sortie.*5\\|--duree\\|duree_s\" docs/ reports/ tools/chantier/ journal/ --include=*.md --include=*.json --include=*.py | head -80", "description": "Search spec for exit code 5 and duree"}`

  ```
docs/archive/architecture-kimi-k3.md:284:| MLA à rang faible + tête latente + porte de sortie | V4/V4.1 (`Mla4`) | **acquis**, à adapter aux dims (1 536/512/192/128/64) |
docs/archive/cerveau-facultes.md:23:| **réflexes** | chemin court **entraîné** (LoRA couches basses + lecteur de sortie) | **÷1,47** (m32) et **÷1,24** (m20) à 8 couches, lus par le moteur | 0,07 % des poids (rang 8) · **0,035 %** au point efficient (rang 4) | ✅ |
docs/archive/cerveau-facultes.md:39:| **motricité / effecteurs** | `--sortie F` + réflexes ; le moteur **écrit** ce que le réflexe produit | le signal **courant** est dans la sortie (R² 0,992) ; le réflexe distillé génère **×2,0** plus vite mais **différemment** du cerveau | 357,8 M paires/décision (complet) | 🟡 |
docs/archive/etat-cerveau.md:10:> une action était **périmée** (la carte des sorties de H avait tourné le 11/10 à 00 h 15, le plan
docs/archive/etat-cerveau.md:53:| **C7** | consolidation · **+ sélection par ÉTALEMENT (15/10, tempérée)** | ✅ **fait, et désormais mesurée DANS LES POIDS (14/10)** | l'**exemplaire** bat la **moyenne** (7 % du magasin → **87 %** de rappel) ; rejeu répété = **point fixe exact** (0,00e0) ; et la consolidation par rej
… [18345 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"returncode\\|exit.*2\\|code.*2\\|code 2\\|--fichier\" tools/tests/test_produit.py tools/porte-produit.sh 2>/dev/null | head -80", "description": "Inspect existing tests exit code assumptions"}`

  ```
tools/tests/test_produit.py:33:    return (f"code={resultat.returncode}\n"
tools/tests/test_produit.py:45:            version.returncode == 0
tools/tests/test_produit.py:47:            and aide.returncode == 0
tools/tests/test_produit.py:55:            resultat.returncode == 0 and "langue=fr" in resultat.stdout,
tools/tests/test_produit.py:67:            resultat.returncode == 0
tools/tests/test_produit.py:79:            premier.returncode == 0
tools/tests/test_produit.py:93:            resultat.returncode == 0
tools/tests/test_produit.py:104:            (sans_commande.returncode, langue_inconnue.returncode),
tools/tests/test_produit.py:116:        self.assertEqual(sortie.returncode, 0, detail(sortie))
tools/tests/test_produit.py:139:        self.assertEqual(sortie.returncode, 0, detail(sortie))
tools/tests/test_produit.py:152:        self.assertEqual(sortie.returncode, 0, detail(sortie))
tools/tests/test_produit.py:214:        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
tools/tests/test_produit.py:223:        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
tools/tests/test_produit.py:233:        self.assertEqual(sortie.returncode, 0, detail(sortie))
too
… [1445 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,130p' tools/tests/test_produit.py && echo ==== && sed -n '250,354p' tools/tests/test_produit.py", "description": "Read product tests"}`

  ```
"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.

Huit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe
aussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du
dépôt directement, il lance la commande comme un utilisateur.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Lance la commande depuis la racine du dépôt, en UTF-8, sans réseau."""
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return (f"code={resultat.returncode}\n"
            f"stdout={resultat.stdout}\n"
            f"stderr={resultat.stderr}")


class TestProduit(unittest.TestCase):
    """Le contrat produit : version/aide, analyse, JSON, rejeu, usage."""


… [8889 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p))\ns=json.dumps(p,ensure_ascii=False)\ni=s.find('T5')\nprint(s[max(0,i-500):i+2500])\nPY", "description": "Read plan T5"}`

  ```
<class 'dict'>
), la **mémoire** (pic RSS), la **taille du JSON**, et le même sur 100 phrases courtes (le coût fixe par appel) ; compare avec `--tagger` (le coût réseau) ; le **contrôle négatif** : le temps doit croître linéairement avec la taille (pas quadratiquement). Fiche `reports/rapport-performance.md` + JSON, un banc reproductible (`tools/banc_performance.py` ?).", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-performance.md && echo FICHE-OK", "attendu": "FICHE-OK"}]}, {"id": "T5", "jour": 19, "titre": "La CLI — durée, codes de sortie, aide", "mandat": "Tâche T5 (exploitable, 5/5) : la **robustesse de la CLI** — (1) `--duree` dans le JSON (le temps de l'analyse) ; (2) le **tableau des codes de sortie** (0 succès, 3 refus, 4 clé/dépendance, 5 usage) dans `docs/produit/README.md` et le `--aide` ; (3) `--aide`/`--help` vérifiés sur les quatre sous-commandes ; (4) un `--fichier` sur un chemin **inexistant** et un **répertoire** : le message et le code attendus, pas de trace. Fiche `reports/rapport-cli-robuste.md` + JSON, un test par cas dans `tools/tests/test_produit.py`.", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-cli-robu
… [784 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"code 2\\|code=2\\|code.*\\b2\\b\\|sort 2\\|sortie 2\\|returncode.*2\\|\\$code.*2\\|-eq 2\" docs/produit/ tools/tests/test_produit.py tools/porte-produit.sh tools/verifier_faq.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md 2>/dev/null | head -80", "description": "Find c … [18 caractères tronqués]`

  ```
docs/produit/README.md:383:code **3**, distinct des erreurs (1) et de l'usage (2). Le message reste sur `stderr`. Un texte
docs/produit/README.md:505:prototype ; `evaluer --tagger auto` rend un code **2** d'usage. Mesures réelles, cache neuf par
docs/produit/README.md:753:| `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
tools/porte-produit.sh:111:if [ "$code" -eq 3 ] && printf '%s' "$refus" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['refus'] and d['schema']" 2>/dev/null; then
tools/verifier_faq.py:80:    assert refus.returncode == 2, refus.returncode
tools/verifier_faq.py:320:        assert r.returncode == 2, (fantome, r.returncode)
tools/verifier_faq.py:355:        "options_fantomes": {"--sortie": "code 2", "--mode": "code 2", "--strict": "code 2"},
tools/verifier_faq.py:432:    # Faux : « le CLI accepte --langue de ». Le code doit sortir 2.
tools/verifier_faq.py:436:    detecte = (r.returncode == 2
tools/verifier_faq.py:440:            "le CLI accepte --langue de (il sort 2)",
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../th
… [3300 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"erreur d'usage\\|usage invalide\\|Codes de sortie\\|codes de sortie\" tools/drave.py docs/produit/README.md docs/produit/demarrage.md docs/produit/exemples.md tools/porte-produit.sh | head -80", "description": "Find usage/error messages"}`

  ```
tools/drave.py:35:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
tools/drave.py:760:        print(f"{NOM}: erreur d'usage : --tagger auto n'est disponible que pour analyser",
tools/drave.py:912:        print(f"{NOM}: erreur d'usage : --roles-v3 et --canonique sont exclusifs",
tools/drave.py:916:        print(f"{NOM}: erreur d'usage : --roles (v2) et --roles-v3 sont exclusifs",
tools/drave.py:920:        print(f"{NOM}: erreur d'usage : --roles et --canonique sont exclusifs",
tools/drave.py:924:        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles ou "
tools/drave.py:929:            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
tools/drave.py:972:        print(f"{NOM}: erreur d'usage : TEXTE ou --fichier requis", file=sys.stderr)
tools/drave.py:1040:        self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")
tools/drave.py:1076:        "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·\n"
docs/produit/README.md:688:**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3 / 4** :
docs/produit/README.md:694:| **2** | usage invalide : argument, sous-commande, 
… [316 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"duree\\|cout\\|def json\\|def mesurer\" tools/bloc_linguistique.py | head -80", "description": "Find cout/duree in block"}`

  ```
69:    def json(self) -> dict:
87:    def json(self) -> dict:
132:    cout: dict = field(default_factory=dict)
149:    def json(self, avec_duree: bool = False) -> dict:
150:        cout = dict(self.cout)
151:        if not avec_duree:
152:            cout.pop("duree_s", None)
161:            "trace": list(self.trace), "cout": cout, "contexte": self.contexte,
365:              "regardes regardons regardez regardent écoute écoutes écoutons écoutez écoutent ouvre "
420:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
467:travailles travaillent travaillait regarder regarde regardes regardent regardait écouter écoute
468:écoutes écoutent écoutait aimer aime aimes aiment aimait finir finis finit finissent finissait
1569:                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
1575:                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})
1926:                          cout={"octets": len(texte.encode("utf-8", "replace")), "caracteres": len(texte),
1927:                                "etiquettes": len(etiquettes), "duree_s":
… [2506 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '680,700p' docs/produit/README.md; echo ====; sed -n '225,250p' docs/produit/demarrage.md; echo ====; sed -n '65,90p' tools/verifier_faq.py; sed -n '310,365p' tools/verifier_faq.py; sed -n '425,445p' tools/verifier_faq.py", "description": "Read docs and faq verifier sections"}`

  ```
| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |

**La porte produit, mesurée le 07/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et
étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **18 tests** de fumée, **8 tests**
de schéma (v2 + rétro-compatibilité v1), **4 tests** sur 50 textes libres, **11 tests** de
restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est
`tools/tests/test_produit.py`.

**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3 / 4** :

| code | sens | aujourd'hui |
|---:|---|---|
| **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
| **1** | erreur ; tagger qui refuse une phrase sans POS | argument illisible, divergence de rejeu, exception |
| **2** | usage invalide : argument, sous-commande, langue hors `fr`/`en` | `argparse` |
| **3** | refus **distinct** de l'erreur, avec l'annotation de refus sur `stdout` | `analyser ""`, `restituer "..."` |
| **4** | dépendance absente : la clé du tagger (absente **ou refusée**), en `--tagger` **explicite** |
… [7209 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"T5\\|durée, codes\\|robustesse de la CLI\\|fichier.*répertoire\\|répertoire.*fichier\\|code 5\\|code.*5\" docs/pilotage/semaine-2.md docs/pilotage/*.md reports/rapport-quickstart.md reports/rapport-empaquetage.md 2>/dev/null | head -80", "description": "Search planning docs f … [7 caractères tronqués]`

  ```
docs/pilotage/semaine-2.md:61:existe et sans changer le code de sortie. J2 fournit le coût et les cas d'erreur ; J5 applique ou
docs/pilotage/semaine-2.md:118:| **le code** | règles de rôles v3 ; décision tagger (si retenue) ; migration `/` et référents (S, sous-module) ; tests | tests verts, non-régression 452 et 56 tests S |
docs/pilotage/semaine-2.md:120:| **la clôture** | rapport semaine 2 + JSON ; tag `semaine-2-2026-11-20` sur le dernier commit de code vert ; semaine 21–22 en réserve | `awk '$2 != 0'` sur `work/portes-1115-09h53/registre.txt` ; ciblage `work/portes/w6-ciblage*` ; tag annoté |
docs/pilotage/chantiers.md:84:| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique** (POS **86,25 %**, F1 **0,7902**, attachement **238/238 labels (238/239 cibles, 0,9958)**, 1 span) + **produit `drave`** (contrat v1) ; **183/183** portes | B10.3 (encodeur) ; **B13** : 1 span (`g017`) ; la coordination S/A/R/N2 | A, N1, D (corpus) | R (R5), S/L (sémantique, pragmatique) |
docs/pilotage/chantiers.md:202:(encodeur), A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE l
… [6342 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/semaine-2.md; echo ====; sed -n '1,130p' reports/rapport-quickstart.md", "description": "Read planning and quickstart report"}`

  ```
# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle
… [18817 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '125,175p' reports/rapport-quickstart.md; echo ====; grep -n \"erreur\\|code\" docs/produit/demarrage.md | head -50; echo ====; sed -n '195,240p' docs/produit/demarrage.md", "description": "Read quickstart error section"}`

  ```
| **avec clé, explicite** | `drave analyser "Le chat dort." --tagger` | **0** | `source=cascade`, `TAGGER API … réseau=1 · cache=0 · tokens=130 · latence=0.9 s` | vide |
| **avec clé, cache chaud** | le même, seconde fois | **0** | `réseau=0 · cache=1 · tokens=0 · latence=0.0 s` | vide |

La clé n'apparaît ni dans `stdout`, ni dans `stderr`, ni dans le JSON. Le mode `auto` ne change
jamais le code de sortie (0 dans les deux cas) ; le 4 reste réservé à `--tagger` explicite.

### 3.6 Les trois erreurs

| cas | commande | code | `stdout` | `stderr` (extrait) |
|---|---|---:|---|---|
| texte vide | `drave analyser ""` | **3** | vide | `drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)` |
| `--tagger` sans clé | `drave analyser "Le chat dort." --tagger` | **4** | vide | `drave: dépendance absente : clé DeepSeek absente …` |
| `--fichier` inexistant | `drave analyser --fichier absent.txt` | **1** | vide | `drave: erreur : FileNotFoundError : [Errno 2] No such file or directory: 'absent.txt'` |

Avec `--json`, le refus de texte sort un **JSON valide** sur `stdout` (`refus: "vide"`,
`etiquettes: []`) et le code reste **3**. Un répertoire à la place du
… [4247 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2950,3020p' tools/bloc_linguistique.py; sed -n '140,170p' tools/bloc_linguistique.py", "description": "Read block CLI and annotation json"}`

  ```
# --------------------------------------------------------------------------- CLI


def _annotation_depuis_args(args) -> Annotation:
    if args.texte:
        texte = args.texte
    elif args.fichier:
        texte = pathlib.Path(args.fichier).read_text(encoding="utf-8")
    else:
        texte = sys.stdin.read()
    profils = None
    if args.profils:
        profils, _ = charger_profils_udhr(pathlib.Path(args.profils))
    h = Heuristique(profils=profils)
    n = MockNeuronal(profils)
    if args.mode == "heuristique":
        return h.analyser(texte, args.langue, args.contexte)
    if args.mode == "neuronal":
        if args.neuronal_reel:
            return NeuronalLLM(args.modele).analyser(texte, args.langue, args.contexte)
        return n.analyser(texte, args.langue, args.contexte)
    if args.mode == "parallele":
        return Parallele([h, n]).analyser(texte, args.langue, args.contexte)
    if args.mode == "cascade":
        return Cascade(h, n, seuil=args.seuil).analyser(texte, args.langue, args.contexte)
    raise SystemExit(f"mode inconnu : {args.mode}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--texte", default="
… [3378 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '650,875p' tools/drave.py", "description": "Read evaluer"}`

  ```
"""Contrôle négatif : une cible **exacte** tirée au hasard parmi les cibles du gold.

    Graine fixe, donc reproductible : c'est un plancher, pas une mesure de qualité.
    """
    cibles = _cibles_gold(phrases)
    if not cibles:
        return 0.0
    univers = sorted(set(cibles))
    rng = random.Random(0)
    justes = sum(1 for c in cibles if rng.choice(univers) == c)
    return round(justes / len(cibles), 4)


def _pct(valeur: float) -> str:
    return f"{100.0 * float(valeur):.2f} %"


def _points(delta: float) -> str:
    """Un écart de taux en **points** de pourcentage, avec son signe."""
    return f"{100.0 * float(delta):+.2f} pts"


def _formater_evaluation(rapport: dict) -> str:
    gold = rapport["gold"]
    mesure = rapport["heuristique"]
    pos = mesure["pos"]
    syn = mesure["syntagme"]
    tete = syn["tete"]
    att = mesure["attachement"]
    att_tete = mesure["attachement_tete"]
    prag = mesure["pragmatique"]
    controle = rapport["controle_negatif"]
    lignes = [
        f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
        f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
        f"{gold['cibles_attachement']}
… [10407 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"code 2\\|code=2\\|sort 2\\|CODES\\|codes\" reports/faq.json tools/verifier_faq.py reports/rapport-faq.md docs/produit/exemples.md | head -60", "description": "Find code 2 in faq artifacts"}`

  ```
reports/faq.json:25:     "--langue de": "code 2"
reports/faq.json:274:     "--sortie": "code 2",
reports/faq.json:275:     "--mode": "code 2",
reports/faq.json:276:     "--strict": "code 2"
reports/faq.json:343:   "le CLI accepte --langue de (il sort 2)",
reports/faq.json:347:   "--langue de": "code 2",
tools/verifier_faq.py:355:        "options_fantomes": {"--sortie": "code 2", "--mode": "code 2", "--strict": "code 2"},
tools/verifier_faq.py:440:            "le CLI accepte --langue de (il sort 2)",
reports/rapport-faq.md:15:> contrôle négatif est explicite : le CLI **refuse** `--langue de` (code 2) et le schéma v2
reports/rapport-faq.md:56:| 1 | **Quelles langues ?** | détection `de`/`es`, `und` sous le seuil ; `--langue` limité à `fr`/`en` ; `--langue de` → code 2 ; 398 profils UDHR (0,9687) | `q1_langue` |
reports/rapport-faq.md:64:| 9 | **Les limites ?** | pas de génération, serveur, RSN, local, classement, calibration, `--langue-forcee`, garantie hors domaine ; `--sortie`/`--mode`/`--strict` → code 2 ; **pas de wheel/PyPI** | `q9_limites` |
reports/rapport-faq.md:120:   `--langue`, les codes de sortie, la fusion `--tagger`, les choix de `--partition` ou la
  ```

- **bash** `{"command": "grep -rn \"return 2\\|exit(2\\|code 2\\|code=2\\|-eq 2\\|== 2\" tools/drave.py tools/porte-produit.sh tools/verifier_faq.py tools/tests/test_produit.py docs/produit/*.md reports/rapport-quickstart.md reports/quickstart.json 2>/dev/null", "description": "Find all code 2 references"}`

  ```
tools/drave.py:762:        return 2
tools/drave.py:914:        return 2
tools/drave.py:918:        return 2
tools/drave.py:922:        return 2
tools/drave.py:926:        return 2
tools/drave.py:931:            return 2
tools/drave.py:973:        return 2
tools/drave.py:1040:        self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")
tools/verifier_faq.py:80:    assert refus.returncode == 2, refus.returncode
tools/verifier_faq.py:135:    assert apres["cout"]["tokens"] == 22299, apres["cout"]["tokens"]
tools/verifier_faq.py:197:    assert len(vingt["cas"]) == 26 and all(c["ok"] for c in vingt["cas"]), vingt["cas"]
tools/verifier_faq.py:202:    assert v2["properties"]["version"]["const"] == 2
tools/verifier_faq.py:221:    assert d["gold"]["phrases"] == 612 and d["gold"]["cibles_attachement"] == 239, d["gold"]
tools/verifier_faq.py:222:    assert a["cibles"] == 239 and a["labels"] == 238, a
tools/verifier_faq.py:320:        assert r.returncode == 2, (fantome, r.returncode)
tools/verifier_faq.py:355:        "options_fantomes": {"--sortie": "code 2", "--mode": "code 2", "--strict": "code 2"},
tools/verifier_faq.py:436:    detecte = (r.returncode == 2
docs/produit/README.md:753:| 
… [125 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/porte-produit.sh", "description": "Read product gate"}`

  ```
#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
  if printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['langue'] == '$langue', d.get('langue')
assert len(d['etiquettes']) > 5, len(d['etiquettes'])
assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
" 2>/dev/null; then
    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  else
    dit ❌ "analyser $langue : JSON invalide 
… [4225 caractères tronqués]
  ```

- **bash** `{"command": "date -Iseconds; git branch --show-current; sed -n '1,40p' docs/pilotage/en-cours.md; sed -n '1,40p' reports/rapport-performance.md 2>/dev/null", "description": "Check date, branch, state"}`

  ```
2026-11-15T23:17:44-05:00
s/v7
# En ce moment

**Mis à jour : 2026-11-15, 23 h 12 HNE (T4 : la performance ; lecture des préfixes corrigée)**

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
> le hook pre-commit refuse un fait 
… [3744 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-contrat-json.md 2>/dev/null; echo ====; sed -n '1,60p' reports/quickstart.json 2>/dev/null", "description": "Read report format examples"}`

  ```
# T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T2** (exploitable, 2/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **contrat livré et mesuré**.
>
> **Le chiffre.** Sur le gold vivant **612 phrases** : **1 883 syntagmes**, **1 883 rôles**
> non vides, **21 rôles bruts** ramenés à **8 rôles normalisés**, **0** hors table et **0**
> hors vocabulaire. Les **1 295 attachements** portent tous des `candidats` **objets**
> `{span, cible, source}` : **2 139 objets** (dont **1 062** dans `meta.alternative`),
> **0 span faux**, **1 295/1 295** cibles choisies présentes dans la liste. **Contrôle
> négatif** : un consommateur qui filtre `role == "predicat"` trouve **711** prédicats
> (**711 GV**) ; `role == "prédicat"` en trouve **0**. Le schéma v2 valide **612/612**
> annotations, les **612** v1 dérivées restent lues, et v2 refuse **612/612** v1.
>
> **Dispositif** : [`mesurer_contrat_json.py`](../tools/mesurer_contrat_json.py),
> [`roles_vocabulaire.py`](../tools/roles_vocabulaire.py),
> [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
> [`verifier_schema_produit.py`](../tools/verif
… [5415 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"code \\*\\*2\\|code 2\\|sans durée\\|duree\\|--duree\\|Codes de sortie\\|code \\*\\*3\\|code \\*\\*4\\|ce qui manque\\|Ce qui est déjà tenu\\|--fichier\" docs/produit/README.md", "description": "Locate README lines to edit"}`

  ```
223:python3 tools/drave.py analyser --fichier corpus.txt --jsonl   # une ligne JSON par phrase
224:python3 tools/drave.py analyser --fichier corpus.txt --json    # le texte entier
227:`--fichier` lit un texte UTF-8 ; `--jsonl` rend une **ligne JSON par phrase** (le format des
383:code **3**, distinct des erreurs (1) et de l'usage (2). Le message reste sur `stderr`. Un texte
439:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
463:message clair sur `stderr` et sort avec le code **4** ; rien n'est rendu sur `stdout`.
505:prototype ; `evaluer --tagger auto` rend un code **2** d'usage. Mesures réelles, cache neuf par
510:code **4** (le premier texte sans appel neuronal ne déclenche pas le 401) ; le message et le
677:| **UTF-8** | le JSON est en UTF-8, non échappé, sans durée | `--json` ; `test_produit.py` vérifie l'absence de `duree_s` |
688:**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3 / 4** :
713:python3 tools/drave.py analyser --fichier corpus.txt [--jsonl|--json] [--tagger]
716:python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
753:| `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** d
… [811 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '370,390p' docs/produit/README.md; sed -n '495,512p' docs/produit/README.md; sed -n '670,710p' docs/produit/README.md; sed -n '740,805p' docs/produit/README.md", "description": "Read exact README blocks"}`

  ```
### 3.5 Le refus, et la langue inconnue

```bash
python3 tools/drave.py analyser ""; echo "exit=$?"
```
```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=3
```

**Lecture.** Le refus est une **réponse** : le CLI écrit un **JSON d'annotation** sur `stdout`
(`refus: "vide"`, `schema: "drave.annotation"`, `version: 2`, `etiquettes: []`) et sort avec le
code **3**, distinct des erreurs (1) et de l'usage (2). Le message reste sur `stderr`. Un texte
vide n'est jamais une annotation « comme les autres ». Pour la langue, `und` est une réponse
honnête : « Élodie sourit. » rend `langue=und` (confiance 0,04 < seuil 0,12), même avec
`--langue fr` — l'indice n'est pas une contrainte. Et `--langue de` sort **2** : le CLI n'accepte
que `fr` et `en`.

### 3.6 Restituer la surface (v0)

|---|---|---:|---|---|
| **clé présente** | cascade API (si le seuil 0,60 l'appelle) | **0** | `source=cascade`, POS `neuronal` | `TAGGER API · appels=1 · réseau=1 · tokens=130 …` puis `tagger auto · API (clé présente)` |
| **clé invalide** (401/403) | **replie**, ne sort pas 4 | **0** | `source=heuristique`, `refus` non vide | `tagger auto · heuristique (repli : clé r
… [8873 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '705,740p' docs/produit/README.md", "description": "Read CLI command list"}`

  ```
Le point d'entrée existe : `tools/drave.py`, version **0.1.0**, sans dépendance externe.

```bash
python3 tools/drave.py --version
python3 tools/drave.py --aide
python3 tools/drave.py analyser "Le chat dort." [--langue fr|en] [--json] [--tagger] \
    [--partition brut|alternative|filtrer_union|filtrer] [--contexte TEXTE]
python3 tools/drave.py analyser --fichier corpus.txt [--jsonl|--json] [--tagger]
python3 tools/drave.py evaluer [--gold] [--json] [--par-langue] [--tagger]
python3 tools/drave.py rejouer "TEXTE" [--langue fr|en]
python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
python3 tools/drave.py restituer "TEXTE" --roles
python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--json]
python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles
```

`--tagger` est la **seule** option qui sort du hors ligne : elle appelle l'API DeepSeek (clé et
réseau, § 3.7). Toutes les autres lignes ci-dessus restent CPU, déterministes et sans socket.

**Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles
mesurées le 14/11) :

```
$ python3 tools/drave.py --version
drave
… [364 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,65p' tools/verifier_faq.py; sed -n '445,540p' tools/verifier_faq.py", "description": "Read FAQ verifier top/main"}`

  ```
#!/usr/bin/env python3
"""verifier_faq.py — les dix réponses de la FAQ produit, vérifiées contre le code courant.

La FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : chaque
réponse est adossée à une commande, à un chiffre de `reports/` ou à une constante du
code. Ce vérificateur exécute les dix contrôles, imprime un JSON (ou un résumé) et sort
avec le code 1 si une réponse ne tient plus.

Ce qu'il ne fait pas : aucune mesure nouvelle, aucun appel réseau, aucune clé lue. Il
rejoue le CLI en local, lit les JSON de résultats déjà publiés et inspecte le source.

Usage :
    python3 tools/verifier_faq.py            # résumé lisible
    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json

Le **contrôle négatif** est explicite : on vérifie qu'une affirmation fausse (« le CLI
accepte --langue de ») est bien rejetée par le code. Si ce contrôle passait, le
vérificateur ne prouverait rien.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
DRAVE = RACINE / "tools" / "drave.py"
DATE = "2026-11-1
… [3499 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"code 2\\|code \\*\\*2\\|code 1\\|--duree\\|durée\" docs/produit/exemples.md docs/produit/demarrage.md docs/produit/README.md | head -60", "description": "Find remaining code refs in product docs"}`

  ```
docs/produit/demarrage.md:218:**`--fichier` inexistant → code 1.**
docs/produit/README.md:368:durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
docs/produit/README.md:505:prototype ; `evaluer --tagger auto` rend un code **2** d'usage. Mesures réelles, cache neuf par
docs/produit/README.md:677:| **UTF-8** | le JSON est en UTF-8, non échappé, sans durée | `--json` ; `test_produit.py` vérifie l'absence de `duree_s` |
docs/produit/README.md:753:| `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
docs/produit/README.md:777:| **`--duree`** | pas de durée dans le JSON du CLI (le bloc l'a avec `--duree`) |
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\n# docstring exit codes\ns=s.replace(\n\"Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible\\n(absente ou refusée) · 1 erreur.\",\n\"Codes de sortie :  … [6268 caractères tronqués]`

  ```
ok
118:class ErreurEntree(RuntimeError):
525:            raise ErreurEntree(f"fichier introuvable : {args.fichier!r}", 4)
527:            raise ErreurEntree(
533:            raise ErreurEntree(
554:        sys.stdout.write(_sur(json.dumps(a.json(avec_duree=getattr(args, "duree", False)),
626:                    sys.stdout.write(_dumps(annotation.json(avec_duree=getattr(args, "duree", False))))
643:                sys.stdout.write(_dumps(annotation.json(avec_duree=getattr(args, "duree", False))))
650:        sys.stdout.write(_dumps(annotation.json(avec_duree=getattr(args, "duree", False))))
793:        return 5
945:        return 5
949:        return 5
953:        return 5
957:        return 5
962:            return 5
1004:        return 5
1168:                          help="sortie JSON complète (annotation, sans durée sauf avec --duree)")
1169:    analyser.add_argument("--duree", action="store_true",
1279:    except ErreurEntree as exc:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --json --duree | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['cout'].get('duree_s'), sorted(d['cout']))\"; echo \"code=$?\"", "description": "Test duree JSON"}`

  ```
0.00427 ['caracteres', 'duree_s', 'etiquettes', 'octets']
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser --fichier /tmp/ce-fichier-nexiste-pas-t5.txt; echo \"inexistant=$?\"; python3 tools/drave.py analyser --fichier /tmp; echo \"repertoire=$?\"; python3 tools/drave.py analyser \"Le chat dort.\" --langue  … [111 caractères tronqués]`

  ```
inexistant=4
repertoire=5
langue=5
sans=5
[stderr]
drave: dépendance absente : fichier introuvable : '/tmp/ce-fichier-nexiste-pas-t5.txt'
drave: erreur d'usage : un répertoire n'est pas un fichier : '/tmp' (--fichier attend un fichier UTF-8)
usage: drave analyser [-h] [--partition {brut,alternative,filtrer_union,filtrer}] [--fichier CHEMIN]
                      [--jsonl] [--contexte CONTEXTE] [--langue {fr,en}] [--tagger] [--json]
                      [--duree]
                      [TEXTE]
drave analyser: erreur d'usage : argument --langue: invalid choice: 'de' (choose from 'fr', 'en')
usage: drave [-h] [-V] {analyser,evaluer,rejouer,restituer} ...
drave: erreur d'usage : the following arguments are required: {analyser,evaluer,rejouer,restituer}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py --aide | tail -30; echo ====; python3 tools/drave.py analyser --aide | head -5; python3 tools/drave.py evaluer --help | head -3; python3 tools/drave.py rejouer --aide | head -3; python3 tools/drave.py restituer … [58 caractères tronqués]`

  ```
Point d'entrée produit du bloc linguistique (analyse et restitution).

arguments:
  {analyser,evaluer,rejouer,restituer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme
    restituer           reconstruire la surface depuis l'annotation et mesurer le miroir

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Commandes : analyser, evaluer, rejouer, restituer.
Codes de sortie : 0 succès · 3 refus d'analyse (JSON) · 4 clé/dépendance absente
(--tagger explicite sans clé, ou --fichier introuvable) · 5 usage (argument, sous-commande,
langue hors fr/en, --fichier sur un répertoire) · 1 autre erreur.
Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,
--contexte, --banc, --tagger [auto].
Limites : heuristique CPU, hors ligne, déterministe par défaut ; --tagger appelle l'API
DeepSeek (clé, réseau) pour le POS ; --tagger auto l'appelle seulement si une clé existe,
sinon il rend l'heuristique, sans changer le code de sortie ; la restitution
… [1418 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && printf 'Le chat dort.\\n\\nLa voisine parle.\\n' > /tmp/t5-corpus.txt && python3 tools/drave.py analyser --fichier /tmp/t5-corpus.txt --jsonl --duree | python3 -c \"import json,sys; [print(json.loads(l)['cout'].get('duree_s')) for l  … [94 caractères tronqués]`

  ```
0.004229
0.000702
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/tests/test_produit.py')\ns=p.read_text(encoding='utf-8')\nold='''    def test_codes_usage(self) -> None:\n        sans_commande = drave()\n        langue_inconnue = drave(\"analyser\", \"Le chat dort.\", \"--langue\", \"de\")\n   … [5893 caractères tronqués]`

  ```
ok
    self.assertIsNotNone(ligne, f"ligne du code {code} absente de la notice")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: unexpectedly None : ligne du code 5 absente de la notice

----------------------------------------------------------------------
Ran 30 tests in 15.863s

FAILED (failures=1)
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md')\ns=p.read_text(encoding='utf-8')\n# 1. refusal/usage code\ns=s.replace('code **3**, distinct des erreurs (1) et de l\\'usage (2).',\n            'code **3**, distinct des autres erreurs (1) et de l\\'usage (5). … [7241 caractères tronqués]`

  ```
README ok
demarrage ok
restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est
`tools/tests/test_produit.py`.

**Codes de sortie.** Le CLI implémente **0 / 1 / 3 / 4 / 5** ; le contrat est écrit dans
`--aide` et vérifié par `tools/tests/test_produit.py` :

| code | sens | aujourd'hui |
|---:|---|---|
| **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
| **3** | refus d'analyse : une **réponse**, pas une erreur | `analyser ""` (JSON de refus sur `stdout`), `restituer ""`, `rejouer ""` |
| **4** | clé/dépendance absente : clé du tagger (absente **ou refusée**) en `--tagger` explicite, ou **fichier introuvable** | `--tagger` sans clé, clé refusée HTTP 401/403, `--fichier absent.txt` : message clair, rien sur `stdout`, pas de trace |
| **5** | usage invalide : argument, sous-commande, langue hors `fr`/`en`, `--fichier` sur un **répertoire** | `argparse` et les contrôles de cohérence du CLI |
| **1** | autre erreur : divergence de rejeu, tagger qui refuse une phrase sans POS, exception inattendue | cas résiduels, jamais un refus ni un usage |

**Les deux erreurs de `--fich
… [1239 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/verifier_faq.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('assert refus.returncode == 2, refus.returncode','assert refus.returncode == 5, refus.returncode')\ns=s.replace('assert r.returncode == 2, (fantome, r.returncode)',' … [914 caractères tronqués]`

  ```
verifier_faq ok
80:    assert refus.returncode == 5, refus.returncode
112:    assert r.returncode == 0, r.stderr[-600:]
117:    assert sans_cle.returncode == 4, sans_cle.returncode
135:    assert apres["cout"]["tokens"] == 22299, apres["cout"]["tokens"]
197:    assert len(vingt["cas"]) == 26 and all(c["ok"] for c in vingt["cas"]), vingt["cas"]
202:    assert v2["properties"]["version"]["const"] == 2
221:    assert d["gold"]["phrases"] == 612 and d["gold"]["cibles_attachement"] == 239, d["gold"]
222:    assert a["cibles"] == 239 and a["labels"] == 238, a
314:    assert aide.returncode == 0
320:        assert r.returncode == 5, (fantome, r.returncode)
369:    assert version.returncode == 0 and version.stdout.strip() == "drave 0.1.0", version.stdout
375:    assert sans_site.returncode == 0, sans_site.stderr[-600:]
436:    detecte = (r.returncode == 5
FAQ produit — 10/10 réponses vérifiées · contrôle négatif détecté
  ✅  1. Quelles langues le produit reconnaît-il ?
  ✅  2. Est-ce que ça marche hors ligne ?
  ✅  3. Combien ça coûte ?
  ✅  4. Qu'est-ce que --tagger change ?
  ✅  5. Quel est le format de sortie, et est-il stable ?
  ✅  6. Que veut dire « attachement », et à quel point est
… [253 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py 2>&1 | tail -8", "description": "Run product tests"}`

  ```
..............................
----------------------------------------------------------------------
Ran 30 tests in 16.701s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_faq.py --json > reports/faq.json && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-faq.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('(code 2)','(code 5)')\ns=s.replace('code 2','code  … [254 caractères tronqués]`

  ```
rapport-faq ok
reports/rapport-faq.md:15:> contrôle négatif est explicite : le CLI **refuse** `--langue de` (code 5) et le schéma v2
reports/rapport-faq.md:56:| 1 | **Quelles langues ?** | détection `de`/`es`, `und` sous le seuil ; `--langue` limité à `fr`/`en` ; `--langue de` → code 5 ; 398 profils UDHR (0,9687) | `q1_langue` |
reports/rapport-faq.md:64:| 9 | **Les limites ?** | pas de génération, serveur, RSN, local, classement, calibration, `--langue-forcee`, garantie hors domaine ; `--sortie`/`--mode`/`--strict` → code 5 ; **pas de wheel/PyPI** | `q9_limites` |
reports/faq.json:25:     "--langue de": "code 5"
reports/faq.json:274:     "--sortie": "code 5",
reports/faq.json:275:     "--mode": "code 5",
reports/faq.json:276:     "--strict": "code 5"
reports/faq.json:343:   "le CLI accepte --langue de (il sort 5)",
reports/faq.json:347:   "--langue de": "code 5",
  ```

- **bash** `{"command": "grep -rn \"code 2\\|code \\*\\*2\\|→ code 2\\|sort 2\\|sortie 2\\|0–4\\|0 / 1 / 2\" docs/produit/ tools/drave.py tools/verifier_faq.py tools/tests/test_produit.py | head -40", "description": "Check remaining old code refs in product docs"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -rn \"0 / 1 / 2 / 3 / 4\\|0/1/2/3/4\\|code 1\\|code \\*\\*1\\|code 1.*fichier\\|--fichier.*code\" docs/produit/ | head -40", "description": "Check old file error references"}`

  ```
docs/produit/README.md:794:`--fichier`/`--jsonl`, `--duree`, `--banc`, `--partition`, le **tagger API en option** (`--tagger`, code 4,
docs/produit/README.md:925:n'existe pas : la commande échoue avec `command not found` (code **127**), pas avec une trace
docs/produit/demarrage.md:66:Si la commande n'existe pas, le venv n'est pas activé ou l'installation a échoué (code **127**).
docs/produit/demarrage.md:218:**`--fichier` inexistant → code 4.**
  ```

- **bash** `{"command": "grep -n -B3 -A2 \"return 5\" tools/drave.py", "description": "Inspect all return 5 contexts"}`

  ```
790-    if getattr(args, "tagger_auto", False):
791-        print(f"{NOM}: erreur d'usage : --tagger auto n'est disponible que pour analyser",
792-              file=sys.stderr)
793:        return 5
794-    evaluateur = _module_evaluation()
795-    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
--
942-    if args.roles_v3 and args.canonique:
943-        print(f"{NOM}: erreur d'usage : --roles-v3 et --canonique sont exclusifs",
944-              file=sys.stderr)
945:        return 5
946-    if args.roles and args.roles_v3:
947-        print(f"{NOM}: erreur d'usage : --roles (v2) et --roles-v3 sont exclusifs",
948-              file=sys.stderr)
949:        return 5
950-    if args.roles and args.canonique:
951-        print(f"{NOM}: erreur d'usage : --roles et --canonique sont exclusifs",
952-              file=sys.stderr)
953:        return 5
954-    if args.gold and not (args.banc and (args.roles or args.roles_v3)):
955-        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles ou "
956-              "--banc --roles-v3", file=sys.stderr)
957:        return 5
958-    if args.banc:
959-        if args.texte is not None or args.fichier:
9
… [578 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\nold='''    if getattr(args, \"fichier\", None):\n        chemin = pathlib.Path(args.fichier)\n        if not chemin.exists():\n            raise ErreurEntree(f\"fichier introuvable : { … [1885 caractères tronqués]`

  ```
ok
Codes de sortie : 0 succès · 3 refus d'analyse (JSON) · 4 clé/dépendance absente
(--tagger explicite sans clé, ou --fichier introuvable) · 5 usage (argument, sous-commande,
langue hors fr/en, --fichier sur un répertoire) · 1 autre erreur.
Options : --json, --jsonl, --duree, --fichier CHEMIN, --langue fr|en,
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ns=json.load(open('tools/schemas/drave-annotation-v2.json'))\nprint(json.dumps(s['properties']['cout'],ensure_ascii=False,indent=2))\nPY", "description": "Check schema cout allows duration"}`

  ```
{
  "type": "object"
}
  ```

- **bash** `{"command": "sed -n '1,80p' tools/verifier_schema_produit.py", "description": "Check schema verifier usage"}`

  ```
#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.

Deux schémas sont publiés (Draft 2020-12) :

- `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;
- `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute
  `meta.partition` et `meta.alternative`, les deux champs qui documentent les syntagmes qui se
  chevauchent, les **candidats d'attachement structurés** (`meta.attachement.candidats`,
  objets `{span, cible, source}`) et les **rôles normalisés** (vocabulaire fermé).

Le vérificateur lit `version` dans l'annotation et choisit le schéma correspondant : une
annotation v1 reste donc **lue** et validée par le schéma v1. Il compile les schémas une fois,
puis valide les annotations de cas choisis : français, anglais, refus (texte vide), entrée non
textuelle, texte très long, plus une annotation v1 de rétro-compatibilité. Il ne dépend que de
`fastjsonschema` (sinon il se rabat sur une validation minimale des champs obligatoires et de la
version). Un **contrôle négatif** vérifie que le schéma v2 refuse bien une annotation v1.

Usage :
    python3 tools/ve
… [2450 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"code\\|1 / 4\\|3 / 4\\|erreur\" docs/produit/demarrage.md | sed -n '1,80p'", "description": "Review demarrage code references"}`

  ```
66:Si la commande n'existe pas, le venv n'est pas activé ou l'installation a échoué (code **127**).
88:code Unicode, 0-based, fin exclue. `COUVERTURE` est la confiance **déclarée**, pas une précision.
189:Le mode **`auto`** est le choix sûr : l'API si une clé existe, l'heuristique sinon, **code 0**
199:## 5. Les trois erreurs courantes
201:**Texte vide → code 3.**
212:(`refus: "vide"`, `etiquettes: []`) et le code reste **3**. Même refus pour `"..."`.
214:**`--tagger` sans clé → code 4.** `stdout` vide, message `drave: dépendance absente : clé
216:l'heuristique avec le code **0**.
218:**`--fichier` inexistant → code 4.**
229:(code **5**) : `drave: erreur d'usage : un répertoire n'est pas un fichier : 'corpus/'
232:## 6. Les codes de sortie
234:| code | sens | exemple |
240:| **1** | autre erreur d'exécution | divergence de rejeu, exception inattendue |
243:le code reste **0**, et la cause est dans `refus`. Le **4** est réservé à `--tagger` explicite.
  ```

- **bash** `{"command": "sed -n '238,246p' docs/produit/demarrage.md; grep -n \"réservé au\\|4.*tagger\\|code 4\" docs/produit/README.md | head -20", "description": "Find code 4 claims"}`

  ```
| **4** | clé/dépendance absente | `--tagger` sans clé, clé refusée (HTTP 401/403), `--fichier absent.txt` |
| **5** | usage invalide | `--langue de`, `--fichier` sur un répertoire |
| **1** | autre erreur d'exécution | divergence de rejeu, exception inattendue |

Un réseau coupé ou un refus du modèle **ne sort pas 4** : la cascade replie sur l'heuristique,
le code reste **0**, et la cause est dans `refus`. Le **4** est réservé à `--tagger` explicite.

## 7. Et après

72:| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
471:| **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide | `drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.` |
497:| **clé invalide** (401/403) | **replie**, ne sort pas 4 | **0** | `source=heuristique`, `refus` non vide | `tagger auto · heuristique (repli : clé refusée (HTTP 401))` ; `TAGGER API · appels=1 · réseau=0 · tokens=0` |
558:porte qui peut sortir **4** (clé a
… [737 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/demarrage.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace(\"le code reste **0**, et la cause est dans `refus`. Le **4** est réservé à `--tagger` explicite.\",\n\"le code reste **0**, et la cause est dans `refus`. Le **4 … [295 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cat > tools/banc_cli_robuste.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"banc_cli_robuste.py — rejoue les cas de robustesse du CLI `drave` (T5).\n\nCe que le banc mesure, sans réseau et sans clé :\n\n1. `--duree` : la durée est **absente** du JSON par défaut, **présente** dans `cout.duree_ … [10136 caractères tronqués]`

  ```
CLI robuste — 20/20 cas tenus · commit 7e195ee6
✅ CLI robuste
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/banc_cli_robuste.py --json > reports/cli-robuste.json && python3 -c \"import json;d=json.load(open('reports/cli-robuste.json'));print(d['ok'], len(d['cas']));print([c['cas'] for c in d['cas']])\"", "description": "Save  … [21 caractères tronqués]`

  ```
True 20
['duree_json', 'duree_jsonl', 'aide_globale', 'analyser_aide', 'analyser_help', 'evaluer_aide', 'evaluer_help', 'rejouer_aide', 'rejouer_help', 'restituer_aide', 'restituer_help', 'fichier_inexistant', 'fichier_repertoire', 'usage_sans_commande', 'usage_langue_inconnue', 'usage_option_fantome', 'refus_texte_vide', 'refus_rejouer', 'dependance_cle_absente', 'tableau_codes_notice']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in 1 2 3; do python3 tools/drave.py analyser \"Le chat dort.\" --json --duree | python3 -c \"import json,sys;d=json.load(sys.stdin);print(d['cout']['duree_s'], len(d['etiquettes']), len(json.dumps(d,ensure_ascii=False)))\"; don … [253 caractères tronqués]`

  ```
0.005588 20 4950
0.00474 20 4949
0.004846 20 4950
====
0.005882
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py 2>&1 | tail -3; python3 tools/drave.py analyser \"\" --json >/tmp/refus.json 2>/tmp/refus.err; echo \"refus=$?\"; python3 -c \"import json;d=json.load(open('/tmp/refus.json'));print(d['refus'],d['s … [101 caractères tronqués]`

  ```
Ran 30 tests in 16.074s

OK
refus=3
vide drave.annotation 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/cli-robuste.json'))\nfor c in d['cas']:\n    print(c['cas'], c.get('code'), c.get('attendu'), c['ok'], (c.get('message') or '')[:110])\nPY", "description": "Summarize bench JSO … [3 caractères tronqués]`

  ```
duree_json None None True 
duree_jsonl 0 None True 
aide_globale 0 None True 
analyser_aide 0 None True 
analyser_help 0 None True 
evaluer_aide 0 None True 
evaluer_help 0 None True 
rejouer_aide 0 None True 
rejouer_help 0 None True 
restituer_aide 0 None True 
restituer_help 0 None True 
fichier_inexistant 4 None True drave: dépendance absente : fichier introuvable : '/tmp/drave-t5-17vwq6zy/absent.txt'
fichier_repertoire 5 None True drave: erreur d'usage : un répertoire n'est pas un fichier : '/tmp/drave-t5-17vwq6zy' (--fichier attend un fic
usage_sans_commande 5 5 True 
usage_langue_inconnue 5 5 True 
usage_option_fantome 5 5 True 
refus_texte_vide 3 3 True 
refus_rejouer 3 3 True 
dependance_cle_absente 4 4 True 
tableau_codes_notice None None True
  ```

- **bash** `{"command": "cat > reports/rapport-cli-robuste.md <<'MD'\n# T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T5** (exploitable, 5/5) ·\n> **Date** : 2026-11-15 · **Verd … [9930 caractères tronqués]`

  ```
179 reports/rapport-cli-robuste.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/banc_cli_robuste.py && python3 tools/tests/test_produit.py 2>&1 | tail -3", "description": "Re-run bench and tests"}`

  ```
CLI robuste — 20/20 cas tenus · commit 7e195ee6
✅ CLI robuste
Ran 30 tests in 16.070s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_faq.py | tail -3; python3 tools/revue_documentation.py 2>&1 | tail -30", "description": "Run FAQ and doc review"}`

  ```
✅  9. Quelles limites faut-il connaître avant de s'en servir ?
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
  revue de documentation · 764 fiche(s) · 859 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 763 fichiers, le disque en a 764
     · compteurs : en-cours.md dit 858 JSON, le disque en a 859
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"763\\|858\\|T4\\|T5\\|chantier\\|Compteurs\\|compteurs\" docs/pilotage/en-cours.md | head -60", "description": "Find counters and T4 in state"}`

  ```
3:**Mis à jour : 2026-11-15, 23 h 12 HNE (T4 : la performance ; lecture des préfixes corrigée)**
29:- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
65:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) ; **T4** : 10 000 mots **4,01 s**, contrôle **α 1,55** ; [fiche](../../reports/rapport-performance.md), [JSON](../../reports/performance.json).
66:- **Prochaine action** : **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) ; T132/T133, gold de pensée ; **T4 : borner `_groupes_partition` et `_cible_proche`** (O(k²) sur les syntagmes).
94:- **Bilans** : F1 **0,7902**, chantier **20/21** ; [semaine](../../reports/rapport-semaine.md), [bilan](../../reports/rapport-bilan-chantier.md), [clôture](../../reports/rapport-cloture-chantier.md).
104:| fichiers / JSON de résultats | **763** / **858** | `reports/*.md` / `reports/*.json` |
108:## Les chantiers et leurs bloquants
113:| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,30p' docs/pilotage/en-cours.md; sed -n '80,130p' docs/pilotage/en-cours.md; tail -60 docs/pilotage/en-cours.md", "description": "Read state sections"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 23 h 12 HNE (T4 : la performance ; lecture des préfixes corrigée)**

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
> le hook pre-commit refuse un fait sans ligne d'état ; une session
… [12717 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Current time"}`

  ```
2026-11-15 23:23 EST
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**Mis à jour : 2026-11-15, 23 h 12 HNE (T4 : la performance ; lecture des préfixes corrigée)**',\n            '**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la C … [1781 caractères tronqués]`

  ```
en-cours ok
  revue de documentation · 764 fiche(s) · 859 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-cli-robuste.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('> Commit mesuré : `7e195ee6`.','> Commit de base mesuré : `7e195ee6` ; le diff T5 est appliqué par-dessus (le hash du JSON\\n> est celui du `HEAD` au momen … [109 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -10; echo \"code=${PIPESTATUS[0]}\"", "description": "Run table gate"}`

  ```
✅ 1841 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4672 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py; echo \"en_cours=$?\"; python3 tools/verifie_journal.py 2>&1 | tail -5; echo \"journal=$?\"; python3 tools/verifier_schemas.py 2>&1 | tail -5; echo \"schemas=$?\"; python3 tools/taille_documents.py 2 … [94 caractères tronqués]`

  ```
en-cours · 1654 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
en_cours=0
  journal · 47 jour(s) · 221 session(s) · 2676 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
journal=0
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
schemas=0
  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4024 mots (AGENTS + en-cours + une tâche) > budget 4 000
taille=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | head -40", "description": "See document size details"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    8999    501   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2733    231   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [519 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,70p' docs/pilotage/en-cours.md; sed -n '88,94p' docs/pilotage/en-cours.md", "description": "Read state lines to trim"}`

  ```
- **Stratégie** : v0.
- **Ambition** : runtime tracé.
- **Objectif final** : moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) ; **T4** : 10 000 mots **4,01 s**, contrôle **α 1,55** ; [fiche](../../reports/rapport-performance.md), [JSON](../../reports/performance.json). **T5** : CLI **20/20** cas, **30 tests** ; [fiche](../../reports/rapport-cli-robuste.md), [JSON](../../reports/cli-robuste.json).
- **Prochaine action** : **T6 — le bilan de la nuit exploitable** ; **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) ; T132/T133, gold de pensée ; **T4 : borner `_groupes_partition` et `_cible_proche`** (O(k²) sur les syntagmes).
- **Bloquants** : 7B locales interdites (règle 1
… [2036 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace(' **T5** : CLI **20/20** cas, **30 tests** ; [fiche](../../reports/rapport-cli-robuste.md), [JSON](../../reports/cli-robuste.json).','')\ns=s.replace('**T5** : * … [775 caractères tronqués]`

  ```
ok
  T0 max : 3997 mots (budget 4 000)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -5; python3 tools/verifie_en_cours.py; python3 tools/taille_documents.py 2>&1 | grep \"T0 max\"", "description": "Re-run doc/state checks"}`

  ```
revue de documentation · 764 fiche(s) · 859 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  T0 max : 3997 mots (budget 4 000)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh", "description": "Run product gate", "run_in_background": true, "timeoutMs": 900000}`

  ```
started background job bash-70
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"B13\" docs/pilotage/roadmap.md | head -10", "description": "Find B13 roadmap row"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [8898 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\nold='**J9.1 passe d\\'honnêteté**'\nnew='**T5 CLI : 20/20 cas, codes 0/3/4/5, `--duree`** ([fiche](../../reports/rapport-cli-robuste.md)) ; **J9.1 passe d\\'honnêteté**'\nass … [268 caractères tronqués]`

  ```
roadmap ok
  revue de documentation · 764 fiche(s) · 859 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
    9009    501   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3997 mots (budget 4 000)
     · docs/pilotage/roadmap.md : 9009 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**T5 CLI : 20/20 cas, codes 0/3/4/5, `--duree`** ([fiche](../../reports/rapport-cli-robuste.md)) ;',\n            '**T5 CLI : 20/20, codes 0/3/4/5, `--duree`** ; … [322 caractères tronqués]`

  ```
ok
    9005    501   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3997 mots (budget 4 000)
     · docs/pilotage/roadmap.md : 9005 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\nold='**J9.1** (**19** fiches « instantané historique » : 10 encarts réécrits, 9 ajoutés ; **0 fiche de résultats** ne publie les quatre marqueurs sans mention, hors 2 faux po … [354 caractères tronqués]`

  ```
ok
    8998    501   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3997 mots (budget 4 000)
  ```

- **job_output** `{"job_id": "bash-70"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && echo ==== && git diff --stat", "description": "Review changed files"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/demarrage.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/digest.md
 M journal/sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md
 M reports/faq.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-faq.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
 M tools/tests/test_produit.py
 M tools/verifier_faq.py
?? journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c/
?? reports/cli-robuste.json
?? reports/rapport-cli-robuste.md
?? reports/rapport-s-paragraphes.md
?? tools/banc_cli_robuste.py
?? tools/tests/linguistique/gold_reel_50.py
====
 docs/pilotage/en-cours.md                          |   8 +-
 docs/pilotage/roadmap.md                           |   2 +-
 docs/produit/README.md                             |  38 +-
 docs/produit/demarr
… [1215 caractères tronqués]
  ```

- **bash** `{"command": "env | grep -i \"DSH\\|SESSION\" | head -20; ls journal/sessions | tail -5; git log --oneline -3 -- journal | cat", "description": "Find session id and journal conventions"}`

  ```
SESSION_MANAGER=local/Hauru:@/tmp/.ICE-unix/64061,unix/Hauru:/tmp/.ICE-unix/64061
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session1
DSH_PROFILE=headless
SHELL_SESSION_ID=9ccf95734de74d019d86e8774384d6fe
DSH_PROFILE_DIR=/home/stephane/.dsh/profiles/headless
DESKTOP_SESSION=plasma6
DSH_SHELL=1
XDG_SESSION_DESKTOP=KDE
XDG_SESSION_TYPE=x11
DSH_SESSION_ID=session-faf940b2-b9f9-4948-abe4-6aee0d73595c
MEMORY_PRESSURE_WATCH=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-ksmserver.service/memory.pressure
KONSOLE_DBUS_SESSION=/Sessions/5
XSESSION_IS_UP=yes
KDE_SESSION_UID=1000
XDG_SESSION_CLASS=user
KDE_SESSION_VERSION=6
XDG_SESSION_ID=4
DSH_HOME=/home/stephane/.dsh
KDE_FULL_SESSION=true
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
session-ed9b8942-25a3-48ee-9f86-f6821e56df9d
session-f198001c-49da-4e65-8a44-782f9605fd7a
session-f30f0289-2506-4596-be01-4e10f2a2073c
session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb
session-faf940b2-b9f9-4948-abe4-6aee0d73595c
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PLUS DE SYNTAGMES (1 075 CONTRE 1 006) ET VA PLUS VITE ; LE TEMPS NE SUIT PAS LES MOTS SEULS
7f0e8320 T4 — LA PERFORMANCE : 10 000 
… [307 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c -maxdepth 2 -type f -printf '%p\\n' | sort; echo ====; for f in $(find journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c -maxdepth 1 -type f); do echo \"- … [84 caractères tronqués]`
- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- journal/README.md journal/sessions/MANIFEST.md | head -80; echo ====; sed -n '1,80p' journal/README.md", "description": "Inspect journal diffs"}`

  ```
diff --git a/journal/README.md b/journal/README.md
index ef67e552..0f31f080 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -276,7 +276,7 @@ de la session ; le `digest.md` voisin en donne le verbatim complet.
 | `session-` | Restitution v3 et rôles _role_gp | 2026-11-15 11:05 | 1.0 h | 1 | 230 | 10 | 0 | [rapport](sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/rapport.md) |
 | `session-` | Vérificateur indépendant du corpus CIC | 2026-11-14 05:43 | 0.7 h | 1 | 138 | 5 | 1 | [rapport](sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/rapport.md) |
 | `session-` | Protocole d'annotation or de rôles S | 2026-11-15 12:40 | 0.2 h | 1 | 102 | 3 | 0 | [rapport](sessions/session-c6d0e659-7d2e-4d23-a2b4-d50387bb6f61/rapport.md) |
-| `session-` | Benchmark performance de l'analyseur NLP | 2026-11-15 22:35 | 0.6 h | 1 | 174 | 4 | 4 | [rapport](sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md) |
+| `session-` | Benchmark performance de l'analyseur NLP | 2026-11-15 22:35 | 0.7 h | 1 | 177 | 4 | 4 | [rapport](sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md) |
 | `session-` | Rédiger le rapport bilan du chantier | 2026-11-14 03:46 | 0.2 h | 1 
… [20660 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/2026-11-15/ && sed -n '1,80p' journal/2026-11-15/README.md", "description": "Inspect today's journal"}`

  ```
distribue.md
docs.md
memoire.md
mesures.md
modele.md
outils.md
portes.md
README.md
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**50 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 8 | [distribue.md](distribue.md) |
| docs | 14 | [docs.md](docs.md) |
| memoire | 3 | [memoire.md](memoire.md) |
| mesures | 18 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 3 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 366.5 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

… [7608 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-70"}`

  ```
✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ❌ restitution v0/v1 en échec (voir /tmp/porte-produit-restitution.log)
[status: running]
  ```

- **bash** `{"command": "tail -60 /tmp/porte-produit-restitution.log", "description": "Inspect restitution test failure"}`

  ```
test_50_textes_46_annotations (__main__.TestCinquanteTextes.test_50_textes_46_annotations) ... ok
test_stabilite_et_controles_v1 (__main__.TestCinquanteTextesV1.test_stabilite_et_controles_v1) ... ok
test_structure_v1 (__main__.TestCinquanteTextesV1.test_structure_v1) ... ok
test_synthese_v1 (__main__.TestCinquanteTextesV1.test_synthese_v1) ... ok
test_restituer_banc (__main__.TestCommande.test_restituer_banc) ... ok
test_restituer_banc_canonique (__main__.TestCommande.test_restituer_banc_canonique) ... ok
test_restituer_canonique (__main__.TestCommande.test_restituer_canonique) ... ok
test_restituer_canonique_json (__main__.TestCommande.test_restituer_canonique_json) ... ok
test_restituer_json (__main__.TestCommande.test_restituer_json) ... ok
test_restituer_multiligne (__main__.TestCommande.test_restituer_multiligne) ... ok
test_restituer_refus (__main__.TestCommande.test_restituer_refus) ... FAIL
test_restituer_texte (__main__.TestCommande.test_restituer_texte) ... ok
test_controles_negatifs (__main__.TestFormeCanonique.test_controles_negatifs) ... ok
test_distance_canonique (__main__.TestFormeCanonique.test_distance_canonique) ... ok
test_forme_simple (__main__.TestFormeCanoniq
… [1242 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"returncode.*2\\|code.*2\\|== 2\\|assertEqual.*2\" tools/tests/*.py | grep -i \"drave\\|restitu\\|produit\\|usage\\|langue\\|refus\" | head -40", "description": "Find tests expecting code 2"}`

  ```
tools/tests/test_empaquetage.py:11:- **sans installation**, `drave` échoue **proprement** : code 127, « command not found »,
tools/tests/test_produit.py:134:            self.assertEqual(len(lignes), 2, detail(sortie))
tools/tests/test_produit.py:428:        self.assertEqual(d["gold"]["phrases"], 452)
tools/tests/test_produit.py:435:        self.assertEqual(d["reel"]["phrases"], 452)
tools/tests/test_restitution.py:77:        self.assertEqual(drave("restituer").returncode, 2)
tools/tests/test_restitution.py:90:        self.assertEqual(donnees["synthese"]["annotations"], 2)
tools/tests/test_restitution.py:92:        self.assertEqual(donnees["synthese"]["surface"]["exacts"], 2)
tools/tests/test_restitution.py:109:        self.assertEqual(len(donnees["forme"]["segments"]), 2)
tools/tests/test_restitution.py:141:        self.assertEqual(len(forme["segments"]), 2)
tools/tests/test_restitution.py:165:        self.assertEqual(mesure["structure"]["cibles_resolues"], 2)
tools/tests/test_restitution.py:176:        self.assertEqual(structure["roles_retires"], 2)
tools/tests/test_restitution.py:177:        self.assertEqual(structure["cibles_retirees"], 2)
tools/tests/test_restitution.py:203:   
… [2804 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '65,85p' tools/tests/test_restitution.py; sed -n '60,80p' tools/tests/test_restitution_v2.py", "description": "Read code 2 test contexts"}`

  ```
texte = "# Notes\nLe chat dort.\nLa voisine parle.\n"
        sortie = drave("restituer", "--fichier", _fichier_temp(texte), "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["surface"]["rendu"], texte)
        self.assertTrue(donnees["surface"]["exact"])

    def test_restituer_refus(self):
        for texte in ("", "..."):
            sortie = drave("restituer", texte)
            self.assertEqual(sortie.returncode, 3, detail(sortie))
            self.assertIn("refus d'analyse", sortie.stderr)
        self.assertEqual(drave("restituer").returncode, 2)

    def test_restituer_banc(self):
        banc = {"banc_50": {"resultats": [
            {"id": "t1", "texte": "Le chat dort."},
            {"id": "t2", "texte": "The cat sleeps."},
            {"id": "t3", "texte": "..."},
        ]}}
        chemin = _fichier_temp(json.dumps(banc, ensure_ascii=False), suffixe=".json")
        self.assertEqual(donnees["version"], 1)
        self.assertEqual(donnees["roles"]["principal"]["agent"], "Le chat")
        self.assertEqual(donnees["roles"]["principal"]["predicat"], "dort")
        self.as
… [872 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"returncode, 2\\|returncode == 2\\|returncode ==2\\|code=2\\|code == 2\" tools/ --include=*.py | head -40", "description": "Find all code 2 test expectations"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/network/auth.py:150:            res.returncode == 2
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/network/lazy_wheel.py:59:        assert head.status_code == 200
tools/docwatch/.venv/lib/python3.13/site-packages/jaraco/context/__init__.py:394:    >>> on_interrupt('error', code=255)(do_interrupt)()
tools/docwatch/.venv/lib/python3.13/site-packages/jaraco/functools/__init__.py:716:    ...     dict(msg='smile!', code=20),
tools/docwatch/.venv/lib/python3.13/site-packages/twine/repository.py:216:            if response.status_code == 200:
tools/tests/test_restitution.py:77:        self.assertEqual(drave("restituer").returncode, 2)
tools/tests/test_restitution_v2.py:70:        self.assertEqual(sortie.returncode, 2, detail(sortie))
tools/tests/test_restitution_v2.py:76:        self.assertEqual(sortie.returncode, 2, detail(sortie))
tools/tests/test_restitution_v3.py:333:        self.assertEqual(sortie.returncode, 2, detail(sortie))
tools/tests/test_restitution_v3.py:336:        self.assertEqual(sortie.returncode, 2, detail(sortie))
tools/tests/test_restitution_v3.py:341:        self.assertEqual(sortie.return
… [125 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '325,345p' tools/tests/test_restitution_v3.py; sed -n '720,735p' tools/tests/test_tagger_api.py", "description": "Read more code 2 contexts"}`

  ```
self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["schema"], "drave.restitution.v2.banc")
        self.assertEqual(d["synthese"]["cadre"]["exacts"], 19)
        self.assertEqual(d["synthese"]["roles"]["f1"], 0.5270)

    def test_exclusifs(self):
        sortie = drave("restituer", "Le chat dort.", "--roles", "--roles-v3")
        self.assertEqual(sortie.returncode, 2, detail(sortie))
        self.assertIn("exclusifs", sortie.stderr)
        sortie = drave("restituer", "Le chat dort.", "--roles-v3", "--canonique")
        self.assertEqual(sortie.returncode, 2, detail(sortie))
        self.assertIn("exclusifs", sortie.stderr)

    def test_gold_avec_roles_v3(self):
        sortie = drave("restituer", "Le chat dort.", "--roles-v3", "--gold", str(GOLD))
        self.assertEqual(sortie.returncode, 2, detail(sortie))
        self.assertIn("--banc", sortie.stderr)


if __name__ == "__main__":
            defaut = drave_cli("analyser", TEXTE, "--json", env=env)
            auto = drave_cli("analyser", "--tagger", "auto", TEXTE, "--json", env=env)
        self.assertEqual(auto.returncode, 0, auto.stderr)
        self.ass
… [587 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\nfor f in ('tools/tests/test_restitution.py','tools/tests/test_restitution_v2.py','tools/tests/test_restitution_v3.py','tools/tests/test_tagger_api.py'):\n    p=Path(f); s=p.read_text(encodi … [252 caractères tronqués]`

  ```
tools/tests/test_restitution.py 1
tools/tests/test_restitution_v2.py 2
tools/tests/test_restitution_v3.py 3
tools/tests/test_tagger_api.py 1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_restitution.py 2>&1 | tail -3; python3 tools/tests/test_restitution_v2.py 2>&1 | tail -3; python3 tools/tests/test_restitution_v3.py 2>&1 | tail -3", "description": "Run restitution tests"}`

  ```
Ran 22 tests in 16.628s

OK
Ran 17 tests in 1.439s

OK
Ran 29 tests in 2.578s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -5", "description": "Run tagger API tests"}`

  ```
----------------------------------------------------------------------
Ran 30 tests in 7.085s

OK
  ```

- **job_output** `{"job_id": "bash-70"}`

  ```
❌ restitution v2 en échec (voir /tmp/porte-produit-restitution-v2.log)
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '\"code\": 2\\|code 2\\|code=2\\|sort 2\\|code \\*\\*2' reports/ docs/ tools/ --include=*.md --include=*.json --include=*.py --include=*.sh 2>/dev/null | grep -v \"docs/archive\\|tools/docwatch\\|reports/archive\" | head -40 … [65 caractères tronqués]`

  ```
reports/campagne-benefices/038-35-decouverte-le-registre-des-regions-c11.md:25:| région **absente** du registre | refus en la nommant, **code 2**, rien n'est calculé |
reports/campagne-benefices/042-39-audit-des-drapeaux-par-chemin-une-method.md:86:  des trois réglages est donné, le moteur **s'arrête en expliquant** (code 2, aucune perplexité).
reports/campagne-benefices/050-47-attn-sinks-le-drapeau-vit-mais-seulement.md:9:**refus** (`code 2`) allait être livré sur cette base. Il a été écrit, vérifié… puis **retiré
reports/rapport-c8-peripherie.md:24:| **canal** `--entree-canal K`, **gain** `--entree-gain X`, **jeton de base** `--entree-jeton N` | ✅ | refus (code 2) si le canal ou le jeton sort du modèle |
reports/rapport-c2-recurrence.md:28:- **bornée** : α hors de [0, 8] est **refusé** (code 2) — une récurrence qui ne converge pas ne doit
reports/rapport-passe-complete-13-octobre.md:41:`porte-greffe`, `porte-indice`, `porte-melange` et `porte-topologie` sortaient **« code 2 »** —
reports/rapport-passe-complete-13-octobre.md:76:2. **`code 2` ne doit pas ressembler à un succès** : la passe affiche la marque, mais un `code 2`
reports/rapport-tableaux-casses.md:27:« une porte qui ren
… [3291 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-70"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/drave.py | sed -n '1,240p'", "description": "Review drave.py diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index d38f59ae..755ec247 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -32,8 +32,8 @@ et la ligne `TAGGER API` porte le coût de l'appel quand il a eu lieu. Le mode `
 Ce que la commande n'expose pas : le neuronal local (`llama-cli` ou endpoint), la traduction et la
 génération : ils demandent des poids, un service ou un GPU.
 
-Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
-(absente ou refusée) · 1 erreur.
+Codes de sortie : 0 succès · 3 refus d'analyse · 4 clé/dépendance absente
+(ou fichier introuvable) · 5 usage · 1 autre erreur.
 """
 from __future__ import annotations
 
@@ -115,6 +115,19 @@ class CleTaggerRefusee(RuntimeError):
         )
 
 
+class ErreurEntree(RuntimeError):
+    """L'entrée `--fichier` n'est pas lisible : le code dit pourquoi (4 ou 5), sans trace.
+
+    Un chemin **inexistant** est une dépendance absente (4) ; un **répertoire** est un
+    usage invalide de `--fichier` (5). Dans les deux cas, le message nomme le chemin et
+    rien ne part sur `stdout`.
+    """
+
+    def __init__(self, message: str, code: int) -> None:
+        self.code = int(code)
+        super()
… [9280 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('a.json(avec_duree=getattr(args, \"duree\", False)),\\n                                            ensure_ascii=False)',\n            'a.json(avec_duree=args.duree), ensure … [669 caractères tronqués]`

  ```
ok
Ran 30 tests in 15.963s

OK
  ```

- **job_output** `{"job_id": "bash-70"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sort \\*\\*2\\*\\*\\|sort 2\\|code \\*\\*2\\*\\*\\|code 2\" docs/produit/ | head -20", "description": "Find lingering code 2 in product docs"}`

  ```
docs/produit/README.md:819:une contrainte ; `--langue de` sort **2** (usage invalide). Les 398 profils ne sont pas
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md'); s=p.read_text(encoding='utf-8')\ns=s.replace('`--langue de` sort **2** (usage invalide).','`--langue de` sort **5** (usage invalide).')\np.write_text(s,enc … [163 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/banc_cli_robuste.py --json > reports/cli-robuste.json && python3 tools/banc_cli_robuste.py && python3 tools/verifier_faq.py --json > reports/faq.json && python3 tools/verifier_faq.py | tail -2", "description": "Regenera … [23 caractères tronqués]`

  ```
CLI robuste — 20/20 cas tenus · commit 7e195ee6
✅ CLI robuste
[still running after 60000ms; moved to background job bash-93]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 👤 Utilisateur

background job bash-70 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh) finished [status: completed, exit code: 1]. Read its output with job_output.

- **job_output** `{"job_id": "bash-70"}`

  ```
✅ autotest parallèle : 183/183 portes tenues
❌ porte produit rouge
[status: completed, exit code: 1]
  ```

- **job_output** `{"job_id": "bash-93"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-cli-robuste.md'); s=p.read_text(encoding='utf-8')\ns=s.replace('| `tools/tests/test_produit.py` | 6 tests T5 : durée JSON/JSONL, tableau, aide/help × 4, fichier inexistant, répertoire |',\n            '| `tools/tests/te … [332 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"rejouer.*returncode\\|returncode.*rejouer\\|rejouer.*code\" tools/tests tools/verifier_faq.py tools/porte-produit.sh | head -20", "description": "Check rejouer refusal tests"}`

  ```
tools/tests/documents/corpus/technique/lecteur-controleur.md:4:> choisit, ce qu'il paie, et ce qui permet de rejouer sa trajectoire. Le code est
  ```

- **job_output** `{"job_id": "bash-93"}`

  ```
✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-93 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/banc_cli_robuste.py --json > reports/cli-robuste.json && python3 tools/banc_cli_robuste.py && python3 tools/verifier_faq.py --json > reports/faq.json && python3 tools/verifier_faq.py | tail -2) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh", "description": "Re-run product gate after fixes", "run_in_background": true, "timeoutMs": 900000}`

  ```
started background job bash-96
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/produit/README.md docs/produit/demarrage.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md | sed -n '1,260p'", "description": "Review docs diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index aa1ec05e..1a689e20 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 23 h 12 HNE (T4 : la performance ; lecture des préfixes corrigée)**
+**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -63,7 +63,7 @@
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
 - **Ce que font les autres** : **N2**, **S**, **hub**.
 - **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) ; **T4** : 10 000 mots **4,01 s**, contrôle **α 1,55** ; [fiche](../../reports/rapport-performance.md), [JSON](../..
… [22100 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-96"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -4; bash tools/porte-tableaux.sh 2>&1 | tail -4; python3 tools/taille_documents.py 2>&1 | grep \"T0 max\\|roadmap.md\"", "description": "Final doc checks"}`

  ```
revue de documentation · 764 fiche(s) · 859 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ 1841 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4672 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
    8998    501   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3997 mots (budget 4 000)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md docs/produit/demarrage.md reports/faq.json reports/rapport-faq.md tools/drave.py tools/tests/test_produit.py tools/tests/test_restitution.p … [187 caractères tronqués]`

  ```
check=0
  ```

- **job_output** `{"job_id": "bash-96", "wait": true, "timeout_ms": 300000}`

  ```
✅ smoke test : Ran 30 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-* | sed 's#.*/##' | grep -i \"produit\\|cli\\|lang\\|tagger\\|resti\"", "description": "List relevant gates"}`

  ```
porte-melange.sh
porte-produit.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 7e195ee6 | head -40; echo ====; git show --stat --oneline 7f1519f7 | head -40", "description": "Check recent commit file sets"}`

  ```
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PLUS DE SYNTAGMES (1 075 CONTRE 1 006) ET VA PLUS VITE ; LE TEMPS NE SUIT PAS LES MOTS SEULS
 docs/pilotage/en-cours.md                          |   2 +-
 journal/2026-11-15/README.md                       |   5 +-
 journal/2026-11-15/mesures.md                      |   4 +-
 journal/README.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   2 +-
 .../digest.md                                      | 146 +++++++++++++++++++++
 .../rapport.md                                     |  26 +++-
 reports/rapport-performance.md                     |  11 +-
 8 files changed, 180 insertions(+), 18 deletions(-)
====
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
 .gitignore                                         |    3 +
 docs/pilotage/en-cours.md                          |    8 +-
 docs/produit/README.md                             |  131 +-
 docs/produit/exemples.md                           |    8 +-
 journal/2026-11-15/README.md                       | 
… [2134 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/session_report.py --help 2>&1 | head -30; echo ====; python3 tools/journal_auto.py --help 2>&1 | head -30", "description": "Check journal generators usage"}`

  ```
usage: session_report.py [-h] [--repo REPO] [--session SESSION] [--quiet]

options:
  -h, --help         show this help message and exit
  --repo REPO
  --session SESSION
  --quiet
====
usage: journal_auto.py [-h] [--jour JOUR] [--depuis DEPUIS] [--lister]
                       [--dry-run] [--quiet]

options:
  -h, --help       show this help message and exit
  --jour JOUR      AAAA-MM-JJ (défaut : aujourd'hui)
  --depuis DEPUIS  générer chaque jour depuis cette date
  --lister         montrer les thèmes et leurs mots-clés
  --dry-run
  --quiet
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/session_report.py --session session-faf940b2-b9f9-4948-abe4-6aee0d73595c --quiet; echo \"code=$?\"; sed -n '1,45p' journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c/rapport.md", "description": "Regenerate ou … [18 caractères tronqués]`

  ```
code=0
# Session session- — Robustesse de la CLI

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-faf940b2-b9f9-4948-abe4-6aee0d73595c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 23:16 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 95 |
| Appels d'outils | 113 |
| Fichiers touchés | 0 |
| Commandes | 103 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche T5 (exploitable, 5/5) : la **robustesse de la CLI** — (1) `--duree` dans le JSON (le temps de l'analyse) ; (2) le **tableau des codes de sortie** (0 succès, 3 refus, 4 clé/dépendance, 5 usage) dans `docs/produit/README.md` et le `--aide` ; (3) `--aide`/`--help` vérifiés sur les quatre sous-commandes ; (4) un `--fichier` sur un chemin **inexistant** et un **répertoire** : le message et le cod … [124 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche T5 (exploitable, 5/5) : la **robustesse de la CLI** — (1) `--duree` dans le JSON (le temps de l'analyse) ; (2
… [579 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- journal/README.md journal/sessions/MANIFEST.md | sed -n '1,80p'; git status --short | grep journal", "description": "Check journal diffs after regen"}`

  ```
diff --git a/journal/README.md b/journal/README.md
index ef67e552..0f31f080 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -276,7 +276,7 @@ de la session ; le `digest.md` voisin en donne le verbatim complet.
 | `session-` | Restitution v3 et rôles _role_gp | 2026-11-15 11:05 | 1.0 h | 1 | 230 | 10 | 0 | [rapport](sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/rapport.md) |
 | `session-` | Vérificateur indépendant du corpus CIC | 2026-11-14 05:43 | 0.7 h | 1 | 138 | 5 | 1 | [rapport](sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/rapport.md) |
 | `session-` | Protocole d'annotation or de rôles S | 2026-11-15 12:40 | 0.2 h | 1 | 102 | 3 | 0 | [rapport](sessions/session-c6d0e659-7d2e-4d23-a2b4-d50387bb6f61/rapport.md) |
-| `session-` | Benchmark performance de l'analyseur NLP | 2026-11-15 22:35 | 0.6 h | 1 | 174 | 4 | 4 | [rapport](sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md) |
+| `session-` | Benchmark performance de l'analyseur NLP | 2026-11-15 22:35 | 0.7 h | 1 | 177 | 4 | 4 | [rapport](sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md) |
 | `session-` | Rédiger le rapport bilan du chantier | 2026-11-14 03:46 | 0.2 h | 1 
… [2844 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add \\\n  docs/pilotage/en-cours.md \\\n  docs/pilotage/roadmap.md \\\n  docs/produit/README.md \\\n  docs/produit/demarrage.md \\\n  reports/faq.json \\\n  reports/rapport-faq.md \\\n  reports/cli-robuste.json \\\n  reports/rapp … [364 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
M  docs/produit/demarrage.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/digest.md
 M journal/sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md
A  reports/cli-robuste.json
M  reports/faq.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
A  reports/rapport-cli-robuste.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
M  reports/rapport-faq.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
A  tools/banc_cli_robuste.py
 M tools/chantier/plan.json
M  tools/drave.py
M  tools/tests/test_produit.py
M  tools/tests/test_restitution.py
M  tools/tests/test_restitution_v2.py
M  tools/tests/test_restitution_v3.py
M  tools/tests/test_tagger_api.py
M  tools/verifier_faq.py
?? journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c/
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS\"", "description": "Commit T5 changes"}`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-106]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-106", "wait": true, "timeout_ms": 300000}`

  ```
[s/v7 9a291c8b] T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
 32 files changed, 3446 insertions(+), 100 deletions(-)
 create mode 100644 journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c/digest.md
 create mode 100644 journal/sessions/session-faf940b2-b9f9-4948-abe4-6aee0d73595c/rapport.md
 create mode 100644 reports/cli-robuste.json
 create mode 100644 reports/rapport-cli-robuste.md
 create mode 100755 tools/banc_cli_robuste.py
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | sed -n '1,80p'; echo ====; git status --short | sed -n '1,40p'", "description": "Inspect commit contents and status"}`

  ```
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
 docs/pilotage/en-cours.md                          |    8 +-
 docs/pilotage/roadmap.md                           |    2 +-
 docs/produit/README.md                             |   40 +-
 docs/produit/demarrage.md                          |   19 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    5 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   14 +
 .../rapport.md                                     |    8 +-
 .../digest.md                                      |  102 +
 .
… [1407 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -12 journal/2026-11-15/README.md; grep -n \"T5\" journal/2026-11-15/README.md | tail -3; git log --oneline -2", "description": "Check day journal includes T5"}`

  ```
### T3 — le démarrage en 5 minutes : rejoué sur un clone public

Le quickstart [`docs/produit/demarrage.md`](../../docs/produit/demarrage.md) part d'un clone
public neuf, installe dans `.venv` et lance trois commandes ; **3/3** sortent **0**, le JSON
fait **5 899 octets** en schéma **v2**, `--tagger` sans clé sort **4**, `auto` sort **0**, et
les trois erreurs sortent **3 / 4 / 1**. Le contrôle négatif « débutant sans le dépôt » passe,
mais découvre que `tools/structures` (URL locale dans `.gitmodules`) manque à un clone public :
`analyser` rend `objet` / `—` au lieu de `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %**
au lieu de **79,02 %** / **99,58 %**. Le document affiche la sortie réelle du clone et nomme
l'écart ; la correction du sous-module reste à faire.
[`fiche`](../../reports/rapport-quickstart.md) · [`JSON`](../../reports/quickstart.json).
<!-- /notes -->
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PLUS DE SYNTAGMES (1 075 CONTRE 1 006) ET VA PLUS VITE ; LE TEMPS NE SUIT PAS LES MOTS SEULS
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -4; python3 tools/verifie_en_cours.py; python3 tools/verifie_journal.py 2>&1 | tail -4; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|roadmap.md :\"", "description": "Post- … [25 caractères tronqués]`

  ```
revue de documentation · 764 fiche(s) · 859 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  journal · 47 jour(s) · 221 session(s) · 2676 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  T0 max : 3997 mots (budget 4 000)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -4; python3 tools/verifier_schemas.py 2>&1 | tail -3", "description": "Post-commit tables/schemas checks"}`

  ```
✅ 1841 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4672 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

### 🤖 Assistant

T5 est livré, mesuré, testé et committé.

## Ce qui a été fait

1. **`--duree`** — ajouté à `analyser` pour `--json` et `--jsonl` : `cout.duree_s` (4,7–5,9 ms sur les phrases de test). Absent par défaut, donc le déterminisme de `--json` / `rejouer` est conservé. La durée est le **seul** ajout (texte et étiquettes identiques).

2. **Codes de sortie** — contrat passé à **0 succès / 3 refus / 4 clé ou dépendance / 5 usage / 1 autre erreur** :
   - `2` → `5` pour tous les usages (`argparse`, langue inconnue, options exclusives) ;
   - `--fichier` inexistant → **4** (`dépendance absente : fichier introuvable`) ;
   - `--fichier` sur un répertoire → **5** (`erreur d'usage : un répertoire n'est pas un fichier`) ;
   - refus de `rejouer` → **3** au lieu de 1 ;
   - tableau écrit dans `docs/produit/README.md` **et** dans `--aide`.

3. **`--aide` / `--help`** — les 8 combinaisons sur les 4 sous-commandes sortent **0** et affichent leur usage.

4. **Fixtures** — `reports/rapport-cli-robuste.md`, `reports/cli-robuste.json`, banc reproductible `tools/banc_cli_robuste.py` : **20/20 cas**. Tests ajoutés dans `tools/tests/test_produit.py` (durée JSON/JSONL, tableau, aide/help, fichier inexistant, répertoire) ; les attentes des autres tests CLI ont été alignées sur le nouveau code 5.

## Vérifications

- `python3 tools/tests/test_produit.py` → **30 tests OK**
- `python3 tools/banc_cli_robuste.py` → **20/20 cas**
- `bash tools/porte-produit.sh` → **✅ porte produit verte** (autotest 183/183)
- `revue_documentation.py`, `porte-tableaux.sh`, `verifie_en_cours.py`, `verifie_journal.py`, `verifier_schemas.py`, `taille_documents.py` → verts
- Commit : **`9a291c8b`** — `T5 — LA CLI ROBUSTE : --DUREE …, CODES 0/3/4/5 …, AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`

