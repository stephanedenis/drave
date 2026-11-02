# N2 → R1 — Ce que la nuit dit à la ligne « fenêtre »

> **Objet.** Une note de **passage** : ce que N2 a mesuré sur la longueur, la position et la
> fenêtre, et ce que R1.1/R1.2 devraient tester en premier. Les chiffres sont dans les fiches
> citées ; ici, seulement les conséquences.

## Trois faits mesurés

1. **La position absolue est un défaut d'architecture, pas une propriété du corpus.** Sur 3,24 Mo
   (N2.h3) comme sur 186 Mo (N2.j2), la PPL à 256 octets tombe de **14,11 → 3,25** et de
   **9,28 → 4,49** quand les positions sont tirées au hasard à l'entraînement. Le coût est petit
   (+0,15 et +0,36 en domaine) ; le gain à 512 est de **÷2,1 à ÷2,4**.
2. **La fenêtre locale (256) est le second plafond, mais elle n'est pas seule.** Élargir le masque
   à l'inférence ne récupère rien (N2.h3b : 6,13 → 6,37) : c'est l'entraînement sur des contextes
   longs qui manque. Et la **capacité** compte : à 34,3 M, la PPL à 512 passe de 5,67 à **4,19**
   (N2.p), sans changer la fenêtre.
3. **La distillation ne lève pas le plafond.** Les élèves reproduisent la courbe du professeur
   (N2.j4, N2.n) : à 512, la distillation ne gagne rien (5,67 → 5,76) parce que le professeur a la
   même fenêtre.

## Ce que R1.1 et R1.2 devraient tester

- **R1.1 (la position relative)** : remplacer la position apprise absolue par un schéma **relatif**
  (RoPE ou ALiBi), et vérifier que le gain des positions aléatoires (N2.j2) est **reproduit par
  construction** — sans le coût en domaine. Contrôle : la courbe 129→512 doit être plate, et la PPL
  à 128 ne doit pas se dégrader de plus de 0,1.
- **R1.2 (la fenêtre apprise)** : entraîner sur des contextes **plus longs que la fenêtre** (512,
  1 024) avec les positions relatives, et mesurer la PPL à 512/1 024. Contrôle : le modèle doit
  **utiliser** les octets au-delà de 256 — le test est la PPL à 512, pas la PPL à 128.
- **Le facteur capacité** : refaire R1.1/R1.2 au moins à **21,65 M** et **34,3 M**, parce que
  N2.p montre que la longueur s'améliore avec la capacité — un résultat négatif à 11,47 M ne dirait
  rien du régime utile.

## Ce que R1 ne doit pas attendre

- **La porte < 2,5** : elle est à 0,59 sur le corpus propre (N2.h) et ne dépend pas de la fenêtre.
- **La distillation** : elle transporte la fenêtre du professeur ; former un professeur long
  d'abord, distiller ensuite.
- **Le corpus** : R1 est une question d'architecture, pas de données ; les deux se testent
  séparément.

## Fichiers

- Fiches : [`n2-longueur`](rapport-n2-longueur.md), [`n2-longueur-reelle`](rapport-n2-longueur-reelle.md),
  [`n2-capacite-34m`](rapport-n2-capacite-34m.md), [`n2-distillation-reelle`](rapport-n2-distillation-reelle.md).
- Roadmap : R1.1/R1.2 (programme R), N2 (programme N).
