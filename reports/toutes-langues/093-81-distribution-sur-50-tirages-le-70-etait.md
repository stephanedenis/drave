> Campagne : **toutes-langues** · expérience **81**
> Titre : 81. DISTRIBUTION SUR 50 TIRAGES : le §70 était faux dans sa formulation
> Date réelle : **2026-10-07 09:44 HAE** (source : commit `36e1f2c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 81. DISTRIBUTION SUR 50 TIRAGES : le §70 était faux dans sa formulation

### 81.1 La lacune

Toute la conclusion du §70 — *« le réservoir ABAISSE le rapport, de 1,698 à 1,354 »* —
portait sur **un seul tirage** (graine 5). Un échantillon de taille un, présenté comme une
propriété. C'est la même faute d'ordre que celle du bilan : conclure avant d'avoir
échantillonné.

### 81.2 Les 50 tirages

Même protocole, mêmes réglages (120 neurones, centrage de l'entrée, 30 articles ×
3 langues), **seule la graine change** :

| | moyenne | écart-type | min | max |
|---|---:|---:|---:|---:|
| **fidélité** | 0,4656 | **0,0013** | 0,4624 | 0,4681 |
| `P_lang` | 45,6 | 9,97 | 21,7 | 73,4 |
| `P_cont` | 90,1 | 7,75 | 65,2 | 104,4 |
| **RAPPORT** | **2,093** | **0,584** | **1,298** | **4,298** |

**Médiane 1,947 · 5ᵉ centile 1,398 · 95ᵉ centile 3,054.** Le professeur, sur ce panel :
**13,222**.

### 81.3 Et la comparaison honnête, sur le même panel

| | fidélité | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| **entrée seule, 0 neurone** | **0,5268** | 88,8 | 173,7 | **1,956** |
| **50 tirages de réservoir** | **0,4656** | 45,6 | 90,1 | **2,093** (médiane 1,947) |
| *professeur* | — | *398,1* | *5 263,4* | ***13,222*** |

### 81.4 Ce qui est corrigé

**1. Le réservoir n'abaisse PAS le rapport.** La médiane des 50 tirages (1,947) est
**égale** à l'entrée seule (1,956). Le §70 avait mesuré un tirage mal placé. **La
formulation correcte est : le réservoir est NEUTRE sur cet axe au tirage médian, et il
peut le dépasser au sommet de la distribution (jusqu'à 4,298, soit 2,2× l'entrée seule).**

**2. Mais il coûte en fidélité, systématiquement.** 0,4656 contre **0,5268** pour l'entrée
seule : **−0,061**, soit **47 fois l'écart-type entre graines (0,0013)**. Ce n'est donc pas
un problème de tirage — c'est une perte systématique que **aucune graine ne rattrape**.

**3. La variation porte sur l'axe de LANGUE, pas sur le contenu.** `P_lang` varie d'un
facteur **3,4** (21,7 à 73,4) quand `P_cont` ne varie que d'un facteur **1,6** (65,2 à
104,4). **Le tirage contrôle surtout combien de langue le réservoir injecte** — ce qui est
cohérent avec le §70 : la langue est dans l'entrée, et la projection aléatoire en laisse
passer plus ou moins.

### 81.5 Ce que la sélection Monte-Carlo apporte, chiffré

**Puisque la fidélité est CONSTANTE sur les 50 tirages (0,4656 ± 0,0013), choisir un
tirage du haut de la distribution ne coûte RIEN de plus en fidélité.**

| stratégie | fidélité | rapport |
|---|---:|---:|
| entrée seule, 0 neurone | **0,5268** | 1,956 |
| réservoir, tirage médian | 0,4656 | 1,947 |
| **réservoir, meilleur de 50** | 0,4633 | **4,298** |

**Sélectionner le tirage achète 2,2× sur le rapport pour zéro fidélité supplémentaire.**
Le compromis réel n'est donc pas « graine » mais **« réservoir contre entrée seule » :
−0,061 de fidélité pour +2,2× de rapport.**

C'est un arbitrage utilisable, et il n'était pas visible avant d'échantillonner.

### 81.6 La leçon, la troisième du même genre

Après le §79 (un effet de petit panel publié trop vite) et le bilan (« treize heures avant
de tester la ligne de base »), voici la troisième : **une conclusion tirée d'un seul
tirage, présentée comme une propriété du mécanisme.**

**Les trois ont la même forme** : une mesure unique, un énoncé général. La règle qui les
couvre toutes : **avant d'écrire « le mécanisme fait X », compter combien de fois on l'a
mesuré.**

---
