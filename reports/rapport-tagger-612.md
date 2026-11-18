# R0.7 — le tagger API sur le gold 612 : POS 0,9572 contre 0,8625 (heuristique), +9,47

> **Ligne de roadmap** : R0.7 (le lecteur) · **Date** : 2026-11-18 11 h 30 → 11 h 40 EST (fenêtre
> remisée) · **Verdict** : ✅ **le tagger API gagne** — POS **0,9572** contre **0,8625** pour
> l'heuristique (**+9,47 points**), porté par les classes **ouvertes** (**0,978** contre 0,7918,
> **+18,6**) ; les classes fermées sont à parité (0,9353 contre 0,9373, −0,2). **0 refus.**
>
> **Dispositif** : [`rapport-tagger-lot-612-prep.md`](rapport-tagger-lot-612-prep.md) (la commande,
> le gold, le coût prédit) · `analyser --jsonl --tagger` puis `evaluer --tagger --json` · gold
> **612 phrases** (hand + reel + synthétique), 3 179 tokens · données
> [`tagger-612-api.json`](tagger-612-api.json).

## Les chiffres

| | heuristique | **tagger API** | Δ |
|---|---:|---:|---:|
| **POS (exactitude)** | 0,8625 | **0,9572** | **+9,47** |
| classes fermées | 0,9373 | 0,9353 | −0,20 |
| **classes ouvertes** | 0,7918 | **0,9780** | **+18,62** |
| attachement, exact | 0,9958 | 0,9958 | 0 |
| refus | — | **0** | — |

**Le coût réel** : 611 appels (608 réseau, 3 cache), **87 550 tokens**, **0,01869 $** remisé
(0,03738 $ plein), **612,6 s** (10 min 13). Le prep avait prédit **608 appels et 87 550 tokens** :
la prédiction par le cache est **exacte à l'unité**.

## Lecture

1. **Le gain est dans les classes ouvertes** (+18,6) : c'est là que l'heuristique lexicale est
   faible (noms/adjectifs/verbes inconnus) et que le modèle tranche. Les classes fermées sont déjà
   à 0,94 pour l'heuristique — le gain y est nul (−0,2, dans le bruit).
2. **L'attachement ne bouge pas** (0,9958 des deux côtés) : le modèle ne dégrade pas ce que
   l'heuristique réussissait, il ajoute le POS.
3. **0 refus** : le lot n'est pas tombé en repli silencieux (un 429 aurait donné des refus ou un
   token count bas) — le contrôle du prep est passé.
4. **Le débit** : 612,6 s pour 608 appels, soit ~1 s/appel — cohérent avec la latence de l'API.

## Les contrôles

- **L'heuristique est le même code, le même gold** : elle rend exactement 0,8625, le chiffre de
  `rapport-etat-r` (HEAD) — la mesure n'a pas bougé sous nos pieds.
- **Le coût prédit = le coût réel** (608 appels, 87 550 tokens) : le prep s'appuyait sur les `usage`
  du cache X3 ; l'écart nul valide la méthode d'estimation.
- **Le cache est neuf** (`mktemp -d`) : sans lui, 604/608 réponses auraient été des rejeux du 15/11
  — un contrôle, pas une mesure. Le log dit `réseau=608, cache=3`.
- **614 lignes JSONL pour 612 phrases** : deux phrases du gold contiennent deux phrases ; l'éval
  garde les 612 items — écart de forme connu, pas une perte.

## Ce qui pourrait le rendre faux

- **Le gold n'est pas gelé** (« vivant » : hand + reel + synthétique) et le `synthétique` (160
  items) a été produit par un modèle — l'or n'est pas humain sur cette part.
- **Fuite possible** : si les 432 items « réel » ont servi à régler l'heuristique, le +9,47 est une
  borne haute ; le test propre demanderait un gold tenu à l'écart.
- **Un seul run, un seul modèle** (`deepseek-chat`) : la version du modèle peut changer ; le coût
  et le score sont datés du 18/11.
- **L'attachement à 0,9958** est peut-être plafonné par le gold (239 cibles) : le tagger ne pouvait
  pas faire mieux que +1.

## Ce que ça change

R0.7 a son chiffre : **0,9572** avec l'API, **0,8625** hors ligne. Le produit peut **router** : les
classes fermées restent à l'heuristique (gratuite, à parité), les **ouvertes** passent à l'API
(+18,6). Le coût du passage complet est de **2 centimes** pour 612 phrases — le seul obstacle est la
dépendance réseau, pas le prix.

## Voir aussi

- [la préparation du lot](rapport-tagger-lot-612-prep.md) · [les données](tagger-612-api.json) ·
  [l'état R](rapport-etat-r.md) · [W2](rapport-tagger-h50.md) · [W3](rapport-tagger-defaut.md)
