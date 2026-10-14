# N4 — la porte d'exécution : le chemin court entraîné est mesuré par le MOTEUR (÷1,47 et ÷1,24)

> Campagne : **cerveau** · expérience : rendre le dessin B **exécutable** par `drave` — écriture
> d'un GGUF dense (Qwen2), pose du lecteur appris sur un chemin tronqué, et mesure par le moteur.
> Question : les chiffres du dessin B, mesurés en torch le 14/10 (`reports/rapport-n4-dessin-b.md`),
> sont-ils ceux du **moteur** ? Un chiffre que le moteur ne reproduit pas n'est pas encore un
> chiffre du dépôt.
> Verdict : **oui, à 2 % près, et le verdict du moteur est plus net que celui de torch.**
> À profondeur 8, sur les deux morceaux de test jamais vus : l'adaptateur seul rend **272,45**
> (m32) et **168,85** (m20) ; le même adaptateur sur un modèle dont les **8 premières couches ont
> été entraînées** rend **185,67** et **136,33** — soit **÷1,47** et **÷1,24**, mesurés par
> `drave` sur un fichier écrit ici. Sur trois entraînements à graine fixée, le rapport vaut
> ÷1,32 · ÷1,46 · ÷1,43 (m32) et ÷1,01 · ÷1,25 · ÷1,22 (m20) : **le signe est stable, la taille
> varie de ±10 %** (§ 4 — la graine ne suffit pas dès qu'on rétropropage à travers les couches).
> La tête **empruntée** du modèle réécrit rend 4 480 788,40 (référence : 4 481 378,88), donc la
> réécriture ne déplace rien.
> Date réelle : **2026-10-14 14 h 10-15 h 00 HAE** (heure lue sur la machine)
> Protocole : `tools/exporter_gguf_dense.py` (nouveau, dense Qwen2 : biais q/k/v, tête liée) ·
> `drave --couches 0:8 --tete-partielle --adaptateur-sortie <fichier>` (nouveau drapeau) ·
> poids appris par `tools/n4_dessin_b.py` (protocole propre, m20 exclu, graine 0) ·
> morceaux m32 et m20 du corpus de 33 × 1 024 jetons.

## 1. Ce qu'il fallait écrire, et ce que le premier essai a appris

| pièce | pourquoi elle est nécessaire | ce qui a été mesuré |
|---|---|---|
| **un GGUF dense Qwen2** | `tools/exporter_gguf.py` ne connaît que la famille **MoE** de Qwen3 ; Qwen2.5-0.5B est dense, avec **biais** q/k/v et tête **liée** | 290 tenseurs écrits, relus **exactement** (écart 0,00e+00) |
| **le format d'échange** | le moteur lit les projections denses par `q8_view` | un export **F32** (1,98 Go, écrit et relu sans erreur) fait **paniquer** le moteur : `q8_view : type 0 non géré`. Q8_0 est donc le format d'échange ; les normes et les biais restent en f32 (`row_f32` lit les deux) |
| **les métadonnées** | un tokenizer réécrit à la main dérive en silence — et un tokenizer différent ne se voit pas | les 38 paires KV sont copiées **verbatim** du GGUF de référence (tokenizer de 151 936 jetons, 151 323 fusions, template de chat, RoPE) ; seul `general.file_type` est réécrit quand le format change, et `general.quantization_version` **jamais** (elle décrit le schéma, pas le type) |
| **un drapeau pour le lecteur appris** | la chaîne mesurée est `logits = tête · rmsnorm(A · état_brut)` : la matrice `A` n'existe dans aucun fichier du moteur | `--adaptateur-sortie F` : matrice `h × h` f32 brute, appliquée à l'état brut avant la norme finale d'une plage, sur les **quatre** fins de plage du moteur (`forward`, `forward_lot`, `forward_mla`, `norme_finale` du chemin réparti) |

**La fidélité de l'écriture est vérifiée sur place**, pas par un raisonnement : le modèle de
référence est réécrit à l'identique (déquantifié puis requantifié Q8_0) et le moteur doit rendre
les **mêmes** chiffres — c'est fait, au chiffre près :

| chemin | original | réécrit |
|---|---:|---:|
| modèle complet (m32, 1 024 jetons) | 7,4242 | **7,4242** |
| tronqué 8 couches, tête empruntée | 4 481 378,8799 | **4 481 378,8799** |

## 2. Le drapeau fait-il quelque chose ? (la question du dépôt)

Un drapeau inerte est le défaut le plus coûteux de ce dépôt, et l'invariant d'identité **ne suffit
pas** à l'exclure : une échelle globale est absorbée par la norme finale. Quatre contrôles, tous
dans `tools/porte-adaptateur-sortie.sh` (40ᵉ porte) :

| contrôle | attendu | mesuré |
|---|---|---|
| adaptateur = identité | chiffre **exactement** identique | 4 481 378,8799 → **4 481 378,8799** |
| adaptateur = demi-échelle (pas une échelle globale) | le chiffre **doit changer** | 4 481 378,88 → **13 314 758,17** |
| `--adaptateur-sortie` **sans** `--tete-partielle` | refus, code **2** | code **2** |
| matrice de mauvaise taille, ou fichier absent | refus, code **2** | code **2** (65536 octets pour 896×896) |

## 3. Les bras, mesurés par le MOTEUR

Même entraînement que la fiche du 14/10 (protocole propre : m20 **exclu** de l'entraînement,
29 morceaux, validation m30+m31, graine 0), mais lu par `drave` sur les fichiers exportés :

| bras | m32 (jamais vu) | m20 (jamais vu) | époque (validation) |
|---|---:|---:|---:|
| tête **empruntée** (modèle réécrit, sans adaptateur) | 4 480 788,4025 | 1 789 541,8768 | — |
| `adaptateur` (dessin A : couches gelées) | 272,4482 | 168,8502 | 2 |
| `lora` seul (tête gelée) | 262,7173 | 225,6785 | 11 |
| **`lora+adaptateur`** (dessin B) | **185,6664** | **136,3294** | 4 |

**Et le moteur retrouve torch à ~2 %** — c'est la quantification Q8_0, pas un désaccord (le
modèle complet montre le même écart de +3 %) :

