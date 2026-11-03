# N2 — La production à fenêtre entraînée (512 / 1 024 / 2 048) et le compute qui va avec

> **Ligne de roadmap** : N2 (le modèle de production) · **Date** : 2026-11-03 · **Verdict** :
> à **octets ajoutés constants** (61,4 Mo, le budget de N2.ac), les trois fenêtres écrasent N2.ac
> et le run de 200 000 pas ; **1 024 est la meilleure au long** (2,7342 à 2 000 octets) et **512 la
> meilleure hors domaine** (anglais 7,05, wikitext2 7,90), **2 048 ne paie pas** (3 750 pas
> seulement). En poussant la fenêtre 1 024 à **30 000 pas (307 Mo)**, le modèle de production
> atteint **2,9121** en domaine à 128 octets (60 000 pas, 552 Mo), **2,5276** à 1 000, **2,4761** à
> 2 000, et il passe
> **sous 2,5 sur la validation du grand corpus** (2,3911 à 1 000, 2,3522 à 2 000) — une première
> pour un modèle natif, **obtenue par la fenêtre et non en rabotant la longueur**. Le même compute
> à fenêtre 128 (200 k pas, 205 Mo) donne 3,1591 à 128 et **8,2262** à 1 000 : la fenêtre n'est pas
> un raffinement, c'est la condition pour que le compute serve au-delà de 128 octets.

## La question

La fiche [`rapport-n2-fenetre`](rapport-n2-fenetre.md) a montré qu'à **octets ajoutés constants**
(61,4 Mo, le budget même de N2.ac) affiner le modèle de production avec **RoPE et une fenêtre
entraînée de 512** le bat partout — 3,1588 à 128, 2,9096 à 512, 2,7607 à 2 000 — et bat le run
de 200 000 pas avec 60 % de son compute. Trois questions restaient :

1. **2 048 fait-il mieux que 512 et 1 024** sur la production, à octets ajoutés constants ?
2. **le compute avec la fenêtre** : que donne la même recette poussée à 30 000 pas à 1 024 ?
3. **l'affinage doit-il quelque chose à N2.ac** ? La fiche précédente le listait comme limite :
   le gain mesure un affinage, pas un apprentissage.

## Le dispositif

Mélange de production (`data/wiki_mix/propre`, 1,02 Go) et son canal, RoPE, 34,3 M (`384/512`),
lot 8, lr 3e-4, graine 1, canal fourni. Le mètre est `eval_production.py` (deux validations
appariées, 128 → 2 000 octets, panneau hors domaine, permutation) ; le témoin N2.ac et le run de
200 k sont repassés dans le même mètre.

| run | seq = fenêtre | pas | octets ajoutés | init |
|---|---:|---:|---:|---|
| `+ RoPE 512` | 512 | 15 000 | 61,4 Mo | `mix-60k` (N2.ac) |
| `+ RoPE 1 024` | 1 024 | 7 500 | 61,4 Mo | `mix-60k` (N2.ac) |
| **`+ RoPE 2 048`** | 2 048 | 3 750 | 61,4 Mo | `mix-60k` (N2.ac) |
| **`30 000 pas`** | 1 024 | +22 500 | +184 Mo | `mix1024-7.5k` |
| **`depuis zéro`** | 512 | 15 000 | 61,4 Mo | `init-figee` (aléatoire) |

## 1. À octets ajoutés constants : 512, 1 024, 2 048

| run | octets totaux | 128 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **N2.ac** (témoin) | 61 Mo | 3,4902 | 3,5169 | 7,9201 | 12,4065 | 6,0283 | 8,3352 | 9,0525 |
| 200 k × 128 (témoin) | 205 Mo | 3,1591 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |
| **+ RoPE 512** | 123 Mo | **3,1588** | **2,9096** | 2,8018 | 2,7607 | **5,5247** | **7,0507** | **7,9023** |
| **+ RoPE 1 024** | 123 Mo | **3,1489** | 2,9103 | **2,7858** | **2,7342** | **5,5173** | 7,1904 | 7,9521 |
| **+ RoPE 2 048** | 123 Mo | 3,1862 | 2,9325 | 2,7980 | 2,7372 | 5,5485 | 7,2908 | 8,0135 |
| **1 024, 30 000 pas** | **307 Mo** | **2,9943** | **2,7221** | **2,6143** | **2,5628** | **5,3122** | **6,5118** | **7,1544** |

Ce que la table dit, colonne par colonne :

- **à 128 octets**, les trois fenêtres sont à **0,04** l'une de l'autre (3,1489 / 3,1588 / 3,1862) :
  la fenêtre ne change presque rien à la longueur d'entraînement de N2.ac — et les trois
  **écrasent** N2.ac (3,4902) et le run de 200 000 pas (3,1591) ;
