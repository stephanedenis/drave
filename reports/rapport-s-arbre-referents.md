# S — L'arbre a une profondeur et les référents sont proposés : 99 candidats à ≥3, 294/371 formes

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : la validation humaine s'était
> arrêtée sur deux manques — « il manque trop souvent de profondeur » et « les référents ne
> semblent pas résolus avant que je tranche ». Le cycle les traite : l'arbre a maintenant un
> **père** et une **profondeur** réelle (**99 candidats sur 359** atteignent la profondeur 3 ou
> plus, contre **277 sur 369** bloqués à 1 avant), et `referents()` propose un antécédent pour
> **294 des 371 formes** pronominales/possessives des 207 phrases ; les **77** qui restent sont
> ceux qui demandent le **contexte d'un paragraphe**. L'exemple complet, en SVG, est
> [`docs/schemas/arbre-referents.svg`](../docs/schemas/arbre-referents.svg).

## Le problème, tel que l'humain l'a posé

La banque de 200 phrases réelles s'est arrêtée après 142 verdicts : les candidats s'affichent
comme une liste de segments plats, et rien ne dit à quoi renvoient « elle », « son » ou « lui »
avant que le valideur tranche. Le chiffre donnait raison à l'humain : 277 candidats sur 369
avaient une profondeur maximale de 1, et l'outil ne proposait **aucun** antécédent pour 371
formes. Une validation qui demande de trancher sur une structure plate et des référents absents
n'est pas une validation, c'est une devinette. Le cycle ne demande donc pas plus de verdicts : il
change ce que l'outil montre.

## L'arbre

`construire_arbre()` prend les segments et leur donne un **père** et une **profondeur**. Le GV
principal est la racine ; les GN (sujet et objet) sont ses enfants ; les GP, REL et SUB
s'accrochent au plus proche segment à gauche d'un type nominal ou verbal. L'indentation (`niveau`)
devient cette profondeur, et non plus un niveau plat par type. Sur « Le chat de la voisine qui
dort sur le toit se réveille », le GV « se réveille » est la racine, le GN « Le chat » est à la
profondeur 1, le GP « de la voisine » à 2, la REL « qui dort sur le toit » à 3. La préposition
seule ne fabrique plus un GP : le « de » orphelin qui apparaissait dans le paragraphe d'Alice a
disparu, et l'arbre y gagne un nœud utile. Sur les 207 phrases, la mesure (`mesure_arbre.py`)
passe de 277/369 candidats à profondeur 1 à **37 seulement** ; 221 sont à 2, **84 à 3, 13 à 4 et
2 à 5** — 99 candidats, soit 27,6 %, ont enfin une vraie profondeur.

## Les référents, et le paragraphe

