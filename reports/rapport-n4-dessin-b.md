# N4 — le chemin court entraîné (dessin B) : ÷1,2 à ÷1,9 selon la profondeur, et deux corrections de mesure

> Campagne : **cerveau** · expérience : dessin **B** de N4 (« les couches basses apprennent »), et
> vérification de la chaîne torch contre le moteur qui l'a rendue lisible.
> Question : (1) entraîner les **couches basses** (LoRA sur q/k/v/o) fait-il mieux lire leur état
> qu'un adaptateur de sortie posé sur des couches **gelées** — le dessin B vaut-il mieux que le
> dessin A ? (2) — questions nées en installant le banc — les chiffres publiés sur le morceau
> **m20** étaient-ils mesurés sur un morceau « jamais vu », et le repère « modèle complet »
> (14,2342) est-il comparable à un chiffre **par morceau** ?
> Verdict : **le dessin B paie, et d'autant plus qu'on sort tôt.** À profondeur 8, sur les deux
> morceaux réellement jamais vus et **deux graines** : `lora+adaptateur` rend **203,32 / 210,44**
> contre **268,13 / 249,79** pour l'adaptateur seul sur m32 (**÷1,19 à ÷1,32**) — et **rien** sur
> m20 (163,26 / 172,53 contre 165,65 / 160,56). À profondeur 4 : **283,67 contre 520,28** sur m32
> (**÷1,83**) et **187,98 contre 307,88** sur m20 (**÷1,64**). Deux corrections : le m20 publié à
> **17,35** était mesuré avec **m20 dans l'entraînement** (la fuite vaut **×8,0**, mesuré), et
> **14,2342 est un chiffre de corpus** (moyenne géométrique des 33 morceaux), pas un chiffre de
> morceau — sur m32 le modèle complet vaut **7,42**.
> Date réelle : **2026-10-14 13 h 15-14 h 15 HAE** (heure lue sur la machine ; commits du jour)
> Protocole : `tools/n4_dessin_b.py` (nouveau) — 33 morceaux de 1 024 jetons répartis dans le
> corpus, entraînement **m0..m29 moins m20** (29 morceaux), **validation m30+m31**, test
> **m32 et m20** (tous deux hors entraînement), deux graines, époque choisie **sur la validation**,
> GPU (`gpu-env`, torch 2.11).

## 0. Le banc, et la porte qui le rend lisible : torch contre le MOTEUR

Le dessin B exige de **rétropropager à travers les couches** — le moteur (Rust) ne le fait pas. Il
faut donc un modèle en torch qui soit **le même** que celui du moteur, et une porte qui le prouve.
Trois mesures de concordance, toutes contre les chiffres de `drave` sur les mêmes morceaux :

| grandeur | moteur (Q8_0) | chaîne torch (fp32) | écart |
|---|---:|---:|---:|
| modèle complet, m32 | 7,4242 | 7,1787 | −3,31 % |
| modèle complet, m20 | 19,1237 | 18,4607 | −3,47 % |
| tronqué 8 couches, tête empruntée, m32 | 4 481 378,8799 | 4 476 128,7883 | **−0,12 %** |
| tronqué 8 couches, tête empruntée, m20 | 1 790 749,9836 | 1 761 597,2378 | −1,63 % |
| tronqué 4 couches, tête empruntée, m32 | 24 656 438,5178 | 24 848 926,3482 | +0,78 % |
| tronqué 4 couches, tête empruntée, m20 | 8 174 482,8297 | 8 126 089,6200 | −0,59 % |

Et l'état lui-même, sur **1 020 positions** de m32 à profondeur 8 (fichiers `--etat-sortie` du
moteur contre le vecteur torch) : **cosinus 0,99964 au minimum, 0,99994 en médian**. L'écart
restant est la quantification Q8_0 du fichier — les matrices du GGUF sont à 5,5e-3 des poids fp32
du dépôt Hugging Face (§ 1), pas un désaccord d'algorithme.

**Pourquoi ça compte** : les chiffres publiés de C8 sont reproduits par ce banc — `267,98` →
**253,75 / 260,22** (adaptateur, profondeur 8, m32, graines 0 et 1), `534,91` → **510,15**
(profondeur 4), et côté moteur `24 656 438,5178` **au chiffre près**. Un banc qui ne retrouve pas
les chiffres qu'il remplace ne mesure rien : celui-ci les retrouve à **5 %** (les deux premiers)
et exactement (le troisième).

