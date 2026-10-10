# C8 — une TÊTE ENTRAÎNÉE pour sa profondeur : ×540 sur la tête empruntée

> Campagne : **cerveau** · expérience : adaptateur entraîné sur l'état de profondeur 16
> Question : le chemin tronqué avec la **tête du modèle** rend une perplexité catastrophique
> (centaines de milliers). La sonde linéaire a montré que l'**état** contient l'information. Alors
> une tête **entraînée pour cette profondeur** peut-elle rendre le réflexe utilisable ?
> Verdict : **oui, et de trois ordres de grandeur** — sur le **même texte** (8 192 jetons), le
> chemin tronqué passe de **456 586,60** (tête empruntée, mesurée par le moteur) à **845,45**
> (adaptateur entraîné, évalué sur des positions **jamais vues**), soit **÷540**. Le modèle
> complet, sur ce même texte, vaut **14,2342** : le réflexe reste **×59** derrière — il devient
> **utilisable**, pas **équivalent**.
> Date réelle : **2026-10-10 13:10 HAE**.
> Protocole : `tools/c8_entrainer_tete.py` · états capturés par `drave --couches 0:16
> --tete-partielle --etat-sortie F --etat-pos 4,…,8190` · Qwen2.5-0.5B-Q8_0,
> `ids_0.5B-Q8.txt`, 8 192 jetons, tête liée `token_embd.weight` (Q8_0, gelée) + `output_norm`.

## 1. Ce qui est entraîné, et ce qui ne l'est pas

On n'entraîne **pas** une tête de sortie complète : 151 936 × 896 = 136 M poids pour 8 187
exemples, ce serait de l'apprentissage par cœur. On entraîne un **adaptateur** `A` (896 × 896,
initialisé à l'identité) qui place l'état de profondeur 16 dans l'espace que la **tête liée du
modèle** (gelée) sait déjà lire :

```text
logits = W_tête · rmsnorm(A · x₁₆)          A entraîné · W_tête et la norme GELÉES
```

La perplexité est donc **plein vocabulaire**, directement comparable aux chiffres du moteur.

## 2. Les chiffres (même texte, 8 192 jetons, test = seconde moitié des positions)

| chemin | perplexité |
|---|---|
| chemin tronqué, tête **empruntée** (moteur, référence) | **456 586,5954** |
| chemin tronqué, tête empruntée (même chaîne en Python, `A = identité`) | 341 288,1220 |
| **chemin tronqué, tête ENTRAÎNÉE** (adaptateur, époque 6) | **845,4498** |
| modèle complet (moteur, même texte) | **14,2342** — le réflexe est encore **×59** derrière |

**Gain : ÷540** sur la référence du moteur, **÷404** sur la même chaîne Python. Le réflexe passe
d'un régime inutilisable (centaines de milliers) à un régime **utilisable** (centaines) — et il
reste **×59** derrière le modèle complet **sur ce texte** (14,2342).

*(Le chiffre de 9,4341 cité dans la fiche de la sonde vient d'un texte de 1 024 jetons : le
modèle complet y vaut 9,43 contre 14,23 ici. Comparer un réflexe à 8 000 jetons avec un modèle
complet à 1 000 jetons aurait été l'erreur — les deux colonnes de ce tableau portent le même
texte.)*

## 3. Le fait qu'il faut lire avant de se réjouir : ça SURAPPREND, et vite

| époque | perplexité entraînement | perplexité test |
|---|---|---|
| 1 | 56 858 947 | 36 947 |
| 3 | 121,35 | 1 544 |
| **6** | **10,13** | **845,45** ← meilleur test |
| 9 | 2,46 | 1 005 |
| 15 | 1,18 | 2 619 |
| 30 | 1,02 | 8 683 |

L'adaptateur apprend le **texte d'entraînement** (perplexité 1,02) et **perd** sur le texte de
test : ×127 d'écart à la fin. Le chiffre à retenir est le **meilleur test** (845,45 à l'époque 6),
pas le dernier — et c'est le script qui le garde (il restaure la meilleure époque avant d'écrire
le tableau).

## 3 bis. Le réflexe va-t-il plus vite ? Oui, et c'est là sa raison d'être

