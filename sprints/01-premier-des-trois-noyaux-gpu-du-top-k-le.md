# Sprint 1 — Premier des trois noyaux GPU du top-k : les scores d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur banc

- **Début** : 17:41 · **Fin prévue** : 19:41 (boxing de 120 min)
- **Objectif** : Premier des trois noyaux GPU du top-k : les scores d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur banc
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 120 min (boxing 120 min). Commits : 20.

  - `03243f7` Compteur de lignes Rust re-mesuré en fin de sprint : 13 480 (le chiffre avait bougé de 312 lignes pendant le sprint)
  - `22d3004` --options-actives dit si le top-k déporté s'applique, et pourquoi sinon
  - `e49f3bb` Rapport : l'étape 5 est faite, et la ligne de l'étape 4 dit la bonne variable (clés vues, pas contexte)
  - `c1fdfd4` Rapport et plan : 14 noyaux et 956 lignes (le noyau 3 est arrivé après le comptage), ordre réel de la collecte
  - `dada69a` Journal : index des sessions régénéré
  - `b8d4fa5` Correction d'interprétation : les clés notées dépendent du nombre de JETONS, pas du contexte — le croisement est entre 255 et 2 047 clés, pas « entre 8 k et 16 k »
  - `f9f2f99` --attn-topk en mode lot : le drapeau ne fait rien, il le dit maintenant
  - `aa43de9` Chiffres du 16 k sur le binaire final : attention 19,58 → 7,59 ms/jeton (−61 %), balayage −24 %
  - `64c9d26` Top-k déporté : une synchro en trop, un budget de scores, un échec dit une seule fois
  - `b58f441` Plan et REPRISE : l'étape 6 est verte, et la prochaine étape est la FUSION de la chaîne, pas un noyau de plus
  - `abcfab7` Relecture du branchement : un faux résultat silencieux dans attn_kv_recombine, et le top-k gagne à 16 k
  - `d221ead` Étape 4 : le top-k déporté tourne dans le moteur (opt-in), et l'étape 5 est chiffrée
  - `1f53667` Compteur de lignes Rust unifié : 13 168 (un seul chiffre, mesuré, dans README ×2 et REPRISE)
  - `674a334` Noyau 3 : softmax sur les k retenus + Σ w·V, écart 1,0 à 4,8e-7
  - `47ce9b7` Relecture adversariale : 7 défauts corrigés, dont un bloquant sur les chemins d'échec
  - `a891c31` Rapport de sélection : le second passage k doublé, et la durée mal étiquetée
  - `fa6a4f3` Collecte top-k : réallouer quand k GRANDIT, et un banc qui le prouve
  - `e950075` Noyaux 2b : collecte des k indices — même ensemble que le CPU, 896× le tri à 262 k clés
  - `d00c01c` Noyau 2a du top-k GPU : histogramme d'octet, seuil exact sur 14/14 lignes
  - `5e8bf48` Sprint 1 : noyau GPU de scores d'attention — exact à 1,03e-7, 40× plus rapide

**Objectif du sprint** : « Premier des trois noyaux GPU du top-k : les scores
d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur
banc ». **Livré : les trois noyaux, le banc, le branchement dans le moteur, les
portes, et deux relectures adversariales.**

### Ce qui est livré, chiffre par chiffre

