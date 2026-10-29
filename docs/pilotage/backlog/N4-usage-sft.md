# N4 — Usage : SFT, service, sûreté

> **Statut** : partiel · **Priorité** : P1 · **Programme** : N · **Dépend de** : — · **Plafonné par** : N2 (la qualité du student)
> **Ligne de roadmap** : N4 · **Fiche de résultat attendue** : rapport-n4-usage.md (à créer dans `reports/`)
> **Résumé** : Rendre le natif utilisable : répondre, s'arrêter, suivre une consigne, servir sur une API.
> **Glossaire** : [SFT](../../theorie/glossaire/entrees/sft.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [jeton](../../theorie/glossaire/entrees/jeton.md).

## Le besoin

Le service tourne (69 octets, 611 ms) mais le SFT mémorise : 24/24 vus, 0/4 tenus. Sans tenue à l'écart, il n'y a pas d'assistant.

## L'état

Génération greedy 160 octets (12 cohérents), service Python/Rust, jeton 401/200, pas d'alignement SFT.

## La porte

≥ 80 % des instructions tenues sur des documents/consignes non vus ; refus explicite ; pas de fuite.

## Contrôles négatifs

- vus/non vus ; consigne impossible ; réponse sans document
- même budget de calcul

## Prochaine action

Construire un jeu SFT avec partage par document, entraîner, évaluer tenu à l'écart ; écrire la fiche.

## Voir aussi

- [Programme N](../roadmap.md#programme-n--le-natif-drvm-drave-n0-distillation)
- [Programme R, R3](../roadmap.md#r3--la-restitution)
