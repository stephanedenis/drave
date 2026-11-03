# N2/R1 — La fenêtre entraînée, de 128 à 1 024 : elle gagne où elle sert, et elle bat 200 000 pas

> **Lignes de roadmap** : **R1** (la fenêtre native) et **N2** (le modèle de production) ·
> **Date** : 2026-11-02/03 · **Verdict** : à **octets constants** (20,5 Mo vus), entraîner sur des
> séquences longues avec RoPE abaisse la PPL là où la fenêtre sert — à **1 000 octets**,
> 3,2545 (fenêtre 256) → 3,0107 (512) → **2,9950** (1 024) ; à **2 000**, 3,2459 → 2,9728 →
> **2,9449** — et à courte longueur l'ordre **s'inverse** (128 : 3,3399 pour 512 contre 3,3878
> pour 1 024) : la fenêtre longue échange du **démarrage à froid** contre de la **profondeur**.
> Le contrôle « même texte » le tranche : **chaque modèle sature exactement à sa fenêtre** —
> fenêtre 256 : 3,0663 → 3,1411 (il **se dégrade** au-delà de 256) ; 512 : 2,9068 → 2,8076 ;
> 1 024 : 2,9197 → **2,7837**, et 1 024 = 2 000 au millième. Sur le **modèle de production**,
> affiner N2.ac avec RoPE et 512 octets pendant **61,4 Mo** (le budget même de N2.ac) le bat
> **partout** : 3,4902 → **3,1588** à 128, 3,5169 → **2,9096** à 512, 7,9201 → **2,8018** à
> 1 000, 12,4065 → **2,7607** à 2 000, et 6,03 → **5,52** en littérature, 8,34 → **7,05** en
> anglais, 9,05 → **7,90** sur wikitext2. Il **bat aussi le run de 200 000 pas** (205 Mo) à 128
> (3,1588 contre 3,1591) et sur les trois mesures hors domaine, avec **60 % de son compute**.

## La question

R1.1/R1.2 ont montré deux choses : les positions relatives ôtent l'**explosion de table** (mais
ne donnent pas la lecture longue depuis zéro), et à **une seule** fenêtre (512, à octets
constants) la PPL baisse et le gain **croît avec la longueur**. Il manquait la **loi** : que
donne 1 024 ? où s'arrête le gain ? Et la question de production : **la fenêtre battrait-elle le
compute**, qui vient de coûter 3 h 10 pour −0,33 ?

## Le dispositif

| run | corpus | seq / fenêtre | pas | octets vus | init |
|---|---|---:|---:|---:|---|
| R1.1 | `data/wiki_fr` | 128 / 256 | 20 000 | 20,5 Mo | `base-wiki-45m` |
| R1.2-512 | `data/wiki_fr` | 512 / 512 | 5 000 | 20,5 Mo | `base-wiki-45m` |
| **R1.2-1 024** | `data/wiki_fr` | **1 024 / 1 024** | **2 500** | **20,5 Mo** | `base-wiki-45m` |
| R1.2-1 024 long | `data/wiki_fr` | 1 024 / 1 024 | 20 000 | 164 Mo | (suite du précédent) |
| **prod + 512** | `data/wiki_mix` | **512 / 512** | **15 000** | **61,4 Mo** | `mix-60k` (N2.ac) |
| **prod + 1 024** | `data/wiki_mix` | 1 024 / 1 024 | 7 500 | 61,4 Mo | `mix-60k` (N2.ac) |

Tous : RoPE, 34,3 M (`384/512`), lot 8, lr 3e-4, graine 1, canal. Mètre `eval_production.py`
(128/256/512/1 000/2 000 sur les deux validations appariées), `eval_fenetre.py` (même texte à
contexte 256/512/1 000/2 000), `miroir_copie.py`. Le témoin `mix-60k` repassé dans le même mètre
redonne N2.ac à l'identique.

## 1. La loi de la fenêtre, à octets constants (20,5 Mo)

