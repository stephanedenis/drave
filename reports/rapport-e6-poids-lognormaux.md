> **⚠ CHIFFRES EN COURS DE RE-MESURE (11/10, 01 h 50).** Un défaut vient d'être trouvé dans le
> harnais : sous reparamétrisation, `named_parameters()` rend `...parametrizations.weight.original`
> et **non** `...weight`, si bien qu'un filtre ajouté la veille excluait le poids lui-même — les
> variantes **log-normale, signes libres et signes figés** n'avaient donc **que leurs experts
> élagués** (attention : 1,0 % de zéros au lieu de 75 %). Tous les chiffres de cette fiche portant
> sur ces trois variantes ont été mesurés sous un élagage **plus léger** que celui du témoin dense
> et sont **en cours de re-mesure** ; ceux du témoin dense, des contrôles et des occupations
> restent valides. Le défaut est corrigé et vérifié (les quatre variantes donnent maintenant
> 25,2 % d'occupation d'attention à 25 % gardés).

# E6 — poids log-normaux : l'hypothèse est RÉFUTÉE, c'est la CONTRAINTE DE SIGNE qui fait tout

> Campagne : **biologie** · expérience : E6 (`docs/biologie-pour-drave.md`), poids tirés d'une
> log-normale (`w = signe · e^θ`, principe de Dale) au lieu d'une gaussienne
> Question : la biologie corticale a des efficacités synaptiques **log-normales** ; nos modèles
> sont quasi gaussiens ; une distribution **multiplicative** devrait donc être **élagable par
> construction**. Le variant vaut-il mieux **sous élagage** ?
> Verdict : **NON — la bonne réponse est ailleurs, et le plan 2x2 la nomme.**
> Un contrôle sépare ensuite les deux causes : **c'est la CONTRAINTE DE SIGNE qui porte tout**
> (§ 4 et 4 ter) — et la **loi log-normale NUIT** (17,50 contre 7,95 à contrainte comparable).
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

## 4. Premier contrôle : à loi log-normale, les signes libres ou figés ?

Le variant log-normal diffère du témoin dense par **deux** choses : la **loi** des magnitudes
(multiplicative) et le **signe figé** (principe de Dale). Le croisement du § 1 ne dit pas laquelle
des deux porte la robustesse. Le contrôle : **mêmes magnitudes log-normales, signes MOBILES** —
`w = tanh(ψ) · e^θ`, ψ initialisé sur les signes de naissance (`tanh(±6) = ±1,0000`) mais libre de
basculer pendant l'entraînement.

| 25 % de poids gardés | témoin dense | log-normal, **signes libres** | log-normal, **signes figés** (Dale) |
|---|---:|---:|---:|
| perplexité | 49,4291 | **36,3771** | **17,5009** |
| occupation stockée | 26,0 % | 26,0 % | 30,1 % |

Et **sans aucun élagage**, les trois partent du même point : **7,3429** (dense) · **7,5112**
(log-normal, signes libres) · **7,5666** (signes figés).

**Lecture (provisoire — le § 4 bis la corrige).** À loi log-normale, libérer les signes coûte cher
(36,38 contre 17,50), donc la contrainte de signe **compte**. Mais ce plan ne dit pas si c'est
ELLE qui fait tout : il manque le coin « magnitudes libres, signes figés », et c'est le § 4 bis. Sous élagage agressif, ce n'est donc **pas** la distribution des magnitudes qui sauve le
modèle : c'est le fait qu'un poids ne puisse **pas changer de signe**. Un neurone excitateur le
reste — et c'est cela qui rend l'élagage supportable.

## 4 bis. LE PLAN 2x2 COMPLET : c'est la CONTRAINTE DE SIGNE qui fait tout, et la loi log-normale NUIT

Le § 4 comparait trois coins du plan 2x2. Le quatrième — **magnitudes libres, signes figés**
(`w = signe · |θ|`, `--signes-figes`) — le complète, et il **renverse la lecture** :

| 25 % de poids gardés | magnitudes libres, signes libres (dense) | **magnitudes libres, signes FIGÉS** | log-normales, signes libres | log-normales, signes FIGÉS |
|---|---:|---:|---:|---:|
| perplexité | 49,4291 | **7,9467** | 36,3771 | 17,5009 |
| facteur sur le non-élagué | x6,7 | **x1,09** | x4,8 | x2,3 |
| occupation stockée | 26,0 % | 30,3 % | 26,0 % | 30,1 % |

Et **aux trois taux d'élagage**, les quatre variantes (même graine, même protocole) :

