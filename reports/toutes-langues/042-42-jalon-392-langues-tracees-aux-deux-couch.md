> Campagne : **toutes-langues** · expérience **42**
> Titre : 42. Jalon : 392 langues tracées aux DEUX couches, zéro échec
> Date réelle : **2026-10-06 13:18 HAE** (source : commit `ce3b05d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 42. Jalon : 392 langues tracées aux DEUX couches, zéro échec

| corpus | contenu | taille | langues | échecs |
|---|---|---:|---:|---:|
| `udhr392/` | couches 0 et 10 | 2,7 Go | **392/392** | **0** |
| `udhr392_c8/` | couches 0, **8** et 10 | 4,0 Go | **392/392** | **0** |
| `unites/` | 10 unités alignées, couches 0, 8 et 10 | 491 Mo | **400/400** | **0** |

Passe couche 8 : **241 minutes**, 36,9 s par langue en moyenne. Passe couche 10 :
environ 4 h 17 (§35). Les deux passes ont coûté **~8 heures de professeur**, dont
4 h 17 auraient pu être évitées : `--trace-couches` ne filtre que l'**écriture**, donc
écrire 0, 4, 8, 10, 12 et 16 dans la première passe n'aurait presque rien coûté. C'est
la leçon la plus chère de la session, et elle est corrigée pour toute passe future.

L'objectif « étendre le pont à TOUTES les langues de l'UDHR » est donc atteint **sur
les deux cibles**, et l'invariance se mesure désormais sur **dix points alignés par
langue** au lieu d'un.


---
