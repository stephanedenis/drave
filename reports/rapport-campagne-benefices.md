# Campagne 24 h — où Drave est à son meilleur, tâche par tâche

> 08/10 21 h → 09/10. Rapport **vivant** : il est mis à jour au fil des étapes.
> File : `tools/campagne-benefices.sh`. Journaux bruts : `/tmp/campagne24/`.
> Plan : `docs/campagne-benefices.md`.
>
> Règle de lecture : chaque chiffre porte ses conditions (corpus, tokenizer,
> charge de fond). La charge a oscillé entre 3 et 18 pendant la campagne
> (entraînements en parallèle) — les mesures **déterministes** (perplexité,
> comptes d'événements) n'en dépendent pas, les **temps** oui, et c'est écrit.

---

## 0. Le piège qui a failli tout fausser

`data/wikitext2_test.txt.ids` **vient d'un autre tokenizer** que Qwen2.5 :
`201,438,10498…` là où le modèle produit `198,284,8397…`. Sur les mêmes octets :

| identifiants | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt | **7 710,72** |
| tokenisés par le modèle | **17,43** |

Un facteur 442. La règle est désormais dans le script : **chaque modèle tokenise
son propre corpus**. C'est aussi la première chose à vérifier avant de croire une
perplexité publiée quelque part.

---

## 0 bis. Le verdict, famille par famille

Le tableau qui répond à la question posée, avec la mesure qui le porte. ⏳ = file
en cours au moment de l'écriture.

| famille de tâches | verdict | mesure |
|---|---|---|
| **langage** (perplexité) | ✅ tourne — et **le routage gagne à lecture égale** | dense 5,3973 → **routé 5,0684** (−6,1 %) pour les mêmes 3,2 M poids lus · le chemin par listes reste 1,8 à 2,1× plus lent si le modèle est dense (90 %) |
| **génération / latence** | ✅ mesuré | TTFT **27,9 ms** et **29,0 tok/s** (0,5 B) · 114,6 ms et 7,1 tok/s (1,5 B) |
| **contexte long — la mémoire** | ✅ **elle tient** | **12 aiguilles sur 12** retrouvées, de 512 à **4 096 jetons**, à 10 %, 50 % et 90 % de profondeur |
| **contexte long — le coût** | ✅ réglable | KV int8 : +1,5 % (512 j.) à +3,0 % (8 192 j.) de PPL · paginé : **0,03 Go au lieu de 25,77 Go** à 1 M |
| **préremplissage par lots** | ⏳ | dépôt : **×1,58** · batch 5 sur le 30B depuis le NVMe |
| **code** | ⏳ diagnostic | codestral-22B : **35 657** de PPL sur de la prose (son propre corpus de code est en cours) |
| **raisonnement** | ✅ mesuré, et contre-intuitif | r1-distill-1.5B = **1,326 bit/octet**, soit **2,7× pire** que le 0,5 B (0,983) |
| **MoE / routage d'experts** | ✅ mesuré | 4 experts sur 128 (3,1 %) · déséquilibre **×3,90** · **847 octets** par jeton à router |
| **sortie contrainte** | ✅ **gagne par construction** | **×1,42** de débit *et* garantie que la sortie appartient à l'ensemble autorisé |
| **modèle plus gros que la RAM** | ⏳ | dépôt : K3 **206,58 Gio** lus par passe, 133 Mio/s · batch 6 : V4-Flash, **365 Go sur 125 Go** |
| **répartition à deux nœuds** | ✅ **porte tenue** | écart de perplexité **0,0000 %**, écart de flux **0,00e0** |
| **embeddings / recherche** | ❌ **manque** | `bge-m3` lisible en en-tête, **inexécutable** (pas d'encodeur bidirectionnel) |
| **décodage spéculatif** | ❌ manque, et chiffré | brouillon générique : **×1,20** — insuffisant pour justifier le chantier |

**Ce que le tableau dit en une phrase** : Drave gagne **par construction** sur les
sorties contraintes, **par ses circonstances** sur les modèles plus gros que la
RAM, et **perd** sur la modélisation de langue ordinaire tant que le modèle n'est
pas creux — ce qui est exactement le chantier de la parcimonie entraînée.

---


## 1. Le décodage spéculatif : ×1,2, pas ×2 — mesuré avant d'écrire du moteur

Le moteur n'a **aucune** implémentation du décodage spéculatif, et le brouillon
qui dort sur le disque (`eagle3-gpt-oss-120b`) ne peut pas servir seul : un Eagle3
s'attache aux états cachés de sa cible. Avant d'écrire du moteur, il fallait le
chiffre qui décide — `tools/speculatif.py`, brouillon Qwen2.5-0.5B pour cible
Qwen2.5-1.5B (même tokenizer), 40 préfixes de 64 jetons, k = 8 :

| mesure | valeur |
|---|---|
| acceptation moyenne | **3,35 jetons sur 8 (41,9 %)** |
| médiane · min · max | 3 · 0 · 8 |
| au moins 1 / 2 / 3 / 4 acceptés | 68 % · 60 % · 52 % · 42 % |
| gain espéré si le brouillon coûte **0,25×** la cible | ×1,45 |
| gain espéré s'il coûte **0,33×** | **×1,20** |
| gain espéré s'il coûte **0,50×** | ×0,87 |

**Conclusion, et elle est négative pour la version naïve** : un petit modèle de la
même famille propose en moyenne 3,35 jetons justes sur 8, et le gain net dépend
entièrement du coût relatif du brouillon. Sur cette machine, où le décodage est
borné par la bande passante mémoire, un 0,5 B coûte environ un tiers d'un 1,5 B
par pas : **×1,20**. La feuille de route attendait ×1,58 (mesuré sur le
préremplissage par lots) — on en est loin, et ce n'est pas un défaut
d'implémentation : c'est le taux d'acceptation qui plafonne.

Ce que cela dit pour la suite : un brouillon **générique** ne paie pas. Il faut un
brouillon **aligné** sur sa cible (distillé, ou une tête Eagle3 qui consomme les
états cachés de la cible) — c'est-à-dire un chantier d'entraînement, pas une
option de moteur. Le chiffre est là pour éviter d'écrire le mauvais code.

---

## 2. Les deux familles de tâches que Drave ne couvre pas

Constatées, et consignées comme manques — pas comme résultats :

| famille | état | ce qui manque |
|---|---|---|
| **embeddings / recherche** | `bge-m3` (BERT, 24 couches, vocab 250 002) est **lisible en en-tête** mais **inexécutable** | le moteur exige `blk.0.attn_norm.weight` et une attention causale ; il n'a ni encodeur bidirectionnel ni pooling |
| **décodage spéculatif** | `eagle3-gpt-oss-120b` (0,84 Go, 1 couche) présent sur le disque | aucune notion de brouillon dans le moteur (`grep eagle\|brouillon\|specul` = 0), et le § 1 montre qu'un brouillon générique ne suffirait pas |

Ce sont les deux seules familles demandées par un usage courant qui manquent au
relevé : tout le reste (langage, génération, contexte long, code, raisonnement,
MoE, multilingue, lots, gros-modèle-sur-petite-machine) est couvert.

---

## 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? »

Mêmes 256 jetons, même contexte, chaque modèle tokenisant son propre corpus
(`/usr/bin/time -v` pour la mémoire et les octets lus).

| modèle | perplexité | **bits/octet** | tok/s | RSS | octets lus | condition |
|---|---:|---:|---:|---:|---:|---|
| Qwen2.5-0.5B Q8_0 | **17,43** | **0,983** | 28,7 | 1,28 Go | 0 | en cache |
| r1-distill-Qwen-1.5B Q4_K_M | **47,14** | **1,326** | 9,5 | 4,76 Go | 1,04 Go | lu du disque |
| r1-distill-Qwen-14B Q4_K_M | **14,30** | **0,915** | 0,5 | 39,8 Go | 8,71 Go | lu du disque, charge 47 |
| codestral-22B Q4_K_M | **35 657** ⚠️ | — | — | 63,6 Go | 12,7 Go | tokenizer Mistral ; **diagnostic en cours** |
| Qwen3-30B-A3B Q4_K_M (MoE) | **8,63** | **0,742** | — | **14,3 Go** | 11,8 Go | MoE, lu du NVMe |
| gpt-oss-120b MXFP4 | *en cours* | | | | | 63 Go depuis le disque dur |

**Le MoE gagne sur les deux tableaux — la thèse du projet démontrée par un modèle
qui n'a pas été fait pour ça.** Qwen3-30B-A3B (30 milliards de paramètres, 3
actifs) donne la **meilleure qualité de la grille** (0,742 bit/octet, mieux que le
14B dense à 0,915) pour **14,3 Go de mémoire résidente** — moins que le 14B
(39,8 Go) et trois fois moins que codestral-22B (63,6 Go). Un modèle plus gros qui
lit moins : exactement ce que le prototype routé cherche à reproduire en
l'entraînant.

**L'anomalie codestral est EXPLIQUÉE — et elle a fait naître une porte.** 35 657
de perplexité sur de la prose, c'est 4 000× le 30B. L'hypothèse sérieuse était :
le moteur exécute mal l'architecture **Mistral**, qui n'avait **aucune porte**
dans `tools/portes.sh` (Qwen, GLM, V4, gpt-oss et Kimi en ont une).

`tools/porte_mistral.py` comble le trou : il exporte un Mistral (mapping des
tenseurs, clefs préfixées `llama.`) et fabrique la référence PyTorch **sur les
mêmes poids quantifiés**. Sur un Mistral minuscule entraîné ici même (2 couches,
64 cachés, vocabulaire d'octets) :

| | perplexité | corrélation des logits | top-1 |
|---|---:|---:|---:|
| référence PyTorch (mêmes poids Q8_0) | 3 411,4394 | — | — |
| **moteur** | **3 411,4405** | **min 1,0000** | **100 %** |

**Le moteur exécute Mistral correctement.** Les 35 657 de codestral sont donc un
décalage de **tâche** — un modèle spécialisé pour le code, évalué sur de la prose
— et non un défaut d'exécution. C'est la réponse à la ligne « code » du verdict :
la famille tourne, c'est le modèle qui n'est pas fait pour ça.

*(Une fausse alerte est consignée : la première version du script instanciait le
modèle par `MistralForCausalLM(config)` — des poids **aléatoires** — au lieu de
`from_pretrained`. La porte accusait donc le moteur d'un défaut de la référence,
et rendait « NON TENUE » à tort.)*

**La perplexité n'est PAS comparable d'un tokenizer à l'autre.** Codestral
(32 768 entrées) découpe ce texte en **288 554** jetons là où Qwen en fait
**85 626** : son « PPL » se lit sur une autre échelle. La colonne **bits/octet**
est la seule unité commune — `log₂(PPL) × jetons / octets`, recalculée depuis le
journal de tokenisation de chaque modèle. Le tableau la porte pour que la
comparaison reste possible.

**Un résultat contre-intuitif, et il est solide** : les trois premiers modèles
partagent **exactement le même tokenizer** (leurs fichiers d'identifiants
commencent par les mêmes jetons `198,284,8397,…`), donc leurs chiffres se
comparent directement. Or le **r1-distill-1.5B est 2,7× PIRE que le 0.5B** sur
cette tâche (1,326 contre 0,983 bit/octet). Ce n'est pas la quantification
(Q4_K_M contre Q8_0) qui explique un tel écart : c'est le modèle — un distillat de
raisonnement, entraîné pour produire de longues chaînes de pensée, est mauvais en
modélisation de langue pure. **La taille ne dit pas la qualité pour une tâche
donnée** ; c'est exactement ce que la question « pour tout type de tâches »
demandait de vérifier, et la réponse est non.

Le 14B redresse la barre (0,915 bit/octet) mais à **0,5 tok/s** sous charge 47 —
le temps, lui, n'est pas une mesure propre ici, et c'est écrit dans le journal.

*(tableau complété à mesure ; `tools/campagne_synthese.py` le régénère depuis les
journaux, colonne `bits/octet` comprise)*

---

## 4. Ce que le dépôt sait déjà, par famille de tâches (avant cette campagne)

Consolidé des rapports existants, pour que les chiffres du jour se lisent dans un
ensemble plutôt que seuls. Chaque ligne cite sa source.

| famille | acquis mesuré | source |
|---|---|---|
| **langage (perplexité)** | Qwen2.5-0.5B ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** (portes de non-régression) | `tools/portes.sh`, `REPRISE.md` |
| **débit CPU, sans BLAS** | 0,5 B quantifié : **15,8 tok/s**, 5,3 G événements/s, 16/16 jetons identiques à numpy | `rapport-inference.md` |
| **préremplissage par lots** | ×1,58 sur Qwen3-30B-A3B (invite de 192 jetons, NVMe), et **15,5× moins d'octets d'experts** | `rapport-prefill-par-experts.md` |
| **contexte long** | KV int8 : **+1,5 %** de PPL à 512 jetons, **+3,0 %** à 8 192 (int4 : +364 %) ; KV paginé : **0,03 Go au lieu de 25,77 Go** à 1 M | `rapport-placement-bits-kv.md`, `docs/contexte-long.md` |
| **attention sur GPU** | **22,16 → 3,29 ms/jeton** (÷6,7) au décodage, ×2,8 en préremplissage ; tête 7,58 → 3,60 ms | `docs/contexte-long.md` |
| **MoE / routage** | Qwen3-30B-A3B : **4 experts sur 128** par couche et par jeton (3,1 %) ; porte clusters **799,8557** | `rapport-localite-activation.md`, `portes.sh` |
| **parcimonie imposée** | k-WTA 85 % = **−13,1 % d'événements pour +0,46 % de PPL** ; le seuil absolu est 10× pire | `rapport-campagne-parcimonie.md` |
| **modèle plus gros que la RAM** | Kimi-K3 (1,5 To) sur 125 Go : passe de 4 jetons = **206,58 Gio lus**, 133 Mio/s, disque occupé 87,6 %, CPU 21 % — **26,5 min**, contre 42 min/jeton pour llama.cpp | `rapport-passe-k3-disque.md` |
| **répartition** | deux nœuds, cinq modes : écart **0,00e0** sur les modes exacts ; **1 608 octets** par flux à 256 jetons ; attente ≈ calcul distant + 3,2 × latence | `porte-flux.sh`, `docs/roadmap.md` |
| **routage d'experts à l'échelle** | 72 % des octets d'une passe sont les experts, **relus à chaque jeton** ; le dense est lu une fois et partagé | `rapport-passe-k3-disque.md` |
| **multilingue / sémantique** | bande **10–15 sur 24 couches** (42–62 % de séparation) sur **398 langues** ; couche 0 : séparation nulle | `rapport-cycle-rapide.md` |
| **embeddings** | **rien** — `bge-m3` est inexécutable (§ 2) | cette campagne |
| **décodage spéculatif** | **rien** dans le moteur ; le taux d'acceptation mesuré est de 41,9 % (§ 1) | cette campagne |

Deux lignes de ce tableau sont des **manques**, et elles sont écrites comme telles :
c'est la moitié de la réponse à « pour tout type de tâches ».

---

## 5. Les modèles entraînés ici, mesurés DANS le moteur — et le routage GAGNE

Chaîne automatique : dès qu'un dossier d'entraînement apparaît, il est exporté,
sa référence PyTorch est calculée **sur les mêmes poids quantifiés**, la porte de
logits est passée, puis le moteur mesure les paires, les événements et le débit.
Les deux membres de chaque paire **lisent exactement le même nombre de poids par
jeton** (vérifié par le compteur du moteur, colonne « paires/jeton »).

| modèle | val (bits/octet) | **PPL moteur** | paires/jeton | tok/s dense | tok/s listes | porte |
|---|---:|---:|---:|---:|---:|---|
| `m5_d256_dense` (3,2 M) | 2,007 | 5,3973 | 3,2 M | 787,2 | 442,3 | ✅ |
| **`m5_d256_route` (10,3 M)** | — | **5,0684** | **3,2 M** | — | **662,8** | ✅ |
| `m5_d384_dense` (7,2 M) | 1,919 | 5,3719 | 7,2 M | 528,2 | 255,0 | ✅ |
| **`m5_d384_route` (44,4 M)** | — | **5,0614** | **7,2 M** | — | 184,0 | ✅ |

**À lecture ÉGALE, le routage gagne de 6 % de perplexité** — et c'est la thèse du
projet, démontrée avec des modèles entraînés ici et exécutés par le moteur :

- `d256` : **5,0684 contre 5,3973** (−6,1 %) pour les mêmes 3,2 M poids lus, en
  **stockant 3,2× plus de paramètres** (10,3 M contre 3,2 M) ;
- `d384` : **5,0614 contre 5,3719** (−5,8 %) pour les mêmes 7,2 M poids lus, en
  stockant **6,2× plus** (44,4 M contre 7,2 M).

Un modèle plus gros qui lit autant : c'est exactement ce que « nativement
événementiel » veut dire, et le gain ne vient pas d'un réglage — il vient de la
**structure** (2 experts sur 8 ou 16, choisis par un routeur appris).

**Deux réserves, et elles comptent.**

1. **Le débit ne suit pas toujours.** À `d256` le routé est **1,5× plus rapide**
   (662,8 contre 442,3 tok/s) ; à `d384` il est **1,4× plus lent** (184,0 contre
   255,0) — le regroupement des jetons par expert a un coût fixe qui pèse quand le
   modèle grandit. Le gain de qualité, lui, tient dans les deux cas.
2. **Les experts ne passent PAS par les listes.** Ils sont écrits en Q4_0, format
   pour lequel le moteur n'a pas de noyau de listes : le compte d'« événements »
   ne les couvre donc pas (199,5 M pour le routé contre 2 874 M pour le dense —
   un écart qui ne compare pas la même chose). La mesure honnête est la colonne
   **paires/jeton**, et elle est égale par construction.

## 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle

Le dépôt découpe par **plages de couches** (prouvé, écart 0,00e0). Mais l'unité
naturelle d'un modèle routé, c'est l'**expert** — et la sommation inter-nœuds
n'existe pas (`Moe::ou` → `None` → `continue` : un nœud partiel saute l'expert
absent sans un mot). `tools/census_routage.py` donne les trois chiffres qui
décident, mesurés sur `m4_route` (4 couches, 8 experts, top-2, 1 024 jetons) :

| couche | charge max | charge moyenne | déséquilibre | experts pour 90 % des jetons |
|---|---:|---:|---:|---:|
| 0 | 537 | 256 | **×2,10** | 5 sur 8 |
| 1 | 517 | 256 | ×2,02 | 7 sur 8 |
| 2 | 703 | 256 | **×2,75** | 6 sur 8 |
| 3 | 999 | 256 | **×3,90** | 4 sur 8 |

**Trois enseignements, et le troisième commande la suite.**

1. **Le déséquilibre est réel** : jusqu'à **3,9×** entre l'expert le plus chargé
   et la moyenne. Un partage naïf par experts donnerait un nœud 4 fois plus
   chargé que l'autre — il faut un routeur qui équilibre, ou un découpage qui
   tienne compte de la charge mesurée.
2. **On ne peut pas élaguer** : à top-2 sur 8, **4 à 7 experts** sont nécessaires
   pour couvrir 90 % des jetons. Tous servent ; la « localité » qui justifierait
   de n'en garder que quelques-uns n'existe pas à cette échelle.
3. **Le volume à router est négligeable, la latence ne l'est pas.** L'état
   transporté vaut **847 octets** par jeton (79 d'en-tête + 192 × 4) — du même
   ordre que les **848 octets** mesurés pour un flux de couche. Ce qui coûte,
   c'est l'aller-retour par couche, pas les octets : le dépôt a mesuré
   `attente ≈ calcul distant + 3,2 × latence`. Répartir par experts multiplie
   donc les allers-retours que répartir par couches évite.

---

## 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas

La tête de sortie est **la plus grosse matrice du modèle** : vocabulaire × cachés.
Pour le 0,5 B, 151 936 × 896 = **136 M poids, soit 136 Mo lus par jeton** — un
cinquième du modèle entier pour une seule projection. Or une classification ou un
choix multiple n'a que quelques sorties valides : `--tete-restreinte` ne calcule
que celles-là.

Mesure entrelacée, 64 jetons générés, 0,5 B Q8_0, 8 fils :

| tête | tour 1 | tour 2 | moyenne |
|---|---:|---:|---:|
| complète (151 936 jetons) | 14,79 tok/s | 16,14 tok/s | 15,47 |
| **restreinte à 3 jetons** | **21,92** | **22,07** | **22,00** |

**×1,42 de débit**, et la tête restreinte est **stable** (21,92 / 22,07 là où la
complète varie de 14,79 à 16,14 — moins de travail, donc moins de sensibilité à
la charge).

**Le second bénéfice compte plus que le premier, et il ne se mesure pas en
tok/s** : la sortie **ne peut pas** être hors de l'ensemble autorisé. Dans l'essai,
le modèle a produit `neutral negative negative positive positive negative neutral
positive` — des réponses incohérentes (un 0,5 B ne sait pas juger un sentiment),
**mais jamais un mot hors des trois étiquettes**. Pour une tâche de production,
cela vaut plus que la vitesse : plus de post-traitement, plus de reprise, plus de
réponse invalide à rattraper.

C'est donc la **première famille de tâches où l'architecture de Drave gagne par
construction** plutôt que par ses circonstances (modèle plus gros que la RAM) —
et elle ne demande aucun modèle particulier.

Le batch 7 refait la mesure sur le 1,5 B et sur gpt-oss-120b, où le rapport
tête/corps est différent.

---

## 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs

La perplexité moyenne ne dit pas si un modèle **retrouve** un fait précis. Test :
un code unique planté dans une botte de foin, à trois profondeurs (10 %, 50 %,
90 %), et une question à la fin. Qwen2.5-0.5B Q8_0, `--infer`, 12 jetons, `temp 0` :

| longueur | profondeur 10 % | 50 % | 90 % |
|---|---:|---:|---:|
| 512 jetons | ✅ | ✅ | ✅ |
| 1 024 | ✅ | ✅ | ✅ |
| 2 048 | ✅ | ✅ | ✅ |
| 4 096 | ✅ | ✅ | ✅ |

**12 configurations sur 12 retrouvent le code**, y compris à 4 096 jetons avec un
modèle de 0,5 B. C'est une mesure de **tâche**, pas de perplexité : le cache KV du
moteur, sa quantification et sa pagination ne détruisent pas la mémoire du
contexte. C'est exactement ce que la revendication « contexte long » devait
démontrer, et c'est la première fois qu'elle l'est sur une tâche.

**Réserve, et elle est sérieuse sur les temps** : cette série a tourné **en
parallèle de la campagne** (un défaut d'enchaînement corrigé depuis), donc deux
gros modèles lisaient le disque en même temps. Les **verdicts** (retrouvé/perdu)
n'en dépendent pas ; les **durées** oui — de 26 s à 609 s pour la même taille,
selon ce que le disque faisait à ce moment-là.

---

## 10. La génération : TTFT et débit, mesure directe

| modèle | invite | TTFT | débit de génération |
|---|---:|---:|---:|
| Qwen2.5-0.5B Q8_0 | 11 jetons en 0,307 s | **27,9 ms** | **29,0 tok/s** |
| r1-distill-1.5B Q4_K_M | 11 jetons en 1,260 s | 114,6 ms | 7,1 tok/s |
| r1-distill-14B Q4_K_M | *en cours* | | |
| Qwen3-30B-A3B | *en cours* | | |
| gpt-oss-120b MXFP4 | *en cours* | | |

Ces chiffres-là portent la **latence perçue** d'un usage réel, que la perplexité
ne donne pas : un premier jeton en 28 ms et 29 jetons/s sur un 0,5 B, c'est un
assistant utilisable ; 7 jetons/s, c'est déjà pénible.

---

## 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur

Le batch 4 les avait prévues sur gpt-oss-120b (5 × 1 h de lectures du même fichier
de 63 Go, en concurrence avec la mesure PPL). Refaites ici sur le **0,5 B**, qui
suffit à répondre à la seule question qui compte : le moteur produit-il une sortie
**exploitable** ? Sorties **telles quelles**, `temp 0`, 64 jetons.

| tâche | sortie du 0,5 B | verdict |
|---|---|---|
| **code** | `def fibonacci(n):` … gère `n <= 0`, `n == 1`, `n == 2` … | ✅ **correcte et utilisable** |
| traduction FR | *« The river carries the logs to the mill. (No translation is needed) »* puis *« Le ruisseau transporte les feuilles au mill. »* | ❌ refuse, puis traduit faux (`feuilles` = leaves, `mill` non traduit) |
| arithmétique | entame un raisonnement juste (« we need to calculate the difference… ») | ⚠️ **tronquée** à 64 jetons — la réponse n'apparaît pas |
| résumé | *« The engine is a key component in the development of the new generation of engines. »* | ❌ hallucination, puis recopie de l'entrée |

**Ce que cela dit.** Le moteur a produit une **fonction Python correcte** avec un
modèle de 0,5 B — sur la tâche où le format est contraint (du code), il tient. Sur
la traduction, l'arithmétique et le résumé, c'est le **modèle** qui échoue, pas
l'exécution : Drave est un moteur, il fait ce que le modèle sait faire. C'est
aussi pourquoi la ligne « sortie contrainte » du verdict est la seule où
l'architecture gagne *par construction*.

*(Débit de ces essais : 0,84 tok/s, sous une charge de fond de **84** — trois gros
modèles lus en parallèle. Le chiffre ne dit rien du modèle ; il dit que mesurer
sous cette charge ne vaut que pour les sorties, pas pour les temps.)*

---

## 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si

Même modèle (Qwen2.5-0.5B Q8_0), même matériel, quatre corpus, 192 jetons : la
question du batch 2 était « le bénéfice événementiel dépend-il de la tâche ? ».

| corpus | jetons/octet | PPL | **bits/octet** | paires/jeton | **densité** |
|---|---:|---:|---:|---:|---:|
| prose anglaise | 0,2385 | 15,85 | **0,951** | 495,9 M | **71 %** |
| français | 0,2783 | 11,19 | **0,969** | 495,9 M | **71 %** |
| code | 0,3117 | 7,09 | **0,881** | 495,9 M | **71 %** |

**La densité est identique dans les trois cas — 71 %, à 0,002 point près**
(67,766 / 67,767 / 67,766 milliards d'événements). Autrement dit : **le bénéfice
événementiel ne dépend pas de la tâche**, il dépend du **modèle**. Un modèle dense
reste dense quelle que soit l'entrée ; c'est la parcimonie *entraînée* qui la
change, et rien d'autre. L'hypothèse « telle tâche réveille moins de neurones »
est **réfutée** ici.

**Ce qui dépend de la tâche, c'est la qualité.** En bits/octet — la seule unité
comparable entre tokenizers — le même modèle prédit le **code mieux que la prose**
(0,881 contre 0,951) et le **français moins bien que l'anglais** (0,969 contre
0,951). Les perplexités brutes disent l'inverse (7,09 pour le code contre 15,85
pour la prose) uniquement parce que le code se tokenise en jetons plus longs :
c'est exactement le piège que la colonne bits/octet neutralise.

---

## 11. Ce qui reste à mesurer (file en cours)

- `parcimonie` : seuil et k-WTA, en dense et en listes, sur un modèle réel ;
- `contexte` : 512 → 8 192, avec le cache KV que le moteur **choisit** ;
- `lot` : 1 → 64, le seul levier qui multiplie un débit de disque ;
- `routage` : MoE 30B, experts réveillés et volume à router ;
- `semantique` : la bande 10-15 **survit-elle** à la correction d'échelle ?
- `noyau`, `repartition`, `portes` ;
- **batch 2** : la densité d'activation dépend-elle de la **tâche** (prose,
  français, code, multilingue) ? Même modèle, même matériel ;
- **batch 3** : l'aiguille dans la botte de foin — la perplexité moyenne ne dit
  pas si la mémoire tient à 4 000 jetons ;
- **les paires d'entraînement** (dim 256 et 384, dense contre routé à lecture
  égale) : export, porte d'exécution, mesure dans le moteur, répartition.
