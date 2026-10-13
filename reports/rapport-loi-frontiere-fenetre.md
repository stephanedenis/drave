# La frontière de la fenêtre : pas de loi en N, un régime sûr (la moitié des clés) et un régime imprévisible en dessous

> Campagne : **cerveau** · expérience : la loi de la frontière en N (question ouverte du plan § 6.7)
> Question : le plan laisse ouvert « **la loi de la frontière en N** » — le prix de la fenêtre
> croît-il avec N, et à quelle vitesse ? Autrement dit : existe-t-il une règle qui dise, pour une
> séquence de N jetons, combien de clés garder pour rester sous un coût donné ?
> Verdict : **pas de loi en N seule — mais un régime sûr, et il est robuste.** À N = 2 048, garder
> **la moitié** des clés coûte **+0,5 %, +1,9 % et +0,8 %** sur trois textes différents (≤2 %
> partout) ; garder le **quart** coûte **+49,2 %, +9,7 % et +5,3 %** — un **facteur 9 selon le
> texte**. La dispersion entre textes **domine** toute tendance en N : une mesure sur un seul texte
> ne dit rien de la loi, et c'est exactement ce qui a produit la « non-monotonie » déjà notée au
> § 6.7. Le régime sûr (la moitié des clés) recoupe ce que la campagne de 4 096 jetons avait
> trouvé — il est ici **confirmé sur trois textes**.
> Date réelle : **2026-10-13, 02 h 41-03 h 58 HAE** (heure lue sur la machine)
> Protocole : `CTX=<N> FENETRES="…" PUITS="0" tools/carte-fenetre-puits.sh <N>` — perplexité de
> l'attention à fenêtre pure (aucun puits) sur les N premiers jetons, Qwen2.5-0.5B-Q8_0, machine au
> repos ; les trois textes sont trois **décalages** du même corpus (0, 20 000, 40 000 jetons)

## 1. Le prix d'une fenêtre fixe, quand N grandit (un seul texte — donc à lire avec le § 2)

| N | référence | fenêtre 256 | fenêtre 512 | fenêtre 1 024 | fenêtre 2 048 |
|---:|---:|---:|---:|---:|---:|
| 512 | 13,1368 | **+26,9 %** | 0 % (complète) | — | — |
| 1 024 | 9,4341 | **+95,7 %** | **+51,4 %** | — | — |
| 2 048 | 10,3703 | — | **+49,2 %** | **+0,5 %** | 0 % (complète) |
| 4 096 | 12,2177 | — | **+32,1 %** | **+3,2 %** | **+0,77 %** |
| 8 192 | 14,2342 | — | — | **+5,6 %** | **+2,0 %** |

Lecture naïve : « la fenêtre 512 coûte 30 à 50 % quel que soit N, la 1 024 coûte de +0,5 % à
+5,6 % selon N, la 2 048 est sous 2 % ». On en tirerait une loi en N. **Le § 2 montre que c'est
faux.**

## 2. Le même point, sur SEPT textes (N = 2 048) — c'est la mesure qui tranche

| texte (décalage du corpus) | référence | fenêtre 1 024 (N/2) | fenêtre 512 (N/4) |
|---|---:|---:|---:|
| 0 (début) | 10,3703 | **+0,5 %** | **+49,2 %** |
| 10 000 | 10,1538 | **+2,1 %** | **+8,8 %** |
| 20 000 | 14,6247 | **+1,9 %** | **+9,7 %** |
| 30 000 | 15,7767 | **+1,6 %** | **+12,8 %** |
| 40 000 | 11,0465 | **+0,8 %** | **+5,3 %** |
| 50 000 | 18,0669 | **+1,3 %** | **+3,9 %** |
| 60 000 | 12,9855 | **+0,7 %** | **+2,8 %** |
| **dispersion sur 7 textes** | — | **+0,5 % à +2,1 %** | **+2,8 % à +49,2 % (facteur 17,6)** |