| # | livrable | mesure |
|---|---|---|
| 1 | `attn_scores` + banc `--banc-topk` (objectif du sprint) | écart **1,6–2,3e-7** (critère 1e-6) · **26,7–40×** le CPU de 4 k à 262 k clés |
| 2 | `attn_topk_histo` : seuil radix 4 passes | k-ième score **exact au bit près 14/14 lignes** à 4 k / 65 k / 262 k / **1 M** clés ; **224×** le tri+comptage CPU à 262 k |
| 3 | `attn_topk_compte` + `attn_topk_ecrit` : collecte | **même ensemble que le CPU, 14/14 lignes, différence symétrique 0** ; 0 doublon, 0 hors borne, 0 case vide ; **0,95 ms** contre 1 653 ms de tri CPU à 1 M (×1 744) |
| 4 | `attn_topk_somme` : softmax sur k + puits, Σ w·V | écart **1,0–4,8e-7** · temps GPU **constant (0,07 ms) de 4 k à 262 k clés** |
| 5 | branchement `DRAVE_GPU_TOPK=1` dans `forward`, repli CPU sur tout refus | PPL identique (9,4162/9,4167 à 2 k ; 13,1355/13,1358 à 8 k ; 12,2265/12,2267 à 16 k) |
| 6 | étape 5 du plan : à 1 M de clés | chaîne complète **3,90 ms** contre 539,9 ms d'attention CPU (×138) et 13,2 ms en VRAM — **0,3×** le complet (critère ≤ 2×) |
| 7 | **le gain dans le moteur** (4 095 jetons, 2 047 clés en moyenne) | attention **19,58 → 7,59 ms/jeton (−61 %)**, balayage **203,7 → 155,5 s (−24 %)**, perplexité identique à 2e-5. À 511 jetons (255 clés en moyenne) le CPU gagne encore (4,21 contre 7,68) : **le croisement en clés est entre 255 et 2 047** |
| 8 | portes de non-régression | Qwen2.5-0.5B Q8_0 ctx 256 = **19,3885** (CPU *et* `DRAVE_GPU_KV`) · gpt-oss MXFP4 ctx 256 = **15,1757** (CPU) et **15,1667** (`DRAVE_GPU`) · `cargo test` **17/17** · `--banc-topk` vert de n = 1 à 1 000 000 · `--banc-kv` ×35,6 |
| 9 | documentation | `reports/rapport-gpu-topk-selection.md` (nouveau) · plan à jour (étapes 1–6) · README, REPRISE, `docs/contexte-long.md` · compteur de lignes unifié (**13 480**) |

### Les cinq défauts attrapés, et par quel moyen

| défaut | trouvé par | effet mesuré |
|---|---|---|
| le banc réutilisait la même clé partout : scores d'une ligne **exactement égaux**, donc la descente radix ne choisissait jamais entre deux seaux | **relecture du banc** (pas un échec) | 14/14 lignes vertes **sans rien tester** ; l'écart du noyau 1 est passé de 1,03e-7 (flatteur) à 1,6–2,3e-7 (vrai) |
| le puits du noyau 3 était ajouté par **chaque fil** au lieu d'une fois (chaque fil ne tient qu'une somme partielle) | **le banc**, en une ligne | dénominateur ×45,7, sortie 55× trop petite à k = 1, écart 2,05e-1 → 4,79e-7 après correction |
| le garde de réallocation de la collecte suivait les **dimensions** au lieu des **capacités** : un échec d'allocation au milieu du `\|\|` laissait un pointeur 0 | **relecture adversariale n° 1** | bloquant sur le chemin d'échec ; corrigé (garde par capacités, auto-réparateur) |
| `attn_kv_recombine` lisait `sinks[warp]` au lieu de `sinks[kvh*rep + warp]` | **relecture adversariale n° 2** | gpt-oss `DRAVE_GPU_KV=1` : PPL **17,6531 AVANT** → **15,1786 APRÈS** (référence CPU 15,1757) |
| cinq chiffres faux ou périmés dans la documentation (dont la ligne 65 536 du rapport des scores, 7,4 ms alors que la re-mesure dit 2,36 ms) | **audit de documentation** (sous-agent) | corrigés, source citée |

Cinq autres points de la relecture n° 2 ont été corrigés dans la foulée : limites du
noyau 3 testées **après** sept lancements, couverture de la collecte non vérifiée
alors que la copie qui le permet est déjà payée, unités de capacité mélangées
(`sinks_cap`/`out_cap` en éléments d'un côté, en octets de l'autre), compteur
d'événements incohérent entre les deux chemins, `DRAVE_GPU_TOPK=0` qui **activait**
le chemin.

## Rétrospective — garder / changer

- **Garder** :
  - le banc comme **référence indépendante** : il a attrapé le puits compté 256 fois
    en une ligne, là où la relecture du noyau ne voyait rien ;
  - les **relectures adversariales par sous-agent** : 7 + 13 défauts, dont un faux
    résultat silencieux en production (les puits) — et elles ont trouvé ce que les
    bancs ne cherchaient pas ;
  - l'**audit de documentation** après coup : quatre chiffres faux, dont un qui
    servait à dimensionner la suite ;
  - la discipline « un refus rend la main au CPU, aucun résultat partiel publié —
    et on le vérifie » : la relecture a confirmé la propriété, puis on l'a
    renforcée (contrôle de couverture de la collecte) ;
  - les **portes en fin de sprint** sur le binaire final, pas sur un binaire
    intermédiaire.
