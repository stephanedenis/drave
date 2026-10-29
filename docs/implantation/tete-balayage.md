# La tête de balayage (R05) — l'index de spans, avant toute tête

> **Ligne de roadmap** : R0.4 (deuxième tête) · **Code** : `tools/index_spans.py` · **Porte** :
> `tools/porte-balayage.sh` · **Dépend de** : R0.1 (les régions), R0.3 (le banc).

## 1. Le besoin

Le balayage humain trouve « 3 663 » ou « 12 septembre 2025 » sans lire le document : il cherche
une **forme** — un nombre, une date — pas une phrase. Le contrôleur de R0.2 classe des
**passages** ; il ne sait pas qu'un nombre est une réponse possible. La fiche R05 demande un
chemin **classique** d'abord (regex + BM25) ; la tête neuronale ne s'ajoute que si ce chemin ne
suffit pas.

## 2. L'index

| élément | contenu |
|---|---|
| **spans** | nombres (avec séparateurs et unité : « 3 663 octets », « 24,05 % ») et dates (ISO, françaises) |
| **offsets** | `start` en octets dans le **flux** R0.1, `octets` = longueur UTF-8 ; vérifiés (`flux[start:start+octets] == span`) |
| **classement** | BM25 du **passage porteur**, puis ses spans dans l'ordre — le span hérite du score de sa phrase |
| **recherche exacte** | `exact(valeur)` : le balayage d'un terme connu (offset direct) |
| **coût** | 0,1 ms par requête |

## 3. Ce qui est mesuré

| banc | n (questions à valeur numérique) | rappel@10 | temps |
|---|---:|---:|---:|
| lexical (249 questions) | 249 | **0,984** | 0,1 ms |
| paraphrases (84 questions) | 84 | **0,702** | 0,1 ms |

**La porte 1 de la fiche est franchie sur le lexical** (≥ 0,95) : quand la question partage ses
mots avec le document, le span gold est dans les dix premiers. Sur les **paraphrases**, 0,702 :
c'est là qu'une tête serait utile — et c'est là que R0.4 a montré qu'elle **ne paie pas**
(0,575 contre 0,745 pour BM25).

## 4. Les contrôles de la porte

| contrôle | ce qu'il prouve |
|---|---|
| offsets exacts | 223 spans de `format-flux.md`, tous dans le flux |
| rejeu | deux indexations → mêmes spans, mêmes offsets |
| recherche exacte | « 3 663 » trouvé, à l'offset 8036 |
| balayage | la valeur est dans les dix premiers spans |
| terme absent | « zorglub 42 » ne rend rien |
| **terme d'un autre document** | « drave » / « billots » dans `format-flux.md` ne rendent rien |

## 5. Ce qui pourrait le rendre faux

- **le terme de la question est dans le span gold par construction** : sur le banc lexical, le
  rappel@10 mesure surtout que BM25 retrouve la phrase — le span index hérite des limites du
  contrôleur, il ne les dépasse pas ;
- **le classement est celui du passage** : deux spans de la même phrase ont le même score ;
- **les paraphrases** (0,702) ne sont pas résolues : c'est le domaine de la tête, qui échoue ;
- **la tokenisation** : les offsets sont en octets du flux, pas du fichier source ; la provenance
  `prov` donne le fichier, l'offset donne le flux.

## 6. Branché dans le pipeline

`lecture.py --lecteur span` rend le **span** (valeur + offset) au lieu de la phrase :

| voie | questions à valeur (249) | paraphrases (84) | questions mixtes (20) | coût |
|---|---:|---:|---:|---:|
| span | **0,944** | 0,405 | 3/20 | 0,1 ms |
| extractif | 0,851 | 0,286 | **12/20** | ~1 ms |
| modèle | — | **0,381** | — | 1,9 s |

**La question décide de la voie** : un nombre ou une date → le span ; un sens avec les mots du
document → l'extractif ; une paraphrase → le modèle. Le pipeline garde l'extractif par défaut ;
le choix automatique reste à faire.

## 7. Ce que ça change

1. **Le contrôleur peut balayer** : `index_spans` donne au pipeline une action « balayage » qui
   rend des valeurs, pas des passages — le branchement reste à faire ;
2. **La tête de balayage n'est pas ajoutée** : la porte 2 de la fiche (« la tête bat BM25 sur
   les paraphrases ») est le même mur que R0.4, et il est nommé.

## 8. Voir aussi

- [Le graphe de document](document-graph.md) — les régions et les offsets.
- [Le contrôleur](lecteur-controleur.md) — le scoreur que l'index réutilise.
- [La tête de survol](../../reports/rapport-r04-tete-survol.md) — le négatif qui vaut pour elle.
