# Références de non-régression

> **Dernière passe complète — 2026-11-03 à 11 h 30 :** **82 portes, 80 vertes, 2 rouges**,
> **1 h 48** (journaux durables `work/portes/passe-0303-11h30`), **machine au repos** (GPU libres ;
> seuls des claims CPU). Les **2 rouges sont les connues, structurelles** : `porte-indice` (821 s),
> `porte-melange` (102 s). `porte-homeostasie` **verte** (495 s, LoRA régénéré), `porte-reparti-moteur`
> **verte** (ré-étalonnée à 8,7434), `porte-sessions` **verte** (N2/S en pause), `porte-tableaux` et
> `porte-ressources` vertes.
>
> **Passe précédente — 2026-11-03 à 04 h 10 :** 82 portes, 77 vertes, 5 rouges, 1 h 40 — 4 connues +
> `porte-sessions` (coordination, rejouée verte à 08 h 10 après la pause de N2/S).
>
> **83e porte — 04/11 :** `porte-n3-inventaire` (1 s) ajoutée et **verte** dans la passe N3
> (17/17, 92 s, 0 rouge, `work/portes-n3-cloture/registre.txt`) ; elle entrera dans la prochaine
> passe complète (83 portes).

> **Passe précédente — 2026-11-02 à 19 h 32 :** **81 portes, 76 vertes, 5 rouges**, **1 h 52** (journaux durables `work/portes/passe-1102-19h32`). Rouges : 4 connues (`porte-indice` **1 027 s**, `porte-melange` 123 s, `porte-homeostasie` env., `porte-reparti-moteur` 51 s) + **`porte-tableaux`** (1 s) : lien `reports/rapport-n2-fenetre.md` → `n2-fenetre.json` cassé (fiche N2 en cours) — **rouge de passage**, **rejouée verte à 21 h 57** le 02/11 (2 747 liens, 1 577 fichiers), dès que le JSON a existé ; aucune régression structurelle. La 82e porte (`porte-ressources`) n'était pas dans cette passe : la suivante comptera **82**.

> **Passe précédente — 2026-11-02 à 06 h :** 81 portes, 76 vertes, 5 rouges (`/tmp/portes-…`,
> effacés au reboot) ; `porte-greffe` à 700 s, **rejouée verte à 1200 s** (délai, pas régression).

> **Passe précédente — 2026-11-01 à 00 h 56 :** **80 portes, 76 vertes, 4 rouges, 1 h 46**
> (journaux `/tmp/portes-1101-n2h`). Mêmes rouges que la passe du 31/10 : `porte-indice` (921 s),
> `porte-melange` (112 s), `porte-homeostasie` (environnementale) et `porte-reparti-moteur`.
> Aucune régression ; `porte-vision` et `porte-ocr-scans` sont vertes.

> **Passe précédente — 2026-10-31 à 19 h 42 :** **79 portes, 75 vertes, 4 rouges, 1 h 39**
> (journaux `/tmp/portes-1031-n2d`) : mêmes rouges ; `porte-ocr` (48 s) était verte.

> **Ce que ce fichier porte.** Les repères chiffrés qu'une passe complète imprime, et
> les invariants qui ne sont pas des chiffres. Les mesures de campagne (perplexités,
> budgets, latences) sont dans `reports/` — une fiche par expérience — et non ici :
> ce fichier ne porte que ce qu'une **porte** vérifie.

> **Historique des passes** : les passes antérieures au 26/10 14 h 30, dont celle du
> 25/10 04 h 51, sont conservées dans
> [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md).

## 1. Ce qui se vérifie en une commande

| quoi | commande | attendu |
|---|---|---|
| tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |
| toutes les portes | `tools/toutes-les-portes.sh` | **83 portes** (82 à la dernière passe complète ; la 83e, `porte-n3-inventaire`, testée verte le 04/11) ; dernière passe **80 vertes, 2 rouges** (03/11 11 h 30, machine au repos) : les 2 connues (`indice`, `melange`) · ⚠ **ne jamais lire une porte à travers un `tail`** |
| une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |

> **16/10 — l'audit des 46 portes** (deux vrais défauts corrigés, des faux positifs
> documentés) : le récit et les tableaux sont dans
> [`historique-passes-portes.md`](../../reports/historique-passes-portes.md).

