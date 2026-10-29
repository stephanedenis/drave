# R06 — Tête de relecture (confiance et contradiction)

> **Statut** : partiel · **Priorité** : P2 · **Programme** : R · **Dépend de** : R03, R21, R22
> **Ligne de roadmap** : R0.4 · **Résultat** : [rapport-r06-relecture.md](../../../reports/rapport-r06-relecture.md) — **triple négatif** : relire plus ne change rien (0/249, 0/84), le déclencheur par refus récupère 2/9 et en manque 15, le recouvrement ne sépare pas. À réécrire autour du **changement de modalité** ; la porte « gist » (R21) n'est pas testable.
> **Résumé** : Déclencher une relecture ciblée quand la réponse est incertaine ou contredit une autre région.
> **Glossaire** : [relecture](../../theorie/glossaire/entrees/relecture.md) · [gist](../../theorie/glossaire/entrees/gist.md).

## Le besoin

La régression est une partie de la lecture humaine : on revient sur ce qu'on n'a pas compris. Le modèle causal ne revient jamais ; il faut un déclencheur explicite, sinon la relecture n'existe pas.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une réponse candidate, les régions lues et l'état de confiance |
| **sortie** | un drapeau de relecture, la région à relire et la raison |
| **coût** | la relecture doit coûter moins que le gain d'exactitude |
| **trace** | le déclenchement, la région et le gain sont tracés |

## Ce qui est mesuré

- précision/rappel des relectures nécessaires
- gain d'exactitude par relecture
- coût supplémentaire (événements, octets)

## Portes

1. le gain d'exactitude dépasse le coût sur 3 types
2. pas de fausse alerte sur les documents faciles
3. la relecture récupère une information que le gist a perdue

## Contrôles négatifs

- toujours relire ; ne jamais relire ; déclencheur aléatoire
- relecture de la même région (sans information nouvelle)

## Ce qui pourrait le rendre faux

- le déclencheur apprend la longueur du document, pas l'incertitude
- les étiquettes de contradiction sont bruitées
- la relecture lit la réponse gold

## Étapes

1. définir les signaux de confiance (accord entre régions, couverture, contradiction)
2. collecter un petit jeu de relectures nécessaires
3. évaluer le déclencheur contre les trois contrôles
4. brancher dans le contrôleur ; écrire la fiche

## Documents à écrire

- `tete-relecture.md` (signaux, déclencheur, porte, dans `docs/implantation/`)
- mettre à jour R0.4

## Voir aussi

- [Programme R](../roadmap.md#r0--le-lecteur-v0-système-sans-entraînement)
- [Analyse, § 5.3](../../theorie/lecture-rapide.md#53-la-politique-de-lecture-l3--le-cœur-du-sujet)
