# L'architecture du cerveau — et ce qui manque à Drave pour la porter

> 9 octobre 2026. `docs/biologie-pour-drave.md` traitait de la **brique** (le
> neurone, la synapse, l'énergie). Ce document traite de l'**édifice** : les régions,
> les fibres, les noyaux, les organes — et fait l'inventaire de ce que Drave possède
> déjà, de ce qui lui manque **comme moteur**, et de ce qu'il ne faut pas copier.

---

## 1. L'architecture, en chiffres mesurés

| structure | ce qui est établi | source |
|---|---|---|
| **cortex** | ~16 × 10⁹ neurones, découpé en **180 aires** par hémisphère — la carte n'est pas arbitraire, elle est multi-modale (connexions, myéline, fonction) | [Glasser et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27437579/) |
| **corps calleux** | ~2 × 10⁸ axones reliant les deux hémisphères, majoritairement **homotopiques** (aire ↔ aire symétrique) | [Hubel, *Eye, Brain and Vision*, ch. 7](http://hubel.med.harvard.edu/book/ch7.pdf) |
| **thalamus** | relais de **toutes** les modalités sauf l'olfaction — et surtout **boucles cortico-thalamo-corticales** : la plupart des échanges cortico-corticaux passent par lui | — |
| **hippocampe** | circuit trisynaptique (cortex entorhinal → gyrus denté → CA3 → CA1), mémoire **épisodique**, et **rejeu** des séquences pendant les ondes sharp-wave | [Phil. Trans. R. Soc. B 2020](https://royalsocietypublishing.org/rstb/article/375/1799/20190236/23761/Potential-factors-influencing-replay-across-CA1) |
| **cervelet** | de l'ordre de **7 × 10¹⁰ neurones** — plus que tout le reste du cerveau réuni —, une seule sortie (cellule de Purkinje), un seul signal d'erreur (fibre grimpante) | Herculano-Houzel |
| **système visuel** | rétine → nerf optique (**~1,2 × 10⁶ axones** de cellules ganglionnaires) → LGN → V1, et une fraction majeure du cortex | [NCBI, nerf optique](https://www.ncbi.nlm.nih.gov/books/NBK507907/), [encyclopédie du cortex visuel](https://stanford.edu/~wandell/data/papers/2024_Encyclopedia_Human%20visual%20cortex.pdf) |
| **neuromodulation** | des noyaux **minuscules** (locus coeruleus : quelques dizaines de milliers de neurones) projettent **partout** et changent le gain de tout le reste | [Luo lab, Stanford](https://luolab.stanford.edu/news/shades-blue-how-position-gradually-shapes-structure-and-function-locus-coeruleus) |
| **substance blanche** | de l'ordre de 1,5 × 10⁵ km d'axones myélinisés, vitesses de conduction de 1 à 100 m/s → **délais de 1 à 100 ms** entre régions | ordres de grandeur publiés |
| **périphérie** | moelle épinière (qui **décide** sans le cortex : réflexes), motoneurones, nerfs | — |

**Le contraste avec un transformeur est brutal** : ce n'est pas un empilement de
couches, c'est un **graphe** de régions, avec des **délais**, des **boucles**, des
**noyaux diffuseurs**, **deux mémoires** et une **périphérie**.

---

## 2. Les six motifs qui font « cerveau » plutôt que « réseau »

1. **Boucles, pas seulement hiérarchie.** Les projections descendantes sont aussi
   nombreuses que les montantes : chaque aire est à la fois prédicteur et prédite.
2. **Noyaux diffuseurs.** Quelques dizaines de milliers de neurones (noradrénaline,
   dopamine, sérotonine, acétylcholine) modifient le **gain** de milliards d'autres —
   un scalaire global, pas un chemin de données.
3. **Deux mémoires, deux vitesses.** Épisodique et rapide (hippocampe, écriture en un
   seul passage), sémantique et lente (cortex, consolidation par **rejeu**).
4. **Le temps compte.** Des délais de conduction de 1 à 100 ms font partie du calcul
   (synchronie, oscillations) ; il n'y a **aucune horloge globale**.
5. **Latéralité.** Deux hémisphères quasi symétriques, reliés par un faisceau massif,
   avec des voies croisées (décussation) dans la périphérie.
6. **La périphérie a sa propre intelligence.** La moelle épinière produit des
   réflexes complets sans le cerveau : le corps n'est pas un capteur passif.

---

## 3. Ce que Drave possède déjà, et à quoi cela ressemble

| primitive du moteur | structure cérébrale qu'elle approche | l'écart |
|---|---|---|
| **plages de couches + nœuds distants** (flux TCP, écart 0,00e0, modes 0-4) | fibres entre régions | c'est une **chaîne** 1→1, pas un graphe : pas de plusieurs entrées, pas de récurrence |
| **listes d'événements** (paires poids × activation) | axone qui ne transporte que ce qui compte | la topologie reste celle du modèle, pas celle d'une région |
| **cache KV** (paginé, int8, partagé/compressé, MLA) | mémoire de travail | une seule mémoire, pas d'écriture en un coup |
| **routage d'experts**, clusters, nœud partiel | **aires spécialisées** — le seul mécanisme de régionalisation existant | les experts sont dans *une* couche ; il n'y a pas d'aire avec ses propres entrées/sorties |
| **engram** (adressage par hachage, injection branchée) | mémoire associative rapide — le plus proche d'un hippocampe | pas de consolidation vers les poids |
| **traces DRVF + rejeu** (écart 0,00e0) | rejeu hors ligne | le rejeu existe ; la **consolidation** n'existe pas |
| **`patch`** (greffe d'un neurone sans réentraînement) | croissance locale | un neurone, à une couche, sans règle de naissance |
| **capteur + adaptateur hebbiens** | plasticité locale | **mesuré et réfuté en l'état** (§ 5 bis de `docs/impulsion-pure-apprenant.md`) |
| **hyper-connexions** (V4) | mélanges résiduels appris | motif de *couche*, pas de région |
| **banc vision** (embedding de patchs) | entrée sensorielle | pas de boucle sensorimotrice, pas d'effecteur |
| **GPU par projection, NVLink, NUMA** | tissu hétérogène | le moteur mesure déjà les octets, les paires et les temps par lien |

**En une phrase** : Drave possède les **briques** d'une architecture cérébrale
(événements, mémoire adressable, rejeu, routage, transport exact entre nœuds) et
aucune de ses **formes** (graphe, délais, boucles, noyaux diffuseurs, consolidation).

---

## 4. Les manques, par ordre de coût de mise en œuvre

Chacun est justifié par une mesure du dépôt, pas par l'analogie.

| # | manque | ce que ça débloque | coût | justification mesurée |
|---|---|---|---|---|
| **M1** | **bus de neuromodulation** : un scalaire diffusé à toutes les couches pendant une passe | l'apprentissage local devient possible (troisième facteur) | **faible** — un scalaire dans l'état du moteur | E7 mesuré : moduler par la **nouveauté** dégrade (+20,4 %) ; ce qui manque est un signal de **valeur**, et la distillation (notre seule valeur) marche |
| **M2** | **topologie en graphe** : plusieurs entrées par unité, sorties multiples, récurrence, ordonnancement | boucles, thalamus, régions qui se parlent | **élevé** — le moteur exécute une chaîne | le découpage prouvé aujourd'hui est une **plage de couches** ; toute la Phase 3 repose sur cette forme |
| **M3** | **délais par lien** | le temps comme information (synchronie) | **faible côté moteur** (attendre), **élevé côté modèle** (il faut que ça serve) | la carte de latence est mesurée : **3,4 ms par jeton et par ms de RTT** ; on sait donc déjà ce qu'un délai coûte |
| **M4** | **module épisodique adressable** : écriture en un coup, lecture par similarité | mémoire d'un épisode, pas d'un texte | **moyen** — l'engram est la moitié du chemin | l'engram existe (adressage vérifié sur 479 723 rangées) ; le cache KV est une mémoire *par position*, pas par contenu |
| **M5** | **consolidation** : rejeu → poids | apprendre sans repasser par l'entraînement hors moteur | **élevé** — c'est de l'apprentissage | le rejeu est exact (0,00e0) et la distillation marche ; entre les deux, il n'y a rien |
| **M6** | **interface périphérique** : capteurs continus, effecteurs, boucles réflexes locales | un agent, pas un modèle de langue | **moyen** | le banc vision lit des patchs ; rien ne sort du moteur |
| **M7** | **latéralité / corps calleux** : deux copies + échange massif | redondance, spécialisation | **faible** (c'est du découpage par couches) | on sait découper à 0,00e0 ; le gain, lui, n'est **pas** démontré |
| **M8** | **budgets par lien** (énergie, bande passante) | un planificateur au lieu de mesures | **moyen** | le moteur mesure octets, paires, temps ; il n'impose aucune contrainte |

---

## 5. Ce qu'il ne faut PAS copier

- **Le cortex n'est pas un transformeur, et l'inverse est vrai aussi.** On ne sait
  pas si une architecture de régions apporte quoi que ce soit à un modèle de langue :
  c'est une **hypothèse**, pas un résultat — et ce document ne la présente pas comme
  telle.
- **Pas de rétropropagation dans le cerveau.** Nos modèles en vivent. Copier
  l'architecture en gardant l'apprenant est un mélange non testé.
- **Pas d'horloge globale, pas de tokens.** Nos passes sont synchrones et
  discrètes ; introduire des délais sans introduire d'asynchronisme ne donne rien.
- **Le corps n'est pas un accessoire.** Un cerveau sans périphérie n'a ni fonction ni
  critère d'évaluation ; ajouter des régions sans tâche ne se mesurerait pas.
- **Et une réserve de méthode** : les chiffres du § 1 sont des ordres de grandeur
  publiés (sauf indication), pas des comptages sur cette machine — et **aucune** des
  structures décrites ici n'a été simulée ici.

---

## 6. Le plan minimal qui répondrait à des manques MESURÉS

Sur les huit manques, deux seulement correspondent à un défaut que **nos propres
mesures** ont identifié :

1. **M1 (bus de neuromodulation)** — parce que notre seule règle d'apprentissage
   locale a été réfutée *faute de signal de valeur*, et que nous avons mesuré que la
   nouveauté n'en est pas un. Un scalaire diffusé par passe, modulé par la perte ou
   par un enseignant, est le mécanisme le moins cher qui manque.
2. **M4 + M5 (mémoire épisodique et consolidation)** — parce que le moteur sait déjà
   **rejouer** une passe à l'identique et **distiller** ; il ne sait pas écrire un
   épisode en un coup ni le consolider. C'est le couple qui transformerait le rejeu
   (déjà exact) en apprentissage (déjà outillé, mais hors moteur).

Les six autres (graphe, délais, périphérie, latéralité, budgets) sont des chantiers
d'architecture qui n'ont d'intérêt **que si un modèle en a besoin** — et aucun modèle
n'existe aujourd'hui qui les réclame. Les ouvrir sans modèle serait construire une
route sans véhicule ; c'est écrit ici pour que la décision soit explicite.