| bras | torch (fp32) m32 / m20 | moteur (Q8_0) m32 / m20 | écart |
|---|---:|---:|---:|
| `adaptateur` | 268,13 / 165,65 | 272,45 / 168,85 | +1,6 % / +1,9 % |
| `lora` | 257,66 / 219,47 | 262,72 / 225,68 | +2,0 % / +2,8 % |
| `lora+adaptateur` | 184,23 / 132,67 | 185,67 / 136,33 | +0,8 % / +2,8 % |

Ce que ça dit :

* **le dessin B est un résultat du moteur** : ÷1,47 (m32) et ÷1,24 (m20) sur les deux morceaux
  jamais vus, dans un fichier que `drave` exécute. Ce n'est plus une mesure qui n'existe qu'en
  torch — et l'exécution exportée est celle qui donnait ÷1,46 / ÷1,25 en torch, donc c'est bien
  *le même* modèle des deux côtés ;
* **le gain est plus net côté moteur** que côté torch sur les deux morceaux (÷1,47 contre ÷1,46 ;
  ÷1,24 contre ÷1,25) — la quantification ne mange pas l'effet, elle le laisse passer ;
* **le LoRA seul reste derrière l'adaptateur sur m20** (225,68 contre 168,85) et légèrement devant
  sur m32 (262,72 contre 272,45) : la conclusion de la fiche du 14/10 tient, sans changement de
  signe ;
* **la chaîne complète est réutilisable** : exporter un modèle dense demande 10 s et 0,53 Go, et
  le drapeau ne coûte rien quand il n'est pas donné (invariant d'identité bit à bit).

## 4. Une variabilité qui n'était pas prévue : la GRAINE NE SUFFIT PAS

En réentraînant le **même** protocole (même graine 0, mêmes morceaux, même validation) pour
produire les poids à exporter, les bras LoRA n'ont **pas** rendu les mêmes chiffres. **Trois**
exécutions complètes, à graine fixée :

