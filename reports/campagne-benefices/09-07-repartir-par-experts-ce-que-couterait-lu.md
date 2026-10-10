> Campagne : **campagne-benefices** · expérience **07**
> Titre : 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle
> Date réelle : **2026-10-08 21:57 HAE** (source : commit `1e11cc7`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle

Le dépôt découpe par **plages de couches** (prouvé, écart 0,00e0). Mais l'unité
naturelle d'un modèle routé, c'est l'**expert** — et la sommation inter-nœuds
n'existe pas (`Moe::ou` → `None` → `continue` : un nœud partiel saute l'expert
absent sans un mot). `tools/census_routage.py` donne les trois chiffres qui
décident, mesurés sur `m4_route` (4 couches, 8 experts, top-2, 1 024 jetons) :

| couche | charge max | charge moyenne | déséquilibre | experts pour 90 % des jetons |
|---|---:|---:|---:|---:|
| 0 | 537 | 256 | **×2,10** | 5 sur 8 |
| 1 | 517 | 256 | ×2,02 | 7 sur 8 |
| 2 | 703 | 256 | **×2,75** | 6 sur 8 |
| 3 | 999 | 256 | **×3,90** | 4 sur 8 |

**Trois enseignements, et le troisième commande la suite.**

1. **Le déséquilibre est réel** : jusqu'à **3,9×** entre l'expert le plus chargé
   et la moyenne. Un partage naïf par experts donnerait un nœud 4 fois plus
   chargé que l'autre — il faut un routeur qui équilibre, ou un découpage qui
   tienne compte de la charge mesurée.
2. **On ne peut pas élaguer** : à top-2 sur 8, **4 à 7 experts** sont nécessaires
   pour couvrir 90 % des jetons. Tous servent ; la « localité » qui justifierait
   de n'en garder que quelques-uns n'existe pas à cette échelle.
3. **Le volume à router est négligeable, la latence ne l'est pas.** L'état
   transporté vaut **847 octets** par jeton (79 d'en-tête + 192 × 4) — du même
   ordre que les **848 octets** mesurés pour un flux de couche. Ce qui coûte,
   c'est l'aller-retour par couche, pas les octets : le dépôt a mesuré
   `attente ≈ calcul distant + 3,2 × latence`. Répartir par experts multiplie
   donc les allers-retours que répartir par couches évite.

---
