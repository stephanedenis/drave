# C8 — transfert d'un corpus à un AUTRE : la tête lit quand même l'état (÷1 730)

> Campagne : **cerveau** · expérience : tête entraînée sur le corpus de campagne, testée sur un
> corpus de **prose** qu'elle n'a jamais vu
> Question : tous les morceaux des expériences précédentes venaient du **même document**. Une tête
> entraînée sur un corpus sait-elle lire l'état d'un **autre corpus** ? Autrement dit : le réflexe
> apprend-il une **lecture** (transférable) ou une **clé de domaine** (locale) ?
> Verdict : **les deux, et la lecture domine** — sur un morceau de prose tenu à l'écart, la tête
> empruntée rend **363 649,14** ; la tête entraînée sur **le corpus de campagne** rend
> **210,21** (**÷1 730**) ; la même tête entraînée **dans** le corpus de prose rend **81,63**
> (**÷4 456**). Le modèle complet vaut **8,3650** sur ce morceau : le transfert reste à
> **×25,1** du modèle, la version du domaine à **×9,8**. **Le changement de corpus coûte un
> facteur 2,6**, pas l'effondrement qu'on pouvait craindre.
> Date réelle : **2026-10-10 15:10 HAE** · graine fixée (`--graine 0`), morceau de test **exclu**
> de l'entraînement dans les deux cas.
> Protocole : `tools/c8_corpus.sh` sur `ids_b2_prose.txt` (30 morceaux) et sur `ids_0.5B-Q8.txt`
> (40 morceaux), puis `tools/c8_entrainer_tete.py --train … --test …`.

## 1. Les chiffres

Test : **morceau 29 de la prose**, 1 024 jetons, jamais vu par aucune des deux têtes.

| tête (adaptateur 896×896) | entraînée sur | perplexité | vs modèle complet (8,3650) |
|---|---|---|---|
| **empruntée** (identité, moteur) | — | 363 649,1382 | ×43 470 |
| **entraînée** | **corpus de campagne**, 30 morceaux | **210,2077** | **×25,1** |
| **entraînée** | **prose**, 28 morceaux | **81,6323** | **×9,8** |

**Ce que ça dit** : la lecture apprise sur un corpus **se transporte** à un autre (÷1 730 sur la
tête empruntée), et le domaine ajoute **×2,6**. Le réflexe n'est donc pas une clé de domaine : il
apprend à **lire un état intermédiaire**, ce qui est précisément ce que C8 demandait.

## 2. Le protocole, et ce qu'il exclut

- les deux corpus sont **tokenisés par le même tokenizer** (celui du modèle) : les identifiants sont
  comparables, et c'est une condition du test — un autre tokenizer aurait mêlé deux questions ;
- le morceau de test (29) est **exclu de la liste d'entraînement** dans les deux cas, et la liste
  est construite **par un programme**, jamais à la main (une première tentative avait laissé le
  morceau de test *dans* l'entraînement : 1,5978 de perplexité, « mieux » que le modèle complet —
  c'était de la mémorisation, voir `rapport-c8-generalisation.md` § 3) ;
- la **graine est fixée** : sans elle, deux exécutions identiques donnaient 2 632 puis 9 056 ;
- la meilleure époque est **restaurée** avant la lecture du tableau (le surapprentissage arrive à
  l'époque 2 dans les deux cas).

## 3. Ce que ça ne dit pas

- **deux corpus, un seul sens de transfert** : on a mesuré campagne → prose. Le sens inverse
  (prose → campagne) n'est pas mesuré, et rien ne dit que le transfert est symétrique ;
- **les deux corpus sont du français** : le transfert **inter-langue** n'est pas mesuré, alors que
  le dépôt a des corpus multilingues (`ids_b2_multilingue.txt`) — c'est la question suivante ;
- **la tête reste linéaire** (adaptateur) et **le chemin reste à 16 couches** : la variante
  non linéaire a été *pire* à cette échelle (272 contre 51), faute de réglage ;
- **la latence** du chemin court est mesurée à part (**×1,54** en génération), mais pas avec la
  tête entraînée en place (le matmul 896×896 est négligeable devant une couche, mais ce n'est pas
  mesuré).

## 4. Protocole, pour rejouer

```bash
IDS=/tmp/campagne24/ids_b2_prose.txt T=/tmp/c8-prose tools/c8_corpus.sh 30 1024 16
PY=/home/stephane/gpu-env/bin/python
A=$(python3 -c "print(','.join(f'/tmp/c8-corpus/etat-m{i}' for i in range(0,31) if i != 7))")
P=$(python3 -c "print(','.join(f'/tmp/c8-prose/etat-m{i}' for i in range(0,29)))")
CUDA_VISIBLE_DEVICES=0 $PY tools/c8_entrainer_tete.py --train "$A" \\
   --test /tmp/c8-prose/etat-m29 --modele models/Qwen2.5-0.5B-Q8_0.gguf --limite 1024 \\
   --epoques 20 --graine 0          # transfert  → 210,21
CUDA_VISIBLE_DEVICES=0 $PY tools/c8_entrainer_tete.py --train "$P" \\
   --test /tmp/c8-prose/etat-m29 --modele models/Qwen2.5-0.5B-Q8_0.gguf --limite 1024 \\
   --epoques 20 --graine 0          # dans le domaine → 81,63
```