| bras | exécution 1 (m32 / m20) | exécution 2 (m32 / m20) | exécution 3 (m32 / m20) | étendue |
|---|---:|---:|---:|---:|
| `adaptateur` | 268,1317 / 165,6517 | 268,1317 / 165,6517 | 268,1317 / 165,6517 | **0,00 %** |
| `lora` | 244,0011 / 219,5141 | 257,6593 / 219,4666 | 255,6862 / 230,0257 | 5,4 % / 4,8 % |
| `lora+adaptateur` | 203,3172 / 163,2643 | 184,2311 / 132,6675 | 187,4948 / 135,9105 | **9,4 % / 18,7 %** |

Le dessin A (états précalculés en une passe, puis une matrice apprise) est **reproductible au
chiffre près** ; les bras qui rétropropagent à travers les couches ne le sont pas. La cause
probable est l'**ordre des réductions CUDA** (cuBLAS choisit ses noyaux selon l'état de la
mémoire, et onze époques amplifient une différence de 1e-7), mais **ce n'est pas démontré ici** :
ce qui est mesuré, c'est que **la graine ne suffit pas à rendre un chiffre reproductible dès
qu'on entraîne à travers les couches**, et que le dessin A, lui, l'est.

**Ce que ça fait au résultat, et ce que ça ne fait pas.** Le rapport `adaptateur / lora+adaptateur`
— la grandeur qui décide — vaut, exécution par exécution : **÷1,32 · ÷1,46 · ÷1,43** sur m32 et
**÷1,01 · ÷1,25 · ÷1,22** sur m20. Autrement dit : **le signe est stable** (le dessin B n'est
jamais pire, sur trois exécutions et deux morceaux), la **taille** varie de ±10 %, et une seule
exécution ne doit pas être citée à 1 % près. Le tableau du § 3 est celui de **l'exécution
exportée** (la 2ᵉ), et c'est la seule dont les poids ont été portés dans le moteur.

## 4bis. La passe complète du 14/10 (14 h 55)

Le moteur a changé (un champ, quatre fins de plage, un drapeau) : la passe complète est donc due,
et elle a été faite — **40 portes, 38 vertes, 2 rouges**, ~75 min, **aucune sautée**. Les deux
rouges sont **les mêmes qu'avant** et pour la même cause structurelle (`porte-indice`,
`porte-melange` : leur critère est marginal par construction, `reports/rapport-niah-fragilite.md`).
`porte-flux` rend ses cinq modes aux références (61,9920 / 60,8135) — **aucune valeur de porte n'a
bougé** — et la **40ᵉ porte** (`porte-adaptateur-sortie`) y est verte du premier coup, en 58 s.
Repères : `docs/references-non-regression.md`.

## 5. Ce que cette fiche ne dit pas

* **un seul entraînement exporté** (exécution 2) : le moteur retrouve *cet* entraînement à 2 %,
  pas « le dessin B » en général — la variabilité du § 4 (÷1,32 à ÷1,46 sur m32) n'a pas été
  portée dans le moteur trois fois ;
* **le LoRA n'est pas quantifié « pour le moteur »** : il est fusionné en fp32 **puis** quantifié
  Q8_0 avec le reste. À 5,5e-3 d'erreur relative par matrice, l'effet appris pourrait être
  partiellement absorbé — il ne l'est pas (les chiffres du moteur suivent torch à 2 %), mais la
  marge n'est pas mesurée ;
* **rien n'est fait pour que l'adaptateur survive à un déplacement** : il est écrit en f32 brut,
  sans en-tête ; le moteur vérifie la taille (896 × 896 × 4) et rien d'autre — un fichier d'un
  autre modèle de même largeur passerait ;
* **la porte d'exécution ne mesure que la perplexité** : la génération libre (décodage) n'est pas
  testée sur le chemin court — c'est un autre protocole ;
* **la cause du non-déterminisme n'est pas instruite** : ordre des réductions CUDA, choix de noyau
  `cuBLAS`, ou effet de bord d'un autre calcul — c'est dit comme une mesure, pas comme une cause.
  Ce qui est établi, c'est que le dessin A est reproductible et que les dessins B ne le sont pas.
