# La décision par couche : à 20-56 % de densité, le dense gagne (2 %) ; le push est pour les couches creuses

> Mesure du 24/10/2026, Qwen2.5-0.5B Q8_0 (24 couches, 896 cachés), 255 jetons notés, contexte 256,
> 20 fils, perplexité et temps par le binaire du dépôt (`--ppl`). La densité par couche vient de
> [`rapport-analyse-flux.md`](rapport-analyse-flux.md) (le même modèle, le même contexte).

## La question

Le moteur a **deux chemins** : le **push** (les listes valuées, l'AER) et le **pull** (la matrice dense). Le
croisement mesuré est à **~22 % de densité** ([`rapport-croisement-push-pull.md`](rapport-croisement-push-pull.md)
§1, corrigé le 27/09) : en dessous, le push ; au-dessus, le dense. Or la densité **varie du simple au triple selon
la couche** — la décision ne peut donc pas être une propriété du modèle, elle doit être une propriété de la
**couche**. Reste à savoir ce que cette table prédit, et si la mesure le confirme.

## La table

Densité par couche (0,5 B, contexte 256) et chemin prédit par le croisement de 22 % :

| couche | densité | chemin prédit |
|---|---:|---|
| **9** | **20,1 %** | **push** |
| 0 | 25,9 % | dense |
| 4 | 26,7 % | dense |
| 3 | 28,8 % | dense |
| 8 | 29,2 % | dense |
| 6 | 40,5 % | dense |
| 5 | 45,6 % | dense |
| 1 | 56,3 % | dense |

*Prédiction : **1 couche sur 24** passe par le push ; les 23 autres par le dense.*

## La mesure

Deux exécutions du même texte, même contexte, mêmes fils — seul le chemin change :

| | perplexité | temps | ms/jeton |
|---|---:|---:|---:|
| **push** (défaut) | 28,4015 | 9,4 s | 36,9 |
| **dense** (`--dense`) | **28,4015** | **9,2 s** | 36,1 |

- **La perplexité est IDENTIQUE au chiffre près** (28,4015) : les deux chemins font le **même** calcul — c'est le
  contrôle qui autorise à comparer les temps.
- **Le dense est 2 % plus rapide** (9,2 contre 9,4 s) : la direction prédite par la table (23 couches sur 24 au
  dense) est celle qu'on observe.
- L'écart reste **petit** : 2 % sur un total, pour une décision qui, couche par couche, ne changerait que la
  neuvième.

## Ce que ça dit

- **La table par couche est cohérente avec la mesure** : sur ce modèle et ce contexte, le dense est le bon défaut,
  et le push ne concerne qu'une couche (la 9) — dont le gain propre n'est pas isolé ici.
- **Le « push gagne » n'est pas une propriété du modèle** : à 20-56 % de densité, c'est le dense ; le push paie
  dans les régimes plus creux (la vision mesure **17,9 %** sur ce modèle à **512** jetons — la densité baisse avec
  le contexte, et c'est là que la liste reprend l'avantage).
- **Le défaut du moteur (push) n'est pas le meilleur pour ce cas** : l'écart est de 2 %, dans le bruit d'une mesure
  unique, mais la direction est celle de la table — et elle ne coûte rien à suivre.

## Ce que ce résultat ne dit pas

- **Une seule taille** (0,5 B Q8_0) et **un seul texte** ; les 3 B et 14 B, et les textes longs, ne sont pas
  mesurés ici.
- Les temps sont **globaux** (le `--ppl` ne donne pas le temps par couche) : la prédiction par couche est
  analytique, pas mesurée couche par couche.
- L'écart de 2 % est **à la limite du bruit** (une seule exécution par chemin) ; il faudrait trois passages pour
  l'affirmer au-delà de la direction.
- La densité de référence vient d'un rapport **antérieur** : elle n'a pas été re-mesurée dans cette exécution, et
  ce rapport dit « croisement ~10 % » là où le rapport de croisement, corrigé, dit **22 %** — c'est la valeur
  corrigée qui fait foi ici (la mention à 10 % est périmée).
