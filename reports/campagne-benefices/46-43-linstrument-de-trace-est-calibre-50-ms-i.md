> Campagne : **campagne-benefices** · expérience **43**
> Titre : 43. L'instrument de trace est CALIBRÉ : 50 ms injectés, 50,2 ms mesurés
> Date réelle : **2026-10-10 09:11 HAE** (source : commit `4367099`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 43. L'instrument de trace est CALIBRÉ : 50 ms injectés, 50,2 ms mesurés

Toute la partie « asynchronisme » (C4) repose sur une question préalable : **la trace globale
sait-elle mesurer le temps ?** Un instrument d'observabilité qu'on n'a jamais étalonné ne prouve
rien sur les régions qu'il observe. La campagne avait mesuré la **loi de latence** (3,4 ms par
jeton et par ms de RTT) ; il manquait l'étalonnage de l'instrument lui-même.

**Protocole** : un délai **connu** est injecté sur le lien (`"delai_ms": 50` dans la topologie),
les deux côtés tracent, la fusion apparie les croisements par nom de lien et par pas, et l'on
compare l'horodatage de l'**envoi** (pilote) et de la **réception** (nœud) pour chaque pas :

| mesure | valeur |
|---|---|
| croisements par source | **46** (23 pas × 2 liens) |
| liens confrontés par la fusion | **46 identiques, 0 divergents** |
| **écart envoyé → reçu, médian** | **50,2 ms** (min 50,2 · max 50,2) |
| délai injecté | **50 ms** |
| paires appariées | 23 |

**L'instrument mesure le temps à 0,2 ms près**, et cette différence est le transport lui-même
(l'aller-retour localhost). L'écart est **rigoureusement constant** (min = max) parce que le
délai injecté l'est aussi : un instrument qui aurait du bruit l'aurait montré.

**Ce que cela établit, et pourquoi c'est un préalable** : quand C4 mesurera que deux régions
avancent à des rythmes différents, l'instrument qui le dira aura été **étalonné contre une
valeur connue** — et non supposé juste parce qu'il produit des nombres.
