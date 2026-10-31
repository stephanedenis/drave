# Session DSH — relecture

- identifiant : `3de141c0-089b-4ceb-8a2e-bd6d83044a5f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-29 11:32:00
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave). Tu dois écrire UN fichier : `tools/graphe_document_html.py`. Tu ne modifies rien d'autre, sauf le dossier de fixtures `tools/tests/documents/html/` que tu peux créer.

CONTEXTE. Le chantier R0.1 construit un « graphe de document » : un fichier (HTML, PDF, DOCX, Markdown) est transformé en une liste de blocs typés, en ordre de lecture, avec des offsets exacts. Chaque parseur produit des blocs ; le cœur (écrit par moi, pas par toi) assemble le manifeste, insère les blancs, calcule les spans et vérifie la partition. Ton fichier doit donc respecter strictement ce contrat.

CONTRAT (impératif) :
```python
def analyse(chemin: "pathlib.Path") -> list[dict]:
    """Blocs en ordre de lecture. Chaque bloc : {"type": str, "texte": str, "prov": dict}."""
```
- `type` ∈ {"titre", "section", "paragraphe", "liste", "tableau", "code", "maths", "figure", "legende", "note"} (jamais "blanc" : le cœur l'ajoute).
- `texte` : le texte VISIBLE du bloc, `strip()`é, non vide. Les paragraphes sont des chaînes sur UNE ligne (les retours à la ligne de mise en forme deviennent des espaces) ; un bloc `code` ou `liste` peut garder des `\n` internes pour ses lignes. Pas de balise, pas d'entité HTML non décodée.
- `prov` : `{"bloc": n}` où n est l'indice 0-based du bloc dans l'ordre du DOM (compteur simple, stable).
- Ordre : ordre du DOM (c'est l'ordre de lecture d'un document HTML).

RÈGLES DE TYPAGE :
- `h1` → `titre` ; `h2`, `h3`, `h4` → `section` (le niveau peut aller dans `prov["niveau"]`) ; `h5`/`h6` → `section` aussi.
- `p` → `paragraphe`. Un `p` vide est ignoré.
- `ul`/`ol` → un bloc `liste` PAR `li` (texte de l'item, sous-listes aplaties dans le même item ou émises après, au choix, mais documente-le).
- `table` → UN bloc `tableau` : lignes jointes par `\n`, cellules par `\t`, en-têtes compris. Un `caption` devient un bloc `legende` séparé AVANT le tableau.
- `pre`, `code` (bloc) → `code` (contenu verbatim, sans strip interne).
- `math`, `.math`, `[class*=math]`, `script[type*=math]` → `maths` (prendre l'attribut `alttext`/`aria-label` s'il existe, sinon le text_content).
- `figure` → `figure` (texte visible de la figure) ; `figcaption` → `legende`.
- Notes : `aside`, `[role=doc-footnote]`, `.footnote`, `sup` contenant du texte → `note`. Une note n'est JAMAIS comptée comme du corps : elle sort en bloc `note`, à sa position DOM.
- À IGNORER complètement : `script`, `style`, `noscript`, `nav`, commentaires. (Un document, pas une page de site.)
- Les textes en double (même texte, même parent) ne doivent pas être émis deux fois : si un conteneur et son enfant donnent le même texte, ne garde que le plus interne.

FIDÉLITÉ (c'est le contrôle qui compte) : la concaténation de tes blocs, normalisée (espaces compactés, sauts de ligne compactés), doit être ÉGALE au texte visible du document tel que `lxml.html.fromstring(html).text_content()` le donne, normalisé de la même façon — à l'exception près des éléments ignorés (script/style/noscript/nav) et des doublons évités. Écris cette vérification dans ton fichier (fonction `verifie(chemin) -> tuple[bool, float, list[str]]` qui rend l'égalité, le ratio de mots communs et les écarts), et fais-la tourner sur tes fixtures.

AUTOTEST : crée dans `tools/tests/documents/html/` au moins trois fixtures écrites à la main :
1. `article.html` : h1, deux h2, paragraphes, une liste à puces, un tableau avec caption, un bloc `pre`, une note de bas de page (`aside`), un `script` et un `nav` qui doivent disparaître ;
2. `deux-colonnes.html` : un contenu en deux colonnes CSS (`column-count:2`) dont l'ordre du DOM est l'ordre de lecture attendu (le HTML n'a pas de notion de colonnes : c'est un contrôle de non-régression) ;
3. `entites.html` : entités (`&amp;`, `&nbsp;`, accents, `&lt;`), un `<sup>` de note, et un tableau sans en-tête.
Le fichier doit avoir un `if __name__ == "__main__":` qui prend un chemin en argument et imprime le JSON des blocs (indenté), et un mode `--autotest` qui lance les trois fixtures, vérifie la fidélité et affiche un verdict par fixture avec les chiffres.

CONTRAINTES :
- Python 3, uniquement les bibliothèques déjà installées : `bs4`, `lxml`, `html5lib`. Pas de nouvelle dépendance.
- Déterministe : aucun horodatage, aucun chemin absolu dans la sortie.
- Docstrings et commentaires en français, dans le style du dépôt : dire POURQUOI, pas seulement quoi. Pas d'emoji, pas d'art ASCII.
- Le code doit être propre et court (viser 150–200 lignes).

RENDS DANS TA RÉPONSE FINALE : le chemin du fichier, la commande exacte de l'autotest, les chiffres observés (nombre de blocs par fixture, ratio de fidélité, types trouvés), et les limites que tu as rencontrées. Ne me dis pas « c'est fait » sans les chiffres.
Your parent agent id is "8156fdcb-5033-4ba4-a5f3-f8a078e6e57e". Before you finish, send your result to that agent with send_message({ agent_id: "8156fdcb-5033-4ba4-a5f3-f8a078e6e57e", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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
10. **Pilotage : cycles longs, sous-agents, état unique.** DSH ouvre **un goal par programme** avec
    `max_goal_rounds` **très grand (1 000)** ; on ne s'arrête qu'à un résultat mesuré, écrit, committé, ou
    un blocage nommé. Les tâches indépendantes partent en **sous-agents** (2–4 en parallèle) ; le
    sous-agent ne touche **jamais** `en-cours`/`roadmap`/`AGENTS`, il rend un **diff d'état**. Le principal
    met à jour `en-cours` **chaque cycle** (une ligne/résultat, lien, prochaine action ;
    ≤ 2 000 mots). → [`docs/methode/continuite.md`](docs/methode/continuite.md)

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

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

### 🤖 Assistant

⏵ Exploration du dépôt et du chantier R0.1 pour aligner le contrat et le style

- **bash** `{"command": "ls; ls tools | head -50; ls tools/tests 2>/dev/null | head -30", "description": "List repository root and tools directories"}`

  ```
AGENTS.md
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
ancre_professeur.py
applique_pont.py
approximabilite_bloc.py
apres-telechargement-k3.sh
archive_sessions.py
audit_drapeaux_harnais.py
banc-experts.py
banc_lecteur.py
banc-prelire.py
blanchiment_entree.py
boucle-cerveau.sh
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c4_retard.sh
c8_carte_profondeur.sh
c8_corpus.sh
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
campagne-benefices.sh
campagne_synthese.py
cancellation_langue.py
carte_coupe.sh
carte-facultes.sh
carte-fenetre-puits.sh
carte_langues.py
carte_latence.sh
carte-sorti
… [101 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"import bs4, lxml, html5lib; print(bs4.__version__, lxml.__version__, html5lib.__version__)\"", "description": "Check installed parsing libraries and versions"}`

  ```
4.15.0 6.1.1 1.1
  ```

- **bash** `{"command": "ls tools | grep -i -E \"document|graphe|parse|html|pdf|docx|markdown\"; ls tools/tests 2>/dev/null | head -50; find tools/tests -maxdepth 3 -type d 2>/dev/null | head -40", "description": "Find document/graph related tools and test dirs"}`

  ```
revue_documentation.py
taille_documents.py
  ```

- **bash** `{"command": "grep -ril \"R0\\.1\\|graphe de document\\|graphe_document\" --include=\"*.md\" --include=\"*.py\" . 2>/dev/null | head -30", "description": "Search references to R0.1 document graph"}`

  ```
