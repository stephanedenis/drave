# Session DSH — relecture

- identifiant : `13446299-79d8-497c-ba83-673c176a4637`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-01 00:54:37
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSARIAL autonome dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave »). Mission : vérifier les artefacts du sprint 4 (23h44 → 01h44) — aucun chiffre sans source, aucune affirmation non mesurée, aucun raisonnement qui va plus loin que la mesure. Le dépôt a une règle : « chaque chiffre publié doit avoir une source ». Trois erreurs de ce type ont déjà été commises cette nuit et corrigées (un « 511/511 » annoncé pour 497/511, un garde-fou jamais testé, un « --infer ignore --lot » démenti par le code).

Artefacts à auditer :

1. `reports/rapport-aiguille-topk.md`, section « Suite (sprint 4) : le k est un RÉGLAGE, pas une fatalité » — sources : `/tmp/aiguille_rep.log` (les 12 sondes du sprint 4 : complète ×3, k=256 ×3, k=512 ×3, k=1024 ×3), `/tmp/aiguille_k.log` (le premier balayage, une sonde par point, avec les résultats non monotones), `/tmp/aiguille_topk2.log` (sprint 3).
2. `docs/contexte-long.md`, section « Le PRÉREMPLISSAGE aussi : 286,6 s → 63,8 s sur un prompt de 3 961 jetons » — sources : la sortie des deux commandes `--infer` (non conservée dans un fichier : refais-les si tu veux vérifier, elles prennent ~286 s et ~64 s sur Qwen2.5-0.5B Q8_0 avec `/tmp/prompt4096.txt`) et `/tmp/prefill_gpu.log` (perplexité 9,4335 CPU contre 9,4337 GPU KV à ctx 4 096, 1 023 jetons).
3. Le message de commit `09adea5` et celui de `2ae761c` : disent-ils la même chose que les fichiers ?