| longueur | fenêtre 256 (20 000 pas) | fenêtre 512 (5 000 pas) | **fenêtre 1 024 (2 500 pas)** |
|---|---:|---:|---:|
| 128 | 3,3696 | **3,3399** | 3,3878 |
| 256 | 3,3217 | **3,2271** | 3,2542 |
| 512 | 3,2892 | **3,0990** | 3,1098 |
| 1 000 | 3,2545 | 3,0107 | **2,9950** |
| 2 000 | 3,2459 | 2,9728 | **2,9449** |

Chaque fenêtre gagne **jusqu'à sa longueur** (512 domine jusqu'à 512) et la plus longue prend le
relais **au-delà** (1 024 gagne à 1 000 et 2 000). À 128 octets, la fenêtre 512 est la meilleure :
la fenêtre longue paie un peu de **démarrage à froid** — elle a moins de pas d'optimisation à
octets constants (2 500 contre 5 000 et 20 000), et sa distribution d'entraînement est faite de
séquences profondes.

## 2. Le contrôle « même texte » : la saturation est exactement la fenêtre

Même flux d'octets, mêmes 128 cibles finales, seul le préfixe disponible change :

| modèle | contexte 256 | contexte 512 | contexte 1 000 | contexte 2 000 |
|---|---:|---:|---:|---:|
| fenêtre 256 (20 000 pas) | 3,0663 | 3,1392 | 3,1413 | 3,1411 |
| fenêtre 512 (5 000 pas) | 2,9068 | **2,8119** | 2,8073 | 2,8076 |
| **fenêtre 1 024 (2 500 pas)** | 2,9197 | 2,8125 | **2,7847** | **2,7837** |

Trois signatures nettes :
1. **fenêtre 256** : au-delà de 256, le contexte supplémentaire **coûte** (+0,07) — le modèle n'a
   jamais vu ces distances ;
2. **fenêtre 512** : le gain s'arrête **à 512** (2,8119 → 2,8073 → 2,8076) ;
3. **fenêtre 1 024** : le gain continue jusqu'à **1 024** (2,8125 → 2,7847) puis s'arrête
   (2,7847 → 2,7837) — et l'invariance 1 024 = 2 000 confirme que RoPE ne dépend que de l'écart.

C'est la démonstration la plus directe de la nuit : **la fenêtre entraînée est la borne**, et le
modèle l'utilise jusqu'au dernier octet.

## 3. La production : la fenêtre bat le compute

| modèle | octets vus | 128 | 256 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **N2.ac** (60 k × 128) | 61,4 Mo | 3,4902 | 3,4615 | 3,5169 | 7,9201 | 12,4065 | 6,0283 | 8,3352 | 9,0525 |
| 200 k × 128 | 205 Mo | 3,1591 | 3,2047 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |
| **prod + RoPE 512** (15 k) | 123 Mo | **3,1588** | **3,0430** | **2,9096** | **2,8018** | **2,7607** | **5,5247** | **7,0507** | **7,9023** |
| prod + RoPE 1 024 (7,5 k) | 92 Mo | 3,1489 | 3,0488 | 2,9103 | 2,7858 | 2,7342 | 5,5173 | 7,1904 | 7,9521 |

Trois lectures :
1. **à 128 octets, la fenêtre rattrape les 200 000 pas** (3,1588 contre 3,1591) avec **60 %** de
   leur compute (123 Mo contre 205 Mo) ;
2. **au-delà, elle les écrase** : 2,9096 contre 3,6577 à 512, 2,8018 contre 8,2262 à 1 000,
   2,7607 contre 12,8723 à 2 000 — l'écart n'est pas une marge, c'est un **facteur 4,7** ;
3. **le hors domaine s'améliore aussi** (littérature −0,50, anglais −1,28, wikitext2 −1,15) :
   la fenêtre ne coûte rien à la largeur, elle la sert.
4. le contrôle « même texte » du modèle 512 sature **à 512** (2,7321 → 2,6357 → 2,6268 →
   2,6275) : il utilise bien la fenêtre qu'on lui a donnée, pas plus. Celui du modèle 1 024 :
   2,7401 → 2,6277 → **2,5846** (1 024) → 2,5868 (2 000) — il sature **à 1 024**, et à contexte
   1 024 il **bat de 0,043** le modèle 512 (2,5846 contre 2,6275).
