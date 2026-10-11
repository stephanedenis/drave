# Registre des manques

> 9 octobre 2026. Ce que le dépôt **ne sait pas faire**, consigné comme manque — pas
> comme résultat. Chaque ligne porte la mesure qui l'établit, ce qu'elle bloque, et
> où c'est documenté. Rien ici n'est une feuille de route : la feuille de route est
> `docs/plan-cerveau-complet.md`.

---

## 1. Les manques du MOTEUR

| # | manque | ce qui l'établit (mesure) | ce qu'il bloque | coût |
|---|---|---|---|---|
| **M1** | **noyau de listes pour les experts** — le chargeur refuse Q8_0, les experts sont en Q4_0 (format sans noyau de listes) | `[moe] couche 0 : « blk.0.ffn_gate_exps.weight » de type Q8_0 — format sans noyau ni déquantification` | **un modèle routé ne peut pas être exécuté en listes** : le routage économise des experts, pas des événements | 2-3 sem. |
| **M2** | **noyau de listes sur GPU** — le noyau `proj()` reçoit le vecteur d'activation **complet**, zéros compris | nos projections font **0,45-0,80 Mio** contre un seuil de 8 Mio ; et `proj()` est dense par construction | déporter un modèle creux **détruirait** ce que la parcimonie apporte (on gagnerait la bande passante, on perdrait le saut des lectures) | 3-4 sem. |
| **M3** | **chemin par lots et hyper-connexions** — non porté, et refusé explicitement | `chemin par LOTS et hyper-connexions : ce chemin n'est pas porté (le résidu y est additionné au lieu d'être remélangé par hc_post)` | le lot est **impossible** sur le seul modèle plus gros que la RAM de la machine (V4.1) ; la question « le lot amortit-il les lectures du disque » reste ouverte | 2 sem. |
| **M4** | **encodeurs / embeddings** — ni attention bidirectionnelle, ni pooling | `bge-m3` est lisible en en-tête et **inexécutable** | toute la famille « recherche / similarité / RAG » | 3-4 sem. |
| **M5** | **décodage spéculatif** — aucune ligne de moteur | brouillon générique ×0,70 · paire alignée ×1,09 · brouillon minuscule **×1,52** | la latence du décodage ; mais le cahier des charges est mesuré | 2-3 sem. |
| **M6** | **le moteur n'apprend pas** — il applique, mesure, sauve et recharge une matrice additive, mais ne touche jamais aux poids | notre seule règle locale est **réfutée** (transfert nul, −5 à −10 % hors langue) ; le rejeu est exact et la distillation marche, **hors moteur** | tout apprentissage embarqué (consolidation, adaptation en ligne) | 4-6 sem. |
| **M7** | **qualité des modèles plus gros que la RAM** — coût mesuré, qualité non | V4-Flash : perplexité **659 139** (sans valeur : Q2 + fenêtre de 16 jetons) | on sait qu'ils **tournent**, pas ce qu'ils **valent** | — |
| **M8** | ~~**défaut du variant log-normal** — le fichier sauvé ne reproduit pas le modèle entraîné~~ **CAUSE TROUVÉE ET CORRIGÉE le 2026-10-10 22 h 50** | la **tête liée à la table d'entrée** (`tie_word_embeddings` : `lm_head.weight` **est** `model.embed_tokens.weight`) était reparamétrée comme un `nn.Linear` ordinaire : le partage cassait, la table restait figée pendant l'entraînement, et la matérialisation écrivait ensuite les poids de la **tête** dans la **table** — validation **3,6465 → 8,8257** bits/octet au moment exact de la matérialisation, puis perplexité **436** dans le moteur. Les poids **partagés** sont désormais **exclus** de la reparamétrisation (`--verifier-sauvegarde` : les quatre moments donnent la même perte, ✅). **Le moteur était fidèle** : l'export simulé en PyTorch redonne **exactement** ses chiffres (7,3429 et 436,6) | le variant log-normal d'E6 est de nouveau **mesurable** ; la leçon générale est dans `REPRISE.md` § 3 |

**Et un manque de méthode, qui compte autant** : la lecture disque en mmap atteint
**8,6 Mo/s sur disque dur** contre 243 Mo/s en séquentiel (÷28) — un préchargement
ordonné (`madvise`, lecture des experts par grappe) n'existe pas.

---

## 2. Les manques du MODÈLE (ce qu'aucun modèle d'aujourd'hui ne fait)