Points à vérifier en priorité (ce sont les affirmations qui engagent la feuille de route) :
- **La conclusion « le k est un réglage »** est-elle soutenue par les données ? Compte les oui/NON dans `/tmp/aiguille_rep.log` et vérifie qu'ils correspondent au tableau (3/3, 0/3, 0/3, 3/3) et aux durées citées.
- **La comparaison est-elle valide ?** Les sondes d'une même série utilisent-elles la même fenêtre de corpus ? Le script `/tmp/aig5.sh` passe `4096 0.5,0.5,0.5` — vérifie dans `tools/aiguille.py` que cela fait bien TROIS sondes à trois offsets DIFFÉRENTS (et non trois fois la même).
- **Le « 0/3 à k = 512 »** : le premier balayage (`/tmp/aiguille_k.log`) avait donné NON pour k=512 avec UNE sonde ; les trois nouvelles concordent-elles ?
- **L'affirmation sur `--lot 1`** (« l'attention complète échoue aussi au milieu ») : dans `/tmp/aiguille_k.log`, la ligne « complet(lot 1, milieu) » dit-elle bien NON ? Une seule sonde suffit-elle pour l'affirmer, et le rapport le dit-il ?
- **Le chiffre du préremplissage** (286,6 s → 63,8 s, ×4,5 ; attention 52,6 → 2,2 ms/jeton) : re-mesurable en ~6 min au total ; si tu le refais, donne les valeurs obtenues et l'écart avec celles publiées.
- **La perplexité du préremplissage déporté** (9,4335 / 9,4337) : est-elle reproductible, et l'écart de 2e-5 est-il correctement qualifié ?
- Le rapport dit-il clairement ce qui reste NON mesuré (8 192, 16 384, d'autres modèles, plusieurs codes par sonde) ?

Méthode : pour chaque écart, (a) section citée, (b) chiffre écrit, (c) ce que dit la source, (d) verdict, (e) correction minimale. Tu peux exécuter des commandes de lecture et re-mesurer (les sondes d'aiguille prennent 4 min chacune — n'en lance pas plus de deux ; le préremplissage, 5 min). NE MODIFIE AUCUN fichier. Termine par la liste des écarts classés par gravité, puis par ce que tu as vérifié et trouvé conforme.
Your parent agent id is "bbd6969f-0f70-42b2-8951-64d1f2f36d2e". Before you finish, send your result to that agent with send_message({ agent_id: "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Auditing sprint 4 artifacts — starting with sources and repo state

I'll start by orienting myself in the repo and locating the artifacts and source logs.

- **bash** `{"command": "ls /tmp/aiguille_rep.log /tmp/aiguille_k.log /tmp/aiguille_topk2.log /tmp/prefill_gpu.log /tmp/aig5.sh /tmp/prompt4096.txt 2>&1; echo \"---\"; ls -la /tmp/*.log 2>&1 | head -40", "description": "Check existence of cited source files"}`

  ```
/tmp/aig5.sh
/tmp/aiguille_k.log
/tmp/aiguille_rep.log
/tmp/aiguille_topk2.log
/tmp/prefill_gpu.log
/tmp/prompt4096.txt
---
-rw-r--r--. 1 stephane stephane   5761 24 sep 15:00 /tmp/ab-8075.log
-rw-r--r--. 1 stephane stephane    320 24 sep 15:00 /tmp/ab-after.log
-rw-r--r--. 1 stephane stephane   1657 24 sep 17:08 /tmp/agent-after-fix.log
-rw-r--r--. 1 stephane stephane   1657 24 sep 16:51 /tmp/agent-final.log
-rw-r--r--. 1 stephane stephane   3728 24 sep 15:02 /tmp/agentic.log
-rw-r--r--. 1 stephane stephane    397 25 sep 07:43 /tmp/agentic-test2.log
-rw-r--r--. 1 stephane stephane    378 25 sep 07:41 /tmp/agentic-test.log
-rw-r--r--. 1 stephane stephane   1500 24 sep 16:47 /tmp/agent-offline2.log
-rw-r--r--. 1 stephane stephane   1676 24 sep 16:39 /tmp/agent-offline.log
-rw-r--r--. 1 stephane stephane   1500 24 sep 16:34 /tmp/agent-test-run2.log
-rw-r--r--. 1 stephane stephane    349 24 sep 16:27 /tmp/agent-test-run.log
-rw-r--r--. 1 stephane stephane    659 29 sep 18:00 /tmp/aiguille_1p5b.log
-rw-r--r--. 1 stephane stephane    949 30 sep 16:58 /tmp/aiguille2048_runner.log
-rw-r--r--. 1 stephane stephane    163 29 sep 12:40 /tmp/aiguille30b.log
-rw-r--r--. 1 stephane stephane   10
… [1912 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -15 && echo \"--- STATUS ---\" && git status --porcelain | head -30", "description": "Show recent git log and status"}`

  ```
09adea5 Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point)
2ae761c Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5
9e22ed8 Sprint 3 : cérémonie (aiguille × attention creuse, revue adverse, planning du sprint 4)
470e3e9 Revue adverse du sprint 3 : deux écarts graves, dans les phrases qui commentent les chiffres
d29e043 Correction : `--infer` n'ignore PAS `--lot` (mon grep ne suivait pas la chaîne d'appels)
6ad2bc6 Aiguille × attention creuse : le milieu du contexte est perdu (et le doute sur les projections est instruit)
6633338 « Accord du top-1 : 511/511 » était faux — 497/511, et l'outil ne le disait pas
c752ad4 Le déport des projections est EXACT sur un modèle dense — et déplace la perplexité d'un MoE
b795f09 Sprint 2 : cérémonie (revue adverse autonome, introspection, planning du sprint 3)
a76d8c8 REPRISE : le doute sur les projections est à moitié levé (ctx 512 et 1024 identiques, ctx 256 évalue une autre chose)
1dee0e6 REPRISE : sprint 2 (fusion du top-k, croisement à ~300 clés, le filet testé, le doute sur les projections)
5bc4c0c Grille propre, noyau fusionné dans le moteur, et gpt-oss (les pu
… [300 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading cited logs and the report section under audit

- **read** `{"file_path": "/tmp/aiguille_rep.log"}`
- **read** `{"file_path": "/tmp/aiguille_k.log"}`

  ```
<path>/tmp/aiguille_rep.log</path>
<type>file</type>
<content>
1: ########## complete 3 fenetres
2:      4096        0.50     oui     383.6  prompt 4114 jetons
3:      4096        0.50     oui     326.5  prompt 4114 jetons
4:      4096        0.50     oui     251.5  prompt 4114 jetons
5: ########## k=256 3 fenetres
6:      4096        0.50     NON     244.7  prompt 4114 jetons · [attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo
7:      4096        0.50     NON     237.8  prompt 4114 jetons · [attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo
8:      4096        0.50     NON     237.0  prompt 4114 jetons · [attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo
9: ########## k=1024 3 fenetres
10:      4096        0.50     oui     239.6  prompt 4114 jetons · [attention] --attn-topk 1024 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --l
11:      4096        0.50     oui     253.2  prompt 4114 jetons · [attention] --attn-topk 1024 est IGNORÉ en mode lot (--lot 256) : l'attention pa
… [844 caractères tronqués]
  ```


  ```
<path>/tmp/aiguille_k.log</path>
<type>file</type>
<content>
1: k=512  (lot 256, milieu) :      4096        0.50     NON     274.8  prompt 4114 jetons · [attention] --attn-topk 512 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo
2: k=1024 (lot 256, milieu) :      4096        0.50     oui     241.8  prompt 4114 jetons · [attention] --attn-topk 1024 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --l
3: k=256  (lot 1,   milieu) :      4096        0.50     oui     190.7  prompt 4114 jetons
4: k=1024 (lot 1,   milieu) :      4096        0.50     NON     220.1  prompt 4114 jetons
5: complet(lot 1,   milieu) :      4096        0.50     NON     251.0  prompt 4114 jetons
6: k=1024 (lot 256, prof 0.1) :      4096        0.50     oui     389.4  prompt 4114 jetons · [attention] --attn-topk 1024 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --l
7: === AIG4 FINIE ===

(End of file - total 7 lines)
</content>
  ```

- **bash** `{"command": "cat /tmp/aig5.sh; echo \"=== topk2 ===\"; cat /tmp/aiguille_topk2.log", "description": "Show aig5 script and sprint3 topk log"}`

  ```
#!/bin/bash
# RÉPÉTITION : la grille du sprint 4 a donné des résultats NON monotones en k
# (k=512 échoue, k=1024 réussit ; en --lot 1, k=256 réussit et k=1024 échoue).
# Avec UNE sonde par configuration, on ne peut pas distinguer « l'attention creuse
# échoue » de « cette exécution-là a déraillé ». Trois sondes par configuration,
# avec trois FENÊTRES DE CORPUS différentes (le script avance l'offset de 200 000
# caractères à chaque profondeur listée) : c'est la seule façon de dire si l'effet
# est reproductible.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
M=models/Qwen2.5-0.5B-Q8_0.gguf
J=/tmp/aiguille_rep.log
: > "$J"
serie() {
  local nom=$1; shift
  echo "########## $nom" >> "$J"
  timeout 3600 python3 tools/aiguille.py $M 4096 0.5,0.5,0.5 --n 24 --lot 256 "$@" 2>&1 \
    | grep -E "^ +4096" >> "$J"
}
serie "complete 3 fenetres" 
serie "k=256 3 fenetres" --attn-topk 256
serie "k=1024 3 fenetres" --attn-topk 1024
serie "k=512 3 fenetres" --attn-topk 512
echo "=== REPETITIONS FINIES ===" >> "$J"
=== topk2 ===
ctx 4096 · prof 0.1 · complete   :      4096        0.10     oui     256.5  prompt 4114 jetons
ctx 4096 · prof 0.1 · topk-CPU   :      4096        0.10     oui
… [730 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Locating and reading the report + docs sections under audit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"sprint 4\\|Sprint 4\\|SPRINT 4\\|RÉGLAGE\\|RÉGLAGE\\|k est un\" reports/rapport-aiguille-topk.md | head -40; echo \"=== wc ===\"; wc -l reports/rapport-aiguille-topk.md docs/contexte-long.md", "description": "Find sprint 4  … [19 caractères tronqués]`

  ```
71:## Suite (sprint 4) : le k est un RÉGLAGE, pas une fatalité
117:  sprint 4 reprend la grille là où elle s'arrête.
=== wc ===
  137 reports/rapport-aiguille-topk.md
  575 docs/contexte-long.md
  712 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"286,6\\|286.6\\|63,8\\|63.8\\|9,4335\\|9,4337\\|préremplissage\\|PRÉREMPLISSAGE\\|3961\\|3 961\" docs/contexte-long.md | head -40", "description": "Find prefill section in docs"}`

  ```
41:### a. Le préremplissage — le mur n° 1, et de très loin
46:| contexte | préremplissage estimé, séquentiel |
54:matrice-vecteur). Un préremplissage par tranches de 2 048 jetons relit les poids
94:plus tôt : c'est le préremplissage (§3.a).
111:quelques minutes), puis E4/E5 selon l'usage (décodage long ou préremplissage
299:### Le PRÉREMPLISSAGE aussi : 286,6 s → 63,8 s sur un prompt de 3 961 jetons
301:Mesuré au sprint 4 (Qwen2.5-0.5B Q8_0, prompt de 3 961 jetons, `--lot 256`,
306:| CPU | **286,6 s** (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 |
307:| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s** (62,1 tok/s) | attention **2,2** · matvec+mlp 12,8 |
309:L'attention du préremplissage est **le** poste dominant sur CPU (73 % du temps :
311:pas : à ctx 4 096 et 1 023 jetons, perplexité **9,4335 (CPU)** contre **9,4337
331:### Le préremplissage par lots emprunte le même noyau
346:**×2,8 sur le préremplissage**, perplexité identique au chiffre près. C'est le
494:préremplissage), et **le YaRN déclaré n'est pas la bonne réponse sur du texte
539:   l'identique, ne fait pas un banc d'essai valable, et le préremplissage
542:   et des réponses plus longues — et c'est le préremplissage par 
… [177 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md", "offset": 40, "limit": 98}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md", "offset": 290, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md</path>
<type>file</type>
<content>
40: 
41: **Leçon** : un `grep` qui s'arrête à la fonction qu'on regarde ne suit pas la
42: chaîne d'appels. La vérification se fait dans le code appelé, pas dans l'appelant.
43: 
44: ## La grille
45: 
46: | contexte | profondeur | attention complète | top-k 256 CPU | top-k 256 GPU |
47: |---|---|---|---|---|
48: | 4 096 | 0,1 | **oui** (256,5 s) | **oui** (238,5 s) | **oui** (243,1 s) |
49: | 4 096 | **0,5** | **oui** (246,5 s) | **NON** (242,0 s) | **NON** (267,6 s) |
50: | 4 096 | 0,9 | **oui** (249,9 s) | **oui** (236,4 s) | **oui** (248,3 s) |
51: 
52: Neuf sondes, même modèle, mêmes fenêtres de corpus : le seul point qui échoue est
53: le MILIEU, et il échoue des deux côtés (CPU et GPU).
54: 
55: ## Ce que ça veut dire
56: 
57: 1. **La profondeur médiane est le point dur**, et c'est exactement le phénomène
58:    « perdu au milieu » : la sélection top-k d'une requête, à 4 096 clés, retient
59:    les jetons récents (et les puits d'attention du début) ; une phrase plantée au
60:    milieu n'entre pas dans les 256 premières. L'attention complète, elle, la
61:
… [5009 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
290: Le poste « attention » devient **plat** (3,3 ms/jeton quelle que soit la
291: longueur) là où le CPU croît linéairement : à 32 k il serait à ≈ 180 ms/jeton,
292: à 1 M à ≈ 5,7 s. Le point de croisement est vers **4 000 clés** (en dessous, les
293: lancements et les recopies coûtent plus que le calcul).
294: 
295: Piège de mesure noté au passage : les tampons du noyau étaient alloués à chaque
296: appel — 24 couches × 6 appels CUDA par jeton, mesuré **24,5 ms/jeton** à 512
297: jetons au lieu de 2,9. Les réutiliser a ramené l'attention déportée à 3,2 ms.
298: 
299: ### Le PRÉREMPLISSAGE aussi : 286,6 s → 63,8 s sur un prompt de 3 961 jetons
300: 
301: Mesuré au sprint 4 (Qwen2.5-0.5B Q8_0, prompt de 3 961 jetons, `--lot 256`,
302: `--infer`) :
303: 
304: | chemin | prompt | postes (ms/jeton) |
305: |---|---|---|
306: | CPU | **286,6 s** (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 |
307: | `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s** (62,1 tok/s) | attention **2,2** · matvec+mlp 12,8 |
308: 
309: L'attention du préremplissage est **le** poste dominant sur CPU (73 %
… [2929 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the harness script: offsets, windows, and the top-k/lot interaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/aiguille.py && grep -n \"offset\\|OFFSET\\|200000\\|200_000\\|seed\\|random\\|depth\\|profondeur\" tools/aiguille.py | head -60", "description": "Inspect aiguille.py for offset handling"}`

  ```
181 tools/aiguille.py
5:un code à une profondeur donnée dans un contexte long, puis le redemande.
24:    aiguille.py <modele.gguf> <longueurs> <profondeurs> [options]
53:def sonde(modele, corpus, ctx, profondeur, offset, args):
54:    """Une sonde. `offset` décale la fenêtre de corpus pour varier le texte."""
59:    if offset + besoin > len(corpus):
60:        offset = 0
61:    remplissage = corpus[offset:offset + besoin]
62:    coupe = int(len(remplissage) * profondeur)
121:    ap.add_argument("profondeurs")
148:    profondeurs = [float(x) for x in args.profondeurs.split(",")]
155:    print(f"{'contexte':>9} {'profondeur':>11} {'trouvé':>7} {'secondes':>9}  détail")
157:    offset = 0
159:        for p in profondeurs:
160:            ok, dt, detail = sonde(args.modele, corpus, ctx, p, offset, args)
161:            offset += 200_000          # fenêtre différente à chaque sonde
162:            if offset > len(corpus) - 400_000:
163:                offset = 0
173:            f.write("| contexte | profondeur | trouvé | secondes | détail |\n")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 09adea5 2ae761c | head -60; echo \"=== MSG 09adea5 ===\"; git log -1 --format=%B 09adea5; echo \"=== MSG 2ae761c ===\"; git log -1 --format=%B 2ae761c", "description": "Show commit messages and stats"}`

  ```
commit 09adea5ac96cef6d328e76ed4e03243de5263704
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 00:54:18 2026 -0400

    Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point)
    
    La grille du sprint 3 n'avait qu'UNE sonde par configuration, et le premier balayage
    en k donnait des résultats non monotones (512 échoue, 1 024 réussit) : impossible de
    distinguer « l'attention creuse échoue » de « cette exécution a déraillé ». Trois
    sondes par configuration, trois fenêtres de corpus, 4 096 clés, profondeur 0,5 :
    
    | configuration | trouvé |
    |---|---|
    | attention complète | **3/3** |
    | k = 256 (6,25 %) | **0/3** |
    | k = 512 (12,5 %) | **0/3** |
    | k = 1 024 (25 %) | **3/3** |
    
    Conclusion CORRIGÉE : l'échec au milieu n'est pas une impossibilité structurelle du
    top-k mais un réglage — le seuil est entre 512 et 1 024 clés. L'affirmation du
    sprint 3 (« sans index, l'attention creuse ne peut pas remplacer l'attention
    complète ») était trop forte. La vraie question de feuille de route : comment le k
    nécessaire évolue avec le contexte (s'il reste au quart, l'élagage ne rapporte rien
    à 32
… [2838 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading aiguille.py fully to verify windows and corpus determinism

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Aiguille dans la botte de foin — version 2, celle qui mesure vraiment.
3: 
4: La perplexité ne dit pas si un modèle RETROUVE une information. Ce script plante
5: un code à une profondeur donnée dans un contexte long, puis le redemande.
6: 
7: Ce qui a changé par rapport à la v1 (mesurée et arrêtée) :
8: 
9: 1. **le remplissage est du vrai texte VARIÉ** (`data/wikitext2_test.txt`), et non
10:    la même phrase recopiée jusqu'à la longueur voulue. Un remplissage répété ne
11:    teste rien : le modèle pouvait répondre en devinant la structure. Chaque sonde
12:    prend en plus une FENÊTRE DIFFÉRENTE du corpus, pour que les sondes ne
13:    partagent pas leur remplissage ;
14: 2. **la réponse est longue** (`--n 40` par défaut) : un code peut sortir au
15:    deuxième ou troisième jeton, et s'arrêter à 8 jetons faisait échouer des
16:    sondes que le modèle savait résoudre ;
17: 3. **le préremplissage par lots** (`--lot`) rend chaque sonde abordable : le
18:    moteur ne l'utilisait que pour la perplexité ;
19: 4. le contexte réellement atteint est
… [8466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Tracing the engine's "IGNORÉ en mode lot" warning in Rust source

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"IGNORÉ en mode lot\" --include=*.rs . | head; echo \"=== context ===\"; grep -rn \"est IGNORÉ\" --include=*.rs . | head", "description": "Find the top-k lot warning in source"}`

  ```
./drave-core/src/model.rs:2358:            eprintln!("[attention] --attn-topk {} est IGNORÉ en mode lot (--lot {t}) : \
=== context ===
./drave-core/src/model.rs:2358:            eprintln!("[attention] --attn-topk {} est IGNORÉ en mode lot (--lot {t}) : \
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"t=open('data/wikitext2_test.txt',encoding='utf-8',errors='replace').read(); t=t.replace('@-@','-').replace('@,@',',').replace('@.@','.'); t=' '.join(t.split()); print('len corpus:',len(t)); print('len-400000:',len(t)-400 … [59 caractères tronqués]`

  ```
len corpus: 353778
len-400000: -46222
  ```

### 🤖 Assistant

⏵ Major lead: the corpus is only 353k chars — checking the offset-reset logic impact

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l data/wikitext2_test.txt && git log --oneline -3 -- data/wikitext2_test.txt tools/aiguille.py && echo \"=== rust attn_topk uses ===\" && grep -rn \"attn_topk\\|attn-topk\" --include=*.rs drave-core/src | head -40", "description" … [50 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 359041 25 sep 18:02 data/wikitext2_test.txt
470e3e9 Revue adverse du sprint 3 : deux écarts graves, dans les phrases qui commentent les chiffres
c752ad4 Le déport des projections est EXACT sur un modèle dense — et déplace la perplexité d'un MoE
b97d129 Drave : renommage complet (crate, binaire, variables, documents)
=== rust attn_topk uses ===
drave-core/src/main.rs:359:             mdl.attn_topk, mdl.qk_topk, mdl.moe_topk, mdl.act_topk_proj);
drave-core/src/main.rs:381:        let k = mdl.attn_topk;
drave-core/src/main.rs:383:            "inactif : --attn-topk n'est pas donné"
drave-core/src/main.rs:482:    attn_sinks: usize, attn_topk: usize, qk_topk: usize,
drave-core/src/main.rs:579:            "--attn-topk" => { o.attn_topk = suivant(i).parse().unwrap(); 2 }
drave-core/src/main.rs:674:        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
drave-core/src/main.rs:727:    mdl.attn_topk = attn_topk;
drave-core/src/main.rs:1394:    mdl.attn_topk = opt.attn_topk;
drave-core/src/main.rs:1451:// top-k · renorm · attn_topk · qk_topk · moe_topk · topk_proj[7]
drave-core/src/main.rs:1466:    attn_topk: u32,
drave-core/src/mai
… [3206 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 2320, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2320:                 let b = t[i + half];
2321:                 t[i] = a * c - b * s;
2322:                 t[i + half] = b * c + a * s;
2323:             }
2324:         }
2325:     }
2326: 
2327:     /// **Préremplissage par lots** : `t` jetons d'un coup, aux positions
2328:     /// `pos0..pos0+t`.
2329:     ///
2330:     /// Toute la différence avec `forward` est dans les projections : elles
2331:     /// passent d'un produit matrice-vecteur par jeton à un produit
2332:     /// matrice-matrice pour le lot, donc chaque ligne de poids n'est lue qu'une
2333:     /// fois au lieu de `t` fois (mesuré au noyau : ×2,4 à 16 jetons sur une
2334:     /// matrice 4864 × 896).
2335:     ///
2336:     /// L'attention reste par jeton (elle est causale : le jeton i doit voir le
2337:     /// cache écrit par les jetons < i), mais elle réutilise les Q, K, V calculés
2338:     /// en lot. Les modèles à experts retombent sur le chemin jeton par jeton :
2339:     /// leur regroupement par expert est l'étape suivante.
2340:     pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> 
… [4290 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Found a likely major flaw: corpus too short, offsets reset to 0 every probe

- **bash** `{"command": "python3 - <<'EOF'\ncorpus_len = 353778\noffset = 0\nfor i in range(3):\n    print(f\"sonde {i+1}: offset utilisé = {offset} (fenêtre {offset}:{offset+17603})\")\n    offset += 200_000\n    if offset > corpus_len - 400_000:\n        offset = 0\n        print(f\"   -> garde-fou: {200_000  … [136 caractères tronqués]`

  ```
sonde 1: offset utilisé = 0 (fenêtre 0:17603)
   -> garde-fou: 200000 > -46222 => offset REMIS À 0
sonde 2: offset utilisé = 0 (fenêtre 0:17603)
   -> garde-fou: 600000 > -46222 => offset REMIS À 0
sonde 3: offset utilisé = 0 (fenêtre 0:17603)
   -> garde-fou: 600000 > -46222 => offset REMIS À 0
  ```

- **read** `{"file_path": "/tmp/prefill_gpu.log"}`

  ```
<path>/tmp/prefill_gpu.log</path>
<type>file</type>
<content>
1: CPU      (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4335 sur 1023 tokens
2: GPU KV   (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4337 sur 1023 tokens
3: === PREFILL GPU FINI ===

(End of file - total 3 lines)
</content>
  ```

### 🤖 Assistant

⏵ Hunting the exact prefill commands to re-measure the timings

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"286,6\\|286\\.6\\|prefill_gpu\\|DRAVE_GPU_KV=1\" journal/sessions/ sprints/ 2>/dev/null | head -30", "description": "Search journal for prefill measurement commands"}`

  ```
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:30455:236:### Dans le moteur (`DRAVE_GPU=1 DRAVE_GPU_KV=1`)
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:31307:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && D=./drave-core/target/release/drave; M=models/Qwen2.5-0.5B-Q8_0.gguf; echo \"=== le miroir VRAM est-il refusé avec les clés f16 ? ===\"; DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1 $D $M --ppl /tmp/ids_qwen.txt --ctx  … [413 caractères tronqués]`
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32509:| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32776:drave-core/src/model.rs:900:    /// Miroir VRAM du cache KV, une entrée par couche (`DRAVE_GPU_KV=1`).
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35226:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== B : GPU (top-k déporté) ===\" && DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1 /usr/bin/time -f \"%e s\" ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /
… [8308 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"prompt4096\" . --include=*.md --include=*.sh --include=*.py 2>/dev/null | head -20; echo \"=== tmp scripts ===\"; ls -la /tmp/*.sh 2>/dev/null | tail -20", "description": "Find prompt4096 usage and scripts"}`

  ```
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38195:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nt=open('data/wikitext2_test.txt').read()[:17000]\nopen('/tmp/prompt4096.txt','w').write(t)\nprint('prompt écrit :', len(t), 'caractères')\n\" && timeout 600 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gg … [262 caractères tronqués]`
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38233:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DRAVE_GPU=1 DRAVE_GPU_KV=1 timeout 900 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --prompt \"$(cat /tmp/prompt4096.txt)\" --n 4 --ctx 4608 --lot 256 --threads 16 --temp 0 2>&1 | grep -E \"prompt  :|généré … [130 caractères tronqués]`
=== tmp scripts ===
-rwxr-xr-x. 1 stephane stephane 1088 29 sep 14:32 /tmp/rotation_seuil.sh
-rw-------. 1 stephane stephane 1078 30 sep 15:38 /tmp/run_attack.sh
-rw-------. 1 stephane stephane 1150 30 sep 15:36 /tmp/run_e2e.sh
-rw-------. 1 stephane stephane 1206 30 sep 15:37 /tmp/run_matrix.sh
-rw-------. 1 stephane stephane 2571 30 sep 15:39 /tmp/run_suite2.sh
-rw---
… [1055 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extracting exact prefill commands from the session digest

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '38180,38260p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md", "description": "Read digest around prefill measurement"}`

  ```
```
cérémonie 3 corrigée
61:### 4. ⚠️ Une affirmation fausse, écrite puis corrigée dans le box
100:| 1 | **Où passe le temps d'un prompt ?** Le préremplissage par lots EST actif, mais une sonde de 4 096 jetons coûte 250 s : profiler (lots, attention, projections) et réduire | ≥ 2× sur le temps de prompt à 4 096 jetons, sortie inchangée à la tolérance du chemin par lots (13,1368 → 13,1359) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S; git log --oneline --since=\"2026-09-30 21:49\" | wc -l; git status --short | head -3; sleep 420; date +%H:%M:%S", "description": "Check state and wait for box end", "timeoutMs": 500000}`

  ```
23:01:44
5
 M journal/README.md
23:08:44
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nt=open('data/wikitext2_test.txt').read()[:17000]\nopen('/tmp/prompt4096.txt','w').write(t)\nprint('prompt écrit :', len(t), 'caractères')\n\" && timeout 600 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gg … [262 caractères tronqués]`

  ```
prompt écrit : 17000 caractères
prompt  : 3961 tokens en 286.638 s  (13.8 tok/s, TTFT 72.4 ms)
généré  : 4 tokens
… [5716 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Launching the prefill re-measurement in background (CPU then GPU)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && uptime && ls -l drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf && wc -c /tmp/prompt4096.txt && git log -1 --format='%H %ci' -- tools/aiguille.py && stat -c '%y %n' tools/aiguille.py data/wikitext2_test.txt", "descripti … [46 caractères tronqués]`

  ```
00:56:08  up 9 days 14:08,  2 users,  load average: 7,84, 11,77, 15,67
-rwxr-xr-x. 2 stephane stephane   1798656 30 sep 20:17 drave-core/target/release/drave
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 models/Qwen2.5-0.5B-Q8_0.gguf
17033 /tmp/prompt4096.txt
470e3e9d45819963f3f9c54933d96c8d8adb7235 2026-09-30 23:18:58 -0400
2026-09-30 23:15:54.352004535 -0400 tools/aiguille.py
2026-09-25 18:02:22.675769428 -0400 data/wikitext2_test.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"9.4335\\|9.4337\\|1023\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | tail -20", "description": "Find perplexity measurement command in digest"}`

  ```
36049:lot 8 : perplexité 9.4335 sur 1023 tokens
36050:lot 1 : perplexité 9.4167 sur 1023 tokens
36695:cpu ctx2048 : perplexité 9.4167 sur 1023 tokens
36696:gpu ctx2048 : perplexité 9.4162 sur 1023 tokens
36699:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== CPU (ctx 2048, 1023 jetons) ===\"; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen_long.txt --ctx 2048 --limit 1024 --dense --threads 16 --attn-topk 256 2>&1 | grep -E \"perplexité [0-9] … [359 caractères tronqués]`
36702:=== CPU (ctx 2048, 1023 jetons) ===
36703:=== perplexité 9.4167 sur 1023 tokens (0 événements, 38.0 s) ===
36706:=== perplexité 9.4162 sur 1023 tokens (0 événements, 35.8 s) ===
36853:cpu     1023 : attention 7.17 | 
36854:gpu     1023 : attention 4.62 | 
36961:10. Perf (à titre indicatif, non bloquant) : le fil 0 fait en série la descente (jusqu'à 256 itérations partagées × 4 passes), le balayage exclusif de 1024 cases (1049-1057) et la somme du poison (1084), pendant que 1023 fils attendent — ~3 000 accès partagés sérieux par ligne sur le chemin critique. Un balayage en log(blockDim) pas et une descente coopérative (warp 0) les enlè
… [935 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Starting the ~6 min prefill re-measurement in the background

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c '\nD=./drave-core/target/release/drave\nM=models/Qwen2.5-0.5B-Q8_0.gguf\nJ=/tmp/audit_prefill.log\n: > $J\necho \"=== load avant : $(cut -d\" \" -f1-3 /proc/loadavg) ===\" >> $J\necho -n \"CPU re-mesure (lot 256, ctx 46 … [739 caractères tronqués]`

  ```
started background job bash-89
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '38460,38490p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md", "description": "Read perplexity command context in digest"}`

  ```
- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup /tmp/aig4.sh > /dev/null 2>&1 & sleep 5; cat /tmp/aiguille_k.log 2>/dev/null; date +%H:%M:%S", "description": "Launch sprint 4 needle grid"}`

  ```
k=512  (lot 256, milieu) : 23:44:34
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c '\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nD=./drave-core/target/release/drave\nM=models/Qwen2.5-0.5B-Q8_0.gguf\nJ=/tmp/prefill_gpu.log\n: > $J\necho -n \"CPU      (lot 256, ctx 4096, 1023 jetons) : \" >> $J … [583 caractères tronqués]`

  ```
A/B préremplissage lancé
23:44:46
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 420; echo \"=== aiguille k ===\"; cat /tmp/aiguille_k.log; echo \"=== préremplissage GPU ===\"; cat /tmp/prefill_gpu.log; date +%H:%M:%S", "description": "Check sprint 4 measurements", "timeoutMs": 500000}`

  ```
=== aiguille k ===
k=512  (lot 256, milieu) :      4096        0.50     NON     274.8  prompt 4114 jetons · [attention] --attn-topk 512 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo
k=1024 (lot 256
… [932 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking machine load/client jobs and counting verdicts programmatically

- **bash** `{"command": "ps -eo pid,pcpu,etime,comm,args --sort=-pcpu | head -12; echo \"---\"; nproc", "description": "Inspect running processes and CPU count"}`

  ```
PID %CPU     ELAPSED COMMAND         COMMAND
2565272  764       01:03 drave           ./drave-core/target/release/drave /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf --ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512
2567136 79.0       00:05 drave           ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --prompt   = Robert Boulter =     Robert Boulter is an English film , television and theatre actor . He had a guest @-@ starring role on the television series The Bill in 2000 . This was followed by a starring role in the play Herons written by Simon Stephens , which was performed in 2001 at the Royal Court Theatre . He had a guest role in the television series Judge John Deed in 2002 . In 2004 Boulter landed a role as " Craig " in the episode " Teddy 's Story " of the television series The Long Firm ; he starred alongside actors Mark Strong and Derek Jacobi . He was cast in the 2005 theatre productions of the Philip Ridley play Mercury Fur , which was performed at the Drum Theatre in Plymouth and the Menier Chocolate Factory in London . He was directed by John Tiffany and starred alongside Ben Whishaw , Shane Zaza , Harry Kent , 
… [18520 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\ntxt=open('/tmp/aiguille_rep.log').read().splitlines()\nserie=None; res={}\nfor l in txt:\n    if l.startswith('##########'):\n        serie=l.replace('#','').strip(); res[serie]=[]\n    elif serie and l.strip().startswith('4096'):\n        parts=l.split()\n … [405 caractères tronqués]`

  ```
complete 3 fenetres      oui=3 NON=0  durées=['383.6', '326.5', '251.5']  prof={'0.50'}
k=256 3 fenetres         oui=0 NON=3  durées=['244.7', '237.8', '237.0']  prof={'0.50'}
k=1024 3 fenetres        oui=3 NON=0  durées=['239.6', '253.2', '244.1']  prof={'0.50'}
k=512 3 fenetres         oui=0 NON=3  durées=['240.5', '238.1', '237.8']  prof={'0.50'}

total sondes: 12
  ```

### 👤 Utilisateur

background job bash-89 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c '
D=./drave-core/target/release/drave
M=models/Qwen2.5-0.5B-Q8_0.gguf
J=/tmp/audit_prefill.log
: > $J
echo "=== load avant : $(cut -d" " -f1-3 /proc/loadavg) ===" >> $J
echo -n "CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : " >> $J
timeout 900 $D $M --infer --prompt "$(cat /tmp/prompt4096.txt)" --n 4 --ctx 4608 --lot 256 --threads 16 --temp 0 2>&1 | grep -E "prompt  :|généré|postes" >> $J
echo "=== load milieu : $(cut -d" " -f1-3 /proc/loadavg) ===" >> $J
echo -n "GPU re-mesure (lot 256, ctx 4608, 3961 jetons) : " >> $J
DRAVE_GPU=1 DRAVE_GPU_KV=1 timeout 900 $D $M --infer --prompt "$(cat /tmp/prompt4096.txt)" --n 4 --ctx 4608 --lot 256 --threads 16 --temp 0 2>&1 | grep -E "prompt  :|généré|postes" >> $J
echo "=== load fin : $(cut -d" " -f1-3 /proc/loadavg) ===" >> $J
' >/dev/null 2>&1 & echo "job lancé pid $!") finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Checking what the two commits propagated into journal files

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 09adea5 -- journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md | head -60", "description": "Show 09adea5 journal report diff"}`

  ```
commit 09adea5ac96cef6d328e76ed4e03243de5263704
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 00:54:18 2026 -0400

    Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point)
    
    La grille du sprint 3 n'avait qu'UNE sonde par configuration, et le premier balayage
    en k donnait des résultats non monotones (512 échoue, 1 024 réussit) : impossible de
    distinguer « l'attention creuse échoue » de « cette exécution a déraillé ». Trois
    sondes par configuration, trois fenêtres de corpus, 4 096 clés, profondeur 0,5 :
    
    | configuration | trouvé |
    |---|---|
    | attention complète | **3/3** |
    | k = 256 (6,25 %) | **0/3** |
    | k = 512 (12,5 %) | **0/3** |
    | k = 1 024 (25 %) | **3/3** |
    
    Conclusion CORRIGÉE : l'échec au milieu n'est pas une impossibilité structurelle du
    top-k mais un réglage — le seuil est entre 512 et 1 024 clés. L'affirmation du
    sprint 3 (« sans index, l'attention creuse ne peut pas remplacer l'attention
    complète ») était trop forte. La vraie question de feuille de route : comment le k
    nécessaire évolue avec le contexte (s'il reste au quart, l'élagage ne rapporte rien
    à 32
… [1476 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 2ae761c -- journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md sprints/ | head -80", "description": "Show 2ae761c journal diff"}`

  ```
commit 2ae761cbdb8ed7cfba3ec36562aa1465301698e1
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 23:52:07 2026 -0400

    Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5

diff --git a/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md b/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
index 38eb54c..d5c8318 100644
--- a/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
+++ b/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
@@ -5,14 +5,14 @@
 | Identifiant | `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` |
 | Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
 | Début | 2026-09-28 14:46 |
-| Durée | 57.0 h |
+| Durée | 57.1 h |
 | Tours | 48 |
-| Messages | 2423 |
-| Appels d'outils | 2295 |
+| Messages | 2430 |
+| Appels d'outils | 2302 |
 | Fichiers touchés | 50 |
-| Commandes | 1940 |
+| Commandes | 1947 |
 | Sous-agents | 16 |
-| Commits | 208 |
+| Commits | 209 |
 | Compactages de contexte | 3 |
 
 ## Objectifs déclarés
@@ -2234,7 +2234,7 @@ Fusionner la sélection en un noyau par ligne (8 lancements → 2), supprimer le
 
 ### Tour 48 — Continue en blocs de 2h j
… [2555 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the earlier report context and the GPU crossover section

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md", "limit": 43}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md", "limit": 35, "offset": 266}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md</path>
<type>file</type>
<content>
1: # Rapport — l'attention creuse perd-elle l'information ? (aiguille × `--attn-topk`)
2: 
3: **En une ligne** : à 4 096 clés, l'attention à **256 clés (6,25 %)** des 24 jetons
4: de DÉCODAGE retrouve l'information placée **au début** (profondeur 0,1) et **à la
5: fin** (0,9), mais **pas au milieu** (0,5) — là où l'attention complète la retrouve.
6: CPU et GPU se comportent pareil, ce qui est aussi un contrôle croisé des deux
7: implémentations.
8: 
9: ⚠️ **Portée exacte de la mesure** : avec `--lot 256` (le réglage de cette grille),
10: le moteur **ignore `--attn-topk` au préremplissage** — il l'imprime lui-même
11: (« l'attention par lots est DENSE »). Le k = 256 ne s'applique donc qu'aux 24 jetons
12: générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder
13: en arrière — mais la phrase « une attention qui ne garde que 256 clés » décrit le
14: DÉCODAGE, pas le passage entier. Une grille en `--lot 1` lèverait l'ambiguïté ; elle
15: est au planning (le message d'avertissement du moteur n'est pas lu par
16: `aiguille.py`, qui ne lit la
… [1449 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
266:    partagée ;
267: 2. les partiels n'étaient **pas indexés par tête KV** : les blocs d'une même
268:    tranche s'écrivaient au même endroit, et 7 têtes sur 14 restaient à zéro ;
269: 3. les **échelles** du KV quantifié étaient indexées en éléments au lieu d'être
270:    indexées par vecteur (`vec * nb + i/32`) : écart de 7e7 en int8.
271: 
272: ### Dans le moteur (`DRAVE_GPU=1 DRAVE_GPU_KV=1`)
273: 
274: Les DEUX variables sont nécessaires : c'est `DRAVE_GPU` qui ouvre le pilote (`gpu::instance`),
275: `DRAVE_GPU_KV` qui demande le miroir. Avec la seule seconde, il ne se passe rien — et
276: rien ne le dit, d'où la note.
277: 
278: Le cache est recopié en VRAM par **tranches contiguës** (une copie par couche et
279: par tête KV et par lot, pas une par vecteur), et l'attention par jeton emprunte
280: le noyau dès que la couche est en attention complète (ni fenêtre ni top-k). Le
281: chemin par lots garde le CPU.
282: 
283: | contexte | mode | perplexité | attention (ms/jeton) | durée du balayage |
284: |---|---|---|---|---|
285: | 512 | CPU | 13,1368 | 2,91 | 18,4 s |
… [929 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the re-measurement progress and reading the docs' source attributions

- **bash** `{"command": "cat /tmp/audit_prefill.log 2>/dev/null; echo \"--- procs ---\"; ps -o pid,pcpu,etime,args -C drave --sort=-pcpu | head -5 | cut -c1-160", "description": "Check re-measurement log progress"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- procs ---
    PID %CPU     ELAPSED COMMAND
2567136 1078       00:30 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --prompt   = Robert Boulter =     Robert Boulter is an English 
2565272 1049       01:28 ./drave-core/target/release/drave /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf --ppl /tmp/ids_oss_512.txt --ctx 256 --dense -
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"prefill_gpu\\|aiguille_rep\\|aiguille_k\\|/tmp/\" docs/contexte-long.md reports/rapport-aiguille-topk.md | head -20", "description": "Check source citations in artifacts"}`

  ```
(no output)
  ```

### 🤖 Assistant

⏵ Timeline check: did the 12 probes really run sequentially?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"aig5\\|REPETITIONS\\|aiguille_rep\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | head -20", "description": "Find aig5 launch in digest"}`

  ```
38516:<path>/tmp/aig5.sh</path>
38523:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod +x /tmp/aig5.sh && nohup /tmp/aig5.sh > /dev/null 2>&1 & sleep 10; date +%H:%M:%S; cat /tmp/aiguille_k.log | tail -2", "description": "Launch repetition grid"}`
38531:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 540; echo \"=== répétitions ===\"; cat /tmp/aiguille_rep.log; echo \"=== k sweep ===\"; tail -2 /tmp/aiguille_k.log; date +%H:%M:%S", "description": "Check repetition grid progress", "timeoutMs": 600000}`
38541:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 600; cat /tmp/aiguille_rep.log; date +%H:%M:%S", "description": "Check repetition results", "timeoutMs": 660000}`
38549:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat /tmp/aiguille_rep.log; echo \"---\"; ps -eo pid,etime,args | grep \"aiguille.py\" | grep -v grep | head -2; date +%H:%M:%S", "description": "Check reps and running probes"}`
38572:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 580; cat /tmp/aiguille_rep.log | tail -6; date +%H:%M:%S", "d
… [689 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nd=[383.6,326.5,251.5,244.7,237.8,237.0,239.6,253.2,244.1,240.5,238.1,237.8]\nprint('somme 12 sondes =', sum(d), 's =', round(sum(d)/60,1),'min')\nprint('de 00:10:40 a 00:52 =', (41+20/60)*60, 's')\n\"", "description": "Compare summed durations vs mtime window"}`

  ```
somme 12 sondes = 3134.4 s = 52.2 min
de 00:10:40 a 00:52 = 2480.0 s
  ```

### 🤖 Assistant

⏵ Reading the launch timestamps around the repetition grid

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '38516,38630p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md", "description": "Read repetition grid timeline in digest"}`

  ```
<path>/tmp/aig5.sh</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod +x /tmp/aig5.sh && nohup /tmp/aig5.sh > /dev/null 2>&1 & sleep 10; date +%H:%M:%S; cat /tmp/aiguille_k.log | tail -2", "description": "Launch repetition grid"}`

  ```
00:00:48
k=1024 (lot 1,   milieu) :      4096        0.50     NON     220.1  prompt 4114 jetons
complet(lot 1,   milieu) :
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 540; echo \"=== répétitions ===\"; cat /tmp/aiguille_rep.log; echo \"=== k sweep ===\"; tail -2 /tmp/aiguille_k.log; date +%H:%M:%S", "description": "Check repetition grid progress", "timeoutMs": 600000}`

  ```
=== répétitions ===
########## complete 3 fenetres
=== k sweep ===
complet(lot 1,   milieu) :      4096        0.50     NON     251.0  prompt 4114 jetons
k=1024 (lot 256, prof 0.1) : 00:09:58
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 600; cat /tmp/aiguille_rep.log; date +%H:%M:%S", "description": "Check repetition results", "timeoutMs": 660000}`

  ```
(no output)
[timed out after 6
… [5495 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying corpus length with the real loader and checking log mtimes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport sys; sys.path.insert(0,'tools'); import aiguille\nc = aiguille.charger_corpus()\nprint('len(charger_corpus()) =', len(c))\nprint('seuil du garde-fou len(corpus)-400000 =', len(c)-400000)\nprint('besoin pour ctx  … [386 caractères tronqués]`

  ```
len(charger_corpus()) = 353778
seuil du garde-fou len(corpus)-400000 = -46222
besoin pour ctx 4096 = 17603
offsets utilisés par les 3 sondes : [0, 0, 0]
fenêtres identiques ? True
  ```

- **bash** `{"command": "stat -c '%y  %n' /tmp/aiguille_rep.log /tmp/aiguille_k.log /tmp/prefill_gpu.log; echo \"---\"; tail -c 300 /tmp/audit_prefill.log", "description": "Precise mtimes and re-measurement progress"}`

  ```
2026-10-01 00:52:52.997226638 -0400  /tmp/aiguille_rep.log
2026-10-01 00:10:37.644208171 -0400  /tmp/aiguille_k.log
2026-09-30 23:46:10.720475803 -0400  /tmp/prefill_gpu.log
---
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) :
  ```

### 🤖 Assistant

⏵ Checking the ppl command details and re-measurement progress

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l /tmp/ids_qwen_long.txt /tmp/ids_qwen.txt 2>&1 | head; echo \"--- ids count ---\"; head -c 100 /tmp/ids_qwen_long.txt; echo; wc -w /tmp/ids_qwen_long.txt; echo \"--- digest ppl cmds ---\"; grep -n \"limit 1024\" journal/sessions … [111 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 43220 30 sep 17:13 /tmp/ids_qwen_long.txt
-rw-r--r--. 1 stephane stephane 21380 30 sep 17:11 /tmp/ids_qwen.txt
--- ids count ---
198,284,8397,425,10965,465,284,14731,8397,425,10965,465,374,458,6364,4531,1154,12425,323,33496,12089
1 /tmp/ids_qwen_long.txt
--- digest ppl cmds ---
7973:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && P=\"--ppl /tmp/ids_qwen.txt --ctx 256 --limit 1024 --abits 16 --threads 16\"; printf \"int8 emprunte Q8_0        : \"; ./qtrinet-core/target/release/qtrinet-core models/Qwen2.5-0.5B-Q8_0.gguf $P --dense 2>&1 | grep -oE \"perplexité [ … [705 caractères tronqués]`
9448:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup ./qtrinet-core/target/release/qtrinet-core models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 512 --limit 1024 --dense --threads 8 --profil-neurones --neurones-sortie /tmp/neurones_qwen.txt > /tmp/prof_qwen.out 2>&1 &  … [119 caractères tronqués]`
35217:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== A : CPU (attn-topk 256) ===\" && /usr/bin/time -f \"%e s\" ./drave-core/target/release/drave models
… [1196 caractères tronqués]
  ```

- **bash** `{"command": "tail -c 400 /tmp/audit_prefill.log; echo; ps -o pid,pcpu,etime -C drave --sort=-pcpu | head -4", "description": "Poll re-measurement progress"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : 
    PID %CPU     ELAPSED
2567136 1436       01:15
2565272 1288       02:13
  ```

### 🤖 Assistant

⏵ Proving the twelve probes built byte-identical prompts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport sys, hashlib; sys.path.insert(0,'tools'); import aiguille as A\nc = A.charger_corpus()\ndef prompt(offset):\n    besoin = int(4096*4.2)+400\n    if offset + besoin > len(c): offset = 0\n    r = c[offset:offset+b … [849 caractères tronqués]`

  ```
offsets réels        : [0, 0, 0]
md5 des 3 invites    : ['6a94ff027ad0', '6a94ff027ad0', '6a94ff027ad0']
invites identiques ? : True
offsets visés (0/200k/400k) -> md5 distincts ?
   ['6a94ff027ad0', '5637e27c2a06', '6a94ff027ad0'] => uniques : False
  offset 400000 hors corpus ? True (len = 353778 )
  ```

### 🤖 Assistant

⏵ Polling the CPU re-measurement (loaded machine) and checking source-citation convention

- **bash** `{"command": "sleep 60; tail -c 500 /tmp/audit_prefill.log; echo; ps -o pid,pcpu,etime -C drave --sort=-pcpu | head -4", "description": "Poll CPU measurement after a minute"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"log :\\|/tmp/.*\\.log\\|journal :\" reports/*.md | head -15", "description": "Check how other reports cite log sources"}`

  ```
reports/rapport-compacite-trace.md:233:1. **Le rejeu.** La trace n'est pas qu'un journal : `--flux-forcer` la
reports/rapport-gpt-oss-perplexite.md:206:— le RoPE simple à 8 192 — est en cours (`/tmp/audela_4096.log`).
  ```

### 🤖 Assistant

⏵ Checking measurement output without sleeping

- **bash** `{"command": "cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Read current re-measurement output"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2567136 1574       02:43 drave
2574342 1513       00:57 drave
  ```

### 🤖 Assistant

⏵ Cross-checking the prefill numbers against the roadmap table in the docs

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md", "limit": 30, "offset": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
40: 
41: ### a. Le préremplissage — le mur n° 1, et de très loin
42: 
43: Notre moteur traite **un jeton à la fois** : remplir une fenêtre coûte ce que
44: coûterait de générer la même longueur.
45: 
46: | contexte | préremplissage estimé, séquentiel |
47: |---|---|
48: | 32 768 | 4,5 h |
49: | 131 072 | 31 h |
50: | 1 048 576 | **1 234 h** |
51: 
52: C'est le vrai obstacle, et il ne se contourne pas par la quantification : il faut
53: **traiter des tranches par lots** (produits matrice-matrice au lieu de
54: matrice-vecteur). Un préremplissage par tranches de 2 048 jetons relit les poids
55: une fois par tranche au lieu d'une fois par jeton : à 1 M, 512 passes de 62 Go à
56: 20 Go/s ≈ 26 min, et l'attention devient le poste dominant (O(N²) sur la
57: séquence, ≈ 2·10¹⁵ MACs — quelques heures sur CPU, ~30 min sur les deux GPU avec
58: un vrai noyau d'attention). **C'est le chantier à ouvrir en premier** ; il
59: améliore aussi le temps de premier jeton sur tous les contextes.
60: 
61: ### b. La bande passante du KV — le mur du décodage
62: 
63: À chaque jeton, l'attention 
… [480 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"3 961\\|3961\" docs/ reports/ sprint* journal/README.md 2>/dev/null | head -10", "description": "Find all 3961 occurrences in docs"}`

  ```
docs/contexte-long.md:299:### Le PRÉREMPLISSAGE aussi : 286,6 s → 63,8 s sur un prompt de 3 961 jetons
docs/contexte-long.md:301:Mesuré au sprint 4 (Qwen2.5-0.5B Q8_0, prompt de 3 961 jetons, `--lot 256`,
sprints/03-qualit-de-l-attention-creuse-long-contex.md:121:Profilage du préremplissage (3 961 jetons, lot 256) :
  ```

### 🤖 Assistant

⏵ Checking the sprint 3 planning note for the prefill baseline

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '110,140p' sprints/03-qualit-de-l-attention-creuse-long-contex.md", "description": "Read sprint 3 prefill profiling note"}`

  ```
Trois écarts moyens et sept faibles ont été corrigés aussi : dénominateur de
`compare_logits.py` (il imprimait « 0/255 » sans fichier d'ids — il compte
maintenant les positions réellement comparées et **refuse** un ids trop court),
`--gpu-topk` sans `--attn-topk` (affiché et journalisé alors que le moteur ne fait
rien : refusé), p90, chemins de reproduction, « 6 % » → 6,25 %, et trois
affirmations fausses sur les sondes de 8 192 (une seule lancée, ~9 min par sonde
et non 25, par lots et non jeton par jeton).

### 6. Ce que le sprint 4 a déjà, mesuré : le prompt tombe de 286,6 s à 63,8 s

Profilage du préremplissage (3 961 jetons, lot 256) :

| chemin | prompt | postes (ms/jeton) | détail |
|---|---|---|---|
| CPU | 286,6 s (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 | le terme quadratique domine (73 %) |
| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s (62,1 tok/s)** | attention **2,2** · matvec+mlp 12,8 | **×4,5 sur le prompt** |

C'est le levier du sprint 4, et il existe déjà : l'attention du préremplissage est
le poste dominant sur CPU, et le miroir VRAM la divise par 24.

## Introspection

- **Ce qui a marché** : instruire un doute au lieu de le laisser traîner — deux
  export
… [467 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking sprint boundaries to date the prefill measurement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --format='%h %ci %s' -8 | cut -c1-90; echo \"=== sprint 3 header ===\"; head -5 sprints/03-qualit-de-l-attention-creuse-long-contex.md; echo \"=== sprint3 file history ===\"; git log --format='%h %ci' -2 -- sprints/03-qualit- … [89 caractères tronqués]`

  ```
09adea5 2026-10-01 00:54:18 -0400 Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=102
2ae761c 2026-09-30 23:52:07 -0400 Préremplissage déporté : ×4,5 sur un prompt de 3 961 jet
9e22ed8 2026-09-30 23:44:07 -0400 Sprint 3 : cérémonie (aiguille × attention creuse, revue
470e3e9 2026-09-30 23:18:58 -0400 Revue adverse du sprint 3 : deux écarts graves, dans les
d29e043 2026-09-30 23:01:14 -0400 Correction : `--infer` n'ignore PAS `--lot` (mon grep ne
6ad2bc6 2026-09-30 22:59:03 -0400 Aiguille × attention creuse : le milieu du contexte est 
6633338 2026-09-30 22:25:32 -0400 « Accord du top-1 : 511/511 » était faux — 497/511, et l
c752ad4 2026-09-30 22:17:25 -0400 Le déport des projections est EXACT sur un modèle dense 
=== sprint 3 header ===
# Sprint 3 — Qualité de l'attention creuse à long contexte : aiguille à 4k/8k/16k croisée avec --attn-topk 256, et instruction du doute sur le déport des projections

- **Début** : 21:49 · **Fin prévue** : 23:49 (boxing de 120 min)
- **Objectif** : Qualité de l'attention creuse à long contexte : aiguille à 4k/8k/16k croisée avec --attn-topk 256, et instruction du doute sur le déport des projections
- **Engagement de fin** : dépôt vert (tests + 
… [135 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Poll re-measurement"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2567136 1587       03:02 drave
2574342 1559       01:16 drave
  ```

### 🤖 Assistant

⏵ Searching /tmp for a preserved source of the prefill timings

- **bash** `{"command": "grep -rl \"286.638\\|63.793\" /tmp 2>/dev/null | head; echo \"--- exit $? ---\"; ls -la /tmp/*prefill* /tmp/*prompt* 2>/dev/null", "description": "Search /tmp for preserved prefill output"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Poll re-measurement again"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2574342 1624       02:24 drave
2567136 1617       04:09 drave
  ```

### 🤖 Assistant

⏵ Confirming top-k applies to the decode path in --lot 256

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"forward_lot\\|fn generate\" drave-core/src/model.rs | sed -n '1,40p'", "description": "Locate generate and forward_lot call sites"}`

  ```
922:    /// États imposés pour un LOT entier (`forward_lot`) : `t × hidden`, aplati.
1368:/// Un seul message pour `--attn-topk` ignoré en mode lot (voir `forward_lot`).
2340:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
2852:    /// `forward_lot`, et non à chaque appel — `flux_lot` est appelé deux fois par
3074:        // perplexité répartie 798,3 au lieu de 18,2. `forward_lot` et
3910:    pub fn generate(&mut self, ids: &[u32], n_new: usize, temp: f32, top_p: f32,
3916:        // Préremplissage par lots : `forward_lot` sur des tranches de `self.lot`
3917:        // jetons. `lot == 1` reprend exactement l'ancienne boucle (forward_lot
3926:                let hs = self.forward_lot(&ids[pos..pos + t], pos);
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 60, "offset": 3905}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
3905: 
3906:     /// Génère `n_new` tokens après `ids`. `temp` ≤ 0 ⇒ glouton (déterministe).
3907:     /// Génère `n_new` jetons. `flux` reçoit chaque jeton **dès qu'il est
3908:     /// produit**, ce qui permet de l'afficher sans attendre la fin.
3909:     #[allow(clippy::too_many_arguments)]
3910:     pub fn generate(&mut self, ids: &[u32], n_new: usize, temp: f32, top_p: f32,
3911:                     rep_pen: f32, hist: usize, mut flux: Option<&mut dyn FnMut(u32)>)
3912:                     -> (Vec<u32>, Stats) {
3913:         let t0 = Instant::now();
3914:         let mut last = Vec::new();
3915:         let mut events0 = self.events;
3916:         // Préremplissage par lots : `forward_lot` sur des tranches de `self.lot`
3917:         // jetons. `lot == 1` reprend exactement l'ancienne boucle (forward_lot
3918:         // délègue à `forward` pour un jeton), donc rien ne change par défaut.
3919:         let lot = self.lot.max(1);
3920:         let mut pos = 0usize;
3921:         while pos < ids.len() {
3922:             let t = lot.min(ids.len() - pos);
3923:        
… [2263 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Polling the CPU run

- **bash** `{"command": "cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Poll CPU run status"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2574342 1629       02:33 drave
2567136 1620       04:19 drave
  ```

### 🤖 Assistant

⏵ Preparing the perplexity re-run: checking accepted flags

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"--lot\"\\|\"--dense\"\\|\"--ppl\"\\|\"--limit\"' drave-core/src/main.rs | head -12; echo \"=== usage ===\"; ./drave-core/target/release/drave --help 2>&1 | grep -iE \"lot|dense|ppl|limit\" | head -12", "description": "Veri … [26 caractères tronqués]`

  ```
57:        (opt.ppl, "--ppl"), (opt.infer, "--infer"),
529:            "--ppl" => { o.ppl = true; o.ids_file = Some(suivant(i).clone()); 2 }
571:            "--limit" => { o.limit = suivant(i).parse().unwrap(); 2 }
573:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
605:            "--dense" => { o.dense = true; 1 }
=== usage ===
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
  ```

### 🤖 Assistant

⏵ Polling the CPU measurement

- **bash** `{"command": "cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Poll CPU measurement result"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2574342 1634       02:45 drave
2567136 1624       04:30 drave
  ```

### 🤖 Assistant

⏵ Polling the CPU result again

- **bash** `{"command": "cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Poll CPU measurement"}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2574342 1637       02:53 drave
2567136 1626       04:39 drave
  ```

### 🤖 Assistant

⏵ Waiting out the loaded CPU run

- **bash** `{"command": "sleep 50; cat /tmp/audit_prefill.log; echo \"--- ps ---\"; ps -o pid,pcpu,etime,comm -C drave --sort=-pcpu | head -4", "description": "Wait 50s then poll", "timeoutMs": 70000}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ps ---
    PID %CPU     ELAPSED COMMAND
2574342 1652       03:48 drave
2567136 1638       05:33 drave
  ```

### 🤖 Assistant

⏵ Checking which /tmp files existed around the prefill measurement window

- **bash** `{"command": "find /tmp -maxdepth 1 -newermt \"2026-09-30 23:05\" ! -newermt \"2026-09-30 23:20\" -printf '%TY-%Tm-%Td %TH:%TM  %p\\n' 2>/dev/null | sort | head -20", "description": "List /tmp files from the measurement window"}`

  ```
2026-09-30 23:05  /tmp/rev_ids_100.txt
2026-09-30 23:08  /tmp/prompt4096.txt
2026-09-30 23:18  /tmp/ceremonie3.md
  ```

- **bash** `{"command": "sleep 45; cat /tmp/audit_prefill.log; ps -o pid,etime,comm -C drave --sort=-pcpu | head -4", "description": "Wait and poll again", "timeoutMs": 70000}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) :     PID     ELAPSED COMMAND
2574342       04:37 drave
2567136       06:23 drave
  ```

### 🤖 Assistant

⏵ Waiting for the CPU run to finish

- **bash** `{"command": "sleep 55; cat /tmp/audit_prefill.log; ps -o pid,etime,comm -C drave --sort=-pcpu | head -4", "description": "Wait and poll CPU run", "timeoutMs": 75000}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ids générés : [77238, 572, 264, 46741]
prompt  : 3961 tokens en 371.959 s  (10.6 tok/s, TTFT 93.9 ms)
généré  : 4 tokens en 0.416 s  (9.62 tok/s)
postes (ms/token) : matvec-attn 1.5 | rope 0.0 | attention 71.0 | matvec+mlp 21.2 | total mesuré 93.7
=== load milieu : 35.45 28.93 22.34 ===
GPU re-mesure (lot 256, ctx 4608, 3961 jetons) :     PID     ELAPSED COMMAND
2574342       05:36 drave
2575744       00:57 drave
  ```

### 🤖 Assistant

⏵ CPU done: 372.0 s vs 286.6 s published (machine loaded); waiting on GPU

- **bash** `{"command": "sleep 55; cat /tmp/audit_prefill.log; ps -o pid,etime,comm -C drave --sort=-pcpu | head -4", "description": "Wait for GPU re-measurement", "timeoutMs": 75000}`

  ```
=== load avant : 8.66 11.87 15.68 ===
CPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ids générés : [77238, 572, 264, 46741]
prompt  : 3961 tokens en 371.959 s  (10.6 tok/s, TTFT 93.9 ms)
généré  : 4 tokens en 0.416 s  (9.62 tok/s)
postes (ms/token) : matvec-attn 1.5 | rope 0.0 | attention 71.0 | matvec+mlp 21.2 | total mesuré 93.7
=== load milieu : 35.45 28.93 22.34 ===
GPU re-mesure (lot 256, ctx 4608, 3961 jetons) : --- ids générés : [64750, 1033, 279, 1429]
prompt  : 3961 tokens en 95.941 s  (41.3 tok/s, TTFT 24.2 ms)
généré  : 4 tokens en 0.171 s  (23.34 tok/s)
postes (ms/token) : matvec-attn 1.4 | rope 0.0 | attention 2.5 | matvec+mlp 20.1 | total mesuré 24.0
=== load fin : 35.14 30.51 23.60 ===
    PID     ELAPSED COMMAND
2574342       06:37 drave
  ```

### 🤖 Assistant

⏵ Launching the perplexity re-run (CPU then GPU KV) in background

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c '\nD=./drave-core/target/release/drave\nM=models/Qwen2.5-0.5B-Q8_0.gguf\nIDS=/tmp/ids_qwen_long.txt\nJ=/tmp/audit_ppl.log\n: > $J\necho \"=== load avant : $(cut -d\" \" -f1-3 /proc/loadavg) ===\" >> $J\necho -n \"CPU    … [599 caractères tronqués]`

  ```
started background job bash-90
  ```

### 🤖 Assistant

⏵ Verifying the sweep script and the overlap evidence

- **bash** `{"command": "cat /tmp/aig4.sh 2>/dev/null; echo \"=== aig5 mtime/creation ===\"; stat -c '%y %n' /tmp/aig4.sh /tmp/aig5.sh 2>/dev/null; echo \"=== ppl progress ===\"; cat /tmp/audit_ppl.log 2>/dev/null; ps -o pid,etime,comm -C drave --sort=-pcpu | head -4", "description": "Inspect sweep script and p … [9 caractères tronqués]`

  ```
#!/bin/bash
# L'échec au milieu est-il un RÉGLAGE (k plus grand) ou un mécanisme manquant ?
# 1) le k monte : 256 → 512 → 1024 au décodage (--lot 256)
# 2) tout le passage creux : --lot 1 (le préremplissage suit alors le top-k)
# 3) le bord : la profondeur 0.1 et 0.9 avec k = 1024, pour voir si l'élagage
#    finit par casser ce qui marchait.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
M=models/Qwen2.5-0.5B-Q8_0.gguf
J=/tmp/aiguille_k.log
: > "$J"
sonde() {
  local nom=$1; shift
  echo -n "$nom : " >> "$J"
  timeout 2400 python3 tools/aiguille.py $M 4096 0.5 --n 24 --lot 256 "$@" 2>&1 | tail -1 >> "$J"
}
sonde "k=512  (lot 256, milieu)" --attn-topk 512
sonde "k=1024 (lot 256, milieu)" --attn-topk 1024
sonde "k=256  (lot 1,   milieu)" --attn-topk 256 --lot 1
sonde "k=1024 (lot 1,   milieu)" --attn-topk 1024 --lot 1
sonde "complet(lot 1,   milieu)" --lot 1
sonde "k=1024 (lot 256, prof 0.1)" --attn-topk 1024
echo "=== AIG4 FINIE ===" >> "$J"
=== aig5 mtime/creation ===
2026-09-30 23:44:22.201720149 -0400 /tmp/aig4.sh
2026-10-01 00:00:33.565434919 -0400 /tmp/aig5.sh
=== ppl progress ===
=== load avant : 28.66 29.37 23.44 ===
CPU      (lot 256, ctx 4096, 1023 jetons) :    
… [76 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-90 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c '
D=./drave-core/target/release/drave
M=models/Qwen2.5-0.5B-Q8_0.gguf
IDS=/tmp/ids_qwen_long.txt
J=/tmp/audit_ppl.log
: > $J
echo "=== load avant : $(cut -d" " -f1-3 /proc/loadavg) ===" >> $J
echo -n "CPU      (lot 256, ctx 4096, 1023 jetons) : " >> $J
timeout 900 $D $M --ppl $IDS --ctx 4096 --limit 1024 --dense --threads 16 --lot 256 2>&1 | grep -E "perplexité" >> $J
echo -n "GPU KV   (lot 256, ctx 4096, 1023 jetons) : " >> $J
DRAVE_GPU=1 DRAVE_GPU_KV=1 timeout 900 $D $M --ppl $IDS --ctx 4096 --limit 1024 --dense --threads 16 --lot 256 2>&1 | grep -E "perplexité" >> $J
echo "=== load fin : $(cut -d" " -f1-3 /proc/loadavg) ===" >> $J
echo "FINI" >> $J
' >/dev/null 2>&1 & echo "ppl relancé") finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Identifying the still-running drave process and polling ppl

- **bash** `{"command": "ps -o pid,etime,args -p 2574342 2>/dev/null | cut -c1-120; echo \"=== ppl ===\"; cat /tmp/audit_ppl.log; echo \"=== drave procs ===\"; ps -o pid,etime,args -C drave --sort=-pcpu | cut -c1-100 | head -5", "description": "Identify drave processes and ppl status"}`

  ```
PID     ELAPSED COMMAND
2574342       07:10 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --chat --flux --prompt = Rob
=== ppl ===
=== load avant : 28.66 29.37 23.44 ===
CPU      (lot 256, ctx 4096, 1023 jetons) : === drave procs ===
    PID     ELAPSED COMMAND
2574342       07:10 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --chat -
2576414       00:20 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_q
  ```

### 🤖 Assistant

⏵ Checking whether the report flags other models as unmeasured

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"modèle\\|1,5B\\|30B\\|0,5B\\|0.5B\" reports/rapport-aiguille-topk.md", "description": "Grep model mentions in the report"}`

  ```
12:générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder
20:`--gpu-topk`. Modèle : Qwen2.5-0.5B-Instruct Q8_0, 24 jetons de réponse,
26:| modèle | contexte | secondes par sonde |
28:| Qwen2.5-0.5B | 4 096 | ~250 |
30:| Qwen3-30B-A3B | 2 048 | ~670 |
52:Neuf sondes, même modèle, mêmes fenêtres de corpus : le seul point qui échoue est
113:* 8 192 et 16 384 : non mesurés dans ce box. Le taux mesuré du 0.5B est de 58 à
134:python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256
135:python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256
136:python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256 --gpu-topk
  ```

### 🤖 Assistant

⏵ Polling the perplexity re-run

- **bash** `{"command": "sleep 50; cat /tmp/audit_ppl.log; echo \"--- procs ---\"; ps -o pid,etime,args -C drave --sort=-pcpu | cut -c1-80 | head -4", "description": "Wait and poll ppl re-run", "timeoutMs": 75000}`

  ```
=== load avant : 28.66 29.37 23.44 ===
CPU      (lot 256, ctx 4096, 1023 jetons) :     1023 tokens notés — perplexité cumulée 9.433  (20.0 tok/s)
=== perplexité 9.4335 sur 1023 tokens (0 événements, 51.2 s) ===
GPU KV   (lot 256, ctx 4096, 1023 jetons) :     1023 tokens notés — perplexité cumulée 9.434  (29.9 tok/s)
=== perplexité 9.4337 sur 1023 tokens (0 événements, 34.2 s) ===
=== load fin : 35.17 31.30 24.64 ===
FINI
--- procs ---
    PID     ELAPSED COMMAND
2574342       08:21 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.g
  ```

### 🤖 Assistant

⏵ Writing up findings and sending the self-contained result to the parent

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "REVUE ADVERSE SPRINT 4 — terminée. Aucun fichier du dépôt modifié (seuls des logs neufs dans /tmp : /tmp/audit_prefill.log, /tmp/audit_ppl.log). Toutes les sondes/prefill relancés ont été mesurés sous charge (load 8,7 → 35,4 ; un job g … [10468 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Rédaction du verdict final

## Verdict de la revue adverse — sprint 4

Aucun fichier du dépôt modifié. Deux re-mesures lancées (préremplissage, perplexité) ; toutes deux sous **charge** (load 8,7 → 35,4 ; un ppl gpt-oss-120b 16 fils + une sonde aiguille d'un autre agent tournaient en parallèle sur 40 cœurs). Logs neufs : `/tmp/audit_prefill.log`, `/tmp/audit_ppl.log`.

---

### ÉCARTS

**1. GRAVE — « trois fenêtres de corpus différentes » est faux**
- **(a)** `reports/rapport-aiguille-topk.md:76-79` + en-têtes « fenêtre 1/2/3 » (:81-86) ; commit `09adea5` (« trois fenêtres de corpus »).
- **(b)** « trois **fenêtres de corpus différentes** (l'outil avance son offset de 200 000 caractères à chaque profondeur listée) ».
- **(c)** `tools/aiguille.py:161-163` : après **chaque** sonde, `offset += 200_000` puis `if offset > len(corpus) - 400_000 { offset = 0 }`. Or `aiguille.charger_corpus()` rend **353 778** caractères (`data/wikitext2_test.txt`, inchangé depuis le 25/09) → le seuil vaut **−46 222** → la remise à zéro se déclenche **toujours**. Offsets réellement utilisés : **[0, 0, 0]**. Preuve par le vrai module : les 3 invites reconstruites ont le **même md5** (`6a94ff027ad0` ×3). Même sans le garde-fou, l'offset 400 000 est hors corpus (400 000 + 17 603 > 353 778) : au mieux **2** fenêtres distinctes étaient possibles. Les 12 lignes du log disent d'ailleurs toutes « prompt 4114 jetons ».
- **(d)** **FAUX.** Les « 3/3 » et « 0/3 » sont trois répétitions de la **même invite**. La justification annoncée (« avec une seule sonde, impossible de distinguer *l'attention creuse échoue* de *cette exécution a déraillé* ») n'est pas servie : trois fois la même invite ne dit rien de la généralité inter-fenêtres.
- **(e)** Écrire « trois **répétitions** de la même invite (offset remis à 0 par le garde-fou ; corpus de 353 778 car. < 400 000 supposés) », remplacer « fenêtre 1/2/3 » par « répétition 1/2/3 », borner la conclusion à cette fenêtre — ou corriger l'outil et refaire la grille. Le commentaire de `/tmp/aig5.sh` porte la même erreur.

**2. GRAVE (feuille de route) — la grille n'est pas celle de l'objectif du sprint**
- **(a)** section « Suite (sprint 4) » ; `sprints/04-…md`.
- **(b)** « l'échec au milieu n'est PAS une impossibilité structurelle du top-k — c'est un **réglage** ».
- **(c)** L'objectif du sprint exige « Grille en **--lot 1** (tout le passage creux) et k = 256/512/1024 ». `aig5.sh` et `aiguille_k.log` tournent en **--lot 256**, où `--attn-topk` est **IGNORÉ au préremplissage** (`model.rs:2357-2359` ; préremplissage `forward_lot`, décodage `forward` → top-k sur les **24 jetons générés**, 0,58 %).
- **(d)** La conclusion est **plus générale que la mesure** (décodage seul). Le fichier porte l'avertissement en tête (:9-17) et le bullet :126-129, mais **la section sprint 4 ne redit ni « --lot 256 » ni « décodage seul »**, et la grille `--lot 1` — exigée par la revue adverse du sprint 3 *et* par l'objectif du sprint 4 — n'a pas été faite.
- **(e)** Ajouter dans la section : « grille en `--lot 256` : seul le décodage est élagué ; la grille `--lot 1` reste à faire ».

**3. MOYEN — l'écart « 2e-5 » n'est pas qualifié**
- **(a)** `docs/contexte-long.md:311-312` ; message de commit `2ae761c`.
- **(b)** « perplexité **9,4335 (CPU)** contre **9,4337 (GPU KV)**, soit **2e-5** ».
- **(c)** 9,4337 − 9,4335 = **2e-4 en absolu** ; 2e-4/9,4335 = **2,1e-5 en relatif**. Les deux valeurs sont imprimées à 4 décimales (absolu connu à ±1e-4).
- **(d)** **TROMPEUR tel qu'écrit** : « 2e-5 » ne vaut que comme écart **relatif**.
- **(e)** « soit un écart **relatif** de 2,1e-5 (2e-4 sur les valeurs affichées) ».

**4. MOYEN — « Ce que ce rapport ne dit pas » contredit la nouvelle section**
- **(a)** `rapport:111-129`.
- **(b)** :123-125 « l'effet d'un k plus grand (512, 1 024) : **non mesuré**. C'est la première expérience à faire ensuite » ; :118-122 « un seul code et **une seule fenêtre** par (contexte, profondeur) ».
- **(c)** La section :71-101 mesure k = 512/1 024 et **affirme trois fenêtres**.
- **(d)** **INCOHÉRENT** (bullets non mis à jour) ; ironiquement, c'est le bullet « une seule fenêtre » qui est vrai.
- **(e)** Réécrire ces deux bullets (k mesuré ; fenêtre unique) et ajouter « autres modèles non mesurés », absent aujourd'hui.

**5. MOYEN — le contrôle `--lot 1` repose sur UNE sonde, non dit**
- **(a)** `rapport:103-105`.
- **(b)** « en `--lot 1`, l'attention **COMPLÈTE** échoue aussi au milieu (251,0 s, « NON ») ».
- **(c)** `/tmp/aiguille_k.log:5` : `complet(lot 1, milieu) : … NON 251.0` — **une seule** sonde (tout ce balayage est à une sonde par point).
- **(d)** Exact mais présenté **sans n=1**, alors qu'il sert à écarter la comparaison `--lot 1`. Le même balayage donne k=256(lot 1)=**oui** et k=1024(lot 1)=**NON** : inversion cohérente avec la mise en garde, mais n=1 aussi.
- **(e)** Ajouter « (une sonde) ».

**6. MOYEN — « Mesuré au sprint 4 » est faux d'environ 30 minutes**
- **(a)** `docs:299-302`.
- **(b)** « **Mesuré au sprint 4** (… prompt de 3 961 jetons, `--lot 256`, `--infer`) ».
- **(c)** Le run CPU suit le `date` 23:08:44 et le run GPU se termine sur `date` 23:15:20 (digest, sorties brutes 286.638 s / 63.793 s) → mesurés à **23:09-23:15**, dans le box **sprint 3** (21:49-23:49). Seul `/tmp/prefill_gpu.log` (23:44:46-23:46:10) est dans le sprint 4. `sprints/03` dit d'ailleurs « Ce que le sprint 4 a **déjà**, mesuré ».
- **(d)** Inexact. **(e)** « mesuré à la fin du sprint 3, avant le sprint 4 ».

**7. FAIBLE — aucune source citée, commande du sprint 4 absente**
- **(a)** les deux artefacts ; « Reproduire » `rapport:131-137`.
- **(b)** Aucun renvoi à `/tmp/aiguille_rep.log`, `/tmp/aiguille_k.log`, `/tmp/aiguille_topk2.log`, `/tmp/prefill_gpu.log`.
- **(c)** Ces logs existent et contiennent les chiffres ; d'autres rapports citent leurs `/tmp` (ex. `rapport-gpt-oss-perplexite.md:206`). La commande de la grille k (`4096 0.5,0.5,0.5 --n 24 --lot 256 --attn-topk 256|512|1024`, script `/tmp/aig5.sh` non commité) n'est nulle part.
- **(d)** Règle « chaque chiffre publié doit avoir une source » **non satisfaite dans les artefacts**. **(e)** Citer les logs + ajouter la commande.

**8. FAIBLE — durées de la rangée « complète » gonflées par la concurrence**
- **(a)** `rapport:83`.
- **(b)** « oui (383,6 s) | oui (326,5 s) | oui (251,5 s) ».
- **(c)** `aig5.sh` lancé à **00:00:48** (digest) alors que le balayage k tournait encore (mtime de `/tmp/aiguille_k.log` = **00:10:37** ; label de la dernière sonde visible à 00:09:58) → ~10 min à deux jobs 16 fils. Les autres séries (~237-253 s) tournaient seules.
- **(d)** Les **verdicts** ne sont pas affectés, mais les durées ne sont pas comparables entre rangées comme le tableau le suggère. **(e)** Le noter ou refaire la rangée au calme.

**9. FAIBLE — « fenêtres décalées »** : `rapport:21` et la docstring `tools/aiguille.py:12` (« Chaque sonde prend une FENÊTRE DIFFÉRENTE ») sont faux (même cause que l'écart 1).

---

### RE-MESURES (question posée)

| | publié | re-mesuré | écart |
|---|---|---|---|
| préremplissage CPU | 286,638 s (13,8 tok/s) · attention 52,6 · matvec+mlp 18,4 | **371,959 s** (10,6 tok/s) · **71,0** · **21,2** | **+29,8 %** |
| préremplissage GPU KV | 63,793 s (62,1 tok/s) · attention 2,2 · matvec+mlp 12,8 | **95,941 s** (41,3 tok/s) · **2,5** · **20,1** | **+50,4 %** |
| ratio | ×4,49 | **×3,88** | −13 % |
| perplexité CPU / GPU KV | 9,4335 / 9,4337 (1023 jetons) | **9,4335 / 9,4337** | **identiques** |

Prompt reproduit à l'identique (3961 jetons). Le `×4,5` est donc **sensible à la charge** ; les conditions du run publié ne sont écrites nulle part. La perplexité, elle, se **reproduit au chiffre près** (51,2 s / 34,2 s sous charge). Observation annexe : à temp 0 et invite identique, CPU et GPU KV génèrent des continuations **différentes** (`[77238,572,264,46741]` vs `[64750,1033,279,1429]`) — « la qualité ne bouge pas » vaut au sens de la perplexité, pas au sens « jetons identiques » (ids non journalisés à l'origine).

---

### CLASSEMENT PAR GRAVITÉ

1. **GRAVE** — « trois fenêtres de corpus différentes » : faux (3 fois la même invite, offsets 0/0/0). *(écart 1)*
2. **GRAVE** — la conclusion « le k est un réglage » est tirée d'une grille `--lot 256` (décodage seul) alors que l'objectif du sprint exigeait `--lot 1`. *(écart 2)*
3. **MOYEN** — « 2e-5 » non qualifié (absolu 2e-4). *(3)*
4. **MOYEN** — bullets « non mesuré / une seule fenêtre » en contradiction avec la section. *(4)*
5. **MOYEN** — contrôle `--lot 1` à une sonde, n=1 non dit. *(5)*
6. **MOYEN** — « Mesuré au sprint 4 » : mesuré en sprint 3. *(6)*
7. **FAIBLE** — sources non citées, commande du sprint 4 absente. *(7)*
8. **FAIBLE** — durées « complète » mesurées en concurrence. *(8)*
9. **FAIBLE** — « fenêtres décalées » / docstring de l'outil. *(9)*

### VÉRIFIÉ ET CONFORME

- `/tmp/aiguille_rep.log` : complete **3/3 oui**, k=256 **0/3**, k=1024 **3/3**, k=512 **0/3** — exactement le tableau et le message de commit ; **les 12 durées citées sont identiques au log, chiffre pour chiffre**.
- Premier balayage : k=512 NON (274,8 s), k=1024 oui (241,8 s) → la non-monotonie annoncée est bien dans `/tmp/aiguille_k.log` ; les 3 nouvelles sondes **concordent** avec elle (k=512 : 4/4 NON ; k=1024 : 4/4 oui).
- La ligne `complet(lot 1, milieu)` dit bien **NON** (251,0 s), citée exactement.
- Portée « `--lot 256` : top-k ignoré au préremplissage, 24 jetons / 0,58 % » : **exacte** (`model.rs:2350-2371`).
- Toutes les valeurs dérivées du préremplissage : 286,638/63,793 = 4,49 → « ×4,5 » ; 3961/286,638 = 13,8 ; 3961/63,793 = 62,1 ; 52,6/72,2 = **73 %** ; 52,6/2,2 = 23,9 → « ÷24 » : **exactes**.
- `/tmp/prefill_gpu.log` porte exactement 9,4335 et 9,4337 (ctx 4096, 1023 jetons) ; **reproductibles**.
- Ratios k/contexte : 256/4096 = 6,25 %, 512/4096 = 12,5 %, 1024/4096 = 25 % : exacts ; seuil dans (512, 1024] correct pour le cas testé.
- Messages `09adea5` et `2ae761c` : disent la même chose que les fichiers, **y compris les deux défauts partagés** (« trois fenêtres », « 2e-5 » non qualifié) — aucune divergence message/fichier par ailleurs.
- Le rapport dit clairement « 8 192 / 16 384 non mesurés » et « un seul code par sonde » ; il **ne dit pas** « autres modèles non mesurés » (grille 0,5B uniquement).

