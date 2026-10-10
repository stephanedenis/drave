> Campagne : **campagne-benefices** · expérience **40**
> Titre : 40. Protocole v7 : la fenêtre d'attention voyage, et le refus disparaît
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 40. Protocole v7 : la fenêtre d'attention voyage, et le refus disparaît

Le §39 avait montré que `--attn-window` **agit en local** (13,1368 → 21,5801) et **pas en
réparti** ; le câblage naïf donnait un résultat **faux et silencieux** (référence locale
195,5685 contre 50,3829 pour le découpage), parce que le pilote appliquait la fenêtre à ses
douze couches et le nœud gardait la sienne. La conduite retenue alors était un **refus
explicite**.

**Le refus est levé par le protocole v7** : trois champs ajoutés au contrat d'échange
(`attn_window`, `swa_pattern`, `attn_sinks`), l'en-tête passant de **79 à 91 octets** et la
version de **6 à 7**.

**Ce que la mesure dit maintenant**, avec `--attn-window 64` en chemin réparti :

| | perplexité |
|---|---|
| référence locale du run réparti | **18,5520** |
| découpage (12 + 12 couches) | **18,5520** |
| **écart de flux** | **0,00e0** |

**⚠️ CORRECTION (12 octobre, round 41) — la conclusion ci-dessus était HÂTIVE.** Le v7
**transporte** bien les trois champs (ils voyagent dans `Act`, le nœud les applique), mais le
**PILOTE ne les applique toujours pas** : `mdl.attn_window`, `mdl.swa_pattern` et
`mdl.attn_sinks` ne sont assignés **nulle part** dans `run_ppl_reparti` (vérifié par lecture du
code). Les deux nombres qui « s'accordaient » (18,5520 contre 18,5520) s'accordaient parce que
**NI l'un NI l'autre ne changeait** — pas parce que les deux côtés appliquaient la fenêtre.

Mesure refaite au round 41 : à `--limit 128`, `--attn-window 64`, `--swa-pattern 2` et
`--attn-sinks 4` donnent **tous 42,5477**, identiques au run sans drapeau, alors que le même
`--attn-window 64` fait passer le chemin **local** de 13,1368 à 21,5801.

**C'EST FAIT (round 42), ET LA MESURE LE CONFIRME** — trois lignes d'assignation dans
`run_ppl_reparti`, et le réglage cesse d'être inerte :

| | nu | `--attn-window 64` |
|---|---|---|
| **chemin réparti** | 42,5477 | **1 926,1996** |
| chemin local | 14,6496 | 16,1972 |

Le drapeau **agit** désormais en réparti (il ne le faisait pas : 42,5477 dans les deux cas). Que le
chiffre réparti soit mauvais (1 926) est **attendu** : « les 128 derniers jetons d'un fichier de
85 625, avec une fenêtre de 64 » ne laisse presque pas de contexte — mais c'est un calcul
**annoncé**, et non un réglage ignoré.

**La leçon de cette correction vaut plus que la correction elle-même** : **deux nombres égaux ne
prouvent pas qu'ils mesurent la même chose**. Il faut vérifier **pourquoi** ils sont égaux — ici,
la raison était que le réglage était **inerte des deux côtés**.

**Ce qui a failli faire échouer le changement, et qui est maintenant corrigé pour de bon** : les
**tests de trame forgée** construisaient l'en-tête avec un remplissage de **dix mots littéral**.
Passer l'en-tête de 79 à 91 octets faisait tomber neuf tests — non pas à cause du protocole,
mais à cause du littéral. Les constructeurs **calculent** désormais le remplissage à partir de
`TAILLE_TETE` : une modification de protocole se compte en trois endroits (encodeur, décodeur,
**et les tests qui le forgent**), et le troisième ne doit plus être un littéral.

**Vérifications** : `porte-flux.sh` — qui fait parler LES DEUX côtés sur les cinq modes du
protocole — est **vert** avec les écarts inchangés (0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 ·
4,45e-3) : l'en-tête décalé d'un octet y échouerait. **122 tests verts.**