| poids gardés | dense | **signes figés, magnitudes libres** | log-normal, signes libres | log-normal, signes figés |
|---|---:|---:|---:|---:|
| 100 % | 7,3429 | **7,3003** | 7,5112 | 7,5666 |
| 50 % | 7,5680 | **7,3470** | 11,7783 | 13,0622 |
| 25 % | 49,4291 | **7,9467** | 36,3771 | 17,5009 |

**Trois conclusions, et la troisième est la plus forte.**

1. **C'est la contrainte de signe qui porte tout.** Le modèle à signes figés et magnitudes libres
   passe de **7,30** (aucun élagage) à **7,95** (25 % gardés) : **x1,09**. Le témoin dense, lui, est
   multiplié par **6,7**. Aucune autre variante n'en approche.
2. **La loi log-normale NUIT.** À contrainte comparable (signes figés), elle donne **17,50** là où
   des magnitudes libres donnent **7,95** — **2,2 fois pire**. L'hypothèse d'E6 (« une distribution
   multiplicative est élagable par construction ») n'est pas seulement inutile, elle est
   **contre-productive**. Ce qui aide est que `|w|` puisse **descendre à zéro** librement — ce que
   `e^θ` interdit (plancher à 6,1e-6).
3. **le gain est là même sans élaguer** : à 100 %, les signes figés rendent **7,3003** contre
   **7,3429** au témoin. L'écart est petit (0,6 %) et sur **une** graine : il se lit comme « au même
   niveau », pas comme un gain — mais il écarte l'objection « on paie la robustesse par la
   qualité ». **Il n'y a rien à payer.**

**ET LE RÉSULTAT SE REPRODUIT SUR TROIS GRAINES** (25 % gardés, même protocole) :

| graine | témoin dense | **signes figés** | rapport |
|---|---:|---:|---:|
| 1 | 49,4291 | **7,9467** | ×6,2 |
| 2 | 55,4520 | **7,9873** | ×6,9 |
| 3 | 46,6111 | **8,2676** | ×5,6 |

Le témoin dense varie de **46,6 à 55,5** (×5,6 à ×6,9 sur son propre point de départ) ; le modèle à
signes figés reste entre **7,95 et 8,27**, soit **×1,09 à ×1,13**. Les intervalles ne se touchent
pas : ce n'est pas une graine chanceuse.

**Ce que ça change pour la suite.** Le levier n'est pas la loi des poids, c'est le **principe de
Dale** — un signe choisi à la naissance et jamais changé. C'est une recette d'**entraînement** de
trois lignes, pas un changement de moteur, et elle rend un modèle **quasi insensible à l'élagage** :
le dessin « poids creux » redevient mesurable autrement que par sa perte de qualité.

## 5. Le volet COÛT, fermé par l'instrument d'occupation

Le compteur de paires du moteur ne voit pas l'occupation (manque **M9**) : il rend **2,3 M** pour
tous ces modèles. `tools/occupation_poids.py` donne l'autre colonne — ce qu'un format **creux**
lirait, en supposant les non-nuls répartis comme les activations vivantes (**hypothèse**) :

| modèle | paires noyau (moteur) | paires **creuses** estimées | ÷ |
|---|---:|---:|---:|
| dense, aucun élagage | 2,20 M | 1,99 M | ÷1,11 |
| **dense, 25 % gardés** | 2,20 M | **0,55 M** | **÷4,0** |
| **log-normal, 25 % gardés** | 2,20 M | **0,83 M** | **÷2,7** |

**Le dense gagne le coût et perd la qualité ; le log-normal fait l'inverse.** À 25 % gardés, le
dense lirait **÷4,0** de paires pour une perplexité de **49,43**, le log-normal **÷2,7** pour
**17,50**. Le choix dépend donc de ce qu'on paie : des paires, ou de la qualité.

## 6. Ce que cette fiche ne dit PAS

- **les deux taux ne sont pas des courbes** : deux points (50 % et 25 %), une graine, une échelle
  (7,58 M paramètres), un corpus. Le croisement est **entre** les deux, il n'est pas localisé ;
- **le § 4 sépare la loi de sa contrainte, et il donne raison à la contrainte** — mais sur UNE
  graine, une échelle et deux taux d'élagage. Le `tanh(ψ)` est une manière parmi d'autres de
  libérer les signes ;
- **le volet coût du § 4 est une ESTIMATION** : elle suppose les non-nuls répartis comme les
  activations vivantes, et le compteur du moteur ne la vérifie pas (M9, seconde moitié à faire) ;
  à 25 %, le log-normal stocke d'ailleurs **plus** de poids non nuls que le dense (30,1 % contre
  26,0 %) ;
- **elle ne dit pas que le variant est utilisable** : à 50 % il est 72 % pire, et à 100 % il est
  déjà 3 % derrière. Le croisement est un fait de biologie intéressant, pas encore un levier.
