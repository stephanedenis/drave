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

## 3. Ce que ça change pour C8

**Acquis** : les **régions frontière existent** (le plan disait « rien ne sort » — c'était vrai) ;
le déterminisme est tenu au bit près, le délai est exact, et **chaque décision a son prix en
paires**, ce qui est la métrique du plan. Le réflexe (`--couches 0:K`) coûte **−67 %** par décision
à 8 couches.

**Manquant, et nommé** : la **poursuite** — garder un signal pour le rendre plus tard — n'est pas
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
