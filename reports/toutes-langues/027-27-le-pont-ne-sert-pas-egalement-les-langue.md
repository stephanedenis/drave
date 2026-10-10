> Campagne : **toutes-langues** · expérience **27**
> Titre : 27. Le pont ne sert pas également les langues — et le chiffre de tête est surtout la CONSTANTE
> Date réelle : **2026-10-06 08:12 HAE** (source : commit `338d194`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 27. Le pont ne sert pas également les langues — et le chiffre de tête est surtout la CONSTANTE

Le §26 laissait une piste : les langues les plus éloignées du centroïde avaient une
norme plus grande. Je l'ai instruite à l'échelle des 41 langues de test, périmètre
**896 canaux**, réseau **40 neurones / 1 couche**, lecture quadratique — les mêmes
réglages que le résultat de tête. Résultat : la piste était à moitié fausse, et
l'enquête a mis au jour quelque chose de plus important.

### 27.1 D'abord un fait inconfortable : la fidélité EST le témoin constant

J'ai mesuré, langue par langue, la fidélité du pont **et** celle du témoin constant
(la même constante `mt` pour toutes, sans aucun neurone).

| | |
|---|---:|
| **corrélation fidélité ↔ témoin constant** | **+0,9768** |
| apport propre du pont (fidélité − témoin) | **+0,0294** en moyenne |
| étendue de cet apport | +0,0014 (heb) à +0,0885 (dzo) |

**Le classement des langues par fidélité est, à 97,7 %, le classement par le témoin
constant.** Autrement dit : la variation de « fidélité TEST » d'une langue à l'autre
ne dit presque rien du pont — elle dit à quel point la langue ressemble à la moyenne
du vivier. Le chiffre de tête (0,7430 contre 0,7207, écart +0,0223) reste exact,
mais il faut savoir que **0,72 des 0,74 sont la constante**.

Ce n'est pas une erreur de mesure : c'est la même chose que l'écart au témoin déjà
rapporté. C'est un rappel de lecture, et il manquait.

### 27.2 L'apport propre du pont : la FRAGMENTATION du tokeniseur, pas la norme

L'apport `fidélité − témoin` est ce que le pont ajoute réellement. Ce qui le prédit,
mesuré sur les 41 langues :

| variable | corrélation avec l'apport | R² seul |
|---|---:|---:|
| **fragmentation (jetons/caractère)** | **+0,8207** | **0,6735** |
| norme de la cible | −0,5912 | 0,3495 |
| témoin constant (la « marge ») | +0,1127 | 0,0127 |
| fragmentation + norme | | 0,7002 |

**Ce n'est pas un effet de marge** : la corrélation avec `1 − témoin` vaut −0,11, et
en contrôlant le témoin la corrélation avec la fragmentation reste +0,8250. Les
langues qui reçoivent le plus ne sont pas celles qui avaient le plus de place — ce
sont les langues que le tokeniseur hache.

| langue | jetons/car | apport du pont |
|---|---:|---:|
| dzo | 1,324 | **+0,0885** |
| mya | 1,017 | +0,0769 |
| csw | 1,507 | +0,0639 |
| fuf | 1,578 | +0,0610 |
| … | | |
| deu | 0,271 | +0,0133 |
| srp | 0,390 | +0,0128 |
| **heb** | 0,407 | **+0,0014** |

**Sur l'hébreu, le pont n'apporte rien du tout** — 0,0014 au-dessus d'une constante.
Et sur `deu`, `jpn`, `kor`, `heb`, `srp`, la constante est mauvaise (0,31 à 0,48) et
le pont n'y ajoute rien : **ces langues ne sont pas servies**, ni par l'un ni par
l'autre.

### 27.3 L'oracle dit où est le goulot — et la réponse n'est pas unique

Une lecture **ajustée sur la langue elle-même** (oracle, diagnostic) sépare deux
causes que la fidélité confond.

| | moyenne |
|---|---:|
| témoin constant | 0,5678 |
| pont | 0,5972 |
| **oracle par langue** | **0,6935** (+0,0963 sur le pont) |
| oracle ↔ norme | **−0,8368** (Spearman −0,7117) |
| (oracle − pont) ↔ norme | +0,3634 |

L'écart oracle−pont, qui est la part imputable au **partage**, est le plus grand
là où la norme est forte : **jpn +0,245 · fuf +0,219 · kor +0,213 · deu +0,187**,
contre **xsm +0,048**. Mais l'oracle lui-même reste bas sur ces langues (deu 0,539,
srp 0,561, jpn 0,575) : une lecture privée ne suffit donc pas non plus.