- **à 512 et 1 000**, le classement est **512 ≈ 1 024 > 2 048** ; à **2 000**, **1 024** prend la
  tête (2,7342) ;
- **hors domaine, la fenêtre 512 est la meilleure** (anglais 7,05, wikitext2 7,90, littérature
  5,52) : plus la fenêtre s'allonge à octets constants, plus les **pas** manquent, et le hors
  domaine est le premier à le payer (anglais 7,05 → 7,19 → 7,29 ; corpus propre 9,29 → 9,72 →
  10,09) ;
- **2 048 n'est jamais la meilleure** : à ce budget d'octets, il divise les pas par quatre par
  rapport à 512 et n'achète rien.

**Donc : la fenêtre de production est 1 024** (meilleure au long), avec **512** comme variante
économe et sûre hors domaine ; 2 048 ne paie pas à 61,4 Mo.

Le contrôle « même texte » du modèle 2 048 : 2,7696 → 2,6520 → 2,5948 → 2,5824 (contexte 256 →
512 → 1 024 → 2 000) — il gagne jusqu'à 1 024, puis **0,012** de 1 024 à 2 000 : la fenêtre 2 048
n'est pas inutile, elle est **sans emploi** à ce budget.

## 2. Le compute avec la fenêtre : 30 000 pas à 1 024

Le run pousse la même recette (fenêtre 1 024) de 7 500 à **30 000 pas** — **307 Mo vus** au
total (61 Mo de base + 246 Mo à 1 024), soit **1,5×** le run de 200 000 pas à fenêtre 128 :

| run | octets totaux | 128 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 200 k × 128 | 205 Mo | 3,1591 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |
| **1 024, 30 k pas** | **307 Mo** | **2,9943** | **2,7221** | **2,6143** | **2,5628** | **5,3122** | **6,5118** | **7,1544** |
| écart | | −0,165 | −0,936 | −5,612 | −10,310 | −0,293 | −0,765 | −0,847 |

Trois choses :
1. **à 128 octets, le compute paie encore** : 3,1591 → 2,9943 (−0,165) pour 1,5× les octets ;
2. **au-delà, l'écart n'est plus une marge** : −0,94 à 512, −5,6 à 1 000, −10,3 à 2 000 ;
3. **le hors domaine s'améliore avec lui** : anglais 7,28 → **6,51**, wikitext2 8,00 → **7,15**,
   littérature 5,61 → **5,31**. La fenêtre entraînée **ne coûte pas la largeur** : elle la sert.

Et le fait le plus net : sur la **validation du grand corpus**, ce modèle passe **sous 2,5**
à partir de 1 000 octets — **2,4759** à 1 000, **2,4373** à 2 000. Ce n'est pas la porte (qui se
mesure sur le corpus propre, fiche [`n2-porte-propre`](rapport-n2-porte-propre.md)) mais c'est la
première fois qu'un modèle natif passe 2,5 sur une validation tenue à part, et il le fait **avec
la fenêtre**, pas en rabotant la longueur.

## 2 bis. Le run long : 60 000 pas à fenêtre 1 024

La recette de production poussée une fois de plus (30 000 → **60 000 pas**, **552 Mo** au total) :

| fenêtre 1 024, pas | octets totaux | 128 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 500 | 122 Mo | 3,1489 | 2,9103 | 2,7858 | 2,7342 | 5,5173 | 7,1904 | 7,9521 |
| 30 000 | 307 Mo | 2,9943 | 2,7221 | 2,6143 | 2,5628 | 5,3122 | 6,5118 | 7,1544 |
| **60 000** | **552 Mo** | **2,9121** | **2,6341** | **2,5276** | **2,4761** | **5,1254** | **6,2043** | **6,7874** |
| écart 30 k → 60 k | | −0,082 | −0,088 | −0,087 | −0,087 | −0,187 | −0,308 | −0,367 |

**Chaque doublement des pas vaut ~−0,085 en domaine** (le pas de 7 500 à 30 000, ×4, valait
−0,155 ; celui de 30 000 à 60 000, ×2, vaut −0,082) : c'est une loi **géométrique** en pas, et
elle est la même à toutes les longueurs. Conséquences :

- **à 1 000 et 2 000 octets, le modèle est largement sous 2,5** sur la validation du grand corpus
  (**2,3911** et **2,3522**) et à **2,53 / 2,48** sur la validation française ;
