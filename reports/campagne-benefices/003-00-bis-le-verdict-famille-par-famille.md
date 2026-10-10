> Campagne : **campagne-benefices** · expérience **00-bis**
> Titre : 0 bis. Le verdict, famille par famille
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 0 bis. Le verdict, famille par famille

Le tableau qui répond à la question posée, chaque ligne portant sa mesure. ⏳ =
file encore en cours.

| famille de tâches | verdict | mesure |
|---|---|---|
| **langage** (perplexité) | ✅ tourne — **le routage gagne aux petites échelles, et PERD à dim 512** | à lecture égale : dim 256 dense **5,0155** → routé **4,8858** (−2,6 %) → **distillé 4,7642 (−5,0 %)** · dim 384 : 5,0108 → 4,8646 (−2,9 %) · **dim 512 : 4,5686 → 5,0255 (+10 %)**, 12,8 M paires/jeton des deux côtés (§ 5 bis) |
| **génération / latence** | ✅ mesuré | TTFT **27,9 ms**, **29,0 tok/s** (0,5 B) · 114,6 ms, 7,1 tok/s (1,5 B) |
| **contexte long — la mémoire** | ✅ **elle tient, et plus loin qu'annoncé** | **18 aiguilles sur 18** retrouvées, de 512 à **12 288 jetons**, à 10 %, 50 % et 90 % de profondeur (§ 9) |
| **contexte long — le coût** | ✅ réglable | KV int8 : +1,5 % (512 j.) à +3,0 % (8 192 j.) · paginé : **0,03 Go au lieu de 25,77 Go** à 1 M |
| **préremplissage par lots** | ✅ ×1,4 en RAM, ⚠️ disque non testé | 0,5 B, 512 jetons : **16,8 → 23,7 tok/s** et PPL **identique** (13,1368 → 13,1359) · sur le 30B le lot n'a lu que le **cache de pages** (10,9 Go à froid, 0 ensuite) |
| **code** | ✅ mesuré, décalage de tâche | codestral-22B : **133,08** de PPL sur de la prose (255 jetons) = **1,842 bit/octet**, contre **0,983** pour un 0,5 B — un 22 B **1,87× pire** qu'un 0,5 B hors de sa tâche |
| **raisonnement** | ✅ mesuré, contre-intuitif | r1-distill-1.5B : **1,326 bit/octet**, **2,7× pire** que le 0,5 B (0,983) |
| **MoE / routage d'experts** | ✅ mesuré | 4 experts sur 128 (3,1 %) · déséquilibre **×3,90** · **847 octets** par jeton à router |
| **multilingue (399 langues)** | ✅ mesuré, et c'est le point faible du modèle | **3,227 bit/octet** contre 0,951 en prose — **3,4× pire** · densité **identique** (71 %) · seuil absolu : PPL **×11**, le k-WTA tient (§ 10 ter) |
| **sémantique multilingue** | ✅ le résultat publié **survit** au correctif d'échelle | pic de séparation à la **couche 13** (+0,0391) sur 398 langues, bande 10-15 — et l'ancien lecteur donnait +0,0349 au même endroit |
| **parcimonie imposée** | ✅ reproduit, et nuancé | à −30 % d'événements : seuil **+69 %** de PPL, k-WTA **+4 %** (facteur 17) · en dense, **aucune lecture économisée** |
| **parcimonie APPRISE** | ✅ **la réponse qui décide** — et elle est nette | à 50 % gardés : témoin **5,3032**, `kwta050` **5,0606 (−4,6 %)** · à 25 % : témoin **10,8758**, `kwta025` **5,1719 (−52 %)** · **chaque modèle n'est bon que dans son régime** · à dim 512 la recette tient (**6,0503 → 4,9649**, lecture ÷4) — mais le débit ne distingue plus listes et dense (213 contre 211 tok/s) : **le modèle tient dans les caches, les lectures économisées étaient gratuites** (§ 5 ter) |
| **sortie contrainte** | ✅ **gagne par construction** | **×1,36-1,42** de débit *et* garantie que la sortie appartient à l'ensemble autorisé |
| **modèle plus gros que la RAM** | ✅ **démontré, et vérifié au chiffre près** | V4-Flash **365,7 Go sur 125 Go de RAM** : **37,6 Go résidents**, 37,7 Go lus, 266 s pour 16 jetons · gpt-oss (63 Go) : **PPL 15,6017 sur 510 jetons — la valeur attendue, à l'identique** (porte tenue à 02 h 58) |
| **répartition à deux nœuds** | ✅ **porte tenue** | écart **0,0000 %** et flux **0,00e0** — sur le modèle dense, routé **et distillé** |
| **embeddings / recherche** | ❌ **manque** | `bge-m3` lisible en en-tête, **inexécutable** (ni encodeur bidirectionnel ni pooling) |
| **décodage spéculatif** | ⚠️ **le chantier n'existe pas, mais le gain est démontré dans la niche du projet** | trois paires mesurées par le moteur : ×0,70 (brouillon à 0,21×) · ×1,09 (0,13×) · **×1,52 pour un brouillon à 0,039× de sa cible** — c'est le **rapport de coût** qui décide, et il est minimal quand la cible est bornée par le disque (§ 1 bis) |
| **routage à l'échelle** | ⚠️ **le routage seul s'inverse à dim 512, la distillation le rattrape et dépasse** | routé seul : −3,5 % (val, 256) → −1,4 % (384) → **+1,4 % (512)** · **routé distillé : 4,3305 contre 4,5686 au dense (−5,2 %)**, le gain du distillat croissant avec la taille (−2,5 % → −9,3 % → **−13,8 %**) · **12,8 M paires/jeton des deux côtés** |
| **structure innée** | ✅ **le masque aléatoire coûte 1 % et divise les lectures par 4** | connectome tiré à la naissance (25 % des connexions, jamais modifié) : **5,0472** contre 4,9959 au témoin dense, **81,6 M** d'événements/fenêtre contre 336,7 M, **276** tok/s contre 131 (§ 4 bis de `biologie-pour-drave.md`) |
| **fidélité listes ↔ dense** | ✅ **exacte, démontrée** | logits identiques **au bit près** (`cmp` sur 4 254 216 octets) et mêmes jetons gloutons, à encodage de poids égal ; ×0,02 à ×3,19 selon la densité |

