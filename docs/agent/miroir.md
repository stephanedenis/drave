# Le miroir de sortie renforce le modèle d'entrée

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de concevoir un test d'entrée**,
> une correction, ou une interface post-linguistique.

## Le principe

Notre **sens → texte** (la sortie) sera toujours **plus léger et plus fiable** que notre **texte → sens** (l'entrée)
✓✓ — parce que l'entrée doit gérer les **imperfections** du réel (bruit, orthographes multiples, langues mêlées,
coquilles), alors que la sortie part d'un sens **propre** ✓. On s'en sert donc comme d'un **miroir**.

## Les quatre règles

1. **Valider l'entrée par la sortie** ✓✓ : ce que l'entrée a compris doit pouvoir être **reproduit** par la sortie
   (restitution à l'identique, ou **boucle** entrée → sortie → entrée). *Si la sortie ne peut pas le redire, l'entrée
   a inventé ou perdu quelque chose* ✗✓.
2. **Découpler le signal du bruit** ✓✓ : la sortie, plus fiable, sert de **référence** pour juger l'entrée — on
   mesure l'écart entre ce que l'entrée a extrait et ce que la sortie sait reconstruire.
3. **Garder des marqueurs de bruit dans l'interface post-linguistique** ✓✓ : le sens extrait porte **où** et
   **combien** l'entrée est incertaine (confiance par token, ambiguïtés non résolues, langues détectées avec leur
   probabilité). *Le module de pensée abstraite doit recevoir un sens **annoté de son bruit**, pas un sens lissé* ✓✓.
4. **Conséquence pour les tests** : toute mesure d'entrée (traduction, contenu, langue) se double d'une mesure de
   **sortie** (restitution, boucle) — c'est le **juge de paix** de l'**étage** ✓✓.

## Ce que les mesures ont ajouté (à ne pas oublier)

- **La fluidité n'est pas la fidélité** ✗✗ : une correction de bruit peut produire un texte **fluide** (surprisal
  basse) qui a **changé le sens** (mesure 65). Le miroir doit valider le **sens** (boucle, comparaison au sens
  extrait), jamais la seule perplexité.
- **Un banc peut mesurer la mémoire** ✗✗ : sur un texte célèbre, un score de surface ne distingue pas la
  **récitation** de la **traduction** (mesure 61). Toute mesure de sortie doit utiliser un texte que le modèle n'a
  pas pu mémoriser, et un test qui **change la source** pour voir si la sortie change.

## Où cela se mesure

`tools/miroir_boucle.py` (boucle entrée → sortie → entrée), `tools/bruit_entree.py` et `tools/seuil_bruit.py`
(marqueurs et seuil de bruit), `tools/traduire_bench.py` (qualité de traducteur). Les chiffres vont dans
[`reports/`](../../reports/), l'état dans [`docs/en-cours.md`](../en-cours.md).