`referents()` ne résout pas : il **propose**. Pour chaque pronom ou possessif, il liste les GN et
les têtes de GP à sa gauche, les noms propres de la phrase, puis ceux du **contexte** — les
phrases précédentes. Sur les 207 phrases seules (sans contexte), **371 formes** apparaissent dans
**170 phrases** ; **294 ont au moins un candidat** (79,2 %) et **77 n'en ont aucun** (20,8 %) :
ce sont les pronoms en tête de phrase, qui ont besoin du paragraphe. Le paragraphe d'Alice le
montre : « Elle avait pour habitude… » n'a aucun antécédent dans la phrase, mais le contexte
« se dit Alice vivement » donne **Alice** ; « elle » et « lui » la retrouvent. Les candidats
« habitude » et « conseils » sont les faux positifs que l'humain écarte ; le pronom objet « les »
(« qu'elle les suivît ») est classé DET et manqué — deux limites nommées. `donnees/paragraphes.json`
porte **trois paragraphes complets** réels (cible + contexte + antécédent) : c'est l'unité de la
banque suivante, pas la phrase isolée.

## L'arbre SVG

[`docs/schemas/arbre-referents.svg`](../docs/schemas/arbre-referents.svg) est l'exemple rendu par
`arbre_svg.py` : les nœuds du paragraphe d'Alice sont placés par profondeur (GV racine en haut,
GN, GP, SUB en dessous), les arêtes de l'arbre sont pleines, l'antécédent « Alice » est un nœud
de contexte à droite, et les pronoms « Elle », « elle » et « lui » sont reliés par des **flèches
pointillées** à Alice. Le `viewBox` est **calculé** depuis le niveau le plus large, les jetons et
le contexte : 1 020 × 550 pour l'exemple, 1 398 et 1 613 px pour les deux autres paragraphes — le
contenu reste dans le cadre (vérifié sur les trois, le test du cadre). La page est **responsive** :
le header, la légende et le main sont bornés à 1 180 px et centrés, le corps ne déborde pas, et
l'arbre garde sa largeur naturelle avec un **défilement horizontal** dans son cadre quand la
fenêtre est plus étroite. Le SVG a un `<title>`, un `<desc>`, des liens relatifs, et il est valide
au parseur XML ; `arbre_svg.svg_arbre()` est réutilisable pour chaque phrase, et le serveur
l'affiche dans `/paragraphes`.

## Les contrôles

La mesure est la même avant et après, sur les 207 phrases : la profondeur maximale par candidat
passe de 277/369 à 1 à 37/359, et les 371 formes passent de 0 à 294 avec un antécédent proposé.
Le paragraphe d'Alice fournit le contrôle positif : sans contexte, « Elle » n'a aucun candidat ;
avec le contexte, il propose Alice. Le SVG est contrôlé par le parseur XML (racine `svg`,
`viewBox`, `title`, `desc`, classe `ref`) et par `verifier_schemas.py`. Cinquante-deux tests couvrent
l'arbre (profondeur 3, père GP de la REL), les référents (Alice dans les candidats de « Elle » et
« lui ») et le SVG (XML, titre, description, flèches, contenu dans le cadre sur les trois
paragraphes).

## Ce qui pourrait le rendre faux

L'arbre est une **heuristique d'attachement** : le segment le plus proche à gauche n'est pas
toujours le bon père, et une coordination peut déplacer la racine. Les référents sont des
**candidats**, pas une résolution : « habitude » et « conseils » sont proposés à tort, le pronom
objet « les » est manqué, et les 77 formes sans candidat ont besoin d'un contexte que le banc
actuel ne porte pas. Les trois paragraphes sont peu nombreux et viennent d'Alice ; le genre et
l'époque ne sont pas contrôlés. Enfin, la banque partielle (81 lectures / 65 phrases) reste une
trace : elle n'est pas la preuve que l'outil corrigé validera mieux — c'est l'expérience suivante
qui le dira.

## La suite

Le serveur affiche désormais **`/paragraphes`** : le contexte, l'arbre, les référents à trancher
avant le verdict, et le verdict écrit dans `donnees/paragraphes-validations.jsonl` ; le banc de
phrases reste `/`. La validation peut reprendre sur cette page ; la banque suivante part des
**paragraphes complets** (trois pour l'instant, à étendre), avec des identifiants neufs ; la
banque partielle reste archivée. `h050`/`h053` restent les limites de l'analyseur.

## Fichiers

- Sous-module : commits **`b18dbac`** (arbre/référents), **`0422a8c`** (page) et **`4d3a3ca`**
  (cadre) — `construire_arbre`, `referents`, `arbre_svg.py`, `mesure_arbre.py`,
  `donnees/paragraphes.json`, `static/paragraphes.html`, `static/paragraphes.js`, **52 tests**.
- Exemple : [`docs/schemas/arbre-referents.svg`](../docs/schemas/arbre-referents.svg) ;
  l'outil : `tools/structures/arbre_svg.py`.
- Fiche : celle-ci ; état, roadmap et plan mis à jour.
