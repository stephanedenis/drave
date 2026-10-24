# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
tableau, pas la première tuile), et borne **chaque** porte à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (47 portes ; certaines entraînent de petits modèles, d'autres utilisent les GPU).

## Où est le registre (et comment lire le verdict)

Le registre n'est **pas** à la racine : il est écrit dans le dossier des journaux, par défaut
`/tmp/portes-<date>-<heure>/registre.txt` (variable `JOURNAUX`). Chaque ligne vaut :

```
nom-de-la-porte   code-de-sortie   durée-en-secondes
```

On lit le verdict **par le code**, jamais par les marqueurs `✅`/`❌` du source, jamais à travers un tube :

```bash
JOURNAUX=/tmp/portes-1019-13h30   # le dossier affiché au lancement
awk '$2 != 0' "$JOURNAUX/registre.txt"
```

Une porte **verte** a le code `0`. Une porte **rouge** a un code non nul (`1` échec, `124` borne dépassée).

## Les rouges connues

Deux rouges **structurelles** sont connues et tolérées : **`porte-indice`** et **`porte-melange`**. Toute **autre**
rouge est une **régression** et se corrige avant de continuer. *(Une rouge `124` est une porte trop lente ou
bloquée : ce n'est pas un échec de la porte, c'est le délai — relancer la porte seule avec un `DELAI` plus grand.)*

## Lancer un sous-ensemble

```bash
PORTES="tableaux registre vision" DELAI=600 bash tools/toutes-les-portes.sh
```

Le filtre est un `grep` sur le nom du fichier (`*"$f"*`). Utile pour les portes documentaires (quelques secondes) ;
la passe complète reste la règle de fin de cycle.

## Ne pas fausser la passe

- **Les portes et une mesure GPU ne cohabitent pas** : lancer un modèle qui occupe 28 Go de VRAM pendant une passe
  fait attendre ou échouer les portes qui utilisent les cartes (`porte-audit-drapeaux`, `porte-vision`,
  `porte-*moteur`). Faire la passe **seule**, puis les mesures.
- **Les portes de temps** (`porte-delais`, `porte-flux`, `porte-topologie`) mesurent des latences : les lancer
  seules si un chiffre de temps doit être **interprété**. La passe complète est faite pour le **verdict**, pas pour
  le chronomètre.
- Le journal de chaque porte est conservé dans `$JOURNAUX/<porte>.log` : en cas de rouge, `tail -15` sur ce fichier
  donne la raison, pas le marqueur.

## Avant de commiter

La passe complète + `python3 tools/revue_documentation.py` + `porte-tableaux` : c'est le triplet de clôture d'un
sous-chantier (voir [`rangement.md`](rangement.md)).
