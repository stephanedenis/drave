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
