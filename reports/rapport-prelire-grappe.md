# S4 — le préchargement par grappe : la lecture à la demande rend 29 Mo/s là où la grappe rend 1 230

> Campagne : **S4 (Strata → Drave)** · expérience 01 — le mécanisme de lecture, hors du moteur
> Question : `docs/manques.md` § 1 nomme le manque — « la lecture disque en mmap atteint **8,6 Mo/s**
> sur disque dur contre **243 Mo/s** en séquentiel (÷28) ; un préchargement ordonné (`madvise`,
> lecture des experts par grappe) n'existe pas ». **Que vaut ce préchargement, mesuré sur les
> supports d'aujourd'hui**, et le manque tient-il encore tel quel ?
> Verdict : **la grappe est le levier, et sur l'array il vaut ×42.** Même fichier, mêmes octets
> utiles, trois ordres de lecture : **au hasard 29,43 Mo/s · pages consécutives 96,77 Mo/s ·
> grappes de 1 Mio préchargées par `madvise` 1 230 Mo/s** (médianes de trois répétitions
> entrelacées, array raid0). Sur disque dur, les trois bras sont 0,56 / 16,27 / **30,56 Mo/s** —
> le classement tient, l'écart est plus faible parce que le plateau paie le seek dans tous les cas.
> Date réelle : 2026-10-12, 18:38-18:47 HAE (heure lue sur la machine)
> Protocole : `tools/banc-prelire.py` (dans le dépôt, exécutable tel quel)

## 1. Le protocole, et pourquoi il est piégeux

Le banc mappe le fichier (`mmap`), lit **le même nombre d'octets utiles** de trois façons, et rend
des **Mo/s utiles** :

| bras | ce qu'il fait | ce qu'il mesure |
|---|---|---|
| `demande` | des pages tirées au hasard sur **2 Gio** | le régime du manque : un défaut de page par lecture, sans ordre |
| `sequentiel` | des pages consécutives | la borne haute accessible sans `madvise` |
| `grappe` | des fenêtres de **256 pages (1 Mio)** dispersées sur 2 Gio : `madvise(WILLNEED)` sur la fenêtre **puis** parcours | le préchargement ordonné de S4 |

**Trois pièges, chacun payé par une mesure fausse avant d'être corrigé** :

1. **une fenêtre plus petite que la lecture en avance du noyau n'est pas un hasard.** Premier
   essai : 400 pages dans 1,6 Mo → le noyau lisait tout le voisinage au premier défaut et le bras
   « au hasard » rendait **300 Mo/s** (du cache). Les pages sont donc tirées sur 2 Gio, très au-delà
   de `read_ahead_kb` (1 024 Kio ici) ;
2. **le contrôle à froid ne doit pas chauffer ce qu'on mesure.** Il touche une page **8 Mio à
   côté** de la zone mesurée, et le banc publie son temps : **12 à 36 ms** sur le plateau
   (un seek, donc du vrai disque) contre **136 à 3 476 µs** sur l'array. Sans ce témoin, on ne peut
   pas distinguer « rapide » de « déjà en cache » ;
3. **`madvise` est asynchrone** : on le lance sur la fenêtre entière *puis* on parcourt — l'inverse
   mesurerait des défauts de page déguisés.

Neuf zones distinctes (une par bras et par répétition, 4 Gio d'écart) : deux bras ne partagent
jamais une page, et trois répétitions entrelacées donnent la médiane (règle du dépôt).

## 2. Les mesures

```bash
python3 tools/banc-prelire.py ~/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf --pages 600
python3 tools/banc-prelire.py ~/IA/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf --pages 2000
```

| bras | **disque dur** (63,4 Go) | **raid0** (365,7 Go) |
|---|---|---|
| `demande` (au hasard sur 2 Gio) | **0,56** Mo/s | **29,43** Mo/s |
| `sequentiel` (pages consécutives) | **16,27** Mo/s | **96,77** Mo/s |
| `grappe` (`madvise` 1 Mio puis parcours) | **30,56** Mo/s | **1 230,06** Mo/s |
| grappe ÷ demande | ×55 | **×42** |
| grappe ÷ séquentiel | ×1,9 | **×12,7** |

Détail des trois répétitions (Mo/s) — la dispersion est dans la règle du dépôt (charge de fond) :

| bras | disque dur | raid0 |
|---|---|---|
| `demande` | 0,37 · 0,68 · 0,56 | 24,30 · 29,90 · 29,43 |
| `sequentiel` | 16,73 · 13,94 · 16,27 | 83,97 · 96,77 · 98,48 |
| `grappe` | 33,18 · 30,56 · 27,98 | 1 163,62 · 1 274,83 · 1 230,06 |

## 3. Ce que ça dit, et ce que ça ne dit pas

* **sur l'array, lire à la demande laisse 97 % de la bande passante inutilisée.** 29,43 Mo/s au
  hasard, 96,77 Mo/s même en pages consécutives — alors que le même support rend **7,45 Go/s** à
  huit lecteurs (`reports/rapport-raid0-nvme.md`). Le facteur manquant est le **groupe de lectures
  asynchrones** : `madvise` sur 1 Mio fait travailler `md0` sur les quatre disques d'un coup, là où
  un défaut de page fait la queue ;
* **le manque de `docs/manques.md` § 1 tient, et il est plus grand qu'annoncé sur NVMe** : le
  document dit « sur NVMe, 140-300 Mo/s (÷5 à ÷11) » ; mesuré ici, la lecture à la demande sur
  l'array rend **29,43 Mo/s** au hasard et **96,77** en séquentiel — la borne haute de la grappe est
  **1 230 Mo/s**. Le chiffre du 9/10 décrivait le disque dur ; sur l'array, l'écart au préchargement
  est d'un ordre de grandeur de plus ;
* **ce que ces nombres ne sont pas** : des débits de device. Les octets comptés sont les **octets
  utiles** (4 Kio par page touchée) ; le noyau lit souvent davantage (lecture en avance). Ce sont
  donc des débits *vus par le lecteur*, ce qui est la grandeur qui compte pour le moteur — pas une
  mesure de `dd` ;
* **ce qui n'est pas encore mesuré** : les bras **dans le moteur**. Aujourd'hui `model.rs` demande
  les experts de la couche courante *juste avant de s'en servir* (`prelire_expert`, dans l'ordre du
  routage) ; la porte de S4 doit comparer, sur la même passe et la même trace d'experts :
  `DRAVE_PRELIRE=0` (à la demande) · le préchargement actuel · un préchargement **ordonné par la
  disposition** (rangs contigus regroupés, demande émise avant le calcul de la couche). C'est
  l'étape suivante, et elle se paie d'une passe complète des portes (modification du moteur).

## 4. La suite (une seule action)

Écrire la porte `tools/porte-prechargement.sh` : la même passe, trois bras, un **débit de lecture**
(`File system inputs` de `time -v`, la grandeur que la campagne lit déjà) et le **temps de
préchargement**, mesurés séparément du décodage — puis n'implémenter dans `model.rs` que ce que la
porte montre. Le témoin `DRAVE_PRELIRE=0` existe déjà et sert de bras « à la demande ».
