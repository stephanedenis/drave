# S — La traduction contrôle le sens : 14/14 référents anaphoriques confirmés par l'anglais, le « les » → « it » retrouvé

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : les trois paragraphes français
> sont des traductions d'*Alice's Adventures in Wonderland* (1865) ; l'original anglais, qui dit
> explicitement *she / her / herself / it*, tranche les référents que le français laisse flotter.
> Les **14 formes anaphoriques** des trois paragraphes sont confirmées — les **2 que l'outil
> manquait** sont retrouvées (« les » → *it* → les conseils ; « l' » → *it* → la boîte) — et la
> traduction **corrige le contexte** de a003, où Alice n'était pas nommée. La page
> `/paragraphes` affiche désormais la source anglaise à côté du français.

## Le dispositif

Le corpus français (`data/corpus_fr_litterature.txt`) contient la traduction d'Alice ; la source
anglaise est l'original de Lewis Carroll, dans l'édition du Project Gutenberg (#11,
[`gutenberg.org/files/11/11-0.txt`](https://www.gutenberg.org/files/11/11-0.txt)). Les trois
paragraphes de `donnees/paragraphes.json` portent maintenant leur `source_en` (la phrase cible en
anglais) et leur `contexte_en` ; la page les affiche sous le contexte français. La traduction n'est
pas un juge : c'est un **lecteur indépendant** qui a déjà résolu les référents pour traduire — et
dont les choix (she / her / it) se comparent aux propositions de `referents()`.

## La table des référents

| # | forme (fr) | source (en) | référent | l'outil | verdict |
|---|---|---|---|---|---|
| a001 | Elle | She | Alice | Alice | ✓ |
| a001 | se (se donner) | herself | Alice | Alice (candidat) | ✓ |
| a001 | elle (bien qu'elle) | she | Alice | Alice | ✓ |
| a001 | **les** (les suivît) | **it** | **les conseils** | **absent (DET)** | **trouvé** |
| a001 | se (se grondait) | herself | Alice | Alice (candidat) | ✓ |
| a001 | lui | her | Alice | Alice (candidat) | ✓ |
| a001 | en (lui en venaient) | — (tears) | les larmes (partitif) | habitude / conseils | non référent |
| a002 | Elle | her (her eye) | Alice | Alice | ✓ |
| a002 | **l'** (l'ouvrit) | **it** | **la boîte** | **absent (DET)** | **trouvé** |
| a002 | y (y trouva) | in it | la boîte | la boîte (1ᵉʳ) | ✓ |
| a002 | en (en verre) | — | — (préposition) | Alice | faux positif |
| a003 | Elle | She | Alice | Alice | ✓ |
| a003 | sa (sa main) | her | Alice | Alice (après contexte) | ✓ |
| a003 | sa (sa tête) | her | Alice | Alice (après contexte) | ✓ |
| a003 | elle (elle se dit) | herself | Alice | Alice (après contexte) | ✓ |
| a003 | se (se dit) | herself | Alice | Alice (après contexte) | ✓ |
| a003 | Lequel | Which way | le choix | absent | non référent |

**14 formes anaphoriques** (12 vues par l'outil, 2 manquées) et **3 non anaphoriques** (les deux
« en », dont une préposition mal classée, et le « Lequel » du choix) : les 14 sont confirmées, les
3 sont écartées. Le cas décisif est le **« les » de « bien qu'elle les suivît rarement »** :
l'outil le classe DET et ne le propose pas ; l'anglais dit *though she very seldom followed
**it*** — le référent est **les conseils**, pas Alice. La traduction trouve ce que l'analyseur
manquait. Le second cas est le **« l' » de « l'ouvrit »** : *she opened **it*** — la boîte.

## Ce que la traduction corrige dans l'outil

Le paragraphe **a003** (« Elle mangea donc un petit morceau… ») n'avait pas Alice dans son
contexte : les candidats de « sa », « elle » et « se » étaient *un petit morceau*, *gâteau*,
*sa main* — jamais Alice. L'anglais dit *She ate… holding **her** hand…* : le référent est Alice.
Le contexte de a003 a été complété avec « … se dit Alice vivement. Elle aperçut alors une petite
boîte en verre… », et les candidats incluent maintenant Alice ; la page présélectionne
l'antécédent pour les pronoms et possessifs personnels (elle, sa, se, lui…), et laisse les
clitiques (*y*, *en*, *l'*) sur leur premier candidat, que l'humain corrige.

## Les structures, vues par la traduction

L'anglais soutient les découpages : la concession « bien qu'elle les suivît rarement » est *though
she very seldom followed it* ; la relative « qui était sous la table » est *that was lying under
the table* ; le GP « sous la table » est *under the table* ; le gérondif « portant sa main sur sa
tête » est *holding her hand on the top of her head*. Mais la traduction révèle aussi deux
limites : le « **si fort que** les larmes lui en venaient aux yeux » est étiqueté **hypothèse**
par l'analyseur (le « si » pris pour un conditionnel), alors que l'anglais *so severely as to bring
tears into her eyes* en fait une **conséquence** ; et le « **de très-bons conseils** » (GP en
français) est *very good advice* (objet direct en anglais), comme « **pour habitude** » (GP) est
*generally* — la traduction montre la structure française, elle ne la valide pas telle quelle.

## Les contrôles

La source est l'**original**, la version française est la traduction : le sens va de l'anglais vers
le français, pas l'inverse. Les 14 formes anaphoriques sont confirmées par un lecteur qui ne
connaît pas nos candidats ; les 2 manquées sont trouvées ; les 3 non anaphoriques sont écartées.
Le **contrôle négatif** est double : l'outil proposait « habitude »/« conseils » pour « elle » et
« lui » (faux positifs que l'anglais écarte), et il classait l'« en » de « en verre » comme pronom
(préposition, faux positif). La traduction ne confirme pas tout : elle **corrige**.

## Ce qui pourrait le rendre faux

La version française est elle-même une **interprétation** (Bué, 1869) : le traducteur a pu
ajouter, couper ou déplacer (« Lequel est-ce ? » devient *Which way? Which way?* — le français
demande « lequel », l'anglais « de quel côté »). L'alignement est au **paragraphe**, pas au mot ;
trois paragraphes ne font pas une preuve ; l'anglais a ses propres ambiguïtés ; et l'API DeepSeek
n'a pas été utilisée (pas de `DEEPSEEK_API_KEY` dans l'environnement) : la **rétro-traduction**
automatique reste à faire quand la clé sera là, par l'API uniquement (règle 11), jamais par un
serveur local.

## La suite

La page `/paragraphes` montre la source anglaise : l'humain peut confirmer les 14 référents et les
quatre verdicts de structure en voyant les deux langues. Ensuite, la **rétro-traduction**
(FR → EN → FR par l'API) mesurera les pertes de sens, et les **71 langues** de l'UDHR (le travail
L) donneront un test de référents à plus grande échelle — le protocole sémantique, pas seulement la
syntaxe.

## Fichiers

- Sous-module : `donnees/paragraphes.json` (`source_en`, `contexte_en`), `serveur.py`,
  `static/paragraphes.html`, `static/paragraphes.js`, `tests/test_serveur.py`, **52 tests**.
- Source anglaise : [Project Gutenberg #11](https://www.gutenberg.org/files/11/11-0.txt), domaine
  public ; traduction française : le corpus.
- Fiche : celle-ci ; page : `http://127.0.0.1:8765/paragraphes` ; état, roadmap et plan mis à jour.