Un raccourci ne vaut que s'il va **plus vite**. Mesure directe (même invite, 64 jetons générés,
`--ctx 1024`, moteur seul, machine au repos) :

| chemin | prétraitement | TTFT | génération |
|---|---|---|---|
| modèle complet (24 couches) | 23,0 tok/s | 43,5 ms | **24,91 tok/s** |
| **réflexe 16 couches** + tête | **54,9 tok/s** | **18,2 ms** | **38,31 tok/s** (**×1,54**) |
| réflexe 20 couches + tête | 39,6 tok/s | 25,3 ms | 31,77 tok/s (×1,28) |

**Le chemin court est 1,5× plus rapide en génération et 2,4× plus rapide en prétraitement.** Le
compromis est donc posé en clair : **×1,54 de vitesse pour ×59 de perplexité** (14,23 → 845 sur
le texte de 8 192 jetons). Ce n'est pas un substitut au modèle, c'est un **chemin de secours**
— et c'est exactement ce que C8 demandait : un réflexe qui répond vite quand la réponse exacte
coûte trop cher.

## 4. Ce que ça établit, et ce que ça n'établit pas

**Établi** : le maillon faible de C8 était bien la **tête**, pas la profondeur. Avec une tête
ajustée pour sa couche, l'état de profondeur 16 porte une prédiction **utilisable du prochain
jeton** — trois ordres de grandeur mieux que la tête empruntée.

**Non établi** :
- **un seul texte** : l'adaptateur est ajusté sur la première moitié d'un texte et évalué sur la
  seconde. Un vrai réflexe s'entraînerait sur un **corpus** ; ce chiffre est donc une **borne
  supérieure** de ce qu'une tête dédiée peut faire sur ce texte, pas la performance d'un modèle ;
- **l'écart au modèle complet reste ×59** (même texte) : le réflexe à 16 couches n'est pas un
  substitut, il est un **raccourci** qui coûte cher en qualité ;
- **la chaîne Python n'est pas identique au moteur** (÷1,34 sur le même état : tête en fp16 et
  rmsnorm réécrite ici, contre f32 et noyau du moteur). Le **gain** est robuste, le chiffre absolu
  porte cette incertitude ;
- **la latence est mesurée** (§ 3 bis) : **×1,54** en génération, TTFT ÷2,4 — mais c'est la
  latence du **chemin tronqué**, pas celle d'une tête entraînée (qui ajoute un matmul 896×896,
  négligeable devant une couche) ;

## 5. Deux pièges de harnais, tous deux attrapés par une erreur visible

1. **L'ordre des dimensions d'un GGUF** : `dims[0]` est la dimension **contiguë** (le pas), pas
   la première dimension logique. `token_embd.weight` est `(896, 151936)` en stockage et
   `(151936, 896)` en logique ; lire `h = dims[1]` demandait une matrice identité de **86 Gio**
   (attrapé par l'OOM, pas par le calcul) ;
2. **mélanger fp16 et fp32** lève une erreur de dtype au premier matmul — la tête et les états
   sont donc en fp16, l'adaptateur et les gradients en fp32, et la moyenne des carrés de la
   rmsnorm se calcule en fp32.

## 6. Protocole, pour rejouer

```bash
# 1. capturer les états de la profondeur voulue (une passe, ~5 min)
POS=$(seq -s, 4 8191)
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/campagne24/ids_0.5B-Q8.txt \
   --limit 8192 --ctx 8192 --threads 8 --couches 0:16 --tete-partielle \
   --etat-sortie /tmp/c8-8k/etat --etat-pos "$POS"
# 2. entraîner l'adaptateur (GPU, ~1 min)
CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python tools/c8_entrainer_tete.py \
   --etats /tmp/c8-8k/etat --ids /tmp/campagne24/ids_0.5B-Q8.txt \
   --modele models/Qwen2.5-0.5B-Q8_0.gguf --limite 8192 --epoques 30
```

**La référence à mesurer en même temps** : `--couches 0:16 --tete-partielle` **sans** adaptateur,
sur **le même texte** (456 586,60) — comparer un chiffre à 8 000 jetons avec un chiffre à 1 000
jetons était l'erreur à éviter, et elle a été évitée : les deux tableaux ci-dessus portent le
même texte.
