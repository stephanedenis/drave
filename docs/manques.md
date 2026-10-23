# Registre des manques

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

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
| **M6** | **le moteur n'apprend pas** — il applique, mesure, sauve et recharge une matrice additive, mais ne touche jamais aux poids | notre seule règle locale est **réfutée** (transfert nul, −5 à −10 % hors langue) ; le rejeu est exact et la distillation marche, **hors moteur**. **Premier pas mesuré le 14/10** : la boucle **rejeu (moteur) → mise à jour (torch, LoRA) → mesure (moteur)** est complète et vérifiée — −16,4 % en domaine, **+1,3 % hors domaine** ([`rapport-consolidation-c7.md`](../reports/rapport-consolidation-c7.md)) — mais **la mise à jour n'est pas dans le moteur** | tout apprentissage embarqué (adaptation en ligne, consolidation sans torch) | 4-6 sem. (le reste) |
| **M7** | **qualité des modèles plus gros que la RAM** — coût mesuré, qualité non | V4-Flash : perplexité **659 139** (sans valeur : Q2 + fenêtre de 16 jetons) | on sait qu'ils **tournent**, pas ce qu'ils **valent** | — |
| **M8** | ~~**défaut du variant log-normal** — le fichier sauvé ne reproduit pas le modèle entraîné~~ **CAUSE TROUVÉE ET CORRIGÉE le 2026-10-10 22 h 50** | la **tête liée à la table d'entrée** (`tie_word_embeddings` : `lm_head.weight` **est** `model.embed_tokens.weight`) était reparamétrée comme un `nn.Linear` ordinaire : le partage cassait, la table restait figée pendant l'entraînement, et la matérialisation écrivait ensuite les poids de la **tête** dans la **table** — validation **3,6465 → 8,8257** bits/octet au moment exact de la matérialisation, puis perplexité **436** dans le moteur. Les poids **partagés** sont désormais **exclus** de la reparamétrisation (`--verifier-sauvegarde` : les quatre moments donnent la même perte, ✅). **Le moteur était fidèle** : l'export simulé en PyTorch redonne **exactement** ses chiffres (7,3429 et 436,6) | le variant log-normal d'E6 est de nouveau **mesurable** ; la leçon générale est dans `REPRISE.md` § 3 | [`rapport-m8-log-normal.md`](../reports/rapport-m8-log-normal.md) |
| **M9** | ~~aucun instrument ne mesure le coût de la SPARSITÉ DES POIDS~~ **LIVRÉ le 11/10, les deux moitiés** | (1) `tools/occupation_poids.py` lit l'occupation d'un GGUF par genre ; (2) le **moteur** annonce `occupation des poids` et ce qu'un format creux lirait ; (3) un **noyau creux** réel (`DRAVE_POIDS_CREUX=1`, CSR par lignes) **paie** la sparsité : ÷3,8 de paires sur un modèle élagué à 25 %, qualité identique. **MAIS** sa vitesse ne suit qu'à ~10 % de poids gardés — un régime où un modèle élagué est détruit (perplexité ×41 000) ; à 25 % il est **deux fois plus lent** que les noyaux denses int8 | reste, pour que le compte devienne du temps : un noyau creux **vectorisé** (SIMD, blocs creux alignés sur la quantification) **et** un modèle entraîné à survivre à ces densités — c'est le manque **N4** | — |

**Et un manque de méthode, qui compte autant** : la lecture disque en mmap atteint
**8,6 Mo/s sur disque dur** contre 243 Mo/s en séquentiel (÷28) — un préchargement
ordonné (`madvise`, lecture des experts par grappe) n'existe pas.

**Mesuré, et son premier pas comblé le 12/10** — fiches
[`reports/rapport-prelire-grappe.md`](../reports/rapport-prelire-grappe.md) (le mécanisme, hors
moteur) et [`reports/rapport-s4-prechargement-moteur.md`](../reports/rapport-s4-prechargement-moteur.md)
(la passe réelle). Les chiffres ci-dessus décrivent le régime **à la demande**, et ils tiennent :
**29 Mo/s** au hasard sur l'array, **1 126 Mo/s** sur un motif d'experts. Ce qui paie n'est pas
`madvise` — sur une plage entière il rend **×1,06**, et sa granularité **ne change rien** dans le
moteur (31 à 36 s dans tous les cas) — mais des **fils qui entrent les pages** : la prélecture
parallèle ramène le temps de **calcul** d'une passe de **7,70 s à 3,65 s** (−53 %) et la passe de
35,03 s à 31,21 s, **perplexité identique**. Le témoin `DRAVE_PRELIRE=0` rend le bras « à la
demande » rejouable.