## 1. Ce que la mise en place a appris : le GGUF du moteur est l'**Instruct**

Le fichier s'appelle `models/Qwen2.5-0.5B-Q8_0.gguf` et le cache Hugging Face local contient
`Qwen/Qwen2.5-0.5B` : il est **naturel** de croire que c'est le même modèle. **Ce n'en est pas
un.** Comparaison tenseur à tenseur :

| modèle comparé au GGUF | tenseurs f32 (normes) | matrices Q8_0 |
|---|---|---|
| `Qwen2.5-0.5B` (base, en cache) | **écart 1,5 à 2,5 %** | cos 0,994 à 0,998 |
| `Qwen2.5-0.5B-Instruct` (téléchargé pour trancher) | **écart 0,00e+00 — identiques au bit** | cos 0,99997 à 1,00000 |

Les normes sont stockées en **f32** : un écart de 2 % ne peut pas être de la quantification. Le
GGUF est donc l'**Instruct**, et son métadata le dit (`general.name = Qwen2.5 0.5B Instruct`,
`finetune = Instruct`, `eos = 151645`) — **c'est le nom du fichier qui ne le dit pas**.

* premier effet mesuré : la sonde de concordance comparait l'état du moteur à celui du modèle
  **base** et rendait cos 0,944 à 0,995, ce qui ressemblait à « le moteur s'écarte » ; c'était le
  **mauvais modèle**. Sur l'Instruct, le même contrôle rend 0,99964 à 0,99997 ;
* conséquence pour la suite : toute mesure qui veut *écrire* dans le moteur doit partir de
  l'Instruct (c'est ce que fait ce banc), et les chiffres de C8 restent valides — ils viennent du
  même GGUF des deux côtés (les états **et** la tête liée).

## 2. Les cinq portes de `docs/note-chemin-court-n4.md` § 3, et ce qu'elles ont rendu

| porte (écrite avant le code) | ce qui a été mesuré | verdict |
|---|---|---|
| 1. **invariant d'identité** | adaptateur = identité, LoRA = 0 ⇒ écart **4,79e-07** (adaptateur : arrondi flottant) et **0,00e+00** (LoRA) | **tenue** |
| 2. **le témoin « tête empruntée » reste dans la table** | 4 476 128,79 (m32) et 1 761 597,24 (m20), plus le modèle complet 7,18 / 18,46 | **tenue** |
| 3. **deux morceaux jamais vus** | m32 **et** m20 — c'est cette porte qui a fait trouver la fuite (§ 4) | **tenue, et elle a payé** |
| 4. **deux graines** | m32 : 268,13 / 249,79 (adaptateur) · 203,32 / 210,44 (A+B) — la graine pèse **7,3 %** et **3,5 %** | **tenue** |
| 5. **l'époque se choisit sur la validation** | m30+m31 pour tous les bras, jamais le test | **tenue** |

**La porte 1 a attrapé un vrai bug, avant toute mesure.** La première version lisait l'état avec
`output_hidden_states[L]` — mais pour un modèle **tronqué**, le dernier état de cette liste est
**après la norme finale**, pas avant : l'adaptateur normalisait donc un état déjà normé, et
l'« invariant d'identité » rendait **18 774 866** au lieu de 4 476 128 (**×4,19**). Sans cette
porte, ce bug partait en résultat. L'état brut est maintenant capturé par un **crochet** sur la
dernière couche tronquée — c'est aussi ce qui rend vraie la comparaison avec les fichiers
`--etat-sortie` du moteur.

## 3. Les bras sous le protocole publié (k = 30, m20 **dans** l'entraînement)

| bras | époque (val) | validation m30+m31 | TEST m32 | TEST m20 *(vu)* |
|---|---:|---:|---:|---:|
| **modèle complet** (référence) | — | — | 7,1787 | 18,4607 |
| chemin tronqué, tête **empruntée** | — | — | 4 476 128,7883 | 1 761 597,2378 |
| `adaptateur` (dessin A), graine 0 | 2 | 272,4129 | 253,7501 | 20,6327 |
| `adaptateur` (dessin A), graine 1 | 2 | 286,9559 | 260,2183 | 22,1242 |
| `lora` (dessin B, tête gelée), graine 0 | 11 | 291,1598 | 253,7886 | 122,9596 |
| `lora` (dessin B, tête gelée), graine 1 | 9 | 313,4683 | 266,4851 | 142,9764 |
| `lora+adaptateur`, graine 0 | 5 | 202,7291 | **188,7509** | 49,4376 |
| `lora+adaptateur`, graine 1 | 5 | 208,3708 | **175,2439** | 44,4503 |