- **Changer** :
  - **mesurer le coût fixe avant de conclure au gain** : j'ai annoncé « le top-k
    GPU est prêt » alors qu'à 255 clés il est 1,8× plus LENT que le CPU (huit
    lancements et dix-sept transferts par couche et par jeton). Le chiffre était
    dans la mesure, pas dans ma conclusion ;
  - **nommer la variable qu'on fait varier** : j'ai écrit « le croisement est
    entre 8 192 et 16 384 clés » alors que ces deux lignes différaient aussi par
    le NOMBRE DE JETONS (511 contre 4 095, donc 255 contre 2 047 clés notées).
    Corrigé dans les trois documents — le croisement en clés est entre 255 et
    2 047 ;
  - **aucun chiffre sans source, y compris dans un message de commit** : j'ai
    écrit « 27,4911 contre 21,1444 » dans un message alors que le second chiffre
    n'avait pas été mesuré (l'écart réel, à 1 023 jetons, est 9,4335 contre
    9,4167). Commit amendé dans la minute — mais la règle vaut pour les messages
    aussi ;
  - **compter les lancements et les transferts dans la documentation** : « six
    lancements et cinq recopies » était faux d'un facteur 3 (c'est 8 et 17) — et
    c'est ce chiffre-là qui dimensionne la prochaine étape ;
  - une seule unité pour une même capacité (`scores_cap` en éléments contre
    `histo_cap` en octets, `sinks_cap` dans deux unités) : source de bugs
    silencieux deux fois aujourd'hui ;
  - étiqueter les durées : « 0,0004 ms » affiché pour 0,45 ms a failli faire
    chercher un faux défaut dans un noyau ;
  - budgéter les tampons GPU **avant** de les allouer (le tampon de scores
    `nh × n × 4` — 9,2 Go pour gpt-oss à 1 M — n'était budgété nulle part).
- **Doute** :
  - la fusion (un noyau par ligne pour descente + collecte + somme) tiendra-t-elle
    sa promesse de parallélisme à 1 M de clés avec 14 blocs seulement ? À mesurer
    avant d'y croire ;
  - le k-ième score **change** entre les scores CPU et GPU sur 4 à 7 lignes sur 14
    (scores quasi égaux) : la perplexité reste identique à 2e-5, mais personne n'a
    encore mesuré l'effet de ce basculement sur une longue génération ;
  - `--attn-topk` est **ignoré par le mode lot** (`--lot > 1` calcule une
    attention dense, sans message) : défaut pré-existant, signalé par la relecture,
    **non corrigé** — il faut soit l'implémenter, soit le refuser bruyamment.

## Planning — le sprint suivant (2 h)

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Fusionner la sélection** : descente radix + collecte + somme dans un noyau par ligne (k scores en partagé) | 8 lancements → 2 ; le déport dépasse le CPU **dès ~1 000 clés** (aujourd'hui : entre 255 et 2 047) |
| 2 | Supprimer le tampon `nh × n × 4` par couche (candidats seuls en partagé) | 0 tampon de scores complet ; ctx 1 M possible sans budget VRAM |
| 3 | Refuser bruyamment `--attn-topk` en mode lot, ou l'y implémenter | plus aucun drapeau silencieusement ignoré |
| 4 | **Grille propre** : faire varier le NOMBRE DE JETONS à contexte fixé (511 / 1 023 / 2 047 / 4 095 / 8 191 / 16 383) au lieu du contexte | un tableau où une seule variable bouge, perplexité à 2e-5 près à chaque point |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
**État à la clôture** : `cargo test` **17/17** · Qwen2.5-0.5B Q8_0 ctx 256 =
**19,3885** (CPU *et* `DRAVE_GPU_KV`) · gpt-oss-120b MXFP4 ctx 256 = **15,1757**
(CPU) et **15,1667** (`DRAVE_GPU`) · `--banc-topk` vert de n = 1 à 1 000 000 ·
`--banc-kv` ×35,6 · aucun processus laissé derrière, aucun travail non commité.
