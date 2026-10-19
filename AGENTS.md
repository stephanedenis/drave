# Directives de l'agent — Drave Natif

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la mission, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/agent/`](docs/agent/)
> (tableau § 3). L'**état courant** est dans [`docs/en-cours.md`](docs/en-cours.md) ; le récit daté dans
> [`journal/`](journal/).

## 1. La mission (l'essentiel)

Deux **étages** d'architecture, dans cet ordre, et **on ne passe pas au suivant tant que le précédent est perfectible** :

1. **Les modules d'ENTRÉE et de SORTIE linguistiques** — priorité absolue. Ils doivent lire et produire **toutes**
   les langues, dialectes et styles, dans les registres **techniques, littéraires, juridiques, quotidiens**. On les
   juge en **qualité de traducteur** (restitution à l'identique, et traduction du sens). On ne « déclare complet »
   que sur des **chiffres** qui couvrent langues, dialectes, styles et domaines.
2. **Le module de pensée abstraite, indépendant de la langue** — **seulement après**. Il ne peut pas être bâti sur
   une entrée-sortie qui n'est pas fiable.

**Le temps est un plancher, pas un plafond** (*carpe diem*) : on s'arrête quand l'étage est **fait, mesuré et
écrit**, pas quand une échéance passe. Détail : [`docs/agent/mission.md`](docs/agent/mission.md).

**Vocabulaire** : *couche* = **couche de neurones** (couche 1, 2…, un réseau) ; *étage* = **niveau d'architecture**
(étage 1 entrée-sortie, étage 2 pensée) ; *jeton* = **unité du tokeniseur** d'un modèle, **jamais** la
**représentation sémantique neutre (RSN)**, dont les éléments sont des **unités de sens**. Le nom historique
« couche commune entrée-sortie » se lit « étage entrée-sortie ». Voir [`docs/glossaire.md`](docs/glossaire.md).

## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/agent/rangement.md`](docs/agent/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/en-cours.md`. *Sans contrôle négatif, ce n'est pas un résultat.* →
   [`docs/agent/resultats.md`](docs/agent/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   structurelles tolérées : **`porte-indice`** et **`porte-melange`** ; toute autre est une régression. →
   [`docs/agent/portes.md`](docs/agent/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/agent/rangement.md`](docs/agent/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/genealogie-des-langues.md`](docs/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/agent/miroir.md`](docs/agent/miroir.md)
7. **Ne jamais bloquer** sur une question humaine : la consolider dans `docs/en-cours.md` et **continuer** ;
   répondre soi-même si ce n'est pas la vision ou la philosophie. → [`docs/agent/ressources.md`](docs/agent/ressources.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la mission, les priorités, la philosophie | [`docs/agent/mission.md`](docs/agent/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/agent/resultats.md`](docs/agent/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/agent/rangement.md`](docs/agent/rangement.md) |
| lancer ou lire les portes | [`docs/agent/portes.md`](docs/agent/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/agent/miroir.md`](docs/agent/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/agent/ressources.md`](docs/agent/ressources.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/en-cours.md`](docs/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/glossaire.md`](docs/glossaire.md) |
| la carte de la documentation | [`docs/README.md`](docs/README.md) |

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/en-cours.md`](docs/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les deux rouges structurelles connues** ;
- la revue de documentation passe, et les liens résolvent.
