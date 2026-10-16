# En ce moment

> Ce fichier est **écrit à la main à chaque round** : c'est ce que la page d'accueil du serveur de
> documentation affiche en premier. Il dit l'état **courant**, pas l'histoire (l'histoire est dans
> `journal/` et dans les fiches).

**Mis à jour : 2026-10-16, 00 h 45 HAE.**

## Le travail du moment : la tour de vision

La faculté **perception visuelle** est passée aujourd'hui de « **bloquée par un modèle absent** » à
« **vérifiée à l'entrée** » :

| étape | résultat |
|---|---|
| modèle téléchargé | **Qwen2-VL-2B** (986 Mo) + son **`mmproj`** (710 Mo, 520 tenseurs) |
| bugs d'architecture corrigés | **5** — MLP à deux matrices + quick-GELU · fenêtre locale **conditionnelle** · jetons d'image écrits · **biais des LayerNorm** (ignorés) · **convention de rotation 2-D** (lue dans la source) |
| cause de l'écart avec la référence | **le mmproj a perdu une tranche temporelle** du noyau de patchs (0,00 % sur l'une, absente sur l'autre) |
| embedding de patchs, noyau réparé | **EXACT** — 0,00 % sur les 256 patchs |
| couche 0 **à poids égaux** | **cosinus +1,00000059**, écart **5,9e-06** (l'arrondi f32) |
| les 32 couches à poids égaux | **justes sur les 8 premières** (1e-5 : les conventions sont bonnes) ; au-delà, l'écart croît (1e-3 → 0,75) — la tour **amplifie les arrondis**, et c'est mesuré **sur deux images** (une synthétique qui explose à 33 273, une naturelle qui reste à 249) |
| pourquoi les couches profondes ne se comparent pas | **trouvé** : l'attention **s'effondre** (entropie 3,36 → **0,16** entre les couches 1 et 15) et **bascule** d'un patch à l'autre — l'écart est **discret** (variation totale 0,94), aucune tolérance ne peut le résorber |
| **la tour est VÉRIFIÉE** | couche par couche, **en isolation** (même état d'entrée aux deux implémentations, comparaison de la couche seule) : **écart max 7,58e-06 sur les 31 couches** — les conventions du moteur sont justes dans toute la tour |
| le **PROJECTEUR** | ✅ **VÉRIFIÉ** : cosinus **+0,99997509**, écart **0,71 %** (= la quantification Q8_0). L'écart de 66,6 % d'avant venait de **MA comparaison** — je nourrissais la référence avec l'état en **ordre de lecture** alors que son `view` regroupe les quatre entrées **consécutives** (donc une ligne, pas un bloc) |
| le chemin image, complet | embedding **exact** · 31 couches **isolées à 7,58e-06** · `post_ln` conforme (**+1,00000012**) · projecteur **0,71 %** — la porte vérifie désormais les étapes 5 **et** 6 |
| et une leçon pour moi, deux fois | j'ai tiré **deux** conclusions fausses sur le *code* alors que le défaut était dans **ma mesure** : un « correctif » démenti par un panic (`post_ln` fait 1280 poids), puis un écart de 66,6 % qui venait de l'**ordre de mes entrées**. *L'instrument se vérifie avant la conclusion.* |
| ⚠️ **avertissement** | le **binaire** en place a été construit pendant cette investigation, quand le source portait ce correctif faux : **source et binaire ne sont pas le même programme** jusqu'à la reconstruction, qui aura lieu **dès la fin de la passe en cours** (on ne reconstruit pas pendant une passe). La reconstruction numpy du projecteur ne reproduit pas non plus les jetons du moteur (cosinus +0,8388) : il reste une différence **dans ce que le moteur fusionne**, et l'étape suivante est de le lui **faire écrire** |
| ce qui reste | l'**injection** (le chemin image → jetons du modèle de texte) et la **vision multimodale de bout en bout** (une question sur une image) |
| lecture du dépôt | un **serveur de documentation** est en ligne : `http://localhost:8787/` |

## Nouveau : E9, l'homéostasie synaptique (défini et mesuré ce soir)

Le seul emplacement vide de `docs/biologie-pour-drave.md` est **défini et mesuré** : **l'amplitude
globale du changement plastique**. Résultat : **le coût hors domaine est monotone en l'amplitude**
(−0,58 % à ×0,6 → +1,64 % à ×1,25), et l'**optimum ×0,6-0,75 domine le delta entier** —
m32 **−8,75 %** contre −7,47 %, hors domaine **−0,58 %** contre **+0,33 %**. Le réglage publié
jusqu'ici (delta entier) était donc **hors de l'optimum** ✗. Et l'échelle n'a pas besoin d'un oracle : **minimiser la perplexité du modèle sur un texte NEUTRE** (sa propre activité récente, ni rejouée ni visée) désigne **×0,75** ✓ — une règle qu'un cerveau peut appliquer, lui qui a son activité d'hier et pas le domaine de demain. **Et le réglage se RÉPLIQUE** sur trois volumes de rejeu (3, 10, 20 morceaux) : à chaque fois ×0,6 fait mieux en domaine **et** coûte moins cher hors domaine, avec un bénéfice qui **grandit** avec le rejeu (0,7 point à 3 morceaux, 1,4 point à 20). Un essai **par couche** (§ 1ter) montre que **amortir les couches hautes** est le meilleur profil (−0,65 % hors domaine contre −0,04 % pour l'inverse) — mais l'écart est **petit** et le réglage **uniforme** reste le meilleur en domaine : **une seule échelle suffit**. Fiche : [`reports/rapport-e9-homeostasie.md`](../reports/rapport-e9-homeostasie.md). **Et une porte** (`porte-homeostasie.sh`, la 46ᵉ) vérifie désormais le réglage : ×0 rend le modèle, l'activité croît avec l'amplitude, et la domination de ×0,6 est **reproduite** à chaque passe.

## L'ÉTALEMENT, et sa CONTRE-ÉPREUVE (à lire ensemble)

Un critère de **lot** — choisir les morceaux qui **étalent** le plus les pertes — donnait **−10,80 %**
contre −7,21 % pour le hasard, sur **une** graine. La contre-épreuve :
**trois graines** à 3 morceaux → l'étalement gagne **les trois** (moyennes **−10,53 % contre −8,76 %**)
mais de **1,8 point seulement**, du même ordre que le bruit de graine ✗ ; et à **10 morceaux**, il
**perd** contre le hasard (6,5938 contre **6,5073**) ✗.
→ **Le critère n'est pas établi** ✗ ; en revanche **E9 a passé la même épreuve** : sur trois graines, ×0,6 gagne m32 **et** le hors domaine **à chaque fois**, avec un écart de **1,06 point** pour une dispersion de graine de 0,2 — l'effet est **cinq fois le bruit** ✓. (Deux résultats testés le même soir de la même façon : l'un tient, l'autre non — c'est à cela que sert une contre-épreuve.) ce qui reste solide, c'est la **loi** (rejouer compte plus que
choisir, et les critères de **lot** tiennent mieux que ceux de **morceau**). Et la leçon : **une graine
ne mesure pas un critère**. Fiche : [`reports/rapport-sommeil-selection.md`](../reports/rapport-sommeil-selection.md) § 6 et 6bis.
**Ce qui se compose quand même** : étalement ×0,6 (E9) — le coût hors domaine passe de +1,94 % à **−0,05 %** ✓.
**Et la règle d'E9 tient sur trois graines** : minimiser la perplexité sur un texte **neutre** désigne **×0,75** à chaque fois (courbe en U), sans rien savoir du domaine visé ✓ — c'est ce qui la distingue d'un oracle. (Le critère de **diversité**, lui, était déjà validé sur trois graines : la loi « les critères de lot tiennent mieux » a passé l'épreuve ✓.)

## Où en est le dépôt

* **45 portes**, dernière passe **43 vertes** (les deux rouges sont structurels et connus :
  `porte-indice` et `porte-melange`).
* **La carte des facultés** ([`docs/cerveau-facultes.md`](../docs/cerveau-facultes.md)) : neuf
  facultés faites et chiffrées, six partielles, trois négatives, plus **§ 5 « l'architecture qui
  suit »**.
* **La chaîne complète** tourne en une commande : `tools/boucle-cerveau.sh` (percevoir → retenir →
  se souvenir → consolider → agir).

## Les questions ouvertes (réécrites le 15/10 au soir)

1. **La vision multimodale** : le **chemin image est vérifié** (embedding exact, 31 couches à 7,58e-06, projecteur à 0,71 %) — il reste l'**injection**, c'est-à-dire le **mRoPE** du modèle de langue (un projet).
2. **Le décodage spéculatif** : il manque **~10 % d'accord** ; la loi est `gain > 1 ⟺ p > c`.
3. **Le cycle** : **la cause est trouvée, et elle tient en un nombre** — le pas de temps **amplifie** (λ = **206** non entraîné, **136** entraîné : l'entraînement réduit λ de 34 % **sans le soumettre**). Une application expansive n'a pas de point fixe stable : c'est pourquoi **aucun des quatre objectifs** ne converge. L'hypothèse de l'échelle est **réfutée** (renormer rend la divergence ~1000× pire). **La cible de C2 est chiffrée : amener λ sous 1.**
4. **Le critère de rejeu** : la **diversité** tient (un seuil, validé sur trois graines) ; l'**étalement** ne tient **pas** (effet ≈ bruit, et il perd à 10 morceaux) ; le reste = des ordres de grandeur.
5. **L'homéostasie en ligne (E9)** : l'amplitude est un réglage mesuré (×0,6-0,75, trois volumes, trois graines) et une règle auto-contenue la désigne ; reste une règle qui **mesure en continu**.
6. **La modulation par jeton** : la politique par texte marche, mais exige **deux passes**.


## Comment lire le reste

| document | ce qu'on y trouve |
|---|---|
| [`docs/cerveau-facultes.md`](../docs/cerveau-facultes.md) | **la carte** : chaque faculté, son mécanisme le plus efficient, son coût, son verdict |
| [`docs/etat-cerveau.md`](../docs/etat-cerveau.md) | les douze capacités C1-C12 et l'état de chacune |
| [`reports/`](../reports/) | **une fiche par expérience** (protocole, chiffres, ce qu'elle ne dit pas) |
| [`journal/`](../journal/) | le récit jour par jour, écrit à la main |
| [`docs/references-non-regression.md`](../docs/references-non-regression.md) | les portes, leurs valeurs, et les pièges de lecture |
