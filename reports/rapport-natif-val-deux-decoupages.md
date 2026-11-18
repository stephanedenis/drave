# N — la validation change tout : 4,01 ou 4,68 selon le découpage, mêmes poids

> **Ligne de roadmap** : N (le palier 1, la donnée) · **Date** : 2026-11-18 · **Verdict** : mêmes
> poids (73 366 568 paramètres), mêmes **65 536 jetons** notés, même `seq`/`lot` : la perplexité de
> validation vaut **4,0139** sur la **fin du train** (5 %) et **4,6792** sur le **`val.txt` épinglé** —
> **+16,57 %**. Le chiffre dépend du découpage, pas du modèle.
>
> **Dispositif** : `tools/entrainer_native.py` (option `--val` ajoutée) · `work/n2ac/mix1024-100m.pt`
> en init · `data/wiki_mix/propre/val.txt` (10 330 112 o, épinglé `fae5bb73…`) · 65 536 jetons notés,
> seq 1 024, lot 8 · données [`natif-val-deux-decoupages.json`](natif-val-deux-decoupages.json).

## Les deux chiffres

| validation | perplexité | source |
|---|---:|---|
| **fin du train (5 %)** | **4,0139** | `work/n2ac/mix1024-100m.pt.json` (course du 17/11) |
| **`val.txt` épinglé** | **4,6792** | ce banc (`--val`, pin `fae5bb73…`) |
| **écart** | **+16,57 %** | mêmes poids, mêmes jetons |

## Pourquoi c'est important

Le « 2,40 » du 34 M et le « 4,01 » du 73 M ont été mesurés sur la **fin de leur propre train** :
un découpage qui change avec le corpus, sans manifeste. L'alerte du 16/11 l'avait montré
(17,3 à 22,6 selon le morceau) ; ici on le chiffre sur des poids figés : **le choix de la
validation déplace la PPL de 16,6 %**, sans qu'une ligne du modèle change.

Le `--val` et l'épingle donnent désormais un **référentiel** : la PPL d'une campagne se lit avec son
corpus et sa validation (`fae5bb73…`), et deux campagnes sont comparables.

## Les contrôles

- **Même modèle, même nombre de jetons** (65 536), même `seq`, même `lot` : seule la **texture** de
  la validation change — la comparaison est appariée.
- **Le pin est vérifié** : `--verifie` recalcule les empreintes du train, du val et des canaux
  (6,5 s) ; l'épingle `fae5bb73…` est recopiée dans le JSON de la course.
- **La course de 50 pas** (init seule, lr 1e-4) donne 4,6792 — et son `perte_finale` est cohérente
  avec la course d'origine (~1,47 à 1,48) : le chargement des poids est le même des deux côtés.

## Ce qui pourrait le rendre faux

- **La fin du train est aussi « en distribution »** : le val.txt est un fichier distinct (10 Mo) ;
  l'écart mesure un changement de distribution **et** de position dans le corpus, pas seulement la
  difficulté.
- **8 lots de 8 × 1 024 jetons** : l'intervalle de confiance de la PPL n'est pas calculé ; 16 % est
  bien au-delà du bruit attendu, mais il faudrait le vérifier par bootstrap.
- **Une seule paire de fichiers** : un autre corpus peut donner un autre écart.

## Ce que ça change

Toute PPL de la ligne N se lit désormais avec **son** validation et **son** épingle. Le critère du
palier 1 (« 50 octets cohérents sur 3 prompts ») ne dépend pas de la PPL, mais les paliers suivants
si — et ils ne seront comparables qu'à cette condition.

## Voir aussi

- [l'épingle du corpus](rapport-corpus-epingle.md) · [l'alerte de reproductibilité](rapport-native-reproductibilite.md) ·
  [les données](natif-val-deux-decoupages.json) · [le plan natif](../docs/pilotage/natif-plan.md)
