# 2026-10-28 — état ancien migré de `en-cours.md`

> **Pourquoi.** La page vivante ne garde que la session courante. Les résultats et tableaux de bord de plus
> d'une journée — et les chantiers terminés — sont migrés ici, avec leurs liens. Les chiffres restent dans
> `reports/`.

## A7 — grappe déportée (terminé au 27/10)

- **A7.5** : transport TCP sparse, **4,44×** moins d'octets, fidélité 100 %, **0,125 ms** loopback.
- **A7.6** : couche 12 de Qwen 0.5B à distance, **logits bit-à-bit** 3/3, **ΔPPL 0**, RTT **4,05 ms**,
  **4 105 o/jeton** ; négatifs RoPE **5,08**, bfloat16 **0,456**, eager **3,59**.
- **A7.7** : int8 par tenseur **argmax 0** ; par jeton **0,83–0,93** ; négatif.
- **A7.8–A7.15** : int8 par canal **ratio 36–39 %**, **argmax 1,0**, PPL **54,86 vs 55,94** ; cache KV int8
  **32/64** jetons identiques ; **128** jetons divergence **77** ; mixte f32→int8 **237/92,6 %** ; seuils
  **64** meilleur ; **3 prompts** **84,19 %**.
- **A7.16–A7.26** : cache KV int8 stocké **32/64** identiques, **128** divergence **77**, par bloc **41/32,8 %**,
  mixte **237/92,6 %**, seuil 64, **3 prompts 84,19 %**.

## B10–B27 — langue, sémantique, modules (terminés)

- **B10** : encodeur **0,426** contre 0,167 ; décodeur **négatif** chrF **14,0 / 5,4** contre **38,8**.
- **B11** : codec **528/528**, restitution **100 %** ; natif **59,8 / 40,7 %** ; surface **33/79**.
- **B12** : M1 **528/528** solide ; M2 vu ; M3 tautologique ; M4 lookup ; M5 contexte ; M6 sélecteur ; M7
  plafond **3,64 %** ; M8 **marginal**.
- **B13–B23** : chaînes, mémoire LFU, restitution, secours, typos, routeur ; intégration mesurée.
- **B24** : routeur confiance, typo **+7,5**, espaces **−7,5**, oracle **79,45 %**.
- **B25** : M8 rejeu exact **0**, champs **74,6 %**.
- **B26** : M6 conflit **0**, commutation **0**, sélecteur sans compétition.
- **B27** : M6 moteur exact **100 %**, conflit **0**.

## C3.2c/d/e — familles (terminé)

- **9 familles** : **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %**.
- **IE** : **14,7 %** pour la famille, **54,6–100 %** pour les sous-familles.
- **Uralic** : **46,7 %** pour la famille, **100 %** pour la côte.

## Anciens tableaux de bord

- portes : **49** (46 vertes, 3 rouges ; `porte-occupation-moteur` de contention, verte seule).
- **215/282** fichiers/JSON à l'époque ; **217/284** depuis N1.4/N1.5.
- tests cerveau : **180 OK**, 31 skips.
