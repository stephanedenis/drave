# Le budget d'une DÉCISION — deux monnaies, et la métrique du plan n'en voit qu'une

> Campagne : **cerveau** · expérience : le **budget** d'une décision, faculté par faculté — la
> métrique du projet (« paires par décision », `docs/plan-cerveau-complet.md` § C8).
> Question : combien coûte une décision du cerveau, et **quelle faculté** la rend moins chère ?
> Verdict : **la PROFONDEUR est le levier dominant** (357,8 M paires par décision en complet,
> 119,3 M à 8 couches, 59,6 M à 4 — exactement **linéaire en couches**), et **la fenêtre d'attention
> ne bouge PAS cette métrique** : 119,3 M avec toutes les clés, la moitié ou le quart. Ce n'est pas
> une erreur de mesure : la métrique compte les **projections** (poids × activation), pas les
> **scores d'attention**. Un budget de cerveau s'exprime donc en **deux monnaies** — les paires
> (profondeur, experts, largeur) et les **clés/octets** (fenêtre, puits, quantifiés) — et le plan
> n'en comptait qu'une.
> Date réelle : **2026-10-15 01 h 45-02 h 00 HAE** (heure lue sur la machine)
> Protocole : `drave --entree signal:F --sortie G --ctx 8` puis la ligne « paires par pas » du
> moteur · cinq configurations · même signal, même contexte.

## 1. La table

| configuration | facultés allumées | paires par décision | écart au complet |
|---|---|---:|---:|
| **complet** (24 couches, toutes les clés) | — | **357,8 M** | — |
| **chemin court 8 couches** | réflexe | **119,3 M** | **−66,7 %** |
| chemin court 8 couches + fenêtre 128 + 64 puits | réflexe + attention sélective | **119,3 M** | −66,7 % |
| chemin court 8 couches + fenêtre 64 + 64 puits | réflexe + attention sélective (quart) | **119,3 M** | −66,7 % |
| **chemin court 4 couches** | réflexe profond | **59,6 M** | **−83,3 %** |

Ce que ça dit :

* **la profondeur est le levier qui compte, et il est exactement linéaire** : 24 → 8 → 4 couches
  donne 357,8 → 119,3 → 59,6 M, soit ×3 puis ×2 pour ×3 puis ×2 de couches. C'est le seul levier de
  cette table qui déplace la métrique du plan ;
* **la fenêtre d'attention ne déplace PAS les paires** : 119,3 M avec toutes les clés comme avec le
  quart. La raison est structurelle : la métrique compte les **multiplications des projections**
  (Q, K, V, O, FFN sur toutes les positions), et le nombre de **scores d'attention** n'y entre pas.
  Diviser les clés par quatre divise donc les scores par quatre — et le total ne bouge pas d'un
  chiffre affiché ;
* **conséquence de lecture, et elle est importante pour le plan** : la fenêtre a été mesurée comme
  un levier de **clés, d'octets et de paires d'attention** (`rapport-fenetre-puits-attention.md`,
  `rapport-loi-frontiere-fenetre.md`), et **la métrique « paires par décision » ne le voit pas**.
  Les deux ne se contredisent pas : elles ne comptent **pas la même chose**. Un budget de cerveau
  doit donc être déclaré en **deux monnaies** — et c'est ce que C10 (budgets par lien : octets,
  latence, **paires**) fait déjà, alors que la métrique de décision, elle, est restée sur une seule ;
* **et la qualité de ces raccourcis est mesurée ailleurs** : ÷1,47 (réflexe 8 couches entraîné),
  +0,04 à +7,39 % (moitié des clés selon le texte), etc. — un budget sans qualité ne dit rien, et
  les fiches citées la donnent.

## 2. Ce que ça change pour le carte des facultés

* **ce qui rend une décision moins chère, dans l'ordre mesuré** : la **profondeur** (×3 pour 24 → 8
  couches), puis la **profondeur encore** (×2 pour 8 → 4) — et **rien d'autre dans cette table** ;
* **ce qui rend une décision moins chère en clés** (sans déplacer les paires) : la **fenêtre**
  (÷2 à ÷4) et le **drain** — c'est ce qui compte **en réparti**, où ce sont les octets qui
  voyagent ;
* **ce qui ne coûte RIEN en paires** : la mémoire de travail (`--memoire K` : un tampon lu
  directement), la mémoire épisodique (11 jetons sur 2 048 lus), les délais (le temps, pas les
  paires), les budgets (un contrôle), la trace (un enregistrement) ;
* **ce qui coûte** : la consolidation (un entraînement hors ligne), le cycle (**N pas = N fois** le
  calcul d'un pas), la latéralité (÷2 de calcul pour **aucun gain mesuré**).

## 3. Ce que cette fiche ne dit pas

* **une seule définition de « paires »** (celle du moteur) : les paires d'**attention** ne sont pas
  dans le chiffre, et leur budget propre (clés × positions) n'est pas reporté — c'est la monnaie qui
  manque ;
* **rien sur les octets ni le temps** : la table est en paires seulement ; les budgets d'octets et
  de latence sont mesurés ailleurs (C10, `porte-budget.sh`) ;
* **rien sur les experts** : un modèle routé économise des experts (le cœur du projet), et cette
  table est sur un modèle **dense** — les deux budgets ne sont pas comparés ici ;
* **un seul contexte** (8 pas) : le coût des clés croît avec la position, donc la part de
  l'attention dans le total **grandit avec le contexte**, et l'équilibre des deux monnaies change
  avec lui — ce n'est pas mesuré.
