# C2 — la récurrence (boucle sur soi) : la boucle existe, elle est bornée… et elle DÉGRADE la lisibilité

> Campagne : **cerveau** · expérience : une région consomme sa propre sortie du pas précédent
> Question (le plan, § C2) : « une région peut consommer sa propre sortie du pas précédent (état
> explicite par région) » — et le validateur de topologie **refuse encore un cycle**. La boucle
> est-elle utile ?
> Verdict : **la boucle est implémentée, bornée, sans coût — et elle NUIT.** Avec un poids de
> rétroaction α, la lecture du signal **présent** tombe de R² **0,906** (α = 0) à **0,112**
> (α = 0,5) et **0,125** (α = 1,0) ; la lecture du signal d'il y a 8 pas passe de **−0,350** à
> **−4,873**. La boucle ne crée pas de mémoire : elle ajoute au signal un **écho de la
> transformation du réseau**, qui noie l'information d'entrée au lieu de la conserver.
> Date réelle : **2026-10-10 20:07 HAE** (heure lue sur la machine).
> Protocole : `drave --entree signal:F --recurrence α --recurent --sortie G`, puis
> `tools/peripherie_poursuite.py` (lecture apprise, 64 pas de bruit). Porte :
> `tools/porte-recurrence.sh`.

## 1. Ce qui est implémenté

`--recurrence α` : au pas `t`, l'entrée reçoit **en plus** `α × h(t−1)`, où `h(t−1)` est la sortie
du pas précédent. C'est exactement la boucle que le plan décrit — une région qui consomme sa propre
sortie — et elle est :

- **exacte à α = 0** : la sortie est identique **au bit près** à l'exécution sans le drapeau (le
  zéro est exprimable, leçon `--attn-sinks` appliquée d'avance) ;
- **déterministe** : deux exécutions identiques rendent des fichiers identiques ;
- **gratuite en paires** : la rétroaction ne traverse aucune couche de plus (357,8 M paires par
  décision avec et sans) ;
- **bornée** : α hors de [0, 8] est **refusé** (code 2) — une récurrence qui ne converge pas ne doit
  pas rendre un chiffre.

## 2. Ce qu'elle FAIT : elle dégrade, et la mesure dit pourquoi

Lecture apprise (ridge, moitié des pas pour apprendre) de l'état de sortie vers le signal injecté :

| α | lecture de `v[t]` (présent) | lecture de `v[t−8]` (mémoire) |
|---|---|---|
| **0** (pas de boucle) | **R² +0,906** | R² −0,350 |
| 0,25 | R² −0,674 | R² −1,269 |
| 0,5 | R² +0,112 | R² −2,215 |
| 1,0 | R² +0,125 | R² −4,873 |

**La dégradation est monotone en α, et elle touche d'abord le PRÉSENT** : dès α = 0,25, le signal
courant n'est plus lisible du tout (−0,674). Autrement dit, la boucle **détruit** l'information
d'entrée plus vite qu'elle ne pourrait la conserver.

**Le mécanisme est simple et il vaut d'être écrit** : `h(t−1)` n'est pas le signal d'entrée, c'est
**ce que le réseau en a fait** — une transformation non linéaire qui mélange le signal courant,
l'état interne et le bruit numérique. Le réinjecter ajoute un écho qui *ressemble* à un signal sans
en être un : la lecture ne peut plus séparer l'entrée de son écho, et le passé n'y gagne rien (il
n'y est pas davantage).

## 3. Ce que ça dit pour C2, et ce que ça ne dit pas

**Ce que ça dit** : supporter la récurrence (l'interface, l'ordonnancement, l'état par région) est
une chose ; **en tirer quelque chose en est une autre**. Une boucle *non entraînée* sur un réseau
*feed-forward* ne crée pas de mémoire — elle crée un écho. C'est cohérent avec la ligne C8 du même
jour : ce qui manquait n'était pas le câblage (une boucle), c'était la **structure** (un tampon lu
directement : R² 1,000) ou l'**entraînement** (une tête par profondeur).

**Ce que ça ne dit pas** :
- **une récurrence entraînée** est une autre histoire : ici le poids α est fixé après coup et le
  réseau n'a jamais appris à vivre avec sa propre sortie. Les réseaux récurrents entraînés savent
  le faire — c'est précisément ce que l'entraînement apporte ;
- **la projection d'entrée est crue** : on réinjecte l'état **entier** (896 canaux) dans l'entrée
  avec un seul scalaire ; une récurrence apprise aurait une **matrice** de rétroaction, et c'est
  elle qui porterait l'information ;
- **le cycle à DEUX régions** (la validation du plan : « un cycle à deux régions, comparé à une
  implémentation de référence sur 4 pas de temps ») n'est pas mesuré ici : le validateur de
  topologie refuse encore les cycles dans un graphe, et cette fiche ne lève pas ce refus — elle
  mesure la boucle locale, qui est ce qu'on peut mesurer sans lui.

## 4. Protocole, pour rejouer

```bash
D=./drave-core/target/release/drave; M=models/Qwen2.5-0.5B-Q8_0.gguf
python3 -c "
import random; random.seed(11)
open('/tmp/rec/b64.txt','w').write('\n'.join(f'{random.uniform(-2,2):.9g}' for _ in range(64)))"
for A in 0.0 0.25 0.5 1.0; do
  $D $M --entree signal:/tmp/rec/b64.txt --sortie /tmp/rec/rec$A.f32 --ctx 64 --threads 8 \
     --recurent --recurrence $A > /dev/null 2>&1
  python3 tools/peripherie_poursuite.py --signal /tmp/rec/b64.txt --etats /tmp/rec/rec$A.f32 \
     --delai 0 --lags "0,8,-1" | grep "lecture"
done
tools/porte-recurrence.sh        # les invariants seuls (~1 min)
```
