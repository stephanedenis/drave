# Architecture native Drave — le format et le modèle

> **Décision.** Drave ne doit pas être un consommateur de GGUF ni un petit Qwen3-MoE. GGUF est un
> **conteneur de tenseurs** ; Qwen3-MoE est une **architecture générique**. Les deux supposent un
> modèle **monolithique, dense, exécuté d'un bloc**, alors que Drave est un **graphe de blocs
> événementiels**, avec des sorties précoces, des routes, des contrats d'activation et du rejeu.
> On repart donc **à neuf** : un format **DRVM** et un modèle **`drave-n0`**, entraîné pour ce
> régime, pas adapté après coup.

## 1. Ce qui ne va pas avec GGUF

GGUF sait stocker des **tenseurs** et des **métadonnées** ; il ne sait pas dire :

| ce dont Drave a besoin | GGUF |
|---|---|
| un **graphe de blocs** avec ports et régions | absent |
| des **sorties précoces** et un **réflexe** | absent |
| une **table de routage** (experts, blocs, seuils) | absent |
| un **contrat d'activation** (liste valuée, dtype, échelle) | absent |
| un **rejeu** reproductible (graines, positions, trace) | absent |
| un **placement** par bloc (GPU/CPU/réseau) | absent |
| des **têtes typées** (RSN, champs, codec) | absent |
| une **sparsité** par bloc, pas seulement un tenseur creux | absent |

**Étendre GGUF** revient à ajouter un manifeste, un graphe, des routes, des contrats et un
exécuteur : ce n'est plus GGUF. On garde GGUF comme **format d'import/export** pour les modèles
existants, et on crée **DRVM**.

## 2. DRVM — le conteneur du modèle

**DRVM** (Drave Model) est un conteneur **versionné**, **mmap-able**, **par bloc**, avec quatre
sections :

1. **Manifeste** (CBOR ou JSON compact) : magie `DRVM`, version, hash, provenance, tokenizer,
   schéma RSN.
2. **Graphe** : blocs, ports, régions, routes, sorties précoces, cellule de pensée, ponts.
3. **Tenseurs** : offsets alignés, dtype, forme, quantification, masque de sparsité, échelle par
   bloc ; les **types de quantification** de GGUF (Q4/Q8) peuvent être réutilisés, pas son
   manifeste.
4. **Exécution** : placement, cache, graines, contrat d'activation, tolérances de rejeu.

**Propriétés** : un bloc se lit seul (`mmap`), se place seul, se rejoue seul ; le hash du
manifeste couvre le graphe et les poids ; un lecteur qui ne connaît pas un bloc le **refuse**,
il ne l'ignore pas.

**Trois formats distincts, à ne pas confondre** :

| format | porte | rôle |
|---|---|---|
| **DRVM** | le **modèle** | poids + graphe + routes + contrats |
| **DRVF** | les **activations** | trace, rejeu, transport |
| **RSN** | le **sens** | champs typés, codec, universalaux |

## 3. `drave-n0` — le modèle, pas un Qwen adapté

**Échelle** : **12 M** paramètres, **octets** (vocab 256), **6 blocs**, deux régions.

| étage | choix | pourquoi |
|---|---|---|
| **entrée** | octets 256 + mélangeur local (fenêtre 8) | pas de tokeniseur ; séquences plus longues, mais tête minuscule |
| **bloc** | attention locale (fenêtre 256) + **FFN creux routé** (8 experts, top-2, k-WTA 25 %) + **état récurrent** | le régime Drave : peu d'activations, routes explicites, contexte long |
| **sorties précoces** | têtes après les blocs 2, 4, 6 | le **réflexe** est entraîné avec le modèle, pas ajouté après |
| **pensée** | cellule récurrente contractante sur l'état final | λ < 1 et contenu conservé, mesurés |
| **pont** | projection apprise entre régions | le pont tardif coûte **30×** moins cher que le précoce |
| **sortie** | tête octet + tête **RSN** typée + codec classique | le texte et le sens ne sont pas le même canal |