5. **à octets ajoutés égaux, 1 024 ne bat 512 que là où il faut** : −0,016 à 1 000 et −0,027 à
   2 000, mais +0,14 en anglais et +0,43 sur le corpus propre — avec **deux fois moins de pas**
   (7 500 contre 15 000). Sur la production, la fenêtre 512 est le meilleur compromis ; 1 024 est
   meilleur si l'on ne lit que du long.

## 4. Le miroir de copie reste muet

Sur les modèles à fenêtre entraînée (1 024 et production 512), la justesse de copie à distance
reste **0,0078** au mieux (1/128 : le hasard) — la fenêtre plus large **ne crée pas** de circuit
de copie à 34,3 M. La PPL plate et la lecture restent deux choses distinctes ; la fenêtre est une
condition nécessaire, pas suffisante.

## Ce que ça change

- **La recette de production change** : `mix-60k` + **RoPE, fenêtre 512, 15 000 pas** bat N2.ac
  partout, pour une heure de GPU — c'est le nouveau modèle de production proposé. La fenêtre
  **1 024** ne paie que sur le long (et coûte un peu hors domaine) : **512 est le compromis**,
  1 024 la variante « lecture longue ».
- **La fenêtre est le levier**, pas les pas : le run de 200 k a coûté 3 h 10 pour −0,33 en
  domaine et **+0,14 à 512** ; la fenêtre coûte 1 h et rend − 0,33 en domaine **et −0,61 à 512**.
- **La prochaine étape** : fenêtre **2 048** (en cours) et **1 024** sur la production ; puis la
  distillation d'un professeur à fenêtre longue (la note de passage N2 → R1 le demandait déjà).

## Ce qui pourrait le rendre faux

- **Les pas d'optimisation ne sont pas contrôlés à octets constants** : 20 000 / 5 000 / 2 500 pas
  pour 20,5 Mo. La fenêtre longue gagne malgré **moins** de pas, mais l'écart à 128 octets
  (3,3399 contre 3,3878) peut être du budget d'optimisation, pas de la fenêtre. Le run de
  20 000 pas à 1 024 (en cours) tranchera.
- **Un seul lancement par recette** ; la recette RoPE est déterministe (poids au hash près) mais
  un seul point de départ.
- **La production part de N2.ac** : le gain mesure un **affinage**, pas un entraînement depuis
  zéro ; un modèle entraîné directement à 512 ferait peut-être mieux (ou moins bien).
**Le coût d'inférence ne quadruple pas.** Mesuré à batch 8 (`work/n2ac/cout_fenetre.py`),
le débit passe de **22 306** octets/s (fenêtre 256) à **22 730** (512), **21 156** (1 024) et
**19 405** (2 048) : l'attention quadruple à chaque doublement, mais le FFN **domine** à 34,3 M,
donc le débit ne perd que **13 %** de 256 à 2 048. La fenêtre est presque gratuite à cette
taille — elle ne le resterait pas à plus grande échelle.
- **Le corpus propre reste à 9,29** (contre 9,27) : la fenêtre ne transfert pas mieux que le
  compute vers un autre domaine.

## Fichiers

- Modèles : `work/n2ac/rope1024-2.5k.pt` (et `-20k`), `work/n2ac/mix512-15k.pt`,
  `work/n2ac/mix1024-7.5k.pt` ; témoins `work/n2j/base-wiki-45m.pt`, `work/n2w/mix-60k.pt`,
  `work/n2ac/mix-200k.pt`.
- Bancs : `work/n2ac/eval_production.py`, `eval_fenetre.py`, `miroir_copie.py`,
  `chaine_1024.sh`, `chaine_production.sh` ; les mêmes dans
  `journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/`.
- Mesures : [`n2-fenetre.json`](n2-fenetre.json) ; fiches amont
  [`n2-r11`](rapport-n2-r11.md), [`n2-200k`](rapport-n2-200k.md).
