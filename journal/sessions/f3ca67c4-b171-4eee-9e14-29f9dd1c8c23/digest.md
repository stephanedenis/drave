# Session DSH — relecture

- identifiant : `f3ca67c4-b171-4eee-9e14-29f9dd1c8c23`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:19:01
- agent : standard


## Tour 1

### 👤 Utilisateur

MISSION STRICTEMENT EN LECTURE SEULE. Tu ne dois RIEN écrire, RIEN modifier, RIEN exécuter qui écrive ou télécharge. Uniquement read/grep/glob et commandes bash de lecture (ls, wc, file, head). Tu ne dois PAS lancer les scripts Python.

Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave). Tools dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/.

Tâche : pour CHACUN de ces 12 scripts, lis le fichier en entier et décris précisément son éventuel APPRENTISSAGE/AJUSTEMENT (par opposition à une simple mesure) :

1. tools/discriminant_transfert.py
2. tools/discriminant_contenu.py
3. tools/stabilite_directions.py
4. tools/renforcement_directions.py
5. tools/renforcement.py
6. tools/energie_du_contenu.py
7. tools/transfert_ridge.py
8. tools/blanchiment_entree.py
9. tools/sous_espace_du_contenu.py
10. tools/covariance_cible.py
11. tools/decomposition.py
12. tools/amplification.py
13. tools/calibre_modes.py