**Ce qu'on ne fait pas** : pas de MoE générique à 8 experts sans graphe, pas de tenseur dense
monolithique, pas de tokenizer BPE au v0, pas de chat avant les mécanismes.

## 4. L'objectif d'entraînement

Le prochain octet ne suffit pas : il n'apprend ni à sortir tôt, ni à penser, ni à se décomposer.

**Pertes** :

1. **prochain octet** (le socle) ;
2. **distillation** du professeur (séquences et, si disponible, logits) ;
3. **pertes locales par bloc** : chaque région doit rester utile seule ;
4. **pertes des têtes précoces** : la bonne réponse à la profondeur *k* ;
5. **contraction de la pensée** : λ < 1, contenu conservé après *k* pas ;
6. **cohérence du pont** : la sortie d'une région doit rester lisible par la suivante ;
7. **budget de sparsité** : k-WTA 25 %, pas plus.

**Données** : 610 exemples est un **banc**, pas un corpus. Cible v0 : **50 000 séquences**,
UDHR + textes publics + code + dialogue, avec un **jeu tenu à l'écart** et un contrôle par
permutation.

## 5. Les portes de décision

| porte | question | critère |
|---|---|---|
| **N0.1** | DRVM se lit-il ? | aller-retour octet-à-octet, `mmap`, hash, refus de version |
| **N0.2** | le moteur le charge-t-il ? | `drave-core` lit DRVM sans conversion |
| **N0.3** | GGUF reste-t-il importable ? | un GGUF Qwen se convertit en DRVM et rend la même perplexité |
| **N1.1** | l'entraîneur et le moteur sont-ils d'accord ? | même perplexité à 1e-4 près |
| **N1.2** | le réflexe paie-t-il ? | accord de la tête précoce > témoin sans tête |
| **N1.3** | la pensée est-elle contractante ? | λ < 1 et contenu > baseline |
| **N2.1** | la distillation paie-t-elle ? | écart au professeur ≤ **4,40 %** (B9) |
| **N2.2** | les langues tiennent-elles ? | pas de chute > 5 pts sur 30 langues |
| **N3.1** | la sparsité paie-t-elle ? | même qualité, moins d'octets |
| **N3.2** | le rejeu est-il exact ? | trace identique, mêmes logits |
| **N4.1** | le chat est-il utilisable ? | suivi d'instructions, arrêt, multi-tours |

## 6. Ce qu'on garde, ce qu'on jette

**On garde** : le bus, `drave-core`, DRVF, le rejeu, les portes, les mesures B9/B10/B11, les
outils d'entraînement, k-WTA, les têtes précoces, le pont, la discipline du contrôle négatif.

**On jette** : Qwen3-MoE comme base, GGUF comme format natif, le modèle monolithique, le
tokenizer imposé, le chat avant les mécanismes.

**On ajoute** : DRVM, `drave-n0`, les pertes locales, les routes explicites, le manifeste de
graphe.

## 7. Risques, écrits d'avance

- **Trop petit** : 12 M ne parle pas ; c'est un **banc de mécanismes**, pas un assistant.
- **Format trop lourd** : si DRVM devient un second GGUF, on a échoué ; le critère est **un bloc
  lisible seul**.
- **Dépendance au professeur** : la distillation peut plafonner ; le contrôle par permutation et
  le jeu tenu à l'écart sont obligatoires.
- **Octets** : séquences 3–4× plus longues ; le BPE a été **mesuré et écarté** (R13, bits/octet à budget égal) — il reste une condition de réouverture à 50–100 M, pas un prérequis.
- **Données** : sans 50 000 séquences, la capacité ne paie pas — B9 l'a déjà montré.

## 8. La phrase

**On ne cherche plus à faire entrer Drave dans un format et une architecture qui ne sont pas les
siens ; on définit le format et l'architecture qui rendent ses mécanismes mesurables, puis on
entraîne le modèle qui va avec.**
