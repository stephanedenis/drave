# Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte

**En une ligne** : un préremplissage de N états peut voyager en **listes creuses**
au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification
dont l'effet **dépend de la longueur du lot**, ce que ce rapport chiffre au lieu de
le cacher.

## Ce que le mode ajoute

Le mode 3 (lot dense) envoie `t × dimension × f32` : simple, sans perte, et c'est
lui qui a rendu le préremplissage réparti fidèle (0,00e0). Le mode 4 envoie le même
lot **en listes** : chaque état est encodé comme le mode 2 (indices par écarts u8
avec échappement vers u16, valeurs i8, une échelle f32 par bloc de 32 canaux) et
**auto-délimité** par un préfixe de 12 octets — `a_j · n_blocs_j · longueur_j` —
dont les trois tailles se lisent avant toute allocation.

Le mode est **avec perte**, comme le mode 2. Le critère n'est donc pas l'égalité
mais la comparaison à ce que le mode 2 coûte déjà.

## Mesuré

Corpus WikiText-2, 256 jetons, 16 jetons par lot, seuil 0,01, deux processus
locaux :

| | octets par jeton | écart local/réparti |
|---|---|---|
| mode 2, un flux par jeton (référence) | 1 608 par flux | 2,74e-2 |
| **mode 4, lots de 16** | **1,5 ko** | **3,03e-2** |

**÷2,3 sur les octets**, et un écart à 1,11× celui du mode 2 (le critère posé était
1,5×).

### Ce que le ratio vaut selon la longueur (relecture adversariale)

Un relecteur a refait la mesure avec des identifiants synthétiques et des
longueurs variées ; le rapport entre l'écart du mode 4 et celui du mode 2 **n'est
pas constant** :

| jetons | mode 4 | mode 2 | ratio |
|---|---|---|---|
| 20 | 2,30e-1 | 4,09e-2 | **5,6×** |
| 40 | 1,11e-1 | — | — |
| 64 | 1,86e-2 | 3,70e-2 | 0,50× |
| 256 | 6,46e-2 | 5,64e-2 | 1,15× |

Deux choses à en tirer, et une à ne pas en tirer :

* sur une **courte** séquence, la quantification du lot coûte cher en relatif
  (5,6× à vingt jetons) ; sur une séquence longue, elle se dilue comme toute erreur
  stationnaire (1,15× à 256, 0,50× à 64) ;
* le **découpage en lots partiels est innocent** : `--limit 20 --lot 20` et
  `--limit 20 --lot 16` (16 + 4) donnent la **même** perplexité (157,3415) et le
  même écart — l'ordre et la frontière des états sont corrects ;
* les deux séries ne se comparent PAS ligne à ligne (corpus différents : le mien
  est le texte WikiText-2, celui du relecteur des identifiants synthétiques). Seul
  le **ratio**, qui est interne à chaque série, se compare — et il est cohérent
  là où les longueurs le sont.

**Conclusion d'usage** : le mode 4 est fait pour les **gros lots** (le
préremplissage), pas pour envoyer trois jetons ; à petite échelle, le mode 3 dense
coûte moins cher en qualité pour 2,3× d'octets, ce qui est souvent le bon échange.

## Les défauts trouvés en le relisant, et corrigés

La relecture adversariale du mode 4 (dix défauts, deux graves) a surtout trouvé des
choses que le banc ne voyait pas :

1. **le plafond R4 n'était pas cumulatif** : chaque état pouvait être légal et le
   total ne pas l'être — un pair annonçait 268 Mo par état sur 74 898 états
   (~19 Po). La mémoire restait bornée (on décode état par état), le temps non.
   **Vérifié après correction**, avec des états bien formés au maximum légal
   (896 actifs, 3 708 octets chacun, 74 898 états annoncés — la borne nominale
   passe) : le serveur refuse à l'état **72 393**, exactement le point où le cumul
   franchit les 256 Mo, en le disant :
   `corps du lot en listes (cumul après l'état 72393) : 268436952 octets au-delà du
   plafond de 256 Mo` — 258 Mo envoyés en 1,4 s, aucun octet de trop décodé ;
2. **le refus de `n == 0` était trop large** — et c'est un correctif de la même
   journée qui l'avait introduit : en modes 1 et 2, `n` est un nombre de PAIRES, et
   une liste VIDE est légitime (seuil au-dessus du maximum, état nul). La session
   `--flux-blocs --act-thresh 1.0 --lot 1` mourait, et le contrôle indépendant du
   dépôt avec elle. Le refus ne vise plus que les modes où `n` est une dimension ou
   un nombre d'états ;
3. `a_j` n'était pas borné par `hidden` (un million d'actifs pour 896 canaux) ;
4. « hors dimension » s'imprimait une fois PAR ÉTAT (200 lignes pour une trame de
   200 états) au lieu d'une fois par message ;
5. le client mourait en SIGABRT sur une réponse de mode ou de taille différents
   (83 octets d'un pair hostile suffisaient) ; il vérifie et le dit ;
6. la comptabilité « par jeton » divisait par `lot` au lieu de Σt : à 20 jetons en
   lots de 16, elle annonçait 0,9 ko par jeton pour 1,45 réels ;
7. `tools/pair_factice.py` ne savait pas lire le mode 4 — donc le mode n'avait
   aucun contrôle par une seconde implémentation, l'invariant même que la
   spécification revendique. Il le lit maintenant, et vérifie les invariants de
   chaque état (nombre de blocs, longueur des paires) au passage.

## Limites connues

* Σa_j n'est pas affiché dans la ligne de transport (elle compte `t × hidden`,
  c'est-à-dire du dense) — cosmétique, noté ici pour ne pas le redécouvrir ;
* `ChargeFlux::actifs()` est du code mort depuis que la comptabilité est par mode ;
* l'échappement d'indice a été prouvé sur l'émetteur (seuil 0,9) mais pas observé
  dans une réponse du serveur.