**Deuxième pas, la même nuit** : les **tampons** sont entrés dans le moteur (`DRAVE_TAMPONS=1`) —
les experts **retenus** sont lus par `pread`, **par offset croissant** (donc en séquentiel), dans
des tampons réutilisables, et le calcul lit ces octets. Mesuré sur la même passe à 8 jetons,
cache évincé avant chaque bras : **6,22 Go lus et 3,40 s** de passe, contre **10,90 Go / 3,70 s**
pour les fils qui entrent les pages et **9,52 Go / 5,97 s** à la demande — perplexité identique
dans les quatre bras (`reports/rapport-s4-prechargement-moteur.md` § 5). C'est le seul bras qui
gagne **et** sur les octets **et** sur le temps : la lecture en avance du noyau dépasse la plage
utile de 75 %.

**Ce qui reste ouvert est nommé** : le **pool** et le **recouvrement** (une copie ne se recouvre
pas avec un calcul plus court qu'elle), et le même remède côté **VRAM** — où la mesure montre que
**l'allocation** est 37 à 91 % du coût d'un montage d'expert (`reports/rapport-vram-transfert.md`).

---

## 2. Les manques du MODÈLE (ce qu'aucun modèle d'aujourd'hui ne fait)

| # | manque | ce qui l'établit | ce que ça bloquerait |
|---|---|---|---|
| **N1** | **structure innée à l'échelle** — gratuite à 25 % à dim 384 (+1,0 %), coûteuse à 12,5 % (+13,7 %) **et à dim 512 (+6,7 %)** | E1 et m16, mesurés | un connectome inné viable demande un masque **choisi**, pas aléatoire |
| **N2** | **deux axes appris à l'échelle** — ÷7,8 à dim 384 | m11 mesuré ; m17 (dim 512) en cours | savoir si la recette tient en grandissant |
| **N3** | **règle d'apprentissage locale** — aucune ne transfère | 5 variantes mesurées (nue, nouveauté, valeur, valeur externe, décorrélation) ; la meilleure reste **ne rien faire** | tout apprentissage par impulsions |
| **N4** | **profondeur routée** (mixture-of-depths), **budget d'événements appris**, **quantification adaptée aux listes** | dessins évalués ; le **chemin court entraîné** (dessin B) est mesuré depuis le 14/10 et **exécuté par le moteur** — ÷1,47 / ÷1,24 à profondeur 8 lus par `drave` (`reports/rapport-n4-porte-execution.md`), ÷1,32 à ÷1,83 selon la profondeur en torch (`reports/rapport-n4-dessin-b.md`) ; reste la variabilité entre exécutions (±10 %) et la génération libre — et pour H la **borne est maintenant mesurée** : un oracle **parfait** ne sortirait tôt que **30,93 %** des jetons (≈ **10,3 %** des paires), et **aucun seuil de confiance** n'atteint la qualité du chemin long (47,33 % contre 47,73 %) — le facteur limitant est le **chemin court** (adaptateur à 23,19 % contre 47,73 %), pas le routeur — `reports/rapport-design-H-profondeur-routee.md` | les trois leviers inédits de `docs/modele-pour-drave.md` § 3 (H, I, J) |
| **N5** | **mémoire d'un signal injecté** — le modèle n'en a aucune, **et il ne l'APPREND pas** | sonde linéaire **et** non linéaire sur l'état de sortie : le signal **courant** est lisible (**R² 0,992**) mais celui d'il y a 8 pas **ne l'est pas** (−0,681). **Entraînement mesuré le 14/10** (`tools/memoire_travail.py`) : 8 époques de LoRA rang 8 sur les 24 couches, et la mémoire **recule** (−1,091 → **−2,773**, contrôle à cibles mélangées −2,855) — pendant qu'avec le **tampon** dans l'entrée le modèle **gelé** lit déjà (+0,879) et l'entraîné fait mieux (+0,964) ; le moteur confirme la direction (+0,766 non linéaire contre −0,493). `reports/rapport-memoire-travail-n5.md` | toute tâche qui demande de **retenir** (poursuite, mémoire de travail) côté modèle : **la structure est le mécanisme efficient** (tampon : R² 1,000, zéro paire) ; ce qui reste ouvert est de faire **servir** la mémoire par le réseau (une tâche, pas une sonde) |

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
