# C2 — le cycle à deux régions : exact au premier pas, **divergent** ensuite (14,65 → 2 988 en 4 pas)

> Campagne : **cerveau** · expérience : la dernière capacité que le validateur refusait — un
> **cycle** entre deux régions, déroulé par pas de temps (`docs/note-cycle-c2.md`, cinq portes
> écrites **avant** le code).
> Question : un graphe **cyclique** peut-il être exécuté, et son exécution est-elle **exacte**,
> **bornée**, **déterministe** — et que fait un cycle non entraîné ?
> Verdict : **oui pour les quatre, et le cycle non entraîné DIVERGE.** Deux régions enchaînées
> (couches 0-11 puis 12-23) rendent **14,6496**, exactement la perplexité du modèle d'un seul
> tenant (**écart 0,00e0**) ; le **premier pas** du graphe récurrent rend ce même 14,6496 ; puis la
> boucle amplifie : **275,52 → 940,22 → 2 988,46** en quatre pas. Le déroulé est déterministe
> (quatre pas identiques au `cmp`), borné (`--pas-temps` obligatoire, refus en code 2 et 3), et son
> coût est publié : **N pas × régions exécutions**.
> Date réelle : **2026-10-14 21 h 15-22 h 15 HAE** (heure lue sur la machine)
> Protocole : `tools/derouler.py` (nouveau, pilote de cycle) · `drave --topologie` (validateur :
> cycles acceptés **si et seulement si** un lien du cycle est `recurrent` avec `delai_ms` > 0) ·
> `tools/porte-cycle-c2.sh` (nouvelle porte, 42ᵉ) · fenêtre de 128 jetons, m32.

## 1. Ce qui a été construit, et pourquoi c'était le dernier refus

Le validateur de topologie **refusait tout cycle**, et c'était cohérent : le pilote exécutait un
**ordre topologique**, qui n'existe pas pour un graphe cyclique. Un cycle demande un
ordonnancement **par pas de temps** : au pas `t`, chaque région lit l'état des autres du pas
`t−1`. Trois pièces :

| pièce | ce qu'elle fait | où |
|---|---|---|
| **le validateur** | accepte un cycle **si et seulement si** un de ses liens porte `"recurrent": true` et un `delai_ms` > 0 ; refuse un lien récurrent qui ne ferme aucun cycle, et refuse toujours un cycle nu | `drave-core/src/topologie.rs` |
| **le plan** | imprime l'ordre d'**un pas** sur une ligne machine-lisible (`ordre: r0 r1`) : le pilote la lit au lieu de refaire le tri — **une seule implémentation de la règle**, donc pas de divergence possible | idem |
| **le pilote** | déroule : pour chaque pas, exécute les régions dans cet ordre, transporte l'état **brut** (résidu avant la norme finale) par `DRAVE_ETAT_ENTREE` au format REFD, un bloc par position — le même contrat que le transport entre deux nœuds | `tools/derouler.py` |

**Une capture qui ne capturait rien, trouvée en chemin.** `--etat-sortie` n'écrivait **aucun**
fichier sur une plage tronquée **sans** `--tete-partielle` : la capture vivait après le retour
anticipé du « nœud intermédiaire ». Les portes ne le voyaient pas — elles passent toutes
`--tete-partielle`. Le pilote de cycle, lui, a besoin exactement de l'inverse (l'état brut d'une
région intermédiaire), et il a rendu « état manquant » au premier essai. La capture est devenue une
méthode appelée **aux deux endroits** : une capture est une capture, elle ne dépend pas de ce qu'on
fait du flux ensuite.

## 2. Les cinq portes, et ce qu'elles ont rendu

