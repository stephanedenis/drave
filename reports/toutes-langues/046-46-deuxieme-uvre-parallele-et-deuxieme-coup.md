> Campagne : **toutes-langues** · expérience **46**
> Titre : 46. Deuxième œuvre parallèle, et deuxième couple de langues
> Date réelle : **2026-10-06 15:27 HAE** (source : commit `6b1cad4`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 46. Deuxième œuvre parallèle, et deuxième couple de langues

### 46.1 Le manque

Le corpus parallèle du pont ne comptait qu'**une** œuvre : *Roméo et Juliette*, en
anglais et en français, 24 scènes. Or **une seule paire de langues ne permet pas de
distinguer une propriété du PONT d'une propriété du COUPLE de langues.** Si le
transfert se comporte de la même façon sur une seconde paire, c'est le pont ; sinon,
c'était en–fr.

Les bases `backlog_gutenberg_{en,fr,de,es}.db` (Panini-Research) contiennent trois
paires exploitables :

| œuvre | paire | découpage | état |
|---|---|---|---|
| Roméo et Juliette | en–fr | 24 scènes | déjà traité |
| Le Comte de Monte-Cristo | en–fr | tomes de tailles très inégales (2,6 M contre 0,73 M caractères) | écarté |
| **Crime et Châtiment** | **en–es** | **39 chapitres (en) / 40 (es)** | **retenu** |

### 46.2 Alignement EXACT, pas approximatif

On ne découpe pas à offsets fixes : le même caractère ne dit pas la même chose dans
les deux langues. On découpe **par chapitre**, et le chapitre `i` d'une langue
correspond au chapitre `i` de l'autre. Vérifié sur les tailles, dont le rapport reste
entre **0,82 et 1,14** sur les 38 premiers chapitres.

L'anglais marque `CHAPTER <romain>`, l'espagnol une ligne ne portant que le numéro
romain. **On ne garde que les chapitres qui tiennent dans `--ctx 8192` DANS LES DEUX
LANGUES** — un chapitre tronqué d'un seul côté romprait l'alignement sans le dire.
Seuil retenu : 30 000 caractères.

### 46.3 Le corpus

Écrit dans `corpus/parallele_crime/` :

| langue | segments | caractères | moyenne |
|---|---:|---:|---:|
| en | **24** | 590 808 | 24 617 |
| es | **24** | 564 651 | 23 527 |

**24 chapitres alignés — exactement l'ordre de grandeur des 24 scènes de Romeo**, ce
qui rend les deux corpus directement comparables. Mais **2 000 fois plus longs** :
24 600 caractères par segment contre ~1 200 pour une scène de Romeo.

### 46.4 Une fausse alerte que j'ai levée, et qui méritait de l'être

En comparant deux traces du même fichier, j'ai obtenu **des tailles et des empreintes
MD5 différentes** — ce qui aurait signifié que le moteur n'est pas déterministe, et
aurait mis en doute toutes les mesures de la session.

**C'était faux, et l'erreur est de moi** : les deux fichiers comparés étaient **partiels**,
tronqués par les `timeout` que j'avais posés sur mes propres commandes. La comparaison
propre — `--couches 0:9` contre `--couches 0:24`, sur `en_Albert_Einstein` et
`de_Albert_Einstein` — donne des empreintes **identiques** (§45.5). Le moteur est
déterministe ; c'est ma façon de mesurer qui ne l'était pas.

Leçon appliquée : les traçages longs sont lancés **sans `timeout`**, avec un journal
qui permet de savoir ce qui est complet et ce qui ne l'est pas.

### 46.5 Coût, et pourquoi il est acceptable

Un chapitre de 25 000 caractères coûte ~250 s (la machine est partagée). 48 traces,
soit **~3,5 heures**, lancées en tâche de fond et analysables par segment : après `n`
segments on a `n` points alignés.

Traçage en cours, journal `/tmp/trace_crime.log`, garde `grep -qx TERMINE`.


---
