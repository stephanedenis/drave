# La quantification du KV par couche : le coût de l'int8 est dans les **premières** couches

> Mesure du 24/10/2026, Qwen2.5-0.5B Q8_0, **255 jetons**, contexte 256, 20 fils, binaire du dépôt.
> Le nouvel environnement `DRAVE_KV_BITS_COUCHES="0-11:8"` surcharge `DRAVE_KV_BITS` pour les couches citées
> (le code est dans `model.rs`, la table de décision viendra après la mesure).

## Le dispositif

Quatre exécutions, même texte, même contexte, même graine — seule la **précision du cache KV par couche** change :

| variante | perplexité | écart | temps |
|---|---:|---:|---:|
| **f32** (baseline) | **28,4015** | — | 8,8 s |
| 8 bits **partout** | 29,0389 | **+2,24 %** | 9,5 s |
| 8 bits sur **0-11**, f32 sur 12-23 | 29,0501 | **+2,28 %** | 9,1 s |
| f32 sur 0-11, **8 bits sur 12-23** | **28,4102** | **+0,03 %** | 9,5 s |

## Ce que ça dit

- **Le coût de l'int8 est intégralement dans les PREMIÈRES couches** : les couches 0-11 en 8 bits reproduisent
  l'écart de « tout en 8 bits » (+2,28 % contre +2,24 %), et les couches 12-23 en 8 bits ne coûtent **presque rien**
  (+0,03 %).
- **La politique par couche est donc possible** : les couches tardives peuvent passer en 8 bits **sans perte
  mesurable** — la moitié du cache KV à moitié prix, et la moitié du contexte en plus pour la même VRAM.
- C'est la première table de décision **par couche** du moteur, et elle est **choisie par la mesure**, pas par un
  seuil réglé à la main.

## Ce que ça ne dit pas

- **Un seul modèle** (0,5 B) et **un seul texte** (255 jetons) : la frontière 0-11/12-23 n'est pas une loi — il faut
  la refaire sur le 3 B et le 7 B, et **couche par couche** (laquelle des premières est la plus sensible ?).
- À **contexte long** (8 192), l'écart de l'int8 monte à +3,0 % (mesure A5.2) : la perte par couche y est
  probablement plus forte, et la frontière peut se déplacer.
- L'int8 n'est pas l'int4 (+364 % global) : la même expérience en 4 bits par couche dirait si les couches tardives
  tolèrent aussi le 4 bits — c'est le vrai gain de mémoire.
- Le temps ne bouge pas (9,1-9,5 s) : la quantification ne paie pas en vitesse ici, seulement en mémoire.