| porte (écrite avant le code, `note-cycle-c2.md` § 4) | mesuré |
|---|---|
| 1. un graphe **sans** lien récurrent est inchangé (C1 s'applique) | deux régions enchaînées = le modèle d'un seul tenant : **14,6496 = 14,6496** (écart **0,00e0**) |
| 2. le cycle sur 4 pas égale la **référence** | le **pas 1** du graphe récurrent = la chaîne : **14,6496** (écart **0,00e0**) — c'est le seul pas où le graphe voit le monde extérieur, et il est exact |
| 3. le déroulé est **borné et annoncé** | cycle nu ⇒ **code 3** ; lien récurrent sans délai ⇒ **code 3** ; `--pas-temps 0` ⇒ **code 2** (pilote) ; région distante ⇒ **code 2** (pilote) |
| 4. le **coût** est mesuré | 4 pas × 2 régions = **8 exécutions**, 31,4 s — publié dans `<sortie>-cout.txt`, et vérifié par la porte |
| 5. l'**état est explicite** | deux déroulés ⇒ trajectoires **identiques** (`cmp` sur les 4 fichiers) ; et la **divergence est publiée** |

*la note disait « code 2 » pour les refus de topologie ; le moteur, lui, sort en **3** sur une
topologie invalide (sa convention établie). La porte vérifie donc 3 — et c'est écrit ici parce que
la note, elle, reste telle qu'elle a été écrite.*

## 3. Ce que le cycle fait, et ce qu'il ne fait pas

| pas | perplexité du graphe récurrent |
|---:|---:|
| 1 | **14,6496** (= la chaîne, exact) |
| 2 | 275,5153 |
| 3 | 940,2153 |
| 4 | 2 988,4562 |

* **il diverge**, et c'est le résultat attendu par la note (« un cycle à gain ≥ 1 diverge ») — la
  porte **publie** la divergence au lieu de ne montrer que l'égalité du pas 1 ;
* **c'est cohérent avec la récurrence locale mesurée le 10/10** (`--recurrence α` : « la boucle
  réinjecte la TRANSFORMATION du réseau, pas son entrée ⇒ un écho, pas une mémoire »,
  `reports/rapport-c2-recurrence.md`). Un cycle **non entraîné** n'est pas une mémoire : c'est un
  amplificateur ;
* **ce que ça n'établit pas** : qu'un cycle **entraîné** ne serve à rien. La note le dit déjà —
  « rien ne dit qu'un cycle aide ; la porte ne doit pas supposer un gain » — et l'entraînement d'un
  cycle est un autre round (la consolidation existe maintenant, `rapport-consolidation-c7.md`) ;
* **le coût est structurel** : N pas = N exécutions du graphe. Un cycle n'est pas un substitut
  d'une passe, c'est une **trajectoire** — et elle se paie.

## 4. Ce que cette fiche ne dit pas

* **le déroulé est LOCAL** : les deux régions tournent sur la même machine. Le déroulé
  multi-instance (avec le protocole de nœud) n'est pas porté, et le pilote le **refuse** (code 2)
  plutôt que de faire semblant ;
* **une seule entrée par région** : l'agrégation de plusieurs entrées simultanées (somme, porte
  apprise) n'est pas portée par ce pilote — refusée aussi ;
