# R0.7 — la décision de routage du tagger : les options, les chiffres, la recommandation

> **Ligne de roadmap** : R0.7 · **Date** : 2026-11-20 · **Verdict** : **recommandation (b)** — router
> les **classes ouvertes** vers l'API (le gain est là : +18,6 points), laisser les **classes
> fermées** et l'attachement à l'heuristique (la parité : −0,2 et 0), et garder le **défaut hors
> ligne** : l'API ne s'active que si `DEEPSEEK_API_KEY` est présente et que le mode `auto` est
> demandé. **La décision reste humaine** : ce document prépare, il ne tranche pas.
>
> **Les chiffres** viennent de [`rapport-tagger-612.md`](rapport-tagger-612.md) (gold 612 phrases,
> 18/11, fenêtre remisée).

## Les trois options

| option | POS | coût | hors ligne | risque |
|---|---:|---:|---|---|
| (a) heuristique seule | 0,8625 | 0 | oui | le plafond des classes ouvertes (0,7918) |
| **(b) ouvertes → API, fermées → heuristique** | **~0,948** (est.) | 0,019 $ / 612 | oui (repli) | la dépendance à la clé pour les ouvertes |
| (c) API partout | 0,9572 | 0,019 $ / 612 | non | la clé requise pour tout, le coût par phrase |

L'estimation de (b) : les classes fermées (0,9373) et l'attachement (0,9958) inchangés, les
ouvertes à 0,9780 — la moyenne pondérée par la composition du gold donne **~0,948**, à comparer à
0,9572 (c) et 0,8625 (a).

## Pourquoi (b)

1. **Le gain est dans les ouvertes** : +18,6 points, alors que les fermées sont à parité (−0,2) et
   l'attachement identique (0,9958). Payer l'API pour les fermées n'achète rien.
2. **Le repli est gratuit** : sans clé (ou hors ligne), l'heuristique rend 0,8625 — le mode `auto`
   ne casse rien, il améliore quand il peut.
3. **Le coût est négligeable** : 0,01869 $ remisé pour 612 phrases (0,03738 $ plein) — et le lot a
   fait **0 refus**.
4. **Le défaut reste le défaut** : le mode `auto` est un opt-in ; un utilisateur sans clé ne voit
   aucune différence.

## Ce qui pourrait le rendre faux

- Le gold 612 est **petit** et mêlé (hand + reel + synthétique) : les +18,6 des ouvertes ont une
  barre d'erreur que la fiche ne donne pas — un gold plus grand la préciserait.
- La parité des fermées (−0,2) est dans le bruit : l'API pourrait aider les fermées sur d'autres
  textes.
- Le coût extrapolé au corpus entier (des millions de phrases) n'est pas mesuré : 0,00003 $/phrase
  × N — à chiffrer avant un passage à l'échelle.

## La décision demandée

**Rien à coder pour trancher** : le prototype `--tagger auto` existe (opt-in, défaut hors ligne
inchangé). La question est : **adopte-t-on le routage (b) comme comportement par défaut du mode
`auto`** — ouvertes à l'API, fermées à l'heuristique — ou garde-t-on `auto` = l'API partout (c) ?

## Voir aussi

- [le tagger sur le gold 612](rapport-tagger-612.md) · [la préparation du lot](rapport-tagger-lot-612-prep.md) ·
  [le lecteur](../docs/pilotage/roadmap.md#programme-r--le-lecteur)
