# S4 — la prélecture dans le moteur : le calcul ne paie plus les défauts de page

> Campagne : **S4 (Strata → Drave)** · expérience 02 — après le mécanisme, le moteur
> Question : `reports/rapport-prelire-grappe.md` a mesuré le **mécanisme** hors du moteur
> (grappe par `madvise` : 1 230 Mo/s contre 29 à la demande ; puis, sur un motif d'experts,
> **`madvise` sur la plage entière = ×1,06**, par tranches = ×2,5, **fils qui touchent = ×3,5**).
> Ce classement tient-il **dans une passe réelle**, et la prélecture de la couche suivante —
> l'idée de Strata — paie-t-elle ?
> Verdict : **oui pour les fils, non pour la couche suivante.** Sur la même passe (8 jetons,
> Qwen3-30B-A3B, array, cache évincé avant chaque bras) : le calcul passe de **7,70 s à 3,65 s**
> (−53 %) et la passe de **35,03 s à 31,21 s** (−11 %), à **perplexité identique** (799,8557).
> La granularité de `madvise` **ne change rien dans le moteur** (31-36 s dans tous les cas), et
> la prélecture des poids denses de la couche suivante, implémentée puis mesurée, **n'apporte
> rien** (30,47 s sans, 32,05 s avec) : elle reste un témoin éteint.
> Date réelle : 2026-10-12, 18:38-20:40 HAE (heure lue sur la machine)
> Protocole : `tools/porte-prechargement.sh` · mécanisme : `tools/banc-prelire.py`,
> `tools/banc-experts.py` · éviction du cache : `tools/evincer-cache.py`

## 1. Les trois bras, et ce qu'ils mesurent

| bras | réglage | ce que c'est |
|---|---|---|
| `demande` | `DRAVE_PRELIRE=0` | aucune prélecture : chaque page est demandée au moment du calcul |
| `madvise` | `DRAVE_PRELIRE_FILS=0` | l'ancien chemin : `madvise(WILLNEED)` sur la plage de l'expert |
| `fils` | défaut (8 fils) | des fils **entrent les pages** eux-mêmes, en parallèle, avant le calcul |

Le cache de pages est **évincé avant chaque bras** (`posix_fadvise(DONTNEED)` sur le fichier) :
sans cela le deuxième bras lit ce que le premier a laissé et mesure de la RAM — le piège qui
avait donné « 300 Mo/s au hasard » au premier essai du banc.

```bash
tools/porte-prechargement.sh          # 8 jetons, 2 répétitions, ~7 min
JETONS=2 MODELE=<copie sur disque dur> tools/porte-prechargement.sh   # le même, sur plateau
```

## 2. Les mesures (médianes de 2 répétitions, cache froid)

| bras | octets lus | temps mural | **temps de calcul** | perplexité |
|---|---|---|---|---|
| `demande` | 7,52 Go | **35,03 s** | **7,70 s** | 799,8557 |
| `madvise` | 9,52 Go | 32,44 s | 5,60 s | 799,8557 |
| `fils` | 10,89 Go | **31,21 s** | **3,65 s** | 799,8557 |

Détail par répétition (mural · calcul) : `demande` 37,13 · 9,5 puis 32,92 · 5,9 —
`madvise` 32,48 · 5,8 puis 32,41 · 5,4 — `fils` 29,89 · 3,7 puis 32,54 · 3,6.

Ce que ça dit :

* **le calcul ne paie plus les défauts de page** : 7,70 s → 3,65 s. Les défauts majeurs, comptés
  par `time -v`, tombent de **957 170** (demande) à **4 188** (fils) : les pages sont là quand le
  calcul les demande, au lieu d'être attendues une par une ;
* **la prélecture `madvise` n'est pas nulle mais presque** : elle gagne 2,6 s sur 35 au prix de
  2 Go lus en plus, et sa granularité (plage entière, tranches de 1 Mio) **ne change rien dans le
  moteur** — 31 à 36 s dans tous les cas, alors que le mécanisme hors moteur la donnait à ×2,5 ;
* **les octets lus augmentent** (10,89 Go contre 9,52) : les fils parcourent les plages entières,
  là où la demande ne lit que les pages que le calcul touche. C'est un échange assumé **sur un
  support à bande passante** (l'array rend 7,45 Go/s à huit lecteurs) ; sur un disque dur il se
  reprend sur des chiffres, et la porte publie les octets pour ça ;
* le commentaire du code qui affirmait « les demander tous d'un coup laisse le noyau paralléliser
  ses lectures de pages » est **démenti par la mesure** : `madvise` sur une plage entière rend
  ×1,06. La prélecture parallèle est celle qu'on lance soi-même.

## 3. Ce qui a été implémenté, et ce qui a été retiré

| changement | état | mesure |
|---|---|---|
| `gguf::prelecture_parallele` (fils qui entrent les pages) + `prelire` par tranches de 1 Mio | **gardé, actif par défaut** (`DRAVE_PRELIRE_FILS`, 8) | ×3,5 sur le mécanisme ; −53 % de calcul dans la passe |
| prélecture des poids **denses de la couche suivante** (l'idée de Strata) | **implémentée, mesurée, éteinte** (`DRAVE_PRELIRE_DENSE=1` pour la rallumer) | 30,47 s sans, 32,05 s avec : **rien** — le préchargement synchrone ne se recouvre pas avec le calcul |
| témoins `DRAVE_PRELIRE=0`, `DRAVE_PRELIRE_TRANCHE=0`, `DRAVE_PRELIRE_FILS=0` | gardés | ce sont eux qui rendent les trois bras comparables |

## 4. Ce que cette fiche ne dit pas

* **elle ne dit pas que le manque est comblé.** Le mécanisme qui rend **4 Go/s** sur le motif
  d'experts est le **`pread` explicite depuis des fils** (`tools/banc-experts.py` : 3 995 Mo/s
  contre 1 126 pour la demande) — et il demande des **tampons**, donc un chemin de calcul qui
  lit dans une mémoire à nous au lieu du mapping. C'est le chantier « lecteurs parallèles » du
  § 6.5.1 de `docs/configuration-nvme-raid-amd.md`, et il reste ouvert ;
* **elle ne mesure que la passe d'un modèle dense-en-experts sur l'array** : la même porte sur la
  copie du disque dur reste à faire (le bras `demande` y est lent au point de borner la mesure) ;
* **elle ne dit rien du décodage** (un jeton à la fois, où les experts d'un jeton ne sont pas
  connus avant le routage) : ici, c'est le **préremplissage** qui est mesuré, comme chez Strata.
