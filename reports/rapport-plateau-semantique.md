# Rapport — le plateau sémantique, mesuré sur un corpus multilingue réel

**But** (Stéphane) : faire produire au moteur des réponses qui **émulent les
réponses sémantiques des modèles haut de gamme** sur nos corpus multilingues.

**Ce que ça exige d'abord** : un endroit où la représentation ne dépend plus de la
langue. Sans lui, il n'y a rien à émuler. On le mesure par l'**invariance à la
forme de surface** — deux textes de même sens dans deux langues doivent se
ressembler.

## Corpus et méthode

**Article 1 de la Déclaration universelle des droits de l'homme**, dans **10
langues de familles et d'écritures différentes** : deu, eng, nld (germaniques),
fra, ita, por, spa (romanes), rus (cyrillique), hin (devanagari), jpn (japonais).

`tools/plateau_multilingue.py` : pour chaque couche, la similarité cosinus
**moyenne des 45 paires**, sur la représentation de l'énoncé entier, relevée par
`--trace-flux` et lue en DRVF.

## Résultat 1 — le plateau existe, et il est au même endroit relatif

**Qwen2.5-0.5B (24 couches)** :

| couche | 0 | 4 | **10** | 16 | 20 | 23 |
|---|---:|---:|---:|---:|---:|---:|
| cos moyen | 0,174 | 0,601 | **0,649** | 0,573 | 0,363 | 0,280 |
| pire paire | −0,455 | 0,386 | 0,279 | 0,384 | 0,173 | 0,062 |

La forme de surface **s'oppose** en couche 0 (min −0,455). La convergence culmine
à la couche 10, soit **42 % de la profondeur**, puis le modèle **re-spécialise**
vers sa sortie. Le même endroit relatif que la paire FR/EN seule (23/48 = 48 %).

## Résultat 2 — un modèle haut de gamme converge MIEUX, et surtout sur les paires difficiles

**Qwen3-30B-A3B (48 couches)**, mêmes 10 langues, même article :

| | 0,5B (24 c.) | **30B (48 c.)** |
|---|---:|---:|
| pic de convergence | 0,649 (couche 10 = 42 %) | **0,693** (couche 17 = 35 %) |
| **pire paire au pic** | **0,280** | **0,471** (+68 %) |
| largeur du plateau | couches 4-16 | couches **4-42** |
| à la dernière couche | 0,280 | 0,493 |

**Ce que ça dit, et c'est la réponse à la question posée :**

1. **Oui, la qualité se voit dans le plateau.** Le 30B ne fait pas que monter le
   pic (+6,8 %) : il rapproche surtout **les paires que le petit modèle ne
   rapproche pas** — japonais, hindi, devanagari — de 0,280 à 0,471.
2. **Son plateau est bien plus large** (4-42 contre 4-16) : la représentation
   reste sémantique sur 38 couches au lieu de 12.
3. **Il re-spécialise moins** : 0,493 à la sortie contre 0,280.

## La cible mesurable qui en découle

Émuler un modèle haut de gamme sur ce corpus, c'est **amener le plateau du petit
modèle vers celui du grand** :

```
  0,5B aujourd'hui :  pic 0,649 · pire paire 0,280 · plateau 4-16
  cible (30B)      :  pic 0,693 · pire paire 0,471 · plateau 4-42
```

Et la priorité est **la pire paire**, pas la moyenne : c'est là que l'écart est le
plus grand (68 %) et c'est là que se joue « répondre la même chose dans toutes les
langues ».

## Ce que ce rapport ne dit pas

- **10 langues sur 400.** L'UDHR en compte 400 ; l'échantillon couvre quatre
  écritures et quatre familles, ce qui est le minimum pour que la mesure ait un
  sens, mais ce n'est pas l'ensemble.
- **Un seul article** (le premier, le plus court après le préambule).
- **Deux modèles**, de tailles très différentes : l'écart mesuré mêle la taille,
  les données d'entraînement et l'architecture (le 30B est un MoE).
- **L'invariance n'est pas la qualité.** Deux modèles peuvent avoir le même
  plateau et des sorties très différentes. Le plateau dit où la langue cesse
  d'être portée, pas si le sens est juste.

## Résultat 3 — la LECTURE ne rattrape rien (test tenu à l'écart)

Question : peut-on rapprocher les langues **sans rien entraîner**, en changeant
seulement la façon de lire les couches ? `tools/lecture_plateau.py` compare trois
lectures sur les mêmes traces, **6 langues tenues à l'écart de tout entraînement**
(jpn, hin, ell, heb, tha, kor) :

| lecture | cos moyen (meilleur) |
|---|---:|
| **une couche seule** — couche 4 | **0,6027** |
| moyenne de 3 couches voisines — [8,9,10] | 0,5867 |
| moyenne pondérée par l'inverse de la dispersion | 0,5574 |

**Aucune combinaison ne bat la meilleure couche seule : combiner DILUE.** Les
couches ne portent pas la même chose, et les moyenner ne fabrique pas
l'invariance qui manque.

## Ce que les trois résultats disent ensemble

1. Le plateau **existe** et il est au même endroit relatif dans les deux modèles.
2. **Le grand modèle converge mieux** — pic 0,693 contre 0,649, et surtout pire
   paire 0,471 contre 0,280.
3. **La lecture ne rattrape rien** (0,6027 au mieux, la combinaison fait pire).
4. **Une règle locale non ciblée ne rattrape rien non plus** — elle ne transfère
   pas, et sur des langues non vues elle **dégrade** de 5 à 10 %
   (`docs/note-cancellation-evenementielle.md` §9).

**L'écart sémantique entre le petit et le grand modèle est donc DANS LES POIDS.**
Il n'est ni dans la façon de lire, ni accessible par une règle locale qui n'a
aucune raison de préférer l'invariant au spécifique.

**Ce qu'il faudrait pour le réduire** — et c'est nommé, pas supposé :
une règle **contrastive** (anti-Hebbien sur le différentiel inter-langue), avec
deux conditions non remplies aujourd'hui : un **alignement au niveau du jeton**, et
un **terme qui récompense l'invariant**. C'est un travail de conception, pas un
réglage.

---

## CORRECTION (mesurée plus tard, sur d'autres corpus et d'autres panels)

Ce rapport place le pic de convergence à la **couche 10** (42 % de profondeur) pour
Qwen2.5-0.5B. **Deux mesures ultérieures le placent deux crans plus haut :**

| corpus | couche 8 | couche 10 |
|---|---:|---:|
| Romeo and Juliet (24 scènes appariées) | **0,5985** | 0,5703 |
| UDHR propre (46 langues) | **0,5471** | 0,5247 |

**Conséquence pratique** : émuler la couche 10 revient à apprendre une couche déjà
**en re-spécialisation** vers la sortie. En prenant la couche 8 pour cible, la
fidélité **transférée** à une langue jamais vue gagne **+0,0213** (0,5802 → 0,6015),
au prix de 0,0036 d'invariance de sortie.

Le pic mesuré ici à 42 % était vraisemblablement un artifact du corpus initial —
**l'article 1 de l'UDHR avec 40 langues**, soit un seul énoncé court par langue.

Détail dans `reports/rapport-toutes-langues.md`, sections 17 et 19.
