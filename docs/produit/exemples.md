# Exemples — entrées et sorties réelles

> Tous les exemples ci-dessous ont été **lancés** avec `tools/drave.py` le 2026-11-06 sur `s/v7`.
> Les sorties sont recopiées telles quelles (espaces compactés).

## 1. Une phrase simple, en français

```bash
python3 tools/drave.py analyser "Le chat dort."
```

```text
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
```

**À lire** : le GN a le rôle `agent` et sa **cible** est le verbe `dort` ; le GV a pour cible le
sujet `chat`. L'attachement est la relation segment → gouverneur, pas le rôle.

## 2. Une relative, en français

```bash
python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille."
```

```text
GN   [0:7]    Le chat                           rôle=agent       → réveille
GP   [8:21]   de la voisine                     rôle=possession  → réveille
REL  [22:42]  qui dort sur le toit              rôle=qualite     → voisine
REL  [22:54]  qui dort sur le toit se réveille  rôle=qualité     → réveille   ← à ignorer
GV   [43:54]  se réveille                       rôle=predicat    → voisine
```

**À lire** : la REL `[22:42]` est la bonne (son antécédent est `voisine`). La REL `[22:54]` est un
**doublon** produit par le générateur S et ajouté par l'union : elle déborde sur le verbe
principal. C'est une **limite connue** (voir `README.md` § 6) : pour un usage produit, filtrer les
segments qui en contiennent un autre.

## 3. Une phrase anglaise

```bash
python3 tools/drave.py analyser "The cat that sleeps on the roof is black." --langue en
```

```text
GN   [0:7]    The cat                  rôle=groupe nominal  → black
REL  [8:31]   that sleeps on the roof  rôle=qualité         → cat
GV   [32:40]  is black                 rôle=prédicat        → —
```

**À lire** : la REL prend `cat` (l'antécédent) et la relative est bornée au bon endroit.

## 4. Le JSON, pour un client

```bash
python3 tools/drave.py analyser "Le chat dort." --json | head -20
```

```json
{"texte": "Le chat dort.", "langue": "fr", "script": "Latn", "source": "heuristique",
 "etiquettes": [{"niveau": "graphème", "type": "lettres", "valeur": "Le", "debut": 0, "fin": 2,
                 "confiance": 0.99, "candidats": []}, "…"]}
```

Le JSON est **déterministe** (pas d'horodatage ni de durée) : deux appels donnent le même sha256.
C'est ce que vérifie `drave.py rejouer "Le chat dort."`.

## 5. La mesure sur le gold

```bash
python3 tools/drave.py evaluer
```

```text
gold vivant · 612 phrases · 3179 tokens · 239 cibles
POS         exactitude 75.81 %  (fermé 90.04 %, ouvert 62.34 %)
SYNTAGMES   F1 58.49 %  (P 62.92 % / R 54.64 %) · tête 73.36 %
ATTACHEMENT exact 92.89 % · couverture 92.89 % · exact sur span 100.00 % · top-k 92.47 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 %
```

**À lire** : `exact 92.89 %` est le **rendement** (222/239 cibles) ; `exact sur span 100 %` est
l'**exactitude** sur les 222 segments dont le span est prédit. Les 17 cibles restantes n'ont pas
de segment au bon span : c'est un plafond de **couverture**, pas d'attachement.

## 6. Un cas d'échec connu

```bash
python3 tools/drave.py analyser "le chemin nage avec le renard"
```

```text
GP   [10:20]  avec le renard  rôle=instrument
```

**À lire** : le gold synthétique attend un GP `le renard` (sans préposition) — un défaut du
générateur de gold, pas du bloc. C'est l'un des 17 spans inatteignables : le produit ne peut pas
les produire, et la mesure le dit (`couverture 92,89 %`, pas 100 %).