| # | manque | ce qui l'établit | ce que ça bloquerait |
|---|---|---|---|
| **N1** | **structure innée à l'échelle** — gratuite à 25 % à dim 384 (+1,0 %), coûteuse à 12,5 % (+13,7 %) **et à dim 512 (+6,7 %)** | E1 et m16, mesurés | un connectome inné viable demande un masque **choisi**, pas aléatoire |
| **N2** | **deux axes appris à l'échelle** — ÷7,8 à dim 384 | m11 mesuré ; m17 (dim 512) en cours | savoir si la recette tient en grandissant |
| **N3** | **règle d'apprentissage locale** — aucune ne transfère | 5 variantes mesurées (nue, nouveauté, valeur, valeur externe, décorrélation) ; la meilleure reste **ne rien faire** | tout apprentissage par impulsions |
| **N4** | **profondeur routée** (mixture-of-depths), **budget d'événements appris**, **quantification adaptée aux listes** | dessins évalués, **jamais entraînés** — et pour H la **borne est maintenant mesurée** : un oracle **parfait** ne sortirait tôt que **30,93 %** des jetons (≈ **10,3 %** des paires), et **aucun seuil de confiance** n'atteint la qualité du chemin long (47,33 % contre 47,73 %) — le facteur limitant est le **chemin court** (adaptateur à 23,19 % contre 47,73 %), pas le routeur — `reports/rapport-design-H-profondeur-routee.md` | les trois leviers inédits de `docs/modele-pour-drave.md` § 3 (H, I, J) |
| **N5** | **mémoire d'un signal injecté** — le modèle n'en a aucune | sonde linéaire **et** non linéaire sur l'état de sortie : le signal **courant** est lisible (**R² 0,992**) mais celui d'il y a 8 pas **ne l'est pas** (−0,681) ; une **structure** (tampon lu directement) le rend **exactement** (1,000) — `reports/rapport-c8-peripherie.md`, `reports/rapport-c2-recurrence.md` | toute tâche qui demande de **retenir** (poursuite, mémoire de travail) côté modèle ; l'engine, lui, sait maintenant retenir (`--memoire`) — ce qui manque est que le **modèle** s'en serve, et c'est un entraînement |

---

| **M9** | ~~aucun instrument ne mesure le coût de la SPARSITÉ DES POIDS~~ **LIVRÉ le 11/10 (les deux moitiés)** | (1) `tools/occupation_poids.py` lit l'occupation d'un GGUF par genre (F32/F16/Q8_0/Q4_0) — c'est lui qui a révélé que le « meilleur point » annulait l'élagage et que l'attention n'était pas élaguée ; (2) le **moteur** affiche désormais `occupation des poids : X % de non-nuls (attention · experts)` et `⇒ si la représentation était CREUSE : Y M paires par token (÷Z)` — les deux lectures collent à **0,0 point** près, et la porte `tools/porte-occupation-moteur.sh` l'exige. Formats 4 bits sans décodeur d'occupation (Q4_K, Q6_K, MXFP4) **comptés à part et affichés** comme non comptés | reste, pour un vrai gain : une **représentation creuse** dont le noyau lit les seuls non-nuls (le gain estimé n'est pas encore un gain mesuré) |

## 3. Les manques d'ARCHITECTURE (pour porter un cerveau)

Les **douze capacités** de `docs/plan-cerveau-complet.md` § 1 — graphe de régions,
liens multiples et récurrence, délais, horloges, bus de modulation, mémoire
épisodique, consolidation, périphérie, latéralité, budgets, instances concertées,
traçage distribué : **zéro est implémentée**. Six phases, 5 à 7 mois, avec leurs
portes mesurées.

---

## 4. Ce qui n'est PAS un manque, et qu'il ne faut pas confondre

- **L'exécution par listes n'approxime rien** : logits identiques **au bit près**
  contre le chemin dense, à encodage de poids égal.
- **Le découpage à deux nœuds est exact** : 0,00e0 (modes 0, 1, 3), et la perplexité
  ne bouge pas jusqu'à 50 ms de latence par message.
- **Le rejeu est exact** : 0,00e0.
- **Les portes du dépôt tournent TOUTES, et toutes passent** : `tools/toutes-les-portes.sh`,
  **27 vertes sur 27, en 60 min 13 s** (mesuré le 2026-10-10 à 21:33 HAE ; détail et durées
  dans `reports/rapport-passe-complete-portes.md`). La ligne qui était ici affirmait « les 23
  portes sont vertes » alors que la suite n'avait **jamais tourné comme une suite** : une
  porte était **rouge depuis le protocole v7** et une autre **verte en ne comparant rien**
  (`porte-tokenizer-kimi`, corrigée). Une porte se lance **toutes ensemble**, sinon elle ne
  vaut que ce que vaut la mémoire de celui qui l'a lancée.
- **La mémoire tient** : 18 aiguilles sur 18 jusqu'à 12 288 jetons.

**La règle de lecture** : un manque est écrit ici avec la mesure qui l'établit ; une
capacité qui marche est écrite avec la mesure qui le prouve. Aucune ligne de ce
document n'est une opinion.