## 2. Les repères imprimés par chaque porte

| porte | durée | ce qu'elle vérifie, chiffré (passe du 2026-11-03 11:30) |
|---|---:|---|
| `porte-adaptateur-sortie.sh` | 64 s | ✅ porte tenue (écriture fidèle · invariant · effet · refus) |
| `porte-audit-drapeaux.sh` | 167 s | ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun |
| `porte-b1110-hybride.sh` | 0 s | PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case |
| `porte-balayage.sh` | 0 s | ✅ porte balayage verte |
| `porte-bloc-code.sh` | 10 s | ✅ porte bloc code verte |
| `porte-bloc-linguistique.sh` | 12 s | ✅ porte bloc linguistique verte |
| `porte-bloc-maths.sh` | 1 s | ✅ porte bloc maths verte |
| `porte-bloc-tableaux.sh` | 1 s | ✅ porte bloc tableaux verte |
| `porte-budget.sh` | 45 s | ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite |
| `porte-bus.sh` | 78 s | ✅ le canal diffusé par fichier change la région du milieu |
| `porte-bus-socket.sh` | 97 s | ✅ le bus du pilote agit (113.0068 -> 148.9144) |
| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |
| `porte-cerveau.sh` | 8 s | ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe) |
| `porte-consolidation.sh` | 66 s | ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier) |
| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |
| `porte-cycle-c2.sh` | 122 s | ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe · |
| `porte-deepseek.sh` | 0 s | ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation. |
| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |
| `porte-diff-couche.sh` | 17 s | ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé |
| `porte-document.sh` | 6 s | ✅ porte document verte |
| `porte-echange-experts.sh` | 52 s | PORTE TENUE |
| `porte-episodique.sh` | 165 s | ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un |
| `porte-etat.sh` | 0 s | ✅ porte état verte : aucun fait commité après le dernier état |
| `porte-flux.sh` | 24 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
| `porte-fusion.sh` | 7 s | ✅ v1 refusée (code 2), trace seule refusée (code 2) |
| `porte-gain.sh` | 205 s | ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), sans fenê |
| `porte-greffe.sh` | 626 s | ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE |
| `porte-harnais-invariants.sh` | 109 s | ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage |
| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |
| `porte-horloge.sh` | 24 s | ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue |
| `porte-indice.sh` | 821 s | ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, question qui  |
| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |
| `porte-jumeaux.sh` | 28 s | PORTE TENUE : l'échange est exact, il ne crée pas de gain entre jumeaux identiques, il |
| `porte-lecteur.sh` | 0 s | ✅ porte lecteur verte |
| `porte-lecture.sh` | 2 s | ✅ porte lecture verte |
| `porte-m5-brouillon.sh` | 0 s | ✅ brouillon déclaré (cibles [37,38,39]) et porté : 75 tenseurs, 41 263 M poids |
| `porte-melange.sh` | 102 s | ❌ l'état de A ne rend pas le code de A dans une |
| `porte-memoire.sh` | 10 s | PORTE TENUE : la mémoire retient les K derniers signaux HORS du réseau, exactement, sans |
| `porte-miroir-blocs.sh` | 7 s | ✅ porte miroir verte |
| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |
| `porte-n3-cache.sh` | 6 s | PORTE TENUE : saut de calcul mesuré · sortie changée · condition K/V nommée |
| `porte-n3-composition.sh` | 6 s | PORTE TENUE : service + profondeur + routage + comptage composés sur les mêmes modèles |
| `porte-n3-deux-processus.sh` | 4 s | PORTE TENUE : deux processus · fichier de frontière · logits identiques au pas plein |
| `porte-n3-deux-regions.sh` | 4 s | PORTE TENUE : découpage 0..k / k..n bit-exact · pont des deux côtés · prompt différent |
| `porte-n3-generation.sh` | 8 s | PORTE TENUE : génération répartie · deux caches · sortie bit-identique |
| `porte-n3-inventaire.sh` | 1 s | PORTE TENUE : inventaire N3 exécutable (autotest 5/5) · 18 portes, 20 fiches, 20 JSON, 0 orpheline |
| `porte-n3-placement.sh` | 4 s | PORTE TENUE : placement natif = métadonnée · A déterministe · contrôle pont nul détecté |
| `porte-n3-pont.sh` | 5 s | PORTE TENUE : pont natif branché · A déterministe · pont nul change la sortie |
| `porte-n3-positions.sh` | 4 s | PORTE TENUE : position vérifiée pas à pas · désync refusée · succès bit-exact |
| `porte-n3-profondeur.sh` | 6 s | PORTE TENUE : profondeur de service branchée · /sante stable · chaque profondeur déterministe · sort |
| `porte-n3-refus.sh` | 5 s | PORTE TENUE : empreinte refusée (code 4) · même modèle bit-exact |
| `porte-n3-reseau.sh` | 4 s | PORTE TENUE : TCP localhost · aucun cache sur le fil · logits identiques au pas plein |
| `porte-n3-routes.sh` | 4 s | PORTE TENUE : routage vivant · même modèle déterministe · config différente change la sortie |
| `porte-n3-service.sh` | 5 s | PORTE TENUE : service natif vivant · /sante exact · génération déterministe · 404 |
| `porte-n3-service-briques.sh` | 7 s | PORTE TENUE : pont actif dans le service · placement métadonnée · décision à seuil 12/0 vs 0/12 · re |
| `porte-n3-seuil.sh` | 5 s | PORTE TENUE : décision à seuil comptée · 0/1 aux extrêmes · mixte à 0,01 · déterministe |
| `porte-n3-sparsite.sh` | 4 s | PORTE TENUE : kwta et top_k agissent séparément · A déterministe |
| `porte-n3-sparsite-compte.sh` | 4 s | PORTE TENUE : compteurs réels · top_k agit sur les experts · kwta agit sur les canaux · A déterminis |
| `porte-occupation-elagage.sh` | 60 s | ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté |
| `porte-occupation-moteur.sh` | 53 s | ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à |
| `porte-ocr.sh` | 46 s | ✅ porte OCR verte : 10 pages lues, WER sous le seuil, parité tenue et contrôles en échec |
| `porte-ocr-scans.sh` | 425 s | ✅ porte OCR-scans verte : familles, colonnes et tableaux tiennent leurs planchers |
| `porte-pannes.sh` | 46 s | ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité |
| `porte-peripherie.sh` | 15 s | PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont |
| `porte-poids-creux.sh` | 315 s | ✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité — paires divisées sur |
| `porte-pont.sh` | 79 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |
| `porte-prechargement.sh` | 181 s | PORTE TENUE |
| `porte-profondeur-routee.sh` | 511 s | ✅ porte profondeur routée : 16 couches contre 24 sur 8192 jetons de corpus.ids, |
| `porte-push-paresseux.sh` | 26 s | PORTE TENUE |
| `porte-r13-bpe.sh` | 52 s | PORTE TENUE : BPE natif réversible · budgets d'octets égaux · bits/octet meilleurs |
| `porte-recurrence.sh` | 14 s | PORTE TENUE : la boucle existe, elle est déterministe, elle ne coûte aucune paire, son zéro |
| `porte-reflexe.sh` | 141 s | ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée |
| `porte-registre.sh` | 15 s | ✅ région absente : refusée en la nommant (code 2), rien n'est calculé |
| `porte-reparti-moteur.sh` | 3 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |
| `porte-ressources.sh` | 0 s | ✅ porte ressources verte : autotest 9 cas, registre cohérent, GPU réservés à Drave |
| `porte-sauvegarde-modele.sh` | 52 s | ✅ porte sauvegarde du modèle : la perte de validation est la MÊME aux quatre étapes |
| `porte-sessions.sh` | 0 s | PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict |
| `porte-speculatif.sh` | 67 s | ✅ porte tenue (invariant exact · taux rendu · témoin à zéro · brouillon invalide refusé) |
| `porte-tableaux.sh` | 0 s | ✅ la page vivante date du dernier commit (2026-11-03) |
| `porte-tokenizer-kimi.sh` | 6 s | ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres) |
| `porte-topologie.sh` | 92 s | ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.5477 · re |
| `porte-trace.sh` | 26 s | ✅ la trace fausse est détectée et nommée |
| `porte-vision.sh` | 553 s | ✅ porte tenue (refus dit · embedding NON comparé · formes · couches isolées NON vérifiées · projecte |

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
