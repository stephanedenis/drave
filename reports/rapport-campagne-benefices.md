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

## 1. Le décodage spéculatif : ×1,2, pas ×2 — et c'est mesuré avant d'écrire du moteur

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
| codestral-22B Q4_K_M | *en cours* | | | | | tokenizer Mistral (32 768) |
| Qwen3-30B-A3B Q4_K_M (MoE) | *en cours* | | | | | |
| gpt-oss-120b MXFP4 | *en cours* | | | | | 63 Go depuis le disque dur |

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

## 5. Ce qui reste à mesurer (file en cours)

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
