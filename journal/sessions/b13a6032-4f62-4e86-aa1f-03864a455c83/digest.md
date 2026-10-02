# Session DSH — relecture

- identifiant : `b13a6032-4f62-4e86-aa1f-03864a455c83`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:48
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. NE MODIFIE AUCUN FICHIER (lecture seule stricte).

MISSION : dépouiller l'EN-TÊTE (docstring de module, commentaires d'en-tête, constantes de tête) ET LA DÉFINITION DE LA LIGNE DE COMMANDE (argparse : `add_argument`, `help=`, `nargs`, `choices`, `default`) de ces 24 scripts Python, dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ :
aiguille.py, analyse_empreinte.py, analyse_experts_statique.py, analyse_flux.py, clusters_moe.py, compare_etats.py, compare_logits.py, convertir_clusters.py, diff_flux.py, flux_codec.py, harmony_canonique.py, hc_synthetique.py, lire_meta_gguf.py, mesurer_lecture_experts.py, mla_synthetique.py, pair_factice.py, profil_flux.py, proxy_latence.py, session_report.py, telecharger_modeles.py, trace_compacite.py, verifier_formats.py, vision_mtmd.py, vision_ref.py.

MÉTHODE : pour chaque fichier, utilise `read` (les 60-110 premières lignes couvrent en général le docstring + imports + argparse), puis `grep -n "add_argument\|argparse\|ArgumentParser\|def main\|__main__" fichier` pour repérer les arguments définis plus bas, et lis les blocs correspondants. Lis AUSSI les fonctions principales (signatures + docstrings) si elles révèlent le rôle de l'outil.

