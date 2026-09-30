# Session 7d0d2578 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `7d0d2578-0048-4998-8494-7d2daef56769` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 11:47 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 41 |
| Appels d'outils | 53 |
| Fichiers touchés | 1 |
| Commandes | 18 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/Code 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet — corrige : ton dépôt est /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, paquet `drave-core`, binaire `drave`). Toute la documentation est en FRANÇAIS : écris en français.  CONTEXTE : le moteur sait faire  … [3913 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/Code 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHu … [4193 caractères tronqués]

*53 appels d'outils.* Actions notables :

- bash — Lister le dépôt et les fichiers clés
- read
- bash — Repérer le protocole dans main.rs
- bash — Lister les fonctions clés de model.rs
- bash — Repérer les options CLI liées
- bash — Chercher la phase 3.4 et le doc Colab
- bash — Lire roadmap §3 et chiffres transport
- bash — Chercher tests unitaires et aide --lot
- bash — Vérifier l'état git et les usages de emb_imposee_lot
- bash — Voir le diff en cours sur model.rs
- bash — Relever les lignes clés actuelles
- bash — Relever l'état courant des modifications
- bash — Lire le diff en cours de main.rs
- bash — Vérifier l'usage des positions dans forward_lot
- … et 20 autres

**Synthèse produite :**

⏵ Terminé : spécification écrite et transmise au parent

**Livrable** : `docs/plan-prefill-reparti.md` (414 lignes, français) — seul fichier que j'ai créé/modifié. `main.rs`, `model.rs`, `journal/README.md` et `tools/trace_compacite.py` bougeaient en parallèle sous un autre agent ; je n'y ai pas touché.

Résumé — décisions d'architecture et points de choix :

1. **Mode 3 (`MODE_LOT`)** plutôt qu'un champ `t` : `n` (offset 18) porte le nombre d'états, l'en-tête reste à 39 octets, tous les offsets existants sont stables et les modes 0/1/2 restent identiques à l'octet près.
2. **`VERSION_FLUX` passe de 2 à 3** : un nœud v2 lirait `n×4` octets d'un corps qui en fait `n×hidden×4` avant de répondre « mode inconnu » — refus exact mais tardif et muet sur la cause ; le bump rend le refus immédiat et nommé.
3. **Dense f32 seulement** dans ce plan (seul transport sans perte, donc seul candidat à 0,00e0) ; le lot en listes est spécifié comme **mode 4** futur (corps du mode 2 répété, préfixe auto-délimité par état).
4. Corps = `t × hidden × f32` ; `position` = base du lot, positions contiguës par contrat, **dimension non transmise** (même GGUF exigé) ; réponse encodée comme la demande, écho vérifié (mode, pos, n, debut, fin).
5. Côté modèle : `emb_imposee_lot` aplati + wrapper `forward_lot_impose` ; rien d'autre ne change dans `forward_lot` (plage de couches et `flux_brut` déjà corrects).
6. Deux trous du code actuel explicitement corrigés par la spec : `envoyer_lot` écrit **40** octets pour un `TAILLE_TETE` de 39 (décalage silencieux de tout le corps), et `VERSION_FLUX` vaut encore 2.
7. Vérification : `--ppl-reparti --lot N`, les deux chemins découpant à frontières identiques (`ids[..N-1].chunks(lot)`) → « écart 0.00e0 », 5 lots et 3 589 octets/jeton à `t = 8` ; `--lot 1` non régressif (144,8289).
8. Piège central documenté : comparer un run `--lot 8` à un run `--lot 1` donne ~1e-4 pour un non-bug (ordre des accumulations) — le critère est l'égalité des deux chemins à lot égal.
9. Autres pièges : `KvCache::assurer` boucle indéfiniment si `besoin > ctx` ; `forward_lot(&[], pos)` laisse `emb_imposee_lot` fuir sur le lot suivant ; raccourci `t == 1` à contourner.
10. **Deux choix laissés à l'implémenteur** : (a) `--lot` par défaut et son plafond mémoire, (b) le moment d'introduire le mode 4 (lot en listes, ÷2,3 sur le fil pour 2,7e-2 d'écart) — plus, s'il le souhaite, garder la version 2 avec le seul mode 3, au prix d'un refus tardif et non nommé.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md` | 1 | 13 |

### Commandes exécutées (échantillon)

- **T1** Lister le dépôt et les fichiers clés
- **T1** Repérer le protocole dans main.rs
- **T1** Lister les fonctions clés de model.rs
- **T1** Repérer les options CLI liées
- **T1** Chercher la phase 3.4 et le doc Colab
- **T1** Lire roadmap §3 et chiffres transport
- **T1** Chercher tests unitaires et aide --lot
- **T1** Vérifier l'état git et les usages de emb_imposee_lot
- **T1** Voir le diff en cours sur model.rs
- **T1** Relever les lignes clés actuelles
- **T1** Relever l'état courant des modifications
- **T1** Lire le diff en cours de main.rs
- **T1** Vérifier l'usage des positions dans forward_lot
- **T1** Vérifier les lignes citées dans la spec
- **T1** Vérifier les dernières citations de lignes
- **T1** Trouver la ligne exacte de pos0+i
- **T1** Contrôler l'état courant de l'implémentation
- **T1** Relire l'entête et confirmer le périmètre

## 4. Mesures et résultats marquants

- **T1** `redonne **exactement** le calcul local — écart **0,00e0**, perplexité 144,8289 des`
- **T1** `37:   d'octets, pour une perte de 2,6 %. La valeur occupant 16 bits sur le fil, le`
- **T1** `40:   perdu la fidélité (4,9e-2) ; à 0,05 (24 %) l'écart est ×1,8 ; à 0,10 la`
- **T1** `68:où le transport est exact, l'écart passe de 0,00e0 à 5,61e0** (perplexité 119`
- **T1** `104:| 0,00 | 98,1 % | 2 793 | 7,1e-2 | 3 622 octets · 2,6e-2 |`
- **T1** `105:| 0,02 | 60,4 % | **1 778** | **2,2e-3** | 2 203 octets · 4,9e-2 |`
- **T1** `106:| 0,05 | 24,0 % | 799 | 1,1e0 | 897 octets · 8,1e-1 |`
- **T1** `137:toujours les listes à sparsité égale (1 745 contre 2 159 octets, et 14 % contre`
- **T1** `138:16 % d'écart) ; et l'écart dépend du **corpus** bien plus que du seuil — 0,2 % sur`
- **T1** `160:ci-dessous — **÷2,3 sur le fil pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256,`
- **T1** `161:13,7 % à 64) (et 13,7 % d'écart à 64 jetons : sur une séquence courte,`
- **T1** `181:3 623 à 1 568 octets, soit **÷2,3**, pour 2,7 % d'écart sur 256 jetons de vrai`
- **T1** `af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart`
- **T1** `+/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la`
- **T1** `62:                // les relisait `rep` fois — mesuré ×2,2 sur ce poste.`
- **T1** `| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'un lot est `t × hidden × 4` : `n` (offset 18) porte déjà le compte, l'en-tête reste **39 octets**, tous les off`

