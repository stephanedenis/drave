# S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : la banque passe de **3 à 9
> paragraphes complets**. Les six nouveaux — l'ouverture d'Alice, la table de verre, l'attente à
> la petite porte, « Buvez-moi », « Je me sens toute drôle » et le gâteau oublié — portent chacun
> leur **contexte**, leur **antécédent** (Alice) et leur **source anglaise** (Project Gutenberg
> #11). La page `/paragraphes` en affiche neuf, avec l'arbre, les référents et la source ; les
> **55 tests** passent.

## Les six paires

| id | cible (français) | source (anglais) | réf. |
|---|---|---|---:|
| a004 | « ALICE, assise auprès de sa sœur… commençait à s'ennuyer… » | *Alice was beginning to get very tired…* | 1 |
| a005 | « Tout à coup elle rencontra… une petite table à trois pieds, en verre massif… » | *Suddenly she came upon a little three-legged table…* | 3 |
| a006 | « Comme cela n'avançait à rien… elle retourna vers la table… » | *There seemed to be no use in waiting by the little door…* | 4 |
| a007 | « C'est bien facile à dire « Buvez-moi », mais Alice était trop fine… » | *It was all very well to say "Drink me"…* | 0 |
| a008 | « Je me sens toute drôle… je me ferme comme un télescope. » | *"What a curious feeling!" said Alice…* | 7 |
| a009 | « Un moment après… elle s'aperçut qu'elle avait oublié la petite clef d'or. » | *After a while… she had forgotten the little golden key.* | 5 |

## Les référents, et la page

Les contextes nomment Alice ; `referents()` propose donc les antécédents des pronoms et
possessifs — « sa », « elle », « son », « se » — et la page les présélectionne pour les pronoms
personnels. Le a007 n'a aucun pronom (Alice est nommée), le a004 n'en a qu'un (« sa sœur »), et
le a008 en a sept : c'est le cas le plus riche. La nouvelle règle `PROPRE` accepte les majuscules
d'« ALICE », sans quoi le a004 n'aurait pas eu son antécédent. Les neuf arbres SVG passent le
test du cadre, et la page affiche la source anglaise à côté du français.

## Les contrôles

Les 55 tests passent ; le test du serveur vérifie les **neuf** paragraphes, la présence des
sources anglaises et l'ancrage des référents de a003 ; le test du cadre vérifie les neuf SVG.
La page répond 200 et l'API rend les neuf paires avec `source_en` non vide. La traduction reste
le contrôle du sens : chaque cible a son original anglais, et les référents sont confirmés par
*she / her / herself / it*.

## Ce qui pourrait le rendre faux

Les neuf paragraphes viennent tous d'Alice — même autrice, même traduction française, même
époque : ce n'est pas un échantillon de la langue. Les contextes sont des phrases voisines
choisies à la main ; l'alignement français/anglais est au paragraphe, pas au mot. Les référents
sont des **candidats**, pas une résolution : la page les propose, l'humain tranche. Enfin, la
banque partielle (81 lectures / 65 phrases) reste une trace séparée.

## La suite

L'humain valide les neuf paragraphes sur `/paragraphes` (référents puis structure) ; ensuite la
**rétro-traduction** FR → EN → FR par l'API DeepSeek quand la clé sera là, les **71 langues** de
l'UDHR pour un test de référents plus large, et le **nom après un adjectif hors lexique**
(« Le fait divers surprend ») comme prochaine limite de l'analyseur.

## Fichiers

- Sous-module : commit **`4012729`** — `donnees/paragraphes.json` (9), `generateur.py` (`PROPRE`
  majuscules), `tests/test_serveur.py`, `static/paragraphes.html`, README ; **55 tests**.
- Page : `http://127.0.0.1:8765/paragraphes` (serveur relancé) ; sources anglaises affichées.
- Fiche : celle-ci ; état, roadmap et plan mis à jour.