FORMAT DE SORTIE (texte brut, dense, pas d'introduction), un bloc par fichier :
### chemin/fichier.py  (N lignes)
- Rôle (d'après le docstring, en 1-3 phrases, cite le docstring si parlant)
- Usage/positional args : ...
- Options CLI : `--xxx` (type, default, help exact entre guillemets) — fichier:ligne
- Constantes/vocabulaire notable défini en tête (noms de modes, formats, seuils, chemins par défaut) — fichier:ligne
- Formats de fichiers lus/écrits (extensions, JSON fields exposés) si visible
N'invente rien ; si le rôle est ambigu, cite le texte source. Sois exhaustif et cite les numéros de ligne. Aucune modification de fichier.
Your parent agent id is "f2de810a-b765-444d-b3cc-d8fce1ba2105". Before you finish, send your result to that agent with send_message({ agent_id: "f2de810a-b765-444d-b3cc-d8fce1ba2105", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire des 24 scripts et de leur taille avant lecture ciblée

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && wc -l aiguille.py analyse_empreinte.py analyse_experts_statique.py analyse_flux.py clusters_moe.py compare_etats.py compare_logits.py convertir_clusters.py diff_flux.py flux_codec.py harmony_canonique.py hc_synthetique.py lire_ … [272 caractères tronqués]`

  ```
219 aiguille.py
   208 analyse_empreinte.py
   244 analyse_experts_statique.py
    95 analyse_flux.py
   224 clusters_moe.py
    84 compare_etats.py
   109 compare_logits.py
   525 convertir_clusters.py
    91 diff_flux.py
   158 flux_codec.py
    72 harmony_canonique.py
    98 hc_synthetique.py
   117 lire_meta_gguf.py
    81 mesurer_lecture_experts.py
   250 mla_synthetique.py
   140 pair_factice.py
    78 profil_flux.py
    54 proxy_latence.py
   341 session_report.py
   197 telecharger_modeles.py
   432 trace_compacite.py
   108 verifier_formats.py
   159 vision_mtmd.py
   162 vision_ref.py
  4246 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && grep -n \"add_argument\\|ArgumentParser\\|argparse\\|def main\\|__main__\" aiguille.py analyse_empreinte.py analyse_experts_statique.py analyse_flux.py clusters_moe.py compare_etats.py compare_logits.py convertir_clusters.py di … [351 caractères tronqués]`

  ```
aiguille.py:34:import argparse
aiguille.py:125:def main():
aiguille.py:126:    ap = argparse.ArgumentParser()
aiguille.py:127:    ap.add_argument("modele")
aiguille.py:128:    ap.add_argument("longueurs")
aiguille.py:129:    ap.add_argument("profondeurs")
aiguille.py:130:    ap.add_argument("--n", type=int, default=40, help="jetons générés (réponse)")
aiguille.py:131:    ap.add_argument("--threads", type=int, default=16)
aiguille.py:132:    ap.add_argument("--lot", type=int, default=256, help="lot de préremplissage")
aiguille.py:133:    ap.add_argument("--timeout", type=int, default=7200)
aiguille.py:134:    ap.add_argument("--gpu", action="store_true", help="DRAVE_GPU=1 (déport des projections)")
aiguille.py:135:    ap.add_argument("--gpu-kv", action="store_true", help="DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)")
aiguille.py:140:    ap.add_argument("--attn-topk", type=int, default=0,
aiguille.py:142:    ap.add_argument("--gpu-topk", action="store_true",
aiguille.py:144:    ap.add_argument("--journal", default="")
aiguille.py:218:if __name__ == "__main__":
analyse_empreinte.py:29:import argparse
analyse_empreinte.py:67:def main():
analyse_empreinte.py:68:    ap = argparse.ArgumentPar
… [5723 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des en-têtes du premier lot de scripts

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py", "limit": 150}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_empreinte.py", "limit": 90}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py", "limit": 60}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_flux.py"}`

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
19:    ⚠️ et depuis le sprint 4, le décal
… [6836 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_empreinte.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Chiffrer l'empreinte mémoire d'un MoE depuis une trace de routage.
3: 
4:     # 1. produire la trace (modèle en clusters ou GGUF ordinaire)
5:     DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave \\
6:         <modele|dossier> --ppl <ids.txt> --ctx 2048 --limit 2048 --dense --threads 10 --lot 1
7: 
8:     # 2. l'analyser
9:     python3 tools/analyse_empreinte.py /tmp/routage.txt
10:     python3 tools/analyse_empreinte.py /tmp/routage.txt --modele deepseek41
11: 
12: La trace est un texte : « couche jeton expert1 expert2 … ». Rien n'est deviné :
13: tout ce qui suit est calculé sur les appels réellement effectués.
14: 
15: Ce que l'outil rend, et pourquoi chaque chiffre compte :
16: 
17: * **la courbe succès/empreinte par couche** — combien d'experts garder pour
18:   servir X % des appels. C'est la seule mesure qui dimensionne un cache ;
19: * **le verdict sur l'allocation non uniforme** — la même courbe, mais avec les
20:   experts distribués par gain marginal, pour voir si cibler certaines couches
21:   paie (mes
… [2968 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Analyse STATIQUE des experts d'un MoE : que portent les poids eux-mêmes.
3: 
4: Les traces de routage disent quels experts sont *appelés*. Ce script regarde ce
5: qu'ils *sont* : deux experts aux poids presque identiques sont redondants, et
6: l'un des deux peut disparaître — c'est une économie d'empreinte qu'aucune trace
7: ne peut révéler.
8: 
9:     python3 tools/analyse_experts_statique.py <modele.gguf> --couches 0,12,24,36
10: 
11: Trois mesures, et ce que chacune cherche :
12: 
13: * **similarité entre experts** (intra-couche) — des experts jumeaux ? Si deux
14:   experts d'une même couche font la même chose, n'en stocker qu'un divise leur
15:   empreinte par deux ;
16: * **profil de SOURCES** — la norme de chaque colonne d'entrée. Deux experts qui
17:   écoutent les mêmes dimensions d'entrée ont la même source ;
18: * **profil de DESTINATIONS** — la norme de chaque ligne de sortie. Deux experts
19:   qui écrivent dans les mêmes dimensions ont la même destination.
20: 
21: Un couple d'experts dont les sources ET les destina
… [1556 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_flux.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Analyse PURE d'une trace de flux : ce que la vision appelle « voir le modèle
3: neurone par neurone », mais chiffré par couche et sans exécuter le moteur.
4: 
5: Ce que l'outil répond, et pourquoi ces questions-là :
6: 
7: * **quelle couche est creuse** ? C'est la décision push/pull du projet (le
8:   croisement mesuré est à ~22 % de densité) — mais elle se prend PAR COUCHE, pas
9:   pour le modèle entier ;
10: * **quels neurones sont PERSISTANTS** (actifs dans presque tous les jetons) ?
11:   Ceux-là ne bénéficient d'aucune sparsité : les compter dit combien de
12:   « toujours là » porte le modèle ;
13: * **les mêmes neurones dominent-ils d'une couche à l'autre** ? Un recouvrement
14:   élevé des top-k voisins voudrait dire qu'une direction unique traverse la pile.
15: 
16: Usage : analyse_flux.py <trace> [<trace2> ...] [--top 100]
17: """
18: import struct
19: import sys
20: 
21: 
22: def lire(chemin):
23:     with open(chemin, "rb") as f:
24:         assert f.read(4) == b"DRVF"
25:         struct.unpack("<H", f.read(2))
26:         n_lay
… [3051 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Poursuite: fins des scripts déjà entamés + lot suivant

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py", "offset": 151, "limit": 70}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_empreinte.py", "offset": 90, "limit": 120}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py", "offset": 165, "limit": 80}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py", "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py</path>
<type>file</type>
<content>
151:     if args.attn_topk < 0:
152:         ap.error("--attn-topk doit être positif (0 = attention complète)")
153: 
154:     corpus = charger_corpus()
155:     longueurs = [int(x) for x in args.longueurs.split(",")]
156:     profondeurs = [float(x) for x in args.profondeurs.split(",")]
157:     print(f"aiguille v2 : {args.modele}")
158:     print(f"  remplissage : {CORPUS} ({len(corpus)} caractères), fenêtres décalées")
159:     topk = f" · attn-topk {args.attn_topk}" if args.attn_topk else " · attention COMPLÈTE"
160:     gpu = ("top-k déporté" if args.gpu_topk
161:            else ("KV " if args.gpu_kv else ("proj " if args.gpu else "non")))
162:     print(f"  lot {args.lot} · {args.n} jetons de réponse · GPU {gpu}{topk}")
163:     print(f"{'contexte':>9} {'profondeur':>11} {'trouvé':>7} {'secondes':>9}  détail")
164:     lignes = []
165:     offset = 0
166:     fenetres = set()
167:     # Pas = BESOIN d'une sonde : les fenêtres sont alors contiguës et
168:     # non recouvrantes, ce qui en donne len(corpus)/besoin (une vingtaine à
169:     # 4 096 jetons avec le corpus ac
… [3516 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_empreinte.py</path>
<type>file</type>
<content>
90: 
91:     # --- courbe globale par couche -----------------------------------------
92:     print()
93:     print("=== EMPREINTE : experts à garder pour servir X % des appels ===")
94:     print(f"{'objectif':>9} " + " ".join(f"{p:>6}%" for p in (50, 70, 80, 90, 95, 99)))
95:     seuils = (0.50, 0.70, 0.80, 0.90, 0.95, 0.99)
96:     besoins = {p: [] for p in seuils}
97:     for l in couches:
98:         f = collections.Counter()
99:         for exps in trace[l].values():
100:             f.update(exps)
101:         a = sum(f.values())
102:         cum = 0
103:         trouve = {}
104:         for i, (_, c) in enumerate(f.most_common(), 1):
105:             cum += c
106:             for p in seuils:
107:                 if p not in trouve and cum >= p * a:
108:                     trouve[p] = i
109:         for p in seuils:
110:             besoins[p].append(trouve.get(p, len(f)))
111:     moy = {p: sum(v) / len(v) for p, v in besoins.items()}
112:     print(f"{'experts':>9} " + " ".join(f"{moy[p]:>7.1f}" for p in seuils))
113:     print(f"{'% du total':>9} " + " ".
… [4684 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py</path>
<type>file</type>
<content>
165:         return np.frombuffer(octets[:n_lignes * n_cols * 4],
166:                              dtype=np.float32).reshape(n_lignes, n_cols)
167:     if ttype == 1:                        # F16
168:         return f16(octets[:n_lignes * n_cols * 2]).reshape(n_lignes, n_cols)
169:     raise ValueError(f"type {ttype} non géré par ce script")
170: 
171: 
172: def main():
173:     ap = argparse.ArgumentParser(description=__doc__,
174:                                  formatter_class=argparse.RawDescriptionHelpFormatter)
175:     ap.add_argument("modele")
176:     ap.add_argument("--couches", default="0,12,24,36,47")
177:     ap.add_argument("--lignes", type=int, default=16,
178:                     help="lignes de sortie lues par expert (16 par défaut)")
179:     ap.add_argument("--seuil", type=float, default=0.90,
180:                     help="similarité au-delà de laquelle deux experts sont jumeaux")
181:     args = ap.parse_args()
182: 
183:     g = Lecteur(args.modele)
184:     arch = g.meta.get("general.architecture", "?")
185:     n_exp = g.meta.get(f"{ar
… [3533 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Découpage des MoE en clusters — à partir d'une trace de routage réelle.
3: 
4: Le moteur écrit une ligne par (couche, jeton) avec les experts retenus :
5: `DRAVE_TRACE_EXPERTS=/tmp/trace.txt drave <modele> --ppl <ids> --limit N --lot L`
6: 
7: Ce script répond à la question de placement : **quels experts s'allument
8: ENSEMBLE ?** Les compteurs d'usage disent quels experts sont chauds ; ils ne
9: disent pas lesquels sont chauds en même temps, et c'est pourtant ce qui décide si
10: un jeton peut être servi par UN nœud ou doit en interroger quatre.
11: 
12: Trois mesures, et une comparaison qui les rend honnêtes :
13: 
14: * **couverture** : part des k experts d'un jeton qui tiennent dans son meilleur
15:   cluster (1,0 = un seul nœud suffit) ;
16: * **ventilation** (fan-out) : nombre de clusters nécessaires pour couvrir 90 % des
17:   experts d'un jeton (1,0 = le meilleur cas possible) ;
18: * **équilibre** : taille des clusters (un cluster géant ne compte pas comme un
19:   bon découpage) ;
20: * **témoin** : les mêmes mesures avec des clust
… [2018 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la suite clusters_moe + compare_etats + compare_logits + tête convertir_clusters

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py", "offset": 135, "limit": 90}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_etats.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_logits.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py</path>
<type>file</type>
<content>
135:         "ventilation_moyenne": sum(ventilations) / len(ventilations),
136:         "ventilation_max": max(ventilations),
137:         "taille_min": min(tailles.values()),
138:         "taille_max": max(tailles.values()),
139:     }
140: 
141: 
142: def main():
143:     ap = argparse.ArgumentParser()
144:     ap.add_argument("trace")
145:     ap.add_argument("--clusters", type=int, default=8,
146:                     help="nombre de groupes visés (nœuds ou GPU disponibles)")
147:     ap.add_argument("--json", default="")
148:     ap.add_argument("--graine", type=int, default=1234)
149:     args = ap.parse_args()
150: 
151:     par_couche = lire(args.trace)
152:     couches = sorted(par_couche)
153:     ne = 1 + max(e for j in par_couche.values() for ex in j.values() for e in ex)
154:     n_jetons = len(par_couche[couches[0]])
155:     print(f"trace : {len(couches)} couches × {n_jetons} jetons · {ne} experts · "
156:           f"{len(next(iter(par_couche.values()))[0])} par jeton")
157:     print(f"découpage visé : {args.clusters} clusters\n")
158: 
159:     resultat = 
… [3703 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_etats.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Compare les états intermédiaires de Drave à ceux de llama.cpp, tenseur par tenseur.
3: 
4: Deux formats en entrée :
5: 
6: * **Drave** — `DRAVE_DUMP_COUCHES=<préfixe>` écrit des f32 bruts :
7:   `<préfixe>-<nom>-<couche>-<position>.bin`, sans en-tête.
8: * **llama.cpp** — `REF_DUMP=<préfixe> ./tools/ref_logits …` écrit
9:   `<préfixe>-<nom>-<couche>.bin` avec un en-tête `REFD`, `ndim`, `ne[4]`, puis
10:   les f32 dans l'ordre ggml (une colonne par position).
11: 
12: La comparaison porte sur les **vecteurs entiers**, pas sur huit valeurs : c'est
13: ce qui distingue « ça a l'air proche » de « c'est le même calcul ».
14: 
15: Usage :
16:     python3 tools/compare_etats.py <préfixe_drave> <préfixe_ref> <nom> <couche> <positions>
17: 
18: Exemple :
19:     python3 tools/compare_etats.py /tmp/v4flash /tmp/ref_v4flash l_last 0 0,1,2,3
20: """
21: import struct
22: import sys
23: 
24: 
25: def lire_drave(chemin):
26:     with open(chemin, "rb") as f:
27:         b = f.read()
28:     return list(struct.unpack(f"<{len(b) // 4}f", b))
29: 
30: 
31: 
… [2545 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_logits.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Compare deux fichiers de logits au format :
3:    int32 n_vocab, int32 n_pos, puis n_pos lignes de n_vocab f32 (petit-boutiste).
4: 
5: Usage : compare_logits.py <notre.bin> <reference.bin> [ids.txt]
6: 
7: Rend : par position, la perte (NLL) de chacun, l'écart de NLL, le rang du jeton
8: cible dans chacun, et l'accord du top-1. C'est ce qui localise une divergence :
9: une erreur d'embedding ou de norme se voit dès la position 0 ; une erreur de
10: position (RoPE) fait croître l'écart avec la position ; une erreur de MoE ou de
11: tête fait décrocher toutes les positions d'un coup.
12: """
13: import struct, sys, math
14: 
15: try:
16:     import numpy as np
17: except ImportError:
18:     np = None
19: 
20: 
21: def lire(chemin):
22:     with open(chemin, 'rb') as f:
23:         n_vocab, n_pos = struct.unpack('<ii', f.read(8))
24:         data = f.read(n_pos * n_vocab * 4)
25:     assert len(data) == n_pos * n_vocab * 4, f"{chemin} tronqué"
26:     if np is not None:
27:         a = np.frombuffer(data, dtype='<f4').reshape(n_pos, n_vocab
… [3944 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Convertisseur GGUF → « modèle éclaté en clusters », un fichier par cluster.
3: 
4: **Pourquoi.** Notre mode d'opération ne lit que les experts qu'un jeton allume, et
5: les modèles MoE publient leurs experts dans UN tenseur par couche
6: (`blk.N.ffn_gate_exps.weight [n_experts, …]`). Un nœud qui n'héberge que 16 experts
7: sur 128 lit donc un fichier de 18 Go pour en utiliser un huitième. Ici, chaque
8: cluster devient un **fichier GGUF autonome** : on l'ouvre seul, en mmap, et on ne
9: lit que sa tranche.
10: 
11: **Ce que le convertisseur NE fait pas** : il ne requantifie rien. Les octets des
12: poids sont copiés tels quels (les blocs de quantification sont alignés sur l'axe
13: des experts, donc une tranche d'expert est une plage d'octets exacte). Aucune perte,
14: aucune conversion, aucun choix de format de rechange.
15: 
16: **Sortie** (dans un dossier) :
17: 
18:     commun.gguf          ce qui n'est pas un expert : embeddings, sortie, attention,
19:                          normes, routeur de chaque couche
20:     cluster-00.gg
… [1703 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture convertir_clusters CLI + diff_flux + flux_codec + harmony_canonique

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py", "limit": 90, "offset": 340}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/diff_flux.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/flux_codec.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/harmony_canonique.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py</path>
<type>file</type>
<content>
340:                          f"{n_couches} couches × {n_exp} experts")
341:     chemin = os.path.join(dossier, "mapping.tsv")
342:     with open(chemin, "w", encoding="utf-8") as fo:
343:         fo.write("# drave-clusters-mapping v1\n")
344:         fo.write(f"# n_couches {n_couches} · n_experts {n_exp} · clusters {K}"
345:                  f" · experts_par_cluster {n_exp // K}\n")
346:         fo.write("# couche\tlocal\tglobal\tcluster\n")
347:         for couche, local, g, c in lignes:
348:             fo.write(f"{couche}\t{local}\t{g}\t{c}\n")
349:     print(f"mapping.tsv · {len(lignes)} entrées · {n_couches} couches · "
350:           f"{n_exp} experts · {K} clusters")
351: 
352: 
353: def main():
354:     ap = argparse.ArgumentParser()
355:     ap.add_argument("source")
356:     ap.add_argument("dossier")
357:     ap.add_argument("--clusters", type=int, default=8)
358:     ap.add_argument("--trace", default="", help="trace de routage (ordre des experts)")
359:     ap.add_argument("--mode", choices=["experts", "couches"], default="experts")
360:     ap.add_argu
… [3489 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/diff_flux.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Diff de deux traces de **flux d'activation** (format DRVF).
3: 
4: C'est l'outil qui manquait à la vision : deux exécutions du même modèle, et on
5: veut savoir non pas « la perplexité a bougé » mais **où** le flux diverge, à
6: quelle couche, à quel jeton, et de combien.
7: 
8: Usage : diff_flux.py <traceA> <traceB> [--top 8]
9: """
10: import struct
11: import sys
12: 
13: 
14: def lire(chemin):
15:     with open(chemin, "rb") as f:
16:         assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
17:         version, = struct.unpack("<H", f.read(2))
18:         n_layer, hidden = struct.unpack("<II", f.read(8))
19:         listes = {}
20:         while True:
21:             b = f.read(2)
22:             if len(b) < 2:
23:                 break
24:             couche, = struct.unpack("<H", b)
25:             if couche == 0xFFFF:
26:                 break
27:             pos, n, echelle = struct.unpack("<IIf", f.read(12))
28:             actifs = {}
29:             for _ in range(n):
30:                 i, v = struct.unpack("<Ih", f.read(6
… [2612 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/flux_codec.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2).
3: 
4: Le format de trace et le contrat d'échange de la phase 3 sont le MÊME format :
5: une liste d'activation est ce qu'un nœud distant doit recevoir pour continuer le
6: calcul. Ce fichier est la deuxième implémentation de ce format — la première est
7: en Rust (`--trace-flux`) — et c'est ce qui permet de dire qu'il est sans
8: ambiguïté : deux implémentations indépendantes, un aller-retour identique.
9: 
10: Structure :
11:     en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
12:     liste     u16 couche · u32 position · u32 n_actifs · f32 echelle
13:               puis n_actifs × ( u32 indice · i16 valeur )          [v1]
14:               puis n_actifs × ( u8 écart · i16 valeur )            [v2]
15:                    l'écart de 255 annonce l'indice ABSOLU sur u16
16:     fin       u16 0xFFFF
17: 
18: v2 : les indices sont écrits par ÉCARTS (la liste est triée). Mesuré sur une trace
19: réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2
… [5708 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/harmony_canonique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Construit un identifiant de perplexité au format harmony CANONIQUE.
3: 
4: Le montage forcé `<|start|>assistant<|channel|>final<|message|>texte` est hors
5: distribution : le modèle attend d'abord le canal `analysis` (mesuré : p=0,9999
6: contre 0,0001 pour `final`). Ce script construit donc la séquence telle que
7: l'implémentation officielle la produirait : message système complet, tour
8: utilisateur, puis un canal `analysis` court, puis le canal `final` qui porte le
9: texte à noter.
10: 
11: Sortie : /tmp/harmony_canonique.ids (identifiants) et /tmp/harmony_canonique.dep
12: (indice du premier jeton de contenu), pour que la perplexité du contenu seul
13: puisse être recalculée depuis les logits exportés.
14: """
15: import subprocess, sys, os
16: 
17: Q = "/home/stephane/Data13TB/stephane/GitHub/Drave/drave-core/target/release/drave"
18: M = "/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf"
19: 
20: DEB, FIN, MSG, CANAL = 200006, 200007, 200008, 200005
21: 
22: 
23: def encode(texte, nom):
24:     """Passe par
… [2495 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture hc_synthetique + lire_meta_gguf + mesurer_lecture_experts + mla_synthetique

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/hc_synthetique.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lire_meta_gguf.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_lecture_experts.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py", "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/hc_synthetique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Référence **numpy** des hyper-connexions de DeepSeek-V4, et valeurs-témoins.
3: 
4: Les formules sont recopiées des opérations ggml de
5: `llama.cpp/src/models/deepseek4.cpp` (`build_hc_pre`, `build_hc_sinkhorn`,
6: `build_hc_post`, `build_hc_head`), **pas** de l'implémentation Rust : c'est ce
7: qui rend la comparaison utile. Les mêmes formules sont écrites deux fois, dans
8: deux langages — un écart se voit.
9: 
10: Ce que le script imprime est collé dans le test Rust
11: `model::tests_hc::hyper_connexions_conforme_a_la_reference` : petite dimension
12: (`hc = 4`, `h = 3`) et poids entiers, pour que le test se relise à la main.
13: 
14: Usage :  python3 tools/hc_synthetique.py
15: """
16: import numpy as np
17: 
18: HC, H = 4, 3
19: EPS = 1e-6           # hyper_connection.epsilon (V4.1)
20: ITERS = 20           # hyper_connection.sinkhorn_iterations (V4.1)
21: 
22: 
23: def rms_norm_sans_poids(x, eps):
24:     """`ggml_rms_norm` SEUL : aucune échelle apprise, contrairement à nos rmsnorm."""
25:     return x / np.sqrt(np.mean(x * x) + eps
… [4051 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/lire_meta_gguf.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Lit les métadonnées d'un GGUF (en-tête seul) et imprime les clés demandées.
3: 
4: Pourquoi un outil séparé : le moteur expose `--tensors` (inventaire) et
5: `--config` (résumé), mais ni l'un ni l'autre ne montre une **liste** de
6: métadonnées — et certaines décisions d'architecture tiennent à une liste
7: (`compress_ratios` : quelles couches sont compressées, et à quel ratio).
8: 
9: Usage :
10:     python3 tools/lire_meta_gguf.py <fichier.gguf> [motif ...]
11: 
12: Sans motif, imprime toutes les clés et leurs valeurs (tronquées).
13: """
14: import struct
15: import sys
16: 
17: TYPES = {0: "u8", 1: "i8", 2: "u16", 3: "i16", 4: "u32", 5: "i32",
18:          6: "f32", 7: "bool", 8: "str", 9: "array", 10: "u64", 11: "i64", 12: "f64"}
19: FIXES = {0: ("<B", 1), 1: ("<b", 1), 2: ("<H", 2), 3: ("<h", 2), 4: ("<I", 4),
20:          5: ("<i", 4), 6: ("<f", 4), 7: ("<?", 1), 10: ("<Q", 8), 11: ("<q", 8),
21:          12: ("<d", 8)}
22: 
23: 
24: class Lecteur:
25:     def __init__(self, chemin):
26:         self.f = open(chemin, "rb")
27: 
28: 
… [3698 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_lecture_experts.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Lectures d'experts : série contre parallèle, sur un VRAI fichier froid.
3: 
4:     tools/mesurer_lecture_experts.py <shard.gguf> [nb_blocs] [nb_fils]
5: 
6: Pourquoi : le chargeur d'experts lit aujourd'hui les blocs un par un, en
7: s'appuyant sur le défaut de page du mmap. Le disque de cette machine a été
8: mesuré à **5,37 Go/s avec un lecteur et 31 Go/s avec seize** — donc si le défaut
9: de page sérialise, il y a un facteur 5 à prendre. Mais « il y a un facteur à
10: prendre » n'est pas une mesure, et le cache de pages a déjà fait mentir quatre
11: mécanismes de prélecture sur des modèles qui tenaient en RAM.
12: 
13: Ici on force le froid avec `posix_fadvise(DONTNEED)` sur les plages visées, et on
14: compare deux passes sur des blocs DIFFÉRENTS de même taille (comparaison
15: appariée) : une en touchant les pages une par une, l'autre en répartissant les
16: blocs entre `nb_fils` fils.
17: """
18: import mmap
19: import os
20: import sys
21: import threading
22: import time
23: 
24: PAGE = 4096
25: 
26: 
27: def toucher(mm, b
… [2313 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Modèle MLA synthétique + référence numpy — le harnais du chantier 5.
3: 
4: MLA (attention latente, DeepSeek-V2/V3) n'est pas testable en l'état : aucun
5: modèle MLA en GGUF sur cette machine (le « deepseek-r1-distill » local est un
6: Qwen dense). Ce script fabrique donc un modèle minuscule dont les poids sont
7: aléatoires mais les FORMES correctes, l'écrit en GGUF, et calcule une référence
8: indépendante en numpy — c'est elle que le moteur devra retrouver.
9: 
10: Pourquoi c'est un vrai test : la référence est écrite à partir des formules, pas
11: du code Rust ; si les deux tombent d'accord sur un modèle dont le cache KV est
12: LATENT (une seule tête de 128 + 32 valeurs par jeton au lieu de n_head × 192),
13: alors l'implémentation est validée sur ce qu'elle a de spécifique.
14: 
15: Usage :
16:     mla_synthetique.py --sortie /tmp/mla_minuscule.gguf --dossier /tmp/mla_ref
17: """
18: import argparse
19: import json
20: import os
21: import struct
22: 
23: import numpy as np
24: 
25: # -----------------------------------------------
… [2364 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture mla_synthetique (sortie/main) + pair_factice + profil_flux + proxy_latence

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py", "limit": 80, "offset": 171}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pair_factice.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/profil_flux.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/proxy_latence.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py</path>
<type>file</type>
<content>
171:     for nom in noms:
172:         t = p[nom]
173:         dims = dims_gguf(t.shape)
174:         infos.append((nom, dims, 0, decalage))       # type 0 = F32
175:         decalage += t.nbytes
176:     with open(chemin, "wb") as f:
177:         f.write(b"GGUF")
178:         f.write(struct.pack("<IQQ", 3, len(noms), len(kv)))
179:         for cle, typ, val in kv:
180:             ecrire_chaine(f, cle)
181:             f.write(struct.pack("<I", typ))
182:             if typ == 8:
183:                 ecrire_chaine(f, val)
184:             elif typ == 4:
185:                 f.write(struct.pack("<I", val))
186:             elif typ == 6:
187:                 f.write(struct.pack("<f", val))
188:             elif typ == 9:
189:                 f.write(struct.pack("<IQ", 8, len(val)))     # tableau de chaînes
190:                 for v in val:
191:                     ecrire_chaine(f, v)
192:             else:
193:                 raise ValueError(typ)
194:         for nom, dims, typ, off in infos:
195:             ecrire_chaine(f, nom)
196:             f.write(struct.pack
… [2436 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pair_factice.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Pair factice du protocole de flux (v2) : il ÉCOUTE et DIT ce qu'il reçoit.
3: 
4: Pourquoi cet outil : un banc à deux nœuds qui « marche » peut cacher un
5: protocole faux — c'est exactement ce qui est arrivé avec un flux de 919 canaux
6: là où le modèle en a 896. Un pair qui parle le protocole sans calculer le modèle
7: rend visible ce que l'autre bout envoie vraiment : tailles, positions, modes,
8: réglages. Il répond un flux de la dimension demandée pour que le pilote continue.
9: 
10:     python3 tools/pair_factice.py <port> [dimension]
11: """
12: import socket, struct, sys
13: 
14: MAGIE = 0x44525631
15: TETE = 79   # en-tête v4 : magie, version, mode, plage, position, n, échelle,
16:             # niveaux, seuil, top-k, renorm, 7 top-k par projection, 3 top-k globaux
17: MODES = {0: "dense f32", 1: "listes quantifiées", 2: "blocs (i8 + écarts)",
18:          3: "lot dense (t états × dimension)", 4: "lot en listes (mode 2 par état)"}
19: 
20: 
21: def lire_tout(sock, n):
22:     buf = b""
23:     while len(buf) < n:
24:         morceau
… [6428 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/profil_flux.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Profilage par neurone à partir d'une trace de flux (format DRVF).
3: 
4: Ce que la vision demande, rendu calculable : « quels neurones s'allument, à
5: quelle fréquence, avec quelle magnitude » — par couche, depuis n'importe quelle
6: trace, sans instrumenter le moteur autrement.
7: 
8: Usage : profil_flux.py <trace> [--couche N] [--top 6] [--csv sortie.csv]
9: """
10: import struct
11: import sys
12: 
13: 
14: def lire(chemin):
15:     with open(chemin, "rb") as f:
16:         assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
17:         struct.unpack("<H", f.read(2))
18:         n_layer, hidden = struct.unpack("<II", f.read(8))
19:         listes = []
20:         while True:
21:             b = f.read(2)
22:             if len(b) < 2:
23:                 break
24:             couche, = struct.unpack("<H", b)
25:             if couche == 0xFFFF:
26:                 break
27:             pos, n, echelle = struct.unpack("<IIf", f.read(12))
28:             actifs = []
29:             for _ in range(n):
30:                 i, v = struct
… [2188 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/proxy_latence.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien
3: distant coûte à un découpage de modèle.
4: 
5: Pourquoi : sur localhost, l'attente du pair vaut 1,01× le calcul local — c'est un
6: plancher optimiste. Une VM Colab est à quelques dizaines de millisecondes, et la
7: phase 3.3 demande « à partir de quel débit le découpage gagne ». Le débit n'est
8: jamais le problème (0,25 Mbit/s) ; la latence, si. Ce relais la rend réglable.
9: 
10:     python3 tools/proxy_latence.py <port_écoute> <hôte_cible:port> [délai_ms]
11: """
12: import socket, sys, threading, time
13: 
14: 
15: def relais(src, dst, delai):
16:     try:
17:         while True:
18:             donnees = src.recv(65536)
19:             if not donnees:
20:                 break
21:             if delai:
22:                 time.sleep(delai)
23:             dst.sendall(donnees)
24:     except OSError:
25:         pass
26:     finally:
27:         for s in (src, dst):
28:             try:
29:                 s.shutdown(socket.SHUT_RDWR)
30:             except OS
… [1039 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture session_report + telecharger_modeles + trace_compacite + verifier_formats

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py", "limit": 70}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py", "limit": 65, "offset": 277}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/telecharger_modeles.py", "limit": 70}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/telecharger_modeles.py", "limit": 80, "offset": 118}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Produit, pour chaque session DSH, un rapport qui reconstitue son essence et
3: démontre le travail accompli, étape par étape.
4: 
5: Sortie, à côté du digest brut :
6: 
7:   journal/sessions/<id>/rapport.md   la synthèse structurée de la session
8:   journal/README.md                  l'index des sessions
9: 
10: Ce que le rapport contient, et pourquoi :
11: 
12:   1. fiche      — identité, durée, volumes : de quoi situer la session
13:   2. demandes   — ce qui a été demandé, tour par tour, verbatim
14:   3. déroulé    — pour chaque tour : les actions (fichiers, commandes, délégations)
15:                   puis la synthèse produite. C'est la démonstration du travail.
16:   4. travail    — tables des fichiers créés/modifiés, des commandes, des sous-agents
17:   5. mesures    — les lignes de résultat qui portent un chiffre mesuré
18:   6. erreurs    — ce qui a échoué, et où
19:   7. commits    — ce qui a été inscrit dans l'histoire du dépôt
20: 
21: Usage :
22:   python3 tools/session_report.py [--repo DIR] [--session ID] [--quiet]
23: """

… [1794 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py</path>
<type>file</type>
<content>
277:               f"{len(a['erreurs'])} sorties en erreur ou divergentes. Les premières :", ""]
278:         for tour, e in a["erreurs"][:15]:
279:             L += [f"- **T{tour}** : {e.replace(chr(10),' ')[:200]}"]
280:         L += [""]
281: 
282:     if a["commits"]:
283:         L += ["## 6. Commits", ""]
284:         for c in a["commits"]:
285:             m = re.search(r"-m\s+[\"'](.{0,160})", c)
286:             L += [f"- {m.group(1) if m else c[:160]}"]
287:         L += [""]
288:     return "\n".join(L) + "\n"
289: 
290: 
291: def main() -> int:
292:     ap = argparse.ArgumentParser()
293:     ap.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
294:     ap.add_argument("--session", default=None)
295:     ap.add_argument("--quiet", action="store_true")
296:     args = ap.parse_args()
297: 
298:     repo = Path(args.repo)
299:     dsh = Path(os.environ.get("DSH_HOME", Path.home() / ".dsh"))
300:     slug = "--" + str(repo).strip("/").replace("/", "-") + "--"
301:     src = dsh / "sessions" / slug
302:     if not src.is_dir():
303:     
… [2235 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/telecharger_modeles.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Télécharge les modèles LOURDS, par tranches, avec reprise.
3: 
4: Pourquoi par tranches : le pont Xet de Hugging Face refuse un GET plein sur le
5: fichier de 365,7 Go de `antirez/deepseek-v4.1-flash-gguf` (HTTP 400) alors qu'il
6: sert très bien une requête `Range` (HTTP 206). Mesuré, pas supposé. La découpe a
7: un second mérite : une coupure réseau ne coûte que la tranche en cours.
8: 
9: Le NVMe ne sert plus qu'aux fichiers que NOUS produisons : les modèles bruts vont
10: sur le disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf`).
11: 
12: Usage :
13:     telecharger_modeles.py --manifeste tools/manifeste_modeles_lourds.json
14:     telecharger_modeles.py --seulement Kimi-K2.7-Code-UD-IQ1_M
15:     telecharger_modeles.py --etat          # où en est chaque fichier
16: """
17: import argparse
18: import json
19: import os
20: import shutil
21: import subprocess
22: import sys
23: import time
24: 
25: RACINE = "https://huggingface.co"
26: CHUNK = 256 << 20          # 256 Mo
27: DEST_DEFAUT = "/home/stephane/Data13TB/st
… [1728 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/telecharger_modeles.py</path>
<type>file</type>
<content>
118:     return os.path.getsize(dest) >= octets
119: 
120: 
121: def libre_go(chemin):
122:     return shutil.disk_usage(chemin).free / 1e9
123: 
124: 
125: def main():
126:     ap = argparse.ArgumentParser()
127:     ap.add_argument("--manifeste", default="tools/manifeste_modeles_lourds.json")
128:     ap.add_argument("--dest", default=DEST_DEFAUT)
129:     ap.add_argument("--seulement", default="")
130:     ap.add_argument("--etat", action="store_true")
131:     ap.add_argument("--journal", default="/tmp/telechargement_lourds.log")
132:     args = ap.parse_args()
133: 
134:     entrees = json.load(open(args.manifeste, encoding="utf-8"))
135:     if args.seulement:
136:         entrees = [e for e in entrees if e["nom"] == args.seulement]
137:         if not entrees:
138:             print(f"aucune entrée nommée {args.seulement}")
139:             return 1
140: 
141:     def journal(texte):
142:         ligne = f"{time.strftime('%H:%M:%S')}  {texte}"
143:         print(ligne, flush=True)
144:         with open(args.journal, "a", encoding="utf-8") as f:
145:         
… [2701 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture trace_compacite + verifier_formats + vision_mtmd + vision_ref

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/trace_compacite.py", "limit": 70}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/trace_compacite.py", "limit": 75, "offset": 275}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_formats.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/vision_mtmd.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/trace_compacite.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Chiffre ce que coûterait une trace DRVF v1 sous plusieurs encodages.
3: 
4: Le problème
5: -----------
6: Sur le DISQUE, une trace coûte 6 octets par neurone actif : indice u32
7: (4 octets) + valeur i16 (2 octets), plus les en-têtes de listes. Sur le RÉSEAU,
8: le transport est descendu à ~2 octets par neurone actif : indice u8 par écarts
9: (255 = échappement vers l'indice absolu u16), valeur i8, et une échelle par bloc
10: de 32 canaux. Le même contenu coûte donc trois fois plus cher sur le disque que
11: sur le câble. Cet outil le chiffre, poste par poste.
12: 
13: La lecture du format est celle de `tools/flux_codec.py` — l'implémentation de
14: référence, validée par un aller-retour identique contre le Rust. Cet outil ne la
15: réimplémente pas : il ne fait que compter des octets sur les listes décodées.
16: 
17: Variantes comparées
18: -------------------
19:     actuel          ce que le fichier fait réellement (taille mesurée)
20:     écarts+i16      indices par écarts + valeurs i16 + échelle f32 par liste
21:                     
… [2160 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/trace_compacite.py</path>
<type>file</type>
<content>
275: 
276: def corps_tableau(nom, v, actifs, reference):
277:     return (f"{nom:<24}{nb(v['total']):>14}{dec(v['total'] / actifs):>9}"
278:             f"{dec(v['total'] / reference):>8}{nb(v['indices']):>14}"
279:             f"{nb(v['valeurs']):>14}{nb(v['echelles']):>12}"
280:             f"{nb(v['entetes']):>11}")
281: 
282: 
283: def main(argv=None):
284:     p = argparse.ArgumentParser(
285:         description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
286:     p.add_argument("trace")
287:     p.add_argument("--couches", action="store_true",
288:                    help="ventilation par couche")
289:     p.add_argument("--sans-compression", action="store_true",
290:                    help="saute le point de repère zstd/gzip")
291:     p.add_argument("--sans-erreur", action="store_true",
292:                    help="saute le calcul de l'erreur de quantification i8")
293:     p.add_argument("--echantillon", type=float, default=16.0, metavar="Mio",
294:                    help="taille de l'échantillon compressé (défaut : 16 Mio)")
295:     p.a
… [2678 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_formats.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Compare notre déquantification d'un super-bloc à celle de **libggml**.
3: 
4:     tools/verifier_formats.py <modele.gguf> <tenseur> [index] [--type N]
5: 
6: La référence est la bibliothèque ggml elle-même (`tools/ref_ggml_bloc.c`), pas
7: une seconde lecture du format écrite ici : une réimplémentation Python partage
8: les mêmes erreurs de lecture et validerait un déquantificateur faux — c'est
9: exactement ce qui est arrivé pour IQ2_XXS (pas de 8 octets sur `qs` au lieu de
10: 4), IQ1_M (échelles lues en premier alors qu'elles sont en dernier) et Q2_K
11: (mauvais indice d'échelle).
12: 
13: Le côté Rust est interrogé par `drave <modele> --bloc <tenseur>:<index>`, qui
14: passe par `row_f32` — le chemin du chargement réel du modèle. Vérifier un
15: déquantificateur par un chemin qui n'est pas celui du moteur ne prouve rien.
16: 
17: Sortie : écart max et verdict ; code de retour 1 si divergence.
18: """
19: import os
20: import subprocess
21: import sys
22: 
23: sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
24: from an
… [3359 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/vision_mtmd.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Référence de vision : interroger libmtmd d'ollama, sans en-têtes.
3: 
4: C'est la SEULE vérification qui tranche d'un coup la rotation 2-D, la fenêtre
5: locale et la fusion 2 × 2 du ViT de Qwen2.5-VL : elle compare la sortie complète
6: de l'implémentation de référence (llama.cpp, embarquée par ollama) aux 3 584
7: valeurs du projecteur du moteur.
8: 
9: Aucun en-tête n'est installé, donc les prototypes sont déclarés ici. La structure
10: de paramètres est déclarée OPAQUE et GÉNÉREUSE (256 octets) : au-delà de 16
11: octets, l'ABI SysV passe la structure sur la pile et l'appelé ne lit que ce dont
12: il a besoin — une déclaration plus grande que la réelle est sans danger. Les
13: valeurs par défaut viennent de `*_default_params()`, pas d'un tampon à zéro.
14: 
15: Usage : vision_mtmd.py <modele.gguf> <mmproj.gguf> [sortie.bin]
16: """
17: import ctypes
18: import os
19: import struct
20: import sys
21: 
22: OLLAMA = "/usr/lib/ollama"
23: MODELE = "/home/stephane/Data13TB/stephane/modeles/gguf/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
24: MMPROJ = 
… [7234 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernier lot: vision_ref, fin convertir_clusters, fin trace_compacite, milieu session_report

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/vision_ref.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py", "limit": 96, "offset": 430}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/trace_compacite.py", "limit": 83, "offset": 350}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py", "limit": 100, "offset": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/vision_ref.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Référence numpy de l'embedding de patchs (première tranche du chemin image).
3: 
4: Le moteur écrit deux fichiers : les sorties (`--banc-vision`) et les POIDS
5: lus dans le GGUF. Ce script refait le CALCUL en numpy — l'extraction des
6: teneurs, elle, est vérifiée par `--tensors`. C'est le même partage des rôles
7: que pour MLA : une implémentation indépendante de la formule.
8: 
9: Usage : vision_ref.py <sortie.bin> [--poids <sortie.bin.poids>]
10: """
11: import sys
12: import numpy as np
13: 
14: 
15: def erf(x):
16:     """Erf vectorisé (Abramowitz-Stegun 7.1.26), la même approximation que le
17:     moteur : comparer deux formules différentes mesurerait l'approximation, pas
18:     l'implémentation."""
19:     x = np.asarray(x, dtype=np.float64)
20:     signe = np.sign(x)
21:     a = np.abs(x)
22:     t = 1.0 / (1.0 + 0.3275911 * a)
23:     y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
24:                 - 0.284496736) * t + 0.254829592) * t * np.exp(-a * a)
25:     return signe * y
26: 
27: def main():
28:     s
… [7203 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py</path>
<type>file</type>
<content>
430:         manifeste["experts"] = {str(l): ordres[l] for l in sorted(ordres)}
431:         for c in range(args.clusters):
432:             ids = list(range(c * taille, min(ne, (c + 1) * taille)))
433:             if not ids:
434:                 break
435:             nouveaux, morceaux = [], []
436:             for l in sorted(experts):
437:                 for t in experts[l]:
438:                     # tranche d'experts : blocs alignés le long de l'axe 0
439:                     par_expert = t["octets"] // ne
440:                     assert par_expert * ne == t["octets"], \
441:                         f"{t['nom']} : la tranche d'expert n'est pas alignée"
442:                     plages = []
443:                     for e in ids:
444:                         global_id = ordres[l][e] if args.mode == "experts" else e
445:                         plages.append((t["offset"] + global_id * par_expert, par_expert))
446:                     nouveaux.append({"nom": t["nom"], "dims": [len(ids)] + t["dims"][1:],
447:                                      "ttype": t["ttype"]
… [4760 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/trace_compacite.py</path>
<type>file</type>
<content>
350:     print("─" * 106)
351:     noms = [("actuel (u32 + i16)", "actuel"),
352:             ("écarts + i16", "i16"),
353:             ("écarts + blocs i8", "blocs"),
354:             ("blocs, échelles f16", "f16")]
355:     for libelle, cle in noms:
356:         print(corps_tableau(libelle, total[cle], actifs, reference))
357:     meilleur = min(("i16", "blocs", "f16"), key=lambda k: total[k]["total"])
358:     gain = 100.0 * (1.0 - total[meilleur]["total"] / reference)
359:     print("─" * 106)
360:     print(f"meilleure variante sans compression : {meilleur} "
361:           f"({nb(total[meilleur]['total'])} octets, "
362:           f"{dec(total[meilleur]['total'] / actifs)} o/actif, −{dec(gain, 1)} %)")
363:     print()
364: 
365:     # Les postes qui ne se voient pas dans la formule « 2 octets par actif ».
366:     utiles = total["blocs_utiles"]
367:     emis = total["blocs_emis"]
368:     ech = total["echappements"]
369:     print("Détail des postes")
370:     print(f"  échappements d'indice      {nb(ech)} sur {nb(actifs)} "
371:           f"({dec(100.0 * ech / a
… [3383 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py</path>
<type>file</type>
<content>
70: 
71: def sans_titres(s: str) -> str:
72:     """Neutralise les titres markdown d'un texte inséré : sans cela les messages
73:     de l'assistant cassent la table des matières du rapport."""
74:     return "\n".join(("\\" + l) if l.lstrip().startswith("#") else l
75:                      for l in (s or "").splitlines())
76: 
77: 
78: def tronque(s: str, n: int) -> str:
79:     s = (s or "").strip()
80:     return s if len(s) <= n else s[:n] + f"\n… [{len(s)-n} caractères tronqués]"
81: 
82: 
83: def charge(chemin: Path):
84:     """Rend la liste des enregistrements d'une session."""
85:     recs = []
86:     for ligne in decompresse(chemin).splitlines():
87:         if ligne.strip():
88:             try:
89:                 recs.append(json.loads(ligne))
90:             except json.JSONDecodeError:
91:                 pass
92:     return recs
93: 
94: 
95: def analyse(recs) -> dict:
96:     """Extrait tout ce qui servira au rapport."""
97:     d: dict = {
98:         "id": None, "cwd": None, "debut": None, "fin": None, "titre": None,
99:         "tours": [],          
… [3650 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérifications ciblées: constantes de tête et options non documentées

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in convertir_clusters.py analyse_experts_statique.py trace_compacite.py session_report.py telecharger_modeles.py; do echo \"=== $f\"; grep -n \"^[A-Z_][A-Z0-9_]* *=\" $f; done", "description": "List top-level constants in … [15 caractères tronqués]`

  ```
=== convertir_clusters.py
42:TYPES = {
=== analyse_experts_statique.py
=== trace_compacite.py
56:BLOC = 32           # canaux par bloc d'échelle (comme le cache KV et le réseau)
57:ECHAPPEMENT = 255   # marqueur « l'écart déborde, voici l'indice absolu u16 »
58:TAILLE_ENTETE_FICHIER = 14
59:TAILLE_ENTETE_LISTE = 10            # couche u16 · jeton u32 · n_actifs u32
60:TAILLE_QUEUE_BLOCS = 8              # n_blocs u32 · longueur du corps u32
=== session_report.py
38:TRONC_SORTIE = 700
39:TRONC_DEMANDE = 700
40:TRONC_SYNTHESE = 2500
45:MOTIFS_MESURE = re.compile(
50:MOTIFS_ERREUR = re.compile(
=== telecharger_modeles.py
25:RACINE = "https://huggingface.co"
26:CHUNK = 256 << 20          # 256 Mo
27:DEST_DEFAUT = "/home/stephane/Data13TB/stephane/modeles/gguf"
28:LIBRE_MINIMUM_GO = 300     # on s'arrête bien avant de remplir le disque
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"=== --couche usages\"; grep -n -- '\"--couche\\|--couche' profil_flux.py diff_flux.py analyse_flux.py; echo \"=== convertir_clusters section prints/names\"; grep -n 'mapping.tsv\\|manifeste.json\\|commun.gguf\\|cluster-\ … [223 caractères tronqués]`

  ```
=== --couche usages
profil_flux.py:8:Usage : profil_flux.py <trace> [--couche N] [--top 6] [--csv sortie.csv]
=== convertir_clusters section prints/names
18:    commun.gguf          ce qui n'est pas un expert : embeddings, sortie, attention,
20:    cluster-00.gguf …    par cluster : les tranches d'experts de TOUTES les couches
21:    manifeste.json       rôle de chaque fichier, tenseurs portés, tailles, ordre des
108:def lire_entete(chemin):
150:def ecrire_gguf(chemin, kv_brut, tenseurs, source, debut_donnees, alignement,
222:def reecrire_kv(kv_brut, remplacements):
251:def parcourir_kv(kv_brut):
283:def ordre_experts(trace, couche, ne):
297:def lire_trace(chemin):
308:def ecrire_mapping(dossier, manifeste):
309:    """Écrit `mapping.tsv` : la seule chose qui relie un expert GLOBAL à sa ligne
323:                       if f.get("role", "").startswith("cluster-")),
327:        assert f["role"] == f"cluster-{c:02d}", f["role"]
341:    chemin = os.path.join(dossier, "mapping.tsv")
349:    print(f"mapping.tsv · {len(lignes)} entrées · {n_couches} couches · "
415:    # ---- commun.gguf
417:        chemin = os.path.join(args.dossier, "commun.gguf")
420:        manifeste["fichiers"].appen
… [776 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières vérifications de formats et sections en sortie

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"=== trace_compacite defs\"; grep -n \"^def \\|^    # ---\" trace_compacite.py | head -40; echo; echo \"=== session_report sections/paths\"; grep -n 'L += \\[\"## \\|rapport.md\\|README.md\\|session.jsonl\\|digest' sessio … [103 caractères tronqués]`

  ```
=== trace_compacite defs
67:def f32_vers_f16(x):
105:def ventilation(indices=0, valeurs=0, echelles=0, entetes=0):
111:def analyser(listes, hidden, avec_erreur=True):
201:def encoder_v2(listes, n_layer, hidden):
246:def mesurer_compression(blob, echantillon):
266:def nb(n):
271:def dec(x, n=2):
276:def corps_tableau(nom, v, actifs, reference):
283:def main(argv=None):

=== session_report sections/paths
5:Sortie, à côté du digest brut :
7:  journal/sessions/<id>/rapport.md   la synthèse structurée de la session
8:  journal/README.md                  l'index des sessions
211:        L += ["## Objectifs déclarés", ""]
216:    L += ["## 1. Ce qui a été demandé", ""]
222:    L += ["## 2. Déroulé, étape par étape", ""]
245:    L += ["## 3. Travail accompli", "", "### Fichiers créés ou modifiés", "",
263:        L += ["## 4. Mesures et résultats marquants", ""]
276:        L += ["## 5. Erreurs rencontrées", "",
283:        L += ["## 6. Commits", ""]
311:             "de la session ; le `digest.md` voisin en donne le verbatim complet.", "",
317:        traces = sorted(sess.glob("session.jsonl*"))
323:        (dest / sess.name / "rapport.md").write_text(md, encoding="utf-8")
331:           
… [153 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py", "limit": 30, "offset": 283}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py</path>
<type>file</type>
<content>
283: def ordre_experts(trace, couche, ne):
284:     """Ordre des experts par fréquence décroissante (trace de routage), sinon
285:     l'ordre naturel. C'est la seule décision « intelligente » du convertisseur, et
286:     elle vient d'une mesure : les experts chauds d'abord, pour que le premier
287:     cluster soit celui qu'un nœud veut garder."""
288:     if not trace:
289:         return list(range(ne))
290:     import collections
291:     compte = collections.Counter()
292:     for ligne in trace.get(couche, []):
293:         compte.update(ligne)
294:     return sorted(range(ne), key=lambda e: (-compte.get(e, 0), e))
295: 
296: 
297: def lire_trace(chemin):
298:     par_couche = defaultdict(list)
299:     with open(chemin, encoding="utf-8") as f:
300:         for ligne in f:
301:             m = ligne.split()
302:             if len(m) < 3:
303:                 continue
304:             par_couche[int(m[0])].append([int(x) for x in m[2:]])
305:     return par_couche
306: 
307: 
308: def ecrire_mapping(dossier, manifeste):
309:     """Écrit `mapping.tsv` : la seu
… [367 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Envoi du dépouillement complet au parent

- **send_message** `{"agent_id": "f2de810a-b765-444d-b3cc-d8fce1ba2105", "message": "DÉPOUILLEMENT EN-TÊTE + CLI — 24 scripts de /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ (lecture seule stricte, aucun fichier modifié).\n\n### tools/aiguille.py  (219 lignes)\n- Rôle : « Aiguille dans la botte de foin — vers … [26468 caractères tronqués]`

  ```
message delivered to agent f2de810a-b765-444d-b3cc-d8fce1ba2105
  ```

### 🤖 Assistant

### tools/aiguille.py  (219 lignes)
- Rôle : « Aiguille dans la botte de foin — version 2, celle qui mesure vraiment. » La perplexité ne dit pas si un modèle RETROUVE une information : plante un code (« AZUR-7391 ») à une profondeur donnée dans un contexte long, puis le redemande. Remplissage = vrai texte varié (`data/wikitext2_test.txt`), fenêtre différente par sonde ; réponse longue ; préremplissage par lots ; contexte réellement atteint relu dans la sortie du moteur.
- Positional args : `modele` (l.127), `longueurs` CSV de contextes (l.128), `profondeurs` CSV de fractions 0..1 (l.129). Usage docstring l.27-28.
- Options CLI : `--n` (int, 40, "jetons générés (réponse)") l.130 — `--threads` (int, 16, sans help) l.131 — `--lot` (int, 256, "lot de préremplissage") l.132 — `--timeout` (int, 7200, sans help) l.133 — `--gpu` (store_true, "DRAVE_GPU=1 (déport des projections)") l.134 — `--gpu-kv` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)") l.135 — `--attn-topk` (int, 0, "--attn-topk N (0 = attention complète)") l.140-141 — `--gpu-topk` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1") l.142-143 — `--journal` (str, "", sans help) l.144. Contraintes : `--gpu-topk` exige `--attn-topk N` sinon ap.error (l.149-150) ; `--attn-topk` doit être ≥0 (l.151-152). Aucun `choices`/`nargs`.
- Constantes/vocabulaire de tête : `Q="./drave-core/target/release/drave"` l.41 ; `CORPUS="data/wikitext2_test.txt"` l.42 ; `CODE="AZUR-7391"` l.43 ; `AIGUILLE` l.44 ; `QUESTION` l.45-46 ; env DRAVE_GPU / DRAVE_GPU_KV / DRAVE_GPU_TOPK l.74-82.
- Formats lus/écrits : lit wikitext2 (normalisation `@-@ @,@ @.@`, l.53) ; lance le moteur `--infer --chat --flux --prompt --n --ctx --threads --temp 0 --lot [--attn-topk]` l.83-91 ; journal markdown `| contexte | profondeur | trouvé | secondes | détail |` l.205-215 ; `sys.exit(main())` l.219.

### tools/analyse_empreinte.py  (208 lignes)
- Rôle : « Chiffrer l'empreinte mémoire d'un MoE depuis une trace de routage. » Rend : courbe succès/empreinte par couche, verdict sur l'allocation non uniforme, taille minimale utile d'un cache LRU, structure périodique (Jaccard par écart de couches), extrapolation.
- Positional : `trace` (l.70). Usage l.4-10.
- Options CLI : `--limite` (int, None, "ne lire que les N premiers jetons") l.71-72 — `--modele` (str, None, "nom d'un modèle connu pour l'extrapolation (deepseek4, deepseek41, qwen3moe)") l.73-75. Parser : `description=__doc__`, `RawDescriptionHelpFormatter` l.68-69.
- Constantes/vocabulaire : `connus = {"deepseek4": (43,256,6,5.51), "deepseek41": (40,384,6,9.95), "qwen3moe": (48,128,8,3.05)}` = (couches, experts, top-k, Mo/expert) l.188-192 ; seuils (0.50…0.99) l.95 ; caches testés (topk,16,32,64,128) l.120 ; sortie code 1 si trace vide l.80, modèle inconnu l.194.
- Formats : lit la trace texte « couche jeton expert1 expert2 … » (l.12, produite via `DRAVE_TRACE_EXPERTS`, l.5) ; stdout texte.

### tools/analyse_experts_statique.py  (244 lignes)
- Rôle : « Analyse STATIQUE des experts d'un MoE : que portent les poids eux-mêmes. » Mesures : similarité intra-couche (experts jumeaux), profil de SOURCES (norme de colonne d'entrée), profil de DESTINATIONS (norme de ligne de sortie). « Ne lit que la tête des tenseurs ».
- Positional : `modele` (.gguf) l.175. Usage l.9.
- Options CLI : `--couches` (str, "0,12,24,36,47", sans help) l.176 — `--lignes` (int, 16, "lignes de sortie lues par expert (16 par défaut)") l.177-178 — `--seuil` (float, 0.90, "similarité au-delà de laquelle deux experts sont jumeaux") l.179-180.
- Constantes/vocabulaire : classe `Lecteur` « Lecteur GGUF minimal : en-tête, descripteurs, et octets d'un tenseur » l.35-36 ; tenseurs cherchés `blk.{l}.ffn_gate_exps.weight`, `ffn_up_exps.weight`, `ffn_down_exps.weight` l.190-191 ; clés GGUF `general.architecture`, `{arch}.expert_count` l.184-185 ; types ggml gérés F32=0 et F16=1, sinon ValueError l.167-169 ; `{12:144, 14:210, 8:34, 0:4, 1:2}` l.200 ; seuil « 80 % » n80 l.230.
- Formats : GGUF en-tête + tête de tenseurs ; stdout.

### tools/analyse_flux.py  (95 lignes)
- Rôle : « Analyse PURE d'une trace de flux : ce que la vision appelle “voir le modèle neurone par neurone”, mais chiffré par couche et sans exécuter le moteur. » Répond : quelle couche est creuse (croisement mesuré ~22 % de densité), quels neurones sont PERSISTANTS, recouvrement des top-k entre couches.
- Usage/positional : `analyse_flux.py <trace> [<trace2> ...] [--top 100]` l.16 ; traces limitées à 3 (`[:3]`) l.85.
- Options CLI : `--top` (int, défaut 100, parsé à la main `sys.argv` l.83-84, pas d'argparse, pas de help).
- Constantes/vocabulaire : magie `b"DRVF"`, u16 version, u32 n_layer, u32 hidden ; listes u16 couche / u32 pos / u32 n / f32 echelle ; paires u32 indice + i16 valeur ; sentinelle 0xFFFF (l.24-33) ; persistant si fréquence ≥ 0.9·jetons l.61 ; top1 %/top10 % l.64-65 ; couche ≥1000 → « FFN {couche-1000} » l.74.
- Formats : lit binaire DRVF ; stdout.

### tools/clusters_moe.py  (224 lignes)
- Rôle : « Découpage des MoE en clusters — à partir d'une trace de routage réelle. » Question de placement : quels experts s'allument ENSEMBLE ? Mesures couverture / ventilation (fan-out 90 %) / équilibre, avec témoins aléatoire et fréquence seule.
- Usage/positional : `clusters_moe.py /tmp/routage.txt [--clusters 8] [--json /tmp/clusters.json]` l.23-24 ; `trace` l.144.
- Options CLI : `--clusters` (int, 8, "nombre de groupes visés (nœuds ou GPU disponibles)") l.145-146 — `--json` (str, "", sans help) l.147 — `--graine` (int, 1234, sans help) l.148.
- Constantes/vocabulaire : `partition_equilibree(..., passes=6)` l.60 ; témoin fréquence en tranches ceil(ne/K) l.185-188 ; clés JSON `couches/clusters/n_jetons/n_experts` l.159-160 ; par couche `appris|hasard|frequence|affectation|membres` l.190-191 ; mesures `couverture_moyenne`, `ventilation_moyenne`, `ventilation_max`, `taille_min`, `taille_max` l.130-139.
- Formats : lit la trace texte « couche jeton experts… » (`lire` l.32-42) ; écrit JSON indent=1 si `--json` l.217-219.

### tools/compare_etats.py  (84 lignes)
- Rôle : « Compare les états intermédiaires de Drave à ceux de llama.cpp, tenseur par tenseur. » « La comparaison porte sur les vecteurs entiers, pas sur huit valeurs. »
- Usage/positional : `python3 tools/compare_etats.py <préfixe_drave> <préfixe_ref> <nom> <couche> <positions>` l.15-16 ; exactement 5 (`len(sys.argv)!=6` → SystemExit(__doc__)) l.46-48.
- Options CLI : aucune (pas d'argparse).
- Constantes/vocabulaire : magie `REFD` l.34 ; dispositions `l_last` = [embd, hc, position], `hc_attn_pre` = [embd, position] l.51-56 ; verdicts ✅ si écart max ≤ 1e-4 × dynamique, « ~ » si corr > 0.999, sinon ❌ l.78.
- Formats : Drave = f32 bruts sans en-tête `<préfixe_drave>-<nom>-<couche>-<position>.bin` (écrits par `DRAVE_DUMP_COUCHES`) ; llama.cpp = `<préfixe_ref>-<nom>-<couche>.bin`, en-tête `REFD`+ndim+ne[4] puis f32 ordre ggml (l.5-10, 30-42).

### tools/compare_logits.py  (109 lignes)
- Rôle : « Compare deux fichiers de logits » ; par position NLL de chacun, écart de NLL, rang du jeton cible, accord du top-1 (localise embedding/norme/RoPE/MoE/tête).
- Usage/positional : `compare_logits.py <notre.bin> <reference.bin> [ids.txt]` l.5, 44-47.
- Options CLI : aucune.
- Constantes/vocabulaire : format = int32 n_vocab, int32 n_pos, puis n_pos × n_vocab f32 LE l.2-3 ; numpy optionnel (fallback Python pur) l.15-18 ; échantillon affiché si `i<24 or i%32==0` (l.71, 88) mais accord top-1 compté sur toutes les positions (l.73-76) ; codes retour 2 si ids absents/vides ou <2 ids l.58-65.
- Formats : binaire logits ; ids texte (espaces/virgules) l.47.

### tools/convertir_clusters.py  (525 lignes)
- Rôle : « Convertisseur GGUF → “modèle éclaté en clusters”, un fichier par cluster. » Chaque cluster = GGUF autonome ouvrable seul en mmap. « il ne requantifie rien » : octets copiés tels quels (blocs alignés sur l'axe experts). `<arch>.expert_count` ajusté.
- Usage/positional : `convertir_clusters.py <source.gguf> <dossier> [--clusters 8] [--trace routage.txt] [--mode experts|couches] [--verifier]` l.28-30 ; `source` l.355, `dossier` l.356.
- Options CLI : `--clusters` (int, 8, sans help) l.357 — `--trace` (str, "", "trace de routage (ordre des experts)") l.358 — `--mode` (choices ["experts","couches"], défaut "experts", sans help) l.359 — `--verifier` (store_true, "relit chaque fichier produit et compare les empreintes") l.360-361.
- Constantes/vocabulaire : `TYPES` ggml -> (nom, octets/bloc, éléments/bloc) l.42-48 : 0 F32(4,1), 1 F16(2,1), 2 Q4_0(18,32), 3 Q4_1(20,32), 6 Q5_0(22,32), 7 Q5_1(24,32), 8 Q8_0(34,32), 9 Q8_1(36,32), 10 Q2_K(84,256), 11 Q3_K(110,256), 12 Q4_K(144,256), 13 Q5_K(176,256), 14 Q6_K(210,256), 15 Q8_K(292,256), 39 MXFP4(17,32).
- Formats lus/écrits : sorties `commun.gguf` l.417, `cluster-NN.gguf` l.449/464, `manifeste.json` (champs source, mode, clusters, n_experts, fichiers[fichier, role, octets, tenseurs | experts_locaux, experts_globaux_par_couche, couches], experts[ordre par couche]) l.391-393, 420-422, 455-459, 467-470, `mapping.tsv` avec `# drave-clusters-mapping v1` et colonnes couche/local/global/cluster l.341-348 ; trace lue en texte (couche jeton experts) l.297-305 ; mode experts si `"_exps." in nom` l.377, mode couches = groupes de couches l.396-412 ; vérif sha256 produit vs source l.481-519.

### tools/diff_flux.py  (91 lignes)
- Rôle : « Diff de deux traces de flux d'activation (format DRVF) » : où le flux diverge, à quelle couche, à quel jeton, de combien.
- Usage/positional : `diff_flux.py <traceA> <traceB> [--top 8]` l.8 ; traceA/traceB = sys.argv[1],[2] l.37-38.
- Options CLI : `--top` (int, défaut 8, parsé main l.39-41, pas de help).
- Constantes/vocabulaire : magie `b"DRVF"`, u16 version, u32 n_layer, u32 hidden, listes u16/u32/u32/f32, paires u32+i16, sentinelle 0xFFFF l.14-33 ; comparaison des valeurs DÉQUANTIFIÉES (v × échelle) l.54-61 ; dynamique = echelle·32767 l.70 ; couche ≥1000 → « FFN N » l.85 ; retour 1 si aucune liste commune, 0 si flux identiques l.46-48, 78-80.

### tools/flux_codec.py  (158 lignes)
- Rôle : « Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2) » ; 2e implémentation du contrat d'échange de la phase 3 (la 1re est en Rust `--trace-flux`).
- Usage/positional : `flux_codec.py <trace>` / `<trace> --jetons N` l.22-25 ; `trace` = sys.argv[1] l.123.
- Options CLI : `--jetons` (int, parsé main, l.146-147).
- Constantes/vocabulaire : `MAGIE=b"DRVF"` l.30 ; `VERSION=2` « ce que ce fichier ÉCRIT ; il LIT la 1, la 2 et la 3 » l.31 ; structs `ENTETE "<4sHII"`, `LISTE "<HIIf"`, `PAIRE_V1 "<Ih"`, `PAIRE_V2 "<Bh"`, `FIN "<H"` l.32-36.
- Format : en-tête DRVF + u16 version + u32 n_layer + u32 hidden ; liste u16 couche/u32 position/u32 n_actifs/f32 echelle ; v1 paires (u32 indice, i16 valeur) ; v2 écarts u8 + i16, écart 255 → indice absolu u16 ; v3 (lecture seule) u32 n_blocs + échelles f16 + paires (u8 écart, i8 valeur) indexées par bloc de 32 l.76-94 ; fin u16 0xFFFF. Mesure citée : v1 132 396 736 o → v2 66 370 408 o (−49,87 %) l.18-20.

### tools/harmony_canonique.py  (72 lignes)
- Rôle : « Construit un identifiant de perplexité au format harmony CANONIQUE » (montage forcé hors distribution : p=0,9999 pour `analysis` contre 0,0001 pour `final`) : message système complet, tour user, canal analysis court, puis canal final portant le texte à noter.
- Usage/positional : aucun positional. Option : `--sans-analysis` (flag testé par `"--sans-analysis" in sys.argv` l.45) = même séquence SANS le message analysis (contrôle).
- Constantes : `Q="/home/stephane/.../Drave/drave-core/target/release/drave"` l.17 ; `M=".../gpt-oss-120b-MXFP4.gguf"` l.18 ; `DEB, FIN, MSG, CANAL = 200006, 200007, 200008, 200005` l.20 ; message système verbatim l.49-53.
- Formats : lit `/tmp/wt2_prefixe.txt` et `/tmp/wt2_suite.txt` l.47-48 ; tokenizer du moteur (`--tokenize --fichier --sortie`) l.28-29 ; écrit `/tmp/harmony_canonique[_sans_analysis].ids` et `.dep` (indice du premier jeton de contenu) l.63-66.

### tools/hc_synthetique.py  (98 lignes)
- Rôle : « Référence numpy des hyper-connexions de DeepSeek-V4, et valeurs-témoins. » Formules recopiées des opérations ggml de `llama.cpp/src/models/deepseek4.cpp` (build_hc_pre, build_hc_sinkhorn, build_hc_post, build_hc_head), PAS du Rust ; sortie collée dans le test Rust `model::tests_hc::hyper_connexions_conforme_a_la_reference`.
- Usage/positional : `python3 tools/hc_synthetique.py` (aucun argument) l.14.
- Options CLI : aucune.
- Constantes : `HC, H = 4, 3` l.18 ; `EPS = 1e-6` (« hyper_connection.epsilon (V4.1) ») l.19 ; `ITERS = 20` (« hyper_connection.sinkhorn_iterations (V4.1) ») l.20 ; graine np 20261002 l.63 ; `scale = [0.5, 1.5, 2.0]` l.67.
- Format de sortie : lignes Rust `const MELANGE/BASE/SCALE/X/Y/PRE/POST/COMB/ENTREE/SORTIE: [f32; N] = [...]` l.79-89 + invariants sommes par destination/source l.90-94.

### tools/lire_meta_gguf.py  (117 lignes)
- Rôle : « Lit les métadonnées d'un GGUF (en-tête seul) et imprime les clés demandées » (ex. `compress_ratios` : quelles couches compressées). Sans motif, imprime tout (listes >64 éléments tronquées l.66-67).
- Usage/positional : `python3 tools/lire_meta_gguf.py <fichier.gguf> [motif ...]` l.10-12 ; sys.argv[1] + sys.argv[2:] l.71-74.
- Options CLI : aucune.
- Constantes : `TYPES` ggml {0:u8,1:i8,2:u16,3:i16,4:u32,5:i32,6:f32,7:bool,8:str,9:array,10:u64,11:i64,12:f64} l.17-18 ; `FIXES` structs LE l.19-21.
- Remarque : `lire_tenseur_f32(chemin, motif, index)` existe APRÈS le bloc `__main__` (l.77-117), non exposée en CLI ; utilise `general.alignment` (défaut 32), F32 seulement.
- Format : GGUF (magie b"GGUF", version u32, n_tensors/n_kv u64).

### tools/mesurer_lecture_experts.py  (81 lignes)
- Rôle : « Lectures d'experts : série contre parallèle, sur un VRAI fichier froid. » Froid forcé par `posix_fadvise(DONTNEED)`, deux passes appariées sur des blocs différents.
- Usage/positional : `tools/mesurer_lecture_experts.py <shard.gguf> [nb_blocs] [nb_fils]` l.4 ; `chemin` l.36, nb_blocs défaut 240 l.37, nb_fils défaut 16 l.38.
- Options CLI : aucune.
- Constantes : `PAGE = 4096` l.24 ; `taille_bloc = 4 << 20` (4 Mo ≈ un expert) l.39 ; `debut = taille // 2`, `zone_b = debut + nb_blocs*taille_bloc` l.45-47.
- Format : mmap PROT_READ du GGUF ; stdout Go/s série vs parallèle + rapport ×.

### tools/mla_synthetique.py  (250 lignes)
- Rôle : « Modèle MLA synthétique + référence numpy — le harnais du chantier 5. » Modèle minuscule (poids aléatoires, formes MLA correctes) écrit en GGUF + référence numpy indépendante (cache KV latent : 1 tête de 128 + 32 valeurs par jeton).
- Usage/positional : `mla_synthetique.py --sortie /tmp/mla_minuscule.gguf --dossier /tmp/mla_ref` l.15-16 ; aucun positional.
- Options CLI : `--sortie` (str, "/tmp/mla_minuscule.gguf", sans help) l.226 — `--dossier` (str, "/tmp/mla_ref", sans help) l.227 — `--graine` (int, 1234, sans help) l.228 — `--n` (int, 8, "jetons d'entrée") l.229.
- Constantes : `H=64` hidden, `NL=2`, `NH=4`, `NKV=1` (MLA = MQA), `QL=32` q_lora_rank, `KVL=48` kv_lora_rank, `QKR=16` qk_rope, `QKN=16` qk_nope, `VD=16` value_length, `FFN=128`, `VOCAB=64`, `EPS=1e-5`, `ROPE_BASE=10000.0` l.28-40.
- Formats : GGUF version 3, tenseurs F32 (type 0), alignement 32 l.176-206 ; noms `token_embd.weight`, `output_norm.weight`, `blk.N.attn_q_a`, `attn_q_a_norm`, `attn_q_b`, `attn_kv_a_mqa`, `attn_kv_a_norm`, `attn_kv_b`, `attn_output`, `ffn_*` l.50-70 ; dossier : `logits.npy`, `ids.npy`, `forme.json` (hidden, n_layer, n_head, q_lora, kv_lora, qk_rope, qk_nope, v_dim, ffn, vocab, graine) l.237-242.

### tools/pair_factice.py  (140 lignes)
- Rôle : « Pair factice du protocole de flux (v2) : il ÉCOUTE et DIT ce qu'il reçoit. » Un pair qui parle le protocole sans calculer le modèle rend visible ce que l'autre bout envoie (tailles, positions, modes, réglages) ; répond un flux de la dimension demandée.
- Usage/positional : `python3 tools/pair_factice.py <port> [dimension]` l.10 ; port défaut 45760 l.32, dimension défaut 896 l.33.
- Options CLI : aucune.
- Constantes/vocabulaire : `MAGIE = 0x44525631` l.14 ; `TETE = 79` (en-tête v4 : magie, version, mode, plage, position, n, échelle, niveaux, seuil, top-k, renorm, 7 top-k par projection, 3 top-k globaux) l.15-16 ; `MODES = {0:"dense f32", 1:"listes quantifiées", 2:"blocs (i8 + écarts)", 3:"lot dense (t états × dimension)", 4:"lot en listes (mode 2 par état)"}` l.17-18.
- Protocole : réponse `struct.pack("<IBBIIIIfffIBIIIIIIIIII", ...)` l.115-117 ; mode 3 = n états × dimension × 4 ; mode 4 = n états à liste vide, nb = (dimension+31)//32 blocs ; mode 2 = nb blocs + échelles f32 + longueur 0 ; dense = dimension × 4 (l.118-134) ; invariants mode 4 vérifiés (`nb` attendu, `2a ≤ lg ≤ 4a`) l.80-86 ; écoute 127.0.0.1.

### tools/profil_flux.py  (78 lignes)
- Rôle : « Profilage par neurone à partir d'une trace de flux (format DRVF) » — quels neurones s'allument, à quelle fréquence, avec quelle magnitude, par couche.
- Usage/positional : `profil_flux.py <trace> [--couche N] [--top 6] [--csv sortie.csv]` l.8 ; `trace` = sys.argv[1] l.37.
- Options CLI RÉELLES : `--top` (int, défaut 6, parsé main l.39-40) — `--csv` (chemin, parsé main l.42-43). ⚠️ DISCRÉPANCE : `--couche N` est annoncé l.8 mais n'est jamais lu/implémenté.
- Constantes/vocabulaire : format DRVF identique à analyse_flux l.14-33 ; top10 % = len(forts)//10 l.61 ; couche ≥1000 → « FFN N » l.64.
- Formats : lit DRVF ; CSV en-tête `couche,neurone,magnitude,frequence` l.70.

### tools/proxy_latence.py  (54 lignes)
- Rôle : « Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien distant coûte à un découpage de modèle » (le débit n'est jamais le problème — 0,25 Mbit/s — la latence si).
- Usage/positional : `python3 tools/proxy_latence.py <port_écoute> <hôte_cible:port> [délai_ms]` l.10 ; port l.35, `hôte:port` (rsplit ":",1) l.36, délai ms→s défaut 0.0 l.37.
- Options CLI : aucune.
- Constantes : recv 65536 l.18 ; bind 127.0.0.1, `listen(4)`, TCP_NODELAY sur les deux sockets l.40-48 ; un thread daemon par direction l.49-50.

### tools/session_report.py  (341 lignes)
- Rôle : « Produit, pour chaque session DSH, un rapport qui reconstitue son essence et démontre le travail accompli, étape par étape. » Contenu : fiche, demandes, déroulé, travail, mesures, erreurs, commits (l.10-19).
- Usage/positional : `python3 tools/session_report.py [--repo DIR] [--session ID] [--quiet]` l.22 ; aucun positional.
- Options CLI : `--repo` (str, défaut `Path(__file__).resolve().parent.parent`, sans help) l.293 — `--session` (str, None, sans help) l.294 — `--quiet` (store_true, sans help) l.295.
- Constantes : `TRONC_SORTIE=700`, `TRONC_DEMANDE=700`, `TRONC_SYNTHESE=2500` l.38-40 ; `MOTIFS_MESURE` regex (tok/s | G év | MHz | ALMs | M20K | DSP | Go/s | Mo | Ko | % | ms, ou perplexité|surcoût|résidu|rang|R²|× suivi d'un nombre) l.45-49 ; `MOTIFS_ERREUR` regex (exit code [1-9], panicked at, ^Error, ^error[, ECHEC/ÉCHEC, DIVERGENT au rang, Error (n), fatal error) l.50-52.
- Formats : lit `$DSH_HOME/sessions/--<slug>--/session.jsonl*` (zstd via `zstd -dc` si `.zstd`) l.55-61, 299-317 ; JSONL par `type` : session, session/title, turn/start, user/message, assistant/message, tool/call, tool/result l.112-169 ; écrit `journal/sessions/<id>/rapport.md` et `journal/README.md` l.7-8, 306-336 ; sections « ## Objectifs déclarés », « ## 1. Ce qui a été demandé », « ## 2. Déroulé, étape par étape », « ## 3. Travail accompli », « ## 4. Mesures et résultats marquants », « ## 5. Erreurs rencontrées », « ## 6. Commits » l.211, 216, 222, 245, 263, 276, 283 ; retour 1 si aucune session l.303-304.

### tools/telecharger_modeles.py  (197 lignes)
- Rôle : « Télécharge les modèles LOURDS, par tranches, avec reprise. » Le pont Xet de HF refuse un GET plein sur le fichier de 365,7 Go (HTTP 400) mais sert une requête `Range` (HTTP 206).
- Usage/positional : `--manifeste tools/manifeste_modeles_lourds.json` / `--seulement Kimi-K2.7-Code-UD-IQ1_M` / `--etat` l.12-15 ; aucun positional.
- Options CLI (aucun `help=`) : `--manifeste` (str, "tools/manifeste_modeles_lourds.json") l.127 — `--dest` (str, DEST_DEFAUT) l.128 — `--seulement` (str, "") l.129 — `--etat` (store_true) l.130 — `--journal` (str, "/tmp/telechargement_lourds.log") l.131.
- Constantes : `RACINE="https://huggingface.co"` l.25 ; `CHUNK = 256 << 20` l.26 ; `DEST_DEFAUT="/home/stephane/Data13TB/stephane/modeles/gguf"` l.27 ; `LIBRE_MINIMUM_GO = 300` l.28 ; `telecharger(..., fils=6, essais=6)` l.69, `_tranche(..., essais=6)` l.35 ; curl `-sSL -f --retry 3 --retry-delay 10 --retry-all-errors -r pos-haut` l.48-51.
- Formats : manifeste JSON (entrées `nom`, `repo`, `chemin`, `octets`) l.134, 177-178 ; URL `{RACINE}/{repo}/resolve/main/{chemin}` l.178 ; fichier préalloué + sidecar `<dest>.etat.json` (position absolue par tranche) + temporaires `.part<cle>` l.41-64, 155-165 ; `--etat` lit le sidecar (getsize = 100 % dès le 1er octet sinon) l.147-174.

### tools/trace_compacite.py  (432 lignes)
- Rôle : « Chiffre ce que coûterait une trace DRVF v1 sous plusieurs encodages. » Disque = 6 o/neurone actif (u32+i16), réseau ≈ 2 o/actif ; variantes `actuel`, `écarts+i16`, `écarts+blocs`, `blocs f16`, zstd/gzip. Lecture du format déléguée à `tools/flux_codec.py` (implémentation de référence).
- Usage/positional : `python3 tools/trace_compacite.py <trace.bin> [options]` l.29 ; `trace` l.286.
- Options CLI : `--couches` (store_true, "ventilation par couche") l.287-288 — `--sans-compression` (store_true, "saute le point de repère zstd/gzip") l.289-290 — `--sans-erreur` (store_true, "saute le calcul de l'erreur de quantification i8") l.291-292 — `--echantillon` (float, 16.0, metavar="Mio", "taille de l'échantillon compressé (défaut : 16 Mio)") l.293-294 — `--zstd-v2` (store_true, "compresse aussi la variante écarts+blocs reconstruite") l.295-296.
- Constantes : `BLOC = 32` l.56 ; `ECHAPPEMENT = 255` l.57 ; `TAILLE_ENTETE_FICHIER = 14` l.58 ; `TAILLE_ENTETE_LISTE = 10` l.59 ; `TAILLE_QUEUE_BLOCS = 8` l.60 ; import `flux_codec` via sys.path l.53-54.
- Formats/vocabulaire : variantes "actuel","i16","blocs","f16" + postes "blocs_utiles","blocs_emis","echappements","n_err","err2" l.351-380 ; retour 1 si trace introuvable, non DRVF ou sans activation l.299-313.

### tools/verifier_formats.py  (108 lignes)
- Rôle : « Compare notre déquantification d'un super-bloc à celle de libggml » — référence = `tools/ref_ggml_bloc.c`, côté Rust via `drave <modele> --bloc <tenseur>:<index>` (chemin row_f32). Sortie : écart max + verdict, retour 1 si divergence.
- Usage/positional : `tools/verifier_formats.py <modele.gguf> <tenseur> [index] [--type N]` l.4 ; modele l.58, tenseur l.58, index défaut 0 l.59-67.
- Options CLI : `--type` (int, forcé, parsé main l.64-65).
- Constantes : `RACINE` = racine du dépôt l.26 ; `DRAVE = RACINE/drave-core/target/release/drave` l.27 ; `REF = os.environ.get("REF_GGML_BLOC", "/tmp/ref_ggml_bloc")` l.28 ; `OCTETS_256` l.31-51 : 0 F32 1024, 1 F16 512, 2 Q4_0 144, 3 Q4_1 160, 6 Q5_0 176, 7 Q5_1 192, 8 Q8_0 272, 10 Q2_K 84, 11 Q3_K 110, 12 Q4_K 144, 13 Q5_K 176, 14 Q6_K 210, 16 IQ2_XXS 66, 18 IQ3_XXS 98, 19 IQ1_S 50, 23 IQ4_XS 136, 29 IQ1_M 56, 30 BF16 512, 39 MXFP4 136.
- Import : `from analyse_experts_statique import Lecteur` l.23-24 ; CONCORDE si écart < 1e-6 ; codes retour 2 (usage/type non couvert/rien rendu), 1 (DIVERGE), 0 l.96-104.

### tools/vision_mtmd.py  (159 lignes)
- Rôle : « Référence de vision : interroger libmtmd d'ollama, sans en-têtes. » Seule vérification qui tranche rotation 2-D, fenêtre locale et fusion 2×2 du ViT Qwen2.5-VL : compare la sortie complète de llama.cpp (via ollama) aux 3 584 valeurs du projecteur. Structure de params opaque et généreuse (256 o).
- Usage/positional : `vision_mtmd.py <modele.gguf> <mmproj.gguf> [sortie.bin]` l.15 ; modele défaut MODELE l.59, mmproj défaut MMPROJ l.60, sortie optionnelle l.150.
- Options CLI : aucune.
- Constantes : `OLLAMA = "/usr/lib/ollama"` l.22 ; `MODELE = .../Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` l.23 ; `MMPROJ = .../mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf` l.24 ; `TAILLE_PARAMS = 256` l.25 ; backends chargés explicitement `libggml-cpu-haswell/alderlake/sandybridge` l.44-45 ; image déterministe 336×336 (dégradé + carré central) l.76-85 ; 3584 valeurs attendues (projection_dim du mmproj) l.146 ; invite `"<|im_start|>user\n<marker>\ndecris cette image<|im_end|>\n<|im_start|>assistant\n"` l.117 ; type de morceau image = 1 l.138.
- Format écrit : `sortie.bin` = i32 longueur + N f32 l.151-153.

### tools/vision_ref.py  (162 lignes)
- Rôle : « Référence numpy de l'embedding de patchs (première tranche du chemin image). » Le moteur écrit les sorties (`--banc-vision`) et les POIDS lus dans le GGUF ; ce script refait le CALCUL (même partage des rôles que MLA).
- Usage/positional : `vision_ref.py <sortie.bin> [--poids <sortie.bin.poids>]` l.9 ; `sortie` = sys.argv[1] l.28 ; poids = sys.argv[2] si fourni, sinon `sortie + ".poids"` l.29.
- Options CLI : aucune. ⚠️ le `[--poids …]` du docstring n'est pas une option : c'est un 2e positional (passer littéralement `--poids` donnerait un chemin « --poids »).
- Constantes : `erf` vectorisé Abramowitz-Stegun 7.1.26 (même approximation que le moteur) l.15-25 ; image du banc cote=28, carré central 10≤x<18 l.38-44 ; GELU exact `0.5*h*(1+erf(h/√2))` l.75 ; eps LayerNorm 1e-6 l.109 ; rotation 2-D mRoPE : 4 blocs de hd/4, blocs 0/2 par la LIGNE, 1/3 par la COLONNE, base 10000, 16 têtes l.114-137 ; DÉSACCORD si écart relatif > 1e-5 l.156.
- Formats lus : `sortie.bin` = i32 n_patch, i32 cout puis n_patch×cout f32 l.30-33 ; `sortie.bin.poids` = i32 cout, cin, ky, kx puis f32 (reshape [cout,cin,ky,kx]) l.34-36 ; `sortie.bin.projecteur` = 4 i32 (n0,n1,n2,n3) + w0,b0,w2,b2 f32 l.65-72 ; `sortie.bin.bloc` = 3 i32 (npatch, e, nff) + poids f32 (ln1, ln2, wq/bq, wk/bk, wv/bv, wo/bo, wg/bg, wu/bu, wd/bd, x_eng) l.92-108.

POINTS TRANSVERSAUX
1. argparse : 9 scripts seulement (aiguille, analyse_empreinte, analyse_experts_statique, clusters_moe, convertir_clusters, mla_synthetique, session_report, telecharger_modeles, trace_compacite) ; les 15 autres parsent `sys.argv` à la main.
2. Docstrings qui annoncent des options inexistantes : `profil_flux.py --couche N` (l.8 vs main l.36-43) et `vision_ref.py --poids` (l.9 vs l.29, simple 2e positional).
3. Le format DRVF est réimplémenté 4 fois (analyse_flux, diff_flux, profil_flux, flux_codec) ; trace_compacite réutilise flux_codec par import.
4. Vocabulaire commun : couche ≥ 1000 = « FFN {couche-1000} » (analyse_flux l.74, diff_flux l.85, profil_flux l.64, trace_compacite l.422).

Aucun fichier modifié (lecture seule stricte). Résultat complet également transmis au parent (f2de810a-b765-444d-b3cc-d8fce1ba2105).

