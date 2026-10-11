# Dessin H — la carte des points de sortie : la borne monte quand on sort tard, mais le gain atteignable s'effondre

> Campagne : **cerveau** · expérience : sortir à **12, 16, 20 ou 22** couches au lieu de 24
> Question : la mesure du dessin H (`reports/rapport-design-H-profondeur-routee.md`) ne portait que
> sur **une** sortie — 16 couches sur 24. Or sortir plus tard rend le chemin court bien meilleur
> (donc la borne plus haute) mais épargne moins de couches. **Y a-t-il un bon point de sortie ?**
> Verdict : **la borne monte bien, mais le gain ATTEIGNABLE s'effondre.**
> (1) l'accord (ce qu'un routeur **parfait** épargnerait sans changer une décision) monte de
> **25,19 %** (sortie 12) à **42,33 %** (sortie 22) — la borne est réelle et croît ;
> (2) le **produit** qui compte — accord × couches sautées — est **maximal au point le PLUS
> précoce** (sortie 12 : **12,6 %** des paires), parce que 25 % de 12 couches battent 42 % de 2 ;
> (3) un routeur **réel** (seuil de confiance) n'atteint la parité qu'à la sortie **22** : 4,7 % des
> jetons sortent tôt, **0,39 %** des paires épargnées — et le +0,05 point de justesse affiché est
> **dans le bruit** (2 001 jetons, erreur-type ≈ 1,1 point).
> Date réelle : **2026-10-11 00 h 15 HAE** (heure lue sur la machine ; la journée a changé en
> cours de mesure, et les deux journaux portent leur date).
> Protocole : `tools/carte-sortie-profondeur.sh` · mesure : `tools/profondeur_routee_oracle.py` ·
> vérification de la chaîne : `tools/verifier_chaine_etat.py` (0,013 % et 0,006 %).

## 1. La carte

Même texte, même découpage (test = positions 1 000 à 3 000, entraînement = positions 3 512 à 7 254,
512 positions de marge), même adaptateur entraîné **pour chaque profondeur de sortie**, même chemin
long (l'état de 24 couches lu par la tête du modèle : **11,9921** de perplexité, **47,73 %** de
justesse, identique dans les quatre colonnes — c'est le même modèle).

| sortie | couches sautées | perplexité du court | justesse du court | **accord** (borne) | paires au mieux | seuil 0,99 : part sortie | justesse globale |
|---|---:|---:|---:|---:|---:|---:|---:|
| 12 / 24 | 12 | 762,0132 | 20,34 % | **25,19 %** | **12,60 %** | 5,0 % | 47,13 % |
| 16 / 24 | 8 | 499,0613 | 23,19 % | **30,93 %** | 10,31 % | 5,1 % | 47,33 % |
| 20 / 24 | 4 | 228,5551 | 30,58 % | **41,98 %** | 7,00 % | 6,6 % | 47,23 % |
| 22 / 24 | 2 | 167,1173 | 28,94 % | **42,33 %** | 3,53 % | 4,7 % | **47,78 %** |

*« paires au mieux » = accord × couches sautées / 24 : ce qu'un routeur **parfait** épargnerait,
sans changer une seule décision.*

## 2. Trois lectures, et la troisième tranche

1. **La borne croît avec la profondeur de sortie** (25 % → 42 %) : plus on sort tard, moins la
   décision change. C'est la confirmation de ce que la fiche précédente supposait sans le mesurer.
2. **Mais le gain utile décroît** : 12,6 % de paires au mieux à la sortie 12 contre 3,5 % à la
   sortie 22. Le meilleur point pour un **oracle** est donc le plus **précoce** testé — et rien ne
   dit que 12 soit l'optimum (8 et 4 couches ne sont pas mesurés, et un chemin court de 8 couches
   serait très mauvais : la perplexité du court passe déjà de 167 à 762 entre 22 et 12).
3. **Un routeur RÉEL, lui, n'atteint la parité qu'à la sortie 22** — et « parité » veut dire ici
   **47,78 % contre 47,73 %**, soit **+0,05 point** sur 2 001 jetons : **dans le bruit**. Aux
   sorties 12, 16 et 20, le seuil de confiance rend **moins** que le chemin long seul. Le gain
   atteignable est donc **0,39 %** des paires (4,7 % des jetons × 2 couches sur 24), c'est-à-dire
   rien.

**Le chiffre à retenir** : entre la borne (12,6 %) et le gain atteignable (0,39 %), il y a un
facteur **32**. Le dessin H n'est pas limité par la borne — il est limité par le fait qu'**on ne
sait pas, sans oracle, quels jetons peuvent sortir tôt**.

## 3. Ce que cette carte NE dit pas

- **elle ne teste pas d'autres points de sortie** : 12, 16, 20, 22 sur 24. Un optimum plus précoce
  (8, 4) n'est pas mesuré, et la tendance (le produit croît vers les sorties précoces) plaide pour
  l'aller voir — mais un chemin court de 8 couches n'a plus grand-chose du modèle ;
- **elle ne teste qu'un texte**, une graine et un type d'adaptateur (linéaire 896×896). Le chiffre
  du chemin court est celui d'un adaptateur **posé après coup**, pas d'un modèle entraîné pour
  sortir tôt — c'est le manque **N4**, et c'est lui qui plafonne la borne ;
- **elle ne mesure pas l'effet sur une génération libre** : la comparaison est jeton par jeton, en
  contexte imposé. Un routeur qui se trompe tôt peut entraîner la suite ailleurs ;
- **le +0,05 point de la sortie 22 n'est PAS un gain** : il est écrit ici pour être lu comme une
  parité dans le bruit, pas comme une victoire.
