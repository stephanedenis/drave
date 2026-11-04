# N3 — l'inventaire exécutable : 17 portes vertes, la fiche de backlog était périmée

> **Ligne de roadmap** : N3 · **Date** : 2026-11-04 · **Verdict** : ✅ **N3 couvert et
> vérifié** — les **17 portes de brique** sont vertes en **92 s** (04/11 11 h 32, registre
> `work/portes-n3-cloture/registre.txt`), la chaîne fiche → JSON → porte est **complète**
> (18 portes avec l'inventaire, 20 fiches, 20 JSON, **0 orpheline, 0 référence morte**), et
> l'inventaire devient une **porte** (`porte-n3-inventaire`, autotest **5/5**). ⛔ **deux
> conditions nommées** restent : le **placement** est une métadonnée, le **saut de calcul**
> est conditionnel (N3.2b2). Ce n'est pas une porte manquante, c'est une architecture absente.
>
> **Dispositif** : `PORTES=n3 taskset -c 10-19,30-39 bash tools/toutes-les-portes.sh` sur
> **cpu1** (claim `aeafe951/n3-cloture`, cpu1=4), pendant que N2 tient les deux GPU ;
> **aucun run GPU**, aucun modèle réel : les 17 portes utilisent des `drave-n0` synthétiques
> (132 528 paramètres). Données [`n3-inventaire.json`](n3-inventaire.json).

## 1. La passe : 17/17, 92 s, zéro rouge

| porte | brique | s | verdict (dernière ligne du journal) |
|---|---|---:|---|
| `porte-n3-service` | service natif | 6 | service vivant · `/sante` exact · génération déterministe · 404 |
| `porte-n3-profondeur` | sortie précoce fixe | 6 | profondeur branchée · `/sante` stable · chaque profondeur déterministe |
| `porte-n3-seuil` | décision à seuil | 6 | 0/1 aux extrêmes · mixte à 0,01 · déterministe |
| `porte-n3-cache` | saut de calcul | 6 | sortie changée · **condition K/V nommée** |
| `porte-n3-routes` | routage / k-WTA | 5 | routage vivant · config différente ⇒ sortie différente |
| `porte-n3-sparsite` | `kwta` vs `top_k` | 5 | les deux agissent **séparément** · A déterministe |
| `porte-n3-sparsite-compte` | compteurs d'experts | 4 | compteurs réels · top_k agit sur les experts · kwta sur les canaux |
| `porte-n3-composition` | composition | 6 | service + profondeur + routage + comptage sur les mêmes modèles |
| `porte-n3-pont` | pont natif | 4 | pont branché · A déterministe · **pont nul change la sortie** |
| `porte-n3-placement` | placement | 5 | placement = **métadonnée** · contrôle pont nul détecté |
| `porte-n3-deux-regions` | découpage | 4 | 0..k / k..n **bit-exact** · pont des deux côtés |
| `porte-n3-deux-processus` | deux processus | 5 | fichier de frontière · logits identiques au pas plein |
| `porte-n3-reseau` | TCP localhost | 5 | aucun cache sur le fil · logits identiques au pas plein |
| `porte-n3-refus` | refus | 5 | empreinte refusée (code 4) · même modèle bit-exact |
| `porte-n3-generation` | génération répartie | 9 | deux caches · sortie **bit-identique** |
| `porte-n3-positions` | positions | 5 | position vérifiée pas à pas · désync refusée |
| `porte-n3-service-briques` | pont + placement + seuil | 6 | pont actif · placement métadonnée · seuil **12/0 vs 0/12** |
| **total** | | **92** | **17 vertes, 0 rouge** (code de sortie du registre, jamais le marqueur) |

## 2. La contradiction que la passe a trouvée

Le code n'a pas bougé ; **la documentation, si**. Trois artefacts se contredisent :

- **`N3.1-etat` (29/10)** : « sortie précoce — service : **non** » et « k-WTA / routes :
  **aucune porte, aucun chemin** ». Refutés **le même jour** par N3.2b0
  (`DRAVE_NATIVE_PROFONDEUR`), N3.2b1 (seuil) et N3.3a/b/c (routes, sparsité, compteurs).
- **`N3.4d-couverture` (29/10 21 h 10)** : conclut déjà « chaque opération native a une porte
  verte ou une condition nommée » — c'est la bonne conclusion, et elle n'a pas été propagée.
- **`docs/pilotage/backlog/N3-operations-natives.md`** (lue ce matin) : statut **partiel**,
  étapes 3 « ⏳ une porte par brique » et 4 « ⏳ k-WTA et routes » alors que les 17 portes
  existent et passent ; « il reste un chemin natif distribué » alors que N3.5a–f l'ont mesuré.

C'est le défaut que le dépôt traque appliqué à la documentation : **une affirmation qu'on
croit vraie et qu'on n'a pas relancée**. L'inventaire statique a menti en quatre endroits en
six jours ; l'instrument ci-dessous rend le prochain mensonge **impossible à commiter** — en
tout cas pour les liens, pas pour les phrases.

## 3. L'instrument : `tools/porte-n3-inventaire.sh` (1 s)

`tools/n3_inventaire.py` vérifie, sans aucun run :

1. chaque porte `tools/porte-n3-*.sh` est **citée par une fiche** `reports/rapport-n3*.md`
   (aucune porte orpheline) ;
2. chaque porte citée **existe** et passe `bash -n` (aucune référence morte, aucune porte
   cassée) ;
3. chaque JSON `reports/n3*.json` est **cité par une fiche**, et chaque JSON cité existe
   (la chaîne fiche → données → porte est complète) ;
4. les **seuils de couverture** du 04/11 ne baissent pas : **18 portes, 20 fiches,
   20 JSON** (17 portes de brique + l'inventaire ; 19 fiches + celle-ci ; 19 JSON +
   celui-ci). Perdre un instrument est une régression, pas un ménage.

État mesuré : **18 portes, 20 fiches, 20 JSON, 0 orpheline, 0 référence morte**.

## 4. Le contrôle négatif

- **Autotest 5/5** : dépôt temporaire minimal ; le vérificateur **passe** sur l'état sain et
  **échoue** quand on retire une porte (référence morte), quand on ajoute une porte
  orpheline, quand on retire un JSON, quand on ajoute un JSON orphelin. C'est la porte qui
  doit échouer, et elle échoue.
- **Le contrôle externe est historique** : N3.1 et le backlog ont réellement dérivé ; la
  passe du 04/11 le montre (17/17) alors que la fiche annonçait des étapes non faites. Un
  instrument qui n'aurait rien trouvé n'aurait rien prouvé.
- **Le registre**, pas le marqueur : le verdict se lit par le **code de sortie** de chaque
  porte (`registre.txt`), conformément à `portes.md`.

## 5. Ce qui pourrait le rendre faux

- **Existence ≠ comportement** : l'inventaire prouve que la chaîne de fichiers tient, pas
  qu'une porte mesure quelque chose. Une porte qui dit toujours ✅ passerait l'inventaire ;
  seuls ses propres contrôles négatifs la gardent.
- **Point dans le temps** : 17/17 le 04/11 11 h 32, sur cpu1, pendant les runs N2 ; les
  durées ne sont pas interprétées (ce sont des portes de correction, pas de performance).
- **Les phrases ne sont pas vérifiées** : le backlog peut encore affirmer un chiffre faux ;
  l'outil empêche les liens morts et les orphelins, pas la prose périmée.
- **17 portes du même auteur** peuvent partager un angle mort ; N3.4d le dit déjà — la
  couverture est par brique, pas une preuve d'architecture complète.
- **Les deux conditions** (placement métadonnée, saut de calcul) sont des négatifs mesurés :
  les compter comme « faits » serait le contresens que la fiche évite.

## 6. Ce que ça change — et ce que le hub doit écrire

**N3 est clos sur ses deux négatifs.** Les trois documents à mettre à jour (le hub tient
`en-cours`, `roadmap` et `backlog`) :

- **backlog `N3-operations-natives.md`** : statut `partiel` → **`mesurée`** ; étapes 3 et 4
  `⏳` → **`✅`** ; ajouter la fiche de résultat ci-dessous ; « Ce qui reste » garde les deux
  **conditions** (chemin distribué natif, saut de calcul), pas des portes.
- **roadmap, ligne N** : `N3` → **couvert** (17 portes, inventaire), reste les deux
  conditions.
- **en-cours** : la ligne proposée est
  `- **N3 — clos** : 17 portes de brique vertes (04/11 11 h 32, 92 s, 0 rouge) ; inventaire
  exécutable (\`porte-n3-inventaire\`, autotest 5/5) ; deux conditions nommées (placement =
  métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).`
  et le compteur de portes **82 → 83**.

## 7. Fichiers

- `tools/n3_inventaire.py` — le vérificateur (statique, `--autotest`).
- `tools/porte-n3-inventaire.sh` — la porte (1 s), lancée par `toutes-les-portes.sh`.
- `reports/n3-inventaire.json` — l'inventaire mesuré.
- `reports/rapport-n3-inventaire.md` — cette fiche.
