# Références de non-régression

> **Dernière passe :**
> **49 portes, 46 vertes, 3 rouges, 1 h 40** (28/10 00 h 12). L'historique des
> passes est dans [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md).
> Les compteurs de la page d'état sont vérifiés par `tools/revue_documentation.py`.

> **Ce que ce fichier porte.** Les repères chiffrés qu'une passe complète imprime, et
> les invariants qui ne sont pas des chiffres. Les mesures de campagne (perplexités,
> budgets, latences) sont dans `reports/` — une fiche par expérience — et non ici :
> ce fichier ne porte que ce qu'une **porte** vérifie.

> **Passe du 2026-10-28 à 00 h 12** (**49 portes, 46 vertes, 3 rouges**, **1 h 40 min**) — la passe
> du programme N. Les deux rouges structurelles (`porte-indice`, `porte-melange`) et
> `porte-occupation-moteur` (contention ; elle passe **verte seule**) ; aucune régression.
> Journaux : [`journal/2026-10-28.md`](../../journal/2026-10-28.md).

> **Passe précédente — 2026-10-27 à 14 h 33** (**49 portes, 47 vertes, 2 rouges**, **1 h 48 min**) — la passe
> finale du sprint 24 h. `porte-indice` **843 s** et `porte-melange` **112 s** restent les deux
> rouges structurelles, avec les mêmes diagnostics ; **aucune régression**. Journaux :
> `/tmp/portes-1027-12h45`.