Pour chacun, rends une ligne dense avec :
- chemin absolu
- type d'apprentissage (ridge forme fermée / moindres carrés / discriminant LDA / power-iteration / covariance / ACP-SVD / NLMS / aucun apprentissage = pure mesure)
- architecture exacte si réseau de neurones (couches, dimensions d'entrée/sortie, activation, nombre de paramètres si calculable depuis le code)
- entrée et sortie (dimensions numériques exactes quand le code les donne, ex. 896 canaux, couche 10, H neurones cachés)
- cible et fonction de coût (loss) exacte (ex. ||Y - XW||² + λ||W||², cosinus, Fisher, variance expliquée)
- optimiseur (forme fermée np.linalg.solve/lstsq, itérations, epochs, nombre de passes, boucle de croissance) et valeurs par défaut des hyperparamètres (lambda/ride, seuils, patience, nombre d'itérations)
- où il sauvegarde un fichier de poids/artefact : chemin exact écrit par np.save/np.savez/savez_compressed/open(...,'wb'), nom de variable, taille si tu peux l'estimer
- pour chaque affirmation, distingue « LU DANS LE CODE » (avec numéro de ligne) de « SUPPOSÉ ».

Termine par : la liste des fichiers de poids/artefacts locaux écrits par ces scripts, et ceux qui existent réellement sur le disque (vérifie avec ls -la les chemins trouvés, y compris /tmp, /home/stephane/Data13TB/stephane/, et le dépôt).

Réponds en français, format liste dense, ≤ 45 lignes. Ne joins pas de long extrait de code, seulement lignes/faits.
Your parent agent id is "ee19a880-cc76-4c5c-9fe0-5972bd73b533". Before you finish, send your result to that agent with send_message({ agent_id: "ee19a880-cc76-4c5c-9fe0-5972bd73b533", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Lecture intégrale des 13 scripts tools/ pour cartographier apprentissages et artefacts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && wc -l discriminant_transfert.py discriminant_contenu.py stabilite_directions.py renforcement_directions.py renforcement.py energie_du_contenu.py transfert_ridge.py blanchiment_entree.py sous_espace_du_contenu.py covariance_cibl … [117 caractères tronqués]`

  ```
227 discriminant_transfert.py
   185 discriminant_contenu.py
   178 stabilite_directions.py
   246 renforcement_directions.py
   174 renforcement.py
   170 energie_du_contenu.py
   126 transfert_ridge.py
   141 blanchiment_entree.py
   162 sous_espace_du_contenu.py
   143 covariance_cible.py
   207 decomposition.py
   177 amplification.py
   150 calibre_modes.py
  2286 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools/ | head -60", "description": "List tools directory"}`

  ```
total 1508
drwxr-xr-x. 1 stephane stephane   4850  7 oct 20:59 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rwx--x--x. 1 stephane stephane  11640  1 oct 04:21 aiguille.py
-rw-------. 1 stephane stephane   7797  6 oct 22:04 amplification.py
-rwx--x--x. 1 stephane stephane   8850  1 oct 17:40 analyse_empreinte.py
-rw-------. 1 stephane stephane   4614  2 oct 17:28 analyse_engram.py
-rwx--x--x. 1 stephane stephane  11086  1 oct 20:13 analyse_experts_statique.py
-rwxr-xr-x. 1 stephane stephane   5449  3 oct 04:19 analyse_flux.py
-rwx--x--x. 1 stephane stephane   6767  3 oct 09:42 analyse_hc.py
-rwx--x--x. 1 stephane stephane   6364  3 oct 08:11 analyse_octets_par_jeton.py
-rwx--x--x. 1 stephane stephane   6029  3 oct 11:51 analyse_reutilisation_experts.py
-rw-------. 1 stephane stephane   5049  3 oct 13:04 analyse_union_experts.py
-rw-------. 1 stephane stephane   4815  7 oct 10:32 ancre_professeur.py
-rwxr-xr-x. 1 stephane stephane   2995  5 oct 10:44 applique_pont.py
-rwxr-xr-x. 1 stephane stephane   6030  5 oct 08:43 approximabilite_bloc.py
-rwx--x--x. 1 stephane stephane   3776  3 oct 11:50 apres-telechargement-k3.sh
-rwx--x--x. 1 stephane stephane   8444 27 sep 11:40 
… [3074 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des 5 premiers scripts en parallèle

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_transfert.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_contenu.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/stabilite_directions.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/renforcement_directions.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_transfert.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """discriminant_transfert.py — les directions apprises sur un panel servent-elles sur un autre ?
3: 
4: LA QUESTION, ET ELLE EST NEUVE. Le §80 a mesuré qu'un discriminant linéaire appris portait
5: le rapport contenu/langue à **105 % du professeur**. Mais ce résultat a été obtenu SUR LE
6: PANEL ROMAN (es/it/pt) et mesuré SUR CE MÊME PANEL. Or le §83 vient d'établir que le
7: professeur lui-même vaut 12,001 sur ce panel et **1,494 sur sa pire paire (de–en)**.
8: 
9: Un projecteur appris à séparer l'espagnol, l'italien et le portugais sait-il séparer
10: l'allemand de l'anglais ? Rien ne l'assure : le discriminant maximise `C_cont/C_lang`, et
11: `C_lang` est estimé sur LES LANGUES DU PANEL D'APPRENTISSAGE. Si l'axe de langue appris est
12: « l'axe roman », il peut être orthogonal à « l'axe germanique ».
13: 
14: CE QUI EST MESURÉ. Trois caches, quatre cas. Le pont est appris sur `--appr` ; le
15: discriminant sur `--disc` ; la mesure sur `--eval`. Les cas se lisent deux à deux :
16: dans-panel contre transfert, dans les deux sens.
17:
… [10176 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_contenu.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """discriminant_contenu.py — maximiser le rapport contenu/langue par les DIRECTIONS.
3: 
4: CE QUI MÈNE ICI, en trois étapes établies :
5:   §67 — le rapport `P_cont/P_lang` est INVARIANT D'ÉCHELLE : aucune amplitude ne peut
6:         le corriger, seulement un changement de DIRECTIONS ;
7:   §68 — imposer la covariance TOTALE de la cible ne marche pas, parce que la covariance
8:         globale ne détermine pas le partage contenu/langue ;
9:   §61 — le partage dépend des **moyennes PAR ENTRÉE**, donc de la structure de groupes.
10: 
11: L'OUTIL QUI VISE EXACTEMENT CELA. On cherche les directions de l'espace de sortie qui
12: **maximisent le rapport** entre l'énergie de contenu et l'énergie de langue. C'est un
13: problème aux valeurs propres généralisé — l'analyse discriminante linéaire :
14: 
15:     C_cont · v = λ · C_lang · v
16: 
17: où, calculées sur les **moyennes par entrée** de l'APPRENTISSAGE :
18:     C_cont = covariance des moyennes par CONTENU   (μ_k − μ̄)
19:     C_lang = covariance des moyennes par LANGUE    (ν_L − ν̄)
20
… [7509 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/stabilite_directions.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """stabilite_directions.py — les directions du discriminant viennent-elles des DONNÉES ou du TIRAGE ?
3: 
4: LA QUESTION. Le §92 montre qu'un discriminant de rang 2 appris sur nos sorties sépare le
5: contenu de la langue mieux que le professeur sur dix des quinze paires. Mais **nos sorties
6: dépendent d'un tirage aléatoire gelé** : `P` et `B` sont tirés avec `np.random.RandomState(5)`.
7: La question est donc :
8: 
9: > **L'axe contenu/langue que le discriminant trouve est-il une propriété de la structure
10: > exposée par le professeur, ou une propriété de NOTRE tirage ?**
11: 
12: Si deux graines différentes donnent des sous-espaces très différents, alors « la direction du
13: contenu » n'existe pas dans notre représentation — elle est fabriquée par le tirage, et le
14: résultat du §92 ne se reproduirait pas avec une autre graine.
15: 
16: CE QUI EST MESURÉ. Pour chaque graine, on apprend le pont, on lit les sorties, on apprend le
17: discriminant, et on garde le sous-espace `V_r` de ses `r` premiers axes. Puis on mesure les
18: **a
… [7285 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/renforcement_directions.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """renforcement_directions.py — la réserve du §72 : apprendre QUOI LIRE.
3: 
4: LA SEULE RÉSERVE QUI RESTAIT. Le §72 a testé **la forme de renforcement implémentée
5: dans le dépôt** — mettre à l'échelle les poids d'un neurone selon sa capture du résidu —
6: et elle échoue : +1,7 % du chemin nécessaire, plateau dès la deuxième passe. La raison
7: était nette : la capture moyenne vaut ≈ 0,5, **aucun neurone ne capte le résidu mieux
8: que le hasard**, donc aucun n'est franchement renforcé.
9: 
10: **Mais mettre à l'échelle ne change PAS ce qu'un neurone lit** — seulement l'amplitude
11: de ce qu'il lit déjà. Or si aucun neurone ne capte le résidu, c'est peut-être qu'aucun
12: ne lit la bonne direction de l'entrée.
13: 
14: LA FORME DIFFÉRENTE, testée ici. On apprend à chaque neurone **la direction de l'entrée
15: qui prédit le résidu**, par corrélation seule :
16: 
17:     G = Eᵀ·R          (H × canaux) — covariance croisée entrée / résidu
18:     SVD(G) = U·S·Vᵀ   — les colonnes de U sont les directions de l'entrée
19:               
… [11764 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des scripts 5-8 plus le module Pont (architecture du réseau)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/renforcement.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/energie_du_contenu.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/transfert_ridge.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/blanchiment_entree.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/renforcement.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """renforcement.py — le mécanisme du mandat peut-il produire la transformation ?
3: 
4: LA QUESTION OUVERTE, APRÈS LES §57-§71. Le professeur crée, entre sa couche 0 et sa
5: couche 8, une séparation contenu/langue d'un facteur **10,912** — que sa propre couche 0
6: n'a pas (**1,698** au mieux). Un réservoir à poids **aléatoires gelés** ne la produit
7: pas : mesuré, il l'**abaisse** à 1,354 (§70).
8: 
9: LA CONTRAINTE DU PROJET est explicite : *« A et B aléatoires et gelés, seule la lecture
10: s'ajuste en forme fermée »* — **mais** elle sanctionne aussi, mot pour mot :
11: *« L'ajout d'une couche suppose donc une relecture du corpus pour réajuster les poids
12: par renforcement/atrophie (pas de backprop). »*
13: 
14: **Le renforcement/atrophie est donc le seul mécanisme d'ajustement autorisé** — et il
15: n'a JAMAIS été testé sur l'axe contenu/langue. C'est ce que fait ce script.
16: 
17: LE MÉCANISME, tel qu'il est implémenté dans `Pont.renforce` :
18:   1. on ajuste la lecture, puis on calcule le **résidu** `R = Y − (φ(X)·W + mt)` ;
19:   2
… [7275 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/energie_du_contenu.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """energie_du_contenu.py — peut-on retrouver l'ÉNERGIE de contenu, pas seulement son rapport ?
3: 
4: CE QUI MÈNE ICI. Le §87 a mesuré, hors vivier sur un panel de 6 langues, que notre pont
5: atteint **136 % du RAPPORT** du professeur avec **3,4 % de son énergie de contenu** et
6: 2,5 % de son énergie de langue. Le rapport est un quotient : deux énergies qui s'effondrent
7: ensemble le laissent intact. Le critère qui compte est celui du §62.3 — **`P_cont` proche du
8: professeur ET `P_lang` qui ne le dépasse pas**.
9: 
10: L'HYPOTHÈSE, ET ELLE EST ANCIENNE (§58, `ou_est_le_contenu.py`). La fidélité est un cosinus
11: par ligne, mais l'ajustement est une erreur QUADRATIQUE ABSOLUE. La cible a une masse
12: commune énorme (norme ~440) et les écarts qui distinguent les contenus sont petits devant
13: elle. En minimisant l'erreur absolue, la lecture est payée pour reproduire la masse
14: commune — et les petites composantes, celles qui portent le contenu, pèsent peu.
15: 
16: TROIS FAMILLES DE REMÈDES, toutes CONVEXES et en forme fermée :
17
… [6914 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/transfert_ridge.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """LE READOUT SUR-APPREND-IL LE VIVIER ? — balayage du ride, deux panneaux.
3: 
4: DIAGNOSTIC ÉTABLI (§36). Avec le protocole à deux panneaux :
5:     écart à l'oracle — VALIDATION (même vivier) : +0,0112
6:     écart à l'oracle — TEST (hors vivier)       : +0,0975
7: Dans le vivier notre lecture partagée est quasi optimale ; hors vivier il reste
8: 0,0975 sur la table. Le goulot est le TRANSFERT.
9: 
10: L'HYPOTHÈSE LA PLUS SIMPLE, et elle se teste à un paramètre près : si la lecture
11: transfère mal, c'est peut-être qu'elle s'ajuste à des directions PROPRES AU VIVIER.
12: Le remède classique est de régulariser davantage. Or le ride est aujourd'hui une
13: constante choisie à la main (0,3), jamais balayée sur ce critère.
14: 
15: PRÉDICTION, ÉCRITE AVANT LA MESURE : si le readout sur-apprend le vivier, augmenter
16: le ride doit
17:   - DÉGRADER légèrement la validation (moins bon ajustement dans le vivier),
18:   - AMÉLIORER le test (moins de directions propres au vivier),
19:   - donc RÉDUIRE l'écart à l'oracle hors vivier.
20: Si les de
… [4690 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/blanchiment_entree.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """blanchiment_entree.py — retirer de l'entrée sa structure de COVARIANCE par langue.
3: 
4: CE QUE LE §70 A ÉTABLI. L'axe de langue vient de **l'entrée** du professeur, et le
5: réservoir ne fait que l'**amplifier** : `P_lang` passe de 199,5 (entrée seule) à 238,8
6: (réservoir), pendant que `P_cont` baisse. La couche 8 du professeur a un rapport de
7: 10,912 ; sa propre couche 0, lue le mieux possible, n'en a que 1,698.
8: 
9: CE QUI RESTE PERMIS PAR LES CONTRAINTES : `A` et `B` sont aléatoires et **gelés**, seule
10: la lecture s'ajuste. On ne peut donc pas *apprendre* la transformation manquante. Mais
11: on peut **changer ce qu'on donne à lire** au réservoir.
12: 
13: Le §64 a montré qu'en retirant à l'entrée son **jeton moyen** (le premier moment), le
14: rapport gagne 28 %. Reste le **second moment** : la structure de covariance, qui est
15: elle aussi massivement propre à la langue (écriture, morphologie, longueur des mots).
16: On la retire par un **blanchiment par langue** :
17: 
18:     E' = (E − moyenne) · C_langue^(-1/2)
19: 
… [5332 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des 5 derniers scripts + le module de référence Pont

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sous_espace_du_contenu.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/covariance_cible.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/decomposition.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/amplification.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/calibre_modes.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sous_espace_du_contenu.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """sous_espace_du_contenu.py — rendre le remède DÉPLOYABLE.
3: 
4: LE PROBLÈME, EN UNE PHRASE (§62). L'énergie de contenu de notre sortie est
5: sous-produite d'un facteur ~3,6 ; elle est récupérable par mise à l'échelle ; mais la
6: mise à l'échelle essayée exigeait de savoir **quelles entrées partagent un contenu** —
7: information qui n'existe pas pour un texte neuf.
8: 
9: L'IDÉE QUI MANQUAIT, et elle est simple. Ce regroupement n'est pas nécessaire **à
10: l'inférence** : il ne l'est qu'à l'**apprentissage**. On apprend donc, une fois pour
11: toutes et sur les données d'apprentissage :
12: 
13:   1. le SOUS-ESPACE DU CONTENU — l'espace engendré par les écarts de contenu
14:      `μ_k − m̄`, où `μ_k` est la moyenne des sorties des entrées partageant le
15:      contenu `k` ;
16:   2. un projecteur `Π` sur ce sous-espace.
17: 
18: Puis, à l'inférence, on applique à la sortie d'un texte neuf :
19: 
20:     O_new = O + (γ − 1)·Π·(O − m̄)
21: 
22: `Π` est une **matrice fixe** de 896×896 apprise une fois. Aucun regroupement n'est
23: 
… [6648 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/covariance_cible.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """covariance_cible.py — donner à la sortie la COVARIANCE de la cible.
3: 
4: LE CONSTAT QUI MÈNE ICI. Le §67 a montré une chose mathématiquement nette : **le
5: rapport `P_cont/P_lang` est invariant d'échelle**. Une amplification uniforme de
6: l'écart multiplie les deux énergies par le même facteur, donc ne change jamais leur
7: rapport — mesuré : 3,064 exactement pour α de 1 à 5, à tous les rangs essayés.
8: 
9: **Le rapport ne peut donc venir que d'un changement de DIRECTIONS**, pas d'amplitude.
10: C'est cohérent avec tout ce que la série §58-§67 a trouvé.
11: 
12: L'IDÉE, et elle vise exactement cela. Le professeur a un rapport de **10,912** ; nous
13: sommes à 3,064. Sa **matrice de covariance** contient cette structure directionnelle.
14: On construit donc une transformation linéaire `A` qui **donne à notre sortie la
15: covariance de la cible** :
16: 
17:     C_O = covariance de nos sorties   (sur l'APPRENTISSAGE)
18:     C_Y = covariance des cibles       (sur l'APPRENTISSAGE)
19:     A   = C_Y^(1/2) · C_O^(-1/2)
20:     sortie cor
… [5436 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/decomposition.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """decomposition.py — où va la variance : en LANGUE ou en CONTENU ?
3: 
4: Après quatre causes écartées (§58 à §60), il reste à LOCALISER le défaut. La bonne
5: façon n'est pas une similarité cosinus mais une **décomposition de variance**, qui est
6: exacte et additive.
7: 
8: Pour chaque entrée (langue L, contenu k), on prend sa moyenne `m_Lk`. On décompose :
9: 
10:     ν_L  = moyenne de `m_Lk` sur les contenus        -> effet LANGUE
11:     μ_k  = moyenne de `m_Lk` sur les langues         -> effet CONTENU
12:     r_Lk = m_Lk − ν_L − μ_k + m̄                      -> résidu (interaction)
13: 
14:     P_lang = Σ_L n_L ‖ν_L − m̄‖²     énergie portée par la LANGUE
15:     P_cont = Σ_k n_k ‖μ_k − m̄‖²     énergie portée par le CONTENU
16: 
17: Le RAPPORT `P_cont / P_lang` est la quantité qui compte : il dit lequel des deux
18: axes structure le plus la représentation. On le mesure sur **notre sortie** et sur
19: **celle du professeur**, sur les mêmes entrées — c'est une comparaison directe, sans
20: cible mouvante.
21: 
22: C'est aussi le remède 
… [9471 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/amplification.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """amplification.py — notre sortie est-elle ÉCRASÉE VERS LA MOYENNE ?
3: 
4: L'OBSERVATION QUI N'AVAIT PAS ÉTÉ FAITE. Le §57 a montré que notre sortie ne sépare
5: plus contenu et langue (S_langue ≈ S_domaine ≈ 0,99 sur Wikipedia), là où le
6: professeur, si (0,9454 / 0,8937 · écart +0,052). Quatre objectifs ont été essayés
7: pour corriger cela (§58, §59), tous écartés.
8: 
9: Mais une chose n'a jamais été regardée : **notre sortie est-elle seulement plus PETITE
10: que sa cible, autour du même point ?**
11: 
12: La lecture prédit `O = φ(X)·W + mt`, où `mt` est la moyenne globale des cibles. Si les
13: caractéristiques ne peuvent pas produire toute l'amplitude de la cible, le moindres
14: carrés **rétrécit** la prédiction vers la moyenne — c'est le phénomène classique de
15: régression vers la moyenne. Or `mt` est **le même pour toutes les entrées** : une
16: prédiction dominée par `mt` a donc des moyennes par entrée presque identiques, ce qui
17: produit exactement le tableau du §57 — `S_langue ≈ S_domaine ≈ 1`.
18: 
19: LE TEST, et il est t
… [7341 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/calibre_modes.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """calibre_modes.py — le mode DENSE trace-t-il la même chose que le mode ÉVÉNEMENTIEL ?
3: 
4: POURQUOI LA QUESTION SE POSE. Le mode par défaut du moteur construit ses listes
5: d'événements **au chargement** : sur Qwen2.5-0.5B, 15,6 M d'événements pour ~6 s,
6: à chaque invocation. Le calcul par jeton, lui, est identique (mesuré : 32,4 contre
7: 32,3 ms/jeton). Sur un corpus de 455 langues tracées une par une, ces 6 s fixes
8: coûtent **45 minutes** — d'où l'envie de tracer en `--dense`.
9: 
10: MAIS TOUT CE DÉPÔT A ÉTÉ TRACÉ EN MODE ÉVÉNEMENTIEL. Changer de mode sans le
11: mesurer rendrait le nouveau corpus incomparable à l'ancien sans que rien ne le
12: dise. Le moteur annonce déjà, ailleurs, que les deux chemins diffèrent
13: légèrement (corrélations 0,998 contre 0,9998 contre la référence) — ce n'est pas
14: « identique », c'est « proche », et « proche » doit se chiffrer.
15: 
16: CE QUI EST MESURÉ : pour chaque langue, les mêmes positions, la même couche, et
17: la similarité cosinus entre les deux traces. On rapporte le cosinus minimum
… [5577 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du module Pont + recherche des écritures d'artefacts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && wc -l pont_generatif.py && ls -la pont_generatif.py", "description": "Check pont_generatif size"}`

  ```
1041 pont_generatif.py
-rw-r--r--. 1 stephane stephane 55157  6 oct 19:46 pont_generatif.py
  ```

- **grep** `{"pattern": "np\\.save|savez|savez_compressed|open\\([^)]*['\\\"]w|\\.write\\(|pickle\\.dump|joblib\\.dump|tofile|savetxt", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools", "include": "*.py"}`

  ```
Found 82 matches

tools/trace_gpu.py
Line 131:                 g.write(blob)

tools/premiere_couche_semantique.py
Line 107:     np.savez_compressed(sortie, langues=np.array(langues),
Line 222:                     g.write("couche,meme,autre,separation\n")
Line 224:                         g.write(f"{c},{m:.6f},{a:.6f},{s:.6f}\n")

tools/extrait_article1.py
Line 90:             g.write(t + "\n")

tools/profil_couches.py
Line 227:             f.write("couche,P_lang,P_cont,rapport,dim_eff\n")
Line 229:                 f.write(f"{c},{a:.4f},{b:.4f},{r:.6f},{dm:.3f}\n")

tools/engram_reference.py
Line 195:         with open(f, "w") as g:

tools/extrait_crime.py
Line 86:             open(p, "w", encoding="utf-8").write(S[i])

tools/wiki_apparie.py
Line 115:             open(p, "w", encoding="utf-8").write(blocs[L])

tools/profil_langues.py
Line 210:     with open(csv, "w") as fh:
Line 211:         fh.write("langue;frag;norme;norme896;pas;temoin;fid_ref;oracle_ref;"
Line 214:             fh.write(f"{r['cl']};{r['frag']:.4f};{r['norme']:.3f};"

tools/profil_flux.py
Line 69:         with open(csv, "w") as f:
Line 70:             f.write("couche,neurone,magnitude,frequence\n")
Line 72:       
… [4569 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in discriminant_transfert.py discriminant_contenu.py stabilite_directions.py renforcement_directions.py renforcement.py energie_du_contenu.py transfert_ridge.py blanchiment_entree.py sous_espace_du_contenu.py covariance_c … [264 caractères tronqués]`

  ```
== discriminant_transfert.py
  (aucune écriture)
== discriminant_contenu.py
  (aucune écriture)
== stabilite_directions.py
  (aucune écriture)
== renforcement_directions.py
  (aucune écriture)
== renforcement.py
  (aucune écriture)
== energie_du_contenu.py
  (aucune écriture)
== transfert_ridge.py
  (aucune écriture)
== blanchiment_entree.py
  (aucune écriture)
== sous_espace_du_contenu.py
  (aucune écriture)
== covariance_cible.py
  (aucune écriture)
== decomposition.py
  (aucune écriture)
== amplification.py
  (aucune écriture)
== calibre_modes.py
40:    with open(chemin, "rb") as f:
101:    os.makedirs(tmp, exist_ok=True)
110:        texte = open(f, encoding="utf-8").read().strip()
  ```

- **grep** `{"include": "pont_generatif.py", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools", "pattern": "^(class |def |    def )"}`

  ```
Found 28 matches

tools/pont_generatif.py
Line 32: def charge(p):
Line 40: def cos_lignes(A, B):
Line 46: def inv(V):
Line 54: class Pont:
Line 76:     def __init__(self, donnees, a, graine, H, decal=0):
Line 135:     def debut_couche(self, c):
Line 138:     def taille_couche(self, c):
Line 142:     def nait(self, k, nouvelle_couche=True):
Line 217:     def _norm(self, X):
Line 223:     def phi(self, X):
Line 230:     def ajuste(self, idx, ride, mt, quel=slice(None)):
Line 304:     def fid(self, idx, W, mt, quel):
Line 309:     def dernier(self, idx, W, mt, quel):
Line 313:     def _W_neurones(self, W, K):
Line 322:     def contribution(self, W, idx):
Line 328:     def redondance(self, W, idx):
Line 344:     def recalcule(self, S, Ek=None):
Line 394:     def compacte(self, S):
Line 418:     def couches_de(self, S):
Line 422:     def communs(self, idx, quel, L=64):
Line 457:     def communs_fin(self, idx, quel):
Line 486:     def contraste(self, W):
Line 500:     def _recalcule_un(self, j, Ek=None):
Line 524:     def renforce(self, j, itr, mt, ride, eta=0.6):
Line 558:     def evalue(self, X, Y, W, mt):
Line 562:     def invariance(self, X, W, mt):
Line 566: def main():
Line 569:   
… [23 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des sections-clés de Pont (naissance, phi, ajuste)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py", "offset": 1, "limit": 310}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pont_generatif.py — le réseau NAÎT, puis subit une ATTRITION qui le fait généraliser.
3: 
4: Deux phases, dans cet ordre, et c'est l'apprentissage qui décide des tailles.
5: 
6: PHASE GÉNÉRATIVE. On part d'un seul neurone. Chaque pas de croissance ajoute une
7: COUCHE de neurones. Une couche nouvelle ne lit que les couches ANTÉRIEURES (plus
8: elle-même) : jamais l'inverse. Conséquence exacte, et c'est ce qui rend la
9: croissance gratuite — les trajectoires déjà calculées ne sont PAS perturbées, on
10: ne calcule que la couche qui naît. Le coût total de la croissance vaut donc à peu
11: près celui du réseau final, pas la somme de tous les états intermédiaires.
12: 
13: PHASE D'ATTRITION. Périodiquement, on retire les neurones REDONDANTS — ceux dont
14: la trajectoire se reconstruit à partir des autres — puis on RÉAJUSTE la lecture
15: sur les survivants. C'est le réajustement qui fait généraliser : la capacité
16: retirée doit être réabsorbée par les unités qui restent, ce qui remplace des
17: détecteurs particuliers par des concepts plus
… [16090 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification format des caches (couche, 896 canaux) et artefacts sur disque

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cache_pont.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cache_pont.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """cache_pont.py — parse UNE fois les traces, puis toutes les expériences sont rapides.
3: 
4: Le goulot de `pont_reservoir.py` n'est pas le réservoir (64 neurones, quelques
5: milliers de pas) mais la LECTURE : 2,1 Go de DRVF en Python pur, ~10 min par
6: essai. Hors de question de balayer des réglages à ce prix.
7: 
8: Usage : cache_pont.py <dossier> <sortie.npz> [--couche 10] [--hidden 896]
9: """
10: import glob, os, struct, sys
11: import numpy as np
12: 
13: 
14: def lire(chemin):
15:     def paires(f, n, version, bloc=32):
16:         ech = None
17:         if version == 3:
18:             nb, = struct.unpack("<I", f.read(4))
19:             ech = [struct.unpack("<e", f.read(2))[0] for _ in range(nb)]
20:         out, prev = [], 0
21:         for _ in range(n):
22:             if version == 1:
23:                 i, = struct.unpack("<I", f.read(4))
24:             else:
25:                 e, = struct.unpack("<B", f.read(1))
26:                 i = struct.unpack("<H", f.read(2))[0] if e == 255 else prev + e
27:                 prev = i
28:
… [2710 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la 2>/dev/null; echo \"--- npz/npy dans le dépôt (hors .git)\"; find . -path ./.git -prune -o \\( -name \"*.npz\" -o -name \"*.npy\" \\) -print 2>/dev/null | head -40; echo \"--- /tmp\"; ls -la /tmp 2>/dev/null | head -40", "desc … [51 caractères tronqués]`

  ```
total 308
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 .
drwxr-xr-x. 1 stephane stephane   2374  3 oct 10:09 ..
drwxr-xr-x. 1 stephane stephane     40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane     56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 data
drwxr-xr-x. 1 stephane stephane   1130  5 oct 13:47 docs
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane    164  8 oct 09:11 .git
-rw-r--r--. 1 stephane stephane    399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane     34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane     88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane    114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane   4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane  36518  2 oct 10:21 README.md
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 reports
-rw-------. 1 stephane stephane 120322  5 oct 16:21 REPRISE.md
-rw-------. 1 stephane stephane   8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane  10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane  12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephan
… [3578 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== npz/npy dans le dépôt, y compris data/ et models/\"; find . -path ./.git -prune -o -type f \\( -name \"*.npz\" -o -name \"*.npy\" -o -name \"*.drvf\" \\) -print 2>/dev/null | head -30; echo \"=== data/\"; ls -laR data/ 2>/ … [121 caractères tronqués]`

  ```
=== npz/npy dans le dépôt, y compris data/ et models/
=== data/
data/:
total 776
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 359041 25 sep 18:02 wikitext2_test.txt
-rw-r--r--. 1 stephane stephane 398564  1 oct 07:37 wikitext2_test.txt.ids
-rw-r--r--. 1 stephane stephane  30005 25 sep 17:53 wt2.json
=== models/
total 863324
drwxr-xr-x. 1 stephane stephane        88 25 sep 17:13 .
drwxr-xr-x. 1 stephane stephane       612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
  ```

- **bash** `{"command": "find /tmp -maxdepth 2 -name \"*.npz\" -print 2>/dev/null | head -30; echo \"=== /home/stephane/Data13TB/stephane (hors Qtrinet)\"; find /home/stephane/Data13TB/stephane -maxdepth 3 -name \"*.npz\" -print 2>/dev/null | head -30", "description": "Search /tmp and home for npz caches"}`

  ```
/tmp/pcs_a2.derniere.npz
/tmp/pcs_a1.derniere.npz
/tmp/pcs_a2.moyenne.npz
/tmp/pcs_a1.moyenne.npz
/tmp/cache_6l_test.npz
/tmp/cache_6l_train.npz
/tmp/cache_6l.npz
/tmp/cache_vf_test.npz
/tmp/cache_vf_train.npz
/tmp/cache_wikitest.npz
/tmp/cache_wikitrain.npz
/tmp/cache_wiki_pt.npz
/tmp/cache_wiki_it.npz
/tmp/cache_wiki_es.npz
/tmp/cache_wiki_de.npz
/tmp/cache392c8_test.npz
/tmp/cache392c8_train.npz
/tmp/cache_unites8_test.npz
/tmp/cache_unites8_train.npz
/tmp/cache_unites_test.npz
/tmp/cache_unites_train.npz
/tmp/cache_wiki_fr.npz
/tmp/cache_wiki_en.npz
/tmp/cache_rj8_fr.npz
/tmp/cache_rj8_en.npz
/tmp/cache_rj_fr.npz
/tmp/cache_rj_en.npz
/tmp/cache392_test.npz
/tmp/cache392_train.npz
/tmp/cache_str_test.npz
=== /home/stephane/Data13TB/stephane (hors Qtrinet)
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz
/home/stephane/Data13TB/stephane/pont_semantique.npz
  ```

### 🤖 Assistant

⏵ Recherche des invocations réelles dans reports/ (canaux, couche, caches)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && ls -la | head -50; echo \"=== grep invocations\"; grep -rl -E \"discriminant_contenu\\.py|discriminant_transfert\\.py|renforcement_directions\\.py|energie_du_contenu\\.py\" . 2>/dev/null | head -20", "description": "List repo … [33 caractères tronqués]`

  ```
total 1256
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane    386  1 oct 09:38 aiguille-30b.md
-rw-r--r--. 1 stephane stephane    370  1 oct 09:38 aiguille-gpt-oss.md
-rw-------. 1 stephane stephane   9416  2 oct 15:32 bilan-multi-materiel.md
-rw-r--r--. 1 stephane stephane  16731  2 oct 21:44 decoupage-v41-digest.txt
-rw-r--r--. 1 stephane stephane   2465 30 sep 08:44 rapport-8bits.md
-rw-------. 1 stephane stephane   5208 29 sep 19:14 rapport-aiguille.md
-rw-------. 1 stephane stephane  19506  1 oct 06:53 rapport-aiguille-topk.md
-rw-r--r--. 1 stephane stephane   3250 30 sep 10:36 rapport-analyse-flux.md
-rw-------. 1 stephane stephane  20161  1 oct 22:26 rapport-architecture-memoire.md
-rw-------. 1 stephane stephane   7834 30 sep 08:44 rapport-attention-creuse.md
-rw-r--r--. 1 stephane stephane   2532 30 sep 15:30 rapport-attribution-kv.md
-rw-------. 1 stephane stephane   5096  3 oct 11:50 rapport-budget-kimi-k3.md
-rw-r--r--. 1 stephane stephane   4211  4 oct 10:43 rapport-cache-experts-vram.md
-rw-------. 1 stephane stephane   4652 30 sep 08:44 rapport-campagne-parcimonie.md
-rw-----
… [2606 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && grep -rhoE \"(discriminant_(transfert|contenu)|stabilite_directions|renforcement(_directions)?|energie_du_contenu|transfert_ridge|blanchiment_entree|sous_espace_du_contenu|covariance_cible|decomposition|amplification|calibre_ … [111 caractères tronqués]`

  ```
calibre_modes.py`, 8 langues, 4 écritures) :
discriminant_transfert.py` prend trois
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -B4 -A10 \"calibre_modes.py\" reports/rapport-toutes-langues.md | head -80", "description": "Read calibre_modes context in report"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -E \"python3? tools/(discriminant_contenu|discriminant_transfert|stabilite_directions|renforcement_directions|renforcement|energie_du_contenu|transfert_ridge|blanchiment_entree|sous_espace_du_contenu|covariance_cible|decompo … [183 caractères tronqués]`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i -B6 -A12 \"calibre_modes\" reports/rapport-toutes-langues.md | head -100", "description": "Grep calibre_modes mentions in report"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -E \"calibre_modes|discriminant_transfert\" --include=\"*\" -l . 2>/dev/null | grep -v \"^./.git/\" | head -20", "description": "Find all files mentioning these scripts"}`

  ```
./reports/rapport-toutes-langues.md
./reports/rapport-cycle-rapide.md
./tools/discriminant_transfert.py
./tools/calibre_modes.py
./tools/trace_gpu.py
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
./journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && grep -n \"calibre_modes\\|discriminant_transfert\" rapport-toutes-langues.md rapport-cycle-rapide.md | head -20", "description": "Locate mentions of the two scripts"}`

  ```
rapport-toutes-langues.md:5431:C'est la prochaine mesure. Les outils sont en place : `discriminant_transfert.py` prend trois
rapport-cycle-rapide.md:68:(`tools/calibre_modes.py`, 8 langues, 4 écritures) :
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && sed -n '55,95p' rapport-cycle-rapide.md; echo \"===== 5420-5445\"; sed -n '5420,5445p' rapport-toutes-langues.md", "description": "Read context around calibre_modes and discriminant_transfert"}`

  ```