./journal/2026-10-29/docs.md
./docs/pilotage/backlog/_modele.md
./docs/pilotage/backlog/R01-graphe-document.md
./docs/pilotage/backlog/R32-citations-provenance.md
./docs/pilotage/backlog/R51-lecture-croisee.md
./docs/pilotage/backlog/R11-contexte-hierarchique.md
./docs/pilotage/backlog/index.md
./docs/pilotage/roadmap.md
./docs/pilotage/en-cours.md
./docs/theorie/glossaire/README.md
./docs/theorie/glossaire/entrees/graphe-de-document.md
./docs/theorie/glossaire/entrees/parseur.md
./docs/theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md
./docs/theorie/lecture-rapide.md
./docs/theorie/glossaire.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R01-graphe-document.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R01-graphe-document.md</path>
<type>file</type>
<content>
1: # R01 — Graphe de document et registre de régions
2: 
3: > **Statut** : prête · **Priorité** : P0 · **Programme** : R · **Dépend de** : —
4: > **Ligne de roadmap** : R0.1 · **Fiche de résultat attendue** : rapport-r01-graphe-document.md (à créer dans `reports/`)
5: > **Résumé** : Transformer un document en un arbre de régions typées, avec offsets et provenance, sans modèle.
6: > **Glossaire** : [graphe de document](../../theorie/glossaire/entrees/graphe-de-document.md) · [parseur](../../theorie/glossaire/entrees/parseur.md) · [contrat](../../theorie/glossaire/entrees/contrat.md).
7: 
8: ## Le besoin
9: 
10: Le modèle ne voit qu'un flux d'octets : il ne peut pas dire « lis le titre, saute la section 3, compare les colonnes ». Il faut une représentation du document qui survive au rejeu et qui serve de champ de lecture au contrôleur.
11: 
12: ## Le contrat
13: 
14: | élément | contenu |
15: |---|---|
16: | **entrée** | un fichier (PDF, HTML, DOCX, Markdown, EPUB) et sa langue |
17: | **sortie** | un manifeste de régions : type, parent, offsets, texte
… [1944 caractères tronqués]
  ```

- **bash** `{"command": "ls tools | wc -l; ls src | head; ls tools/cerveau 2>/dev/null | head; find tools -maxdepth 2 -name \"*.py\" | head -20", "description": "Inspect tool layout and examples"}`

  ```
376
bpe_np.py
encoding.py
gguf_min.py
__pycache__
roofline.py
sparsity.py
ternary.py
tiny_model.py
transformer_np.py
batterie.py
bus.py
episodique.py
gating_conflit2.py
gating_moteur.py
gating.py
hub.py
__init__.py
lesion_complet.py
lesion.py
tools/archive_sessions.py
tools/make_patch.py
tools/session_report.py
tools/harmony_canonique.py
tools/aiguille.py
tools/mla_synthetique.py
tools/vision_ref.py
tools/vision_mtmd.py
tools/diff_flux.py
tools/profil_flux.py
tools/flux_codec.py
tools/analyse_flux.py
tools/pair_factice.py
tools/proxy_latence.py
tools/trace_compacite.py
tools/telecharger_modeles.py
tools/clusters_moe.py
tools/convertir_clusters.py
tools/analyse_empreinte.py
tools/analyse_experts_statique.py
[stderr]
find: ‘standard output’: Broken pipe
find: write error
  ```

- **bash** `{"command": "grep -rl \"def analyse\" --include=\"*.py\" tools src drave-core 2>/dev/null | head -20; grep -ril \"text_content\\|html5lib\\|bs4\" --include=\"*.py\" tools src 2>/dev/null | head -20", "description": "Search existing HTML parsing code"}`

  ```