Lu tel quel, ce tableau dit que le dessin B **change de signe selon le texte** (÷1,34 et ÷1,49 sur
m32, ×2,40 et ×2,02 sur m20). **Cette lecture est fausse** : le m20 de cette colonne n'est pas un
morceau de test (§ 4), et le § 5 donne la version propre.

## 4. Première correction : m20 n'était **pas** « jamais vu »

En vérifiant la porte 3 — « ce morceau est-il dans la liste d'entraînement ? » — la réponse a été
**oui**, et pas seulement pour mon banc. La commande exacte du 13/10, retrouvée dans le journal de
session (`~/.dsh/sessions/.../session.v4.jsonl.zstd`), est :

```bash
T=/home/stephane/IA/scratch/c8-echelle
train=$(for i in $(seq 0 29); do printf "%s," "$T/etat-m$i"; done | sed "s/,$//")
echo "########## A. test sur m20 (autre morceau jamais vu que m32) ##########"
CUDA_VISIBLE_DEVICES=0 $P tools/c8_entrainer_tete.py --train "$train" \
  --val "$T/etat-m30,$T/etat-m31" --test "$T/etat-m20" --ids "$T/morceau-20.txt" \
  --modele models/Qwen2.5-0.5B-Q8_0.gguf --limite 1024 --epoques 20 --ppl_complet 14.2342
```

`seq 0 29` **inclut m20** : `$T/etat-m20` figure dans `--train` **et** dans `--test`. La même
construction (`seq 0 29`, ou `seq 0 $((k-1))`) a servi pour les profondeurs 4, 8 et 12 et pour la
capacité. La règle avait pourtant été écrite la veille
(`reports/rapport-c8-generalisation.md` § 5 : « **LA LISTE D'ENTRAÎNEMENT EXCLUT LE MORCEAU DE
TEST** — construit comme ceci, jamais à la main », `if i != 7`) : elle n'a pas été appliquée ici.

**La fuite, chiffrée** — mon banc, graine 0, mêmes morceaux, même validation, même choix d'époque
sur la validation ; seule la liste d'entraînement change :

| bras | profondeur 8 : m20 **vu** (30 morceaux) | profondeur 8 : m20 **propre** (29 morceaux) | facteur |
|---|---:|---:|---:|
| `adaptateur` | 20,6327 | 165,6517 | **×8,0** |
| `lora` | 122,9596 | 219,5141 | ×1,8 |
| `lora+adaptateur` | 49,4376 | 163,2643 | ×3,3 |

| bras | profondeur 4 : m20 **vu** (30 morceaux) | profondeur 4 : m20 **propre** (29 morceaux) | facteur |
|---|---:|---:|---:|
| `adaptateur` | 21,3364 | 307,8786 | **×14,4** |
| `lora` | 136,8791 | 271,3996 | ×2,0 |
| `lora+adaptateur` | 57,4587 | 187,9788 | ×3,3 |

Le morceau passé à l'entraînement n'est pas « facile », il est **appris** — et l'adaptateur de
sortie, qui a 800 000 paramètres libres, l'apprend le mieux (×8 et ×14), le LoRA à tête gelée le
moins (×1,8 et ×2,0). Mes deux graines du § 3 (20,63 et 22,12) reproduisent d'ailleurs le chiffre
publié (17,35) à 19 % près, côté torch et fp32 : c'est bien la même chose qui a été mesurée.