sur Qwen2.5-0.5B, **15,6 M d'événements pour ~6 s**, à chaque invocation. Le
calcul par jeton, lui, est identique :

| mode | ms/jeton (mesuré) | temps total d'une trace |
|---|---:|---:|
| défaut (événementiel) | 32,4 | **8,00 s** |
| **`--dense`** | 32,3 | **1,94 s** |

**Même calcul, 6 s de moins par invocation.** Sur 399 langues tracées une par
une, ces 6 secondes fixes font **40 minutes**.

**Mais changer de mode sans le mesurer rendrait le nouveau corpus incomparable à
tout ce que ce dépôt a tracé.** La calibration a donc été faite
(`tools/calibre_modes.py`, 8 langues, 4 écritures) :

| | valeur |
|---|---:|
| cosinus **moyen** entre les deux modes | **0,9964** |
| cosinus **minimum** | 0,9160 |
| 5ᵉ centile | 0,9924 |
| rapport des normes | **1,000** |

**Verdict** : les deux modes tracent la même direction à 0,4 % près en moyenne,
8 % au pire, et à la même amplitude. Un corpus tracé en dense est donc comparable
à un corpus tracé en événementiel — **à condition de le dire**, ce qui est fait
ici.

## 4. La mesure que ce corpus rend possible : la première couche sémantique

