# S — Les trois limites de la v4 sont fermées : h050, h053 et « si fort que » ; 60/60 types, 142/142 rôles

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : les trois limites nommées du
> cycle précédent sont **fermées**. `h050` (« le triste **fait** demeure ») et `h053` (« le grand
> **lit** ») trouvaient un nom après un adjectif ; le « **si fort que** » était étiqueté
> hypothèse alors que la traduction anglaise en faisait une **conséquence**. Le gold passe de
> **55 à 60 phrases** (la vague 5, `h056–h060`, écrite après les règles et mesurée une fois) et la
> mesure donne **60/60 types**, **142/142 rôles**, **50/50 compléments**, couverture **1,00** ;
> les contrôles restent à **102/142**, **104/142** et **0,10**. Le corpus réel re-mesuré garde ses
> taux (65,5 % de GN+GV sur la littérature propre contre 9,1 % pour le mélange) et compte
> **596/1 184** homographes.

## Les trois fermetures

La première est un **nom après un adjectif devant un verbe** : « Le triste **fait** demeure. »
L'analyseur s'arrêtait au déterminant parce que « fait » est dans le lexique des verbes ; la règle
v6 regarde le mot **précédent** (l'adjectif « triste », ou le déterminant) et le mot **suivant**
(« demeure » est un verbe) : « fait » est un nom, le GN va jusqu'à « Le triste fait », et
« demeure » ouvre le GV. La deuxième est le même nom **en fin de phrase** : « Le grand **lit**. »
Le suivant est la ponctuation, mais l'adjectif « grand » devant suffit : le GN est « Le grand
lit ». La troisième vient de la **traduction** : dans « elle se grondait **si fort que** les larmes
lui en venaient aux yeux », le « si » n'est pas un conditionnel, c'est un **intensif**, et le
« que » ouvre une **conséquence** — l'anglais *so severely as to bring tears into her eyes* le
disait. La v6 ajoute donc l'intensif « si » au GV, et rend au « que » qui suit un adjectif ou un
adverbe le rôle **consequence**. Le lexique des verbes gagne « demeure » et « crier », et un
lexique d'adjectifs (grand, petit, vieille, triste, simple, fort…) sert aux deux règles.

## Le gold et la mesure

Le gold passe à **60 phrases** : les 7 `dev`, les 16 `test`, et **37 holdout** en cinq vagues.
La vague 5 (`h056–h060`) teste exactement les trois fermetures : la conséquence (« Le chien crie
si fort que la maison tremble »), l'hypothèse conditionnelle (« S'il pleut, je reste »), le nom
après adjectif (« La vieille ferme demeure », « La vieille porte ») et le **contrôle négatif** du
« fait » verbe après un nom (« Le chat fait des bonds »). Elle a été écrite **après** les règles et
mesurée **une fois**, comme la vague 4. La mesure donne **60/60 types**, **142/142 rôles**,
**50/50 compléments**, couverture **1,00** ; la holdout seule : 37/37, 80/80, 21/21. Les deux
limites de la vague 4 (`h050`, `h053`) passent désormais, et la conséquence de `h056` aussi.

## Les contrôles

Les trois contrôles sont ceux du cycle précédent, sur les 60 phrases : la **baseline** à rôle
constant par type fait **102/142** (0,718), les **règles coupées** (`roles=False`) **104/142**
(0,732), et les **rôles mélangés** (200 permutations) **0,10** [0,00 ; 0,24]. Le 142/142 n'est donc
pas un rôle répété ni une distribution : ce sont les règles qui lisent les mots. Le **corpus réel**
sert de second contrôle : les taux de GN+GV ne bougent pas (65,5 % sur la littérature propre,
9,1 % pour le mélange, 8,5 % sur le CEGEP OCR), mais les homographes nominaux passent de 1 134 à
**1 184** sur les phrases et la couverture propre de 0,89 à 0,88 — les nouvelles règles changent
des frontières, pas le signal.

## Ce qui pourrait le rendre faux

Le lexique d'adjectifs est une **liste** : « Le fait divers surprend » reste mal découpé parce que
« divers » n'y est pas ; « une demeure » passe par la règle du déterminant en fin de phrase, mais
un nom sans adjectif devant un verbe (« la maison demeure ») peut encore être coupé. Le gold est de
la **même main** que les règles, et la vague 5 a été écrite après elles : elle teste la règle, elle
ne prouve pas la langue. Le 60/60 est un instrument de cohérence, pas de généralité ; les 60
phrases ne couvrent ni la voix, ni les causatives, ni les verbes à double complément. Le corpus
re-mesuré ne mesure pas la même chose que le gold : ses taux sont stables, mais les homographes
comptés sont des **suspects**, pas des erreurs. Enfin, la traduction a trouvé la limite du « si
fort que », pas toutes : « de très-bons conseils » (GP français) reste un objet direct en anglais,
et « Lequel est-ce ? » reste *Which way?*.

## La suite

La page `/paragraphes` affiche la source anglaise et les référents ; l'humain peut y confirmer les
14 référents et les quatre verdicts de structure, maintenant que l'arbre ne coupe plus le « si fort
que ». La **rétro-traduction** (FR → EN → FR par l'API DeepSeek, quand la clé sera là) mesurera
les pertes de sens ; les **71 langues** de l'UDHR donneront un test de référents à plus grande
échelle. La banque de candidats réels (200 phrases, 355 candidats) reste à valider ; `h050` et
`h053` ne sont plus des limites, la prochaine est le **nom après un adjectif hors lexique**.

## Fichiers

- Sous-module : commit **`230d03a`** — `generateur.py`, `donnees/gold-analyseur.json` (60),
  `donnees/mesure-analyseur.json`, `donnees/mesure-corpus.json`, `tests/test_generateur.py`,
  README ; **55 tests**.
- Mesure : `python3 mesure_analyseur.py` (gold 60) ; `python3 mesure_corpus.py --max 50000`.
- Fiche : celle-ci ; état, roadmap et plan mis à jour ; page `/paragraphes` (serveur relancé).
