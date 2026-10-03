# Session e14c26ae — Tu es relecteur ADVERSARIAL, en

| | |
|---|---|
| Identifiant | `e14c26ae-6d52-41f9-a72f-6ebdcef172d5` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 21:15 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 49 |
| Appels d'outils | 76 |
| Fichiers touchés | 1 |
| Commandes | 54 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL, en lecture seule. Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », `drave-core`, std seul). Tu ne modifies AUCUN fichier du dépôt : tu lis, tu mesures, tu rapportes. Tu peux écrire dans /tmp.  Contexte : le dernier commit `ac80e7e` (« Découpage V4.1 : la couture est exacte au bit près, l'instrument est innocenté ») prétend cor … [5056 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL, en lecture seule. Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inféren … [5336 caractères tronqués]

*76 appels d'outils.* Actions notables :

- bash — Show recent commits and stats
- bash — List repo root and tools
- bash — Show commit diff for core files
- bash — Check tmp dump directories
- todo_write
- bash — Rest of main.rs diff
- bash — Read porte-flux.sh
- bash — Grep key symbols in model.rs
- bash — Grep key symbols in main.rs
- read
- bash — Locate callers and decode/encode functions
- bash — Find all callers outside model.rs
- bash — Read vider_couche
- bash — Summarize tensor name prefixes per dump
- … et 45 autres

**Synthèse produite :**

⏵ Rapport rendu ; aucun processus résiduel

Rapport envoyé au parent (aussi écrit dans `/tmp/adv_rapport_ac80e7e.md`). Aucun fichier du dépôt n'a été modifié ; aucun run lourd lancé.

\## Ce que j'ai trouvé

**FAUX — 3**

1. **« 2 544 tenseurs du pilote (couches 0-19, pos 0-3) : 0 »** — mesure des mtimes : seuls **954** des 2 544 fichiers de `/tmp/dpil4` viennent de la passe répartie ; **1 590** viennent de la passe de référence du pilote, qui écrit dans le même `DRAVE_DUMP_COUCHES` (1 260 couches 20-39, 327 pos 3 = le dernier jeton sauté, 3 `hidden_final`). L'étiquette est impossible avec n=2544 (ce sous-ensemble = 1 284). Le verdict survit sur les 954 + 945, mais 62 % du chiffre publié ne peut pas échouer.
2. **« mode faux et muet », « décalé de quatre octets »** — j'ai rejoué la trame d'avant correctif (mode 3 sans octet `np`) contre un vrai serveur : il **bloque** dans `read_exact` et ne se plaint qu'à la fermeture du client. Aucun `set_read_timeout` en production ⇒ vrai pilote = **interblocage**, pas un chiffre faux ; décalage = 1+4·np octets.
3. **« 81 999 au retour »** — le compte des octets reçus n'inclut jamais l'octet `np` (ni le pré-mix) alors que l'émission le compte : le vrai retour = **82 000**. Mesuré sur Qwen 0.5B (np=0 des deux côtés) : **3664 / 3663** pour 896 canaux.

**TROU — 7** : `portes.sh:184-189` ignore le code retour et ne cherche que « ❌ » (démontré : modèle absent → code 1 → `ECHEC=0`, « toutes les portes sont vertes ») ; aucun délai sur le pilote dans la porte (un interblocage ⇒ vert après `timeout 900`) ; **`np = 1` n'est exercé par aucun test** ; `norme_finale` ne `take()` que dans une branche ; le chemin `--lot` n'affecte jamais `hc_porte_imposee` ; `reprend` ignore le cas `flux_brut` + `debut=0` ; chemins `/tmp` partagés sans PID.

**FAIBLE — 4** : plafond du mode 4 à 11× le mesuré (et égal à celui du mode 2) ; « réduction finale comprise » alors que la sortie de `norme_finale` n'est jamais dumpée ; recette du digeste qui omet `--abits 8` (dref vient de `/tmp/exp_ref.sh`, un `--ppl-reparti` vers un port mort) ; `etat_impose` vidé même quand rien n'est imposé.

**SOLIDE** : le diagnostic et le correctif de la fuite (629 → 0, 7,05e-1 → 0,00e0) ; `norme_finale` consomme dans le seul chemin atteignable ; l'encodage v6 cohérent pour les 5 modes, porte exécutée en **17,3 s, code 0**, avec exactement les chiffres publiés ; 62 tests verts ; le `trap` tue bien le serveur sous `timeout` (mon soupçon initial était faux) ; un `nan` ne p
… [144 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/adv_rapport_ac80e7e.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show recent commits and stats
- **T1** List repo root and tools
- **T1** Show commit diff for core files
- **T1** Check tmp dump directories
- **T1** Rest of main.rs diff
- **T1** Read porte-flux.sh
- **T1** Grep key symbols in model.rs
- **T1** Grep key symbols in main.rs
- **T1** Locate callers and decode/encode functions
- **T1** Find all callers outside model.rs
- **T1** Read vider_couche
- **T1** Summarize tensor name prefixes per dump
- **T1** Numpy comparison of all published pairs
- **T1** Check mtimes to detect stale tensors
- **T1** Analyze write-time windows per layer/position
- **T1** Read digest head and tail
- **T1** Per-file write times by layer and position
- **T1** Count subsets and inspect digest sections
- **T1** Classify split vs reference writes and test transport
- **T1** Check first divergent tensor between 16 and 8 bit
- **T1** Check f32 matvec and read sprint doc
- **T1** Run porte-flux.sh
- **T1** All hc_porte occurrences
- **T1** Read format-flux doc
- **T1** Read first raccord and Hc::melanger
- **T1** Read hc_porte update site
- **T1** Find other emitters/consumers
- **T1** Check version constants and doc mentions
- **T1** Read porte output and check leftovers
- **T1** Read pair_factice v6 handling
- **T1** Callers of tete_flux and binary date
- **T1** Test EXIT trap under timeout SIGTERM
- **T1** All octets_corps occurrences
- **T1** Run 2-node mode 0 and read transport bytes
- **T1** Run unit tests
- **T1** Check portes.sh wiring
- **T1** Read hc_retarde detection
- **T1** List early exits without failure marker
- **T1** Demonstrate silent failure through portes.sh wiring
- **T1** Read rest of sprint 13
- … et 14 autres

## 4. Mesures et résultats marquants

- **T1** `-> applique YaRN ×16 à toutes les positions des couches de ratio > 0 (mscale`
- **T1** `+> applique bien YaRN ×16 à toutes les positions dès que `compress_ratio > 0``
- **T1** `4336-    /// V4-Flash — position 0 juste à 1e-3, position 1 fausse à 30 %.`
- **T1** `fichiers par passe, ~50 Mo) : ils ne sont pas versionnables. Ce digeste l'est, et`
- **T1** `trace creuse (39,9 % d'activité) : 6,04 et 3,04 — deux centièmes de plus, parce que`
- **T1** `99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T1** `| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour`
- **T1** `f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `référence locale  : perplexité 61.9920  (0.9 s)`
- **T1** `deux nœuds        : perplexité 61.9920  (0.9 s)`
- **T1** `transport         : dense f32 · 3664 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 23 flux`
- **T1** `2040-/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,`
- **T1** `référence locale  : perplexité 1743713.6243  (65.7 s)`
- **T1** `deux nœuds        : perplexité 514722.0611  (48.8 s)`
- **T1** `transport         : dense f32 · 82016 octets par flux (aller) · 81999 au retour · 400.0 % d'activité (20480 neurones par flux) · 3 flux`
- **T1** `référence locale  : perplexité 1743713.6243  (68.0 s)`
- **T1** `deux nœuds        : perplexité 1743713.6243  (51.3 s)`
- **T1** `référence locale  : perplexité 1743713.6243  (66.9 s)`
- **T1** `3 tokens notés — perplexité cumulée 208411.867  (0.0 tok/s)`
- **T1** `=== perplexité 208411.8674 sur 3 tokens (0 événements, 67.6 s) ===`
- **T1** `3 tokens notés — perplexité cumulée 1743713.624  (0.1 tok/s)`
- **T1** `=== perplexité 1743713.6243 sur 3 tokens (0 événements, 35.7 s) ===`
- **T1** `3 tokens notés — perplexité cumulée 208411.867  (0.1 tok/s)`
- **T1** `=== perplexité 208411.8674 sur 3 tokens (0 événements, 36.6 s) ===`
- **T1** `16:| deux nœuds, dense | **8 311,3347** — écart **0,00e0** | 65 615 | 400 % (16 384 canaux) | 4 873 ms (1,11×) |`
- **T1** `[config] attention V4 : 40 couches · 1 tête latente de 512 (448 nope + 64 rope) · 64 têtes de requête · sortie groupée 8×1024 · puits par tête`
- **T1** `[config] engram : tables sur les couches [1, 14] (rangées [384006168, 384016682]) · 24 colonnes de hachage (3 reculs × 8 têtes) · injection BRANCHÉE · 6336 octets lus par jeton et par table (24 rangée`
- **T1** `[config] rotation : RoPE simple sur les couches BRUTES (régime retardé : YaRN au-delà de quatre fois la longueur d'origine, seuil mesuré sur gpt-oss) — mais les couches COMPRESSÉES sont en YaRN ×16 à `
- **T1** `+        // obtenu n'est plus V4.1 (l'engram est 55 % du fichier), et le moteur le`
- **T1** `// (24 × 264 octets) sont lues dans la table de 101 Go : c'est le`
- **T1** `reports/rapport-decoupage-v41.md:24:| comparaison (2 544 tenseurs, 40 couches × 4 positions) | tenseurs différents |`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : [flux] quantification : 127 niveaux, seuil 0, top-k 0, renorm false   référence locale  : perplexité 61.9920  (0.9 s)   deux nœuds        : perplexité 61.9920  (0.9 s)   écart             : 0.00e0   t
- **T1** : commit ac80e7e0682685809b9506004a294debe1aed377 Author: Stéphane <stephane@localhost> Date:   Fri Oct 2 21:15:19 2026 -0400      Découpage V4.1 : la couture est exacte au bit près, l'instrument est in
- **T1** : 30-PORT=${PORT:-$((48000 + RANDOM % 1000))} 31- 32:[ -x "$D" ] || { echo "  $D absent : construire d'abord (cargo build --release)"; exit 1; } 33:[ -s "$MODELE" ] || { echo "  $MODELE absent"; exit 1;
- **T1** : --- simulation du câblage portes.sh (lignes 184-189) avec MODELE absent ---   /tmp/nexistepas.gguf absent code retour porte = 1 ECHEC vu par portes.sh = 0  (0 = vert !)
- **T1** : 4:processus et rend **exactement** la même perplexité (écart `0,00e0` en mode 16:| deux nœuds, dense | **8 311,3347** — écart **0,00e0** | 65 615 | 400 % (16 384 canaux) | 4 873 ms (1,11×) | 19:Le tra
- **T1** : [options] 1 drapeau(x) INCONNU(S), donc sans effet : --ctx-impose [options] (une faute de frappe suffit — `--options-actives` montre ce que le moteur applique vraiment) [rope] YaRN déclaré par le JSON

