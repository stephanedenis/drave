# Sprint 12 — La rotation des couches compressées : un correctif, et l'instrument qui mentait

- **Début** : 19:30 · **Fin** : 21:30 (bloc de 120 min)
- **Objectif** : fermer les questions ouvertes du bloc précédent — la mesure
  manquante du YaRN, la sélection de l'indexeur sur V4.1, les trous relevés par
  la relecture adverse.
- **Engagement de fin** : dépôt vert, mesures consignées, machine rendue.

## Le résultat

**Le correctif YaRN est validé par la mesure, et il cachait un bug d'instrument.**

| question | réponse |
|---|---|
| llama.cpp applique-t-il YaRN sur ses couches compressées ? | **oui** — mesuré : à la position 127, YaRN donne 4,515e-03 d'écart contre 5,376e-03 pour le RoPE simple, et la corrélation monte (0,999996 contre 0,999993). L'écart se réduit de 15 %, et le gain croît avec la position |
| pourquoi la première comparaison disait-elle l'inverse ? | parce que la **rampe** du moteur était calculée avec un contexte d'origine de **4 096** au lieu de 65 536 : `Meta::as_f64()` ne lit que les flottants et `rope.scaling.original_context_length` est un **u32** — `None`, donc le défaut |
| comment l'a-t-on vu ? | en remontant des écarts aux **angles** appliqués, paire par paire (`θ = atan2(b'·a − a'·b, a·a' + b·b')`) : la rampe mesurée était (8, 18), la rampe attendue (15, 25) |
| le sélection de l'indexeur s'exerce-t-elle sur V4.1 ? | **oui** : à la position 512 d'une couche de ratio 1, 513 blocs → **512 gardés**, et le masque est le top-k des scores (cas serré à 2,7e-05) |

## Ce que la relecture adverse a trouvé (et ce qui a été corrigé)

| trouvaille | gravité | correctif |
|---|---|---|
| `--sans-yarn` ne coupait PAS le YaRN des couches compressées (`cfg_yarn_off` ne touchait que `cfg.yarn`, lu par les seuls chemins denses) | **faux** | `cfg_yarn_off` vide aussi `yarn_declare` et `yarn_compresse` ; mesuré avant/après (64 730 738 contre 65 819 810) |
| `corr0`/`corr1` non bornées (ggml et vLLM les bornent) | trou | `MAX(0,·)`, `MIN(n_dims − 1,·)` |
| l'annonce de rotation disait « RoPE simple » sur un modèle dont 41 couches sur 44 sont en YaRN | faible, mesuré | la ligne dit maintenant les DEUX régimes |
| justification du mscale citée de travers (c'est `dsv4_rope_attn_factor`, pas `llama-context`) | faible | citation corrigée, conclusion inchangée (produit = 1,0) |
| le refus `candidate_*` s'appliquait à TOUTES les couches à indexeur (vLLM ne masque que celles après la source) | sur-refus | restreint à `l > candidate_source_layer_id` |
| `tools/rope_yarn_temoin.py` cité par un test… n'existait pas | faible | écrit, et il recalcule le témoin depuis ggml |
| l'oracle `v41_compresseur_reference.py` resté en RoPE simple | faible | mis à la convention du moteur (YaRN dès ratio > 0) |
| l'engram acceptait des entrées mal formées en silence (`zip` tronquant vers une adresse VALIDE 0, id hors `token_map` → pad muet, positions dupliquées) | trou | refus explicites (longueurs, croissance stricte, id hors table, `max_ngram ≥ 2`) |
| `indexer.attn_k` sur une consommatrice écrivait dans le tampon aliasé de sa source | trou | refusé (posséder le cache d'indexeur = être une source de KV) |

Ce que la relecture a confirmé, mesure à l'appui : l'équivalence YaRN ↔ ggml
(**1,8e-12** sur 309 positions, rampe identique à 0,000e+00, mscale net 1,0), le
hachage d'engram sur la fenêtre (**180 259 comparaisons, 0 désaccord**), la
projection et l'injection de l'engram (noyau vLLM identique ligne à ligne),
l'indexeur de V4.1 conforme (une clé de 128 par bloc, cache possédé par 2/8/14/20
seulement — inventaire GGUF à l'appui), et la sélection (**135 460 accords sur
135 460**).

## Introspection

**1. Un instrument faux ne se voit pas dans ses propres mesures.** La rampe
mesurée (8, 18) ne « sentait » pas l'erreur : elle était plausible, stable, et
reproductible. Ce qui l'a démasquée n'est pas un test unitaire — la fonction
`rope_norm_yarn` était *juste*, vérifiée au 1e-12 contre ggml — mais le **chemin
complet** : la valeur passée en paramètre ne venait pas d'où je croyais. Le test
unitaire testait la fonction ; il ne testait pas la *lecture des métadonnées*.

**2. Le type d'une clef GGUF est une donnée, pas un détail.** `as_f64` sur un
`u32` ne lève pas : il rend `None`, et le défaut prend la place. C'est le même
motif que le `n_expert` relu en GGUF-seul du bloc précédent, et le même que le
`rms_norm_eps` : une valeur *absente* remplacée par une valeur *plausible*. Les
trois ont été trouvés par une mesure de bout en bout, aucun par relecture.

**3. La relecture adverse a trouvé ce que mes vérifications ne cherchaient pas.**
Neuf trouvailles, dont deux « FAUX » : un drapeau CLI inerte sur 41 couches sur 44,
et une phrase de commentaire qui mentait sur sa propre fenêtre. Aucune n'était
dans le périmètre de mes scripts — ils vérifient des *nombres*, pas des
*contrats* (ce qu'un drapeau annonce, ce qu'un commentaire promet).

**4. Deux références qui semblent d'accord peuvent diverger à l'exécution.** La
première mesure disait « llama.cpp ne fait pas ce que son code dit » : c'était
faux, et j'ai failli l'écrire. La bonne réaction n'est pas de choisir la source
qui arrange, c'est de chercher **pourquoi** la mesure contredit la source — ici,
un paramètre lu de travers. Une divergence entre références est une hypothèse à
creuser, pas une conclusion.

## Ce qui reste, nommé

- La **porte V4-Flash** doit être re-mesurée (la rampe corrigée change le
  chiffre) : la valeur attendue de `tools/portes.sh` est mise à jour avec sa
  raison, et les chiffres V4-Flash antérieurs au 03/10 sont à revérifier.
- Les preuves dans `/tmp` (vides engram, indexeur, YaRN) sont **transitoires** :
  les commandes sont dans les rapports, pas les artefacts. Un dépôt de vides
  versionné serait la vraie réponse (à trancher : taille contre rejouabilité).
- La **sélection à deux niveaux** reste non portée, mais refusée au bon seuil
  (`candidate_topk_blocks × candidate_block_size`).
- Le **pré-mix sur le fil DRVF** (le dernier refus pour un V4.1 découpé) : les
  deux champs sont posés côté moteur (`hc_porte_flux`, `hc_porte_imposee`), le
  protocole reste à passer en v6.
