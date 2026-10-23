# 3. Les modes et les portes — ce que le moteur fait vraiment

> **Périmètre** : ce chapitre relève du programme **moteur** ; la vision est dans [`docs/vision.md`](../vision.md), la roadmap dans [`docs/roadmap.md`](../roadmap.md).

## Six façons de faire tourner le même modèle

![Les modes d'exécution](schemas/modes.svg)

| mode | la commande | ce qu'il répond | ce qu'il ne fait pas |
|---|---|---|---|
| mesurer | `--ppl` | à quel point le modèle prédit un texte | il ne génère rien |
| générer | `--infer` | un texte, jeton par jeton | il ne garde pas la conversation |
| converser | `--chat` + `--prompt` | un tour de dialogue, avec le gabarit du modèle | il ne tient pas l'historique (c'est `tools/chat.py` qui le fait) |
| court-circuiter | `--couches 0:L` | ce que voit la tête posée tôt (le réflexe) | la qualité d'un passage complet |
| observer | `--etat-sortie` | l'état brut, position par position | il ne le réinjecte pas tout seul |
| itérer | le cycle | une pensée qui boucle sur l'état | il ne garantit pas la convergence |
| piloter | `--bus-fichier` | le monde distribué : régions, horloges, budgets | il n'invente pas la topologie |

**Le point important** : les six partagent le **même moteur** — mêmes couches, même attention, même cache.
Ce qui change est le **chemin**, jamais le modèle. C'est pour cela qu'on peut comparer le réflexe au passage
complet : on compare deux chemins sur les mêmes poids, pas deux modèles différents.

## Le réflexe, et sa mesure

Le **réflexe** (C8) est le chemin court : on pose la tête du modèle **tôt**, après L couches, et on accepte
une réponse moins bonne **beaucoup** plus vite.

Le dépôt a mesuré trois choses, et elles se contredisent utilement :

* le chemin court **tombe d'accord 0 %** avec le chemin complet jusqu'à 16 couches, **8,3 %** à 20 — donc
  un réflexe **emprunté** ne vaut rien ;
* une tête **empruntée** à un autre modèle plafonne à 267,98 de perplexité — donc on ne peut pas tricher ;
* mais une tête **distillée** (entraînée à imiter le chemin long) atteint **30 %** d'accord.

*Un réflexe ne se décrète pas : il s'entraîne.*

## Les portes, et pourquoi elles sont le cœur du dépôt

![Les portes](schemas/portes.svg)

Une **porte** est un script qui vérifie une affirmation et **sort en erreur** si elle est fausse. Il y en a
**46**, et une passe complète dure ~97 minutes.

Les trois règles apprises à la dure :

1. **une porte doit pouvoir échouer** — deux portes ne le pouvaient pas (un `sys.exit` non propagé, un
   `rm -f` qui avalait le code) ; elles ont été corrigées ;
2. **le verdict se lit au code de sortie**, jamais au marqueur — une porte peut échouer sans afficher
   d'échec, et un « ✅ » peut venir de l'outil qu'elle appelle ;
3. **une porte rouge qu'on contourne n'est pas une porte** — si elle échoue, on ne commite pas : c'est une
   règle, pas un conseil.

Et depuis cette nuit, la passe écrit un **registre** (`registre.txt`) avec le code de sortie et la durée de
chaque porte : *une passe qui écrit ses codes est une passe qu'on peut vérifier*.