* **garder la moitié des clés est robuste** : **sept** textes, **sept fois ≤2,1 %** — le coût ne
  dépend presque pas du texte ;
* **garder le quart ne l'est pas** : le même réglage va de **+2,8 %** à **+49,2 %** selon le texte
  (**facteur 17,6**). C'est ce qui rendait la série du § 1 non monotone : la valeur de
  N = 1 024 (+51,4 % pour la fenêtre 512) n'était pas un effet de N, c'était **ce texte-là** ;
* **donc la « loi en N » n'existe pas seule.** Toute loi doit être une **moyenne sur des textes**,
  avec sa dispersion — et la dispersion est du même ordre que l'effet cherché dès qu'on descend
  sous la moitié des clés.

## 2bis. Les deux façons de dépenser la moitié des clés se valent (sept textes)

Un budget d'un demi-million de clés peut se dépenser de deux manières : **une fenêtre pure de
1 024**, ou **une fenêtre de 512 plus 512 puits** (le drain). Mesuré sur les sept mêmes textes,
N = 2 048 :

| texte (décalage) | référence | fenêtre 512 + 512 puits | fenêtre 1 024 pure |
|---|---:|---:|---:|
| 0 (début) | 10,3703 | **+0,3 %** | **+0,5 %** |
| 10 000 | 10,1538 | **+2,1 %** | **+2,1 %** |
| 20 000 | 14,6247 | **+1,5 %** | **+1,9 %** |
| 30 000 | 15,7767 | **+1,9 %** | **+1,6 %** |
| 40 000 | 11,0465 | **+1,5 %** | **+0,8 %** |
| 50 000 | 18,0669 | **+0,6 %** | **+1,3 %** |
| 60 000 | 12,9855 | **+1,3 %** | **+0,7 %** |
| **dispersion** | — | **+0,3 % à +2,1 %** | **+0,5 % à +2,1 %** |

