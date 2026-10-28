# Ressources et philosophie de travail

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **quand on planifie une campagne** ou
> qu'on se demande si on peut travailler en parallèle.

## La machine (Hauru)

- **2 × RTX 5000 en NVLink**, 16 Go chacune : dédiées au projet (la carte AMD est dédiée à l'affichage). Turing :
  **fp16 natif, bf16 non natif** — le bf16 est *lent* (pas faux) ; préférer `float16` pour les gros modèles.
- **RAID NVMe 4 × 256 Go** (`/home/stephane/IA`) à disposition entière pour les modèles et les caches ; les textes
  et le dépôt sont sur `/home`.
- **Beaucoup de RAM, 2 CPU avec beaucoup de cœurs** — attention aux subtilités hyperthread et à l'affinité des
  processus.
- **Allocation de traitement élevée et extensible** : on peut travailler **24/7** sur plusieurs tâches en parallèle.
- Environnement Python du dépôt : `/home/stephane/gpu-env/bin/python` (torch + transformers installés) ; un venv
  local (`/home/stephane/IA/venv-drave`) sert pour les mesures récentes.

## La règle des ressources

Les GPU ne se partagent pas bien : **une mesure qui charge 28 Go de VRAM bloque toute porte ou tout autre modèle**.
Séquence : les portes d'abord, les mesures ensuite ; deux petits modèles peuvent cohabiter sur les deux cartes, un
gros modèle prend les deux.

## La composition mesurée (26/10)

- **CPU** : 2 sockets × 10 cœurs × 2 SMT = **40 threads logiques** ; les frères SMT sont
  `0/20 … 9/29` et `10/30 … 19/39`. Pour un travail CPU soutenu, viser **20 threads physiques**
  (`0-9`, `10-19`) et éviter de saturer les deux frères d'un même cœur.
- **GPU** : 2 × RTX 5000 16 Go. Deux petits `route` (10–32 M) entraînés **en parallèle**, un par
  carte, avec `OMP_NUM_THREADS=4` chacun : **18–25 %** d'utilisation GPU, **560–680 Mo** par
  carte, ~60 s pour 500 pas (31,63 M : 102 s pour 1 000 pas). Le goulot est le **CPU/la boucle**,
  pas la VRAM.
- **NVLink** : `nvidia-smi topo -m` donne **NV1**, `nvidia-smi nvlink --status` **25,781 GB/s** ; NCCL
  **2.28.9**. Le protocole sémantique utilise deux rangs explicites (torchrun/elastic n'a pas démarré ici),
  `all_gather` des `z` et `all_reduce` des gradients par NVLink ; 31,97 M (étage A) / 64,39 M (étage B,
  deux bases), 65–78 % de GPU, seq 256, lot 8/rang, un fil CPU par rang.
- **Portes** : une porte `drave` consomme ~**8,8 cœurs** ; la passe complète 49 portes dure **1 h 34**.
  Pendant une porte CPU, les deux GPU sont **libres** : on peut y lancer **deux entraînements**, pas
  plus, et garder le reste des cœurs pour la porte.
- **Règle** : les portes d'abord ; ensuite deux entraînements GPU en parallèle, données et docs sur
  les cœurs physiques restants. Ne pas lancer quatre gros travaux CPU « pour aller plus vite » : le
  SMT et les verrous de `/tmp` se disputent.

## La répartition du 26/10 — le langage hors GPU

Décision : **le langage sort des GPU**. Les 2 × RTX 5000 et les CPU servent au **modèle natif**
(`route`, `drave-core`) et aux mesures **boîte blanche** (perplexité, activations, flux, sondes) ;
le langage (traduction, jugements, génération, évaluation) passe par l'API **DeepSeek**.

- **DeepSeek** : professeur et juge ; ses sorties peuvent servir à **distiller** `route` (licence
  explicitement autorisée). Aucun Qwen 3B/7B/14B/32B n'est chargé pour le langage.
- **GPU** : `entrainer_moteur.py` (CUDA), `drave-core`, les portes blanches ; 16 Go par carte,
  NVLink.
- **CPU** : `tools/jeux` (RSN, 71 langues, règles, recherche, maîtres), les portes, les mesures
  hors modèle.
- **Qwen2.5-0.5B** ne reste que comme **référence blanche** des portes historiques, jusqu'à ce que
  `route` les reprenne.
- **Secrets** : clé par variable ou fichier `0600` ; jamais dans le dépôt, le cache ou un message
  d'erreur. Détail : [`docs/implantation/llm-externe.md`](../implantation/llm-externe.md) ; fiche :
  [`reports/rapport-deepseek.md`](../../reports/rapport-deepseek.md).

**Ce que la mesure dit** : DeepSeek `deepseek-flash` sert **310/310** prompts, chrF **82,82** contre
**15,64** de plancher ; la distillation native a une **transition entre 9,23 M et 9,96 M** : négative à **4,04 M**
(2,7510 contre 2,7709), transitoire à **9,23 M** (1 graine/3), positive 3/3 à **9,96 M** (2,7389
contre 2,7881, 1,76 %), **10,70 M** (1,65 %), **16,02 M** (1,92 %) et **22,54 M** (1,74 %). Le
**masque calibré** à 4,04 M est **quasi égal** (2,7335 contre 2,7340, 0,02 %). La prochaine action
est de resserrer la transition et de porter le masque dans le trainer, pas de changer la répartition.

## La philosophie carpe diem

**La règle du jamais-en-attente** : si une ligne de la roadmap est bloquée (un corpus introuvable, un compte, du
matériel), on prend la **suivante** dans l'ordre — la file « jamais en attente » de [`docs/pilotage/roadmap.md`](../pilotage/roadmap.md).
Un agent qui attend est un agent qui n'a pas lu la roadmap.

Tu as beaucoup de ressources et de temps, mais **l'humain n'est pas toujours disponible et son temps de vie est
très précieux**. Tu ne dois donc **jamais suspendre tous les travaux en attendant une réponse**.

- Tire le maximum de chaque journée : chaque moment compte.
- Consolide les questions en attente **à même [`docs/pilotage/en-cours.md`](../pilotage/en-cours.md)** — elles ne bloquent rien.
- Pour les questions qui ne sont **pas** sur la vision ou la philosophie, **tente d'y répondre toi-même** plutôt
  que d'attendre un humain si cela retarde un chantier.
- En cas de doute, **travaille sur plusieurs hypothèses** en parallèle ; la mesure tranchera.
- Ne t'arrête pas parce qu'une échéance est passée : *le temps imparti est un plancher, pas un plafond*
  ([`mission.md`](mission.md)).

## Ce qui reste à l'humain

La **vision** de l'**étage**, la **philosophie** du projet, et les arbitrages qui engagent le sens de la mission. Ils
vont dans `en-cours.md` (section « Questions en attente ») et n'empêchent pas de continuer.
