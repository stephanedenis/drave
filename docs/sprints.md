# Les sprints de 2 h — charte

Ce document dit **comment on travaille**, pas ce qu'on fait (ça, c'est
`docs/roadmap.md` et les sprints eux-mêmes, dans `sprints/`).

## Le boxing

Un sprint dure **2 h**, chronométrées (`tools/sprint.sh`, qui lit l'heure du
système — pas une estimation). Le temps est réel : quand la boîte est pleine, on
s'arrête, même si la dernière chose est presque finie. Ce qui reste va au planning
du sprint suivant, écrit noir sur blanc.

```bash
tools/sprint.sh start "l'objectif, en une phrase mesurable"
tools/sprint.sh status     # à chaque itération : temps restant, commits du sprint
tools/sprint.sh close      # écrit la trame de cérémonie dans sprints/NN-*.md
```

## La cérémonie, à la fin de chaque boîte

Trois parties, dans cet ordre, écrites dans le fichier du sprint :

1. **Revue** — ce qui est livré, avec les chiffres mesurés. Pas d'intention : des
   résultats, et pour chacun le rapport ou la commande qui le porte. Ce qui n'est
   pas fini est dit comme tel (un demi-chantier annoncé vaut mieux qu'un chantier
   maquillé).
2. **Rétrospective** — *garder* / *changer* / *doute*. Une rétro qui ne change rien
   n'est pas une rétro : chaque « changer » doit devenir une action du sprint
   suivant.
3. **Planning** — le sprint suivant : deux à quatre chantiers, chacun avec son
   **critère de succès vérifiable**. Le premier de la liste est l'objectif.

## L'engagement de fin de sprint (definition of done)

Un sprint se ferme **vert**, et c'est non négociable :

- `cargo test --release` passe ;
- les portes de non-régression sont intactes : **Qwen ctx 256 = 19,3885**,
  gpt-oss ctx 256 = **15,1757** (sans `DRAVE_GPU`), et le banc réparti donne
  **0,00e0** en dense ;
- tout est **commité** ; ce qui ne l'est pas est explicitement jeté ou remis au
  planning ;
- la machine est **rendue** (pas de processus de banc qui traîne) ;
- tout chiffre annoncé a sa **source** : un rapport, un journal de mesure, ou une
  commande reproductible.

## Les trois rythmes, et pourquoi ils diffèrent

| rythme | durée | ce qu'il produit |
|---|---|---|
| sprint | 2 h | un incrément mesuré, une rétro, un plan |
| créneau long (3 h) | 3 h | deux à trois chantiers, avec relances de campagne |
| journée | 8 h | plusieurs sprints, et un index (`reports/rapport-session-*.md`) |

Un sprint n'est **pas** une session : une session peut contenir plusieurs sprints,
et c'est la rétro qui dit si le découpage était bon.

## Deux règles apprises à la dure

- **Un banc qui passe ne prouve pas qu'il mesure ce qu'on croit.** Trois
  relectures adversariales ont trouvé 28 défauts sur un créneau, presque tous par
  lecture : la revue d'un sprint inclut donc, quand un chantier est délicat, une
  **relecture déléguée** — elle compte comme une tâche du sprint.
- **Le travail non vérifié ne compte pas.** Un chiffre repris d'un commentaire, un
  drapeau jamais exercé, un « fait » sans commande : la revue les attrape ou ils
  deviennent des dettes écrites dans la rétro.
