# Session DSH — relecture

- identifiant : `861d98b1-8179-4589-b485-f1a87704cab1`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-19 14:15:56
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave Natif », tout en français). Ta tâche est un sous-chantier AUTONOME et PRÉCIS : construire et VALIDER un alignement phrase-à-phrase entre l'original français et la traduction anglaise du « Tour du monde en quatre-vingts jours » de Jules Verne, pour servir de banc de traduction littéraire.

CONTEXTE (à lire avant d'agir) :
- Les textes sont dans /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/ :
  around_world_80_days_fr.txt (original, ~452 Ko) et around_world_80_days_en.txt (traduction, ~375 Ko).
- La mesure 59 du dépôt a montré que les tentatives précédentes étaient INVALIDES : découpage par titres donnant 84 sections françaises contre 37 anglaises (la table des matières compte double), puis appariement proportionnel, puis corps à 60 contre 37 — dans les trois cas le chrF était au niveau du hasard. Ce n'est pas le modèle, c'est l'appariement. Lis le récit de la mesure 59 dans reports/07-mesures-couche-commune.md (cherche « Mesure 59 »).
- Le dépôt exige qu'un alignement soit VÉRIFIÉ, PAS SUPPOSÉ. La validation doit utiliser des ANCRES indépendantes : noms propres (Phileas Fogg, Passepartout, Fix, Aouda, Sir Francis Cromarty, le Reform Club, etc.), débuts/fins de chapitres, et la structure en chapitres (37 chapitres dans chaque langue, à vérifier).

CE QUE TU DOIS FAIRE :
1. Écrire un outil CPU-only (pas de GPU, pas de modèle) : tools/aligneur_litteraire.py. Découpage en phrases robuste (abréviations, guillemets, dialogues), puis appariement par longueur type Gale-Church (programmation dynamique) ou meilleur alignement de chaînes, à l'échelle du CHAPITRE (les chapitres sont les ancres structurelles).
2. Vérifier la structure : compter les chapitres dans les deux langues (attention aux tables des matières et aux doublons : filtrer par longueur), et n'apparier que les chapitres dont les numéros correspondent.
3. VALIDER l'alignement avec les noms propres : pour chaque paire de phrases alignées, vérifier que les noms propres attendus (dictionnaire des personnages/lieux, insensible à la casse et aux accents) apparaissent dans les DEUX phrases, ou dans un voisinage de ±2 phrases. Rapporter le taux de rappel des ancres, le taux de phrases sans ancre, et la distribution des rapports de longueur. Un alignement n'est valide que si les ancres se retrouvent à un taux très supérieur au hasard — calcule aussi un contrôle négatif (mélanger les chapitres ou décaler les phrases) pour montrer que le taux tombe.
4. Écrire le résultat dans data/alignement/verne_fr_en.json (paires {chapitre, i_fr, i_en, fr, en}) — data/ est gitignoré, ce n'est pas grave — et un petit rapport de mesure dans reports/alignement-verne.md (fiche autonome, avec le dispositif, les chiffres, le contrôle négatif, et ce qui pourrait rendre le chiffre faux).
5. NE MODIFIE AUCUN fichier existant (surtout pas docs/en-cours.md, reports/07-mesures-couche-commune.md, journal/, AGENTS.md). NE FAIS AUCUN commit. Tu peux créer uniquement : tools/aligneur_litteraire.py, data/alignement/*, reports/alignement-verne.md, et des fichiers temporaires dans /tmp.
6. Utilise /home/stephane/IA/venv-drave/bin/python (il a numpy) et force CUDA_VISIBLE_DEVICES="" pour tout run (d'autres travaux utilisent les GPU).

CE QUE TU DOIS RAPPORTER À LA FIN (dans ta réponse finale, en français) :
- le nombre de chapitres appariés dans chaque langue et la façon dont tu as filtré les tables des matières ;
- le nombre de paires de phrases alignées ;
- le taux de rappel des ancres (noms propres) et le contrôle négatif ;
- la distribution des rapports de longueur des paires ;
- le chemin du JSON et de la fiche ;
- les limites (ce qui pourrait rendre l'alignement faux) ;
- si tu estimes l'alignement VALIDE ou NON, avec le chiffre qui le dit.

Sois rigoureux : un alignement « plausible » ne suffit pas. Si tu n'arrives pas à un alignement validé, dis-le et explique ce qui bloque ; ne fabrique pas de chiffres.
Your parent agent id is "d629d7d7-e122-4596-8757-f4264a2b15cf". Before you finish, send your result to that agent with send_message({ agent_id: "d629d7d7-e122-4596-8757-f4264a2b15cf", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave Natif

> Ce fichier est la **première chose à lire** avant d'agir sur ce dépôt. Il dit la **mission**, l'**ordre des
> priorités**, et les **règles de rangement** — pas l'historique (il est dans `journal/`).

## 1. La mission, et l'ordre des priorités

Drave Natif se construit **couche par couche**, et on ne passe pas à la suivante tant que la précédente est
**perfectible** :

1. **Les modules d'ENTRÉE et de SORTIE linguistiques** — c'est la priorité absolue. Ils doivent être **parfaits** et
   **très riches en langues et en domaines** : lire et produire toutes les langues, dialectes et styles, dans les
   registres techniques, littéraires, juridiques, quotidiens.
   - On les **teste en qualité de traducteur** — c'est le juge de paix : *restitution* (même langue, à l'identique)
     et *traduction* (même sens, autre langue, autre style).
   - **On continue tant qu'ils sont perfectibles**, et on ne « déclare complet » que sur des chiffres qui couvrent
     les langues, les dialectes, les styles et les domaines.
2. **Le module de pensée abstraite, indépendant de la langue** — seulement après. Il ne peut pas être conçu sur une
   entrée-sortie qui n'est pas fiable.

**Le temps imparti est un plancher, pas un plafond** (*carpe diem*, `docs/relations-humaines.md` § Addendum) :
on ne s'arrête pas parce qu'une échéance est passée ; on s'arrête quand la couche est faite, mesurée et écrite.

## 2. Le rangement : `docs/` n'est pas `reports/`

C'est la règle la plus souvent violée, et elle est **stricte** :

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | l'**état actuel**, la **mission**, la **vision**, l'**architecture**, les **concepts** et les **modes d'emploi** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`) | du code |

Une page de `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/` ; il reste dans `docs/` un
**résumé de l'état** (ce qu'on sait, ce qu'on ne sait pas, et le lien vers la fiche).
À chaque cycle : `docs/en-cours.md` dit l'état **courant** en quelques lignes, pas l'historique.

## 3. Ce qu'un résultat doit porter, à chaque fois

- le **chiffre**, la **mesure** qui le produit, et le **dispositif** (quel corpus, quel modèle, quelle couche,
  quel découpage) ;
- le **contrôle négatif** quand il y en a un (hasard, étiquettes mélangées, corpus mélangé) — sans lui, le chiffre
  n'est pas un résultat ;
- **à côté du chiffre, ce qui pourrait le rendre faux** (les pièges d'instrument) ;
- un **commit** par résultat mesuré, et la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
  `docs/en-cours.md`.

## 4. Les portes

`bash tools/toutes-les-portes.sh` écrit `registre.txt` ; on lit le verdict par `awk '$2 != 0'` — **jamais** par les
marqueurs ni à travers un tube. Les deux rouges structurelles connues sont `porte-indice` et `porte-melange` ; toute
**autre** rouge est une régression et se corrige avant de continuer.


## 5. Étudier Panini et Nipada, régulièrement

Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
une **généalogie des langues, dialectes et styles**.

**Règle** : à chaque cycle, lire ce qui a bougé chez eux (docs, publications, journaux de bord) et confronter leurs
résultats aux nôtres. Ce qui en sort va dans [`docs/genealogie-des-langues.md`](docs/genealogie-des-langues.md)
(la théorie) — jamais les chiffres (ils vont dans `reports/`).

**Leur avertissement, à ne pas oublier** ✗✓ : leur signature lexicale capte **l'époque** (β +0,138) bien plus que la
**filiation** (β +0,049) — *la surface transmet les signifiants, pas la généalogie*. Tout test de style doit donc
**contrôler la date**, et tout test de famille doit **contrôler la surface**.

## 6. La documentation : `docs/` reflète **tous** les chantiers, et une synthèse toujours à jour

- **`docs/en-cours.md` est le tableau de bord** : il porte les **sept chantiers**, leurs **dépendances**, leurs
  **sous-chantiers indépendants** (ce qui peut tourner en parallèle) et leur **état**. Il porte aussi, en tête, une
  **synthèse** de l'état de la couche — celle qu'on lit si on ne lit qu'une page.
- **`reports/` reçoit les données intermédiaires et les références** de nos travaux : fiches de mesure, JSON de
  résultats, dumps d'expériences, brouillons de référence. *Tout ce qui n'est pas « ce qui reste vrai quand les
  chiffres changent » va dans `reports/`, jamais dans `docs/`.*
- **`docs/synthese/` porte la synthèse théorique** (7 chapitres, 7 schémas), et son `index.md` doit refléter les
  sept chantiers.

### 6.1 La revue de fin de sous-chantier (obligatoire)

**Quand** : à la **fin de chaque sous-chantier** (et au minimum une fois par cycle), avant le commit de clôture.
**Quoi** : `python3 tools/revue_documentation.py` vérifie, et **corrige** avant de continuer :

1. **classement** : un résultat qui traîne dans `docs/` est déplacé dans `reports/` ; une page de `docs/` qui n'a
   plus de « ce qui reste vrai » est supprimée ;
2. **structure** : chaque chantier de `en-cours.md` a son entrée, son état, sa fiche, et ses sous-chantiers ;
3. **annotation** : tous les **liens internes** résolvent (docs ↔ reports ↔ journal), et les **sources externes**
   (Glottolog, Gutenberg, Unicode UDHR, Panini/Nipada) sont citées avec leur URL ou leur chemin ;
4. **fraîcheur** : la date de `en-cours.md` est l'**heure locale** du dernier commit (jamais une estimation) ;
5. **cohérence** : la synthèse (`docs/synthese/index.md`) et le tableau de bord disent la même chose.

*Une documentation qui n'est pas revue à la fin d'un sous-chantier est une documentation qui mentira au cycle
suivant* ✗✓.

## 7. Le miroir de sortie renforce le modèle d'entrée

**Le principe** : notre **sens → texte** (la sortie) sera toujours **plus léger et plus fiable** que notre
**texte → sens** (l'entrée) ✓✓ — parce que l'entrée doit gérer les **imperfections** du réel (bruit, orthographes
multiples, langues mêlées, coquilles), alors que la sortie part d'un sens **propre** ✓. On s'en sert donc comme
d'un **miroir** :

1. **valider l'entrée par la sortie** ✓✓ : ce que l'entrée a compris doit pouvoir être **reproduit** par la sortie
   (restitution, ou **boucle** entrée → sortie → entrée ✓). *Si la sortie ne peut pas le redire, l'entrée a inventé
   ou perdu quelque chose* ✗✓ ;
2. **découpler le signal du bruit** ✓✓ : la sortie, plus fiable, sert de **référence** pour juger l'entrée — on
   mesure l'écart entre ce que l'entrée a extrait et ce que la sortie sait reconstruire ;
3. **garder des marqueurs de bruit dans l'interface post-linguistique** ✓✓ : le sens extrait porte **où** et
   **combien** l'entrée est incertaine (confiance par token, ambiguïtés non résolues, langues détectées avec leur
   probabilité). *Le module de pensée abstraite doit recevoir un sens **annoté de son bruit**, pas un sens lissé* ✓✓ ;
4. **conséquence pour les tests** : toute mesure d'entrée (traduction, contenu, langue) se double d'une mesure de
   **sortie** (restitution, boucle) — c'est le **juge de paix** de la couche ✓✓.
   
# Ressources

Tu es probablement sur Hauru. Si c'est le cas, tu as beaucoup de ressources matérielles à ta disposition : 2 un tandem RTX 5000 en nvlink est dédié au projet (la carte AMD est dédiée à l'affichage), le raid nvme (4x256GB) est totalement à ta disposition entièrement, tu ax beaucoup de RAM et 2 CPU avec beaucoup de cores (attention aux subtilités hyperthread et affinité des processus). Tu as généralemment une allocation de traitement DeepSeek très élevée et extensible au besoin. Tu peux donc travailler 24/7 sur beaucoup de tâches en parallèles.

# Philosophie carpe diem

Tu as beaucoup de ressources et de temps, mais l'humain n'est pas toujours disponible et son temps de vie est très précieux. Tu ne dois donc jamais suspendre tous les travaux en attendant une réponse. Tire le maximum de chaque journée afin que chaque moment compte. Il vaut mieux consolider les questions en attente à même le fichier en-cours.md et pour les questions qui ne sont pas sur la vision ou la philosophie, tenter d'y répondre toi-même que d'attendre un humain si ça retarde un chantier. Tu peux même travailler sur plusieurs hypothèses dans le doute.



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

⏵ Reading the measure 59 narrative and inspecting the two source texts

I'll start by reading the context: the measure 59 story and the structure of both text files.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/ && wc -c /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/*.txt", "description": "List source text files and sizes"}`

  ```
total 828
drwxr-xr-x. 1 stephane stephane    108 27 jan  2026 .
drwxr-xr-x. 1 stephane stephane    494 27 jan  2026 ..
-rw-r--r--. 1 stephane stephane 383991 27 jan  2026 around_world_80_days_en.txt
-rw-r--r--. 1 stephane stephane 462216 27 jan  2026 around_world_80_days_fr.txt
383991 /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_en.txt
462216 /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt
846207 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Mesure 59\" reports/07-mesures-couche-commune.md | head -20", "description": "Locate measure 59 in report"}`

  ```
2037:## Mesure 59 — le banc littéraire est **invalide** : l'alignement n'est pas résolu
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2030,2140p' reports/07-mesures-couche-commune.md", "description": "Read measure 59 narrative"}`

  ```
intuition était juste** ✓✓ : dans un modèle chinois, le chinois est parmi les langues les mieux supportées ✓✓ ;
* **mais le marqueur a encore un défaut** ✗✓ : l'**article 1 anglais** (le plus court) est détecté « french » 1,00
  ✗✗ — *sur un texte court, la langue de la consigne ou du contexte pèse plus que le texte* ✓✓ (le 22ᵉ piège :
  la détection de langue sur textes courts est une **décision à seuil**, pas une mesure ✓✓) ;
* **ce que cela donne à l'interface** ✓✓ : à 3 B, les marqueurs de bruit sont **fiables** (langue ✓, surprisal ✓) sauf
  sur les textes très courts ✓✗ — *l'interface doit donc marquer la **longueur** comme facteur de confiance* ✓✓.

## Mesure 59 — le banc littéraire est **invalide** : l'alignement n'est pas résolu

Trois tentatives sur Le Tour du monde (français original ↔ traduction anglaise) pour un deuxième domaine ✗✗ :

| tentative | ce qui a été fait | résultat |
|---|---|---|
| 1 | découpage par titres de chapitres | **84 sections françaises** contre 37 anglaises ✗✗ (table des matières comptée deux fois) → chrF 17,7 = hasard |
| 2 | grille anglaise + français **proportionnel**, sortie 400 tokens | chrF 21,4 · plancher 21,7 · **hasard 22,8** ✗✗ |
| 3 | 
… [7396 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && head -60 around_world_80_days_fr.txt && echo \"=====EN=====\" && head -60 around_world_80_days_en.txt", "description": "Show heads of both texts"}`

  ```
﻿The Project Gutenberg eBook of Le tour du monde en quatre-vingts jours
    
This ebook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever. You may copy it, give it away or re-use it under the terms
of the Project Gutenberg License included with this ebook or online
at www.gutenberg.org. If you are not located in the United States,
you will have to check the laws of the country where you are located
before using this eBook.

Title: Le tour du monde en quatre-vingts jours

Author: Jules Verne

Release date: January 1, 1997 [eBook #800]
                Most recently updated: October 5, 2013

Language: French

Credits: Produced by ebooksgratuits


*** START OF THE PROJECT GUTENBERG EBOOK LE TOUR DU MONDE EN QUATRE-VINGTS JOURS ***




Produced by ebooksgratuits





Jules Verne

LE TOUR DU MONDE EN QUATRE-VINGTS JOURS

(1873)




Table des matières


I DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RÉCIPROQUEMENT
L'UN COMME MAÎTRE, L'AUTRE COMME DOMESTIQUE

II OÙ PASSEPARTOUT EST CONVAINCU QU'IL A ENFIN TROUVE SON IDEAL

III OÙ S'ENGAGE UN
… [3974 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && grep -n -E \"^(CHAPITRE|[IVX]+[ .]|CHAPTER)\" around_world_80_days_fr.txt | head -120", "description": "Find chapter-like lines in French text"}`

  ```
46:I DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RÉCIPROQUEMENT
49:II OÙ PASSEPARTOUT EST CONVAINCU QU'IL A ENFIN TROUVE SON IDEAL
51:III OÙ S'ENGAGE UNE CONVERSATION QUI POURRA COUTER CHER À PHILEAS FOGG
53:IV DANS LEQUEL PHILEAS FOGG STUPEFIE PASSEPARTOUT, SON DOMESTIQUE
55:V DANS LEQUEL UNE NOUVELLE VALEUR APPARAÎT SUR LA PLACE DE LONDRES
57:VI DANS LEQUEL L'AGENT FIX MONTRE UNE IMPATIENCE BIEN LEGITIME
59:VII QUI TÉMOIGNE UNE FOIS DE PLUS DE L'INUTILITÉ DES PASSEPORTS EN
62:VIII DANS LEQUEL PASSEPARTOUT PARLE UN PEU PLUS PEUT-ÊTRE QU'IL NE
65:IX OÙ LA MER ROUGE ET LA MER DES INDES SE MONTRENT PROPICES AUX DESSEINS
68:X OÙ PASSEPARTOUT EST TROP HEUREUX D'EN ÊTRE QUITTE EN PERDANT SA
71:XI OÙ PHILEAS FOGG ACHÈTE UNE MONTURE À UN PRIX FABULEUX
73:XII OÙ PHILEAS FOGG ET SES COMPAGNONS S'AVENTURENT À TRAVERS LES FORÊTS
76:XIII DANS LEQUEL PASSEPARTOUT PROUVE UNE FOIS DE PLUS QUE LA FORTUNE
79:XIV DANS LEQUEL PHILEAS FOGG DESCEND TOUTE L'ADMIRABLE VALLÉE DU GANGE
82:XV OÙ LE SAC AUX BANK-NOTES S'ALLÈGE ENCORE DE QUELQUES MILLIERS DE
85:XVI OÙ FIX N'A PAS L'AIR DE CONNAÎTRE DU TOUT LES CHOSES DONT ON LUI
88:XVII OÙ IL EST QUESTION DE CHOSES ET D'AUTRES PENDANT
… [1489 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && grep -n \"^CHAPTER\" around_world_80_days_en.txt | head -60; echo \"---- FR table fin / corps début ----\"; grep -n \"Table des matières\" around_world_80_days_fr.txt", "descri … [41 caractères tronqués]`

  ```
56:CHAPTER I.
223:CHAPTER II.
339:CHAPTER III.
616:CHAPTER IV.
766:CHAPTER V.
876:CHAPTER VI.
1048:CHAPTER VII.
1176:CHAPTER VIII.
1360:CHAPTER IX.
1544:CHAPTER X.
1720:CHAPTER XI.
2018:CHAPTER XII.
2273:CHAPTER XIII.
2520:CHAPTER XIV.
2733:CHAPTER XV.
3005:CHAPTER XVI.
3185:CHAPTER XVII.
3387:CHAPTER XVIII.
3551:CHAPTER XIX.
3830:CHAPTER XX.
4086:CHAPTER XXI.
4384:CHAPTER XXII.
4615:CHAPTER XXIII.
4867:CHAPTER XXIV.
5089:CHAPTER XXV.
5337:CHAPTER XXVI.
5519:CHAPTER XXVII.
5729:CHAPTER XXVIII.
6051:CHAPTER XXIX.
6339:CHAPTER XXX.
6619:CHAPTER XXXI.
6831:CHAPTER XXXII.
7001:CHAPTER XXXIII.
7312:CHAPTER XXXIV.
7435:CHAPTER XXXV.
7646:CHAPTER XXXVI.
7786:CHAPTER XXXVII.
---- FR table fin / corps début ----
43:Table des matières
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && sed -n '138,200p' around_world_80_days_fr.txt", "description": "Show French body start"}`

  ```
XXXVI DANS LEQUEL PHILEAS FOGG FAIT DE NOUVEAU PRIME SUR LE MARCHÉ

XXXVII DANS LEQUEL IL EST PROUVÉ QUE PHILEAS FOGG N'A RIEN GAGNÉ À FAIRE
CE TOUR DU MONDE, SI CE N'EST LE BONHEUR




I

DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RÉCIPROQUEMENT L'UN
COMME MAÎTRE, L'AUTRE COMME DOMESTIQUE


En l'année 1872, la maison portant le numéro 7 de Saville-row,
Burlington Gardens--maison dans laquelle Sheridan mourut en 1814--,
était habitée par Phileas Fogg, esq., l'un des membres les plus
singuliers et les plus remarqués du Reform-Club de Londres, bien qu'il
semblât prendre à tâche de ne rien faire qui pût attirer l'attention.

À l'un des plus grands orateurs qui honorent l'Angleterre, succédait
donc ce Phileas Fogg, personnage énigmatique, dont on ne savait rien,
sinon que c'était un fort galant homme et l'un des plus beaux gentlemen
de la haute société anglaise.

On disait qu'il ressemblait à Byron--par la tête, car il était
irréprochable quant aux pieds--, mais un Byron à moustaches et à
favoris, un Byron impassible, qui aurait vécu mille ans sans vieillir.

Anglais, à coup sûr, Phileas Fogg n'était peut-être pas Londonner. On ne
l'avait jamais 
… [2028 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && grep -n -E \"^[IVXLC]+$\" around_world_80_days_fr.txt | head -60; echo \"count:\"; grep -c -E \"^[IVXLC]+$\" around_world_80_days_fr.txt", "description": "Find bare roman numer … [20 caractères tronqués]`

  ```
count:
0
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && sed -n '140,230p' around_world_80_days_en.txt | head -80; echo \"=== tail fr ===\"; tail -40 around_world_80_days_fr.txt; echo \"=== tail en ===\"; tail -40 around_world_80_day … [59 caractères tronqués]`

  ```
and illumined by blue painted windows. When he breakfasted or dined all
the resources of the club—its kitchens and pantries, its buttery and
dairy—aided to crowd his table with their most succulent stores; he was
served by the gravest waiters, in dress coats, and shoes with swan-skin
soles, who proffered the viands in special porcelain, and on the finest
linen; club decanters, of a lost mould, contained his sherry, his port,
and his cinnamon-spiced claret; while his beverages were refreshingly
cooled with ice, brought at great cost from the American lakes.

If to live in this style is to be eccentric, it must be confessed that
there is something good in eccentricity.

The mansion in Saville Row, though not sumptuous, was exceedingly
comfortable. The habits of its occupant were such as to demand but
little from the sole domestic, but Phileas Fogg required him to be
almost superhumanly prompt and regular. On this very 2nd of October he
had dismissed James Forster, because that luckless youth had brought
him shaving-water at eighty-four degrees Fahrenheit instead of
eighty-six; and he was awaiting his successor, who was due at the house
between eleven and half-past.
… [6030 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && sed -n '148p' around_world_80_days_fr.txt | cat -A | head -5; file around_world_80_days_fr.txt around_world_80_days_en.txt; grep -n \"^\\* END OF\" around_world_80_days_fr.txt  … [85 caractères tronqués]`

  ```
DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RM-CM-^ICIPROQUEMENT L'UN^M$
around_world_80_days_fr.txt: Unicode text, UTF-8 (with BOM) text, with CRLF line terminators
around_world_80_days_en.txt: Unicode text, UTF-8 text, with CRLF line terminators
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp && cat > explore1.py <<'EOF'\nimport re\nFR=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt\"\nEN=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_w … [770 caractères tronqués]`

  ```
FR len 440788 EN len 369287
FR roman-alone: 37
[(146, 'I'), (338, 'II'), (478, 'III'), (797, 'IV'), (975, 'V'), (1100, 'VI'), (1311, 'VII'), (1457, 'VIII'), (1654, 'IX'), (1892, 'X'), (2107, 'XI'), (2465, 'XII'), (2764, 'XIII'), (3059, 'XIV'), (3321, 'XV'), (3631, 'XVI'), (3839, 'XVII'), (4093, 'XVIII'), (4291, 'XIX'), (4617, 'XX'), (4915, 'XXI'), (5270, 'XXII'), (5543, 'XXIII'), (5814, 'XXIV'), (6050, 'XXV'), (6326, 'XXVI'), (6537, 'XXVII'), (6776, 'XXVIII'), (7148, 'XXIX'), (7470, 'XXX'), (7784, 'XXXI'), (8025, 'XXXII'), (8239, 'XXXIII'), (8601, 'XXXIV'), (8748, 'XXXV'), (8975, 'XXXVI'), (9135, 'XXXVII')]
--- EN
EN chapter lines: 74
(15, ' CHAPTER I. IN WHICH PHILEAS FOGG AND PA')
(16, ' CHAPTER II. IN WHICH PASSEPARTOUT IS CO')
(17, ' CHAPTER III. IN WHICH A CONVERSATION TA')
(18, ' CHAPTER IV. IN WHICH PHILEAS FOGG ASTOU')
(19, ' CHAPTER V. IN WHICH A NEW SPECIES OF FU')
(20, ' CHAPTER VI. IN WHICH FIX, THE DETECTIVE')
(21, ' CHAPTER VII. WHICH ONCE MORE DEMONSTRAT')
(22, ' CHAPTER VIII. IN WHICH PASSEPARTOUT TAL')
(23, ' CHAPTER IX. IN WHICH THE RED SEA AND TH')
(24, ' CHAPTER X. IN WHICH PASSEPARTOUT IS ONL')
(25, ' CHAPTER XI. IN WHICH PHILEAS FOGG SECUR')
(26, ' CHAPTER XII
… [1426 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > explore2.py <<'EOF'\nimport re\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\nfor name in [\"around_world_80_days_fr.txt\",\"around_world_80_days_en.txt\"]:\n    s=open(base+name,encoding='utf-8-sig') … [411 caractères tronqués]`

  ```
===== around_world_80_days_fr.txt
START OF THE PROJECT 748 'START OF THE PROJECT GUTENBERG EBOOK LE TOUR DU MONDE EN QUATRE-VINGTS JOURS ***\n\n\n\n\nProduced by ebooksgratuits\n\n\n\n\n\nJul'
END OF THE PROJECT 422286 'END OF THE PROJECT GUTENBERG EBOOK LE TOUR DU MONDE EN QUATRE-VINGTS JOURS ***\n\n\n    \n\nUpdated editions will replace the'
last 600: 'Books are often created from several printed\neditions, all of which are confirmed as not protected by copyright in\nthe U.S. unless a copyright notice is included. Thus, we do not\nnecessarily keep eBooks in compliance with any particular paper\nedition.\n\nMost people start at our website which has the main PG search\nfacility: www.gutenberg.org.\n\nThis website includes information about Project Gutenberg™,\nincluding how to make donations to the Project Gutenberg Literary\nArchive Foundation, how to help produce our new eBooks, and how to\nsubscribe to our email newsletter to hear about new eBooks.\n\n\n'
===== around_world_80_days_en.txt
START OF THE PROJECT 4 'START OF THE PROJECT GUTENBERG EBOOK 103 ***\n\n[Illustration]\n\n\n\n\nAround the World in Eighty Days\n\nby Jules Verne\n\n\nConte'
END OF THE PROJECT 369244 'END OF
… [665 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ | head -40 && ls -la data/ 2>/dev/null | head -20 && ls reports/ | head -30", "description": "List tools, data, reports directories"}`

  ```
adaptateur_langue.py
aiguille.py
amplification.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
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
carte_latence.sh
carte-sortie-profondeur.sh
total 159124
drwxr-xr-x. 1 stephane stephane       388 19 oct 12:13 .
drwxr-xr-x. 1 stephane stephane       630 18 oct 22:11 ..
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 corpus_en.txt
-rw-r--r--. 1 stephane stephane   2032162  8 oct 09:42 corpus_en_val.txt
-rw-r--r--. 1 stephane stephane  17031747 17 oct 18:26 corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane   4633889 17 
… [1359 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > explore3.py <<'EOF'\nimport re\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\nfr=open(base+\"around_world_80_days_fr.txt\",encoding='utf-8-sig').read().replace('\\r\\n','\\n')\nen=open(base+\"around_w … [340 caractères tronqués]`

  ```
"Passepartout, un surnom qui m'est resté, et que justifiait mon aptitude\nnaturelle à me tirer d'affaire. Je crois être un honnête garçon,\nmonsieur, mais, pour être franc, j'ai fait plusieurs métiers. J'ai été\nchanteur ambulant, écuyer dans un cirque, faisant de la voltige comme\nLéotard, et dansant sur la corde comme Blondin; puis je suis devenu\nprofesseur de gymnastique, afin de rendre mes talents plus utiles, et,\nen dernier lieu, j'étais sergent de pompiers, à Paris. J'ai même dans\nmon dossier des incendies remarquables. Mais voilà cinq ans que j'ai\nquitté la France et que, voulant goûter de la vie de famille, je suis\nvalet de chambre en Angleterre. Or, me trouvant sans place et ayant\nappris que M. Phileas Fogg était l'homme le plus exact et le plus\nsédentaire du Royaume-Uni, je me suis présenté chez monsieur avec\nl'espérance d'y vivre tranquille et d'oublier jusqu'à ce nom de\nPassepartout...\n\n--Passepartout me convient, répondit le gentleman. Vous m'êtes\nrecommandé. J'ai de bons renseignements sur votre compte. Vous\nconnaissez mes conditions?\n\n--Oui, monsieur.\n\n--Bien. Quelle heure avez-vous?\n\n--Onze heures vingt-deux, répondit Passepartout, en tirant des\n
… [334 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > proto_seg.py <<'EOF'\nimport re, unicodedata, math\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\ndef load(p):\n    s=open(p,encoding='utf-8-sig').read().replace('\\r\\n','\\n')\n    a=s.find(\"START  … [1847 caractères tronqués]`

  ```
FR chapters 37 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
EN chapters 37 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
FR 1 122 title ["DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RÉCIPROQUEMENT L'UN", "COMME MAÎTRE, L'AUTRE COMME DOMESTIQUE"] body "En l'année 1872, la maison portant le numéro 7 de Saville-row,"
FR 2 314 title ["OÙ PASSEPARTOUT EST CONVAINCU QU'IL A ENFIN TROUVE SON IDEAL"] body "«Sur ma foi, se dit Passepartout, un peu ahuri tout d'abord, j'ai conn"
FR 3 454 title ["OÙ S'ENGAGE UNE CONVERSATION QUI POURRA COUTER CHER À PHILEAS FOGG"] body 'Phileas Fogg avait quitté sa maison de Saville-row à onze heures et'
EN 1 54 title ['IN WHICH PHILEAS FOGG AND PASSEPARTOUT ACCEPT EACH OTHER, THE ONE AS', 'MASTER, THE OTHER AS MAN'] body 'Mr. Phileas Fogg lived, in 1872, at No. 7, Saville Row, Burlington'
EN 2 221 title ['IN WHICH PASSEPARTOUT IS CONVINCED THAT HE HAS AT LAST FOUND HIS IDEAL'] body '“Faith,” muttered Passepartout, somewhat flurried, “I’ve seen people a'
EN 3 337 t
… [168 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > proto_split.py <<'EOF'\nimport re, unicodedata, math, json\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\ndef load(p):\n    s=open(p,encoding='utf-8-sig').read().replace('\\r\\n','\\n')\n    a=s.find( … [4891 caractères tronqués]`

  ```
chapters 37 37
sent counts FR/EN per chapter:
  1  107   93  chars  13966  11290
  2   81   53  chars   9354   8284
  3  218  189  chars  20493  16039
  4  153  115  chars   9490   9239
  5   74   49  chars   8401   7050
  6  141  107  chars  14274  10414
  7  111   96  chars   8512   6247
  8  178  154  chars  10198   8989
  9  164  101  chars  16342  11923
 10  114   83  chars  16334  12501
 11  238  175  chars  23956  19372
 12  211  158  chars  19133  16746
 13  228  160  chars  19225  16638
 14  148  105  chars  19185  15485
 15  250  206  chars  18315  17065
 16  148  103  chars  13872  12065
 17  174  126  chars  17847  13971
 18  141  104  chars  13004  10677
 19  279  219  chars  19151  16450
 20  234  184  chars  17128  14722
 21  265  203  chars  22740  19127
 22  163  125  chars  19463  15507
 23  168  161  chars  17751  16125
 24  150  135  chars  17154  15142
 25  194  156  chars  17743  16458
 26  110   90  chars  15620  14063
 27  111   99  chars  19844  17038
 28  280  228  chars  23400  20351
 29  238  197  chars  19983  18349
 30  274  232  chars  18786  16627
 31  164  142  chars  16155  14295
 32  155  130  chars  12182   8458
 33  278  224  chars  22562  20041
… [1212 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > extract_names.py <<'EOF'\nimport re, unicodedata, collections\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\ndef load(p):\n    s=open(p,encoding='utf-8-sig').read().replace('\\r\\n','\\n')\n    a=s.fi … [1002 caractères tronqués]`

  ```
FR top:
 275 Passepartout
 218 Mr
 212 Fix
 211 Phileas Fogg
 155 Fogg
 104 Mrs
  62 Hong-Kong
  59 Bombay
  56 Londres
  43 Yokohama
  36 Reform-Club
  33 Sir Francis Cromarty
  29 Suez
  28 Liverpool
  28 Calcutta
  26 San Francisco
  25 New York
  22 Français
  21 Parsi
  19 Andrew Stuart
  19 Proctor
  17 Saville-row
  17 Compagnie
  15 Anglais
  14 Angleterre
  14 Francis Cromarty
  14 Japon
  14 Sioux
  13 Gauthier Ralph
  13 Indiens
  13 Chine
  13 Pacifique
  13 Shangaï
  13 John Bunsby
  13 Kearney
  12 Singapore
  12 Speedy
  11 Stuart
  11 Indes
  10 Banque
  10 Europe
  10 Brindisi
  10 Pillaji
   9 Banque d'Angleterre
   9 Amérique
   9 Bundelkund
   9 Obadiah
   8 Paris
   8 Royaume-Uni
   8 Allahabad
   8 Bénarès
   8 Gange
   8 Japonais
   8 Omaha
   7 John Sullivan
   7 Thomas Flanagan
   7 Indous
   7 États-Unis
   7 Votre Honneur
   7 Batulcar
   7 Salé
   7 Mudge
   6 Malebar-Hill
   6 Chinois
   6 Sacramento
   6 Platte-river
   6 Smyth
   6 Andrew Speedy
   6 Queenstown
   5 Chronicle_
   5 Baring
   5 Rouge
   5 Aden
   5 Vindhias
   5 Kiouni
   5 Américains
   5 Kamerfield
   5 Mandiboy
   5 Stamp W
   5 Mormons
   5 Bordeaux
   4 Cité
   4 Samuel Fallentin

… [2224 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > count_names.py <<'EOF'\nimport re, unicodedata\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\ndef load(p):\n    s=open(p,encoding='utf-8-sig').read().replace('\\r\\n','\\n')\n    a=s.find(\"START OF T … [1385 caractères tronqués]`

  ```
aouda                FR= 136 EN= 136
passepartout         FR= 451 EN= 424
phileas fogg         FR= 312 EN= 245
fogg                 FR= 685 EN= 646
fix                  FR= 302 EN= 264
cromarty             FR=  47 EN=  13
reform club          FR=  38 EN=  23
saville row          FR=  17 EN=  16
bombay               FR=  61 EN=  61
calcutta             FR=  29 EN=  33
hong kong            FR=  67 EN=  60
yokohama             FR=  44 EN=  41
suez                 FR=  31 EN=  28
liverpool            FR=  31 EN=  28
san francisco        FR=  27 EN=  28
new york             FR=  28 EN=  27
omaha                FR=  22 EN=  24
chicago              FR=   8 EN=   8
londres              FR=  65 EN=   0
london               FR=   3 EN=  72
angleterre           FR=  37 EN=   0
england              FR=   1 EN=  30
inde                 FR=  59 EN=  26
india                FR=   3 EN= 103
chine                FR=  36 EN=  21
china                FR=   7 EN=  16
japon                FR=  36 EN=   0
japan                FR=   0 EN=  38
amerique             FR=  23 EN=   0
america              FR=  43 EN=  54
etats unis           FR=  10 EN=   0
united states        FR=   0 EN=   8
paris           
… [1130 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && cat > proto_align.py <<'EOF'\nimport re, unicodedata, math, time, collections, json\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\n\n# ---------- load & chapter split (reuse) ----------\ndef load(p):\n    s … [10816 caractères tronqués]`

  ```
ratio 0.8498681222869127 sents 6462 5146
align time 8.15522837638855
bead types Counter({(1, 1): 3615, (2, 1): 989, (1, 0): 178, (3, 1): 148, (1, 2): 104, (0, 1): 54, (2, 2): 37, (3, 2): 20, (2, 3): 3, (1, 3): 3})
chap9 beads sample [(0, 1, 0, 0), (1, 3, 0, 1), (3, 4, 1, 1), (4, 5, 1, 2), (5, 6, 2, 3), (6, 8, 3, 4), (8, 9, 4, 4), (9, 10, 4, 4), (10, 11, 4, 5), (11, 12, 5, 5)]
sent with >=1 anchor FR 0.43624264933457135
sent with >=1 anchor EN 0.4811504080839487
baseline {'occ': 3936, 'occ_hit': 3504, 'occ_hit0': 2671, 'pairs': 2540, 'pairs_hit': 2327} recall 0.8902439024390244 exact 0.6786077235772358 pair cov True
  ```

- **bash** `{"command": "cd /tmp && cat > proto_neg.py <<'EOF'\nexec(open('/tmp/proto_align.py').read().split(\"# ---------- anchors ----------\")[0])\nimport random, unicodedata, collections, math\n\n# anchors block (copy)\nsrc=open('/tmp/proto_align.py').read()\nstart=src.index(\"# ---------- anchors -------- … [4633 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-229]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-229", "wait": true, "timeout_ms": 120000}`

  ```
ratio 0.8498681222869127 sents 6462 5146
align time 7.847541809082031
bead types Counter({(1, 1): 3615, (2, 1): 989, (1, 0): 178, (3, 1): 148, (1, 2): 104, (0, 1): 54, (2, 2): 37, (3, 2): 20, (2, 3): 3, (1, 3): 3})
chap9 beads sample [(0, 1, 0, 0), (1, 3, 0, 1), (3, 4, 1, 1), (4, 5, 1, 2), (5, 6, 2, 3), (6, 8, 3, 4), (8, 9, 4, 4), (9, 10, 4, 4), (10, 11, 4, 5), (11, 12, 5, 5)]
sent with >=1 anchor FR 0.43624264933457135
sent with >=1 anchor EN 0.4811504080839487
DF per anchor: [('fogg', 37), ('passepartout', 33), ('fix', 29), ('aouda', 24), ('londres', 22), ('amerique', 19), ('angleterre', 18), ('inde', 18), ('chine', 17), ('bombay', 16), ('hongkong', 14), ('reformclub', 13), ('paris', 12), ('sanfrancisco', 12), ('newyork', 12), ('calcutta', 11), ('suez', 10), ('savillerow', 9), ('pacifique', 9), ('liverpool', 9), ('yokohama', 9), ('japon', 9), ('mongolia', 7), ('allahabad', 6), ('banque', 6), ('atlantique', 6), ('carnatic', 6), ('singapore', 5), ('rangoon', 5), ('omaha', 5), ('brindisi', 4), ('benares', 4), ('cromarty', 4), ('tankadere', 4), ('proctor', 4), ('platte', 4), ('ralph', 3), ('stuart', 3), ('aden', 3), ('merrouge', 3), ('gange', 3), ('kiouni', 3), ('bunsby', 3), ('shang
… [2496 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-229 (bash: cd /tmp && cat > proto_neg.py <<'EOF'
exec(open('/tmp/proto_align.py').read().split("# ---------- anchors ----------")[0])
import random, unicodedata, collections, math

# anchors block (copy)
src=open('/tmp/proto_align.py').read()
start=src.index("# ---------- anchors ----------")
end=src.index("def evaluate(beads_by_ch")
exec(src[start:end])

def evaluate(beads_by_ch, AE_use, radius=2, AF_use=None, only=None):
    AF_use=AF_use or AF
    tot=hit=hit0=pairs=pairs_hit=0
    for n,beads in beads_by_ch.items():
        for (pi,bi,pj,bj) in beads:
            js=range(max(0,pj-radius), min(len(AE_use[n]), bj+radius))
            neigh=set().union(*(AE_use[n][j] for j in js)) if js else set()
            exact=set().union(*(AE_use[n][j] for j in range(pj,bj))) if bj>pj else set()
            for i in range(pi,bi):
                for a in AF_use[n][i]:
                    if only and a not in only: continue
                    tot+=1; hit+= (a in neigh); hit0+= (a in exact)
            fs=set().union(*(AF_use[n][i] for i in range(pi,bi))) if bi>pi else set()
            if only: fs &= only
            if fs:
                pairs+=1; pairs_hit+= bool(fs & neigh)
    return dict(occ=tot,occ_hit=hit,occ_hit0=hit0,pairs=pairs,pairs_hit=pairs_hit)

# chapter DF
df=collections.Counter()
for n in AF:
    present=set().union(*AF[n]) if AF[n] else set()
    for a in present: df[a]+=1
print("DF per anchor:",sorted(df.items(), key=lambda x:-x[1]))
distinct={a for a,c in df.items() if c<=6}
print("distinctive anchors:",len(distinct),sorted(distinct))

res=evaluate(BEADS_ALL,AE)
print("BASE all",res,res['occ_hit']/res['occ'],res['occ_hit0']/res['occ'])
res=evaluate(BEADS_ALL,AE,only=distinct)
print("BASE distinct",res,res['occ_hit']/res['occ'],res['occ_hit0']/res['occ'])

# chapter anchor matrix
def chapter_sets(A):
    return {n:(set().union(*A[n]) if A[n] else set()) for n in A}
CFS=chapter_sets(AF); CES=chapter_sets(AE)
N=37
w={a:math.log((N+1)/(df[a]+0.5)) for a in df}
def sim(a,b):
    num=sum(w[x] for x in a&b if x in w)
    da=math.sqrt(sum(w[x] for x in a if x in w)); db=math.sqrt(sum(w[x] for x in b if x in w))
    return num/(da*db) if da*db else 0
# only shared anchor vocabulary
M=[[sim(CFS[i],CES[j]) for j in range(1,38)] for i in range(1,38)]
ranks=[]
for i in range(37):
    order=sorted(range(37), key=lambda j:-M[i][j])
    rank=order.index(i)+1
    ranks.append(rank)
print("diagonal rank distribution",collections.Counter(ranks))
print("top1",sum(1 for r in ranks if r==1),"top3",sum(1 for r in ranks if r<=3))
for i in [0,1,4,8,9,10,20,30,36]:
    order=sorted(range(37), key=lambda j:-M[i][j])[:5]
    print("ch",i+1,"best",[(j+1,round(M[i][j],3)) for j in order])

# negative A: chapter permutation
random.seed(7)
def derangement(n):
    while True:
        p=list(range(n)); random.shuffle(p)
        if all(p[i]!=i for i in range(n)): return p
perms=[derangement(37) for _ in range(3)]
for pi in perms:
    B={}; mapping={}
    for n in range(1,38):
        en_ch=pi[n-1]+1
        beads,_=align_chapter(SF[n],SE[en_ch])
        B[n]=beads
    # evaluate with AE of permuted chapter: build AE2 keyed by fr chapter
    AE2={n:AE[pi[n-1]+1] for n in range(1,38)}
    res=evaluate(B,AE2)
    print("NEG chap-perm",res['occ_hit']/res['occ'],res['occ_hit0']/res['occ'],res['pairs_hit']/res['pairs'])
    res=evaluate(B,AE2,only=distinct)
    print("   distinct",res['occ_hit']/res['occ'],res['occ_hit0']/res['occ'],res['pairs_hit']/res['pairs'])

# negative B: shuffle sentences within chapter
for seed in (3,4):
    rnd=random.Random(seed); B={}; AE2={}
    for n in range(1,38):
        en2=SE[n][:]; rnd.shuffle(en2)
        beads,_=align_chapter(SF[n],en2)
        B[n]=beads
        # anchors in shuffled order
        AE2[n]=[AE[n][SE[n].index(s)] if False else None for s in en2]
    # rebuild anchor sets properly by sentence identity is messy; recompute
    def anchors_in2(s,side):
        return anchors_in(s,side)
    AE2={n:[anchors_in(s,'en') for s in SE2[n]] for n in range(1,38)} if False else None
    # simpler: reconstruct shuffled sentence lists globally
    SE2={}; rr=random.Random(seed)
    for n in range(1,38):
        s=SE[n][:]; rr.shuffle(s); SE2[n]=s
    AE2={n:[anchors_in(s,'en') for s in SE2[n]] for n in range(1,38)}
    B={n:align_chapter(SF[n],SE2[n])[0] for n in range(1,38)}
    res=evaluate(B,AE2); print("NEG sent-shuffle",res['occ_hit']/res['occ'],res['occ_hit0']/res['occ'],res['pairs_hit']/res['pairs'])
    res=evaluate(B,AE2,only=distinct); print("   distinct",res['occ_hit']/res['occ'],res['occ_hit0']/res['occ'],res['pairs_hit']/res['pairs'])
EOF
CUDA_VISIBLE_DEVICES="" /home/stephane/IA/venv-drave/bin/python proto_neg.py) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /tmp && cat > verify_anchors.py <<'EOF'\nimport re, unicodedata\nbase=\"/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/\"\ndef load(p):\n    s=open(p,encoding='utf-8-sig').read().replace('\\r\\n','\\n')\n    a=s.find(\"START O … [3828 caractères tronqués]`

  ```
phileas fogg             FR=  331 | phileas fogg             EN=  256
fogg                     FR=  685 | fogg                     EN=  646
passepartout             FR=  451 | passepartout             EN=  424
fix                      FR=  284 | fix                      EN=  255
aouda                    FR=  136 | aouda                    EN=  136
cromarty                 FR=   47 | cromarty                 EN=   13
andrew stuart            FR=   22 | andrew stuart            EN=    9
john sullivan            FR=    7 | john sullivan            EN=    5
samuel fallentin         FR=    4 | samuel fallentin         EN=    3
thomas flanagan          FR=    7 | thomas flanagan          EN=    7
gauthier ralph           FR=   13 | gauthier ralph           EN=    4
james forster            FR=    3 | james forster            EN=    3
proctor                  FR=   25 | proctor                  EN=   23
mudge                    FR=    9 | mudge                    EN=    9
bunsby                   FR=   16 | bunsby                   EN=   15
andrew speedy            FR=    6 | andrew speedy            EN=    5
kiouni                   FR=    8 | kiouni                   EN=   12
batulcar  
… [5509 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && grep -o -i \"jejeeh\\|oysterpuf[a-z]*\\|smyth\\|smith\\|lac sal[ée]\\|salt lake\\|sir francis\\|pilgrim\\|great eastern\" around_world_80_days_fr.txt | sort | uniq -c; echo \"- … [239 caractères tronqués]`

  ```
3 Jejeeh
      7 lac Salé
      2 Oysterpuf
      1 Salt Lake
      1 sir Francis
     50 Sir Francis
      1 Smith
      9 Smyth
---- EN ----
      2 Oysterpuff
      2 pilgrim
     10 Salt Lake
     51 Sir Francis
      9 Smith
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -40 tools/bruit_entree.py && echo \"=====\" && head -30 tools/test_contamination.py", "description": "Inspect existing tool style"}`

  ```
#!/usr/bin/env python3
"""bruit_entree.py — LES MARQUEURS VOIENT-ILS LES IMPERFECTIONS DE L'ENTRÉE ?

LE PRINCIPE (AGENTS.md §7). L'entrée (**texte → sens**) est la partie imparfaite : bruit, langues mêlées, accents
perdus, coquilles ✓✗. Si les **marqueurs de bruit** (surprisal par token, langue, longueur ✓) ne **bougent pas**
quand l'entrée est abîmée, l'interface ne peut pas signaler le bruit au module de pensée ✗✗.

CE QU'ON FAIT. On prend des articles propres (UDHR français ✓) et on fabrique quatre versions :
  · **propre** (référence) ;
  · **fautes** : 10 % des caractères remplacés par un caractère voisin ✓ ;
  · **langue mêlée** : 30 % du texte remplacé par l'article anglais correspondant ✓✓ ;
  · **accents perdus** : tous les accents retirés ✓.
On mesure, pour chaque version : **surprisal moyenne par token** ✓, **bits par phrase** ✓, **fraction de tokens
coûteux** ✓, et **langue répondue** ✓. *Si le bruit est vu, la surprisal monte et/ou la langue devient incertaine* ✓✓.

⚠️ CE QUE ÇA NE DIT PAS ✗ : que le modèle **corrige** le bruit ✓✗ — seulement qu'il le **voit** ✓.
"""
from __future__ import annotations
import argparse, json, math, pathlib, random
import numpy as np


d
… [2856 caractères tronqués]
  ```

- **bash** `{"command": "/home/stephane/IA/venv-drave/bin/python -V && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -20", "description": "Check Python version and git status"}`

  ```
Python 3.13.15
  ```

### 🤖 Assistant

The structure and anchor evidence look strong. Now I'll write the production tool with word-boundary-safe anchors, held-out validation, and negative controls.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "content": "#!/usr/bin/env python3\n\"\"\"aligneur_litteraire.py — ALIGNEMENT PHRASE À PHRASE VÉRIFIÉ PAR LES ANCRES.\n\nLE PROBLÈME. La mesure 59 a montré que le banc littéraire « Le Tour du monde en quatr … [75080 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python -m py_compile tools/aligneur_litteraire.py && echo COMPILE_OK && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --json  … [154 caractères tronqués]`

  ```
COMPILE_OK
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1612, in <module>
    raise SystemExit(principal())
                     ~~~~~~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1594, in principal
    donnees = analyser(args)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1362, in analyser
    perles = aligner_livre(phrases_fr, phrases_en, ratio)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 547, in aligner_livre
    for i0, i1, j0, j1 in aligner_chapitre(phrases_fr[numero_fr], phrases_en[numero_en], ratio):
        ^^^^^^^^^^^^^^
ValueError: too many values to unpack (expected 4)
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nfrom pathlib import Path\nfr=A.lire_gutenberg(A.FR_DEFAUT)\nprint(\"corps total cha … [468 caractères tronqués]`

  ```
corps total chars 421445
stats {'langue': 'fr', 'lignes_candidates': 74, 'chapitres_retenus': 37, 'lignes_rejetees': 37, 'numeros': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]}
1 titre= "DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTE" chars= 9775 debut= "En l'année 1872, la maison portant le numéro 7 de Saville-row,\nBurlington Gardens--maison "
2 titre= "OÙ PASSEPARTOUT EST CONVAINCU QU'IL A ENFIN TROUVE" chars= 7817 debut= "«Sur ma foi, se dit Passepartout, un peu ahuri tout d'abord, j'ai connu\nchez Mme Tussaud d"
3 titre= "OÙ S'ENGAGE UNE CONVERSATION QUI POURRA COUTER CHE" chars= 13485 debut= 'Phileas Fogg avait quitté sa maison de Saville-row à onze heures et\ndemie, et, après avoir'
4 titre= 'DANS LEQUEL PHILEAS FOGG STUPEFIE PASSEPARTOUT, SO' chars= 6304 debut= 'À sept heures vingt-cinq, Phileas Fogg, après avoir gagné une vingtaine\nde guinées au whis'
5 titre= 'DANS LEQUEL UNE NOUVELLE VALEUR APPARAÎT SUR LA PL' chars= 6445 debut= 'Phileas Fogg, en quittant Londres, ne se doutait guère, sans doute, du\ngrand retentissemen'
somme chars 415023
EN total chars 369188
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "old_string": "        numero_en = appariement[numero_fr] if appariement else numero_fr\n        for i0, i1, j0, j1 in aligner_chapitre(phrases_fr[numero_fr], phrases_en[numero_en], ratio):", "new_string":  … [223 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --json /tmp/verne_test.json --rapport /tmp/verne_test.md --sans-controles", "description": "Run tool without negative controls", "timeoutM … [11 caractères tronqués]`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.8 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.913 / distinctives 0.888 ; matrice diagonale top-1 37/37
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1613, in <module>
    raise SystemExit(principal())
                     ~~~~~~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1601, in principal
    rediger_rapport(donnees, args.rapport)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1104, in rediger_rapport
    d = anc["distinctives"]["fr"]
        ~~~~~~~~~~~~~~~~~~~^^^^^^
TypeError: list indices must be integers or slices, not str
[exit code: 1]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "            \"df_fr\": dict(sorted(df_fr.items(), key=lambda x: -x[1])),\n            \"df_en\": dict(sorted(df_en.items(), key=lambda x: -x[1])),\n            \"liste_distinctives\": sorted( … [233 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --json /tmp/verne_test.json --rapport /tmp/verne_test.md --sans-controles", "description": "Re-run tool without negative controls", "timeo … [14 caractères tronqués]`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.8 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.913 / distinctives 0.888 ; matrice diagonale top-1 37/37
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1613, in <module>
    raise SystemExit(principal())
                     ~~~~~~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1601, in principal
    rediger_rapport(donnees, args.rapport)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", line 1263, in rediger_rapport
    f"{_p(neg['chapitres_permutes'][0]['distinctives']['rappel'][r])}, contre "
          ~~~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"neg_moyen\\|neg\\['chapitres_permutes'\\]\\[0\\]\\|hasard_intra\" tools/aligneur_litteraire.py | head -30", "description": "Locate negative-control report code"}`

  ```
739:def controler_hasard_intra_chapitre(
1191:    ha = neg["hasard_intra_chapitre"]
1263:        f"{_p(neg['chapitres_permutes'][0]['distinctives']['rappel'][r])}, contre "
1401:            "hasard_intra_chapitre": {"tirages": 0, "touchees": 0, "taux": 0.0},
1430:        hasard = controler_hasard_intra_chapitre(ancres_fr, ancres_en, rng)
1435:            "hasard_intra_chapitre": hasard,
1472:        neg_moyen = sum(b["distinctives"]["rappel"][str(args.rayon)] for b in neg["chapitres_permutes"]) / len(
1476:        neg_moyen = 0.0
1477:    facteur = (rappel_reel / neg_moyen) if neg_moyen > 0 else float("inf")
1492:            neg_moyen <= args.seuil_controle,
1493:            f"{neg_moyen:.1%} à ±{args.rayon} (seuil {args.seuil_controle:.0%})",
1504:            f"{neg_moyen:.1%} quand les chapitres sont permutés (×{facteur:.0f}) ; les 37 chapitres se "
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1185,1200p;1255,1270p;1465,1510p' tools/aligneur_litteraire.py", "description": "Show code to patch"}`

  ```
"distinctives à distance 0",
            "note",
        ],
        lignes,
    )
    L.append("")
    ha = neg["hasard_intra_chapitre"]
    L.append(
        f"**Hasard pur, phrase contre phrase dans le même chapitre** : {_i(ha['tirages'])} tirages, "
        f"**{_p(ha['taux'], 2)}** de rencontres d'ancres. C'est le plancher absolu : même sans aucun ordre, "
        "deux phrases d'un même chapitre partagent parfois un nom. L'alignement réel fait "
        f"**{_p(d['rappel']['0'], 2)}** à distance 0 sur les ancres distinctives, soit "
        f"**×{_f(d['rappel']['0'] / ha['taux'], 1) if ha['taux'] else '∞'}** ce plancher."
    )
    L.append("")
    L.append("### 3.5 Matrice chapitres × chapitres (contrôle structurel)")
        "favoriser les noms à orthographe stable et sous-représenter les lieux que le traducteur a vraiment "
        "traduits (`Royaume-Uni` → `United Kingdom`, une seule occurrence anglaise, a été écarté). Il reste "
        "indépendant de l'alignement, mais pas indépendant du choix des textes."
    )
    L.append(
        "4. **Le contrôle négatif « chapitres permutés » n'est pas un hasard parfait** : les chapitres voisins "
        "partagent des personnag
… [2902 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    L.append(\"\")\n    ha = neg[\"hasard_intra_chapitre\"]\n    if ha[\"tirages\"]:\n        L.append(\n            f\"**Hasard pur, phrase contre phrase dans le même chapitre** : {_i(ha['ti … [1086 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    L.append(\n        \"4. **Le contrôle négatif « chapitres permutés » n'est pas un hasard parfait** : les chapitres voisins \"\n        \"partagent des personnages, et l'anglais d'un chapi … [958 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    # --- verdict ---\n    rappel_reel = distinct_fr[\"rappel\"][str(args.rayon)]\n    if neg[\"chapitres_permutes\"]:\n        neg_moyen = sum(b[\"distinctives\"][\"rappel\"][str(args.rayon) … [3102 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python -m py_compile tools/aligneur_litteraire.py && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --json /tmp/verne_test.jso … [116 caractères tronqués]`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 3.0 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.913 / distinctives 0.888 ; matrice diagonale top-1 37/37
[6/7] contrôles négatifs (3 répétitions)…
      contrôles en 20.7 s
[7/7] écrit : /tmp/verne_test.json (3397 paires) et /tmp/verne_test.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 88.8% à ±2, contre 0.3% quand les chapitres sont permutés (×281) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
  ```

- **read** `{"file_path": "/tmp/verne_test.md"}`

  ```
<path>/tmp/verne_test.md</path>
<type>file</type>
<content>
1: # Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais)
2: 
3: **Date** : 2026-10-19 18:25 UTC  
4: **Outil** : `tools/aligneur_litteraire.py` (CPU, bibliothèque standard, aucun modèle)  
5: **Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 88.8% à ±2, contre 0.3% quand les chapitres sont permutés (×281) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
6: 
7: ## 1. La question
8: 
9: La mesure 59 a établi que le banc littéraire était **invalide** : trois découpages successifs (titres, grille proportionnelle, corps) donnaient 84, 60 puis 37 sections françaises contre 37 anglaises, et le chrF restait au niveau du hasard. Le problème n'était pas le modèle mais l'**appariement** : les segments comparés ne disaient pas la même chose. Ce sous-chantier construit donc un alignement **phrase à phrase** et, surtout, le **vérifie** avec des ancres indépendantes — sans quoi un alignement « plausible » ne serait qu'une hypothèse de plus.
10: 
11: ## 2. Le dispositif
12: 
13: ### 2.1 Les textes
14: 
15: | | français | anglais |
16: |---|---:|---:|
17
… [12134 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && ls -lh verne_test.json && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport json, random\nd=json.load(open('/tmp/verne_test.json'))\nprint(\"keys\",list(d.keys()))\nprint(\"meta\",{k:v for k,v in d['meta'].items() if k!='ancres'})\nprint(\"ancres\",len(d['meta']['ancr … [1046 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 1,3M 19 oct 14:25 verne_test.json
keys ['meta', 'structure', 'chapitres', 'paires', 'non_appariees', 'validation']
meta {'titre': 'Le Tour du monde en quatre-vingts jours — alignement FR → EN', 'date': '2026-10-19 18:25 UTC', 'outil': 'tools/aligneur_litteraire.py', 'version': '1.0', 'fichiers': {'fr': '/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt', 'en': '/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_en.txt'}, 'graine': 20260227, 'repetitions': 3, 'rayon': 2, 'seuil_distinctif': 6, 'duree_s': 24.94876790046692, 'ratio_global': 0.874618613147623, 'indices': '0-based', 'unite': 'perle Gale-Church (1..3 phrases par côté)'}
ancres 82
paires 3397 non_app 59 8
chapitres 37
premier chapitre {'numero': 1, 'titre_fr': "DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RÉCIPROQUEMENT L'UN COMME MAÎTRE, L'AUTRE COMME DOMESTIQUE", 'titre_en': 'IN WHICH PHILEAS FOGG AND PASSEPARTOUT ACCEPT EACH OTHER, THE ONE AS MASTER, THE OTHER AS MAN', 'n_fr': 76, 'n_en': 69, 'caracteres_fr': 9667, 'caracter
… [4959 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nlignes=A.lire_gutenberg(A.FR_DEFAUT).split(\"\\n\")\nch,st=A.reperer_chapitre … [884 caractères tronqués]`

  ```
FR 76 EN 69
FR00 L= 335 En l'année 1872, la maison portant le numéro 7 de Saville-row, Burlington Gardens--maison dans laquelle Sheridan mourut 
FR01 L= 240 À l'un des plus grands orateurs qui honorent l'Angleterre, succédait donc ce Phileas Fogg, personnage énigmatique, dont 
FR02 L= 198 On disait qu'il ressemblait à Byron--par la tête, car il était irréprochable quant aux pieds--, mais un Byron à moustach
FR03 L=  66 Anglais, à coup sûr, Phileas Fogg n'était peut-être pas Londonner.
FR04 L=  95 On ne l'avait jamais vu ni à la Bourse, ni à la Banque, ni dans aucun des comptoirs de la Cité.
FR05 L= 104 Ni les bassins ni les docks de Londres n'avaient jamais reçu un navire ayant pour armateur Phileas Fogg.
FR06 L=  60 Ce gentleman ne figurait dans aucun comité d'administration.
FR07 L= 108 Son nom n'avait jamais retenti dans un collège d'avocats, ni au Temple, ni à Lincoln's-inn, ni à Gray's-inn.

EN00 L= 117 Mr. Phileas Fogg lived, in 1872, at No. 7, Saville Row, Burlington Gardens, the house in which Sheridan died in 1814.
EN01 L= 219 He was one of the most noticeable members of the Reform Club, though he seemed always to avoid attracting attention; an 
EN02 L= 165 People said tha
… [2868 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, json, statistics\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nd=json.load(open('/tmp/verne_test.json'))\n# per-chapter anchor r … [1904 caractères tronqués]`

  ```
ch  occ  exact  pm2   perles
  1    5  0.80  1.00  63
  2    0  0.00  0.00  42
  3   52  0.83  0.90  116
  4    4  0.75  1.00  70
  5    0  0.00  0.00  38
  6    6  1.00  1.00  69
  7    3  1.00  1.00  54
  8    1  1.00  1.00  93
  9   10  0.50  0.70  72
 10   11  0.82  1.00  58
 11   51  0.67  0.84  122
 12   41  0.68  0.71  106
 13   32  0.59  0.59  111
 14   35  0.60  0.77  75
 15   20  0.65  0.75  116
 16   14  0.71  0.79  76
 17   13  0.62  0.92  87
 18   11  0.82  0.82  72
 19    5  0.80  1.00  141
 20   24  0.92  1.00  112
 21   34  0.82  0.97  144
 22   10  0.90  0.90  88
 23   13  0.77  0.92  93
 24   17  0.94  0.94  90
 25   13  0.92  1.00  105
 26   14  1.00  1.00  61
 27   22  0.95  1.00  68
 28   23  0.87  0.96  143
 29   18  0.94  0.94  127
 30   11  1.00  1.00  158
 31   30  0.97  0.97  102
 32   15  0.93  1.00  78
 33   40  0.90  0.93  156
 34    0  0.00  0.00  61
 35    2  1.00  1.00  101
 36   22  1.00  1.00  63
 37    0  0.00  0.00  66

FR longest:
792 27 23 En ce moment, quelques auditeurs, peu intéressés par le récit rétrospectif du missionnaire, quittèrent le wagon; mais William Hitch, continuant, raconta «comment Smyth junior, réun
685 14 98 À peine les voyag
… [2908 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nd=json.load(open('/tmp/verne_test.json'))\nlignes=A.lire_gutenberg(A.FR_DEFAU … [1857 caractères tronqués]`

  ```
ch FR_chars EN_chars ratio  FR_s EN_s
  1    9667    8267  0.86   76   69
  2    7735    6501  0.84   66   43
  3   13133   11490  0.87  132  130
  4    6152    5490  0.89   97   71
  5    6319    5398  0.85   56   38
  6    8991    7442  0.83   86   71
  7    4859    4275  0.88   64   61
  8    6270    5903  0.94  102   96
  9   11112    9007  0.81  115   73
 10   10339    9141  0.88   73   61
 11   16989   15004  0.88  164  126
 12   13345   12251  0.92  138  109
 13   13100   11459  0.87  158  112
 14   13087   11283  0.86  106   77
 15   11662   10605  0.91  140  119
 16   10662    9153  0.86  110   78
 17   12650   10004  0.79  118   89
 18    9064    7716  0.85   99   72
 19   13725   11740  0.86  166  148
 20   11108    9808  0.88  141  115
 21   16457   14168  0.86  188  147
 22   13421   12013  0.90  113   93
 23   12248   11171  0.91  106  104
 24   11725   11172  0.95  104   96
 25   12867   11516  0.90  137  106
 26   11410    9473  0.83   83   65
 27   12833   11511  0.90   76   71
 28   16140   14108  0.87  174  150
 29   13635   12187  0.89  153  128
 30   13588   12032  0.89  186  162
 31   11976   10290  0.86  122  106
 32    7417    5901  0.80   92   82
 33   1575
… [18574 caractères tronqués]
  ```

### 🤖 Assistant

The diagnostics show one dictionary artifact: French says "Sir Francis Cromarty", English often just "Sir Francis", so they must be one anchor. I'll merge them and add the "Reform" short form.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport re\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\nold='''    (\"cromarty\", (\"cromarty\",), (\"cromarty\",), False),\n    (\"sir_francis\", (\"sir fran … [1023 caractères tronqués]`

  ```
ok
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.9 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.927 / distinctives 0.932 ; matrice diagonale top-1 37/37
[7/7] écrit : /tmp/verne_test2.json (3397 paires) et /tmp/verne_test2.md
      VERDICT : NON VALIDE — critères non réunis : contrôle négatif (chapitres permutés), facteur au-dessus du hasard.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nd=json.load(open('/tmp/verne_test2.json'))\nlignes=A.lire_gutenberg(A.FR_DEFA … [1543 caractères tronqués]`

  ```
ch  occ  exact  pm2
  1    5  0.80  1.00
  2    0  0.00  0.00
  3   52  0.83  0.90
  4    4  0.75  1.00
  5    0  0.00  0.00
  6    6  1.00  1.00
  7    3  1.00  1.00
  8    1  1.00  1.00
  9   10  0.50  0.70
 10   11  0.82  1.00
 11   34  0.82  0.97
 12   30  0.87  0.90
 13   19  0.89  0.89
 14   29  0.66  0.86
 15   20  0.65  0.75
 16   14  0.71  0.79
 17   13  0.62  0.92
 18   11  0.82  0.82
 19    5  0.80  1.00
 20   24  0.92  1.00
 21   34  0.82  0.97
 22   10  0.90  0.90
 23   13  0.77  0.92
 24   17  0.94  0.94
 25   13  0.92  1.00
 26   14  1.00  1.00
 27   22  0.95  1.00
 28   23  0.87  0.96
 29   18  0.94  0.94
 30   11  1.00  1.00
 31   30  0.97  0.97
 32   15  0.93  1.00
 33   40  0.90  0.93
 34    0  0.00  0.00
 35    2  1.00  1.00
 36   22  1.00  1.00
 37    0  0.00  0.00

per-anchor distinctive (occ>=5):
cromarty       occ=  53 exact=0.81
stuart         occ=  31 exact=0.87
rangoon        occ=  31 exact=0.61
carnatic       occ=  29 exact=0.86
proctor        occ=  24 exact=0.88
henrietta      occ=  24 exact=0.88
omaha          occ=  21 exact=0.95
tankadere      occ=  20 exact=0.85
allahabad      occ=  18 exact=0.78
speedy         occ=  18 exact=0.94
ralph          occ=
… [2309 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nd=json.load(open('/tmp/verne_test2.json'))\nlignes=A.lire_gutenberg(A.FR_DEFA … [1572 caractères tronqués]`

  ```
all: total 2641 exact 2178 present ailleurs 432 absent chapitre 31
dist: total 575 exact 491 present ailleurs 80 absent chapitre 4
exemples absents: [(1, 40, 'amerique', "S'il dînait ou déjeunait, c'étaient les cuisines, le garde-manger, l'office, la "), (3, 0, 'savillerow', 'Phileas Fogg avait quitté sa maison de Saville-row à onze heures et demie, et, a'), (3, 68, 'chine', 'De Calcutta à Hong-Kong (Chine), paquebot: 13 jours.'), (5, 32, 'paris', 'Aussi, non seulement les divers membres du Reform-Club établirent-ils des paris '), (6, 9, 'banque', "Cet homme se nommait Fix, et c'était un de ces «détectives» ou agents de police "), (7, 59, 'liverpool', 'Mr. Fogg inscrivit ces dates sur un itinéraire disposé par colonnes, qui indiqua'), (9, 110, 'salcette', 'Le paquebot pénétra dans cette rade formée par les îles Salcette, Colaba, Élépha'), (11, 4, 'suez', "C'était le brigadier général, Sir Francis Cromarty, l'un des partenaires de Mr. "), (14, 41, 'bundelkund', 'Mais, sans toute cette amplification, il suffit de dire que Mrs. Aouda, la veuve'), (15, 89, 'inde', "Que l'on juge du désappointement de Fix, quand il apprit que Phileas Fogg n'étai")]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '640,730p' tools/aligneur_litteraire.py", "description": "Show evaluer_ancres block"}`

  ```
"par_ancre": dict(par_ancre),
    }


def compter_df(ancres: dict[int, list[set[str]]]) -> Counter:
    """Document frequency : dans combien de chapitres chaque ancre apparaît."""
    df: Counter = Counter()
    for numero in ancres:
        for ident in set().union(*ancres[numero]) if ancres[numero] else set():
            df[ident] += 1
    return df


# ---------------------------------------------------------------------------
# Contrôles négatifs
# ---------------------------------------------------------------------------
def derangement(n: int, rng: random.Random) -> list[int]:
    """Permutation sans point fixe (chaque chapitre FR va vers un autre chapitre EN)."""
    while True:
        permutation = list(range(n))
        rng.shuffle(permutation)
        if all(permutation[i] != i for i in range(n)):
            return permutation


def controler_chapitres_permutes(
    phrases_fr: dict[int, list[str]],
    phrases_en: dict[int, list[str]],
    ratio: float,
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    distinctives: set[str],
    rng: random.Random,
    repetitions: int,
    rayon: int,
) -> list[dict]:
    numeros = sorted(phras
… [2134 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '580,645p' tools/aligneur_litteraire.py", "description": "Show par_ancre section"}`

  ```
rayon: int = 2,
    seulement: set[str] | None = None,
    sens: str = "fr",
) -> dict:
    """Rappel des ancres : une occurrence d'un côté doit se retrouver de l'autre, à distance 0..rayon.

    `sens="fr"` : on part des occurrences françaises et on cherche dans la perle anglaise.
    `sens="en"` : l'inverse.
    """
    distances = (0, 1, rayon, 5)
    occurrences = 0
    touchees = {d: 0 for d in distances}
    perles_avec_ancre = 0
    perles_touchees = {d: 0 for d in distances}
    par_ancre: dict[str, dict[str, int]] = defaultdict(lambda: {"occurrences": 0, "touchees_2": 0})

    for perle in perles:
        if sens == "fr":
            ch_source, ch_cible = perle["chapitre_fr"], perle["chapitre_en"]
            i0, i1 = perle["i_fr"], perle["i_fr"] + perle["n_fr"]
            j0, j1 = perle["i_en"], perle["i_en"] + perle["n_en"]
            source = ancres_fr
            cible = ancres_en
        else:
            ch_source, ch_cible = perle["chapitre_en"], perle["chapitre_fr"]
            i0, i1 = perle["i_en"], perle["i_en"] + perle["n_en"]
            j0, j1 = perle["i_fr"], perle["i_fr"] + perle["n_fr"]
            source = ancres_en
            cible = ancres_fr

      
… [1425 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    par_ancre: dict[str, dict[str, int]] = defaultdict(\n        lambda: {\"occurrences\": 0, \"touchees_0\": 0, \"touchees_rayon\": 0}\n    )", "old_string": "    par_ancre: dict[str, dict[s … [74 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "offset": 575, "limit": 75}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
575: 
576: def evaluer_ancres(
577:     perles: list[dict],
578:     ancres_fr: dict[int, list[set[str]]],
579:     ancres_en: dict[int, list[set[str]]],
580:     rayon: int = 2,
581:     seulement: set[str] | None = None,
582:     sens: str = "fr",
583: ) -> dict:
584:     """Rappel des ancres : une occurrence d'un côté doit se retrouver de l'autre, à distance 0..rayon.
585: 
586:     `sens="fr"` : on part des occurrences françaises et on cherche dans la perle anglaise.
587:     `sens="en"` : l'inverse.
588:     """
589:     distances = (0, 1, rayon, 5)
590:     occurrences = 0
591:     touchees = {d: 0 for d in distances}
592:     perles_avec_ancre = 0
593:     perles_touchees = {d: 0 for d in distances}
594:     par_ancre: dict[str, dict[str, int]] = defaultdict(lambda: {"occurrences": 0, "touchees_2": 0})
595: 
596:     for perle in perles:
597:         if sens == "fr":
598:             ch_source, ch_cible = perle["chapitre_fr"], perle["chapitre_en"]
599:             i0, i1 = perle["i_fr"], perle["i_fr"] + perle["n_fr"]
600:             j0, j1 = perle["i_en"], p
… [2285 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    par_ancre: dict[str, dict[str, int]] = defaultdict(\n        lambda: {\"occurrences\": 0, \"touchees_0\": 0, \"touchees_rayon\": 0}\n    )", "old_string": "    par_ancre: dict[str, dict[s … [74 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "            if ident in fenetres[0]:\n                par_ancre[ident][\"touchees_0\"] += 1\n            if ident in fenetres[rayon]:\n                par_ancre[ident][\"touchees_rayon\"] +=  … [112 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "        \"par_ancre\": dict(par_ancre),\n    }\n\n\ndef classer_manques(\n    perles: list[dict],\n    ancres_fr: dict[int, list[set[str]]],\n    ancres_en: dict[int, list[set[str]]],\n    se … [2112 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "limit": 80, "offset": 1390}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
1390: 
1391:     print(f"[2/7] repérage des chapitres (filtre par longueur)…", flush=True)
1392:     chapitres_fr, stats_fr = reperer_chapitres(lignes_fr, "fr")
1393:     chapitres_en, stats_en = reperer_chapitres(lignes_en, "en")
1394:     verifier_structure(chapitres_fr, chapitres_en, stats_fr, stats_en)
1395:     print(
1396:         f"      FR {stats_fr['lignes_candidates']} candidates → {stats_fr['chapitres_retenus']} chapitres ; "
1397:         f"EN {stats_en['lignes_candidates']} → {stats_en['chapitres_retenus']}",
1398:         flush=True,
1399:     )
1400: 
1401:     corps_fr = corps_des_chapitres(lignes_fr, chapitres_fr)
1402:     corps_en = corps_des_chapitres(lignes_en, chapitres_en)
1403: 
1404:     print(f"[3/7] découpage en phrases…", flush=True)
1405:     phrases_fr = {n: phrases_du_chapitre(corps_fr[n], "fr") for n in corps_fr}
1406:     phrases_en = {n: phrases_du_chapitre(corps_en[n], "en") for n in corps_en}
1407:     caracteres_fr = sum(len(p) for s in phrases_fr.values() for p in s)
1408:     caracteres_en = sum(len(p) for s in phrases_en.value
… [3005 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"validation = {\" -A 40 tools/aligneur_litteraire.py | head -60", "description": "Show validation dict construction"}`

  ```
1582:    validation = {
1583-        "ancres": {
1584-            "global": {"fr": global_fr, "en": global_en},
1585-            "distinctives": {"fr": distinct_fr, "en": distinct_en},
1586-            "df_fr": dict(sorted(df_fr.items(), key=lambda x: -x[1])),
1587-            "df_en": dict(sorted(df_en.items(), key=lambda x: -x[1])),
1588-            "liste_distinctives": sorted(distinctives),
1589-            "seuil_distinctif": args.seuil_distinctif,
1590-        },
1591-        "controles_negatifs": neg,
1592-        "matrice_chapitres": matrice,
1593-        "rapports_longueur": longueurs,
1594-        "alignement": alignement,
1595-        "verdict": verdict,
1596-        "hypothese": {
1597-            "appariement": "Gale-Church par chapitre, longueurs en caractères, ratio global",
1598-            "ancres": "indépendantes de l'appariement ; utilisées seulement pour juger",
1599-        },
1600-    }
1601-
1602-    meta = {
1603-        "titre": "Le Tour du monde en quatre-vingts jours — alignement FR → EN",
1604-        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
1605-        "outil": "tools/aligneur_litteraire.py",
1606-        "version": "1.0",
160
… [541 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    distinct_en = evaluer_ancres(\n        perles, ancres_fr, ancres_en, rayon=args.rayon, sens=\"en\", seulement=distinctives\n    )\n    manques_global = classer_manques(perles, ancres_fr,  … [475 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    matrice = matrice_ancres(ancres_fr, ancres_en, df_fr)\n    longueurs = statistiques_longueurs(perles)\n    par_chapitre = {}\n    for numero in sorted(phrases_fr):\n        sous = [p for  … [531 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "            \"df_fr\": dict(sorted(df_fr.items(), key=lambda x: -x[1])),\n            \"df_en\": dict(sorted(df_en.items(), key=lambda x: -x[1])),\n            \"liste_distinctives\": sorted( … [516 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "limit": 70, "offset": 1535}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
1535:     }
1536: 
1537:     # --- verdict ---
1538:     rappel_reel = distinct_fr["rappel"][str(args.rayon)]
1539:     if neg["chapitres_permutes"]:
1540:         neg_moyen = sum(b["distinctives"]["rappel"][str(args.rayon)] for b in neg["chapitres_permutes"]) / len(
1541:             neg["chapitres_permutes"]
1542:         )
1543:     else:
1544:         neg_moyen = None
1545:     facteur = (rappel_reel / neg_moyen) if (neg_moyen is not None and neg_moyen > 0) else (
1546:         float("inf") if neg_moyen == 0 else None
1547:     )
1548:     criteres = {
1549:         "structure 37 / 37": (
1550:             stats_fr["chapitres_retenus"] == 37 and stats_en["chapitres_retenus"] == 37,
1551:             f"{stats_fr['chapitres_retenus']} chapitres FR et {stats_en['chapitres_retenus']} EN, numéros identiques",
1552:         ),
1553:         "matrice des chapitres (diagonale n° 1)": (
1554:             matrice["diagonale_top1"] == matrice["n"],
1555:             f"{matrice['diagonale_top1']} / {matrice['n']} chapitres ont leur homologue en première position",
1556:    
… [2471 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "        \"rappel des ancres distinctives\": (\n            rappel_reel >= args.seuil_rappel,\n            f\"{_p(rappel_reel)} à ±{args.rayon} (seuil {_p(args.seuil_rappel)})\",\n        ),\n … [905 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    if valide:\n        resume = (\n            f\"les ancres distinctives se retrouvent à {_p(rappel_reel)} à ±{args.rayon}, contre \"\n            f\"{_p(neg_moyen)} quand les chapitres son … [485 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "limit": 120, "offset": 1000}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
1000:     meta = donnees["meta"]
1001:     st = donnees["structure"]
1002:     v = donnees["validation"]
1003:     anc = v["ancres"]
1004:     neg = v["controles_negatifs"]
1005:     mc = v["matrice_chapitres"]
1006:     lg = v["rapports_longueur"]
1007:     verdict = v["verdict"]
1008:     align = v["alignement"]
1009:     hypo = v["hypothese"]
1010: 
1011:     L: list[str] = []
1012:     L.append("# Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais)")
1013:     L.append("")
1014:     L.append(f"**Date** : {meta['date']}  ")
1015:     L.append(f"**Outil** : `tools/aligneur_litteraire.py` (CPU, bibliothèque standard, aucun modèle)  ")
1016:     L.append(
1017:         "**Verdict** : **"
1018:         + ("VALIDE" if verdict["valide"] else "NON VALIDE")
1019:         + "** — "
1020:         + verdict["resume"]
1021:     )
1022:     L.append("")
1023:     L.append("## 1. La question")
1024:     L.append("")
1025:     L.append(
1026:         "La mesure 59 a établi que le banc littéraire était **invalide** : trois découpages succe
… [5910 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('    align = v[\"alignement\"]\\n    hypo = v[\"hypothese\"]\\n', '    align = v[\"alignement\"]\\n') … [952 caractères tronqués]`

  ```
ok
1041:    L.append(f"| caractères des phrases | {_i(align['caracteres_fr'])} | {_i(align['caracteres_en'])} |")
1045:        f"Le rapport global de longueur est **{_f(align['ratio'], 3)} caractère anglais par caractère français** ; "
1115:    L.append(f"| caractères des phrases | {_i(align['caracteres_fr'])} | {_i(align['caracteres_en'])} |")
1116:    L.append(f"| rapport global EN/FR | | {_f(align['ratio'], 3)} |")
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "limit": 115, "offset": 1119}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
1119:     L.append("")
1120:     L.append(
1121:         f"**{_i(align['perles_appariees'])} perles appariées** (les deux côtés non vides) sur "
1122:         f"{_i(align['perles_total'])} perles ; {_i(align['paires_1_1'])} sont des paires 1:1 strictes."
1123:     )
1124:     L.append("")
1125:     types = align["types_perles"]
1126:     lignes_types = [[f"{di}:{dj}", _i(n)] for (di, dj), n in types]
1127:     L += _tableau(["type de perle", "nombre"], lignes_types)
1128:     L.append("")
1129:     L.append("| couverture | français | anglais |")
1130:     L.append("|---|---:|---:|")
1131:     L.append(
1132:         f"| phrases dans une perle appariée | {_i(align['phrases_fr_couvertes'])} "
1133:         f"({_p(align['phrases_fr_couvertes'] / align['phrases_fr'])}) | "
1134:         f"{_i(align['phrases_en_couvertes'])} ({_p(align['phrases_en_couvertes'] / align['phrases_en'])}) |"
1135:     )
1136:     L.append(
1137:         f"| phrases non appariées | {_i(align['non_appariees_fr'])} "
1138:         f"({_p(align['non_appariees_fr'] / align['phrases_fr'])}) | "
113
… [4806 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "limit": 55, "offset": 1228}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py</path>
<type>file</type>
<content>
1228:     L += _tableau(
1229:         [
1230:             f"contrôle (rappel ±{meta['rayon']})",
1231:             "toutes ancres",
1232:             "distinctives",
1233:             "distinctives à distance 0",
1234:             "note",
1235:         ],
1236:         lignes,
1237:     )
1238:     L.append("")
1239:     ha = neg["hasard_intra_chapitre"]
1240:     if ha["tirages"]:
1241:         L.append(
1242:             f"**Hasard pur, phrase contre phrase dans le même chapitre** : {_i(ha['tirages'])} tirages, "
1243:             f"**{_p(ha['taux'], 2)}** de rencontres d'ancres. C'est le plancher absolu : même sans aucun ordre, "
1244:             "deux phrases d'un même chapitre partagent parfois un nom. L'alignement réel fait "
1245:             f"**{_p(d['rappel']['0'], 2)}** à distance 0 sur les ancres distinctives, soit "
1246:             f"**×{_f(d['rappel']['0'] / ha['taux'], 1) if ha['taux'] else '∞'}** ce plancher."
1247:         )
1248:         L.append("")
1249:     L.append("### 3.5 Matrice chapitres × chapitres (contrôle structurel)")
1250:     L.a
… [2246 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    L += _tableau([\"mesure (sens EN → FR)\", \"toutes ancres\", \"ancres distinctives\"], lignes)\n    L.append(\"\")\n    # --- où vont les ancres manquées ? (diagnostic) ---\n    mg = anc[ … [3806 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "    def _neg_ligne(nom: str, bloc: dict) -> list[str]:\n        return [\n            nom,\n            _p(bloc[\"global\"][\"rappel\"][r]),\n            _p(bloc[\"distinctives\"][\"rappel\"] … [2003 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Hasard pur\" -A 8 tools/aligneur_litteraire.py", "description": "Locate hasard paragraph"}`

  ```
1300:            f"**Hasard pur, phrase contre phrase dans le même chapitre** : {_i(ha['tirages'])} tirages, "
1301-            f"**{_p(ha['taux'], 2)}** de rencontres d'ancres. C'est le plancher absolu : même sans aucun ordre, "
1302-            "deux phrases d'un même chapitre partagent parfois un nom. L'alignement réel fait "
1303-            f"**{_p(d['rappel']['0'], 2)}** à distance 0 sur les ancres distinctives, soit "
1304-            f"**×{_f(d['rappel']['0'] / ha['taux'], 1) if ha['taux'] else '∞'}** ce plancher."
1305-        )
1306-        L.append("")
1307-    L.append("### 3.5 Matrice chapitres × chapitres (contrôle structurel)")
1308-    L.append("")
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py", "new_string": "            f\"**Hasard pur, phrase contre phrase dans le même chapitre** : {_i(ha['tirages'])} tirages, \"\n            f\"**{_p(ha['taux'], 2)}** de rencontres d'ancres. C'est un plancher * … [1300 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python -m py_compile tools/aligneur_litteraire.py && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --json /tmp/verne_test3.js … [125 caractères tronqués]`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.9 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.927 / distinctives 0.932 ; matrice diagonale top-1 37/37
[7/7] écrit : /tmp/verne_test3.json (3397 paires) et /tmp/verne_test3.md
      VERDICT : NON VALIDE — critères non réunis : contrôle négatif (chapitres permutés), facteur au-dessus du hasard.
  ```

- **read** `{"file_path": "/tmp/verne_test3.md", "limit": 100, "offset": 80}`

  ```
<path>/tmp/verne_test3.md</path>
<type>file</type>
<content>
80: Une **occurrence** est un couple (phrase, ancre). Le rappel à distance *d* est la fraction des occurrences françaises dont l'ancre se retrouve dans la perle anglaise (d = 0) ou dans son voisinage ±*d*. C'est la mesure la plus directe : *si l'alignement est bon, le nom propre doit être là où le français le met*.
81: 
82: | mesure (sens FR → EN) | toutes ancres | ancres distinctives |
83: |---|---:|---:|
84: | occurrences | 2 686 | 587 |
85: | rappel à distance 0 | 81,1 % | 83,6 % |
86: | rappel ±1 | 90,2 % | 91,3 % |
87: | rappel ±2 | 92,7 % | 93,2 % |
88: | rappel ±5 | 95,6 % | 96,1 % |
89: | perles avec ancre | 1 781 | 500 |
90: | perles partageant une ancre (distance 0) | 84,7 % | 83,0 % |
91: | perles partageant une ancre (±2) | 94,8 % | 92,8 % |
92: 
93: Sens inverse (EN → FR), pour vérifier que le résultat ne dépend pas du côté de départ :
94: 
95: | mesure (sens EN → FR) | toutes ancres | ancres distinctives |
96: |---|---:|---:|
97: | occurrences | 2 554 | 567 |
98: | rappel à distance 0 | 85,3 % | 86,6 % |
99: | rappel ±2 | 94,9 % | 95,8 % |
100: | perles avec ancre | 1 687 | 475 |
101: 
102: **Où vont les anc
… [7288 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\n# 1) blank line before the per-anchor table\ns=s.replace('''    L.append(\n        \"Les huit ancres distinctives … [1481 caractères tronqués]`

  ```
ok
COMPILE_OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --json /tmp/verne_final_test.json --rapport /tmp/verne_final_test.md", "description": "Full run with negative controls", "timeoutMs": 6000 … [3 caractères tronqués]`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 3.0 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.927 / distinctives 0.932 ; matrice diagonale top-1 37/37
[6/7] contrôles négatifs (3 répétitions)…
      contrôles en 20.5 s
[7/7] écrit : /tmp/verne_final_test.json (3397 paires) et /tmp/verne_final_test.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
  ```

- **read** `{"file_path": "/tmp/verne_final_test.md"}`

  ```
<path>/tmp/verne_final_test.md</path>
<type>file</type>
<content>
1: # Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais)
2: 
3: **Date** : 2026-10-19 18:29 UTC  
4: **Outil** : `tools/aligneur_litteraire.py` (CPU, bibliothèque standard, aucun modèle)  
5: **Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
6: 
7: ## 1. La question
8: 
9: La mesure 59 a établi que le banc littéraire était **invalide** : trois découpages successifs (titres, grille proportionnelle, corps) donnaient 84, 60 puis 37 sections françaises contre 37 anglaises, et le chrF restait au niveau du hasard. Le problème n'était pas le modèle mais l'**appariement** : les segments comparés ne disaient pas la même chose. Ce sous-chantier construit donc un alignement **phrase à phrase** et, surtout, le **vérifie** avec des ancres indépendantes — sans quoi un alignement « plausible » ne serait qu'une hypothèse de plus.
10: 
11: ## 2. Le dispositif
12: 
13: ### 2.1 Les textes
14: 
15: | | français | anglais |
16: |---|---:|
… [14091 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days && for w in Rangoon steamer vessel; do echo \"EN $w: $(grep -o -i \"\\b$w\\b\" around_world_80_days_en.txt | wc -l)\"; done; echo \"FR Rangoon: $(grep -o -i '\\bRangoon\\b' around … [288 caractères tronqués]`

  ```
EN Rangoon: 22
EN steamer: 91
EN vessel: 17
FR Rangoon: 1
--- EN context 'steamer' ---
488:From Suez to Bombay, by steamer .................... 13 ”
490:From Calcutta to Hong Kong, by steamer ............. 13 ”
491:From Hong Kong to Yokohama (Japan), by steamer ..... 6 ”
492:From Yokohama to San Francisco, by steamer ......... 22 ”
494:From New York to London, by steamer and rail ........ 9 ”
569:trains upon the steamers, and from the steamers upon the trains again.”
689:steamers and railways. He took the carpet-bag, opened it, and slipped
813:not find himself, when travelling by steamer in winter, at the mercy of
--- FR Rangoon count by chapter? ---
31
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nlignes=A.lire_gutenberg(A.FR_DEFAUT).split(\"\\n\"); ch,_=A.reperer_chapitres(ligne … [428 caractères tronqués]`

  ```
FR 24 Toutefois, ses grands yeux se fixaient sur ceux de Mr. Fogg, ses grands yeux «limpides comme les lacs sacrés de l'Himalaya»!
FR 25 Mais l'intraitable Fogg, aussi boutonné que jamais, ne semblait point homme à se jeter dans ce lac.
FR 26 Cette première partie de la traversée du _Rangoon_ s'accomplit dans des conditions excellentes.
FR 27 Le temps était maniable.
FR 28 Toute cette portion de l'immense baie que les marins appellent les «brasses du Bengale» se montra favorable à la marche du paquebot.

EN 13 Whether she would find a protector in him she could not tell; but Mr. Fogg essayed to calm her anxieties, and to assure her that everything would be mathematically—he used the very word—arranged.
EN 14 Aouda fastened her great eyes, “clear as the sacred lakes of the Himalaya,” upon him; but the intractable Fogg, as reserved as ever, did not seem at all inclined to throw himself into this lake.
EN 15 The first few days of the voyage passed prosperously, amid favourable weather and propitious winds, and they soon came in sight of the great Andaman, the principal of the islands in the Bay of Bengal, with its picturesqu
EN 16 The steamer passed along near the shores, but the sava
… [611 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport json, random\nd=json.load(open('/tmp/verne_final_test.json'))\nrnd=random.Random(42)\nones=[p for p in d['paires'] if p['n_fr']==1 and p['n_en']==1]\nprint(\"1:1 pairs\",len(ones))\nfor p in rnd.sample(ones,18):\n    p … [195 caractères tronqués]`

  ```
1:1 pairs 2570

ch10 FR5/EN4
 F: Depuis 1756--époque à laquelle fut fondé le premier établissement anglais sur l'emplacement aujourd'hui occupé par la ville de Madras--jusqu'à cette année dans laquelle éclata la grande insurrection d
 E: The celebrated East India Company was all-powerful from 1756, when the English first gained a foothold on the spot where now stands the city of Madras, down to the time of the great Sepoy insurrection

ch3 FR46/EN45
 F: --Où voulez-vous qu'il aille?
 E: “Where could he go, then?”

ch19 FR135/EN118
 F: Vous ne le connaissez même pas!
 E: You know scarcely anything about him.

ch18 FR42/EN29
 F: Les huniers et les basses voiles purent être établis, et le _Rangoon_ reprit sa route avec une merveilleuse vitesse.
 E: Some of the sails were unfurled, and the “Rangoon” resumed its most rapid speed.

ch16 FR102/EN70
 F: Fix, qui connaissait la dernière partie de ces incidents, semblait les ignorer tous, et Passepartout se laissait aller au charme de narrer ses aventures devant un auditeur qui lui marquait tant d'inté
 E: Fix, who was familiar with the last events, seemed to be equally ignorant of all that Passepartout related; and the later was charmed to 
… [2027 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nlignes=A.lire_gutenberg(A.FR_DEFAUT).split(\"\\n\"); ch,_=A.reperer_chapitres(ligne … [787 caractères tronqués]`

  ```
9 paragraphes FR 46 EN 30 chars 11181 9050
14 paragraphes FR 42 EN 27 chars 13151 11333
15 paragraphes FR 88 EN 76 chars 11714 10648
16 paragraphes FR 31 EN 25 chars 10741 9206
17 paragraphes FR 42 EN 35 chars 12726 10058
para beads 25
FR0:1 EN0:1  ["Le _Rangoon_, l'un des paquebots que la Compagnie péninsulai"] || ['The “Rangoon”—one of the Peninsular and Oriental Company’s b']
FR1:2 EN1:2  ['Pendant les premiers jours de cette traversée, Mrs. Aouda fi'] || ['During the first days of the journey Aouda became better acq']
FR2:4 EN2:3  ['Mrs. Aouda confirma le récit que le guide indou avait fait d', 'La jeune femme comprenait-elle cet horrible adverbe? On ne s'] || ['Aouda confirmed the Parsee guide’s narrative of her touching']
FR4:4 EN3:4  [] || ['The first few days of the voyage passed prosperously, amid f']
FR4:6 EN4:5  ["Cette première partie de la traversée du _Rangoon_ s'accompl", "La côte fut prolongée d'assez près. Les sauvages Papouas de "] || ['The panorama of the islands, as they steamed by them, was su']
FR6:7 EN5:6  ["Le développement panoramique de ces îles était superbe. D'im"] || ['What was detective Fix, so unluckily drawn on from country t']
FR7:9 EN6:7  ["Que fai
… [3103 caractères tronqués]
  ```

### 🤖 Assistant

The paragraph structure is much cleaner than the sentence-level DP in weak chapters. I'll prototype a two-level aligner (chapter → paragraph → sentence) and measure whether it improves the independent anchor validation.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, time\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nlignes=A.lire_gutenberg(A.FR_DEFAUT).split(\"\\n\"); ch,_=A.reperer_chapitres … [2862 caractères tronqués]`

  ```
two-level beads 3431 time 0.933577299118042
all occ 2673 exact 0.7800224466891134 pm1 0.8742985409652076 pm2 0.9083426861204639 pairs 0.944412932501418
dist occ 584 exact 0.8047945205479452 pm1 0.875 pm2 0.9178082191780822 pairs 0.9235412474849095
Counter({(1, 1): 2500, (2, 1): 559, (1, 2): 104, (3, 1): 96, (1, 0): 65, (2, 2): 30, (0, 1): 24, (2, 0): 15, (3, 0): 9, (4, 0): 9, (5, 0): 4, (1, 3): 4, (0, 9): 2, (0, 2): 2, (0, 6): 2, (0, 14): 1, (8, 0): 1, (0, 16): 1, (9, 0): 1, (6, 0): 1, (0, 3): 1})
unpaired FR sentences 201 EN 91
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\n\nold='f\"×{facteur:.1f} (seuil ×{args.seuil_facteur:.0f})\" if facteur is not None else \"non calculable\",'\nne … [3218 caractères tronqués]`

  ```
ok
COMPILE_OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \":%\\|:.1%\\|:.0%\\|:.1f}\\|:.0f}\" tools/aligneur_litteraire.py | grep -v \"_f(\\|_p(\\|ratio:\\|time\\|duree\\|f\\\"{_\" | head -30", "description": "Search for remaining period-decimal formats"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py", "description": "Produce final JSON and report in repo", "timeoutMs": 600000}`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.8 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.927 / distinctives 0.932 ; matrice diagonale top-1 37/37
[6/7] contrôles négatifs (3 répétitions)…
      contrôles en 19.8 s
[7/7] écrit : data/alignement/verne_fr_en.json (3397 paires) et reports/alignement-verne.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh tools/aligneur_litteraire.py data/alignement/verne_fr_en.json reports/alignement-verne.md && echo \"=== git status ===\" && git status --short && echo \"=== git check-ignore ===\" && git check-ignore -v data/alignement/verne_f … [67 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 1,3M 19 oct 14:30 data/alignement/verne_fr_en.json
-rw-r--r--. 1 stephane stephane  16K 19 oct 14:30 reports/alignement-verne.md
-rw-------. 1 stephane stephane  79K 19 oct 14:30 tools/aligneur_litteraire.py
=== git status ===
?? reports/alignement-verne.md
?? tools/aligneur_litteraire.py
=== git check-ignore ===
.gitignore:5:data/	data/alignement/verne_fr_en.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport json\np='data/alignement/verne_fr_en.json'\nd=json.load(open(p))\nprint(\"top keys:\",list(d))\nprint(\"meta:\",{k:v for k,v in d['meta'].items() if k not in ('ancres',)})\npr … [870 caractères tronqués]`

  ```
top keys: ['meta', 'structure', 'chapitres', 'paires', 'non_appariees', 'validation']
meta: {'titre': 'Le Tour du monde en quatre-vingts jours — alignement FR → EN', 'date': '2026-10-19 18:30 UTC', 'outil': 'tools/aligneur_litteraire.py', 'version': '1.0', 'fichiers': {'fr': '/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt', 'en': '/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_en.txt'}, 'graine': 20260227, 'repetitions': 3, 'rayon': 2, 'seuil_distinctif': 6, 'duree_s': 23.909857273101807, 'ratio_global': 0.874618613147623, 'indices': '0-based', 'unite': 'perle Gale-Church (1..3 phrases par côté)'}
nb ancres: 81
chapitres: 37 paires: 3397
non appariées: 59 8
verdict: True les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
première paire keys: ['chapitre', 'i_fr', 'i_en', 'n_fr', 'n_en', 'fr', 'en']
exemple: {"chapitre": 1, "i_fr": 1, "i_en": 0, "n_fr": 2, "n_en": 2, "fr": "À l'un des plus
… [402 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 tools/aligneur_litteraire.py && sed -n '42,50p;104,122p;178,200p' reports/alignement-verne.md", "description": "Read final report key sections"}`

  ```
### 2.5 Les ancres

81 groupes d'ancres (personnages, lieux, navires, institutions), avec leurs formes française et anglaise (`Londres`/`London`, `Inde`/`India`, `Tankadère`/`Tankadere`, `Banque d'Angleterre`/`Bank of England`…). La recherche est insensible à la casse et aux accents, mais **avec frontières de mot** — sans quoi `fixe` compterait pour `Fix`, `comparaison` pour `Paris` et `machine` pour `Chine`. Six ancres ambiguës en anglais (`fix`, `young`, `speedy`, `hitch`, `smith`, `proctor`) exigent une majuscule. **Alias** : le français dit « Sir Francis Cromarty » là où l'anglais abrège souvent en « Sir Francis » ; les deux formes sont un seul groupe (`cromarty`), sinon on compterait comme des échecs des différences de dénomination, pas d'alignement. Les ancres **distinctives** sont celles qui apparaissent dans au plus 6 chapitres : ce sont elles qui portent le contrôle fort.

## 3. Les chiffres

### 3.1 Structure

Les huit ancres distinctives les plus fréquentes — le taux global n'est pas porté par une seule :

| ancre | occurrences | rappel 0 | rappel ±2 |
|---|---:|---:|---:|
| `cromarty` | 53 | 81,1 % | 90,6 % |
| `stuart` | 31 | 87,1 % | 90,3 % |
| `rangoon` | 31 | 61,3 %
… [2624 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\n\nold='''        \"Une **occurrence** est un couple (phrase, ancre). Le rappel à distance *d* est la fraction des … [1962 caractères tronqués]`

  ```
ok
COMPILE_OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py", "description": "Regenerate final outputs", "timeoutMs": 600000}`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.7 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.927 / distinctives 0.932 ; matrice diagonale top-1 37/37
[6/7] contrôles négatifs (3 répétitions)…
      contrôles en 19.3 s
[7/7] écrit : data/alignement/verne_fr_en.json (3397 paires) et reports/alignement-verne.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/alignement-verne.md", "limit": 90, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/alignement-verne.md</path>
<type>file</type>
<content>
1: # Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais)
2: 
3: **Date** : 2026-10-19 18:31 UTC  
4: **Outil** : `tools/aligneur_litteraire.py` (CPU, bibliothèque standard, aucun modèle)  
5: **Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
6: 
7: ## 1. La question
8: 
9: La mesure 59 a établi que le banc littéraire était **invalide** : trois découpages successifs (titres, grille proportionnelle, corps) donnaient 84, 60 puis 37 sections françaises contre 37 anglaises, et le chrF restait au niveau du hasard. Le problème n'était pas le modèle mais l'**appariement** : les segments comparés ne disaient pas la même chose. Ce sous-chantier construit donc un alignement **phrase à phrase** et, surtout, le **vérifie** avec des ancres indépendantes — sans quoi un alignement « plausible » ne serait qu'une hypothèse de plus.
10: 
11: ## 2. Le dispositif
12: 
13: ### 2.1 Les text
… [5138 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/alignement-verne.md", "limit": 55, "offset": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/alignement-verne.md</path>
<type>file</type>
<content>
90: | perles partageant une ancre (distance 0) | 84,7 % | 83,0 % |
91: | perles partageant une ancre (±2) | 94,8 % | 92,8 % |
92: 
93: Sens inverse (EN → FR), pour vérifier que le résultat ne dépend pas du côté de départ :
94: 
95: | mesure (sens EN → FR) | toutes ancres | ancres distinctives |
96: |---|---:|---:|
97: | occurrences | 2 554 | 567 |
98: | rappel à distance 0 | 85,3 % | 86,6 % |
99: | rappel ±2 | 94,9 % | 95,8 % |
100: | perles avec ancre | 1 687 | 475 |
101: 
102: **Où vont les ancres manquées ?** Sur 2 686 occurrences, 81,1 % sont dans la perle, 17,7 % sont **ailleurs dans le même chapitre** (déplacement local, réécriture) et 1,2 % sont **absentes du chapitre** (le traducteur a supprimé ou remplacé le nom). Sur les distinctives : 491/587 dans la perle, 92 ailleurs, 4 absentes. L'essentiel des manques est donc un **déplacement de quelques phrases**, pas une perte de chapitre — c'est ce que rattrape la tolérance ±2. Ce classement est un diagnostic *a posteriori*, pas un critère : le contrôle négatif, lui, ne pardonne rien.
103: 
104: Les huit ancres dis
… [3406 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/alignement-verne.md", "limit": 60, "offset": 145}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/alignement-verne.md</path>
<type>file</type>
<content>
145: |---|---:|
146: | diagonale classée n° 1 | **37/37** chapitres |
147: | diagonale dans le top 3 | **37/37** chapitres |
148: | similarité moyenne sur la diagonale | 0,917 |
149: | similarité moyenne hors diagonale | 0,107 |
150: | similarité minimale sur la diagonale | 0,743 |
151: 
152: ### 3.6 Distribution des rapports de longueur
153: 
154: | mesure | par caractères | par mots |
155: |---|---:|---:|
156: | nombre de perles | 3 397 | 3 397 |
157: | médiane | 0,904 | 1,000 |
158: | quartiles Q1 – Q3 | 0,800 – 1,010 | 0,851 – 1,111 |
159: | 5 % – 95 % | 0,627 – 1,250 | 0,647 – 1,429 |
160: | minimum – maximum | 0,161 – 4,200 | 0,250 – 7,000 |
161: | part dans [0,75 ; 1,25] | 78,5 % | 77,5 % |
162: | part dans [0,80 ; 1,20] | 69,1 % | 68,1 % |
163: | part hors [0,5 ; 2,0] | 1,4 % | 1,4 % |
164: 
165: La médiane **par caractères** (0,904) est inférieure à 1 parce que l'anglais est plus court que le français ; celle **par mots** (1,000) est au niveau. C'est le **ratio global** qui sert de référence, pas 1. Les queues de distribution sont attendues : une perle 1:1 p
… [4449 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport aligneur_litteraire as A\nd=json.load(open('data/alignement/verne_fr_en.json'))\nlignes=A.lire_gutenber … [1162 caractères tronqués]`

  ```
ch9 paired beads 72 FR sentences 115 EN 73

FR1+2 -> EN1+1 miss={'brindisi'}
 F: Le _Mongolia_, dont les feux étaient activement poussés, marchait de manière à devancer l'arrivée réglementaire. La plupart des passagers embarqués à Brindisi avaient presque tous l'Inde pour destinat
 E: The “Mongolia,” thanks to the vigorous exertions of the engineer, seemed likely, so rapid was her speed, to reach her destination considerably within that time.

FR12+2 -> EN7+1 miss={'merrouge'}
 F: On faisait de la musique, on dansait même, quand la mer le permettait. Mais la mer Rouge est fort capricieuse et trop souvent mauvaise, comme tous ces golfes étroits et longs.
 E: When the wind came from the African or Asian coast the “Mongolia,” with her long hull, rolled fearfully.

FR96+1 -> EN63+1 miss={'aden'}
 F: À six heures du soir, le _Mongolia_ battait des branches de son hélice les eaux de la rade d'Aden et courait bientôt sur la mer des Indes.
 E: At six p.m. the “Mongolia” slowly moved out of the roadstead, and was soon once more on the Indian Ocean.

FR97+3 -> EN64+1 miss={'aden'}
 F: Il lui était accordé cent soixante-huit heures pour accomplir la traversée entre Aden et Bombay. Du reste, c
… [560 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find tools -maxdepth 2 -name \"__pycache__\" -o -name \"*.pyc\" | head -20 && ls -la tools/__pycache__ 2>/dev/null | head", "description": "Check for pycache artifacts"}`

  ```
tools/__pycache__
tools/__pycache__/journal_auto.cpython-313.pyc
tools/__pycache__/essai_decharge.cpython-313.pyc
tools/__pycache__/lecture_etat.cpython-313.pyc
tools/__pycache__/occupation_poids.cpython-313.pyc
tools/__pycache__/audit_drapeaux_harnais.cpython-313.pyc
tools/__pycache__/c8_entrainer_tete.cpython-313.pyc
tools/__pycache__/exporter_gguf.cpython-313.pyc
tools/__pycache__/exporter_gguf_dense.cpython-313.pyc
tools/__pycache__/cycle_entraine.cpython-313.pyc
tools/__pycache__/memoire_travail.cpython-313.pyc
tools/__pycache__/vision_hf_ref.cpython-313.pyc
tools/__pycache__/vision_bloc_ref.cpython-313.pyc
tools/__pycache__/vision_isole.cpython-313.pyc
tools/__pycache__/vision_projecteur_ref.cpython-313.pyc
tools/__pycache__/derouler.cpython-313.pyc
tools/__pycache__/cycle_sensibilite.cpython-313.pyc
tools/__pycache__/speculatif_drave.cpython-313.pyc
tools/__pycache__/n4_dessin_b.cpython-313.pyc
tools/__pycache__/mrope_valeurs_or.cpython-313.pyc
total 1100
drwxr-xr-x. 1 stephane stephane   3746 19 oct 14:30 .
drwxr-xr-x. 1 stephane stephane  10200 19 oct 14:28 ..
-rw-------. 1 stephane stephane  13765 17 oct 17:37 adaptateur_langue.cpython-313.pyc
-rw-r--r--. 1 stephane steph
… [481 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\nold='''            \"sont petits (5 à 53 occurrences) : ces variations sont du bruit d'échantillonnage autant que … [1068 caractères tronqués]`

  ```
ok
exit=0
[6/7] contrôles négatifs (3 répétitions)…
      contrôles en 19.7 s
[7/7] écrit : /tmp/verne_check.json (3397 paires) et /tmp/verne_check.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py && echo \"=== remove pyc artifact ===\" && ls -l tools/__pycache__/aligneur_litteraire.cpython-313.pyc 2>/dev/null && realpath tools/__pyc … [123 caractères tronqués]`

  ```
[1/7] lecture des textes…
[2/7] repérage des chapitres (filtre par longueur)…
      FR 74 candidates → 37 chapitres ; EN 74 → 37
[3/7] découpage en phrases…
      FR 4275 phrases / 408378 caractères ; EN 3526 / 357175 ; ratio 0.8746
[4/7] alignement Gale-Church…
      3464 perles en 2.9 s
[5/7] ancres et validation…
      rappel ±2 : toutes 0.927 / distinctives 0.932 ; matrice diagonale top-1 37/37
[6/7] contrôles négatifs (3 répétitions)…
      contrôles en 20.5 s
[7/7] écrit : data/alignement/verne_fr_en.json (3397 paires) et reports/alignement-verne.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
=== remove pyc artifact ===
-rw-r--r--. 1 stephane stephane 100173 19 oct 14:30 tools/__pycache__/aligneur_litteraire.cpython-313.pyc
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/__pycache__/aligneur_litteraire.cpython-313.pyc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f tools/__pycache__/aligneur_litteraire.cpython-313.pyc && rm -f -- tools/__pycache__/aligneur_litteraire.cpython-313.pyc && ls tools/__pycache__/aligneur_litteraire.cpython-313.pyc 2>&1 || echo \"pyc supprimé\"", "description" … [33 caractères tronqués]`

  ```
ls: cannot access 'tools/__pycache__/aligneur_litteraire.cpython-313.pyc': No such file or directory
pyc supprimé
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport json, re, unicodedata\nd=json.load(open('data/alignement/verne_fr_en.json',encoding='utf-8'))\npairs=d['paires']\ndef norm(s):\n    s=unicodedata.nor … [1701 caractères tronqués]`

  ```
paires: 3397 chapitres: 37
intégrité: OK (non vides, chapitres 1..37, i_fr croissants)
fogg           présent FR dans  631 paires ; même ancre EN  525 (83.2 %)
passepartout   présent FR dans  415 paires ; même ancre EN  348 (83.9 %)
aouda          présent FR dans  131 paires ; même ancre EN  110 (84.0 %)
fix            présent FR dans  261 paires ; même ancre EN  213 (81.6 %)
londres        présent FR dans   60 paires ; même ancre EN   50 (83.3 %)
bombay         présent FR dans   58 paires ; même ancre EN   51 (87.9 %)
reform         présent FR dans   37 paires ; même ancre EN   32 (86.5 %)
ratio chars: médiane 0.904  Q1 0.800  Q3 1.010  n=3397
perles multi-FR: 738 exemple: 1 1 2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"rade d'Aden\\|Les chapitres 9\" reports/alignement-verne.md && echo \"---\" && grep -n \"Verdict\\|VALIDE\\|93,2\\|83,6\" reports/alignement-verne.md | head -12 && echo \"=== git status ===\" && git status --short && echo \ … [117 caractères tronqués]`

  ```
121:Les chapitres 9 et 14-17 sont les plus bas pour cette raison : le traducteur y remplace des noms par des périphrases (« la rade d'Aden » → « the roadstead », « les îles Salcette » → « the islands in the bay »), et l'ancre disparaît sans que la phrase ait bougé.
---
5:**Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
85:| rappel à distance 0 | 81,1 % | 83,6 % |
87:| rappel ±2 | 92,7 % | 93,2 % |
131:| **alignement réel** | 92,7 % | 93,2 % | 83,6 % |
140:**Hasard pur, phrase contre phrase dans le même chapitre** : 38 400 tirages, **15,62 %** de rencontres d'ancres. C'est un plancher **phrase contre phrase** — conservateur, parce que les noms propres reviennent beaucoup dans un même chapitre — et non le plancher de la mesure par perle : le contrôle de référence reste la **permutation des chapitres** (0,3 %). L'alignement réel fait **83,65 %** à distance 0 et **93,19 %** à ±2 sur les ancres distinctives, soit **×5,4** et **×6,0** ce plancher.
172:2. **La tolérance ±2 absorbe les différences de découpage.** Le taux à dista
… [1101 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport json\nd=json.load(open('data/alignement/verne_fr_en.json',encoding='utf-8'))\nv=d['validation']['verdict']\nprint(\"valide:\",v['valide'])\nprint(\"resume:\",v['resume'])\nfor … [931 caractères tronqués]`

  ```
valide: True
resume: les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
True structure 37 / 37 : 37 chapitres FR et 37 EN, numéros identiques
True matrice des chapitres (diagonale n° 1) : 37 / 37 chapitres ont leur homologue en première position
True rappel des ancres distinctives : 93,2 % à ±2 (seuil 80,0 %)
True contrôle négatif (chapitres permutés) : 0,3 % à ±2 (seuil 10,0 %)
True facteur au-dessus du hasard : ×272,5 (seuil ×8)

manques distinctifs: {'occurrences': 587, 'exact': 491, 'presente_ailleurs': 92, 'absente_chapitre': 4, 'part_exact': 0.8364565587734242, 'part_presente_ailleurs': 0.1567291311754685, 'part_absente_chapitre': 0.0068143100511073255}
matrice top1: 37
longueurs chars: {'n': 3397, 'moyenne': 0.917, 'mediane': 0.904, 'q1': 0.8, 'q3': 1.01, 'p5': 0.627, 'p95': 1.25, 'minimum': 0.161, 'maximum': 4.2, 'part_0_75_1_25': 0.785, 'part_0_8_1_2': 0.691, 'part_hors_0_5_2': 0.014}

chapitres 1 et 37: 1 37
paires min/max chapitre: 1 37
=== files ===
-rw-r--r--. 1 stephane stephane 1356554 19 oct 14:32 data/alignement/verne_fr_en.json
-rw
… [403 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py --help | head -30 && echo \"=== lignes outil ===\" && wc -l tools/aligneur_litteraire.py reports/alignement-verne.md", "description": "Che … [28 caractères tronqués]`

  ```
usage: aligneur_litteraire.py [-h] [--fr FR] [--en EN] [--json JSON]
                              [--rapport RAPPORT] [--graine GRAINE]
                              [--repetitions REPETITIONS] [--rayon RAYON]
                              [--seuil-distinctif SEUIL_DISTINCTIF]
                              [--seuil-rappel SEUIL_RAPPEL]
                              [--seuil-controle SEUIL_CONTROLE]
                              [--seuil-facteur SEUIL_FACTEUR]
                              [--sans-controles]

Alignement phrase à phrase vérifié par les ancres (Le Tour du monde en 80
jours).

options:
  -h, --help            show this help message and exit
  --fr FR               texte français (Gutenberg)
  --en EN               texte anglais (Gutenberg)
  --json JSON           sortie JSON des paires
  --rapport RAPPORT     fiche de mesure markdown
  --graine GRAINE       graine des contrôles négatifs
  --repetitions REPETITIONS
                        répétitions des contrôles négatifs
  --rayon RAYON         voisinage de validation (phrases)
  --seuil-distinctif SEUIL_DISTINCTIF
                        une ancre est distinctive si elle apparaît dans ≤ N
                        cha
… [318 caractères tronqués]
  ```

### 🤖 Assistant

All checks pass. I'll send the self-contained result to the parent agent, then summarize.

- **send_message** `{"agent_id": "d629d7d7-e122-4596-8757-f4264a2b15cf", "message": "SOUS-CHANTIER TERMINÉ — alignement FR↔EN du Tour du monde en 80 jours : **VALIDE**, vérifié aux ancres.\n\nFICHIERS (créés uniquement ; aucun fichier existant modifié, aucun commit) :\n- outils : `/home/stephane/Data13TB/stephane/GitHu … [3585 caractères tronqués]`

  ```
message delivered to agent d629d7d7-e122-4596-8757-f4264a2b15cf
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python - <<'EOF'\np='tools/aligneur_litteraire.py'\ns=open(p,encoding='utf-8').read()\nold='''        \"`machine` pour `Chine`. Six ancres ambiguës en anglais (`fix`, `young`, `speedy`, `hitch`, `smit … [749 caractères tronqués]`

  ```
ok
exit=0
      contrôles en 20.0 s
[7/7] écrit : data/alignement/verne_fr_en.json (3397 paires) et reports/alignement-verne.md
      VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).
ls: cannot access 'tools/__pycache__/aligneur_litteraire.cpython-313.pyc': No such file or directory
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '45p;121p;183,190p' reports/alignement-verne.md && echo \"=== git ===\" && git status --short && echo \"=== data ignoré ===\" && git check-ignore data/alignement/verne_fr_en.json && echo \"=== tailles ===\" && wc -c tools/alig … [143 caractères tronqués]`

  ```
81 groupes d'ancres (personnages, lieux, navires, institutions), avec leurs formes française et anglaise (`Londres`/`London`, `Inde`/`India`, `Tankadère`/`Tankadere`, `Banque d'Angleterre`/`Bank of England`…). La recherche est insensible à la casse et aux accents, mais **avec frontières de mot** — sans quoi `fixe` compterait pour `Fix`, `comparaison` pour `Paris` et `machine` pour `Chine`. Six ancres ambiguës en anglais (`fix`, `young`, `speedy`, `hitch`, `smith`, `proctor`) exigent une majuscule — et `reform` aussi, pour ne pas confondre le club avec le mot commun. **Alias** : le français dit « Sir Francis Cromarty » là où l'anglais abrège souvent en « Sir Francis » ; les deux formes sont un seul groupe (`cromarty`), sinon on compterait comme des échecs des différences de dénomination, pas d'alignement. Les ancres **distinctives** sont celles qui apparaissent dans au plus 6 chapitres : ce sont elles qui portent le contrôle fort.
Les chapitres 9 et 14-17 sont les plus bas pour cette raison : le traducteur y remplace des noms par des périphrases (« la rade d'Aden » → « the roadstead », « les îles Salcette » → « the islands in the bay »), et l'ancre disparaît sans que la phrase ait b
… [873 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale des sorties et rédaction du bilan

## Verdict : **VALIDE**

L'alignement est validé par des ancres **indépendantes de l'appariement** (elles ne servent jamais à aligner, seulement à juger) : **93,2 % des occurrences d'ancres distinctives se retrouvent à ±2**, contre **0,3 %** quand on permute les chapitres (**×272,5**), et **83,6 %** à distance 0.

## Fichiers créés (aucun fichier existant modifié, aucun commit)

- Outil : `tools/aligneur_litteraire.py` — CPU, bibliothèque standard, aucun modèle.
- JSON : `data/alignement/verne_fr_en.json` — 3 397 paires, 1,3 Mo (gitignoré).
- Fiche : `reports/alignement-verne.md` — 200 lignes, dispositif + chiffres + contrôles + limites.

Reproduction : `CUDA_VISIBLE_DEVICES="" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py` (~24 s).

Remarque : `reports/traduction-eurlex-0.5b.json`, non suivi, n'est pas de moi — je n'y ai pas touché.

## Chapitres et tables des matières

- **37 chapitres français / 37 chapitres anglais**, numéros contigus 1..37 et identiques.
- Chaque langue donne **74 lignes candidates** : 37 entrées de table des matières (même forme que les en-têtes : `I TITRE` / `CHAPTER I. TITRE`) + 37 vrais en-têtes.
- Filtre **par longueur** : pour chaque numéro, on garde la candidate dont le bloc suivant est le plus long (≥ 1 500 caractères ; une entrée de table fait ~100). **37 lignes de table écartées par langue**, puis vérification de contiguïté et d'identité des numéros.

## Paires alignées

- 4 275 phrases FR / 3 526 phrases EN.
- **3 464 perles** Gale-Church (chapitre par chapitre, ratio global EN/FR = 0,875) ; **3 397 perles appariées** des deux côtés, dont **2 570 paires 1:1 strictes** (2:1 : 628 ; 1:2 : 86 ; 3:1 : 81 ; 1:0 : 59 ; 2:2 : 29 ; 0:1 : 8 ; 1:3 : 3).
- Couverture : **4 216 phrases FR (98,6 %)** et **3 518 EN (99,8 %)** ; 59 phrases FR et 8 EN non appariées.

## Rappel des ancres et contrôles négatifs

81 groupes d'ancres (personnages, lieux, navires, institutions), cherchés avec frontières de mot, insensibles aux accents et à la casse (majuscule exigée pour `fix`, `young`, `speedy`, `hitch`, `smith`, `proctor`, `reform`).

| mesure (FR → EN) | toutes ancres | distinctives (≤ 6 chapitres) |
|---|---:|---:|
| occurrences | 2 686 | 587 |
| distance 0 | 81,1 % | **83,6 %** |
| ±1 | 90,2 % | 91,3 % |
| **±2** | 92,7 % | **93,2 %** |
| ±5 | 95,6 % | 96,1 % |

Sens inverse EN → FR (distinctives) : 86,6 % à 0, 95,8 % à ±2. Les manques sont surtout des **déplacements locaux** : 17,7 % des occurrences sont ailleurs dans le même chapitre, 1,2 % seulement sont absentes du chapitre.

**Contrôles négatifs** (même aligneur, même dictionnaire, même mesure) :

| contrôle (distinctives, ±2) | taux |
|---|---:|
| **alignement réel** | **93,2 %** |
| chapitres permutés (3 tirages) | **0,2–0,5 %** (moyenne 0,3 %) |
| chapitre voisin i→i+1 | 9,2 % |
| phrases mélangées dans chaque chapitre | 29,0–31,4 % |
| hasard phrase contre phrase, même chapitre | 15,62 % |

La **matrice chapitres × chapitres** (Jaccard pondérée IDF, indépendante de l'alignement des phrases) place le bon chapitre en **n° 1 pour 37/37 chapitres** (moyenne diagonale 0,917 contre 0,107 hors diagonale).

## Distribution des rapports de longueur (par perle)

| mesure | caractères | mots |
|---|---:|---:|
| médiane | 0,904 | 1,000 |
| Q1 – Q3 | 0,800 – 1,010 | 0,851 – 1,111 |
| 5 % – 95 % | 0,627 – 1,250 | 0,647 – 1,429 |
| min – max | 0,161 – 4,200 | 0,250 – 7,000 |
| dans [0,75 ; 1,25] | 78,5 % | 77,5 % |
| hors [0,5 ; 2] | 1,4 % | 1,4 % |

## Limites (ce qui pourrait rendre le chiffre faux)

1. **Zone aveugle** : 55,1 % des phrases FR et 51,4 % des EN n'ont aucune ancre ; 45,1 % des perles n'en ont ni d'un côté ni de l'autre. Pour elles, seuls la longueur et la position valident — pas une ancre.
2. **Tolérance ±2** : elle absorbe les différences de découpage. Le chiffre strict est 83,6 % à distance 0 ; c'est lui qu'il faut citer si l'on exige l'alignement exact.
3. **Dictionnaire construit à la main**, avec alias assumés (`Cromarty`/`Sir Francis`, `Smyth`/`Smith`, `Oysterpuf`/`Oysterpuff`, `lac Salé`/`Salt Lake`, `Malebar-Hill`/`Malabar Hill`). Il reste indépendant de l'appariement, mais pas du choix des textes.
4. **Le traducteur paraphrase parfois les noms** (`Rangoon` → « the steamer », `Aden` → « the roadstead », `Salcette` → « the islands in the bay », `Obadiah` → « the judge ») : ces cas sont comptés comme des échecs, jamais retirés, donc le taux est **conservateur**.
5. **Fragments non narratifs** : l'itinéraire chiffré du chapitre 3 et les tableaux de distances sont traités comme des phrases et peuvent s'apparier entre eux de travers (peu nombreux).
6. **Un seul livre, un seul traducteur** (Towle, 1873), pas d'alignement de référence externe ; coquilles Gutenberg possibles ; le contrôle « chapitres permutés » n'est pas un hasard parfait (personnages partagés), mais les contrôles plus durs (voisin 9,2 %, mélange 29-31 %) restent très loin de 93,2 %.
7. Le contrôle est **structurel** (noms propres, longueur, position), pas sémantique : il ne garantit pas la fidélité des mots communs.

## Ce que je n'ai pas fait

- Aucun commit, aucune modification de `docs/en-cours.md`, `reports/07-mesures-couche-commune.md`, `journal/` ou `AGENTS.md`.
- Je n'ai pas lancé `tools/revue_documentation.py` : il corrige des fichiers existants, ce que la consigne du sous-chantier interdit. À faire par le parent.

