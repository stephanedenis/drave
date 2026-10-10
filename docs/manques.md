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
| **M8** | **défaut de sauvegarde du variant log-normal** — le fichier sauvé ne reproduit pas le modèle entraîné | entraînement 2,2662 bits/octet ; fichier sauvé **13,0614** avec le protocole de l'entraînement, 15 552 en référence PyTorch | le variant est marqué **inutilisable** dans l'aide du harnais ; cause ouverte (matérialisation **éliminée** : écart 0,000e+00) | à diagnostiquer |

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
| **N4** | **profondeur routée** (mixture-of-depths), **budget d'événements appris**, **quantification adaptée aux listes** | dessins évalués, **jamais entraînés** | les trois leviers inédits de `docs/modele-pour-drave.md` § 3 (H, I, J) |

---

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
  **23 vertes sur 23, en 59 minutes** (mesuré le 2026-10-10 à 17 h 55 HAE ; détail et durées
  dans `reports/rapport-passe-complete-portes.md`). La ligne qui était ici affirmait « les 23
  portes sont vertes » alors que la suite n'avait **jamais tourné comme une suite** : une
  porte était **rouge depuis le protocole v7** et une autre **verte en ne comparant rien**
  (`porte-tokenizer-kimi`, corrigée). Une porte se lance **toutes ensemble**, sinon elle ne
  vaut que ce que vaut la mémoire de celui qui l'a lancée.
- **La mémoire tient** : 18 aiguilles sur 18 jusqu'à 12 288 jetons.

**La règle de lecture** : un manque est écrit ici avec la mesure qui l'établit ; une
capacité qui marche est écrite avec la mesure qui le prouve. Aucune ligne de ce
document n'est une opinion.
