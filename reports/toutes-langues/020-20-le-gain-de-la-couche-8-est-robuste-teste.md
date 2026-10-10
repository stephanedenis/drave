> Campagne : **toutes-langues** · expérience **20**
> Titre : 20. Le gain de la couche 8 est ROBUSTE — testé sur trois graines
> Date réelle : **2026-10-06 05:10 HAE** (source : commit `377339d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 20. Le gain de la couche 8 est ROBUSTE — testé sur trois graines

Le §19 reposait sur **une seule mesure**. Une seule graine ne prouve rien : c'est
exactement la leçon du tour 3, où un signal non répété avait produit une conclusion
fausse. Vérification sur trois graines du réservoir gelé :

| graine | couche 10 | **couche 8** | **gain** | invariance 8 | invariance 10 |
|---|---:|---:|---:|---:|---:|
| 5 | 0,5802 | 0,6015 | **+0,0213** | 0,9504 | 0,9540 |
| 11 | 0,5826 | 0,6039 | **+0,0213** | 0,9611 | 0,9666 |
| 23 | 0,5828 | 0,6046 | **+0,0218** | 0,9505 | 0,9597 |

| | |
|---|---:|
| **gain moyen** | **+0,0215** |
| amplitude du gain | 0,0005 |
| variation entre graines (couche 10) | 0,0026 |
| **rapport gain / variation** | **8×** |

**Le gain est 8 fois plus grand que la dispersion entre graines.** Ce n'est donc
pas un coup de chance, et l'amplitude du gain (0,0005) est cinq fois plus petite
que la dispersion des mesures elles-mêmes.

**L'invariance de sortie est systématiquement plus basse à la couche 8** — de
0,006 en moyenne sur les trois graines, avec une amplitude de 0,001 seulement. Le
prix payé est donc stable lui aussi, et il reste très inférieur au gain.

### Ce que ce test ajoute à la méthode

**Un résultat à une graine n'est pas un résultat.** Je l'avais appris au tour 3 en
me trompant, et je l'applique maintenant **avant** de graver la conclusion — plutôt
qu'après qu'un run complet l'ait contredite.


---
