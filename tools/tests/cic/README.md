# Corpus d'or CIC-lite — copie portable Drave

Ce dossier contient la **copie byte-identique** du corpus d'or CIC de Panini/Research :

- source : `Panini/research/nipada/falsification/corpus_dor_cic_v1.json` ;
- sha256 : `3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec` ;
- commit source : `2130310db46ca9d59883500adc607bd86f534678` ;
- 46 714 octets, 3 définitions, 21 constantes, **42 entrées** (**36** attendues
  `accepte`, **6** attendues `rejette`).

Le fichier `manifeste.json` porte les empreintes de la source, du TSV et de la copie.
La copie existe pour que le vérificateur Drave soit **portable** : il n'a pas besoin
du dépôt Panini pour rejouer les 42 verdicts.

## Ce qu'il faut lancer

```bash
python3 tools/verificateur_cic.py --json     # mesure machine
python3 tools/verificateur_cic.py --verbeux  # une ligne par entrée
bash tools/porte-cic.sh                      # la porte : 42/42 + contrôles négatifs
python3 tools/tests/test_verificateur_cic.py # 21 tests
```

Le vérificateur **ne modifie jamais** ce fichier. Toute altération d'un octet est
détectée par l'empreinte `sha256(preuve || type)` et/ou par le noyau.
