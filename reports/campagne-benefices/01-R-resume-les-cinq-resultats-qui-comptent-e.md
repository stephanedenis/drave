> Campagne : **campagne-benefices** · expérience **R**
> Titre : Résumé — les cinq résultats qui comptent, et les manques
> Date réelle : **2026-10-09 06:34 HAE** (source : commit `4836fc8`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## Résumé — les cinq résultats qui comptent, et les manques

*Détail et conditions dans les sections indiquées ; le verdict famille par famille
est au § 0 bis.*

| # | résultat | mesure |
|---|---|---|
| 1 | **Le chemin par listes n'approxime RIEN** | à encodage de poids égal, `--push` et `--dense` produisent des logits **identiques au bit près** (`cmp` sur 4 254 216 octets) et la même suite gloutonne (§ 22) |
| 2 | **La parcimonie doit être APPRISE, pas imposée** | à 25 % gardés : témoin **10,8758** de perplexité, modèle entraîné creux **5,1719** (−52 %) · à 50 % : 5,3032 contre 5,0606 · **chaque modèle n'est bon que dans son régime**, et la distillation ne s'y ajoute pas (−0,3 %) — elle rattrape le routage, pas la parcimonie (§ 5 ter) |
| 3 | **Le routage seul s'inverse à dim 512 — la distillation le rattrape** | routé : −2,6 % (256), −2,9 % (384), **+10 % (512)** · routé **distillé** : **4,3305 contre 4,5686** au dense (−5,2 %), à 12,8 M paires/jeton des deux côtés (§ 5 bis) |
| 4 | **Le brouillon spéculatif paie quand la cible est bornée par le disque** | ×0,70 à 0,210× de coût relatif · ×1,09 à 0,134× · **×1,52 à 0,039×** — c'est le rapport de coût qui décide, pas l'acceptation (§ 1 bis) |
| 5 | **La mémoire tient, et les gros modèles tournent** | **18 aiguilles sur 18** de 512 à **12 288 jetons** (§ 9) · V4-Flash **365,7 Go sur 125 Go de RAM, 37,6 Go résidents** (§ 12) · gpt-oss rend **15,6017**, la valeur attendue au chiffre près (§ 0 ter) |

**Les cinq manques, consignés comme manques** : les **encodeurs** (`bge-m3`
inexécutable), le **noyau Q8 des experts** (un modèle routé ne peut pas être
exécuté en listes), le **lot sur un modèle plus gros que la RAM** (V4.1 refuse le
chemin par lots, et il a raison), le **décodage spéculatif** (aucune ligne de
moteur, et le cahier des charges est mesuré), et la **qualité** des modèles plus
gros que la RAM (coût mesuré, perplexité sans valeur).

**Cinq pièges de méthode ont été trouvés et corrigés** (§ 16, § 17) — dont un
binaire plus vieux que ses correctifs, une porte qui ne pouvait pas passer, et un
cache qui survivait à son correctif. Ils comptent autant que les chiffres : trois
mesures publiées ont été refaites à cause d'eux.

---