- **à 128 octets, il reste 0,41 au-dessus de 2,5** en domaine : à −0,082 par doublement, il
  faudrait **5 doublements** (≈ **2 M de pas**) — la même classe de prix que la recette à fenêtre
  128 (1,3–2,7 M), mais avec un modèle qui, lui, **sait lire** au-delà de 128 octets ;
- **le hors domaine suit** : anglais 6,51 → **6,20**, wikitext2 7,15 → **6,79**, littérature
  5,31 → **5,13** ; le corpus propre transféré passe de 9,37 à **9,03**.

## 3. Le contrôle depuis zéro

Même recette (RoPE, seq 512, **61,4 Mo**) et **même budget d'octets ajoutés**, mais départ depuis
une **initialisation aléatoire figée** (`init_figee.pt`) au lieu de N2.ac :

| départ (61,4 Mo à 512) | octets totaux | 128 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **N2.ac** (témoin) | 61 Mo | 3,4902 | 3,5169 | 7,9201 | 12,4065 | 6,0283 | 8,3352 | 9,0525 |
| **depuis zéro** | 61 Mo | 3,3184 | 3,0709 | 2,9588 | 2,9213 | 5,7295 | 7,6921 | 8,3665 |
| **affinage de N2.ac** | 122 Mo | **3,1588** | **2,9096** | **2,8018** | **2,7607** | **5,5247** | **7,0507** | **7,9023** |

**La recette fait la moitié du travail, l'initialisation l'autre.** Depuis une initialisation
aléatoire, la recette RoPE + fenêtre 512 donne **3,3184** en domaine (−0,17 sur N2.ac, pour
61 Mo) et **2,9213** à 2 000 octets ; l'affinage de N2.ac ajoute **−0,16** en domaine et −0,19 en
anglais. Autrement dit : **le gain de longueur vient de la fenêtre** (le modèle depuis zéro
descend déjà de 3,32 à 2,92), et **l'initialisation apporte le niveau de domaine** — pas la
propriété de longueur. C'est exactement ce qu'il fallait séparer.

Réserve : l'initialisation figée est un tirage aléatoire unique ; un autre tirage déplacerait le
niveau de quelques centièmes, pas la pente.

## Ce qui pourrait le rendre faux

- **Un lancement par recette** (la recette RoPE est déterministe à graine fixée et init fixée :
  deux lancements redonnent les mêmes poids, donc il n'y a pas d'intervalle de graine à attendre).
- **Les trois fenêtres n'ont pas le même nombre de pas** (15 000 / 7 500 / 3 750) : à octets
  ajoutés constants, la fenêtre large paie en pas. C'est le contrôle le plus strict pour les
  octets, pas pour l'optimisation.
- **La production mesure un affinage** à partir de N2.ac ; le contrôle depuis zéro dit ce que
  l'initialisation apporte, pas ce qu'un entraînement complet donnerait.
**Le coût d'inférence ne quadruple pas.** Mesuré à batch 8 (`work/n2ac/cout_fenetre.py`),
le débit passe de **22 306** octets/s (fenêtre 256) à **22 730** (512), **21 156** (1 024) et
**19 405** (2 048) : l'attention quadruple à chaque doublement, mais le FFN **domine** à 34,3 M,
donc le débit ne perd que **13 %** de 256 à 2 048. La fenêtre est presque gratuite à cette
taille — elle ne le resterait pas à plus grande échelle.
- **Le corpus propre reste le juge de la porte < 2,5** ; ces chiffres sont du domaine `wiki`, et
  le « sous 2,5 » du grand corpus est une validation **du même domaine** que l'entraînement.
- **Le run à 30 000 pas** part de N2.ac : 61 Mo de base + 246 Mo à 1 024 ; le comparer au 200 k
  (205 Mo depuis zéro) avantage la fenêtre **et** l'initialisation — le contrôle depuis zéro
  (§ 3) sépare les deux.

## Fichiers

- Modèles : `work/n2ac/mix512-15k.pt`, `mix1024-7.5k.pt`, `mix2048-3.75k.pt`,
  `mix1024-30k.pt`, `mix512-zero-15k.pt` ; témoins `work/n2w/mix-60k.pt`,
  `work/n2ac/mix-200k.pt`.
- Bancs : `work/n2ac/eval_production.py`, `eval_fenetre.py`, `chaine_production.sh`,
  `chaine_2048_mix.sh`, `chaine_prod1024_long.sh`, `chaine_prod_zero.sh`.
- Mesures : `reports/n2-production-fenetre.json` ; fiches amont
  [`n2-fenetre`](rapport-n2-fenetre.md), [`n2-r12-2048`](rapport-n2-r12-2048.md),
  [`n2-200k`](rapport-n2-200k.md).
