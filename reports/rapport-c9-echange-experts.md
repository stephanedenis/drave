# C9 sur un modèle routé : échanger les choix d'experts ne transfère RIEN d'utilisable

> Campagne : **cerveau** · expérience : `--echange experts` (la « variante la plus plausible » du § 6.8)
> Question : la latéralité entre deux instances jumelles ne gagnait rien en échangeant des **états**
> (`rapport-c9-lateralite.md`). La suite nommée était d'échanger des **choix d'experts** sur un
> modèle **routé** : là, les deux instances voient des choses différentes, donc leurs routages
> pourraient porter une information que l'autre n'a pas.
> Verdict : **non — et la mesure a d'abord menti.** Le premier essai donnait **×0,81** (une
> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont
> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend
> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait
> moins de mal que l'aléatoire » ne tient que **2 fois sur 3** (le sens inverse l'inverse : aléatoire
> ×0,94 contre réel ×1,26). Il n'y a **pas** de gain latéral.
> Date réelle : **2026-10-13, 12 h 57-13 h 20 HAE** (heure lue sur la machine)
> Protocole : Qwen3-30B-A3B (48 couches, 128 experts, 8 utilisés), `--ppl --ctx 512 --limit 32`,
> textes A/B/A2 tirés de trois fenêtres du même corpus ; routage **capturé** par
> `DRAVE_TRACE_EXPERTS` (+`DRAVE_TRACE_EXPERTS_ORDRE=1`) et **imposé** par `DRAVE_ROUTAGE_FORCER`
> (le mécanisme est neuf, voir § 1)

## 1. Le mécanisme, et son invariant (le socle de tout le reste)

La capture existait depuis toujours — `DRAVE_TRACE_EXPERTS` écrit `couche cle e0 e1 …`. Il manquait
son pendant : **imposer** ces choix. `DRAVE_ROUTAGE_FORCER=<fichier>` relit un tel fichier et
remplace la sélection du routeur, en gardant les **poids du modèle** pour les experts imposés
(c'est « et si le routeur avait choisi ceux-là ? », pas « et si on avait pris d'autres poids ? »).
Deux tests unitaires l'accompagnent (lecture du fichier, substitution sans appel au calcul).

