> Campagne : **campagne-benefices** · expérience **19**
> Titre : 19. La parcimonie imposée, sur 24 réglages : le k-WTA écrase le seuil, encore
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 19. La parcimonie imposée, sur 24 réglages : le k-WTA écrase le seuil, encore

Qwen2.5-0.5B Q8_0, 256 jetons, ctx 512, deux familles de réglages et les deux
chemins d'exécution. **Seules les colonnes déterministes sont utilisables** :
`acttopk1000dense` et `actthresh0dense` sont *la même configuration* et donnent
12,1 et 22,6 tok/s — le bruit de temps vaut ×2 sous cette charge de fond (67-84).
Les PPL, les événements et les paires, eux, sont exacts.

| réglage | PPL (dense / listes) | M événements/jeton | **PPL à −30 % d'événements** |
|---|---|---:|---:|
| aucune parcimonie | 17,43 / 17,41 | 354 | — |
| seuil 0,1 % | 17,34 / 17,31 | 344 | −2,6 % d'évts |
| seuil 0,5 % | 17,84 / 17,87 | 312 | **+2,3 % de PPL** |
| seuil 1 % | 21,01 / 20,53 | 281 | **+20 %** |
| seuil 2 % | 29,50 / 29,48 | 229 | **+69 %** |
| seuil 5 % | **3 176** / 3 714 | 151 | effondrement |
| k-WTA 85 % | 17,69 / 17,40 | 302 | −15 % |
| k-WTA 80 % | 17,58 / 17,43 | 284 | −20 % |
| k-WTA 70 % | 18,11 / 18,92 | 248 | **+4 % pour −30 % d'évts** |
| k-WTA 50 % | 28,36 / 30,56 | 177 | +63 % |

**Le résultat du dépôt se reproduit au chiffre près, un autre jour, sous une autre
charge : le seuil absolu est inutilisable, le k-WTA tient.** À −30 % d'événements,
le seuil coûte **+69 %** de perplexité là où le k-WTA coûte **+4 %** — un facteur 17.

### 19 bis. Quelle projection tolère d'être creusée ? Le tableau qui manquait

Le top-k du moteur peut viser **une projection à la fois** (`--topk-o`, `--topk-down`,
`--topk-gate`, `--topk-up`). Même modèle, mêmes 256 jetons, chemin par listes :

| projection creusée | 70 % gardé | 50 % | 30 % | événements au top-k 30 % |
|---|---:|---:|---:|---:|
| `o` (sortie d'attention) | **−0,3 %** | +3,3 % | **+17 %** | 86,95 G (−3,8 %) |
| `down` (descente FFN) | +0,5 % | +3,5 % | **+16 %** | 71,98 G (−20 %) |
| `gate` (porte FFN) | **−1,9 %** | +11 % | **+101 %** | 71,83 G (−20 %) |
| `up` (montée FFN) | +2,3 % | +16 % | **+75 %** | 71,83 G (−20 %) |

*(PPL de référence sans creusage : 17,4084.)*

**Trois enseignements, et ils orientent l'entraînement.**

1. **Le creusage léger AMÉLIORE la perplexité** — `gate` à 70 % gagne 1,9 %, `o`
   0,3 %. La même chose était visible au § 19 sur le seuil à 0,1 %. La parcimonie
   n'est pas qu'un coût : à faible dose, c'est une régularisation.
2. **Les deux projections qui portent une activation CALCULÉE (`o`, `down`) sont
   les plus tolérantes** (+16-17 % à 30 % gardés) ; celles qui lisent le **flux
   résiduel** (`gate`, `up`, et `q/k/v` par construction) s'effondrent (+75 %,
   +101 %). Autrement dit : **ce n'est pas la projection qui compte, c'est ce
   qu'elle lit** — creuser le flux résiduel demande que le modèle ait appris à y
   vivre.
3. **Chaque projection ne pèse que ~20 % des événements** : creuser une seule
   d'entre elles ne peut pas rendre l'architecture gagnante ; c'est le top-k
   **global** (`--act-topk`) qui met tous les événements à l'échelle du taux gardé
   (354 → 248 M au § 19).

C'est exactement pourquoi le k-WTA des modèles entraînés cette nuit porte sur
**toutes les couches linéaires** : le flux résiduel est la partie difficile, et
c'est celle qu'un modèle nativement événementiel doit apprendre en premier.

**Et une nuance que la mesure ajoute** : dans le chemin **dense**, la parcimonie ne
réduit **aucune lecture** (495,4 M paires/jeton dans tous les cas) — elle ne fait
que mettre à zéro des activations. Ce n'est que dans le chemin **par listes** que
les événements baissent (354 → 248 M). Autrement dit, **la parcimonie imposée ne
paie que si le moteur exécute en listes** ; en dense, elle ne coûte que la qualité.

**Correction du 9 octobre : les deux colonnes de ce tableau ne comparent pas la
même arithmétique.** En mode `--dense`, le moteur *emprunte* les blocs Q8_0 du
fichier tels quels (schéma d'échelle de llama.cpp) ; en mode `--push`, il
reconstruit ses propres listes depuis les poids déquantifiés (notre schéma). Même
corpus, même modèle, aucune parcimonie : **17,4315 emprunté · 17,4084 reconstruit ·
17,4084 en listes**. L'écart entre les colonnes dense et listes du tableau
ci-dessus (0,1 à 0,5 %) vient donc **de l'encodage des poids, pas du chemin
d'exécution** — et la variable d'environnement `DRAVE_SANS_EMPRUNT=1` le prouve :
elle ramène le dense sur les listes, au chiffre près, puis au **bit près** (§ 22).

---
