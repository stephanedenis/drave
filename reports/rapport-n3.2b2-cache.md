# N3.2b2 — le saut de calcul est réel, mais il n’est pas gratuit

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ⛔ **condition nommée** —
> la profondeur 1 est **2,6× plus rapide** (2,0 ms contre 5,2 ms médians) mais elle rend une
> **sortie différente** ; les couches sautées ne fournissent plus leurs **K/V** aux jetons
> suivants. Un « cache continu » ne peut pas récupérer ces K/V sans les calculer.
>
> **Dispositif** : `tools/porte-n3-cache.sh`, modèle synthétique 8 blocs (graine 7,
> 663 272 paramètres), service plein et `DRAVE_NATIVE_PROFONDEUR=1`, 16 octets générés ;
> données [`n3.2b2-cache.json`](n3.2b2-cache.json).

## Ce qui est mesuré

| régime | temps médian | déterministe | sortie |
|---|---:|---|---|
| plein | **5,2 ms** | oui | référence |
| profondeur 1 | **2,0 ms** | oui | **différente** |

La profondeur 1 est **2,6× plus rapide** et **change la génération**.

## La condition

Ce n’est pas un défaut de mesure : en génération autoregressive, chaque couche sautée pour un
jeton ne produit pas ses **K/V**, dont les jetons **suivants** ont besoin. Un cache continu ne
peut donc pas « rattraper » ces couches sans les calculer. Trois issues, aucune gratuite :

1. **recalculer** le chemin plein quand la confiance manque — aucun gain net ;
2. **stocker tous les K/V** (calcul plein) — aucun gain ;
3. **accepter le modèle tronqué** — la sortie change, ce n’est plus le même modèle.

## Le contrôle négatif

- **Chaque régime deux/trois fois** : déterministe — la différence n’est pas un tirage.
- **Plein contre profondeur 1** : textes différents — le saut change le contenu.
- **Temps médian** : 5,2 ms contre 2,0 ms — le gain de calcul est réel, pas supposé.

## Ce qui pourrait le rendre faux

- **Modèle synthétique** ; un prompt ; trois mesures.
- **Le temps n’est pas la qualité** : plus rapide ne veut pas dire meilleur.
- **La condition K/V** est une analyse de l’architecture, pas une mesure de cache instrumenté.
- **N3.2b2** pourrait être viable avec une architecture différente (cache par jeton, recalcul
  partiel, sortie précoce seulement sur le dernier jeton) — non testée ici.

## Ce que ça change

N3.2b2 est **nommé** : le saut de calcul ne se transpose pas au cache sans coût. N3 reste
**partielle** : la composition avec pont/placement, et une architecture de cache si elle existe.
N3.2b1 (décision à seuil) reste la brique de décision ; N3.2b2 en est la condition.

## Fichiers

- `tools/porte-n3-cache.sh` — la porte.
- `reports/n3.2b2-cache.json` — les mesures.
- `reports/rapport-n3.2b2-cache.md` — cette fiche.
