> Campagne : **campagne-benefices** · expérience **13**
> Titre : 13. La tête restreinte, sur deux modèles de plus
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 13. La tête restreinte, sur deux modèles de plus

`--tete-restreinte` sur une tâche à trois étiquettes (positive / negative /
neutral), 64 jetons, deux tours entrelacés, sous charge 41-46 :

| modèle | tête complète | **tête restreinte** | gain |
|---|---:|---:|---:|
| Qwen2.5-0.5B | 17,35 / 15,73 tok/s | **21,40 / 23,85** | **×1,36** |
| r1-distill-1.5B | 4,66 / 8,45 tok/s | **6,27 / 7,08** | ×1,11 (bruité) |

Et le contrôle qui compte, sur les mêmes journaux : la sortie de la tête
**restreinte** ne contient que les mots autorisés — les occurrences d'étiquettes
passent de **10 à 67** (0,5 B) et de **7 à 67** (1,5 B), parce que le modèle ne
*peut pas* produire autre chose. La tête complète, elle, écrit du texte libre.

**Ce qui est robuste ici, c'est la garantie, pas le débit** : le gain de vitesse
dépend du rapport tête/corps du modèle (×1,36 sur un 0,5 B, à peine sur un 1,5 B
où d'autres postes dominent), alors que la contrainte de sortie, elle, est
**structurelle** — et c'est la seule ligne du verdict où l'architecture gagne sans
dépendre ni du modèle ni de la machine.

**Et sur un modèle plus gros que la RAM, la tête restreinte ne gagne RIEN** — la
mesure qui manquait, faite le 9 octobre sur gpt-oss-120B (63 Go, MXFP4, disque),
même invite, 64 jetons :

| passe (gpt-oss-120B, 20 threads) | 64 jetons | tok/s | conditions |
|---|---:|---:|---|
| tête complète, 1er essai | **aucun jeton en 3 600 s** | — | une autre passe lisait les mêmes 63 Go |
| tête restreinte (3 jetons) | 163,9 s | 0,39 | cache chaud, lecteur concurrent |
| tête complète, 2e essai | 171,9 s | 0,37 | cache chaud, lecteur concurrent |
| tête restreinte, 2e essai | **71,0 s** | **0,90** | cache chaud, **seule** |

**Les durées ne sont pas comparables entre elles** (la lecture concurrente du même
fichier les domine : 3 600 s contre 164 s pour la même tâche), mais une borne,
elle, ne dépend pas de la charge : la couche de sortie de ce modèle pèse
**0,58 G de poids par jeton sur 4,93 G de paires lues, soit 12 %**. Restreindre la
tête ne peut donc pas rapporter plus de **×1,12** ici — et l'essentiel est dans les
**experts** (3 583 M paires/jeton), que la tête restreinte ne touche pas.

Le diagnostic de colonnes, imprimé par la même passe, va dans le même sens :
94,8 % des coordonnées d'entrée de la tête sont vivantes, donc un stockage par
colonnes n'éviterait que **5 %** de la matrice. **Sur un MoE plus gros que la RAM,
le levier n'est ni la tête ni sa disposition : c'est le routage des experts.**

*(Rappel de méthode : le premier essai « tête complète » a été tué par le délai de
3 600 s **pendant** qu'une mesure de perplexité lisait le même fichier de 63 Go —
c'est un résultat sur la contention, pas sur la tête. Les deux passes à cache
chaud donnent ×1,05, très en dessous de la borne de ×1,12.)*

---