> **Passe précédente — 2026-10-26 à 14 h 30** (**49 portes, 47 vertes, 2 rouges**, **1 h 34 min**) — la passe de clôture
> de **B9**, avec `porte-deepseek` **incluse** (1 s, **verte** : 20 tests, dry-run, 60 et 310 prompts) et
> `porte-jeux` **verte** (106 s : 449/449 au niveau 4, 11/11 paires, permutation 12/275, notation 5 112/5 112,
> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**
> sont les **structurelles connues** : `porte-indice` (861 s) et `porte-melange` (107 s), avec les mêmes
> diagnostics (indice extérieur à 482 jetons, écart nul ou négatif ; état de A qui ne rend pas le code de A).
> `porte-homeostasie` est **verte** (506 s). Les références sont stables : `porte-flux` **60,8135**,
> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →
> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,
> `porte-vision` **559 s**, `porte-poids-creux` **319 s**, `porte-prechargement` **187 s**. Journaux :
> `/tmp/portes-b9-1026-12h55`.
>

> **Historique des passes** : les passes antérieures au 26/10 14 h 30, dont celle du
> 25/10 04 h 51, sont conservées dans
> [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md).

## 1. Ce qui se vérifie en une commande

| quoi | commande | attendu |
|---|---|---|
| tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |
| toutes les portes | `tools/toutes-les-portes.sh` | **49 portes** ; dernière passe : **46 vertes, 3 rouges** (28/10 00 h 12), **1 h 40**, aucune sautée — les deux rouges sont **structurelles** et connues (`porte-indice`, `porte-melange`) · ⚠ **ne jamais lire une porte à travers un `tail`** : sa dernière ligne suit l'échec, et le code de sortie est celui du tuyau |
| une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |

> ### ⚠️ DEUX DÉFAUTS DE MESURE, TROUVÉS LE 16/10 — ET ILS SONT DE LA MÊME FAMILLE
>
> **1. `porte-tableaux` NE POUVAIT PAS ÉCHOUER.** Elle imprimait ses défauts (❌) puis sortait en **0** ✗ :
> le `sys.exit(...)` de son bloc Python n'arrêtait que **Python** ✗, et le script ne propageait pas le
> code ✓. Une porte qui ne peut pas échouer est **pire** qu'une porte absente ✗ — et celle-ci
> **documente** les tableaux depuis des semaines ✓. Corrigé : `[ $? -eq 0 ] || exit 1` juste après le
> bloc ✓ (vérifié : elle sort maintenant en **1** sur un tableau cassé ✓✓).
>
> **2. ET JE L'AI LUE À TRAVERS `tail` PENDANT HUIT ROUNDS** ✗✗. Ce fichier le dit pourtant noir sur
> blanc : « ne jamais lire une porte à travers un pipe — le code de sortie devient celui du pipe » ✓.
> Résultat : **huit commits** sont passés avec un tableau **cassé** dans `docs/archive/cerveau-facultes.md` ✗
> (un bloc de citation inséré **au milieu** d'un tableau ✓) sans que je m'en aperçoive ✓✗. Corrigé ✓.
>
> **3. Et une porte de plus dans la foulée** : `tools/verifier_liens.py` (**308 liens** relatifs
> vérifiés dans `docs/` et `reports/` ✓) est appelé par `porte-tableaux` ✓ — un document de ce dépôt
> **est** fait de renvois, et un renvoi mort ne casse rien le jour où on l'écrit : il casse six semaines
> plus tard ✓.
>
> *Trois défauts, trois leçons déjà écrites ici : une vérification doit pouvoir échouer ; on ne lit pas
> une porte à travers un pipe ; et un renvoi se vérifie à la machine, pas à l'œil.*

> **4. ET UN AUDIT DES 46 PORTES, LE MÊME JOUR** (analyse statique, sans les exécuter ✗) : la question
> posée par `porte-tableaux` — *combien d'autres portes ne PEUVENT PAS échouer ?* ✗ — a une réponse, et
> elle est précise ✓ :
>
> | famille cherchée | trouvée | verdict |
> |---|---|---|
> | heredoc Python avec `sys.exit` **non propagé** | **2** | ✅ **`porte-tableaux`** (corrigée) et **`porte-prechargement`** (corrigée : `rm -f` écrasait le code ✓✗ — elle imprimait « PORTE ROUGE » et sortait en **0** ✗) |
> | heredoc Python avec `sys.exit` **propagé par l'appelant** | 1 | ✅ `porte-bus-socket` — son helper est appelé en `REP=$(moduler …) \|\| { …; exit 1; }` ✓ : **faux positif** ✓ |
> | `\|\| true` | 3 | ✅ **légitimes** ✓ : ils portent sur des **extractions** dont le vide est un état valide ✓ (`grep -m1 …`, `mkdir -p`, un comptage ✓), et la vérification vient **après** ✓ |
> | pipe vers `tail` **dans** une porte | 9 | ✅ **faux positifs** ✓ : ce sont des **extractions de valeur** (`grep … \| tail -1` ✓), pas des affichages de fin — le code de sortie du pipe n'est pas ce que la porte teste ✓ |
>
> **Deux vrais défauts sur les 46 portes de l'époque (16/10)**, tous deux **corrigés et vérifiés** ✓✓ — et les autres signaux
> sont des **faux positifs documentés** ✗✓, ce qui vaut mieux qu'un audit muet ✓. *La leçon vaut pour
> l'audit lui-même : une détection statique propose, la lecture dispose* ✓.
>
> **5. ET L'AUDIT A ÉTÉ POUSSÉ PLUS LOIN, LE MÊME JOUR : chaque porte A-T-ELLE UN CHEMIN D'ÉCHEC ?**
> Une porte sans `exit 1` ne peut pas dire non ✗ — c'est la même famille, un cran plus haut ✓.
>
> | ce qui a été compté | résultat |
> |---|---|
> | portes **sans aucun `exit 1-9`** | **0 sur 46** ✓ (chemins d'échec : médiane **6**, min **2**, max **17** ✓✓) |
> | portes **sans `❌` dans leur propre source** | **1** : `porte-mistral.sh` — **et c'est un faux positif** ✓ : son `exit 1` est précédé de la **dernière ligne** de `compare_logits.py`, qui porte le `❌` ✓✓ (« PORTE DE CORRECTION NON TENUE » ✓) |
> | comment la passe **compte** | par **code de sortie** ✓ (`code=$?` → `✅` / `❌ code N` ✓✓), pas par marqueur ✗ — donc le récapitulatif est **fiable** ✓ |
>
> **Conclusion de l'audit** : la suite est **structurellement saine** ✓ — deux vrais défauts trouvés et
> corrigés ✓✓, et tous les autres signaux sont des **faux positifs documentés** ✓. *Et une leçon de
> plus sur ma façon de lire : je comptais les ❌ d'une porte **dans son source** ✗ alors que le marqueur
> peut venir de l'outil qu'elle appelle ✓ — c'est le **code de sortie** qui fait foi, et la passe le
> lisait déjà correctement ✓✓.*

## 2. Les repères imprimés par chaque porte

| porte | durée | ce qu'elle vérifie, chiffré (passe du 2026-10-11 06:30) |
|---|---|---|
| `porte-audit-drapeaux.sh` | 149 s | ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun |
| `porte-budget.sh` | 42 s | ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite |
| `porte-bus.sh` | 75 s | ✅ le canal diffusé par fichier change la région du milieu |
| `porte-bus-socket.sh` | 88 s | ✅ le bus du pilote agit (113.0068 -> 148.9144) |
| `porte-c4-retard.sh` | 60 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |
| `porte-coupe.sh` | 125 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit |
| `porte-delais.sh` | 20 s | ✅ le temps, lui, augmente : 6.43 s → 9.75 s (+3.3 s ≈ 50 ms × 64 pas) |
| `porte-episodique.sh` | 166 s | ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un |
| `porte-flux.sh` | 20 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
| `porte-fusion.sh` | 7 s | ✅ v1 refusée (code 2), trace seule refusée (code 2) |
| `porte-gain.sh` | 351 s | ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san |
| `porte-greffe.sh` | 829 s | ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE |
| `porte-harnais-invariants.sh` | 105 s | ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage |
| `porte-horloge.sh` | 27 s | ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue |
| `porte-indice.sh` | 770 s | ✅ la porte est franchie. Limite, et elle est écrite : UN SEUL indice extérieur, |
| `porte-jumeaux.sh` | 77 s | PORTE TENUE : l'échange est exact, il ne crée pas de gain entre jumeaux identiques, il |
| `porte-melange.sh` | 805 s | ✅ la porte est franchie. Ce qu'elle dit : deux entrées qui se somment ARBITRENT |
| `porte-memoire.sh` | 7 s | PORTE TENUE : la mémoire retient les K derniers signaux HORS du réseau, exactement, sans |
| `porte-mistral.sh` | 9 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p |
| `porte-occupation-elagage.sh` | 50 s | ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté |
| `porte-occupation-moteur.sh` | 44 s | ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à |
| `porte-pannes.sh` | 45 s | ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité |
| `porte-peripherie.sh` | 9 s | PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont |
| `porte-poids-creux.sh` | 354 s | ✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité — paires divisées sur |
| `porte-pont.sh` | 75 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |
| `porte-profondeur-routee.sh` | 558 s | ✅ porte profondeur routée : 16 couches contre 24 sur 8192 jetons de corpus.ids, |
| `porte-recurrence.sh` | 10 s | PORTE TENUE : la boucle existe, elle est déterministe, elle ne coûte aucune paire, son zéro |
| `porte-reflexe.sh` | 106 s | ✅ l'état de 16 couches CONTIENT le prochain jeton : 25.4 % contre 4.8 % pour la classe majorit |
| `porte-registre.sh` | 14 s | ✅ région absente : refusée en la nommant (code 2), rien n'est calculé |
| `porte-reparti-moteur.sh` | 0 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |
| `porte-sauvegarde-modele.sh` | 45 s | ✅ porte sauvegarde du modèle : la perte de validation est la MÊME aux quatre étapes |
| `porte-tokenizer-kimi.sh` | 5 s | ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres) |
| `porte-topologie.sh` | 36 s | PORTE TENUE : le relais ne change pas un chiffre (42.5477) |
| `porte-trace.sh` | 25 s | ✅ la trace fausse est détectée et nommée |

## 3. Les trois invariants qui ne sont pas des chiffres

1. **Le crate reste `std` seul, zéro dépendance** — toute dépendance ajoutée est un refus, pas
   une négociation ;
2. **le profil `release` est le binaire de MESURE** : toute promotion dans le chemin
   d'exécution se paie d'un passage des portes (`porte-flux.sh` au minimum, cinq modes, ~2 min) ;
3. **on ne laisse jamais l'arbre cassé** : une tentative qui échoue se **renverse** (et la
   tentative est écrite dans le journal), elle ne reste pas à moitié appliquée.

## 4. Où sont les autres chiffres

- **mesures par expérience** : `reports/` (une fiche par fichier ; les campagnes éclatées en
  dossiers avec index, `reports/campagne-benefices/`, `reports/toutes-langues/`) ;
- **état des capacités** : [`docs/pilotage/en-cours.md`](en-cours.md) (état courant) ; l'ancien état complet est archivé dans `docs/archive/etat-cerveau.md` ;
- **ce qui manque** : `docs/pilotage/manques.md` (avec la mesure qui l'établit) ;
- **journal des événements** : `journal/AAAA-MM-JJ.md` (index du jour) et ses fichiers de thème.
