> Campagne : **toutes-langues** · expérience **78**
> Titre : 78. Le corpus Wikipedia apparié est COMPLET : 482 articles × 6 langues, 2 892 traces
> Date réelle : **2026-10-07 04:56 HAE** (source : commit `f8758eb`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 78. Le corpus Wikipedia apparié est COMPLET : 482 articles × 6 langues, 2 892 traces

| | |
|---|---:|
| articles | **482 / 482** |
| traces | **2 892 / 2 892** |
| échecs | **0** |
| articles présents dans les **six** langues | **482** (100 %) |
| entrées d'apprentissage | 1 446 (de, en, fr) |
| entrées de test | 1 446 (es, it, pt) |

Le traçage a duré **~13 heures** à ~19 s par trace, après les corrections du §52 (un
processus orphelin qui volait 18 cœurs et multipliait les durées par 2,5).

**Le corpus aligné est passé de 85 à 482 articles — un facteur 5,7.** Toutes les mesures
de la traque §57-§77 qui portaient sur 85 articles vont pouvoir être resserrées, à
commencer par le résultat central du §75 : **le rapport contenu/langue à 98 % de celui du
professeur par la composition des trois leviers déployables.**

La vérification est lancée et se déclenche seule : intersection des six langues, partage
3 langues apprises / 3 en test, caches couche 8, puis la composition complète.


---

# BILAN — 35 heures contre l'objectif, et contre la raison d'être de Drave

> **AVERTISSEMENT, AJOUTÉ APRÈS COUP.** Ce bilan et la clôture qui le suit ont été écrits
> avant les §82 à §86. Trois de leurs chiffres sont depuis corrigés, et il faut les lire
> avec la correction :
>
> - **« le professeur est à 12,001 »** (§B.2, §C.3) — mesuré sur **trois langues romanes**.
>   Sur six langues, le même professeur, même couche, même corpus, est à **1,697** ; sur sa
>   pire paire (de–en) à **1,494** (§82, §83). La cible était un effet de panel.
> - **« le discriminant dépasse le professeur, 105 % de la cible »** (§80, §B.2) — mesuré
>   **dans-panel**. Hors vivier, en changeant de panel, il retombe à **31–55 %** (§86).
> - **« nous sommes à 2,487 »** (§79) — le chiffre reste juste, mais la **part** du
>   professeur, seule formulation robuste, est de **14 à 23 %** selon le sens du transfert
>   (§85).
>
> Ce qui n'est pas touché par ces corrections : les 392/392 et 400/400 sans échec, la
> couche 8 préférée à la 10 par 41 voix contre 0, le ridge à 0,03, les 2 892 traces, et le
> fait que la séparation contenu/langue se construit entre les couches 3 et 5 (§84).
