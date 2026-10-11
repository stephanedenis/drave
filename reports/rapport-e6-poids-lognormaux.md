# E6 — poids log-normaux : il y a un CROISEMENT. Le variant est pire à 50 % gardé, et bien meilleur à 25 %

> Campagne : **biologie** · expérience : E6 (`docs/biologie-pour-drave.md`), poids tirés d'une
> log-normale (`w = signe · e^θ`, principe de Dale) au lieu d'une gaussienne
> Question : la biologie corticale a des efficacités synaptiques **log-normales** ; nos modèles
> sont quasi gaussiens ; une distribution **multiplicative** devrait donc être **élagable par
> construction**. Le variant vaut-il mieux **sous élagage** ?
> Verdict : **OUI, mais seulement sous élagage AGRESSIF — et il y a un croisement.**
> À **50 %** de poids gardés, le témoin dense passe de **7,3429** à **7,5680** (+3,1 %) quand le
> log-normal passe de **7,5666** à **13,0622** (+72,6 %) : **le dense gagne**. À **25 %**, le dense
> s'effondre à **49,4291** (**×6,7**) quand le log-normal ne rend que **17,5009** (**×2,3**) :
> **le log-normal gagne, et de 2,8×**. L'hypothèse d'E6 n'est donc ni vraie ni fausse — elle est
> **vraie là où elle compte** (élagage fort) et **fausse là où elle ne compte pas** (élagage doux).
> Date réelle : **2026-10-11 00 h 30 HAE** (heure lue sur la machine).
> Protocole : `tools/entrainer_moteur.py` (`--elagage`, `--plancher-elagage`) · export
> `tools/exporter_gguf.py` · **occupation** : `tools/occupation_poids.py` · moteur `drave --ppl`.

## 1. La mesure

Même entraînement des deux côtés (`--dim 192 --couches 4 --tetes 4 --experts 8 --k 2 --pas 3000
--lr 3e-4 --graine 1`), mêmes 28 tenseurs élagués, même export, même texte. L'**occupation** est
mesurée dans le fichier exporté par `tools/occupation_poids.py` (le compteur de paires du moteur,
lui, ne la voit pas — c'est le manque **M9**).

| poids gardés | occupation stockée (dense) | occupation stockée (log-normal) | **dense** | **log-normal** |
|---|---:|---:|---:|---:|
| 100 % (aucun élagage) | 89,2 % | 89,2 % | **7,3429** | 7,5666 |
| 50 % | 50,6 % | 53,3 % | **7,5680** (+3,1 %) | 13,0622 (+72,6 %) |
| 25 % | 26,0 % | 30,1 % | 49,4291 (**×6,7**) | **17,5009** (×2,3) |

**Le croisement est le résultat.** Le variant log-normal **paie** un peu à l'élagage doux (il perd
72 % là où le dense perd 3 %) et **encaisse** l'élagage agressif (il perd ×2,3 là où le dense perd
×6,7). C'est exactement la forme que prédit l'argument biologique : une distribution
**multiplicative** garde ses grandes magnitudes et n'a que des petites à perdre, alors qu'une
gaussienne perd des poids **moyens** — ceux qui portent le signal.

## 2. Le témoin, et pourquoi il était nécessaire

Un poids log-normal **ne peut pas être nul** : `|w| = e^θ ≥ e^−12 = 6,1e-6`. Un poids « élagué »
n'est donc pas annulé, il est **écrasé**. Et l'occupation du fichier le montre, précisément :

| 25 % gardés | experts (Q4_0) | attention (Q8_0) | total stocké |
|---|---:|---:|---:|
| dense | 25,0 % | 25,2 % | **26,0 %** |
| log-normal | 25,0 % | **96,0 %** | **30,1 %** |

Dans les experts (quantification **Q4_0**, grille grossière), le 6,1e-6 tombe à **zéro** ; dans
l'attention (**Q8_0**, grille fine), il **survit** — 96 % des poids d'attention restent non nuls.
Le log-normal **stocke donc PLUS** que le dense (30,1 % contre 26,0 %) et rend pourtant **2,8 fois
moins** de perplexité. Sa robustesse ne vient pas de la place gagnée.

Le témoin sépare les deux causes possibles — « la distribution » et « le plancher » :

| 25 % gardés | dense, zéros exacts | **dense, plancher 6,1e-6** | log-normal |
|---|---:|---:|---:|
| perplexité | 49,4291 | **45,1232** | **17,5009** |

Le plancher **aide** un peu le dense (45,12 contre 49,43) et ne comble pas l'écart : c'est bien la
**distribution log-normale** qui fait la différence, pas l'impossibilité d'atteindre zéro.

## 3. Deux défauts de protocole, trouvés en chemin — et ils avaient INVERSÉ la conclusion

1. **Le « meilleur point » annulait l'élagage.** La sélection garde l'état du pas où la validation
   était la meilleure : pour `dense-g0.25`, c'était le **pas 1000**, où la rampe ne gardait encore
   que **78 %** des poids. Le fichier portait donc **22,3 % de zéros** et **9,0164** de perplexité,
   présentés comme « 25 % de poids gardés ». Corrigé : la cible est **réappliquée** après la
   restauration, et le harnais l'annonce (`# élagage FINAL réappliqué…`). Le chiffre corrigé est
   **49,4291** — sans quoi on aurait conclu « le log-normal est bien pire », c'est-à-dire **le
   contraire** de la vérité à 25 %.
2. **L'élagage ne couvrait que 5,8 % du modèle** (les `nn.Linear` seulement ; les experts
   fusionnés, 83 % des poids, étaient ignorés en silence) — corrigé aussi, et la couverture est
   désormais **annoncée** (28 tenseurs, 100 % des poids de projection).

**C'est l'instrument d'occupation (M9) qui a révélé le premier** : sans lui, rien dans le dépôt ne
distinguait un modèle élagué à 25 % d'un modèle élagué à 78 %.

## 4. Ce que cette fiche ne dit PAS

- **les deux taux ne sont pas des courbes** : deux points (50 % et 25 %), une graine, une échelle
  (7,58 M paramètres), un corpus. Le croisement est **entre** les deux, il n'est pas localisé ;
- **elle ne sépare pas la loi de sa contrainte** : les signes sont **figés** (principe de Dale) dans
  le variant, et c'est peut-être eux — plutôt que la loi log-normale — qui expliquent la
  robustesse. Le test qui trancherait : un modèle log-normal à **signes libres**, élagué pareil ;
- **elle ne dit rien du coût réel** : le compteur de paires du moteur ne voit pas l'occupation
  (M9), donc le gain de stockage se lit dans le **fichier** (occupation, octets) et non dans la
  ligne « paires ». À 25 %, le log-normal stocke d'ailleurs **plus** que le dense ;
- **elle ne dit pas que le variant est utilisable** : à 50 % il est 72 % pire, et à 100 % il est
  déjà 3 % derrière. Le croisement est un fait de biologie intéressant, pas encore un levier.
