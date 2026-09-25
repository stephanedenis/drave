# Moteur d'événements optimisé — les 4 optimisations

Moteur `qtrinet-core` (Rust, **std seul**, aucune dépendance). Matrice réelle
`blk.0.ffn_gate.weight` de Qwen2.5-0.5B-Q8_0 : 4864 entrées × 896 sorties,
**4 303 745 événements** (ternaire issus des signes réels, densité 100 %).
Machine : 2 × Xeon E5-2687W v3, **16 threads** sur les 40.

---

## 1. Réduction incrémentale (fin du memset)

Chaque worker ne remet à zéro **que les destinations qu'il a touchées** (liste
`touched`), et le demandeur ne réduit que la fenêtre `[min, max]` utile au lieu
des 896 sorties.

| | avant | après |
|---|---|---|
| Coût fixe d'un appel à vide | 0,484 ms | **0,0051 ms** (fusion) / 0,0088 ms (2 listes) |

➡️ **×95 sur le coût fixe.** C'est ce qui rend le débit *variable* exploitable :
un événement rare ne paie plus le prix d'un appel plein.

## 2. Décodage SWAR par paquets de 8

Les écarts d'un octet (le cas de 99,99 % des événements à forte densité) sont
décodés **8 à la fois dans un mot de 64 bits** : un seul test
`w & 0x8080_8080_8080_8080` dit si les 8 octets sont des varints d'un octet ;
les 8 valeurs sortent par décalages, sans branche par élément. Accumulation sans
contrôle de borne (le `cap` borne la liste, pas la boucle).

## 3. Vecteur d'activation creux explicite (`SparseVec`)

La cascade produit directement `(indices triés, valeurs contiguës)` — 8 octets
par source active. Plus aucun test de zéro ni accès indirect au tableau dense
dans la boucle chaude. C'est aussi la structure que produira le matériel.

## 4. Listes fusionnées (`FusedSign`)

Au lieu de **deux** listes (destinations « + » et destinations « − »), une
**seule** liste triée par destination, avec les signes dans un plan de bits
parallèle. L'accès à l'accumulateur devient **monotone** (une seule passe
croissante au lieu de deux), et le plan de signe se lit par le même index
d'événement.

Coût : 4,89 Mo (8,97 b/poids) contre 4,34 Mo (7,98 b/poids) pour les deux listes
séparées ; le bitmap+signe reste à 1,09 Mo (1,99 b/poids) mais impose un parcours
dense, donc un débit **constant** et non variable.

---

## Résultats mesurés (16 threads)

| Densité | Événements | Fusion | 2 listes |
|---|---|---|---|
| 0 % | 0 | 0,0051 ms | 0,0088 ms |
| 1 % | 43 560 | 0,51 G év/s | 0,83 G év/s |
| 5 % | 216 960 | 1,57 G év/s | 2,46 G év/s |
| 10 % | 430 359 | 2,46 G év/s | 3,09 G év/s |
| 25 % | 1 076 785 | **2,84 G év/s** | **4,20 G év/s** |
| 50 % | 2 152 648 | 3,44 G év/s | 4,46 G év/s |
| 100 % | 4 303 745 | 3,66 G év/s (1,18 ms) | 4,99 G év/s (0,86 ms) |

**Exactitude** : à 25 %, les deux décodeurs donnent un résultat **IDENTIQUE** au
produit matrice-vecteur dense de référence. ✅

Le chemin « 2 listes » reste ~25 % plus rapide que la fusion ; l'écart n'est plus
le facteur 2 annoncé plus tôt (mesure erronée, voir ci-dessous). La fusion garde
l'avantage d'**une seule passe** et de la moitié des accès mémoire sur les écarts.

> Mesures prises avec une charge système de fond (bureau, load ~1,4) : elles
> varient de ±20 % d'une passe à l'autre et sont donc **pessimistes**.

## Exécution sans multiplieur

| | temps | ops |
|---|---|---|
| multiplication i8×i8 | 2,5 ms | 4,36 M |
| **décalages + additions** | **112,3 ms** | 13,58 M (3,12 additions/poids) |
| rapport | **×44,9** | — |
| résultat | **identique** ✅ | — |

Les niveaux Q8_0 réels contiennent en moyenne 3,12 bits à 1 ⇒ ~3 additions par
poids. Sur CPU le multiplieur est 45× plus rapide ; **sur FPGA il n'existe pas** :
la contrainte du CDC (« aucun DSP ») est satisfaite pour un modèle 8 bits, sans
réentraînement ni élagage.

---

## Le bug qui a coûté deux mesures

La première campagne annonçait « fusion DIVERGENTE au rang 0 : 3838 vs 3513 » et
un chemin 2-listes à 7,53 G év/s. **Les deux chiffres étaient faux**, pour une
seule raison :

> Le chemin « 2 listes » ne tenait pas de liste `touched` : il vidait
> l'accumulateur par un `memset` complet **puis vidait la liste**. L'appel
> fusion suivant ne trouvait donc rien à effacer et **accumulait sur les restes
> de l'appel précédent**.

Le contrat d'invariant est : *toute destination écrite doit être dans `touched`*.
Les deux décodeurs le respectent maintenant (`row_delta_into` prend `touched` en
paramètre), et la remise à zéro ne dépend plus du chemin emprunté. Leçon : quand
deux implémentations partagent un état, **le contrat de nettoyage doit être dans
l'état partagé, pas dans la convention de l'appelant**.

---

## Ce que ça change pour le CDC

1. **Le débit est bien variable** : de 0,005 ms (aucun événement) à 1,18 ms
   (4,3 M événements) sur la même matrice — un rapport de 230. L'argument
   « on ne paie que ce qui s'active » est vérifié à l'échelle du moteur.
2. **La cadence utile est 3–5 G év/s sur 16 threads CPU**, soit ~0,2–0,3 G év/s
   par cœur. Une carte FPGA visant 124 MHz × 32 PEs = 4 G év/s est donc
   **exactement dans la cible d'un CPU 16 cœurs** — la carte ne gagne que par
   son rapport watt/carte, pas par la cadence brute.
3. **Pas de tri, pas de dédoublonnage** : l'ordre naturel des écarts suffit.

## Reste à faire

- **Traitement par blocs de destination** pour vectoriser (AVX2 n'a ni gather ni
  scatter entier : il faut transposer le parcours, pas la boucle).
- **Fusion par compartiments de destination** (réseau de combinaison façon
  routeur AER) pour le cas multi-cartes — c'est le seul dédoublonnage justifié.
