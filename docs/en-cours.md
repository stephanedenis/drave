# En ce moment

> Ce fichier est **écrit à la main à chaque round** : c'est ce que la page d'accueil du serveur de
> documentation affiche en premier. Il dit l'état **courant**, pas l'histoire (l'histoire est dans
> `journal/` et dans les fiches).

**Mis à jour : 2026-10-15, 13 h 55 HAE.**

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
| ce qui reste | comparer des quantités **bornées** (poids d'attention, états avant LayerNorm) : au-delà de la couche 8, une sortie de couche ne distingue plus une convention fausse d'un arrondi amplifié |
| lecture du dépôt | un **serveur de documentation** est en ligne : `http://localhost:8787/` |

## Où en est le dépôt

* **45 portes**, dernière passe **43 vertes** (les deux rouges sont structurels et connus :
  `porte-indice` et `porte-melange`).
* **La carte des facultés** ([`docs/cerveau-facultes.md`](../docs/cerveau-facultes.md)) : neuf
  facultés faites et chiffrées, six partielles, trois négatives, plus **§ 5 « l'architecture qui
  suit »**.
* **La chaîne complète** tourne en une commande : `tools/boucle-cerveau.sh` (percevoir → retenir →
  se souvenir → consolider → agir).

## Les cinq questions ouvertes, dans l'ordre

1. **La vision** : les couches profondes à poids égaux (couche par couche, avec leurs poids).
2. **Le décodage spéculatif** : il manque **10 % d'accord** (la rentabilité est exactement `p > c`).
3. **Le cycle** : aucun des quatre objectifs ne le fait converger.
4. **Le critère de choix du rejeu** : cinq essayés, un seul tient (un **seuil** de diversité).
5. **La modulation par jeton** : la politique par texte marche mais exige deux passes.

## Comment lire le reste

| document | ce qu'on y trouve |
|---|---|
| [`docs/cerveau-facultes.md`](../docs/cerveau-facultes.md) | **la carte** : chaque faculté, son mécanisme le plus efficient, son coût, son verdict |
| [`docs/etat-cerveau.md`](../docs/etat-cerveau.md) | les douze capacités C1-C12 et l'état de chacune |
| [`reports/`](../reports/) | **une fiche par expérience** (protocole, chiffres, ce qu'elle ne dit pas) |
| [`journal/`](../journal/) | le récit jour par jour, écrit à la main |
| [`docs/references-non-regression.md`](../docs/references-non-regression.md) | les portes, leurs valeurs, et les pièges de lecture |
