# Note — C2, le cycle à deux régions : ce qui manque, et comment le mesurer

> **2026-10-10 20:09 HAE** (heure lue sur la machine). Note de conception : `docs/` porte les
> hypothèses et les plans ; les mesures vivent dans `reports/`. Ce qui est **déjà mesuré** est
> renvoyé aux fiches ; ce qui reste est écrit comme une **porte à tenir**.

## 1. Où on en est, en trois lignes

| morceau de C2 | état |
|---|---|
| **entrées multiples** (deux régions se somment, la somme arbitre) | ✅ mesuré (C2 : 7/7, bascule à α = 0,60) |
| **récurrence locale** (`--recurrence α` : une région consomme sa propre sortie du pas précédent) | ✅ **implémentée** (déterministe, bornée, gratuite en paires) — et **mesurée nuisible** : elle réinjecte la *transformation* du réseau, pas son entrée (présent : R² 0,906 → 0,112) · `reports/rapport-c2-recurrence.md` |
| **cycle à deux régions** (la validation du plan) | ❌ **refusé par le validateur de topologie**, et c'est cohérent : le pilote exécute un **ordre topologique**, qui n'existe pas pour un graphe cyclique |

## 2. Pourquoi un cycle n'est pas « une boucle de plus »

Une boucle locale (`--recurrence`) vit **dans** une région : elle consomme sa propre sortie **du pas
précédent**, et le pilote n'a rien à ordonner. Un **cycle entre deux régions** (A → B → A) demande
autre chose : à un même pas de temps, A doit produire, B doit consommer, puis A doit consommer le
résultat de B — **au pas suivant**. C'est un ordonnancement **par pas de temps**, pas un ordre
topologique, et c'est exactement ce que le plan écrit : « la récurrence exige un ordonnancement par
*pas de temps* : une région peut consommer sa propre sortie du pas précédent (état explicite par
région) ».

**La conséquence, et elle est structurelle** : un graphe cyclique n'a pas de « une passe = un
résultat ». Il faut **dérouler le temps** : chaque pas de temps exécute le graphe **une fois par
région**, chaque région lisant l'état des autres **du pas précédent**. Le résultat n'est plus une
fonction pure du graphe, c'est une **trajectoire**.

## 3. La conception minimale, mesurable

| élément | proposition | pourquoi |
|---|---|---|
| **déclaration** | `"recurrent": true` sur un lien, avec `delai_ms` **obligatoire** (> 0) | un cycle sans délai n'a pas de solution à un pas de temps donné ; le délai est ce qui rend le graphe **déroulable** |
| **état par région** | chaque région garde son état de sortie du pas précédent (en mémoire du pilote), et le lien récurrent fournit **cet** état | c'est l'« état explicite par région » du plan ; le mécanisme existe déjà (états imposés, REFD) |
| **ordonnancement** | pour chaque pas `t` : ordre topologique du graphe **privé de ses liens récurrents**, puis injection des états récurrents du pas `t−1` | on réutilise l'ordonnanceur qui existe (Kahn) sur le graphe **déroulé** ; rien de nouveau à écrire sinon la boucle de temps |
| **interface** | `--pas-temps N` : nombre de pas déroulés (le cycle tourne N fois) | un graphe déroulé a besoin d'une **borne**, comme `--pas-max` (code 5) |
| **référence** | la validation du plan : « un cycle à deux régions, comparé à une **implémentation de référence en une seule passe sur 4 pas de temps** » | la référence se calcule **sans le moteur** (4 itérations de deux couches linéaires) : c'est ce qui rend la mesure vérifiable |

## 4. Les portes à tenir (écrites AVANT le code)

1. **un graphe sans lien récurrent est inchangé** : C1 s'applique (0,00e0) — la non-régression de
   tout ce qui existe ;
2. **un cycle à deux régions sur 4 pas de temps égale la référence calculée hors moteur**, au
   chiffre près — c'est la validation du plan, et elle doit être **exacte** (aucune tolérance
   floue : les deux implémentations font les mêmes sommes) ;
3. **le déroulé est borné et annoncé** : `--pas-temps N` sans borne explicite est refusé, et un
   cycle **sans délai** est refusé (code 2) — un cycle sans délai n'a pas de solution ;
4. **le coût est mesuré** : N pas de temps = N exécutions du graphe ⇒ les paires par décision
   doivent être **N fois** celles d'une passe (ou N fois celles des régions, si l'on mesure par
   région) — un cycle qui prétend ne rien coûter mentirait ;
5. **l'état est explicite** : deux exécutions identiques rendent la même trajectoire (déterminisme),
   et couper l'état récurrent (le remettre à zéro) doit ramener le résultat à la première
   itération — c'est ce qui prouve que le lien récurrent **est** ce qui porte le temps.

## 5. Ce qui pourrait invalider la conception

- **la divergence** : un cycle à gain ≥ 1 diverge (comme la récurrence locale mesurée aujourd'hui :
  plus α monte, plus la lecture se dégrade). La porte devra donc **publier la divergence** quand
  elle a lieu, pas seulement l'égalité à la référence ;
- **le coût en temps** : N pas de temps = N passes ⇒ un cycle multiplie le coût par N. C'est
  acceptable pour une **trajectoire** (le but) et inacceptable comme substitut d'une passe ;
- **l'utilité** : rien ne dit qu'un cycle **aide** — la mesure d'aujourd'hui (boucle locale) dit même
  le contraire *non entraînée*. La conception doit donc permettre de mesurer **les deux issues**, et
  la porte ne doit pas supposer un gain.

## 5bis. ÉTAT AU 2026-10-14 : les cinq portes sont tenues

L'ordre de travail du § 6 a été suivi, et les cinq portes du § 4 rendent : chaîne de deux régions
**exacte** (14,6496 = 14,6496, écart 0,00e0), **pas 1** du cycle égal à cette référence (0,00e0),
**borné** (`--pas-temps` obligatoire ; cycle nu et récurrent sans délai refusés en **code 3** ;
pilote en **code 2**), **coût publié** (N pas × régions exécutions) et **trajectoire
déterministe** — avec la **divergence publiée** : 14,65 → 275,52 → 940,22 → **2 988,46** en quatre
pas. Une correction de la note, à garder : le § 4 annonçait « code 2 » pour les refus de
topologie, le moteur sort en **code 3**. Deux ajouts que la note n'avait pas prévus : la capture
d'état ne fonctionnait **pas** sur un nœud intermédiaire (corrigé), et le pilote refuse
explicitement le multi-instance et les entrées multiples. Fiche :
[`reports/rapport-cycle-c2.md`](../reports/rapport-cycle-c2.md).

## 6. Ordre de travail proposé

1. le **validateur** : accepter un cycle **si et seulement si** chaque lien du cycle porte un délai
   > 0 et `recurrent: true` — et le dire (`--topologie` affiche le graphe **déroulé**) ;
2. le **déroulé** : `--pas-temps N`, avec la référence hors moteur sur 4 pas et la porte § 4.1/§ 4.2 ;
3. le **coût** (§ 4.4) et le **déterminisme** (§ 4.5) ;
4. alors seulement : une **tâche** qui utilise la trajectoire (poursuite, oscillation, mémoire
   récurrente) — et la question « un cycle entraîné aide-t-il ? », qui est un entraînement.