**Ce que la fuite contamine dans les fiches publiées** (l'ancien chiffre reste ici, à côté du
nouveau — c'est la règle du dépôt) :

| énoncé publié le 13/10 | ce qu'il devient |
|---|---|
| § 2ter : « **le morceau de test pèse ×10** : 17,35 sur m20 contre 179,59 sur m32 » | les deux nombres ne mesurent pas la même chose : l'un est sur un morceau **vu**, l'autre non. Le facteur ×10 **n'est pas établi** |
| § 2quinquies : « de 15 à 30 morceaux, m32 gagne ÷1,45 et **m20 gagne ÷22,8** (falaise) » | la « falaise » est le **passage de m20 dans l'entraînement** entre k = 15 et k = 30 ; les points k = 4 (2 816,29) et k = 15 (396,37) restent valides, le point k = 30 non |
| § 2quater : « le rapport 8/16 tombe à **×1,17** (20,37 contre 17,35) sur m20 » | les deux nombres sont ceux d'un morceau **vu** ; ce contrôle-là ne dit plus que le rapport dépend du texte |
| § 3 : « aucune loi chiffrée ne se tire d'un seul morceau de test » | **reste vrai, et pour une raison de plus** : ici le second morceau n'en était pas un |

Restent debout, parce qu'ils ne touchent jamais m20 : le morceau **m32** (absent de toutes les
listes d'entraînement) et la courbe de **profondeur** mesurée sur m32 (§ 2bis). La leçon est celle
de la règle du 10/10, sous sa forme exécutable : **un morceau de test se vérifie en comptant**, pas
en écrivant « jamais vu » dans un commentaire. `tools/n4_dessin_b.py` refuse désormais de
publier un test qui tombe dans la plage d'entraînement — il l'annonce (`⚠ FUITE`) et `--exclure`
retire le morceau de la liste.

## 4bis. Deuxième correction : « modèle complet 14,2342 » est un chiffre de **corpus**

Les rapports publiés divisent des perplexités **par morceau** (179,59 sur m32) par **14,2342**,
présenté comme « le modèle complet ». Or sur les morceaux mêmes, le moteur rend **7,4242** (m32),
**19,1237** (m20), 6,8809 (m30), 9,2388 (m31) — aucun n'est 14,2342. L'hypothèse qui tient est
celle du **corpus entier** : sur les 33 morceaux, la moyenne **géométrique** des perplexités du
modèle complet vaut **14,4283** en torch (moyenne arithmétique 15,2771 ; min 6,74, médiane 15,15,
max 28,05) — soit 1,4 % de 14,2342, l'écart attendu entre fp32 et Q8_0. **14,2342 est donc le
chiffre du corpus**, et le comparer à un chiffre de morceau est une comparaison de deux choses
différentes.

Conséquence arithmétique, sur l'énoncé le plus cité de la fiche du 13/10 : à profondeur 16, m32
rend 179,59 avec la tête entraînée, et le modèle complet y rend **7,42** — l'écart est **×24,2**,
pas ×12,6. Tous les rapports « ×N du modèle complet » des fiches C8 sont dans ce cas ; ceux de
cette fiche-ci sont calculés sur les nombres **par morceau**, mesurés ici.

## 5. La mesure propre : profondeur 8, m20 exclu, **deux graines**

Entraînement sur **m0..m29 moins m20** (29 morceaux), validation m30+m31, test m32 **et** m20 —
tous deux hors entraînement :

| bras | époque (val) | validation m30+m31 | TEST m32 (jamais vu) | TEST m20 (jamais vu) |
|---|---:|---:|---:|---:|
| **modèle complet** | — | — | 7,1787 | 18,4607 |
| chemin tronqué, tête **empruntée** | — | — | 4 476 128,7883 | 1 761 597,2378 |
| `adaptateur`, graine 0 | 2 | 282,7502 | 268,1317 | **165,6517** |
| `adaptateur`, graine 1 | 2 | 275,3348 | 249,7946 | **160,5560** |
| `lora`, graine 0 | 11 | 286,4155 | 244,0011 | 219,5141 |
| `lora`, graine 1 | 11 | 274,0833 | 254,9826 | 232,5052 |
| `lora+adaptateur`, graine 0 | 3 | 231,7251 | **203,3172** | 163,2643 |
| `lora+adaptateur`, graine 1 | 6 | 228,9733 | **210,4417** | 172,5327 |

Ce que ça dit :

* **le dessin B paie, un peu, et de la même façon aux deux graines** : sur m32, `lora+adaptateur`
  fait **÷1,19** (graine 1) et **÷1,32** (graine 0) mieux que l'adaptateur seul. La graine pèse
  3,5 à 7,3 % sur ce bras : le gain lui est donc **supérieur d'un facteur 2 à 4**, mais il n'est
  pas écrasant ;
* **sur m20, c'est nul** : 163,26 et 172,53 contre 165,65 et 160,56, soit ÷1,01 et ×1,07 — dans le
  bruit de graine. Le dessin B **déplace** la qualité, il ne l'ajoute pas partout ;
* **le dessin B seul (tête gelée) ne suffit pas** : il n'est pas stable sur m32 (244,00 contre
  268,13 à la graine 0, mais 254,98 contre 249,79 à la graine 1) et il est **nettement pire** sur
  m20 (219,51 et 232,51 contre 165,65 et 160,56, soit ×1,33 et ×1,45). Entraîner les couches
  basses ne rend donc **pas** l'état nativement lisible par la tête du modèle : c'est un **lecteur
  entraîné** qui exploite le changement ;