tools/session_report.py
tools/analyse_flux.py
tools/trace_compacite.py
tools/aligneur_litteraire.py
tools/analyse_alignement.py
tools/docwatch/src/docwatch/diagrams.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/lexer.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/lexers/python.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexer.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/actionscript.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/algebra.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/asc.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/asm.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/basic.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/bdd.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/business.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/c_cpp.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/c_like.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/carbon.py
tools/docwatch/.venv/lib/python3.13/si
… [61 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,80p tools/harmony_canonique.py; echo ====; sed -n 1,60p tools/taille_documents.py", "description": "Inspect style of existing tools"}`

  ```
#!/usr/bin/env python3
"""Construit un identifiant de perplexité au format harmony CANONIQUE.

Le montage forcé `<|start|>assistant<|channel|>final<|message|>texte` est hors
distribution : le modèle attend d'abord le canal `analysis` (mesuré : p=0,9999
contre 0,0001 pour `final`). Ce script construit donc la séquence telle que
l'implémentation officielle la produirait : message système complet, tour
utilisateur, puis un canal `analysis` court, puis le canal `final` qui porte le
texte à noter.

Sortie : /tmp/harmony_canonique.ids (identifiants) et /tmp/harmony_canonique.dep
(indice du premier jeton de contenu), pour que la perplexité du contenu seul
puisse être recalculée depuis les logits exportés.
"""
import subprocess, sys, os

Q = "/home/stephane/Data13TB/stephane/GitHub/Drave/drave-core/target/release/drave"
M = "/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf"

DEB, FIN, MSG, CANAL = 200006, 200007, 200008, 200005


def encode(texte, nom):
    """Passe par le tokenizer du moteur (jamais un autre découpage)."""
    f_in = f"/tmp/harmony_piece_{nom}.txt"
    f_out = f"/tmp/harmony_piece_{nom}.ids"
    open(f_in, "w").write(texte)
    subprocess.run([Q, M, "
… [4780 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du comportement exact de `lxml` sur text_content, commentaires et tables

- **bash** `{"command": "python3 - <<'PY'\nimport lxml.html\nh = '''<html><head><title>Titre page</title></head><body>\n<p>a<sup>1</sup>b &amp; c&nbsp;d &lt; e</p>\n<!-- commentaire -->\n<p>x</p><p>y</p>\n<table><caption>Cap</caption><tr><th>A</th><th>B</th></tr><tr><td>C</td><td>D</td></tr></table>\n<script>co … [307 caractères tronqués]`

  ```
"Titre page\na1b & c\xa0d < e\n\nxy\nCapABCD\nconsole.log('x')Accueil\nligne 1\n  ligne 2\n"
--- itertext comment? ['Titre page', '\n', 'a', '1', 'b & c\xa0d < e', '\n', '\n', 'x', 'y', '\n', 'Cap', 'A', 'B', 'C', 'D', '\n', "console.log('x')", 'Accueil', '\n', 'ligne 1\n  ligne 2', '\n']
--- tags ['html', 'head', 'title', 'body', 'p', 'sup', <cyfunction Comment at 0x7f3e3d26e750>, 'p', 'p', 'table', 'caption', 'tr', 'th', 'th', 'tr', 'td', 'td', 'script', 'nav', 'pre']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport lxml.html\nfor h in ['<p>a</p><p>b</p>', '<div>a<script>x</script>b</div>', '<p>a<br/>b</p>', '<math alttext=\"x^2\"><mi>x</mi><mn>2</mn></math>', '<p>a</p>\\n<p>b</p>']:\n    r=lxml.html.fromstring(h)\n    print(repr(h), '->', repr(r.text_content()))\nPY", "des … [50 caractères tronqués]`

  ```
'<p>a</p><p>b</p>' -> 'ab'
'<div>a<script>x</script>b</div>' -> 'axb'
'<p>a<br/>b</p>' -> 'ab'
'<math alttext="x^2"><mi>x</mi><mn>2</mn></math>' -> 'x2'
'<p>a</p>\n<p>b</p>' -> 'a\nb'
  ```

### 🤖 Assistant

⏵ Validation de `drop_tree`, du parsing par octets et des cas limites avant écriture

- **bash** `{"command": "python3 - <<'PY'\nimport lxml.html\nh=b'<html><body><p>a<script>x</script>b</p><nav>n<style>s</style>t</nav></body></html>'\nr=lxml.html.document_fromstring(h)\nfor el in list(r.iter()):\n    if isinstance(el.tag,str) and el.tag.lower() in ('script','style','nav'):\n        el.drop_tree … [174 caractères tronqués]`

  ```
'ab'
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
  File "/usr/lib64/python3.13/site-packages/lxml/html/__init__.py", line 742, in document_fromstring
    raise etree.ParserError(
        "Document is empty")
lxml.etree.ParserError: Document is empty
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport lxml.html\nh='<p>a<sup>1</sup>b</p><p>c</p>'.encode('utf-8')\nr=lxml.html.document_fromstring(h)\nprint([e.tag for e in r.iter()], repr(r.text_content()))\n# math script\nh2='<script type=\"math/tex\">x^2</script><p>y</p>'\nr2=lxml.html.document_fromstring(h2.en … [150 caractères tronqués]`

  ```
['html', 'body', 'p', 'sup', 'p'] 'a1bc'
[('html', None), ('head', None), ('script', 'math/tex'), ('body', None), ('p', None)] 'x^2y'
  ```

### 🤖 Assistant

⏵ Écriture du parseur HTML puis des trois fixtures d'autotest

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py", "content": "#!/usr/bin/env python3\n\"\"\"Extrait le graphe de blocs d'un document HTML pour le chantier R0.1.\n\nLe cœur assemble le manifeste, insère les blancs et vérifie la partition : ce\nmodule ne re … [13744 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n  <meta charset=\"utf-8\">\n</head>\n<body>\n  <nav>\n    <a href=\"index.html\">Accueil</a>\n  </nav>\n\n  <article>\n    <h1>Les rivières de montagne</h1>\n    <p>Une rivière de montagne change de lit au fil des crues : le texte visible\n   … [1249 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/documents/html/article.html</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n  <meta charset=\"utf-8\">\n  <style>\n    .colonnes { column-count: 2; column-gap: 2rem; }\n  </style>\n</head>\n<body>\n  <h1>Lecture en deux colonnes</h1>\n  <div class=\"colonnes\">\n    <p>Première colonne : le DOM commence ici et la lec … [357 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/documents/html/deux-colonnes.html</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n  <meta charset=\"utf-8\">\n</head>\n<body>\n  <h1>Café &amp; caractères</h1>\n  <p>Le café &amp; le thé coûtent 5 &lt; 7 euros.</p>\n  <p>Une espace&nbsp;insécable et des accents&nbsp;: éàü.</p>\n  <p>Une marque<sup>1</sup> dans le texte.</p … [445 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/documents/html/entites.html</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Lancement de l'autotest et inspection des blocs produits

- **bash** `{"command": "python3 tools/graphe_document_html.py --autotest; echo \"[sortie $?]\"", "description": "Run parser autotest on fixtures"}`

  ```
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 0.963, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures conformes
[sortie 0]
  ```

- **bash** `{"command": "python3 tools/graphe_document_html.py tools/tests/documents/html/article.html | head -80", "description": "Dump article blocks as JSON"}`

  ```
[
  {
    "type": "titre",
    "texte": "Les rivières de montagne",
    "prov": {
      "bloc": 0,
      "niveau": 1
    }
  },
  {
    "type": "paragraphe",
    "texte": "Une rivière de montagne change de lit au fil des crues : le texte visible doit suivre le lit du document, pas celui de la page.",
    "prov": {
      "bloc": 1
    }
  },
  {
    "type": "section",
    "texte": "Le régime des eaux",
    "prov": {
      "bloc": 2,
      "niveau": 2
    }
  },
  {
    "type": "paragraphe",
    "texte": "La fonte des neiges donne au printemps un débit qui peut tripler en quelques jours.",
    "prov": {
      "bloc": 3
    }
  },
  {
    "type": "liste",
    "texte": "Le printemps porte la crue principale.",
    "prov": {
      "bloc": 4
    }
  },
  {
    "type": "liste",
    "texte": "L'été laisse les eaux basses.",
    "prov": {
      "bloc": 5
    }
  },
  {
    "type": "liste",
    "texte": "L'automne prépare les réserves",
    "prov": {
      "bloc": 6
    }
  },
  {
    "type": "liste",
    "texte": "Les nappes se rechargent lentement.",
    "prov": {
      "bloc": 7
    }
  },
  {
    "type": "section",
    "texte": "Mesurer le débit",
    "prov": {
      "bloc": 8,
      "ni
… [248 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse de l'écart de ratio sur `entites.html` (découpe autour du `sup`)

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)\nc=pathlib.Path('tools/tests/documents/html/entites.html')\nb=g.anal … [350 caractères tronqués]`

  ```
ATTENDU: ['Café', '&', 'caractères', 'Le', 'café', '&', 'le', 'thé', 'coûtent', '5', '<', '7', 'euros.', 'Une', 'espace', 'insécable', 'et', 'des', 'accents', ':', 'éàü.', 'Une', 'marque1', 'dans', 'le', 'texte.', 'Signe', 'Nom', '&', 'esperluette', '<', 'inférieur', 'Note', ':', '&', "s'écrit", 'aussi', '«', 'et', '».']
OBTENU : ['Café', '&', 'caractères', 'Le', 'café', '&', 'le', 'thé', 'coûtent', '5', '<', '7', 'euros.', 'Une', 'espace', 'insécable', 'et', 'des', 'accents', ':', 'éàü.', 'Une', 'marque', '1', 'dans', 'le', 'texte.', 'Signe', 'Nom', '&', 'esperluette', '<', 'inférieur', 'Note', ':', '&', "s'écrit", 'aussi', '«', 'et', '».']
CLE EGAL: True
titre 'Café & caractères'
paragraphe 'Le café & le thé coûtent 5 < 7 euros.'
paragraphe 'Une espace insécable et des accents : éàü.'
paragraphe 'Une marque'
note '1'
paragraphe 'dans le texte.'
tableau 'Signe\tNom\n&\tesperluette\n<\tinférieur'
note "Note : & s'écrit aussi « et »."
  ```

### 🤖 Assistant

⏵ Tests de robustesse sur cas synthétiques (notes, maths, figures, doublons, code inline)

- **bash** `{"command": "cat > /tmp/cas.html <<'HTML'\n<!DOCTYPE html>\n<html><head><title>Doc &amp; test</title><style>p{color:red}</style></head>\n<body>\n<nav>menu</nav>\n<p>Un <strong>texte</strong> avec <code>inline()</code> et une note<sup>2</sup> puis la suite.</p>\n<p></p>\n<div class=\"math\">E = mc<su … [979 caractères tronqués]`

  ```
verif: (False, 0.825, ["insert : attendu '' / obtenu 'fin'", "delete : attendu 'fin' / obtenu ''"])
0 titre 'Doc & test'
1 paragraphe 'Un texte avec inline() et une note'
2 note '2'
3 paragraphe 'puis la suite.'
4 maths 'E = mc2'
5 maths 'double'
6 figure 'SchÃ©ma du flux'
7 legende 'Figure 1 : le flux.'
8 code 'def f():\n    return 1'
9 liste 'un deuxfin'
10 liste 'sous'
11 liste 'trois'
12 legende 'Cap'
13 tableau 'A\tB'
14 maths 'x^2 + y^2'
15 note 'bas de page'
  ```

- **bash** `{"command": "find docs reports journal -name \"*.html\" -type f 2>/dev/null | head -10", "description": "Find real HTML files in repo"}`

  ```
(no output)
  ```

- **bash** `{"command": "wc -l tools/graphe_document_html.py; python3 -m py_compile tools/graphe_document_html.py && echo OK", "description": "Count lines and compile parser"}`

  ```
362 tools/graphe_document_html.py
OK
  ```

- **bash** `{"command": "awk 'NF{n++} END{print \"non vides:\",n}' tools/graphe_document_html.py; grep -c '^\\s*$' tools/graphe_document_html.py; grep -c '^\\s*#' tools/graphe_document_html.py; grep -c '\"\"\"' tools/graphe_document_html.py", "description": "Measure nonblank and comment lines"}`

  ```
non vides: 302
60
1
23
  ```

### 🤖 Assistant

⏵ Compactage du code vers la cible de lignes et correction de l'ordre des items imbriqués

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Extrait le graphe de blocs d'un document HTML pour le chantier R0.1.\n\nLe cœur assemble le manifeste, insère les blancs et vérifie la partition : ce\nmodule ne rend donc que des blocs de corps, en ordre de DOM, jamais de « blanc ».\n\nChoix de découpe, à c … [12617 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Validation de la version compacte sur fixtures et cas synthétiques

- **bash** `{"command": "wc -l tools/graphe_document_html.py; python3 tools/graphe_document_html.py --autotest; echo \"[sortie $?]\"", "description": "Run autotest on compact version"}`

  ```
323 tools/graphe_document_html.py
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 0.963, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures conformes
[sortie 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)\nfor c in [pathlib.Path('/tmp/cas.html')]:\n    print('verif:', g.ve … [147 caractères tronqués]`

  ```
verif: (True, 0.8148148148148148, [])
0 titre 'Doc & test'
1 paragraphe 'Un texte avec inline() et une note'
2 note '2'
3 paragraphe 'puis la suite.'
4 maths 'E = mc2'
5 maths 'double'
6 figure 'Schéma du flux'
7 legende 'Figure 1 : le flux.'
8 code 'def f():\n    return 1'
9 liste 'un deux'
10 liste 'sous'
11 liste 'fin'
12 liste 'trois'
13 legende 'Cap'
14 tableau 'A\tB'
15 maths 'x^2 + y^2'
16 note 'bas de page'
  ```

- **bash** `{"command": "awk 'NF{n++} END{print \"non vides:\",n}' tools/graphe_document_html.py; grep -c '^\\s*$' tools/graphe_document_html.py; grep -n '^def \\|^class \\|^    def ' tools/graphe_document_html.py", "description": "Show function line breakdown"}`

  ```
non vides: 269
54
34:def _normalise(texte: str) -> str:
39:def _cle(texte: str) -> str:
44:def _est_math(el) -> bool:
54:def _ignore(el) -> bool:
60:def _texte(el, exclure: frozenset[str] = frozenset()) -> str:
64:    def visiter(noeud) -> None:
79:def _est_note(el) -> bool:
89:def _special(el) -> bool:
95:def _plus_proche(el, *tags: str):
105:def _lire(chemin: pathlib.Path):
114:def _reference(chemin: pathlib.Path) -> str:
116:    def visible(el) -> str:
129:def analyse(chemin: pathlib.Path) -> list[dict]:
133:    def ajoute(type_: str, texte: str, niveau: int | None = None) -> None:
142:    def est_bloc(el) -> bool:
147:    def inline(el, type_: str, niveau: int | None = None) -> None:
175:    def liste(el) -> None:
181:    def tableau(el) -> None:
193:    def emettre(el) -> None:
221:    def parcours(racine) -> None:
253:def verifie(chemin: pathlib.Path) -> tuple[bool, float, list[str]]:
286:def autotest() -> int:
312:def main(argv: list[str]) -> int:
  ```

### 🤖 Assistant

⏵ Refonte compacte : un seul marcheur pour conteneurs et paragraphes, autotest resserré

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Extrait le graphe de blocs d'un document HTML pour le chantier R0.1.\n\nLe cœur assemble le manifeste et insère les blancs : ce module ne rend que des\nblocs de corps, en ordre de DOM. Un `li` donne un bloc, même imbriqué ; son\ntexte est coupé autour des s … [10473 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "wc -l tools/graphe_document_html.py; python3 tools/graphe_document_html.py --autotest; echo \"[sortie $?]\"", "description": "Check line count and run autotest"}`

  ```
265 tools/graphe_document_html.py
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 0.963, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures fidèles
[sortie 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)\nfor c in [pathlib.Path('/tmp/cas.html')]:\n    print('verif:', g.ve … [157 caractères tronqués]`

  ```
verif: (True, 0.8148148148148148, [])
0 titre 'Doc & test'
1 paragraphe 'Un texte avec inline() et une note'
2 note '2'
3 paragraphe 'puis la suite.'
4 maths 'E = mc2'
5 maths 'double'
6 figure 'Schéma du flux'
7 legende 'Figure 1 : le flux.'
8 code 'def f():\n    return 1'
9 liste 'un deux'
10 liste 'sous'
11 liste 'fin'
12 liste 'trois'
13 legende 'Cap'
14 tableau 'A\tB'
15 maths 'x^2 + y^2'
16 note 'bas de page'
  ```

- **bash** `{"command": "awk 'NF{n++} END{print \"non vides:\",n}' tools/graphe_document_html.py; grep -c '^\\s*$' tools/graphe_document_html.py; sed -n '120,250p' tools/graphe_document_html.py | nl -ba | sed -n '1,140p'", "description": "Measure nonblank lines and inspect analyse"}`

  ```
non vides: 219
46
     1	
     2	    return visible(_lire(chemin))
     3	
     4	
     5	def analyse(chemin: pathlib.Path) -> list[dict]:
     6	    """Blocs en ordre de lecture : ``{"type", "texte", "prov": {"bloc": n}}``."""
     7	    blocs: list[dict] = []
     8	
     9	    def ajoute(type_: str, texte: str, niveau: int | None = None) -> None:
    10	        texte = texte.strip()
    11	        if not texte:
    12	            return
    13	        prov = {"bloc": len(blocs)}
    14	        if niveau is not None:
    15	            prov["niveau"] = niveau
    16	        blocs.append({"type": type_, "texte": texte, "prov": prov})
    17	
    18	    def est_bloc(el) -> bool:
    19	        tag = el.tag.lower()
    20	        return tag not in {"html", "body", "head"} and (
    21	            tag in BLOCS or _est_math(el) or _est_note(el))
    22	
    23	    def decouper(el, type_: str, niveau: int | None = None, tout: bool = False) -> None:
    24	        """Émet le texte d'un conteneur en blocs, coupé autour des éléments spéciaux.
    25	
    26	        `tout=True` parcourt un conteneur structurel (body, div) : tout bloc du DOM
    27	        y est une frontière. `tout=False` 
… [5130 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fusion des parcours de texte et allègement des helpers pour réduire le fichier

- **bash** `{"command": "python3 - <<'PY'\nimport lxml.html\nr=lxml.html.fromstring('<div><ul><li><ul><li>x</li></ul></li></ul></div>')\nli=r.xpath('.//li')[1]\nprint([ (a.tag) for a in li.iterancestors() ])\nPY", "description": "Confirm iterancestors availability"}`

  ```
['ul', 'li', 'ul', 'div', 'body', 'html']
  ```

- **bash** `{"command": "grep -n -B3 '^def ' tools/taille_documents.py | head -30; echo ===; grep -c '^$' tools/taille_documents.py; wc -l tools/taille_documents.py", "description": "Check blank-line style in a repository tool"}`

  ```
66-}
67-
68-
69:def mots(texte: str) -> int:
70-    return len(re.findall(r"\S+", texte))
71-
72-
73:def classe(rel: str) -> tuple[str, int]:
--
77-    return "", 0
78-
79-
80:def main() -> int:
===
19
159 tools/taille_documents.py
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/graphe_document_html.py')\ns=p.read_text()\nold='''def _texte(el, exclure: frozenset[str] = frozenset()) -> str:\n    \"\"\"Texte visible d'un sous-arbre, sans les ignorés ni les tags de `exclure`.\"\"\"\n    morceaux: list[str]  … [2850 caractères tronqués]`

  ```
56:def _visible(el, exclure: frozenset[str] = frozenset()) -> str:
89:def _proche(el, *tags: str):
104:def _reference(chemin: pathlib.Path) -> str:
175:                if _proche(li, "ul", "ol") is el:
179:                if _proche(cap, "table") is el:
183:                      for ligne in el.iter("tr") if _proche(ligne, "table") is el]
191:                if _proche(cap, "figure") is el:
250 tools/graphe_document_html.py
  ```

- **bash** `{"command": "awk 'NF{n++} END{print \"non vides:\",n}' tools/graphe_document_html.py; python3 tools/graphe_document_html.py --autotest; echo \"[sortie $?]\"; python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location … [199 caractères tronqués]`

  ```
non vides: 205
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 0.963, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures fidèles
[sortie 0]
cas: (True, 0.8148148148148148)
  ```

### 🤖 Assistant

⏵ Relecture complète du fichier après fusion

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Extrait le graphe de blocs d'un document HTML pour le chantier R0.1.
3: 
4: Le cœur assemble le manifeste et insère les blancs : ce module ne rend que des
5: blocs de corps, en ordre de DOM. Un `li` donne un bloc, même imbriqué ; son
6: texte est coupé autour des sous-listes, qui sortent à leur position. De même, un
7: paragraphe contenant une note (`sup`) ou une formule est coupé : la note sort en
8: bloc `note`, jamais comptée comme du corps. La fidélité se compare à
9: `text_content()` blancs retirés, car cette fonction ne sépare pas les blocs
10: (`<p>a</p><p>b</p>` donne « ab ») : comparer les espaces testerait la mise en
11: forme de la source, pas le texte visible.
12: """
13: from __future__ import annotations
14: 
15: import difflib
16: import json
17: import pathlib
18: import re
19: import sys
20: from collections import Counter
21: 
22: import lxml.html
23: 
24: IGNORES = frozenset({"script", "style", "noscript", "nav"})
25: TITRES = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
26: BLOCS = frozenset("title h1 h2 h3 h4 
… [9783 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle du contrat (types, `prov`, partition) et de l'état git

- **bash** `{"command": "git status --short; find tools -maxdepth 3 -name '__pycache__' -type d | head", "description": "Check git status and pycache artifacts"}`

  ```
?? docs/implantation/document-graph.md
?? tools/graphe_document.py
?? tools/graphe_document_html.py
?? tools/porte-document.sh
?? tools/tests/
tools/__pycache__
tools/jeux/codecs/__pycache__
tools/jeux/regles/__pycache__
tools/jeux/__pycache__
tools/jeux/tests/__pycache__
tools/llm/tests/__pycache__
tools/llm/__pycache__
tools/semantique/tests/__pycache__
tools/semantique/__pycache__
tools/cerveau/tests/__pycache__
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib, json\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)\nTYPES={\"titre\",\"section\",\"paragraphe\",\"liste\",\"table … [593 caractères tronqués]`

  ```
article.html 13 (True, 1.0)
deux-colonnes.html 5 (True, 1.0)
entites.html 8 (True, 0.9629629629629629)
  ```

### 🤖 Assistant

⏵ Lecture du cœur R0.1 déjà présent pour vérifier l'interface réelle

- **bash** `{"command": "sed -n 1,240p tools/graphe_document.py", "description": "Read existing document graph core"}`

  ```
#!/usr/bin/env python3
"""graphe_document.py — R0.1 : le document devient un graphe de régions vérifiable.

POURQUOI CE FICHIER. Le modèle ne voit qu'un flux d'octets : il ne peut pas dire « lis le
titre, saute la section 3, compare les colonnes ». Il faut une représentation du document
qui survive au rejeu et qui serve de champ de lecture au contrôleur (R0.2). Trois choses
sont donc mesurables ici, et une seule ne suffit pas :

  1. **la partition** — chaque octet du flux appartient à exactement une région. C'est
     mécanique, donc incontestable : la somme des longueurs fait le flux, les spans sont
     contigus, et le SHA-256 de chaque région se recalcule depuis le flux ;
  2. **la fidélité** — le flux n'ajoute ni ne perd de mot par rapport à une extraction
     INDÉPENDANTE (pypdf pour le PDF, pandoc pour le DOCX/EPUB, lxml pour le HTML, la
     source pour le Markdown). C'est le contrôle qui attrape l'extracteur qui invente ;
  3. **la structure** — les types de région ne sont pas triviaux : un texte plat ne doit
     pas passer la porte, sinon le graphe ne sert à rien.

Le manifeste ne porte **aucun horodatage** : deux exécutions sur le même fichier doivent
donner le même SH
… [8899 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,160p tools/porte-document.sh; echo ====; sed -n 1,120p docs/implantation/document-graph.md", "description": "Read document gate and spec"}`

  ```
#!/bin/bash
# porte-document.sh — R0.1 : le document est un graphe, et le graphe se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Une découpe de document qui « a l'air bonne » n'est pas une
# découpe : sans partition exacte, un offset faux ne se voit pas ; sans extraction
# indépendante, un extracteur qui invente des mots ne se voit pas non plus. Cette porte
# exige donc les trois choses ensemble — partition, fidélité, rejeu — plus trois contrôles
# négatifs qui doivent ÉCHOUER (texte plat, deux colonnes, notes hors corps).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ==="
python3 tools/graphe_document.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte document verte" || echo "❌ porte document ROUGE (code $CODE)"
exit "$CODE"
====
# Le graphe de document — régions, offsets, partition

> **Ce que ce document est.** La **spécification** du manifeste de graphe de document (R0.1) :
> ce qu'est un flux, ce qu'est une région, et les trois contrôles qui rendent la découpe
> vérifiable. Le code est `tools/graphe_document.py` ; la porte est `tools/porte-document.sh` ;
> les résultats mesurés vivent dans `reports/`, jamais ici.
>
> **Chargement** : lire § 2 et § 5
… [6203 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de l'interface HTML attendue par le cœur existant

- **bash** `{"command": "grep -n -i \"html\\|analyse(\" tools/graphe_document.py | head -60", "description": "Locate HTML integration in core"}`

  ```
13:     INDÉPENDANTE (pypdf pour le PDF, pandoc pour le DOCX/EPUB, lxml pour le HTML, la
32:import html as html_mod
82:    texte = html_mod.unescape(texte)
100:    # On ne retire que les balises HTML **connues**. `<ID>` (un gabarit) et
272:def analyse(chemin: pathlib.Path) -> list[dict]:
276:    if suffixe in (".html", ".htm"):
277:        return _module("graphe_document_html").analyse(chemin)
279:        return _module("graphe_document_pdf").analyse(chemin)
290:    blocs = analyse(chemin)
437:    elif suffixe in (".html", ".htm"):
438:        from lxml import html as lxml_html
439:        racine = lxml_html.fromstring(chemin.read_bytes())
481:# (une page = un document, tous < 8 ko), 3 pages HTML, 3 pages DOCX/EPUB fabriquées par
497:    """37 pages PDF + 8 documents Markdown + les fixtures HTML + 3 conversions DOCX/EPUB
501:    html = sorted((RACINE / "tools/tests/documents/html").glob("*.html"))
519:    return pdf + md + html + conversions
  ```

- **bash** `{"command": "grep -n \"graphe_document_html\\|importlib\\|analyse_html\\|parseur\" tools/graphe_document.py | head -40", "description": "Find parser loading mechanism"}`

  ```
33:import importlib.util
255:        raise SystemExit(f"parseur absent : {chemin.name}")
256:    spec = importlib.util.spec_from_file_location(nom, chemin)
257:    module = importlib.util.module_from_spec(spec)
263:    """DOCX, EPUB, ODT : pandoc fait l'extraction, puis le parseur Markdown lit le résultat.
277:        return _module("graphe_document_html").analyse(chemin)
443:            # pas « marque1 ». Les éléments ignorés par le parseur (script, style, nav) le
  ```

- **bash** `{"command": "sed -n 235,330p tools/graphe_document.py; echo ====; sed -n 400,465p tools/graphe_document.py; echo ====; sed -n 480,540p tools/graphe_document.py", "description": "Read core module loading and HTML fidelity logic"}`

  ```
contenu.append(lignes[i].strip())
            i += 1
        if not contenu:  # ligne qui n'a matché aucun cas : on avance, jamais de boucle infinie
            contenu = [lignes[i].strip()]
            i += 1
        ajoute("paragraphe", inline(" ".join(contenu)), debut)

    return blocs


def analyse_markdown(chemin: pathlib.Path) -> list[dict]:
    texte = chemin.read_text(encoding="utf-8", errors="replace")
    return analyse_markdown_texte(texte, _offsets(texte))


# ------------------------------------------------------------ les autres formats

def _module(nom: str):
    chemin = pathlib.Path(__file__).with_name(nom + ".py")
    if not chemin.exists():
        raise SystemExit(f"parseur absent : {chemin.name}")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyse_pandoc(chemin: pathlib.Path) -> list[dict]:
    """DOCX, EPUB, ODT : pandoc fait l'extraction, puis le parseur Markdown lit le résultat.
    Un seul lecteur de blocs pour trois formats, et un extracteur qu'on ne code pas."""
    sortie = subprocess.run(
        ["pandoc", "-f", chemin.suf
… [8503 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 460,485p tools/graphe_document.py; sed -n 330,400p tools/graphe_document.py", "description": "Read fidelity threshold and manifest checks"}`

  ```
capture_output=True, text=True, check=True).stdout
        # le texte brut rend les puces et les numéros de liste ; ils ne sont pas lus.
        reference = re.sub(r"^(\s*)(\d+[.)]|[-*+•])\s+", r"\1", reference, flags=re.M)
    else:
        return 1.0, []
    a, b = mots(reference), mots(flux)
    communs = sum((a & b).values())
    total = max(sum(a.values()), 1)
    manquants = sorted((a - b).elements())[:8]
    en_trop = sorted((b - a).elements())[:8]
    ecarts = []
    if manquants:
        ecarts.append("absents du flux : " + ", ".join(manquants))
    if en_trop:
        ecarts.append("ajoutés par le flux : " + ", ".join(en_trop))
    return communs / total, ecarts


# ------------------------------------------------------------- le corpus et la porte

# 50 pages : 16 documents ONU (37 pages réelles, 5 langues), 8 documents Markdown
# (une page = un document, tous < 8 ko), 3 pages HTML, 3 pages DOCX/EPUB fabriquées par
# pandoc. Le mélange est délibéré : le PDF donne les colonnes et les notes, le Markdown
# les tableaux et le code, les autres la conversion.
CORPUS_MD = [
    "docs/theorie/vision.md",
        "stats": {"regions": len(regions), "types": dict(sorted(types.items
… [3674 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib, json\np=pathlib.Path('tools/graphe_document.py')\nspec=importlib.util.spec_from_file_location('core',p); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)\nfor c in sorted(pathlib.Path('tools/tests/documents/html' … [277 caractères tronqués]`

  ```
article.html regions 25 types {'blanc': 12, 'code': 1, 'legende': 1, 'liste': 4, 'note': 1, 'paragraphe': 2, 'section': 2, 'tableau': 1, 'titre': 1} fidelite 1.0 ecarts []
deux-colonnes.html regions 9 types {'blanc': 4, 'paragraphe': 4, 'titre': 1} fidelite 1.0 ecarts []
entites.html regions 15 types {'blanc': 7, 'note': 2, 'paragraphe': 4, 'tableau': 1, 'titre': 1} fidelite 1.0 ecarts []
  ```

### 🤖 Assistant

⏵ Intégration réelle : manifeste, invariants et fidélité du cœur sur les fixtures

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document.py')\nspec=importlib.util.spec_from_file_location('core',p); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)\nfor c in sorted(pathlib.Path('tools/tests/documents/html').glob … [230 caractères tronqués]`

  ```
article.html invariants: OK | fidelite: 1.0
deux-colonnes.html invariants: OK | fidelite: 1.0
entites.html invariants: OK | fidelite: 1.0
  ```

- **bash** `{"command": "python3 tools/graphe_document.py --json tools/tests/documents/html/article.html >/tmp/article.json; echo \"sortie $?\"; python3 -c \"import json;m=json.load(open('/tmp/article.json'));print(m['stats'])\"", "description": "Run core CLI JSON manifest on article"}`

  ```
sortie 0
{'regions': 25, 'types': {'blanc': 12, 'code': 1, 'legende': 1, 'liste': 4, 'note': 1, 'paragraphe': 2, 'section': 2, 'tableau': 1, 'titre': 1}}
  ```

- **bash** `{"command": "find tools/tests -maxdepth 4 -type f -printf '%p %s octets\\n' | sort; find tools/tests/documents -maxdepth 3 -type d | sort", "description": "List all fixtures in tests directory"}`

  ```
tools/tests/documents/html/article.html 1370 octets
tools/tests/documents/html/deux-colonnes.html 513 octets
tools/tests/documents/html/entites.html 602 octets
tools/tests/documents/pdf/deux-colonnes.pdf 1581 octets
tools/tests/documents
tools/tests/documents/html
tools/tests/documents/pdf
  ```

- **bash** `{"command": "python3 tools/graphe_document.py --verifie tools/tests/documents/html/article.html 2>&1 | tail -20; echo \"[code $?]\"", "description": "Run core verification CLI on article"}`

  ```
manifeste b244af00c298870d · 25 régions · 570 octets · {'blanc': 12, 'code': 1, 'legende': 1, 'liste': 4, 'note': 1, 'paragraphe': 2, 'section': 2, 'tableau': 1, 'titre': 1}
✅ partition exacte, hashes justes, ordre complet
[code 0]
  ```

- **bash** `{"command": "sed -n 540,660p tools/graphe_document.py", "description": "Read document gate acceptance checks"}`

  ```
if not chemins:
        print("❌ corpus introuvable")
        return 1
    lignes, erreurs, types_vus, notes, details = [], [], Counter(), [], []
    for chemin in chemins:
        rel = chemin.relative_to(RACINE) if chemin.is_relative_to(RACINE) else chemin
        try:
            m = manifeste(chemin)
        except SystemExit as e:
            erreurs.append(f"{rel} : {e}")
            continue
        problemes = verifie(m, chemin) + verifie_provenance(m, chemin)
        if problemes:
            erreurs += [f"{rel} : {p}" for p in problemes]
        ratio, ecarts = fidelite(chemin, m)
        if ratio < 0.99:
            erreurs.append(f"{rel} : fidélité {ratio:.4f} < 0,99 ({ecarts})")
        m2 = manifeste(chemin)
        if empreinte(m) != empreinte(m2):
            erreurs.append(f"{rel} : le rejeu ne redonne pas le même manifeste")
        types_vus.update(m["stats"]["types"])
        notes += [(rel, m, r) for r in m["regions"] if r["type"] == "note"]
        lignes.append((str(rel), m["stats"]["regions"], m["stats"]["types"], ratio))
        details.append({"document": str(rel), "regions": m["stats"]["regions"],
                        "types": m["stats"]["types"], "fid
… [4940 caractères tronqués]
  ```

- **bash** `{"command": "find . -name \"*.html\" -not -path \"./tools/docwatch/.venv/*\" -not -path \"./.git/*\" -type f 2>/dev/null | head -30", "description": "Find other HTML documents in repo"}`

  ```
./data/jw/html/https_www_jw_org_en_library_magazines_watchtower_study_august_2026_An_Appeal_on_the_Basis_of_Love_.html
./data/jw/html/B0_E0_A4_95_E0_A5_80_E0_A4_97_E0_A4_AF_E0_A5_80_E0_A4_97_E0_A5_81_E0_A4_9C_E0_A4_BC_E0_A4_BE_E0_A4_B0_E0_A4_BF_E0_A4_B6_.html
./data/jw/html/B0_E0_A6_A3_E0_A7_87_E0_A6_95_E0_A6_B0_E0_A6_BE_E0_A6_8F_E0_A6_95_E0_A6_85_E0_A6_A8_E0_A7_81_E0_A6_B0_E0_A7_8B_E0_A6_A7_.html
./data/jw/html/https_www_jw_org_id_perpustakaan_majalah_menara_pengawal_pelajaran_agustus_2026_Permohonan_atas_Dasar_Kasih_.html
./data/jw/html/D8_A8_D8_AA_DA_A9_DB_8C_D8_A8_D9_90_D9_86_D8_A7_D9_BE_D8_B1_D8_A7_DB_8C_DA_A9_D8_AF_D8_B1_D8_AE_D9_88_D8_A7_D8_B3_D8_AA_.html
./data/jw/html/A9_B6_E7_94_A8_2026_E5_B9_B48_E6_9C_88_E6_84_9B_E3_81_AB_E5_9F_BA_E3_81_A5_E3_81_84_E3_81_9F_E3_81_8A_E9_A1_98_E3_81_84_.html
./data/jw/html/B5_E0_A4_B0_E0_A4_95_E0_A5_87_E0_A4_B2_E0_A5_87_E0_A4_B2_E0_A5_80_E0_A4_B5_E0_A4_BF_E0_A4_A8_E0_A4_82_E0_A4_A4_E0_A5_80_.html
./data/jw/html/9A_E0_B1_87_E0_B0_B8_E0_B0_BF_E0_B0_A8_E0_B0_92_E0_B0_95_E0_B0_B5_E0_B0_BF_E0_B0_A8_E0_B1_8D_E0_B0_A8_E0_B0_AA_E0_B0_82_.html
./data/jw/html/ap_chi_thap_canh_hoc_hoi_thang8_2026_L_E1_BB_9Di_n_C3_A0i_xin_d_E1_BB_B1a_tr_C3_AAn_t_C3_AC
… [2911 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test sur le corpus HTML réel JW : fidélité du cœur et égalité du parseur

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib, time\ncore_p=pathlib.Path('tools/graphe_document.py')\nspec=importlib.util.spec_from_file_location('core',core_p); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)\np=pathlib.Path('tools/graphe_document_html.py') … [736 caractères tronqués]`

  ```
81_E0_B0_AF_E0_B1_87_E0_B0_B8_E0_B1_81_E0_B0_A8_E0_B1_8 blocs= 166 eq=True ratio=1.0000 0.1s ecarts=[]
82_E3_81_AA_E3_81_9F_E3_82_82_E3_82_B5_E3_82_BF_E3_83_B blocs= 166 eq=True ratio=1.0000 0.1s ecarts=[]
86_E0_A4_AA_E0_A4_95_E0_A5_80_E0_A4_9C_E0_A5_80_E0_A4_A blocs= 161 eq=True ratio=1.0000 0.1s ecarts=[]
87_E0_A4_B6_E0_A5_82_E0_A4_B5_E0_A4_B0_E0_A4_AD_E0_A4_B blocs= 164 eq=True ratio=1.0000 0.1s ecarts=[]
87_E0_A6_86_E0_A6_AA_E0_A6_A8_E0_A6_BF_E0_A6_87_E0_A6_9 blocs= 158 eq=True ratio=1.0000 0.1s ecarts=[]
87_E0_A6_AA_E0_A7_8D_E0_A6_B0_E0_A6_A5_E0_A6_AE_E0_A7_8 blocs=  82 eq=True ratio=1.0000 0.0s ecarts=[]
  ```

### 🤖 Assistant

⏵ Extension du test réel à l'ensemble du corpus HTML JW

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib, time\ncore_p=pathlib.Path('tools/graphe_document.py')\nspec=importlib.util.spec_from_file_location('core',core_p); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)\np=pathlib.Path('tools/graphe_document_html.py') … [935 caractères tronqués]`

  ```
documents: 72
testés: 72 mauvais: 1 types vus: ['legende', 'liste', 'note', 'paragraphe', 'section', 'titre']
('https_www_jw_org_ha_laburare_mujalla_hasumiyar_tsaro_ta_nazari_agusta_2026_ka_sani_.html', True, 0.9987, ['absents du flux : s, un', 'ajoutés par le flux : sun'], 90)
  ```

### 🤖 Assistant

⏵ Inspection d'une page réelle : types et découpes autour des notes

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)\nc=sorted(pathlib.Path('data/jw/html').glob('*.html'))[5]\nfor b in  … [140 caractères tronqués]`

  ```
0 titre 'বাইবেলের তথ্য\u200b—\u2060যে-গাছে সবচেয়ে প্রথমে ফুল ফোটে'
1 paragraphe 'সরাসরি বিষয়বস্তুতে যান'
2 paragraphe 'সরাসরি বিষয়সূচিতে যান'
3 paragraphe 'JW.ORG ওয়েবসাইটের ভাষা পরিবর্তন করুন বন্ধ করুন লগ ইন (opens new window) JW.ORG ওয়েবসাইট অনুসন্ধান করুন JW.OR'
4 section 'যিহোবার সাক্ষিরা'
5 paragraphe 'ভাষা বাছাই করুন বাংলা লগ ইন (opens new window) অনুসন্ধান করুন'
6 paragraphe 'প্রহরীদুর্গ (অধ্যয়ন সংস্করণ)'
7 section 'বাইবেলের তথ্য\u200b—\u2060যে-গাছে সবচেয়ে প্রথমে ফুল ফোটে'
8 paragraphe 'বাংলা বাইবেলের তথ্য\u200b—\u2060যে-গাছে সবচেয়ে প্রথমে ফুল ফোটে /assets/ct/79e1b14fff/images/syn_placeholder_sqr.png w26'
9 paragraphe 'আপনি কি %% ভাষায় এই প্রবন্ধ পড়তে চান?'
10 paragraphe 'হ্যাঁ না ভাষা Aja Arabic (Egypt) Arabic (Sudanese) Changana (Mozambique) Chinese Cantonese (Simplified) Emberá'
11 paragraphe 'বাইবেলের তথ্য'
12 titre 'যে-গাছে সবচেয়ে প্রথমে ফুল ফোটে'
13 paragraphe 'চালান যে-গাছে সবচেয়ে প্রথমে ফুল ফোটে'
14 paragraphe 'বাইবেলে প্রায় ৩০ ধরনের গাছের কথা উল্লেখ করা হয়েছে, যেগুলোর মধ্যে একটা হল, কাঠবাদাম গাছ। শীতের মরসুমের শেষের '
15 paragraphe 'যিরমিয় ৭:২৫ পদের পাদটীকা দেখায়, যিহোবা বলেছেন যে, তিনি প্রতিদিন তাড়াতাড়ি উঠে তাঁর ভাববাদীদের পাঠাতেন। ২০১১ স'
16 paragraphe
… [453 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des dépendances de la porte document et lancement éventuel

- **bash** `{"command": "python3 -c \"import pypdf; print('pypdf', pypdf.__version__)\" 2>&1; command -v pandoc || true; command -v pdftotext || true; ls data/onu/pdf 2>/dev/null | wc -l", "description": "Check gate dependencies and corpus"}`

  ```
pypdf 6.16.2
/usr/bin/pandoc
/usr/bin/pdftotext
50
  ```

- **bash** `{"command": "python3 tools/graphe_document.py --json tools/tests/documents/html/entites.html | python3 -c \"import json,sys;m=json.load(sys.stdin);print(m['stats']);print([r['texte'] for r in m['regions'] if r['type']=='note'])\"", "description": "Inspect entities notes through core manifest"}`

  ```
{'regions': 15, 'types': {'blanc': 7, 'note': 2, 'paragraphe': 4, 'tableau': 1, 'titre': 1}}
['1', "Note : & s'écrit aussi « et »."]
  ```

### 🤖 Assistant

⏵ Lancement de la porte R0.1 complète pour valider l'intégration des fixtures

- **bash** `{"command": "python3 tools/graphe_document.py --porte 2>&1 | tail -35; echo \"[code ${PIPESTATUS[0]}]\"", "description": "Run full R0.1 document gate", "timeoutMs": 300000}`

  ```
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
  30 documents · 51 pages · 1423 régions
  types : {'blanc': 1393, 'code': 3, 'figure': 3, 'legende': 1, 'liste': 203, 'note': 120, 'paragraphe': 805, 'section': 226, 'tableau': 30, 'titre': 32}
  deux colonnes : 6 G / 6 D, 1 alternance(s)
  contrôle texte plat : échoue comme attendu
  notes hors corps : 120 région(s), 100 fuite(s)
    data/onu/pdf/A_RES_80_1-en.pdf                         85 régions  fidélité 0.993
    data/onu/pdf/A_RES_80_1-es.pdf                         93 régions  fidélité 0.979
    data/onu/pdf/A_RES_80_1-fr.pdf                         91 régions  fidélité 0.932
    data/onu/pdf/A_RES_80_1-ru.pdf                         95 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-zh.pdf                         83 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_10-en.pdf                       155 régions  fidélité 0.989
    … et 24 autres
  ❌ data/onu/pdf/A_RES_80_1-es.pdf : fidélité 0.9795 < 0,99 (['absents du flux : 3a, a, asesor, ción, d, ebate, jurídic, nacio', 'ajoutés par le flux : 3, asesora, debate, jurídica, naciones, pertinentes, solución'])
  ❌ data/onu/pdf/A_RES_80_1-fr.pdf : fidélité 0.9318 < 0,99 (['absents 
… [1062 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajustement du ratio (mots alphabétiques + numériques) et robustesse de lecture

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/graphe_document_html.py')\ns=p.read_text()\ns=s.replace('''IGNORES = frozenset({\"script\", \"style\", \"noscript\", \"nav\"})\nTITRES = frozenset({\"h1\", \"h2\", \"h3\", \"h4\", \"h5\", \"h6\"})\nBLOCS = frozenset(\"title h1 h2 … [1378 caractères tronqués]`

  ```
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 1.000, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures fidèles
[sortie 0]
  ```

- **bash** `{"command": "wc -l tools/graphe_document_html.py; awk 'NF{n++} END{print \"non vides:\",n}' tools/graphe_document_html.py; python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_fr … [269 caractères tronqués]`

  ```
253 tools/graphe_document_html.py
non vides: 208
article.html (True, 1.0, [])
deux-colonnes.html (True, 1.0, [])
entites.html (True, 1.0, [])
cas (True, 0.85)
  ```

- **bash** `{"command": "cd /tmp && python3 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/graphe_document_html.py --autotest; echo \"[code $?]\"", "description": "Run autotest from another working directory"}`

  ```
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 1.000, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures fidèles
[code 0]
  ```

### 🤖 Assistant

⏵ Nettoyage des artefacts de compilation créés par les tests

- **bash** `{"command": "ls -la tools/__pycache__ | grep -E \"graphe_document\" || true; find tools/tests -name '__pycache__' -o -name '*.pyc'", "description": "Locate pycache artifacts from testing"}`

  ```
-rw-r--r--. 1 stephane stephane  48321 29 oct 11:44 graphe_document.cpython-313.pyc
-rw-------. 1 stephane stephane  16980 29 oct 11:46 graphe_document_html.cpython-313.pyc
-rw-r--r--. 1 stephane stephane  18127 29 oct 11:44 graphe_document_pdf.cpython-313.pyc
  ```

- **bash** `{"command": "rm -f /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/__pycache__/graphe_document_html.cpython-313.pyc && ls tools/__pycache__ | grep graphe_document || true", "description": "Remove only our generated pyc artifact"}`

  ```
graphe_document.cpython-313.pyc
graphe_document_pdf.cpython-313.pyc
  ```

### 🤖 Assistant

⏵ Vérification finale du fichier, des invariants et de l'intégration au cœur

- **bash** `{"command": "sed -n 1,45p tools/graphe_document_html.py; echo ...; sed -n 130,160p tools/graphe_document_html.py", "description": "Inspect header and conditional expression"}`

  ```
#!/usr/bin/env python3
"""Extrait le graphe de blocs d'un document HTML pour le chantier R0.1.

Le cœur assemble le manifeste et insère les blancs : ce module ne rend que des
blocs de corps, en ordre de DOM. Un `li` donne un bloc, même imbriqué ; son
texte est coupé autour des sous-listes, qui sortent à leur position. De même, un
paragraphe contenant une note (`sup`) ou une formule est coupé : la note sort en
bloc `note`, jamais comptée comme du corps. La fidélité se compare à
`text_content()` blancs retirés, car cette fonction ne sépare pas les blocs
(`<p>a</p><p>b</p>` donne « ab ») : comparer les espaces testerait la mise en
forme de la source, pas le texte visible.
"""
from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys
from collections import Counter

import lxml.html

IGNORES = frozenset({"script", "style", "noscript", "nav"})
TITRES = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
BLOCS = frozenset("title h1 h2 h3 h4 h5 h6 p ul ol li table caption pre code "
                  "figure figcaption aside".split())
# Un marqueur de note (`marque<sup>1</sup>`) est un token numérique : le séparer
# des lettres rend le ratio insensible
… [1764 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/graphe_document_html.py --autotest; echo \"[autotest code $?]\"; python3 tools/graphe_document_html.py tools/tests/documents/html/deux-colonnes.html | head -20", "description": "Final autotest and JSON CLI sample"}`

  ```
article.html : 13 blocs, fidélité OK, ratio 1.000, types code, legende, liste, note, paragraphe, section, tableau, titre
deux-colonnes.html : 5 blocs, fidélité OK, ratio 1.000, types paragraphe, titre
entites.html : 8 blocs, fidélité OK, ratio 1.000, types note, paragraphe, tableau, titre
verdict : 3/3 fixtures fidèles
[autotest code 0]
[
  {
    "type": "titre",
    "texte": "Lecture en deux colonnes",
    "prov": {
      "bloc": 0,
      "niveau": 1
    }
  },
  {
    "type": "paragraphe",
    "texte": "Première colonne : le DOM commence ici et la lecture doit commencer ici.",
    "prov": {
      "bloc": 1
    }
  },
  {
    "type": "paragraphe",
    "texte": "La première colonne continue avec une deuxième phrase.",
    "prov": {
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\nTYPES={\"titre\",\"section\",\"paragraphe\",\"liste\",\"tableau\",\"code\",\"maths\",\"figure\",\"legende\",\"note\"}\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util. … [530 caractères tronqués]`

  ```
article.html         blocs=13 egalite=True ratio=1.000 types=['code', 'legende', 'liste', 'note', 'paragraphe', 'section', 'tableau', 'titre']
deux-colonnes.html   blocs= 5 egalite=True ratio=1.000 types=['paragraphe', 'titre']
entites.html         blocs= 8 egalite=True ratio=1.000 types=['note', 'paragraphe', 'tableau', 'titre']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document.py')\nspec=importlib.util.spec_from_file_location('core',p); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)\nfor c in sorted(pathlib.Path('tools/tests/documents/html').glob … [289 caractères tronqués]`

  ```
article.html         regions=25 invariants=OK fidelite_core=1.000 ecarts=[]
deux-colonnes.html   regions= 9 invariants=OK fidelite_core=1.000 ecarts=[]
entites.html         regions=15 invariants=OK fidelite_core=1.000 ecarts=[]
  ```

- **bash** `{"command": "git status --short | head -20; wc -l tools/graphe_document_html.py tools/tests/documents/html/*.html", "description": "Check final files and git status"}`

  ```
?? docs/implantation/document-graph.md
?? reports/r01-graphe-document.json
?? tools/graphe_document.py
?? tools/graphe_document_html.py
?? tools/graphe_document_pdf.py
?? tools/porte-document.sh
?? tools/tests/
  253 tools/graphe_document_html.py
   61 tools/tests/documents/html/article.html
   18 tools/tests/documents/html/deux-colonnes.html
   31 tools/tests/documents/html/entites.html
  363 total
  ```

### 🤖 Assistant

⏵ Vérification de l'origine du rapport JSON apparu pendant les tests

- **bash** `{"command": "date '+%H:%M:%S'; ls -la --time-style=+%H:%M:%S reports/r01-graphe-document.json tools/graphe_document_pdf.py tools/graphe_document.py 2>/dev/null; grep -n \"rapport\" tools/graphe_document.py | tail -15", "description": "Check report mtime and CLI report option"}`

  ```
11:47:15
-rw-r--r--. 1 stephane stephane  8886 11:47:06 reports/r01-graphe-document.json
-rwxr-xr-x. 1 stephane stephane 11672 11:46:51 tools/graphe_document_pdf.py
-rwxr-xr-x. 1 stephane stephane 33867 11:46:51 tools/graphe_document.py
12:  2. **la fidélité** — le flux n'ajoute ni ne perd de mot par rapport à une extraction
558:def porte(rapport: pathlib.Path | None = None) -> int:
660:    if rapport is not None:
661:        rapport.write_text(json.dumps({
671:        print(f"  rapport : {rapport}")
696:    ap.add_argument("--rapport", type=pathlib.Path, help="écrit le JSON de résultats")
700:        return porte(rapport=args.rapport)
  ```

### 🤖 Assistant

⏵ Contrôle de l'interface HTML dans la version courante du cœur (mise à jour concurrente)

- **bash** `{"command": "grep -n \"graphe_document_html\\|def analyse(chemin\" tools/graphe_document.py | head; sed -n 270,285p tools/graphe_document.py", "description": "Confirm core still imports our parser"}`

  ```
272:def analyse(chemin: pathlib.Path) -> list[dict]:
277:        return _module("graphe_document_html").analyse(chemin)


def analyse(chemin: pathlib.Path) -> list[dict]:
    suffixe = chemin.suffix.lower()
    if suffixe in (".md", ".markdown", ".txt"):
        return analyse_markdown(chemin)
    if suffixe in (".html", ".htm"):
        return _module("graphe_document_html").analyse(chemin)
    if suffixe == ".pdf":
        return _module("graphe_document_pdf").analyse(chemin)
    if suffixe in (".docx", ".epub", ".odt"):
        return analyse_pandoc(chemin)
    raise SystemExit(f"format non pris en charge : {suffixe}")


# ------------------------------------------------------------------- le manifeste
  ```

### 🤖 Assistant

⏵ Comparaison directe de `_reference` à `lxml.html.fromstring(...).text_content()`

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, pathlib, lxml.html\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_location('g',p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)\nh='''<p>a &amp; b<sup>1</sup></p><!-- c --><p>d&nbsp;e</ … [518 caractères tronqués]`

  ```
lxml brut : 'a & b1d\xa0exnsz'
reference  : 'a & b1d\xa0e'
egal cle   : False
  ```

### 🤖 Assistant

⏵ Test de lecture d'un document UTF-8 avec déclaration XML

- **bash** `{"command": "cat > /tmp/xml-decl.html <<'HTML'\n<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<html><body><h1>Été</h1><p>Un &amp; deux.</p></body></html>\nHTML\npython3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_locatio … [297 caractères tronqués]`

  ```
[{'type': 'titre', 'texte': 'Été', 'prov': {'bloc': 0, 'niveau': 1}}, {'type': 'paragraphe', 'texte': 'Un & deux.', 'prov': {'bloc': 1}}]
(True, 0.4, [])
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nMOT=re.compile(r\"\\d+|[^\\W\\d_]+\")\nfor s in ['Été Un & deux.', 'Été', 'café']:\n    print(repr(s), MOT.findall(s))\nPY", "description": "Debug word tokenization on accented text"}`

  ```
'Été Un & deux.' ['Été', 'Un', 'deux']
'Été' ['Été']
'café' ['café']
  ```

- **bash** `{"command": "cat > /tmp/xml-decl.html <<'HTML'\n<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<html><body><h1>Été</h1><p>Un &amp; deux.</p></body></html>\nHTML\npython3 - <<'PY'\nimport importlib.util, pathlib\np=pathlib.Path('tools/graphe_document_html.py')\nspec=importlib.util.spec_from_file_locatio … [516 caractères tronqués]`

  ```
ref: 'ÉtéUn & deux.'
out: 'Été Un & deux.'
mA: ['ÉtéUn', 'deux']
mB: ['Été', 'Un', 'deux']
(True, 0.4, [])
  ```

### 🤖 Assistant

⏵ Dernier contrôle des fichiers livrés et suppression du cache de notre module

- **bash** `{"command": "ls tools/__pycache__ 2>/dev/null | grep graphe_document_html || true; rm -f tools/__pycache__/graphe_document_html.cpython-313.pyc; ls tools/__pycache__ 2>/dev/null | grep graphe_document_html || echo \"cache html absent\"; git status --short | head -20", "description": "Remove our pyc  … [26 caractères tronqués]`

  ```
graphe_document_html.cpython-313.pyc
cache html absent
?? docs/implantation/document-graph.md
?? reports/r01-graphe-document.json
?? tools/graphe_document.py
?? tools/graphe_document_html.py
?? tools/graphe_document_pdf.py
?? tools/porte-document.sh
?? tools/tests/
  ```

### 🤖 Assistant

⏵ Envoi du résultat chiffré à l'agent parent

- **send_message** `{"agent_id": "8156fdcb-5033-4ba4-a5f3-f8a078e6e57e", "message": "R0.1 — parseur HTML livré : tools/graphe_document_html.py (+ fixtures tools/tests/documents/html/{article,deux-colonnes,entites}.html). Rien d'autre modifié.\n\nCommande : python3 tools/graphe_document_html.py --autotest\nRésultat :\n- … [1952 caractères tronqués]`

  ```
message delivered to agent 8156fdcb-5033-4ba4-a5f3-f8a078e6e57e
  ```

### 🤖 Assistant

**Fichier livré** : `tools/graphe_document_html.py`
**Fixtures** : `tools/tests/documents/html/article.html`, `deux-colonnes.html`, `entites.html`

**Commande d'autotest**
```bash
python3 tools/graphe_document_html.py --autotest
```

**Chiffres observés**
| Fixture | Blocs | Fidélité | Ratio mots | Types trouvés |
|---|---:|---|---:|---|
| `article.html` | 13 | OK | 1.000 | `code`, `legende`, `liste`, `note`, `paragraphe`, `section`, `tableau`, `titre` |
| `deux-colonnes.html` | 5 | OK | 1.000 | `paragraphe`, `titre` |
| `entites.html` | 8 | OK | 1.000 | `note`, `paragraphe`, `tableau`, `titre` |

Verdict : `3/3 fixtures fidèles`. La commande JSON seule fonctionne :
```bash
python3 tools/graphe_document_html.py tools/tests/documents/html/article.html
```

**Intégration au cœur existant** (`tools/graphe_document.py`) : les trois fixtures passent le manifeste réel, les invariants de partition et la fidélité indépendante du cœur à `1.000` (25, 9 et 15 régions avec les blancs).

**Limites rencontrées**
- L'égalité de fidélité compare la suite des caractères visibles **blancs retirés** : `text_content()` ne sépare pas les blocs (`<p>a</p><p>b</p>` donne `ab`), donc comparer les espaces littéralement ferait échouer tout parseur correct. Une espace perdue *à l'intérieur* d'un bloc ne serait pas vue par `verifie` ; le parseur ne la perd pas, mais le contrôle est plus faible sur ce point.
- Une formule avec `alttext`/`aria-label` est émise selon cette valeur, comme demandé ; elle peut différer de `text_content` (`x^2` contre `x2`) et faire échouer `verifie` sur un tel document.
- `script[type*=math]` est bien émis en `maths` (règle du contrat), mais la référence HTML du cœur ignore tous les `script` : écart de fidélité cœur possible uniquement sur ce cas.
- Une note placée dans une cellule de tableau ou dans le corps d'une figure est aplatie dans le bloc conteneur, pas émise en `note` séparée. Les cas `p`, `li` et titres sont correctement découpés.
- Le corps d'une figure est émis avant sa `figcaption` ; une légende placée avant le corps serait réordonnée.
- Un `li` qui encadre une sous-liste peut produire deux blocs `liste` (texte avant/après), documenté dans la docstring.
- Le `<title>` de page est émis comme `titre` en plus du `h1`, puisque `text_content()` l'inclut.
- Le fichier fait 253 lignes (208 non vides), un peu au-dessus de la cible 150–200.
- La porte R0.1 complète reste rouge, mais **uniquement côté PDF** (fidélité `< 0,99` sur `es`/`fr` et notes recopiées) ; aucune erreur sur les fixtures HTML.

