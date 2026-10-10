> Campagne : **campagne-benefices** · expérience **22**
> Titre : 22. Les listes ne calculent pas une approximation : les logits sont identiques AU BIT PRÈS
> Date réelle : **2026-10-09 01:55 HAE** (source : commit `69cf405`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 22. Les listes ne calculent pas une approximation : les logits sont identiques AU BIT PRÈS

Le résultat qui compte pour l'architecture, et il tient en une commande. Même
modèle (Qwen2.5-0.5B Q8_0), mêmes 7 jetons, `--logits-bin` écrit les logits
`(positions × 151 936)` en f32 ; on compare les fichiers octet par octet :

| chemin | perplexité (7 jetons) | fichier de logits |
|---|---:|---|
| `--push` (listes) | 920,0752 | 4 254 216 octets |
| `--dense` + `DRAVE_SANS_EMPRUNT=1` | **920,0752** | **identique au bit près** ✅ (`cmp`) |
| `--dense` (blocs Q8_0 empruntés) | 795,0325 | divergent (autre encodage des poids) |

**Le chemin par listes n'approxime rien.** À encodage de poids égal, il produit
les **mêmes octets** que le produit scalaire dense — et la même suite de jetons en
décodage glouton (`[3541, 10908, 1134, 14789, 12422, 355, 13, 356]` des deux
côtés, contre `[512, 13309, 321, 1788, …]` pour le dense à blocs empruntés). Ce qui
diffère entre les deux chemins n'est pas le calcul, c'est **ce qu'on a le droit de
sauter** : un poids nul ne contribue rien, donc l'omettre est exact — et c'est
toute l'architecture.

**Deux conséquences pratiques.** 1) Toute comparaison dense/listes doit fixer
`DRAVE_SANS_EMPRUNT=1`, sinon elle mesure deux quantifications (§ 19). 2) Sur un
modèle **4 bits** la question ne se pose même pas : le moteur n'a qu'un chemin
(`DenseQ4`), sans événements — la forme 4 bits ne paie aucun des deux avantages.
C'est un argument de plus pour entraîner des modèles **creux en 8 bits** (§ 5)
plutôt que d'élaguer des modèles 4 bits.

---