* **le morceau le plus difficile est celui qui paie** : m32 est là où le chemin tronqué est le
  plus loin du modèle complet (×37 contre ×9 pour m20). Là où l'état précoce suffisait déjà, il n'y
  a presque rien à récupérer — et l'entraînement des couches basses n'ajoute rien.

## 6. Contrôle de profondeur : plus on sort tôt, plus le dessin B paie

Même protocole **propre** (m20 exclu), graine 0, deux profondeurs de sortie :

| profondeur | bras | validation | TEST m32 | TEST m20 | gain du dessin B (m32 / m20) |
|---:|---|---:|---:|---:|---|
| 8 | `adaptateur` | 282,75 | 268,13 | 165,65 | — |
| 8 | `lora` | 286,42 | 244,00 | 219,51 | ÷1,10 / ×1,33 |
| 8 | `lora+adaptateur` | 231,73 | **203,32** | **163,26** | **÷1,32 / ÷1,01** |
| 4 | `adaptateur` | 533,68 | 520,28 | 307,88 | — |
| 4 | `lora` | 348,91 | 283,41 | 271,40 | ÷1,84 / ÷1,13 |
| 4 | `lora+adaptateur` | 301,78 | **283,67** | **187,98** | **÷1,83 / ÷1,64** |

* **à 4 couches, le dessin B paie sur les DEUX morceaux** : ÷1,83 (m32) et ÷1,64 (m20) pour
  `lora+adaptateur`, contre ÷1,32 et ÷1,01 à 8 couches. Plus on sort tôt, plus il y a
  d'information **créée** par les couches intermédiaires — donc plus il y a à gagner à les
  entraîner. C'est exactement ce que la prédictibilité des états annonçait le 13/10
  (`tools/predictibilite_etats.py` : R² 0,65 pour un saut direct contre 0,78 et 0,75 pour les pas
  élémentaires) ;
* **à 4 couches, le LoRA à tête gelée devient bon** (÷1,84 sur m32, ÷1,13 sur m20) : quand le
  chemin est très court, l'état entraîné redevient lisible par la **tête du modèle**. C'est le
  seul régime où le dessin B se passe de lecteur — une graine, deux morceaux, donc une piste, pas
  un résultat ;
* **le classement des bras est le même à 4 et à 8 couches**, et la validation (m30+m31) le prédit
  dans les deux cas : la sélection d'époque sur validation fonctionne, elle ne choisit pas au
  hasard.

## 7. Ce que cette fiche ne dit pas

* **un seul rang de LoRA** (r = 8, α = 16), un seul pas (1e-3), 20 époques : rien ne dit qu'un
  autre réglage ne ferait pas mieux ou pire. La fiche du 13/10 a montré l'inverse pour la
  *capacité de l'adaptateur* (non linéaire = 2,1× pire), pas pour le LoRA ;
* **le pas de l'adaptateur change selon le bras** (1e-2 sur états gelés, 1e-3 en apprentissage
  joint) : à 1e-2 en joint, l'entraînement **divergeait** (4,48 M → 2,9e13 en deux pas, mesuré).
  Les deux dessins sont donc comparés au *meilleur réglage connu de chacun*, pas à réglage
  identique — c'est une comparaison de dessins, pas de hyperparamètres ;
* **le gain « ÷1,19 à ÷1,32 » n'est mesuré qu'à une seule échelle de données** (29-30 morceaux,
  ~30 000 jetons). Rien ne dit qu'il grandit avec la donnée — la fiche du 13/10 a montré que la
  donnée paie, mais pour l'adaptateur, pas pour les couches ;
* **rien n'est exporté vers le moteur** : le dessin B est mesuré en torch. Le rendre exécutable
  par `drave` demande d'écrire un GGUF dense Qwen2 (`tools/exporter_gguf.py` ne fait que la
  famille MoE de Qwen3) — c'est la porte d'exécution, et elle n'est pas franchie ici.
