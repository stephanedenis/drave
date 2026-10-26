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
  d'erreur. Détail : [`docs/llm-externe.md`](../llm-externe.md) ; fiche :
  [`reports/rapport-deepseek.md`](../../reports/rapport-deepseek.md).

**Ce que la mesure dit** : DeepSeek `deepseek-flash` sert **310/310** prompts, chrF **82,82** contre
**15,64** de plancher ; la distillation native a un **seuil de capacité** : négative à **4,04 M** (contrôle 2,7510 contre
aligné 2,7709), positive à **22,54 M** (aligné 2,6915 contre contrôle 2,7393, 3/3 graines). La
prochaine action est de **localiser le seuil** et de tester une **perte masquée sur les prompts**,
pas de changer la répartition.

## La philosophie carpe diem

**La règle du jamais-en-attente** : si une ligne de la roadmap est bloquée (un corpus introuvable, un compte, du
matériel), on prend la **suivante** dans l'ordre — la file « jamais en attente » de [`docs/roadmap.md`](../roadmap.md).
Un agent qui attend est un agent qui n'a pas lu la roadmap.

Tu as beaucoup de ressources et de temps, mais **l'humain n'est pas toujours disponible et son temps de vie est
très précieux**. Tu ne dois donc **jamais suspendre tous les travaux en attendant une réponse**.

- Tire le maximum de chaque journée : chaque moment compte.
- Consolide les questions en attente **à même [`docs/en-cours.md`](../en-cours.md)** — elles ne bloquent rien.
- Pour les questions qui ne sont **pas** sur la vision ou la philosophie, **tente d'y répondre toi-même** plutôt
  que d'attendre un humain si cela retarde un chantier.
- En cas de doute, **travaille sur plusieurs hypothèses** en parallèle ; la mesure tranchera.
- Ne t'arrête pas parce qu'une échéance est passée : *le temps imparti est un plancher, pas un plafond*
  ([`mission.md`](mission.md)).

## Ce qui reste à l'humain

La **vision** de l'**étage**, la **philosophie** du projet, et les arbitrages qui engagent le sens de la mission. Ils
vont dans `en-cours.md` (section « Questions en attente ») et n'empêchent pas de continuer.