Un chiffre qui monte ne prouve rien. La similarité entre les représentations d'une
même phrase dans 399 
… [1647 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la /tmp/*.ev.drvf /tmp/*.de.drvf 2>/dev/null | head -20; echo \"=== dossiers tmp candidats\"; ls -la /tmp | grep -iE \"dense|ev|trace|calibre\" | head -20", "description": "Look for calibre_modes trace outputs in /tmp"}`

  ```
=== dossiers tmp candidats
-rw-r--r--.   1 stephane stephane       2638  2 oct 23:20 box17_revue.md
-rw-r--r--.   1 stephane stephane    1031975  5 oct 12:42 cache_tenus_trace.npz
drwxr-xr-x.   2 stephane stephane        360  7 oct 18:22 calibre
drwxr-xr-x.   2 stephane stephane      50920  2 oct 20:55 ddense
-rw-r--r--.   1 stephane stephane         76  2 oct 20:32 dense_test.log
-rw-r--r--.   1 stephane stephane    1956587  7 oct 18:12 essai_trace.drvf
-rw-r--r--.   1 stephane stephane       3145  2 oct 20:55 exp_dense.log
-rwxr-xr-x.   1 stephane stephane        346  2 oct 20:54 exp_dense.sh
-rw-r--r--.   1 stephane stephane      71371  2 oct 22:38 exp_trace.txt
drwx------.   3 stephane stephane         60 21 sep 15:01 gev-heights-ZaCiaS
drwx------.   3 stephane stephane         60 21 sep 15:01 gev-warendorf-j2ANAN
drwxr-xr-x.   9 stephane stephane        240 24 sep 07:36 jev
-rw-r--r--.   1 stephane stephane       1035 25 sep 07:37 jev-check.log
-rw-r--r--.   1 stephane stephane       5103 24 sep 08:14 jev-readme.md
-rw-r--r--.   1 stephane stephane       4195  4 oct 10:38 k3_trace.log
-rw-r--r--.   1 stephane stephane       3877  6 oct 08:53 leviers.log
-rw-r--r--.   1 stephan
… [270 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des caches npz réels et du dossier /tmp/calibre

- **bash** `{"command": "ls -la /tmp/calibre/ 2>/dev/null | head -25; echo \"=== cache npz présents\"; ls -la /tmp/cache_*.npz 2>/dev/null | head -40", "description": "List calibre dir and cache npz files"}`

  ```
total 58532
drwxr-xr-x.   2 stephane stephane      360  7 oct 18:22 .
drwxrwxrwt. 153 root     root       805200  8 oct 09:20 ..
-rw-r--r--.   1 stephane stephane  2622203  7 oct 18:19 deu.de.drvf
-rw-r--r--.   1 stephane stephane  2621807  7 oct 18:19 deu.ev.drvf
-rw-r--r--.   1 stephane stephane 10594580  7 oct 18:21 ell.de.drvf
-rw-r--r--.   1 stephane stephane 10597913  7 oct 18:20 ell.ev.drvf
-rw-r--r--.   1 stephane stephane  1955093  7 oct 18:18 eng.de.drvf
-rw-r--r--.   1 stephane stephane  1956587  7 oct 18:18 eng.ev.drvf
-rw-r--r--.   1 stephane stephane  2977562  7 oct 18:19 fra.de.drvf
-rw-r--r--.   1 stephane stephane  2977955  7 oct 18:18 fra.ev.drvf
-rw-r--r--.   1 stephane stephane  3104984  7 oct 18:21 jpn.de.drvf
-rw-r--r--.   1 stephane stephane  3105035  7 oct 18:21 jpn.ev.drvf
-rw-r--r--.   1 stephane stephane  2921729  7 oct 18:20 rus.de.drvf
-rw-r--r--.   1 stephane stephane  2921012  7 oct 18:20 rus.ev.drvf
-rw-r--r--.   1 stephane stephane  2552261  7 oct 18:20 spa.de.drvf
-rw-r--r--.   1 stephane stephane  2552588  7 oct 18:19 spa.ev.drvf
-rw-r--r--.   1 stephane stephane  3215279  7 oct 18:22 tha.de.drvf
-rw-r--r--.   1 stephane stephane  3216200  7 oct 1
… [3001 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && for f in cache_wiki_de.npz cache392_train.npz cache_wiki_en.npz; do echo \"== $f\"; unzip -l \"$f\" 2>/dev/null | head -8; done", "description": "List npz members of sample caches"}`

  ```
== cache_wiki_de.npz
Archive:  cache_wiki_de.npz
  Length      Date    Time    Name
---------  ---------- -----   ----
     8932  1980-01-01 00:00   cles.npy
      136  1980-01-01 00:00   hidden.npy
  2068096  1980-01-01 00:00   E0.npy
  2003584  1980-01-01 00:00   E1.npy
  2007168  1980-01-01 00:00   E2.npy
== cache392_train.npz
Archive:  cache392_train.npz
  Length      Date    Time    Name
---------  ---------- -----   ----
     4340  1980-01-01 00:00   cles.npy
      136  1980-01-01 00:00   hidden.npy
  7017600  1980-01-01 00:00   E0.npy
  3763328  1980-01-01 00:00   E1.npy
  4974720  1980-01-01 00:00   E2.npy
== cache_wiki_en.npz
Archive:  cache_wiki_en.npz
  Length      Date    Time    Name
---------  ---------- -----   ----
     8932  1980-01-01 00:00   cles.npy
      136  1980-01-01 00:00   hidden.npy
  1552000  1980-01-01 00:00   E0.npy
  1835136  1980-01-01 00:00   E1.npy
  1437312  1980-01-01 00:00   E2.npy
  ```

- **bash** `{"command": "cd /tmp && for m in hidden.npy E0.npy Y0.npy; do echo \"== cache_wiki_en.npz:$m\"; unzip -p cache_wiki_en.npz \"$m\" 2>/dev/null | head -c 128 | od -c | head -6; done", "description": "Read npy headers to get shapes"}`

  ```
== cache_wiki_en.npz:hidden.npy
0000000 223   N   U   M   P   Y 001  \0   v  \0   {   '   d   e   s   c
0000020   r   '   :       '   <   i   8   '   ,       '   f   o   r   t
0000040   r   a   n   _   o   r   d   e   r   '   :       F   a   l   s
0000060   e   ,       '   s   h   a   p   e   '   :       (   )   ,    
0000100   }                                                            
0000120                                                                
== cache_wiki_en.npz:E0.npy
0000000 223   N   U   M   P   Y 001  \0   v  \0   {   '   d   e   s   c
0000020   r   '   :       '   <   f   4   '   ,       '   f   o   r   t
0000040   r   a   n   _   o   r   d   e   r   '   :       F   a   l   s
0000060   e   ,       '   s   h   a   p   e   '   :       (   4   3   3
0000100   ,       8   9   6   )   ,       }                            
0000120                                                                
== cache_wiki_en.npz:Y0.npy
0000000 223   N   U   M   P   Y 001  \0   v  \0   {   '   d   e   s   c
0000020   r   '   :       '   <   f   4   '   ,       '   f   o   r   t
0000040   r   a   n   _   o   r   d   e   r   '   :       F   a   l   s
0000060   e   ,       '   s   h 
… [119 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && for m in hidden.npy E0.npy; do echo \"== cache392_train.npz:$m\"; unzip -p cache392_train.npz \"$m\" 2>/dev/null | head -c 128 | od -c | head -5; done; echo \"== cache_6l_train\"; unzip -l cache_6l_train.npz 2>/dev/null | head -6", "description": "Read shapes of other caches" … [1 caractères tronqués]`

  ```
== cache392_train.npz:hidden.npy
0000000 223   N   U   M   P   Y 001  \0   v  \0   {   '   d   e   s   c
0000020   r   '   :       '   <   i   8   '   ,       '   f   o   r   t
0000040   r   a   n   _   o   r   d   e   r   '   :       F   a   l   s
0000060   e   ,       '   s   h   a   p   e   '   :       (   )   ,    
0000100   }                                                            
== cache392_train.npz:E0.npy
0000000 223   N   U   M   P   Y 001  \0   v  \0   {   '   d   e   s   c
0000020   r   '   :       '   <   f   4   '   ,       '   f   o   r   t
0000040   r   a   n   _   o   r   d   e   r   '   :       F   a   l   s
0000060   e   ,       '   s   h   a   p   e   '   :       (   1   9   5
0000100   8   ,       8   9   6   )   ,       }                        
== cache_6l_train
Archive:  cache_6l_train.npz
  Length      Date    Time    Name
---------  ---------- -----   ----
    35096  1980-01-01 00:00   cles.npy
      136  1980-01-01 00:00   hidden.npy
  2068096  1980-01-01 00:00   E0.npy
  ```

### 🤖 Assistant

⏵ Vérification du nombre de canaux effectif dans les logs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && grep -rhoE \"[0-9]{3,4} canaux\" . 2>/dev/null | sort | uniq -c | sort -rn | head -15", "description": "Count channel mentions in reports"}`

  ```
28 896 canaux
     10 157 canaux
      3 218 canaux
      2 168 canaux
      1 864 canaux
      1 678 canaux
      1 480 canaux
      1 424 canaux
      1 384 canaux
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"neurones\" reports/rapport-toutes-langues.md | head -12; echo \"=== search 'réseau' lines\"; grep -rhoE \"réseau [0-9]+ neurones[^#]*\" reports/*.md 2>/dev/null | sort -u | head -12", "description": "Find network size line … [14 caractères tronqués]`

  ```
151:Un détail structurel au passage : la naissance libre trouve ici **40 neurones en
205:| mémoire du readout quadratique (120 neurones → 240 colonnes) | 419 Mo |
217:s'arrête à 40 ou à 120 neurones. L'analyse en fait deux.
236:**Réseau : 52 neurones en 1 seule couche.**
281:| **0,50** (défaut) | 52 neurones · **1 couche** | 0,7621 | 0,7438 | **+0,0223** | **0,9739** | **0,8929** |
282:| **0,25** | 80 neurones · **5 couches** [44, 10, 10, 11, 5] | **0,7681** | **0,7487** | **+0,0272** | 0,9649 | 0,8745 |
319:| 0,50 | 52 neurones · **1 couche** | 0,7621 | 0,7438 | +0,0223 | **0,9739** | **0,8929** |
320:| **0,25** | 80 neurones · 5 couches [44, 10, 10, 11, 5] | **0,7681** | **0,7487** | **+0,0272** | 0,9649 | 0,8745 |
321:| 0,10 | 80 neurones · 5 couches [44, 8, 8, 16, 4] | 0,7662 | 0,7481 | +0,0266 | 0,9634 | 0,8562 |
379:| neurones | fid appr | fid VAL | **fid TEST** | invariance | pire paire |
388:`communs` reste à **+0,233** avec 14-15 % des neurones au-dessus du seuil de 0,35 :
402:| réseau | **40 neurones · 1 couche** |
=== search 'réseau' lines
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py", "offset": 500, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py</path>
<type>file</type>
<content>
500:     def _recalcule_un(self, j, Ek=None):
501:         """Refait la trajectoire d'UN neurone à partir de ses seuls parents, qui
502:         sont gelés. Sert après un réajustement de ses poids."""
503:         w_par, w_self, b, c = self.poids[j]
504:         n_par = len(w_par)
505:         debut_par = self.debut_couche(c-1) if c > 0 else 0
506:         debut_c = self.debut_couche(c)
507:         r = j - debut_c
508:         for i, E in enumerate(self.E if Ek is None else Ek):
509:             T = len(E)
510:             Xpar = (self.X[i][:, debut_par:debut_par+n_par] if n_par > 0
511:                     else np.zeros((T, 0), dtype=np.float32))
512:             cam = self.X[i][:, debut_c:j]        # camarades de couche, antérieurs
513:             v = np.zeros(T, dtype=np.float32)
514:             sv = 0.0
515:             for t in range(T):
516:                 drive = (float(Xpar[t] @ w_par)) if n_par > 0 else 0.0
517:                 if r > 0:
518:                     drive += float(cam[t] @ w_self[:r])
519:                 drive += float(w_self[r]*sv)
520:       
… [2413 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && tail -12 pont_generatif.py; echo \"=== renforce(s) usages\"; grep -rn \"\\.renforce(\\|renforce(\" --include=\"*.py\" . | head -10", "description": "Check main guard and renforce usages"}`

  ```
print(f"  taille           : {meilleur['neur']} neurones · {meilleur['couch']} couches")
    print(f"  fidélité appr.   : {meilleur['f_tr']:.4f}")
    print(f"  fidélité VAL     : {meilleur['f_va']:.4f}")
    print(f"  fidélité TEST    : {meilleur['f_te']:.4f}   (constante témoin : {base:.4f})")
    print(f"  invariance TEST  : {meilleur['inv']:.4f} · pire paire {meilleur['pire']:.4f}")
    print(f"\n# état final du réseau : {P.compte_neurones} neurones · {len(P.couches)} couches "
          f"({P.couches})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
=== renforce(s) usages
./pont_generatif.py:524:    def renforce(self, j, itr, mt, ride, eta=0.6):
./pont_generatif.py:815:                    P.renforce(P.compte_neurones-1, itr, mt, ride)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py", "limit": 55, "offset": 344}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py</path>
<type>file</type>
<content>
344:     def recalcule(self, S, Ek=None):
345:         """Refait les trajectoires des SEULS survivants, couche par couche.
346: 
347:         Les retirés ne contribuent plus rien. C'est la seule façon de savoir si
348:         une réduction est réelle : un neurone dont la trajectoire a été calculée
349:         par d'autres n'est pas « un neurone », c'est une caractéristique profonde.
350:         """
351:         S = list(S)
352:         pos = {j: r for r, j in enumerate(S)}
353:         EK = self.E if Ek is None else Ek
354:         # GARDE-FOU. `a_neur` est parallèle à `poids` : toute recopie de la
355:         # généalogie qui oublierait l'un des deux produirait soit un plantage
356:         # obscur (IndexError), soit — bien pire — un calcul SILENCIEUX avec la
357:         # mauvaise dynamique. On préfère échouer bruyamment ici. C'est arrivé :
358:         # `pont_parallele` recopiait `poids` sans `a_neur`.
359:         if len(self.a_neur) != len(self.poids):
360:             raise ValueError(
361:                 f"généalogie désynchronisée : {len(self.a_neur)} con
… [2175 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && unzip -p cache_wiki_en.npz hidden.npy | dd bs=1 skip=128 count=8 2>/dev/null | od -An -tu8; unzip -p cache_392_train.npz hidden.npy 2>/dev/null | dd bs=1 skip=128 count=8 2>/dev/null | od -An -tu8", "description": "Read hidden value from npz headers"}`

  ```
896
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la /home/stephane/Data13TB/stephane/pont_semantique*.npz /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique*.npz 2>/dev/null; echo \"=== qui les écrit\"; grep -rn \"pont_semantique\" tools/pont_recurrent.py tools/*.py 2 … [112 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 1382064  5 oct 10:47 /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz
-rw-r--r--. 1 stephane stephane   16560  5 oct 11:02 /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz
-rw-r--r--. 1 stephane stephane 1382064  5 oct 10:45 /home/stephane/Data13TB/stephane/pont_semantique.npz
=== qui les écrit
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"pont_semantique\" --include=\"*.py\" --include=\"*.sh\" . 2>/dev/null | head -12", "description": "Attribute pont_semantique npz writers"}`

  ```
./tools/pont_recurrent.py:189:    #     et pas seulement une mesure. `pont_semantique.npz` porte les trois pièces
./tools/pont_recurrent.py:191:    chemin = os.environ.get("DRAVE_PONT_SORTIE", "pont_semantique.npz")
./tools/applique_pont.py:4:Le pont est un artefact : trois matrices ajustées une fois (`pont_semantique.npz`),
  ```

- **send_message** `{"agent_id": "ee19a880-cc76-4c5c-9fe0-5972bd73b533", "message": "MISSION LECTURE SEULE — 13 scripts Qtrinet/tools. Aucun script exécuté ; seuls read/grep/glob/ls/wc/od/unzip (lecture). Notations : L=n° de ligne ; « LU » = lu dans le code ; « SUP » = supposé/inféré.\n\nBASE COMMUNE (12 des 13 scripts … [6250 caractères tronqués]`

  ```
message delivered to agent ee19a880-cc76-4c5c-9fe0-5972bd73b533
  ```

### 🤖 Assistant

⏵ Résultat transmis au parent ; synthèse finale

**Méthode** : lecture intégrale des 13 fichiers + `pont_generatif.py` (Pont/nait/phi/ajuste) + `cache_pont.py` ; en-têtes npy des caches réels lus via `unzip/od` ; aucun script exécuté, aucune écriture. Notation : L=n° de ligne, « LU » = lu dans le code, « SUP » = supposé.

**BASE COMMUNE (LU, 12/13 scripts importent tools/pont_generatif.py)** — `P.nait(n_neur,True)` = UNE couche de 120 neurones (défaut `--neur 120` ; transfert_ridge : 40) ; `P.quadratique=True` ⇒ φ(X)=[X,X²] ⇒ readout 240 colonnes (L223-228) ; `a_min,a_max=0.02,0.8` ⇒ 120 constantes de temps log-étalées (L165) ; réservoir tanh+fuite s=(1−a)s+a·tanh(drive+E·Bᵀ), B=randn(120,H)/√H, W_self=randn(120,120)/√120, **gelés** (L157-160,197-199) ; seule la lecture s'ajuste : `W=solve(XᵀX+ride·n·I, Xᵀ(Y−mt))` (L302). Canaux : E et Y = (positions,**896**) float32, hidden=896 (cache_pont.py L8/56 + en-tête npy vérifié) ; `garde` = canaux dont (y≠0)≥5 % des positions dans ≥50 % des entrées (part=0,5). Dim. : W=(240,ncan) ; ncan=896 ⇒ 215 040 coeffs ; aléatoires gelés = 107 520 (B) + 14 400 (W_self) + 120 constantes a. **RÉSERVE LU** : les scripts passent `len(garde)` comme H à Pont (ex. discriminant_contenu L113, energie L77) alors que E[i] fait 896 colonnes ⇒ ne tourne que si garde=896 (les rapports affichent « 896 canaux » 28×) ; le H renvoyé par `charge()` n'est pas utilisé pour Pont.

1. `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_transfert.py` — ridge forme fermée L150 (ride 0,03) + **LDA** `eigh(solve(Cl+λI,Cc))` L172, λ=1e-2·trace(Cl)/ncan L171 ; entrée = moyennes par entrée des sorties du pont (ncan dim) ; rangs 0,2,5,10,20,40 L111 ; ratio P_cont/P_lang (Fisher) ; graine 5 ; aucune écriture.
2. `tools/discriminant_contenu.py` — ridge ride=0,03/graine=5/part=0,5 L91-92 ; LDA L135-139, plancher 1e-2·trace(Cl)/ncan L132 ; cibles d'amplification 1000 et 4356,4 L169 ; aucune écriture.
3. `tools/stabilite_directions.py` — 6 apprentissages complets (graines 5..10 L74), ridge 0,03 + LDA par graine ; mesure = angles principaux par SVD de V_iᵀV_j L67 ; aucune écriture.
4. `tools/renforcement_directions.py` — **apprend les poids d'entrée** : G=Eᵀ(R−R̄) L144, SVD(G) L145, b_j←(1−mélange)·b_j+mélange·U[:,j%k]·‖b_j‖ L150 ; passes=5 L74, mélange=1,0 L75 ; ridge 0,03 réajusté chaque passe L153 ; LDA final L190-193 ; Hebb local, sans rétroprop.
5. `tools/renforcement.py` — renforcement/atrophie locale : cap_j=|corr(act_j,résidu)| L144, f=1+η(2cap−1) L146, poids de j ×f L148 ; η∈{0,02;0,1} L77, passes=8 L76 ; ridge 0,03 chaque passe L129/157 ; n'utilise PAS `Pont.renforce` (pont_generatif L524, η=0,6).
6. `tools/energie_du_contenu.py` — 4 variantes forme fermée A/B/C/D (`solve(G+ride·n·I,D)` L109) ; ACP cible par eigh L93 ; ride=0,03 L61, alphas 0,25/0,5/0,75/1,0 L62.
7. `tools/transfert_ridge.py` — ridge seule, balayage rides 0,03→30 L44, `--neur 40` L41 ; Gram calculée une fois L86-95 ; oracle par panneau L105-106 ; validation itr[::7] L60.
8. `tools/blanchiment_entree.py` — blanchiment par langue T[L]=(V·w^(−α/2))Vᵀ, eigh L98-100, plancher 1e-3·trace(C)/d L69 ; **aucun neurone** : readout direct [E,E²]=1792 colonnes, solve ridge 0,03 L115/124 ; alphas 0/0,25/0,5/1 L68.
9. `tools/sous_espace_du_contenu.py` — SVD des offsets de contenu L116-117, projecteur Π=Vᵀ_rV_r (896×896) L120 appris une fois ; ridge 0,03 L99 ; gammas 1/1,5/2/3/5 L74.
10. `tools/covariance_cible.py` — A=CY^½·CO^(−½) par eigh, plancher 1e-3·trace(CO)/ncan L118-119 ; mélanges 0/0,25/0,5/0,75/1 L79 ; ridge 0,03 L104.
11. `tools/decomposition.py` — **mesure pure** (ANOVA P_lang/P_cont/P_res L40-62) ; seul ajustement = readout ridge 0,03 L104 ; β(0..30) L154 et γ(0..5) L187 = diagnostics non appris ; `--mu-lang` pose `P.mu_inv` (pont_generatif L269-278).
12. `tools/amplification.py` — **mesure pure** : α=0,5..3 L84/142 sur sortie fixe ; readout ridge 0,03 L112 ; aucun paramètre appris.
13. `tools/calibre_modes.py` — **aucun apprentissage** : 2 appels par langue au binaire `./drave-core/target/release/drave` (--trace-flux, événementiel puis --dense) L85-92, relecture DRVF L37-81, cosinus/normes L126-137 ; défauts langues 8, modèle Qwen2.5-0.5B-Q8_0.gguf, ctx 256, couches 0:24 ; **écrit** `os.makedirs(tmp)` L101 + `<tmp>/<L>.ev.drvf` et `.de.drvf`.

**ARTEFACTS** — (a) **aucun des 13 ne contient np.save/np.savez/open(...,'wb')/pickle** (grep = 0) ⇒ aucun fichier de poids ; W, P.poids, Π, A, T[L], V restent en RAM. (b) Seule écriture réelle : calibre_modes.py via le binaire. (c) **Existe sur disque** : `/tmp/calibre/` = **16 .drvf** (8 langues × {ev,de}, 1,9–10,6 Mo), 7 oct 18:18-18:22 = artefacts de calibre_modes.py. (d) Entrées des 12 autres, écrites par `cache_pont.py` L79 (pas par ces scripts) : `/tmp/cache_wiki_{de,en,es,fr,it,pt}.npz` (couche 8, E0/Y0 (N,896) f32, hidden=896 vérifié), `/tmp/cache_6l{,_train,_test}.npz`, `/tmp/cache392{,_train,_test}.npz`, `/tmp/cache_wikitrain|test.npz`, `cache_unites*.npz`, `cache_appr10/10c/40.npz`. (e) **Aucun .npz/.npy dans le dépôt**. (f) `/home/stephane/Data13TB/stephane/pont_semantique.npz`, `pont_semantique_r1.npz`, `corpus/udhr/pont_semantique.npz` existent mais sont écrits par `tools/pont_recurrent.py` (L191-193) — hors périmètre. **Conclusion : aucune persistance de poids dans cette chaîne ; tout modèle appris est éphémère et reconstruit à chaque run depuis les caches .npz.**