**En une phrase** : Drave gagne **par construction** sur les sorties contraintes,
**par sa structure** quand le modèle est creux — mais seulement aux petites
échelles : le routage entraîné rend −2,6 % à dim 256 et −2,9 % à dim 384, puis
**+10 % (il perd) à dim 512**, à lecture égale (12,8 M paires/jeton des deux côtés,
§ 5 bis) — **par ses circonstances** sur les modèles plus gros que la RAM, et
**perd** sur un modèle dense ordinaire, où le chemin par listes coûte 1,8 à 2,1×
pour rien.

**Trois documents accompagnent ce rapport** : `docs/modele-pour-drave.md` (quel
modèle *ad hoc* l'architecture récompense — moteur contre modèle, dix dessins
évalués), `docs/biologie-pour-drave.md` (ce que les connectomes imposent comme
contraintes, et l'expérience E1 mesurée) et `docs/impulsion-pure-apprenant.md` (un
exécutant événementiel n'est pas encore un apprenant événementiel, et pourquoi).

**Quatre corrections de méthode sont consignées dans ce rapport**, et elles
comptent autant que les chiffres : le tokenizer étranger (`data/…ids`, facteur
442), la fenêtre d'évaluation trop courte (trois protocoles, trois réponses), le
cache qui survit à son correctif, et le **binaire plus vieux que ses correctifs**
— trois commits de `drave-core/src` n'étaient pas dans le binaire qui a mesuré la
campagne (§ 17).

### 0 ter. L'état de la campagne au 9 octobre, 1 h 05

Les **neuf étapes** de `tools/campagne-benefices.sh` sont allées au bout
(`=== campagne terminée ===` à 01 h 03), et les portes rendent **22 vertes · 1
rouge** — puis, à 02 h 58, **23 vertes · 0 rouge**.

| porte | état | ce qui s'est passé |
|---|---|---|
| `gpt-oss-120b MXFP4 ctx 256` — attendu **15.6017** | ✅ **rend 15.6017 sur 510 jetons**, au chiffre près | elle avait expiré **deux fois** (2 400 s puis 5 400 s). Le délai était en cause, pas le moteur : à 0,074 tok/s mesuré (32 jetons en 432 s), 512 jetons demandent ~1 h 55. Délai recalibré (`GATE_GPTOSS_DELAI`, défaut 9 000 s) ; relancée seule, elle rend la valeur **attendue à l'identique** |

Tout le reste est vert, y compris `cargo test --release` (**77 tests**), les 17
formats confrontés à libggml, la porte de correction contre llama.cpp
(100 % des positions utiles au-dessus de 0,95, top-1 94,4 %), la porte Mistral, et
les cinq modes de découpage à deux nœuds (écart **0,00e0** pour les modes 0, 1 et
3, 3,65e-2 pour le mode 2, 4,45e-3 pour le mode 4).

**Ce que cette porte dit vraiment** : le moteur reproduit **au chiffre près** la
perplexité de référence d'un modèle de 63 Go en MXFP4, exécuté en dense, sur le
disque. C'est la vérification la plus lourde du dépôt, et elle ne tenait qu'à un
délai mal calibré — une porte qui ne peut pas passer ne vérifie rien, et celle-ci
était dans ce cas depuis sa mise en service.

---