**L'invariant, et il a fallu le rendre EXACT** : imposer à une instance **son propre** routage doit
rendre **la même perplexité au bit près**. Le premier essai donnait **37,2013 contre 37,1990**
(0,006 %) — parce que la trace **trie** les experts (« l'ordre de `select_nth` est arbitraire ») et
que l'accumulation flottante change avec l'ordre. `DRAVE_TRACE_EXPERTS_ORDRE=1` écrit l'ordre de
**sélection** : l'invariant est alors **exact** (37,2013 des deux côtés). Sans cela, l'effet mesuré
(±20 %) aurait baigné dans un artefact de 0,006 % — petit, mais du même genre que ce qu'on cherche.

## 2. Les mesures

### 2.1 Tout échanger (les 48 couches)

| condition (A sur son texte) | perplexité | ×réf |
|---|---:|---:|
| A avec **son** routage (référence) | **37,2013** | ×1,00 |
| A + le routage de **B** (autre texte) | **3 445,03** | **×92,6** |
| A + routage **aléatoire** | 13 958,96 | ×375 |
| A + routage de B **décalé d'une couche** | 37 825,73 | ×1 017 |

Échanger tout le routage **détruit** le calcul. Mais l'ordre est instructif : le routage de B est
**4× moins destructeur** que l'aléatoire et **11× moins** qu'un routage cohérent mais mal placé —
il porte donc bien un peu de structure commune (même langue, même corpus).

### 2.2 Échanger UNE couche (à la fois)

| couche échangée seule | perplexité | ×réf |
|---|---:|---:|
| **0** | 133,4957 | **×3,59** |
| 8 | 41,3360 | ×1,11 |
| 16 | 38,1149 | ×1,02 |
| 24 | 37,1813 | ×1,00 |
| 32 | 42,0470 | ×1,13 |
| 40 | 38,4055 | ×1,03 |
| **47** | **30,1705** | **×0,81** |

La couche **0** est de loin la plus sensible (le premier routage conditionne tout), et la
**dernière** donne… une amélioration de 19 %. **C'est là que la mesure a menti**, et c'est le § 3
qui le montre.

## 3. Les contrôles qui ont démonté le « gain »

| ce qu'on impose à la couche 47 de A | A (réf 37,2013) | A2 (réf 92,4832) | B (réf 84,6539) |
|---|---:|---:|---:|
| rien (son propre routage) | 37,2013 (×1,00) | 92,4832 (×1,00) | 84,6539 (×1,00) |
| **le routage de l'autre instance** | **30,1705 (×0,81)** | **135,0935 (×1,46)** | **107,0258 (×1,26)** |
| routage **aléatoire** | 35,4832 (×0,95) | 143,1992 (×1,55) | **79,4284 (×0,94)** |
| routage de l'autre **décalé** d'une couche | 37,9628 (×1,02) | — | — |
| un **troisième** texte (B2) | 34,6692 (×0,93) | — | — |

Ce que ça dit, et rien de plus :

* **le signe dépend du texte** : ×0,81 sur A, ×1,46 sur A2, ×1,26 sur B — un « gain » qui devient
  une perte de 46 % sur un autre texte n'est pas un gain ;
* **tout** routage différent à la dernière couche fait bouger la perplexité de ±20 à 50 %, y
  compris **aléatoire** (qui *améliore* A et B, et *dégrade* A2) : la dernière couche est un poste
  où le routage du modèle n'est pas optimal, mais ce n'est **pas** de la latéralité ;
* **l'ordre « réel < aléatoire »** (le seul indice qui aurait plaidé pour un transfert) tient sur A
  (0,81 < 0,95) et sur A2 (1,46 < 1,55) mais **s'inverse** sur B (1,26 > 0,94) : **2 sur 3**, donc
  non établi ;
* le contrôle **décalé** (×1,02) montre qu'un routage cohérent mais mal apparié est inerte — c'est
  le témoin qui dit que la mesure ne réagit pas à n'importe quoi.

## 4. Conclusion pour C9, et ce qu'elle ferme

**Échanger des choix d'experts entre deux instances qui voient des textes différents n'apporte
rien d'utilisable** : l'effet est dominé par la variabilité propre au texte, sans direction
stable — ce qui **recoupe** le « gain nul » déjà mesuré sur l'échange *d'états*
(`rapport-c9-lateralite.md`). La « variante la plus plausible » du plan est donc **mesurée et
négative**, et la latéralité de C9 n'a plus de piste ouverte dans cette direction.

Ce qui reste ouvert, et ce n'est plus la même question : **la dernière couche** est un poste où le
routage du modèle n'est pas optimal (tout routage différent y change la perplexité de ±20-50 %).
C'est une piste d'**architecture** (le routage final), pas de latéralité — et elle se mesurerait sur
un modèle entraîné, pas sur un modèle téléchargé.

## 5. Ce qui a été écrit dans le moteur (et comment le refaire)

```bash
# capturer un routage, dans l'ordre de sélection (indispensable pour l'invariant exact)
DRAVE_TRACE_EXPERTS=/tmp/rout.txt DRAVE_TRACE_EXPERTS_ORDRE=1 drave <modele> --ppl <ids> …
# imposer un routage (le sien → perplexité EXACTE ; celui d'un autre → la mesure de C9)
DRAVE_ROUTAGE_FORCER=/tmp/rout.txt drave <modele> --ppl <ids> …
```
Les deux variables sont déclarées dans `VARS_LUES` (le test du dépôt l'exige), le lecteur de fichier
et la substitution ont leurs tests unitaires, et l'invariant est verrouillé par
`tools/porte-echange-experts.sh`.