**Les deux valent la même chose** (≤2,1 % partout, et aucune ne domine l'autre texte par texte).
Autrement dit : ce qui compte est le **total** de clés gardées, pas leur **partage** entre fenêtre
et drain. C'est une bonne nouvelle pour le dessin — le partage devient un paramètre d'**implémentation**
(ce que le matériel sait faire : une fenêtre glissante contiguë, ou un drain indexé), pas de
**qualité**.

## 2sexies. À N = 4 096, la dispersion de la fenêtre N/4 se resserre — et la règle tient

Même protocole que le § 2, à **N = 4 096**, sur trois textes (décalages 0, 10 000, 20 000), avec
`tools/loi-fenetre-textes.sh` (outil écrit pour ça — il publie la moyenne, l'étendue et le minimum) :

| décalage | référence | fenêtre 2 048 (**N/2**) | fenêtre 1 024 (**N/4**) |
|---:|---:|---:|---:|
| 0 | 12,2177 | +0,8 % | +3,2 % |
| 10 000 | 7,3980 | +1,5 % | +4,7 % |
| 20 000 | 12,7867 | +0,4 % | +4,4 % |
| **30 000** | 16,1126 | **+3,0 %** | **+9,3 %** |
| **40 000** | 12,6888 | +0,4 % | +5,5 % |
| **moyenne sur 5 textes** | — | **+1,2 %** (étendue **2,6 pts**) | **+5,4 %** (étendue **6,1 pts**) |

*Correction de ma propre conclusion, et c'est la troisième du jour* : avec trois textes j'avais écrit
« N/2 = +0,9 %, étendue **1,0 point**, le régime sûr se confirme (≤2,1 %) ». Les deux textes
suivants montent à **+3,0 %** — donc à N = 4 096, garder la moitié des clés coûte jusqu'à **3 %**, et
l'énoncé « ≤2,1 % » ne tient plus. Trois textes ne suffisaient pas ; cinq non plus, mais ils
suffisent à **démentir les trois premiers**.

À comparer au § 2 (N = 2 048, sept textes) : N/2 = **+0,5 à +2,1 %**, N/4 = **+2,8 à +49,2 %**
(étendue **46 points**).

* **le régime « moitié » coûte ~1 % en moyenne, et jusqu'à 3 %** sur les dix textes des deux N
  (N = 2 048 : +0,5 à +2,1 % ; N = 4 096 : +0,4 à +3,0 %) — c'est le prix **borné** ; il n'est pas
  nul, et l'énoncé « ≤2,1 % » ne vaut que pour N = 2 048 ;
* **la dispersion, elle, ne se transporte pas non plus** : à N = 2 048 le quart des clés allait de
  +2,8 % à **+49,2 %** selon le texte (étendue 46 points), à N = 4 096 il va de +3,2 % à +9,3 %
  (étendue 6,1 points).
  Autrement dit, **même l'incertitude dépend de N et du texte** : ce n'est pas « une loi avec du
  bruit », c'est une grandeur dont la queue épaisse apparaît à certains N ;
* conséquence pratique **renforcée** : budgéter la moitié des clés, et ne jamais promouvoir un
  réglage plus agressif sur un seul texte — la queue de N = 2 048 (+49 %) est exactement ce qu'un
  banc sur un texte ne verrait pas.

### Note de méthode : `--attn-sinks 0` n'est PAS « pas de puits »

Mon premier essai de cet outil passait `--attn-sinks 0` pour dire « fenêtre pure ». Mesuré à
N = 4 096, fenêtre 2 048 : **55,9647 avec**, **12,3112 sans** (référence **12,2177**). Le zéro
**active** le mécanisme avec zéro puits et casse l'attention — c'est un piège, parce que zéro est
la valeur qui *ressemble* au neutre. L'outil **omet** désormais le drapeau, et le commentaire dit
pourquoi. (Le fait que `--attn-sinks 0` soit « exprimable » depuis le 10/10 ne veut pas dire qu'il
soit neutre : ce sont deux choses différentes, et c'est la seconde qui compte pour une mesure.)

## 3. Conséquences pour le dessin de l'attention

1. **budgéter la moitié des clés** : c'est le seul régime que trois textes confirment (≤2 %), et il
   recoupe la campagne de 4 096 jetons (« garder la moitié des clés reste le régime sûr ») ;
2. **en dessous, le prix n'est pas prévisible** : un banc qui montre « fenêtre N/4 = +2,8 % » sur un
   texte peut montrer « +49,2 % » sur un autre — et c'est arrivé **sur sept textes du même corpus**. Toute promotion d'un réglage plus agressif doit se
   faire **sur plusieurs textes**, jamais sur un seul ;
3. **le drain (puits) reste le levier à part entière** : cette expérience ne mesure que la fenêtre
   **pure** (`PUITS=0`), et le plan a montré que les puits portent l'information du début (jusqu'à
   +0,33 % pour ÷2 de clés avec 512 puits à N=2 048). Autrement dit : **la moitié des clés peut être
   prise en compte par la fenêtre, ou partagée avec les puits — mais pas réduite sous la moitié
   sans devenir imprévisible**.

## 4. Ce que cette fiche ferme et ce qu'elle laisse

* **fermé** : « la loi de la frontière en N ». Réponse : pas de loi en N seule ; le régime sûr est
  une **fraction** (la moitié), le reste est gouverné par le texte ;
* **la loi moyennée a été commencée** (§ 2sexies : un outil la mesure, dix textes au total sur
  deux N) — ce qui reste ouvert est la **queue** : combien de textes faut-il pour voir venir un
  +49 % ? La réponse est « beaucoup », et c'est précisément pourquoi la règle est de ne pas
  descendre sous la moitié des clés et le comportement **avec puits** aux mêmes points — deux expériences qui se
  mesurent avec le même outil, `FENETRES`/`PUITS`/`IDS` en paramètres.
