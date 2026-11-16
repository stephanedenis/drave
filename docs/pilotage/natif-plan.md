# Le plan du natif — de 34 M (collages) à un modèle qui écrit

> **Ce que ce document est.** Le **plan de travail** du modèle natif : les paliers, leur coût, leur
> critère de sortie, l'ordre des chantiers. Il part du diagnostic du 16/11
> ([`rapport-natif-exploitable.md`](../../reports/rapport-natif-exploitable.md)) : le 34 M
> **modélise** (PPL 2,40) mais **ne compose pas** (le banc de génération). Il ne promet pas de
> dates : il nomme les **critères** et les **dépendances**.

## 1. Le diagnostic, en une ligne

**La plomberie est faite** (entraînement, génération, service HTTP/Rust, DRVM, distillation, SFT) ;
**la qualité manque** — et elle se paie en **échelle + données + alignement**, pas en jours.

## 2. Les paliers

| palier | modèle | données | effort (CPU/GPU) | critère de sortie (mesuré) | ce qu'on obtient |
|---|---|---|---|---|---|
| **0 — aujourd'hui** | 34 M | 1 Go | 3,7 h (fait) | PPL 2,40 ; 0,87 de mots valides ; répétition 15 | des collages |
| **1 — le pas suivant** | **100–150 M** | **3–6 Go** | **~2–4 jours CPU** (ou 1–2 j GPU) | **50 octets cohérents sur 3 prompts** (le banc) ; répétition ≤ 3 | des phrases |
| **2 — le produit** | **300–600 M** | **10–20 Go** | **~2–4 semaines GPU** | **une phrase sur deux sans faute** (le juge : notre analyseur) | de la prose courte |
| **3 — le service** | 1–3 Md | 20–60 Go | des mois GPU | un discours + le SFT (le refus, la consigne) | un assistant |

**Le critère du palier 1 est le premier vrai test** : le banc de génération
([`tools/banc_generation.py`](../../tools/banc_generation.py)) le mesure déjà (la répétition, les
mots valides), le banc de grammaticalité
([`tools/banc_grammaticalite.py`](../../tools/banc_grammaticalite.py)) le juge avec notre
analyseur (les GV, le ciment).

## 3. L'ordre des chantiers

1. **La donnée d'abord** (le vrai goulot) : 3–6 Go de français **propre** (le wiki actuel fait
   1 Go ; il faut le compléter — des livres, des articles, avec la licence et le dédoublonnage).
   **Ne pas modifier `data/` sans le propriétaire** (le territoire D).
2. **Le modèle** : le palier 1 (100–150 M) sur la donnée nouvelle, avec **le banc dès le premier
   checkpoint** (pas après).
3. **L'alignement** : au palier 2 seulement — le SFT sur des paires d'instruction (le N4.6 a
   montré que le corpus brut ne suffit pas : 24/24 mémorisés, 0/4 tenus).
4. **Le runtime** : le DRVM + un moteur d'inférence (torch est une dépendance lourde ; le
   conteneur est déjà lisible sans torch — il manque le **calcul**).

## 4. Ce qui ne dépend pas du modèle (et qu'on peut faire maintenant)

- **Le banc** (fait) : la génération, la grammaticalité, le contrôle aléatoire.
- **La carte** (faite) : [`fiche-modele-natif.md`](../../reports/fiche-modele-natif.md).
- **`drave generer`** (fait) : le modèle accessible, avec le caveat.
- **Le DRVM** : l'inspection sans torch (fait) ; l'extraction des tenseurs (à faire).
- **Le juge** : notre analyseur comme évaluateur de la grammaticalité (fait).

## 5. Les risques

| risque | effet | parade |
|---|---|---|
| **le GPU est réservé** (règle 11) | le palier 2 en CPU = des semaines | le palier 1 d'abord (CPU) ; le GPU seulement pour le palier 2 |
| **la donnée** (3–6 Go propres) | le palier 1 bloqué | la collecte est un chantier à part (le territoire D) |
| **la licence** (le wiki, CC-BY-SA) | la distribution du modèle | créditer, partager à l'identique, ou changer de corpus |
| **l'échelle ne suffit pas** | le palier 1 échoue au critère | le critère est mesuré tôt (le banc) ; on arrête sans frais |

## 6. La règle du jeu

**Chaque palier est jugé par le banc, pas par l'impression.** Le critère du palier 1
(50 octets cohérents, la répétition ≤ 3) est **falsifiable** ; s'il n'est pas atteint, on ne passe
pas au palier 2. Le produit `drave` (le bloc linguistique) reste la référence : le natif ne
devient un produit que quand il **bat** le banc, pas quand il a une PPL.
