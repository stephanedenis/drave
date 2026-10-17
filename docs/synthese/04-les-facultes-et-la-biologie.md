# 4. Les douze facultés et la biologie

## Ce que Drave cherche à donner à un modèle

![Les facultés](schemas/facultes.svg)

| faculté | ce que c'est | ce qui est mesuré |
|---|---|---|
| **C1 topologie** | couper et répartir | huit coupes, une seule perplexité (113,0068) |
| **C2 cycle** | boucler sur l'état | le pas d'état est expansif (λ ≥ 3,7e4) : à entraîner |
| **C3 horloges** | des régions à leur rythme | résultat identique, coût différent |
| **C4 délais** | des retards entre régions | la perplexité se dégrade, jamais d'un coup |
| **C5 bus** | un canal riche | l'état transfère son contenu (23,4 %) |
| **C6 mémoire** | épisodique, de travail | la mémoire aidée par le texte gagne (+157 %) |
| **C7 sommeil** | consolider | la consolidation « sommeil » +12,56 % hors domaine |
| **C8 réflexe** | répondre vite | 0 % à 16 couches, 8,3 % à 20, 30 % distillé |
| **C9 ponts** | relier deux régions | 448 fibres : +2,81 %, octets ÷1,8 |
| **C10 budgets** | dépenser peu | le débit tient, la qualité se dégrade selon le budget |
| **C11 pannes** | tenir debout | la perte est progressive, jamais un effondrement |
| **C12 trace** | se regarder | traces par couche, rejeu, comparaison |

## Les neuf apports de la biologie

| apport | l'idée biologique | ce que le dépôt en a fait |
|---|---|---|
| **E1 poids log-normaux** | la distribution des synapses | initialisation log-normale, mesurée à l'usage |
| **E2 croissance** | les connexions poussent | masque qui se densifie pendant l'entraînement |
| **E3 Dale** | un neurone est excitateur ou inhibiteur | signes figés, ratio E/I imposé |
| **E4 équilibre** | l'excitation et l'inhibition s'équilibrent | ratio de signes, mesuré |
| **E5 distillation** | apprendre d'un maître | *ne reproduit pas sa configuration publiée*, mais une variante stable bat le témoin |
| **E6 signes figés** | le signe d'une synapse ne change pas | poids à 1 bit, décalages et additions |
| **E7 k-WTA** | peu de neurones actifs | 25 % gardés : paires ÷3,97, perplexité inchangée |
| **E8 topologie innée** | on naît avec un plan | masque initial, mesuré contre le hasard |
| **E9 homéostasie** | l'activité se régule | ×0,6 du delta : m32 −8,75 %, hors domaine −0,58 % |

## La règle qui tient tout

**Une faculté sans mesure n'entre pas dans le tableau.** Chaque ligne ci-dessus renvoie à une fiche
(`reports/`) et à une porte (`tools/porte-*.sh`). Et quand une mesure contredit l'intuition, c'est la
mesure qui est écrite — E5 en est l'exemple : la fiche publiée n'a pas été reproduite, et c'est consigné
à côté de ses chiffres.
