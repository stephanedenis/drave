# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
[tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**81 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **81 portes** (02/11 06 h) a donné
**76 vertes, 5 rouges** ; la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **incluse** et verte.

## Où est le registre (et comment lire le verdict)

Le registre n'est **pas** à la racine : il est écrit dans le dossier des journaux, par défaut
`work/portes-<MMJJ>-<HHhMM>/registre.txt` (variable `JOURNAUX`). **`/tmp` est effacé au reboot** :
pour une passe dont on veut garder les journaux (le cas normal), nommer un dossier durable —
`JOURNAUX=work/portes/<nom>`. Chaque ligne vaut :

```
nom-de-la-porte   code-de-sortie   durée-en-secondes
```

On lit le verdict **par le code**, jamais par les marqueurs `✅`/`❌` du source, jamais à travers un tube :

```bash
JOURNAUX=work/portes/passe-1102-19h32   # le dossier affiché au lancement
awk '$2 != 0' "$JOURNAUX/registre.txt"
```

Une porte **verte** a le code `0`. Une porte **rouge** a un code non nul (`1` échec, `124` borne dépassée).

## Les rouges connues

Les rouges **tolérées** sont celles listées dans
[`references-non-regression.md`](../pilotage/references-non-regression.md) ; toute **autre** rouge est une
**[régression](../theorie/glossaire/entrees/regression.md)** et se corrige avant de continuer. *(Une rouge `124` est une porte trop lente ou
bloquée : ce n'est pas un échec de la porte, c'est le délai — relancer la porte seule avec un `DELAI` plus grand.)*

## Lancer un sous-ensemble

```bash
PORTES="tableaux registre vision" DELAI=600 bash tools/toutes-les-portes.sh
```

Le filtre est un `grep` sur le nom du fichier (`*"$f"*`). Utile pour les portes documentaires (quelques secondes) ;
la passe complète reste la règle de fin de cycle.

## Ne pas fausser la passe

- **Les portes et une mesure GPU ne cohabitent pas** : lancer un modèle qui occupe 28 Go de VRAM pendant une passe
  [fait](../theorie/glossaire/entrees/fait-mesure-projete-deduit.md) attendre ou échouer les portes qui utilisent les cartes (`porte-audit-drapeaux`, `porte-vision`,
  `porte-*moteur`). Faire la passe **seule**, puis les mesures.
- **Un seul GPU libre (dérogation mesurée).** Si une session tient `gpu0` et que `gpu1` est libre, la passe
  peut tourner sur la carte libre : `CUDA_VISIBLE_DEVICES=<libre>,<occupé>` place la carte **libre en device 0
  logique** — on le vérifie à la mémoire (`nvidia-smi` doit voir monter la carte libre) — donc les portes qui
  appellent `cuda` ne touchent pas l'entraînement. C'est une **dérogation nommée** à la règle § 10 de
  [`plan-travail.md`](../pilotage/plan-travail.md) (la passe complète réserve `machine`) : elle ne vaut que si le
  verdict est lu avec la réserve des portes de temps — la charge CPU de l'autre session reste.
- **Les portes de temps** (`porte-delais`, `porte-flux`, `porte-topologie`) mesurent des latences : les lancer
  seules si un chiffre de temps doit être **interprété**. La passe complète est faite pour le **verdict**, pas pour
  le chronomètre.
- **Les portes de données** (`porte-diff-couche`) vérifient un **[contrat](../theorie/glossaire/entrees/contrat.md)**, pas un temps : deux exécutions
  identiques doivent donner un flux **identique** (la reproductibilité), et une divergence doit être **nommée**
  ([couche](../theorie/glossaire/entrees/couche.md), [jeton](../theorie/glossaire/entrees/jeton.md), neurones). Elles sont rapides (~30 s), sans GPU dédié — les lancer même pendant une mesure.
- Le journal de chaque porte est conservé dans `$JOURNAUX/<porte>.log` : en [cas](../theorie/glossaire/entrees/cas.md) de rouge, `tail -15` sur ce fichier
  donne la raison, pas le marqueur.

## Avant de commiter

La passe complète + `python3 tools/revue_documentation.py` + `porte-tableaux` : c'est le triplet de clôture d'un
sous-chantier (voir [`rangement.md`](rangement.md)).