**Deux limitations se superposent** : un partage qui convient mal aux langues
atypiques, et des caractéristiques qui ne portent qu'imparfaitement leur contenu.
Je n'ai pas isolé laquelle domine — les deux proxys (norme, fragmentation) restent
corrélés à −0,55 et je ne peux pas les départager ici.

### 27.4 La norme est une propriété réelle, pas un artefact de longueur

La norme et la longueur sont très liées (corrélation −0,8176) : il fallait écarter
l'artefact. Si la norme décroissait avec la position, une moyenne sur 730 pas
vaudrait plus qu'une moyenne sur 4088.

Mesuré : corrélation norme↔position **−0,157** (jpn), −0,095 (deu), **+0,015** (dzo),
+0,026 (fuf) — quasi nulle. Et sur une **fenêtre commune des 715 premiers pas de
chaque langue**, les normes sont pratiquement identiques aux normes pleines :
écart-type **49,3 contre 49,7**, jpn 575,8 pour 574,0, deu 548,6 pour 542,2,
fuf 354,8 pour 361,7.

**La norme est réelle.** Et en contrôle partiel, elle reste le meilleur prédicteur de
l'oracle : oracle ↔ norme | fragmentation = −0,7653, contre oracle ↔ fragmentation |
norme = +0,1876.

### 27.5 Hypothèse écartée : la pondération du fit

La fidélité est un **cosinus**, donc insensible à l'échelle. Si la norme agit, ce ne
peut être que dans le **fit**, qui minimise une erreur *absolue* : une langue de
norme double y pèse quatre fois plus. J'ai ajouté la correction exacte — une pesée
`1/norme²` par langue, soit l'erreur *relative* — et **écrit la prédiction avant de
mesurer** : si l'effet vient de là, la corrélation doit tendre vers zéro.

| | fit ordinaire | fit pondéré |
|---|---:|---:|
| fidélité TEST | 0,5972 | **0,5969** |
| fidélité ↔ norme | −0,7540 | **−0,7613** |
| Q4 − Q1 (quartiles de norme) | −0,1313 | **−0,1362** |

**Réfuté** — et légèrement pire. La pondération n'est pas retenue.

### 27.6 Ce que cela change pour la suite

Le pont ne sert pas également les langues, et il ne le cachait pas : le calcul le
disait déjà, personne ne l'avait lu langue par langue. Deux conséquences :

1. **Toute affirmation sur ce pont doit nommer la langue ou le groupe.** Une
   fidélité moyenne de 0,60 recouvre 0,35 (deu) et 0,70 (dzo).
2. **Le levier le plus direct n'est pas la lecture, c'est la cible.** Pour `deu`,
   `jpn`, `kor`, `heb`, ni la constante, ni le pont, ni un ajustement privé
   n'atteignent le niveau des autres. C'est un argument pour la couche 8 : non pas
   « meilleure en moyenne » — elle l'est de +0,0215 sur Romeo — mais peut-être
   atteignable plus tôt par ces langues-là. Le traçage de la couche 8 sur les 392
   langues est en chaîne pour répondre exactement à cela.

L'outil est `tools/profil_langues.py`, la table `/tmp/profil_langues.csv` (indexée
par nom de langue).

### 27.7 Une erreur de ma part, corrigée

Dans une analyse intermédiaire, j'ai recopié un tableau de fidélités — trié par
norme décroissante — en l'associant à l'ordre du cache, qui est différent. Les
corrélations de ce script-là étaient **entièrement fausses** : il annonçait −0,042
là où la valeur est −0,754. Les corrélations publiées ici sont calculées **dans le
script**, où l'indexation est cohérente, et la table est écrite en CSV indexé par
nom. Aucun chiffre du §27 ne vient de la version fausse — mais elle a existé, donc
elle est signalée.


---