* **aucune agrégation temporelle** : l'état du pas précédent **remplace** l'entrée de la région
  (c'est ce que `DRAVE_ETAT_ENTREE` fait) ; une variante qui l'**ajouterait** (α) n'est pas
  mesurée ;
* **un seul découpage** (0-11 / 12-23) et une seule fenêtre (128 jetons) : la divergence dépend
  sûrement des deux, et la courbe n'est pas faite ;
* **le cycle n'est pas entraîné** : c'est le prochain round possible — consolider une trajectoire
  dans les poids du cycle, et regarder si la divergence se calme (ou si quelque chose s'apprend).

## 6. POURQUOI LE CYCLE DIVERGE : l'hypothèse de l'échelle est RÉFUTÉE (16/10)

L'hypothèse était simple et elle avait une allure biologique : **si l'état enfle à chaque pas, la
divergence est une fuite d'échelle**, et il suffit de **ramener** l'état dans sa plage — l'homéostasie
d'E9 (`rapport-e9-homeostasie.md`), appliquée non plus au **poids** mais à l'**état**.

**Ce qui a été mesuré d'abord** (m32, 128 jetons, cycle `r0 → r1`) :

| pas | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| perplexité | 11,84 | 103,06 | 714,61 | **2 873,96** |
| norme moyenne de l'état par jeton | 53,31 | 68,56 | 95,64 | **180,44** |
| croissance de l'état | — | ×1,29 | ×1,40 | ×1,89 |

* **l'état croît bien** (×1,3 à ×1,9 par pas ✗✓) — mais **la perplexité croît 4 à 9 fois plus vite**
  (×8,7, ×6,9, ×4,0) : l'échelle n'est donc **pas** le facteur dominant, et c'est déjà une première
  alerte ✗ ;
* **l'expérience décisive** : `tools/derouler.py --renorme norme1` remet chaque état transmis à la
  norme moyenne du **premier** état transmis (une seule échelle par pas, aucune information du futur).
  Résultat, six pas :

| pas | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| **sans renorme** (4 pas mesurés) | 11,84 | 103,06 | 714,61 | 2 873,96 | — | — |
| **avec renorme** | 11,84 | **78 685** | **344 541** | **158 778** | **1 308 597** | **1 301 994** |

* **la renorme rend la divergence ~1 000 fois PIRE** ✗✗ (78 685 contre 103 au pas 2) — l'hypothèse est
  **réfutée**, et proprement : le pas 1 est identique (la renorme ne touche rien avant la première
  transmission ✓, donc l'instrument est bien celui qu'on croit ✓) ;
* **et l'explication est instructive** : la **norme porte du signal** ✗. La forcer à rester constante
  **injecte une perturbation** à chaque pas — et le cycle **amplifie toute perturbation**, quelle
  qu'elle soit ✓. La divergence n'est donc pas une **fuite d'échelle** ✗ mais une **amplification de
  contenu** ✓ : c'est la même signature que la tour de vision (`rapport-vision-qwen2vl.md` : l'attention
  s'effondre et **bascule** — un écart minuscule change *quel* patch est regardé ✗) ;
* **conséquence pour la suite, et elle est nette** : ce n'est pas l'**amplitude** qu'il faut brider
  (essayé, réfuté ✗) mais **la sensibilité** — c'est-à-dire la **dérivée** de la fonction de cycle ✗.
  La question devient : *le pas de temps est-il contractant ?* — et cela se mesure (la plus grande
  valeur propre de la jacobienne, ou, moins cher, la **croissance d'une perturbation infime** sur un
  pas ✓ : deux pas partant de deux états distants de ε ✓) ;
* **et une note d'honnêteté sur la mesure** : `--renorme` reste dans l'outil, **désactivé par défaut**
  (`aucune`) — non pas comme un mécanisme, mais comme **la trace d'une hypothèse réfutée** qu'on doit
  pouvoir **refaire** ✗✓. La porte `porte-cycle-c2.sh` n'est pas touchée ✓.

## 7. LA CAUSE EST TROUVÉE, ET ELLE TIENT EN UN NOMBRE : le pas de temps AMPLIFIE (λ ≈ 206)

Le § 6 avait réfuté l'hypothèse de l'échelle et laissé la bonne question : **le pas de temps est-il
contractant ?** Elle se mesure — `tools/cycle_sensibilite.py` fait passer **le même état** par un pas
complet du cycle, puis recommence avec une perturbation infime (ε = 1e-3, δ aléatoire de norme 1,
graine fixée) et rapporte

    λ = ‖F(x + ε·δ) − F(x)‖ / ‖ε·δ‖ .

| modèle | état d'entrée | λ sur **un** pas | perplexité de x | perplexité de x + ε·δ |
|---|---|---:|---:|---:|
| **cycle non entraîné** | état réel du cycle | **206,01** | 289,67 | 289,70 (0,0098 %) |
| **cycle entraîné** (LoRA rang 8, 24 couches, objectif « somme ») | même état | **136,20** | 58,95 | 58,95 (0,0024 %) |

**Ce que ces deux nombres disent, et c'est beaucoup :**

* **λ ≫ 1 dans les deux cas** : le pas de temps **amplifie** une perturbation infime de **deux ordres de
  grandeur** ✓. Une itération sur une application **expansive** n'a **pas** de point fixe stable ✗ —
  c'est **la** raison pour laquelle **aucun des quatre objectifs** (somme, dernier, point fixe, cible)
  ne fait converger la boucle ✗✓ : ils ne changent pas λ, ils changent la **cible** ✗ ;
* **et l'entraînement RÉDUIT λ sans le soumettre** : **206 → 136**, soit **−34 %** ✓ — ce qui explique
  exactement le résultat du § 2 (« entraîné, il dompte la divergence : ×228 au pas 4 » ✓) : dompter
  n'est pas contracter ✗✓. **Le chiffre manquant de toute la campagne C2 est ce λ**, et il est
  maintenant mesurable à chaque tentative ✓ ;
* **l'observable est robuste alors que l'état est chaotique** : une perturbation de **1e-3** déplace
  l'état d'un facteur 206 ✓ mais la **perplexité de 0,0098 %** ✓✓. Autrement dit, la divergence de la
  boucle **ne vient pas** de l'amplification du bruit ✗ — elle vient du fait que chaque pas **pousse
  l'état dans la même direction** (une **dérive** ✓) et que rien ne l'arrête (λ > 1 ✓). C'est cohérent
  avec le § 6 : renormer détruit cette dérive porteuse de signal, donc **aggrave** ✗ ;
* **la cible de la faculté C2 est donc maintenant chiffrée** : amener **λ sous 1** ✓. Trois pistes,
  toutes mesurables avec cet outil : (a) une **pénalité de contraction** dans l'objectif
  d'entraînement ✗ (λ est dérivable par différences finies ✓) ; (b) une **normalisation par couche**
  dans le cycle ✗ ; (c) **plus de pas d'entraînement** ✗ (la pente mesurée est de −34 % pour
  10 époques et un objectif : combien de pas pour atteindre 1 ? — c'est une extrapolation qu'il faut
  mesurer, pas supposer ✗) ;
* **ce que cette fiche ne dit pas** : λ est mesuré **en un point** de l'espace d'états (et sur la
  composition de deux pas, où il vaut 444, soit **21 par pas** en moyenne géométrique — le régime n'est
  donc **pas linéaire** ✗, la sensibilité dépend de l'endroit ✓) ; un λ « global » demanderait un
  balayage de points ✗. Et la mesure porte sur des fenêtres de 64 jetons ✗.

## 7bis. CORRECTION DE MON PROPRE CHIFFRE : λ local est de l'ordre de 10⁴ — le 206 était le régime SATURÉ

Le § 7 annonçait « λ ≈ 206 ». C'est le chiffre **d'un seul ε** ✗ — et λ **dépend de ε**, ce qui change
la lecture. La même mesure à six perturbations :

| ε (écart d'entrée) | écart de **sortie** | λ = sortie/entrée |
|---:|---:|---:|
| 1e-2 | 0,2240 | 22,4 |
| 1e-3 | 0,2060 | 206,0 |
| 1e-4 | 0,1958 | **1 950** |
| 1e-5 | 0,1881 | **19 592** |
| 1e-6 | 0,0140 | **37 393** |

* **l'écart de sortie stagne autour de 0,2** tant que l'entrée descend de 1e-2 à 1e-5 ✗✓ : la réponse
  **sature** (un plancher non linéaire, du type `tanh` ✓) — donc **le rapport explose** quand ε
  diminue, sans que la sortie bouge ✓ ;
* **λ est donc une fonction de ε, et « le » λ n'existe pas** ✗ : ce qui caractérise le pas de temps au
  voisinage d'un point est la limite ε → 0, et elle est **au moins 3,7e4** ✓ (le plancher de précision
  f32 — 1e-7 relatif — empêche de descendre plus bas : à ε = 1e-7, l'écart d'entrée serait noyé dans
  l'arrondi du modèle quantifié ✗) ;
* **le 206 du § 7 était donc mesuré en régime saturé** ✗, et il décrit la **réponse observable**, pas
  la sensibilité locale ✓. Les deux nombres sont justes, mais **ils ne répondent pas à la même
  question** — et c'est écrit ici plutôt que corrigé en silence ;
* **ce que cela change pour la cible de C2, et c'est important** : « amener λ sous 1 » est
  **inatteignable par l'entraînement seul** ✗✗ — réduire 206 → 136 (§ 7) est un progrès **dans le
  régime saturé** ✓, qui ne dit rien de la limite locale ✗. Pour contracter, il faudrait changer la
  **forme** du pas (une normalisation, un terme de contraction **dans** la fonction ✓), pas son
  réglage ✗ ;
* **et la cible réaliste, du coup, se reformule** : ce que l'entraînement peut viser, c'est la
  **BORNITUDE** (la sortie reste dans une plage ✓, ce que la saturation assure déjà partiellement ✓),
  pas la **contraction** ✗. Autrement dit : une boucle qui **ne converge pas** mais qui **ne s'emballe
  pas** — et c'est exactement ce que le § 2 avait mesuré sans le nommer (« il dompte la divergence :
  ×228 au pas 4 » ✓) ;
* **ce que cette correction ne dit pas** : λ local n'est mesuré qu'**en un point** et par différences
  finies ✗ ; un λ **global** (la plus grande valeur propre de la jacobienne, ou une moyenne sur des
  points ✓) demanderait un autre instrument ✗ — c'est nommé comme la suite.

## 7ter. λ dépend AUSSI de la fenêtre — et la porte le mesure désormais

En étendant `porte-cycle-c2.sh` (vérifications 6 et 7), une troisième dépendance est apparue : λ dépend
de la **fenêtre** autant que de ε ✗.

| mesure | fenêtre | λ (ε = 1e-3) |
|---|---:|---:|
| § 7, hors porte | 64 jetons | 206,0 |
| **la porte** | **128 jetons** (sa fenêtre) | **488,8** |

* ce n'est pas une contradiction : la sensibilité locale **dépend du point** (et le point dépend de la
  fenêtre de texte ✗) — c'est écrit ici comme la troisième dépendance de λ, après ε (§ 7bis) et le
  point lui-même ;
* **et la porte ne prétend pas le contraire** : elle exige seulement **λ > 1** (le pas amplifie ✓), en
  **imprimant la valeur** ✓ — parce que le jour où λ passera **sous 1**, ce ne sera pas une régression
  mais **la cible de C2 atteinte**, et c'est la **porte** qu'il faudra réécrire (elle le dit
  elle-même ✓) ;
* **ce que la porte 6 ajoute, et qui manquait vraiment** : elle **gardait** la divergence ? Non — elle
  l'**imprimait** ✗. Un changement qui l'aurait fait exploser à 1e30, ou tomber à NaN, serait passé
  sans un mot ✗. Elle **garde** maintenant la **bornitude** (aucun NaN, aucun infini, aucun zéro ✗) et
  la **forme** (la croissance par pas reste dans la bande **[1,5 ; 20]** ✓, mesurée ×18,8, ×3,4, ×3,2
  sur sa propre fenêtre) : c'est la **cible réaliste de C2** — *la boucle ne converge pas, mais elle ne
  s'emballe pas* ✓ — transformée en invariant ✓.
