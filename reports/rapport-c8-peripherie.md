# C8 — la périphérie : l'entrée entre, la sortie sort, le délai est exact — mais le modèle ne GARDE pas le signal

> Campagne : **cerveau** · expérience : régions frontière (entrée, sortie, délai) et tâche fermée
> Question : le plan demande une **entrée** (un signal), un **effecteur** avec délai, et une
> **tâche fermée** — « poursuivre une consigne ». La mécanique en place, la sortie **porte-t-elle**
> le signal, et le porte-t-elle **encore** quelques pas plus tard (la poursuite, c'est-à-dire la
> mémoire) ?
> Verdict : **la mécanique est là et vérifiée, la mémoire du signal n'y est pas.** L'état de sortie
> porte le signal **courant** (R² = **0,913** en mode récurrent, 0,377 en pas indépendants), mais
> **pas** le signal d'il y a 8 pas (R² = **−0,973**) : le modèle ne garde rien de linéairement
> lisible. Le délai demandé au moteur, lui, est **exact** — mais c'est **l'interface** qui fait la
> mémoire, pas le cerveau, et la différence est écrite ici pour qu'elle ne se confonde pas.
> Date réelle : **2026-10-10 16:50 HAE**.
> Protocole : `drave --entree signal:F --sortie G [--delai N] [--recurent]`, puis
> `tools/peripherie_poursuite.py` (lecture apprise par régression ridge, moitié des pas pour
> apprendre, l'autre pour mesurer). Porte : `tools/porte-peripherie.sh`.

## 1. Ce qui est branché, et ce que la porte verrouille

| élément | état | vérifié par |
|---|---|---|
| **entrée** `--entree signal:F` (une valeur par ligne) | ✅ | la porte (7 pas écrits, commentaires ignorés) |
| **canal** `--entree-canal K`, **gain** `--entree-gain X`, **jeton de base** `--entree-jeton N` | ✅ | refus (code 2) si le canal ou le jeton sort du modèle |
| **sortie** `--sortie F` : l'état de chaque pas (f32) | ✅ | 7 pas × 896 canaux = 25 088 octets |
| **délai** `--delai N` : le moteur injecte `v[t−N]` | ✅ | les valeurs injectées sont **décalées d'exactement 3**, vérifiées une à une |
| **déterminisme** (invariant du plan) | ✅ | deux exécutions rendent des fichiers **identiques au bit près** ; à gain nul, les 7 pas rendent le **même** état |
| **métrique du plan** : paires par décision | ✅ | passe complète **357,8 M**, réflexe 16 couches **238,6 M**, réflexe 8 couches **119,3 M** (−67 %) |
| **mode récurrent** `--recurent` : positions croissantes, historique dans le cache KV | ✅ | ajouté pour que « poursuivre » ait un sens |

## 2. La tâche fermée : ce que l'état porte, et ce qu'il ne porte pas

Signal : **bruit** uniforme (64 pas, graine fixée) — un signal non prévisible depuis son propre
passé, sans quoi un « témoin » qui lit `v[t+1]` serait lu par simple périodicité (c'est arrivé avec
une sinusoïde : le témoin sortait à R² = 0,85, ce qui ne mesurait rien).

| configuration | lecture de `v[t]` | lecture de `v[t−8]` | témoin `v[t+1]` |
|---|---|---|---|
| **A** pas indépendants, délai 0 | R² **+0,377** | R² −11,289 | R² −2,728 ✅ |
| **B** **récurrent**, délai 0 | R² **+0,913** | R² **−0,973** | R² −0,770 ✅ |
| **C** pas indépendants, **délai 8** | R² −5,899 | R² **+0,207** | R² −8,639 ✅ |

**Trois lectures :**

1. **le signal courant est bien dans la sortie** — et *mieux* en mode récurrent (0,913 contre
   0,377) : l'historique aide à le représenter ;
2. **il n'y a aucune mémoire du signal** : ni en mode récurrent (R² négatif pour `v[t−8]`), ni
   ailleurs. Le modèle n'a aucune raison de retenir un scalaire qu'on lui injecte, et il ne le
   retient pas ;
3. **le délai de l'interface fonctionne** (colonne C : `v[t−8]` lisible, `v[t]` non) — c'est une
   **mémoire faite par le harnais**, pas par le réseau, et il faut le dire ainsi.

**Le témoin est bas partout** (R² négatif) : le protocole ne fuit pas — le modèle ne lit pas
l'avenir, ce qui valide la méthode de lecture.

## 2 bis. La mémoire est-elle APPRENABLE ? Non : elle n'est pas là, même pour une lecture non linéaire

Une lecture linéaire qui échoue ne prouve pas que l'information est absente — elle prouve qu'elle
n'est pas **linéairement** accessible. C'est la leçon de la sonde C8, et il fallait la refaire ici.
Mesure sur **4 096 pas** (signal de bruit, mode récurrent, `--ctx 4096`), apprentissage sur les
2 048 premiers pas, mesure sur les 2 048 derniers (`tools/peripherie_memoire.py`) :

| cible | lecture linéaire | lecture **non linéaire** (896→256→1, GELU) |
|---|---|---|
| **`v[t]`** (le présent) | R² +0,982 | R² **+0,992** |
| **`v[t−8]`** (la mémoire) | R² −0,611 | R² **−0,681** |
| `v[t+1]` (TÉMOIN avenir) | R² −1,704 | R² −0,905 |

**Le présent est parfaitement lisible (0,992) et le passé ne l'est pas du tout (−0,681)** : la
mémoire n'est pas « tordue » dans l'état, elle **n'y est pas**. Le témoin avenir reste négatif —
le protocole ne fuit pas.

**Ce que ça ne dit pas** : l'information du passé existe **ailleurs** — le cache KV garde les clés
et valeurs de tous les pas (c'est son rôle). Ce qui manque, c'est qu'elle **remonte dans l'état
résiduel** : le modèle n'a jamais été entraîné à retenir un scalaire injecté, donc il ne le
retient pas. La suite est donc, là encore, un **entraînement** (ou une lecture branchée sur le
cache KV, qui est une autre expérience) — pas un câblage.

## 2 ter. Est-ce la tâche qui est dure, ou le modèle qui n'a pas de mémoire ? Les deux références

Question légitime après le § 2 bis : si aucune lecture ne retrouve `v[t−8]`, peut-être que la
**tâche** est difficile. Deux références la tranchent (`--reference`) :

| lecture de `v[t−8]` | R² |
|---|---|
| état du modèle, lecture linéaire | −0,611 |
| état du modèle, lecture **non linéaire** | −0,681 |
| **récurrence linéaire à 64 canaux** (`h = σ(a)·h + b·v`, entraînée) | **+0,104** |
| **ligne à retard de 8 pas** (tampon) | **+1,000** (exact par construction) |

**Trois conclusions, et la deuxième est la plus utile :**

1. la tâche **n'est pas dure** : un tampon de 8 pas la résout exactement. Le plancher existe et il
   est trivial ;
2. **une récurrence qui fuit ne suffit pas** : `h = σ(a)·h + b·v` est un **intégrateur** — il rend
   la *somme* des derniers pas, pas le pas d'il y a 8. Elle plafonne à 0,104, et ce n'est pas un
   défaut de réglage : c'est sa nature. (Premier essai avec `tanh` : 0,126 — la saturation écrasait
   l'état ; sans saturation, 0,104. Les deux disent la même chose.) **Retenir demande une
   STRUCTURE, pas un paramètre de plus** ;
3. l'état du modèle ne contient donc pas trace du passé, et **aucune** des deux références ne
   s'applique à lui : il n'a ni tampon, ni récurrence — il a une pile feed-forward, et le passé
   n'existe pour lui que dans le cache KV, où il n'est pas relu.

**Ce que ça ajoute à la ligne C8** : après « il faut une tête entraînée par profondeur » (le
réflexe), voici « il faut une **structure** de mémoire » (la poursuite). Les deux fois, le câblage
n'était pas le manque.

## 2 quater. Donner le passé en entrée : il devient PARTIELLEMENT lisible (0,283)

Si le passé n'est pas dans l'état, une idée évidente est de le **remettre en entrée** : le signal
devient un vecteur — la valeur courante plus les `K` précédentes sur les canaux suivants
(`--entree-memoire K`, vérifié par la porte). Mesure sur 256 pas, lecture de `v[t−8]` :

| configuration | lecture `v[t]` | lecture `v[t−8]` |
|---|---|---|
| récurrent seul | R² +0,980 | R² **−0,399** |
| **récurrent + tampon de 8 pas** | R² +0,852 | R² **+0,283** |

**Le tampon change le signe du résultat** : le passé devient **partiellement** lisible (28 % de la
variance), là où il ne l'était pas du tout. Mais **28 %, ce n'est pas une mémoire** : le réseau
transforme ce qu'on lui donne, et une partie de l'information se perd dans la transformation.

Et un détail qui compte : en mode **pas indépendants**, le même tampon rend les choses **pires**
(R² −3,8) — injecter neuf canaux de bruit dans une entrée que le réseau ne replace dans aucun
contexte produit un état que rien ne lit. La récurrence est ce qui donne un contexte à ce tampon.

**Conclusion de la ligne** : une mémoire exacte demande une **structure qui ne passe pas par la
transformation du réseau** — une ligne à retard lue directement (R² 1,000, § 2 ter). C'est un choix
d'architecture, et il est maintenant chiffré dans les trois sens : sans structure, rien (−0,4) ;
avec un tampon remis en entrée, partiel (0,283) ; avec une ligne à retard, exact (1,000).

## 3. Ce que ça change pour C8

**Acquis** : les **régions frontière existent** (le plan disait « rien ne sort » — c'était vrai) ;
le déterminisme est tenu au bit près, le délai est exact, et **chaque décision a son prix en
paires**, ce qui est la métrique du plan. Le réflexe (`--couches 0:K`) coûte **−67 %** par décision
à 8 couches.

**Manquant, et nommé deux fois** : la **poursuite** — garder un signal pour le rendre plus tard — n'est pas
une propriété de plomberie : elle demande un modèle (ou un adaptateur) **entraîné à retenir**. La
sonde linéaire dit que l'information n'est pas là ; la prochaine étape est donc un **entraînement**,
pas un câblage. C'est cohérent avec toute la ligne C8 : *ce qui manque n'est jamais le câblage,
c'est la tête.*

## 4. Protocole, pour rejouer

```bash
D=./drave-core/target/release/drave; M=models/Qwen2.5-0.5B-Q8_0.gguf
python3 -c "
import random; random.seed(7)
open('/tmp/periph2/bruit.txt','w').write('\n'.join(f'{random.uniform(-2,2):.4f}' for _ in range(64)))"
# A : pas indépendants
$D $M --entree signal:/tmp/periph2/bruit.txt --sortie /tmp/periph2/b_stat.f32 --ctx 8 --threads 8
# B : récurrent (l'historique reste dans le cache KV)
$D $M --entree signal:/tmp/periph2/bruit.txt --sortie /tmp/periph2/b_rec.f32 --ctx 64 --threads 8 --recurent
# C : le délai de l'interface
$D $M --entree signal:/tmp/periph2/bruit.txt --sortie /tmp/periph2/b_d8.f32 --ctx 8 --threads 8 --delai 8
python3 tools/peripherie_poursuite.py --signal /tmp/periph2/bruit.txt \
        --etats /tmp/periph2/b_stat.f32,/tmp/periph2/b_rec.f32,/tmp/periph2/b_d8.f32 --lags "0,8,-1"
```
