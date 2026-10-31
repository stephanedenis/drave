# Session 4f3e8570 — Configuration RAID0 NVMe pour modèles IA

> **Journaux :** [le jour](../../2026-10-12/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `4f3e8570-3d81-41e0-a055-1002702a6959` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-12 15:30 |
| Durée | 25.5 h |
| Tours | 13 |
| Messages | 865 |
| Appels d'outils | 822 |
| Fichiers touchés | 41 |
| Commandes | 616 |
| Sous-agents | 0 |
| Commits | 57 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 08:00 HAE, en rounds autonomes : terminer S4 (porte tools/porte-prechargement.sh + préchargement ordonné dans le moteur), mesurer, garder les portes vertes (cargo test, porte-flux, passe complète des 34 portes), écrire les fiches et
… [186 caractères tronqués]
- **complete** — Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 08:00 HAE, en rounds autonomes : terminer S4 (porte tools/porte-prechargement.sh + préchargement ordonné dans le moteur), mesurer, garder les portes vertes (cargo test, porte-flux, passe complète des 34 portes), écrire les fiches et
… [186 caractères tronqués]
- **create** — Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 12:00 HAE, en rounds autonomes : avancer les actions du plan docs/etat-cerveau.md § 6 (C8 à l'échelle, C9 échange d'experts sur modèle routé, fenêtre × puits, capacité N4/chemin court), en mesurant chaque pas, en gardant cargo test 
… [140 caractères tronqués]
- **complete** — Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 12:00 HAE, en rounds autonomes : avancer les actions du plan docs/etat-cerveau.md § 6 (C8 à l'échelle, C9 échange d'experts sur modèle routé, fenêtre × puits, capacité N4/chemin court), en mesurant chaque pas, en gardant cargo test 
… [140 caractères tronqués]
- **create** — Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 18:00 HAE, en rounds autonomes : avancer les actions du plan docs/etat-cerveau.md § 6 — C9 (échange/latéralité sur un modèle routé), N4 (chemin court : lire la note docs/note-chemin-court-n4.md et exécuter le dessin A ou l'expérienc
… [276 caractères tronqués]
- **complete** — Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 18:00 HAE, en rounds autonomes : avancer les actions du plan docs/etat-cerveau.md § 6 — C9 (échange/latéralité sur un modèle routé), N4 (chemin court : lire la note docs/note-chemin-court-n4.md et exécuter le dessin A ou l'expérienc
… [276 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — tu as maintenant un raid0 nvme pour tes modèles et tes besoins données stockage rapide. fais-en bon usage

**Tour 2** — les deux. ensuite révise le plan de travail du cerveau

**Tour 3** — il ne devrait plus rester de serveur llama.cpp actif

**Tour 4** — le serveur de dosumentation est-il actif

**Tour 5** — lance le

**Tour 6** — reprends les travaux là où on était rendu

**Tour 7** — travaille sur le cerveau jusqu'à demain 13 oct 8h00 hae

**Tour 8** — <goal_round> Objective: "Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 08:00 HAE, en rounds autonomes : terminer S4 (porte tools/porte-prechargement.sh + préchargement ordonné dans le moteur), mesurer, garder les portes vertes (cargo test, porte-flux, passe complète des 34 portes), écrire les fiches et le journal, et committer chaque round ; puis enchaîner sur les actions sui … [654 caractères tronqués]

**Tour 9** — <goal_round> Objective: "Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 08:00 HAE, en rounds autonomes : terminer S4 (porte tools/porte-prechargement.sh + préchargement ordonné dans le moteur), mesurer, garder les portes vertes (cargo test, porte-flux, passe complète des 34 portes), écrire les fiches et le journal, et committer chaque round ; puis enchaîner sur les actions sui … [654 caractères tronqués]

**Tour 10** — le rendu du premier tableau de etat-cerveau.md ne fonctionne pas . on voit le code au lieu du tableau dans http://127.0.0.1:8771/

**Tour 11** — maintenat c'est à partir de "Ce que « C8 » recouvre, et où on en est." que ça dérape

**Tour 12** — travaille sur le cerveau jusqu'à midi

**Tour 13** — travaille sur le cerveau jusqu'à 18h00

## 2. Déroulé, étape par étape

### Tour 1 — tu as maintenant un raid0 nvme pour tes modèles et tes besoins données stockage rapide. fais-en bon usage

*103 appels d'outils.* Actions notables :

- bash — Inspect block devices, mounts and RAID status
- bash — Show working dir, DSH env vars and home contents
- bash — List RAID0 mount contents and sizes
- bash — Inspect FastNVMe dir and fstab entries
- bash — Read phase-1 migration script and logs
- bash — List RAID0 content directories in detail
- bash — Check RAID detail and NVMe SMART health
- bash — Inspect shell env, AI cache variables and cache sizes
- bash — Measure Ollama models, artefacts and large files on root
- bash — Read RAID array state from sysfs
- bash — Read migration READMEs and look for plan notes
- bash — Inspect current project repo state
- bash — Check tmp mounts, I/O tools and fstrim status
- bash — Measure repo size, cargo target and tmp usage
- … et 73 autres

**Synthèse produite :**

⏵ Rédaction du bilan

C'est fait, et mesuré avant d'être fait. Le raid0 est maintenant l'étage rapide de la machine, avec une politique écrite et des chiffres qui la fondent.

**Ce que le banc a établi** (`~/IA/outils/banc-io.py`, O_DIRECT, 0 erreur) :

| | séq. 8 flux | aléa 4 Kio QD1 | écriture |
|---|---|---|---|
| **raid0** | **7,45 Go/s** | 92 µs | **2,86 Go/s** |
| NVMe seul (btrfs) | 3,47 Go/s | 108 µs | 1,13 Go/s |
| HDD 11 To | 0,29 Go/s | 8 646 µs | 0,35 Go/s |

Verdict : le raid gagne **en débit et en écriture** (2,15× et 2,5× le NVMe seul), pas en latence QD1 — quatre disques sans DRAM derrière `md` ne réduisent pas une lecture isolée. C'est exactement le profil des campagnes : lire 341 Go, écrire 81 Go d'artefacts. Sur une entrée d'engram de 264 octets : **92 µs** contre 27 713 µs sur le mécanique.

**Ce qui a été basculé sur le raid** (tout vérifié, rien supprimé avant vérification) : store Ollama 59 Go, gguf qwen3-30b 18,5 Go (SHA-256 identique), cache HuggingFace 6 Go, ccache 528 Mo. **Les chemins configurés n'ont pas changé** — ce sont des liens : si le raid n'est pas monté, l'outil échoue franchement au lieu d'écrire en silence sur le mauvais disque. Ollama a été testé en vrai : les 7 modèles se listent depuis le raid, et le store lui appartient désormais (le `pull` fonctionne, ce qui n'était pas le cas avant).

**Ce que je n'ai pas migré, mesure à l'appui** : la compilation de `drave-core` (48,03 s sur HDD contre 48,79 s sur raid — 47 s de CPU pour 0,7 s de `sys` : c'est le CPU qui limite, pas le disque) et le cache `uv` (il *lie* ses fichiers aux venvs : séparer les deux ferait copier au lieu de lier).

**Le filet de sécurité** : les 116 Go d'artefacts uniques (les clusters réécrits, payés en heures de calcul) sont copiés sur le mécanique — 45 fichiers vérifiés **octet pour octet** contre un manifeste SHA-256, plus une copie du manifeste dans la sauvegarde.

**Deux choses trouvées en chemin** : des `EIO` fantômes en lecture directe concurrente sur le btrfs — ce n'est **pas** le disque (`md0` à 0 erreur, lectures normales toutes bonnes, 0 erreur avec un descripteur par fil) ; et j'ai laissé une porte verte derrière moi (`tools/porte-flux.sh`, 5/5 modes, écarts conformes aux références).

**Il te reste deux commandes** pour récupérer les originaux mis en sursis :

```bash
sudo rm -rf /home/stephane/Data13TB/stephane/ollama-models.sursis-2026-10-12-155736   # 59 Go, root requis
rm -rf /home/stephane/FastNVMe/qwen3-30b-a3b-Q4_K_M.gguf.sursi
… [747 caractères tronqués]

### Tour 2 — les deux. ensuite révise le plan de travail du cerveau

*64 appels d'outils.* Actions notables :

- bash — Read conventions and search for kld references
- read
- bash — Inspect reports/journal conventions and kld headers
- bash — Verify gates count, engine commits and carte status
- bash — Read carte protocol and existing NVMe RAID doc
- bash — Outline the NVMe RAID prep doc
- bash — Check NUMA topology, read-ahead, GPU link widths
- write `/home/stephane/IA/outils/banc-numa-raid.py`
- bash — Measure NUMA/QPI cost of reading the RAID
- bash — Check GPU tooling and engine hardware view
- bash — Find disk enumeration in engine source
- bash — Read disk list context in materiel.rs
- bash — Identify kld format and locate HDD archive dirs
- bash — Check archives dir and any kld usage traces
- … et 37 autres

**Synthèse produite :**

⏵ Bilan des trois tâches

Tout est fait, vérifié, et versionné. Le dépôt est propre (`be29ebc4`, `6a39a8bf`).

**1. La fiche est déposée** — `reports/rapport-raid0-nvme.md`. Elle ne se contente pas de raconter le rangement : elle **répond au protocole § 7** du doc de configuration du 08/10, qui disait « aucune de ces optimisations n'est mesurée sur cette configuration : elle n'existe pas encore ».

| ce que le doc attendait | mesuré le 12/10 |
|---|---|
| les 4 NVMe sur le **nœud 1** | ✅ `numa_node = 1` sur les quatre |
| GPU en **x16** — « si c'est x8, le pari est perdu » | ✅ 16x (le doc prévoyait 2,5 GT/s au repos) |
| array à **6-7 Go/s** | ✅ **7,45 Go/s** (8 lecteurs) ; **2,86 Go/s** en écriture |
| « le QPI portera 6-8 Go/s : à mesurer » | ✅ **7,41 / 7,42 / 7,47 Go/s** selon le placement — **aucun coût** |
| « les contrôleurs DRAM-less peuvent être en dessous » | ✅ confirmé en aléa QD1 : l'array n'y bat pas un NVMe seul (1,1×) |

Et elle trouve un écart que personne n'avait vu : **`drave --materiel` ne voit pas l'array**. La liste des disques est en dur (`materiel.rs:244`), et `md0` n'a pas de `device/numa_node` — même ajouté, il rendrait « nœud ? » comme le HDD. C'est le § 7.2 qui l'exigeait.

**2. `kld` est archivé** — 4 vidages `.kld` de logits (24/09, magie `_logits_`) + WikiText-2 : **zéro référence** dans le dépôt, **zéro** dans `~/.bash_history`. Copiés sur le mécanique (`archives/kld-logits-2026-09-24/`), **sommes de contrôle vérifiées**, avec un README d'identification dedans (format, modèles, pourquoi archivé et non supprimé : le harnais qui les a écrits n'existe plus). Le chemin `~/FastNVMe/kld` reste valide par lien. **6,4 Go rendus** au volume rapide.

**3. Le plan du cerveau est révisé** (`docs/etat-cerveau.md` § 6, et lui seul) — trois constats, chacun vérifié :

- **une action était périmée** : le plan disait que `carte-sortie-profondeur.sh` « reste à lancer ». Elle a tourné le 11/10 à 00 h 15 — et elle tranche : le gain atteignable est **0,39 %** des paires (facteur **32** avec la borne), donc ce n'est pas le point de sortie qui limite, c'est **N4** ;
- **une action manquait** : le moteur ne voit pas l'array (ci-dessus) — devenue le **point 2** du plan, avec sa première commande ;
- **une exception tombe** : `porte-topologie.sh` était la seule porte incapable de tourner après un redémarrage (`/tmp/m5_d384_dense.gguf`, perdu). Elle tourne maintenant, prérequis **persistants sur l'array** : porte **tenue** (référence 17,4702 ; 30,4363 p
… [1145 caractères tronqués]

### Tour 3 — il ne devrait plus rester de serveur llama.cpp actif

*6 appels d'outils.* Actions notables :

- bash — Look for leftover llama.cpp and drave servers
- bash — Comprehensive sweep for leftover servers
- bash — Check mmap'd models, orphans, LM Studio, tmp leftovers
- bash — Inspect the temp dir before removing
- bash — Remove leftover temp dir and final check
- bash — Definitive check with non-self-matching pattern

**Synthèse produite :**

⏵ Vérifié : plus aucun serveur actif

Confirmé — **rien ne tourne**. Sept contrôles, tous négatifs :

| contrôle | résultat |
|---|---|
| processus `llama` / `llama-server` / `drave` / `ollama` / `llmster` | **aucun** |
| écouteurs réseau (8080, 8081, 1234, 11434, 48xxx-50xxx des portes) | **aucun** — il ne reste que les trois nœuds du harnais DSH (3080, 23535, 13141) |
| serveur LM Studio (llama.cpp embarqué) | `lms server status` → *« The server is not running »*, 0 écouteur sur 1234 |
| applications de calcul sur les GPU (`nvidia-smi`) | **aucune** — VRAM libre |
| familles de pages ouvertes sur un `.gguf` (signature d'un serveur vivant) | **0 processus** |
| conteneurs / unités systemd llama-ollama-lmstudio / zombies / orphelins à binaire supprimé | **aucun** |

Une seule trace subsistait, et elle était de moi : `/tmp/tmp.vRUJUkrIzQ`, le dossier de travail de `porte-topologie.sh` laissé par une exécution que j'avais interrompue (il ne contenait qu'un `topo.json` régénérable). **Retiré.** `/tmp` est à 380 Ko.

Deux précisions utiles :

- **Les portes du dépôt ne lancent pas de serveur llama.cpp** — elles lancent des nœuds **drave** (`--flux-serveur`, ports 48000-50999 et 50000+), et elles les tuent en fin de section. Les seuls restes possibles viennent d'une porte tuée en cours de route ; c'est exactement ce que j'ai nettoyé. Côté llama.cpp, le dépôt n'utilise qu'un binaire **one-shot** (`tools/ref_logits`, qui rend la main), pas un serveur.
- **Piège de mesure, celui-là même que `REPRISE.md` documente** : mon premier compte annonçait « 2 processus restants ». C'était mon propre motif qui se comptait — `[o]llama` contient la chaîne `llama`, donc le `grep` et son shell se matchaient eux-mêmes. Refait avec un motif reconstruit (`"lla""ma"`), le compte est **0**. Même famille de piège que `pkill -f` qui se tue lui-même.

Si tu veux un garde-fou avant/après une campagne, la ligne qui tranche est :

```bash
ss -ltn | grep -E ':(1234|8080|8081|11434|48[0-9]{3}|50[0-9]{3}) ' || echo "aucun serveur"
```

Je peux l'ajouter à `~/IA/outils/` (à côté de `etat-raid.sh`) si tu veux qu'elle soit à portée de main.

### Tour 4 — le serveur de dosumentation est-il actif

*3 appels d'outils.* Actions notables :

- bash — Look for a documentation server
- bash — Inspect mdserve and mdopen usage
- bash — Check mdserve status and identify active listeners

**Synthèse produite :**

⏵ Non — inventaire des écouteurs de la machine à l'appui

**Non, il n'est pas actif.**

Le serveur de documentation, c'est **`mdserve`** (lecteur Markdown local en lecture seule, `~/.local/bin/mdserve`, lancé d'ordinaire par `mdopen fichier.md`, qui écoute sur **127.0.0.1:8770** — le défaut de `mdopen`).

| contrôle | résultat |
|---|---|
| processus `mdserve` | **aucun** |
| écouteur sur 8770 (ou 877x / 8000 / 3000 / 4000 / 5000 / 9000) | **aucun** |
| dernier usage | cache HTML écrit le **11/10 08:13**, `pins.json` le **10/10 21:38** — rien depuis |

Et la liste **complète** de ce qui écoute sur cette machine, pour situer :

```
127.0.0.1:23535   node (nœud du harnais DSH)
127.0.0.1:13141   node (nœud du harnais DSH)
0.0.0.0:3080      node  →  /home/stephane/.local/bin/dsh web --no-open   (l'interface web de cette session)
127.0.0.1:631     CUPS         192.168.122.1:53  DNS libvirt
0.0.0.0:25        SMTP         0.0.0.0:22        SSH
```

Le seul « serveur web » de la liste est donc **le harnais DSH lui-même** (port 3080, `dsh web`) — ce n'est pas un serveur de documentation.

Pour le relancer quand tu veux, la porte d'entrée documentée est `mdopen` :

```bash
mdopen docs/etat-cerveau.md                    # démarre mdserve si besoin, ouvre un onglet
mdopen docs/etat.md --port 8771 -r ~/GitHub/Qtrinet   # 2e serveur, autre racine (sans mélanger)
```

Il refuse de mélanger deux racines sur le même port — d'où `--port` si tu veux servir le dépôt en plus de ta racine habituelle (`~/Data13TB/stephane`). Veux-tu que je le lance sur le dépôt (`-r ~/GitHub/Qtrinet`) ?

### Tour 5 — lance le

*6 appels d'outils.* Actions notables :

- read
- bash — Launch mdserve on the repo and open docs
- bash — Launch mdserve with canonical root and verify
- bash — Verify server survival and browser tabs
- bash — Move mdserve into a user systemd unit
- bash — Final verification of the doc server unit

**Synthèse produite :**

⏵ Lancé

**Le serveur de documentation tourne** — `mdserve` sert le dépôt Qtrinet en lecture seule :

```
http://127.0.0.1:8771/                    (l'arbre du dépôt — HTTP 200)
http://127.0.0.1:8771/?f=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/etat-cerveau.md
http://127.0.0.1:8771/?f=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-raid0-nvme.md
```

Les deux onglets ont bien été ouverts (Chrome a écrit son fichier de session à 18:35:52, dix secondes après le lancement). Il écoute **uniquement sur 127.0.0.1**, comme ses propres garanties l'annoncent.

Je l'ai posé sous une **unité utilisateur transitoire**, pas dans le cgroup de ma commande :

```
mdserve-qtrinet.service   active (running)   PID 319875
cgroup : user@1000.service/app.slice/mdserve-qtrinet.service
```

C'est voulu : lancé par `mdopen` seul, il héritait du scope `dsh-subprocess-…` de ma session et serait mort avec elle. Là, il ne dépend plus de moi. Pour l'arrêter : `systemctl --user stop mdserve-qtrinet`. Il est **transitoire** (pas de fichier d'unité) : il ne reviendra pas après un redémarrage — dis-moi si tu veux que j'en fasse une unité permanente (`~/.config/systemd/user/` + `enable`).

Deux remarques :

- **Port 8771, pas 8770** : ton port par défaut (racine `~/Data13TB/stephane`) reste libre, donc `mdopen fichier.md` continue de marcher comme avant. Si tu repasses par `mdopen -r <dépôt> --port 8771`, il **réutilisera** ce serveur (même port, même racine).
- **Une petite infirmité de `mdopen`, rencontrée en chemin** : il compare `realpath(racine)` mais seulement `abspath(fichier)`. Comme `~/GitHub` est un lien vers `~/Data13TB/stephane/GitHub`, il a refusé mes deux fichiers (« hors de la racine servie ») alors qu'ils étaient dedans. J'ai relancé avec le chemin canonique. Le correctif tient en une ligne (`os.path.realpath(f)` au lieu de `os.path.abspath(f)` à la ligne 98) — je te le fais ?

### Tour 6 — reprends les travaux là où on était rendu

*32 appels d'outils.* Actions notables :

- read
- bash — Read state docs and locate the designated next action
- bash — Recon the engine I/O path
- bash — Read the documented manque
- bash — Find the measurement source and existing madvise helper
- bash — Find prefetch call sites in the engine
- bash — Read the exact conditions of the known figure
- bash — Check prefetch history and canonical big-model pass
- write `/home/stephane/IA/outils/banc-prelire.py`
- bash — Measure page-fault vs cluster prefetch on array and HDD
- edit `/home/stephane/IA/outils/banc-prelire.py`
- edit `/home/stephane/IA/outils/banc-prelire.py`
- bash — Run the prefetch mechanism benchmark
- write `/home/stephane/IA/outils/banc-prelire.py`
- … et 13 autres

**Synthèse produite :**

⏵ Bilan de la reprise — S4 attaqué par sa mesure

J'ai repris par la check-list du dépôt (`REPRISE.md` § 1) : la journée avait laissé **une action désignée, seule** — `docs/strata-pour-drave.md` § 4 : **« S4 d'abord »**, le **préchargement ordonné**, adossé au manque chiffré de `docs/manques.md` § 1 (8,6 Mo/s en mmap à la demande contre 243 Mo/s en séquentiel).

**État du moteur, vérifié avant de coder** : `gguf::prelire()` existe (c'est `madvise(MADV_WILLNEED)`), et `model.rs:7986` précharge déjà… les experts de la **couche courante, juste avant de s'en servir**, dans l'ordre du routage. Ce qui manque est donc l'**ordre** et l'**avance**, pas le syscall. Et `DRAVE_PRELIRE=0` fournit déjà le bras témoin.

Comme une modification du moteur se paie d'une passe complète des 34 portes (85 min), j'ai d'abord fait la moitié « mesure » de la porte : `tools/banc-prelire.py` compare **trois ordres de lecture** sur le même fichier et les mêmes octets utiles.

| bras (médiane de 3 répétitions entrelacées) | disque dur | **raid0** |
|---|---|---|
| pages au hasard sur 2 Gio | 0,56 Mo/s | 29,43 Mo/s |
| pages consécutives | 16,27 Mo/s | 96,77 Mo/s |
| **grappes de 1 Mio, `madvise` puis parcours** | **30,56 Mo/s** | **1 230 Mo/s** |
| grappe ÷ à la demande | ×55 | **×42** |

Sur l'array — qui rend **7,45 Go/s** à huit lecteurs — la lecture à la demande laisse donc **~97 % de la bande passante inutilisée**, même en pages consécutives. C'est le mécanisme de S4, chiffré.

**Trois pièges trouvés en chemin, tous consignés dans la fiche** (le premier m'a donné une mesure fausse que j'ai failli publier) :

1. une fenêtre plus petite que la lecture en avance du noyau **n'est pas un hasard** : 400 pages dans 1,6 Mo ont rendu **300 Mo/s** — du cache, pas du disque ;
2. le contrôle à froid doit toucher une page **8 Mio à côté** de la zone mesurée, et le banc publie son temps (**12-36 ms** sur plateau = un vrai seek, **136-3 476 µs** sur l'array) ; sans ce témoin, « rapide » et « déjà en cache » sont indiscernables ;
3. `madvise` est **asynchrone** : on précharge la fenêtre *puis* on la parcourt.

Deux commits : `0c352069` (le banc dans `tools/`, la fiche `reports/rapport-prelire-grappe.md`, mesures et dispersion) et `77a72f81` (le journal du jour, cinq commits). Arbre propre. La fiche est déjà servie par le serveur de documentation que tu m'as fait lancer :

```
http://127.0.0.1:8771/?f=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prelire-grappe.md
```

**La suit
… [670 caractères tronqués]

### Tour 7 — travaille sur le cerveau jusqu'à demain 13 oct 8h00 hae

*171 appels d'outils.* Actions notables :

- create_goal
- bash — Find the canonical big-model pass invocation
- write `/home/stephane/GitHub/Qtrinet/tools/evincer-cache.py`
- bash — Tokenize ids and run a first cold pass
- bash — Compare on-demand vs current prefetch arms
- write `/home/stephane/GitHub/Qtrinet/tools/banc-experts.py`
- bash — Compare prefetch mechanisms on engine-like expert pattern
- edit `/home/stephane/GitHub/Qtrinet/tools/banc-experts.py`
- read
- edit `/home/stephane/GitHub/Qtrinet/tools/banc-experts.py`
- bash — Run expert-pattern mechanism comparison
- edit `/home/stephane/GitHub/Qtrinet/tools/banc-experts.py`
- bash — Rerun with per-zone eviction
- edit `/home/stephane/GitHub/Qtrinet/tools/banc-experts.py`
- … et 137 autres

**Synthèse produite :**

⏵ Ta lecture est confirmée par la mesure — et elle m'a fait trouver plus gros qu'elle

**Oui, et les chiffres vont dans ton sens — avec une correction importante.**

**(1) Ce que ta directive a produit dans le moteur.** J'ai implémenté exactement ce que tu décris pour le MoE : les experts **retenus** sont lus par `pread`, **par offset croissant** (donc en séquentiel), dans des tampons à nous, et le calcul lit ces octets au lieu du mapping (`DRAVE_TAMPONS=1`). Quatre bras, même passe, même fichier, cache évincé avant chacun :

| bras | octets lus | **passe** (hors chargement) | calcul |
|---|---|---|---|
| à la demande (`DRAVE_PRELIRE=0`) | 9,52 Go | 5,97 s | 5,70 s |
| `madvise` (l'ancien chemin) | 8,04 Go | 7,25 s | 7,00 s |
| fils qui entrent les pages (S4) | 10,90 Go | 3,70 s | 3,50 s |
| **tampons séquentiels (ta directive)** | **6,22 Go** | **3,40 s** | **3,20 s** |

Perplexité **799,8557 dans les quatre bras**. Les tampons sont **les plus rapides *et* les plus sobres** : la lecture en avance du noyau fait lire 10,90 Go là où la granularité fine n'en lit que 6,22. Ton intuition — « allocation intelligente plutôt que virtualiser » — est donc le seul bras qui gagne sur les deux tableaux, pas un compromis.

**(2) La correction que la mesure impose.** En cherchant pourquoi la passe ne gagnait pas plus, j'ai trouvé que **je mesurais la passe à travers son chargement** : le moteur construit **par défaut** 2,69 Go de « listes » des poids denses — **27,46 s** — et **ce chemin ne s'en sert pas** (le moteur l'écrit lui-même : « dont en listes : 0,0 M — le reste est dense »). Avec `--dense` : **7,77 s**, perplexité identique (6449,7333). Et ce chargement est **CPU, pas E/S** : 26,80 s à froid, **26,03 s à chaud**, 26,82 s à un seul fil.

Conséquence pour la suite : sur ce chemin, « lecture séquentielle » ne sert à rien — ce qu'il faut, c'est **ne pas construire ce qu'on ne lira pas** (construction paresseuse des listes, seulement quand un chemin de listes le demande). C'est **20 s par exécution** sur tous les modèles concernés, donc le prochain chantier, et il est plus payant que tout ce qu'on a fait ce soir sur l'E/S.

**(3) La VRAM, même principe — état et plan.** Aujourd'hui le cache d'experts en VRAM est un **LRU d'experts téléversés au hasard**, et il a été mesuré **perdant** (×1,09, +6 %) — exactement la maladie du mmap : transferts aléatoires, non recouvrés. Le même remède s'applique : lire l'expert **en séquentiel** dans un tampon RAM (c'est fait), puis 
… [1351 caractères tronqués]

### Tour 8 — <goal_round> Objective: "Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 08:00 HAE, en rounds autono … [934 caractères tronqués]

*227 appels d'outils.* Actions notables :

- bash — Read Proj::load to find the list construction
- bash — Locate the loader function
- bash — Read Proj::load body
- bash — Find the quantization flags
- bash — Compare dense, auto and q4 loading paths
- bash — Find the push/pull decision
- bash — Read the matvec dispatch (push vs pull)
- bash — Read the dispatch conditions
- bash — Check Gguf lifetime in production
- bash — Find how the Gguf is kept alive
- bash — Read the end of load_partiel
- bash — Find how mappings outlive the Gguf
- bash — Search for the mapping ownership trick
- bash — Measure push-path usage across modes
- … et 193 autres

**Synthèse produite :**

⏵ Tout est terminé et vérifié — voici le rapport de la nuit

**Nuit du 12 au 13 octobre — 30 commits, 6 fiches, 3 passes de portes.** Tout est mesuré, committé, arbre propre, 122 tests verts. Voici l'essentiel.

\## Le moteur : quatre changements, tous mesurés

| changement | avant | après | preuve |
|---|---|---|---|
| **Prélecture parallèle** des experts (S4) | calcul d'une passe 7,70 s | **3,65 s (−53 %)** | perplexité identique, défauts majeurs 957 170 → 4 188 |
| **Lecture séquentielle dans nos tampons** (`DRAVE_TAMPONS=1`) | 10,90 Go lus / 3,70 s (fils) | **6,22 Go / 3,40 s** | le seul bras qui gagne **et** sur les octets **et** sur le temps ; 4 bras, cache évincé |
| **Chargement paresseux** (forme « listes ») | 26,95 s (Qwen3-30B) · 6,85 s (0,5B) | **7,36 s** · **0,60 s** | sans déplacer un chiffre ; `porte-push-paresseux` le verrouille, vue rouge avec un défaut volontaire |
| **Pool de tampons VRAM** | 11,72 ms/expert MXFP4 (allocation) | **1,05 ms** en tampon réutilisé | **−11,6 % en bout de chaîne** à travail identique, perplexité inchangée — et une **fuite réparée** (`MatriceGpu` n'a pas de `Drop`) |

Ta directive est confirmée par les chiffres : la lecture séquentielle fine **gagne sur les deux tableaux**, et côté VRAM **91 % du coût d'un montage était l'allocation**, pas le lien. `MADV_POPULATE_READ` est tranché (2 121 Mo/s ≈ `madvise` par tranches, **2,2× sous** `pread` par 8 fils) : les tampons restent justifiés.

\## Le cerveau

- **Dessin H, sorties précoces (8 et 4)** : la question ouverte est fermée. La sortie 8 donne le meilleur produit théorique (**16,96 %** des paires au mieux, 4,8× la sortie 22) mais le **routeur réel y perd 0,30 point** — le facteur limitant reste la qualité du chemin court (N4).
- **La « loi de la frontière en N » n'existe pas seule** : sur **sept** textes, garder **la moitié** des clés coûte **+0,5 à +2,1 %** (robuste), garder le **quart** va de **+2,8 à +49,2 %** (facteur 17,6). Et les deux façons de dépenser la moitié — fenêtre pure ou fenêtre + puits — **se valent** : le partage est un paramètre d'implémentation, pas de qualité.

\## Les portes : 35 vertes sur 37

Trois passes complètes cette nuit. Les deux rouges sont **instruits, pas moteur** : le critère d'indice extérieur de `porte-indice`/`porte-melange` est **marginal par construction** (mesuré sur 5 fenêtres : 2 passent, 3 échouent). Je n'ai **pas** choisi la fenêtre qui passe : une porte verte obtenue en choisissant son entrée ne vérifie plus rien.

La fa
… [1877 caractères tronqués]

### Tour 9 — <goal_round> Objective: "Travailler sur le cerveau Drave (dépôt Qtrinet) jusqu'au 2026-10-13 08:00 HAE, en rounds autono … [934 caractères tronqués]

*28 appels d'outils.* Actions notables :

- bash — Read the buffer-read implementation
- bash — Read the rest and the call site
- bash — Read the MoE buffers call site
- bash — Add the buffer pool to gguf.rs
- bash — Read CacheExpertsRam
- bash — Return buffers to the pool and build
- bash — Add the pool stats and verify correctness
- bash — A/B the buffer pool against per-call allocation
- bash — Run tests and the preload gate
- bash — Write and commit the pool fiche
- bash — Launch the final pass after the pool change
- bash — Document the neutral pool result
- bash — Read the plan's first items for coherence
- bash — Fix the misleading sentence and commit
- … et 12 autres

**Synthèse produite :**

⏵ Objectif clos : voici le bilan final de la nuit

**Objectif atteint.** Tout ce qui était nommé est fait, mesuré, vérifié et committé — **35 commits**, **7 fiches**, arbre propre, 122 tests verts.

\## Les quatre items nommés

| item | état | preuve |
|---|---|---|
| **S4** : porte + préchargement ordonné | ✅ | `tools/porte-prechargement.sh` (verte, 106 s dans la dernière passe) ; `prelecture_parallele` + tampons dans le moteur : calcul d'une passe **7,70 s → 3,65 s (−53 %)** |
| **mesurer** | ✅ | 7 fiches dans `reports/` (S4, chargement, VRAM, pool, dessin H, frontière de fenêtre, fragilité NIAH, passes) |
| **garder les portes vertes** | ✅ 122 tests · porte-flux ✅ · **passe complète 35/37** | les 2 rouges sont **instruits et non moteur** (voir ci-dessous) |
| **fiches + journal + commits chaque round** | ✅ | `journal/2026-10-12_moteur.md`, `journal/2026-10-13_moteur.md`, 4 passes enregistrées dans `docs/references-non-regression.md` |

**Et les trois actions suivantes du § 6 :** array visible de `--materiel` (`be29ebc4`), lecteurs parallèles (prélecture, tampons, pool, verdict `MADV_POPULATE_READ`), dessin H sorties 8/4 (`e1e55caa`) — plus la question « loi de la frontière en N », que j'ai fermée.

\## Ce que la nuit a changé dans le moteur, chiffres à l'appui

- **chargement paresseux** : 26,95 s → **7,36 s** (Qwen3-30B), 6,85 s → **0,60 s** (0,5B), sans déplacer un chiffre ;
- **tampons séquentiels** : 6,22 Go lus / 3,40 s contre 10,90 / 3,70 pour les fils — le seul bras qui gagne sur les deux tableaux ;
- **pool VRAM** : **−11,6 %** à travail identique, perplexité inchangée, et une **fuite réparée** (`MatriceGpu` n'a pas de `Drop`) ;
- **pool de tampons de lecture** : **neutre en temps** — mon hypothèse des 250 000 défauts de page par jeton est **réfutée** (`glibc` réutilise déjà ces blocs). Je l'ai gardé pour borner la mémoire et rendre les allocations visibles, pas pour sa vitesse.

\## Les deux rouges, et pourquoi je ne les ai pas maquillés

`porte-indice` et `porte-melange` dépendent d'une botte de foin **jamais versionnée** (elle vivait dans `/tmp/campagne24`). J'ai mesuré leur critère sur **cinq fenêtres** : **2 passent, 3 échouent** — il est marginal par construction. J'aurais pu choisir la fenêtre qui passe : **je ne l'ai pas fait**, une porte verte obtenue en choisissant son entrée ne vérifie plus rien. À la place : l'entrée est versionnée (`tools/niah_4096_0.5.txt`), les rouges sont instruits, et la correction du critère est proposée par écrit
… [1542 caractères tronqués]

### Tour 10 — le rendu du premier tableau de etat-cerveau.md ne fonctionne pas . on voit le code au lieu du tableau dans http://127.0. … [9 caractères tronqués]

*43 appels d'outils.* Actions notables :

- read
- bash — Fetch the rendered page and inspect the table
- bash — Inspect the mdserve script
- bash — Find mdserve's routes
- bash — Fetch the render route and inspect
- bash — Decode the rendered HTML and inspect the first table
- bash — Inspect how the table rows are rendered and mdserve's renderer
- bash — Test a minimal table and read mdserve's renderer
- bash — Check bytes and bisect the table
- bash — Bisect header, separator and cells
- bash — Bisect the table row by row
- bash — Analyse the offending line
- bash — Read the full offending line
- edit `/home/stephane/GitHub/Qtrinet/docs/etat-cerveau.md`
- … et 29 autres

**Synthèse produite :**

⏵ Corrigé, vérifié dans le navigateur (via le HTML du serveur), et verrouillé par une porte

**C'était le document, pas le serveur.** Une seule ligne du tableau avait **4 cellules pour 5 colonnes** — le lien `note-cycle-c2.md` était resté dans la 4ᵉ colonne au lieu de la 5ᵉ (« où »). Le rendu (mistune) refuse alors **le tableau entier**, sans rien dire : les 14 lignes restent visibles en texte gris, donc personne ne le voit.

\## La bissection (et pourquoi le serveur est innocent)

| essai | résultat |
|---|---|
| un tableau minimal | ✅ rend (1 `<table>`) |
| l'en-tête réel + son séparateur | ✅ rend |
| + les lignes du corps, **une par une** | 12 sur 13 rendent — **la ligne C2 casse tout** |

Vérifié maintenant sur ton URL : le tableau « Les douze capacités » est bien un `<table>` de **14 lignes**, la ligne C2 comprise.

\## Ce n'était pas le seul

Balayage du dépôt : **17 lignes fautives dans 9 fichiers** (`docs/`, `reports/`, `journal/`), toutes corrigées :

| cause | correction |
|---|---|
| barres de valeur absolue dans une cellule (`\|gradient\|`, `\|w\|`, `\|dot\|`) | `∣` (U+2223), qui rend même **dans** un espace de code |
| cellule manquante (lien glissé d'une colonne) | cellule remise dans sa colonne |
| séparateur à 6 colonnes pour un en-tête à 5 | aligné (+ 7 lignes complétées) |
| tableau **triangulaire** (`rapport-minimal.md`) | en-tête élargi à 5 colonnes, trous en `—` |
| `\|` qui s'affichait **avec son antislash** | barre simple en prose, `∣` dans le code |
| ligne **orpheline** hors de son tableau (`M9`) | remise dans le tableau M |

\## La porte qui empêche la récidive

**`tools/porte-tableaux.sh`** (38ᵉ porte, ~1 s, **413 fichiers**) : en-tête ≡ séparateur ≡ chaque ligne, et aucun `\|` là où il s'afficherait. **Vue rouge** sur deux défauts volontaires (tableau à cellules inégales, barre échappée hors tableau).

Sa première version criait sur **tout** `\|` — 15 fausses alertes, y compris là où mistune le désérahappe légitimement. Je l'ai resserrée : *une porte qui crie là où tout va bien se fait ignorer.*

\## Fichiers et commits

- `reports/rapport-tableaux-casses.md` — la fiche (bissection, causes, porte)
- `docs/organisation-du-depot.md` § 1bis — la **règle d'écriture** qui manquait (3 points)
- `docs/references-non-regression.md` — la porte enregistrée, avec sa réserve : elle n'était pas encore dans une passe complète
- commit `3fdbb90f` ; arbre propre, tout est committé

**Ce qu'elle ne vérifie pas, et c'est écrit dans son en-tête** : le
… [395 caractères tronqués]

### Tour 11 — maintenat c'est à partir de "Ce que « C8 » recouvre, et où on en est." que ça dérape

*8 appels d'outils.* Actions notables :

- bash — Map the structure around the C8 blockquote
- bash — Move the blockquote after the table
- bash — Extend the gate to orphan rows and run it
- bash — Inspect the new real case and my own files
- bash — Restore the missing header and rephrase my own docs
- bash — Fix the cell and verify the gate and rendering
- bash — Full render verification of the reported file
- bash — Complete the fiche and commit

**Synthèse produite :**

⏵ Corrigé, et la porte apprend la classe de défaut que tu viens de révéler

**Exactement ça** : un bloc de **citation de 23 lignes** s'était glissé **au milieu** du tableau des capacités — entre la ligne C8 et la ligne C9. Tout ce qui suivait était donc **hors du tableau** : C9, C9×C1, C10, C11, C12, C12bis — **sept lignes**, visibles en texte gris, hors du cadre.

\## Ce que j'ai fait

- **Citation déplacée après le tableau** (elle porte sur la ligne C8, mais une note se lit après le tableau). Le tableau des capacités fait maintenant **21 lignes** rendues, C1 → C12bis d'un seul bloc ✓, et la citation suit.
- **Balayage étendu → un second cas réel** : `docs/plan-modeles-lourds.md` portait **neuf lignes de tableau sans en-tête ni séparateur**, collées à la citation au-dessus (donc rattachées à elle). En-tête et séparateur rendus, 5 colonnes comme ses lignes.

\## La porte apprend la leçon

Vérifier les lignes *d'un* tableau ne suffisait pas : il faut aussi vérifier qu'une ligne **qui a la forme** d'une ligne de tableau **appartient bien à un tableau**. C'est fait — et ça a immédiatement attrapé **mes propres fiches** :

1. j'y écrivais la séquence fautive dans un espace de code pour documenter la règle → reformulée ;
2. et dans une **cellule** de tableau, la barre littérale que j'écrivais redevenait un séparateur de colonnes (4 cellules au lieu de 3) → reformulée sans le caractère.

**Porte verte sur 414 fichiers**, vue rouge sur trois défauts volontaires (cellules inégales, antislash-barre, ligne orpheline).

\## Vérifié par le rendu, pas à l'œil

Sur ton fichier, via le HTML du serveur : tableaux source = rendus (**2/2**), tableau des capacités **21 lignes**, C8/C9/C10/C11/C12bis **dans** le tableau, citation **après**, **0** ligne restée en texte.

Commit `52c35b0a`, arbre propre. La fiche `reports/rapport-tableaux-casses.md` porte les deux classes de défaut et les deux cas réels.

Si tu vois encore une zone qui dérape ailleurs dans le dépôt, dis-moi le fichier et l'endroit : la porte couvre maintenant les trois classes, mais elle est **statique** — un tableau peut aussi mal rendre pour une raison qu'aucune de ces règles ne voit, et c'est le rendu, pas la règle, qui le dira.

### Tour 12 — travaille sur le cerveau jusqu'à midi

*41 appels d'outils.* Actions notables :

- create_goal
- bash — Read plan item 8 (C9/C4)
- bash — List the C8 tools and read c8_corpus
- bash — Read the head trainer's CLI
- bash — Read the training hint and calibrate the capture
- bash — Launch the 33-piece capture and read the trainer's output
- bash — Read the trainer's arguments
- bash — Wait for the capture to advance
- job_output
- bash — Check capture completion
- bash — Train heads on 4, 8, 15 and 30 pieces
- bash — Collect the scaling results
- bash — Test a higher-capacity adapter at equal data
- bash — Read the capacity test result
- … et 24 autres

**Synthèse produite :**

⏵ Objectif clos : voici le bilan de la matinée sur le cerveau

**Matinée du 13/10 (09 h 33 → 11 h 37) — 10 commits, tous committés, arbre propre, 122 tests verts.** La question ouverte du plan § 6.9 (« C8 : reste l'échelle ») est tranchée, et j'ai **corrigé deux de mes propres affirmations** en cours de route.

\## La mesure : C8 à l'échelle, sur un morceau jamais vu

Protocole : 33 morceaux de 1 024 jetons répartis dans le corpus, états de profondeur 16, entraînement sur les k premiers, **validation séparée** (m30+m31), **test sur m32** — jamais vu.

| morceaux (k) | perplexité TEST | écart au modèle complet (14,23) |
|---:|---:|---:|
| 4 | 1 032,58 | ×72,5 |
| 8 | 369,22 | ×25,9 |
| 15 | 260,81 | ×18,3 |
| **30** | **179,59** | **×12,6** |
| *(tête empruntée)* | *449 500,62* | *×31 580* |

\## Les trois conclusions

1. **La donnée paie encore, à rendements décroissants** (÷1,4 par doublement en fin de courbe) → fermer l'écart de ×12,6 demanderait ~4 000 morceaux *(extrapolation, écrite comme telle)*.
2. **La capacité n'est PAS la limite** : à données égales, un adaptateur **non linéaire** (896→512→896, GELU) rend **376,01**, soit **2,1× pire** → agrandir la tête est mesuré **contre-productif**.
3. **La profondeur de sortie est bon marché dès que le lecteur est entraîné** : 179,59 (16 couches) · 205,58 (12) · 267,98 (8) · **534,91** (4) — la tête **empruntée**, elle, s'effondre de 449 500 à **24,7 millions**. À un sixième du réseau, un lecteur entraîné rend 535 quand la tête du modèle rend 24,7 millions (÷46 000) : **l'information est dans l'état, c'est le lecteur qui manquait**. Et les deux leviers (données, profondeur) se multiplient largement.

**Donc le manque est bien N4** — entraîner le chemin court.

\## Les deux corrections que je me suis infligées

- J'avais écrit « le rapport 8/16 couches est ~×1,5 **constant** » → faux : il **dépend du texte** (×1,17 sur m20, ×1,49 sur m32). Corrigé dans la fiche, le plan et le journal.
- J'avais écrit « la tendance se transpose » → trop fort : de 15 à 30 morceaux, m32 gagne **÷1,45** et m20 gagne **÷22,8** (une falaise). **La forme de la courbe ne se transporte pas** ; seule la direction est robuste.

Ces deux-là viennent de contrôles que j'ai ajoutés *après* mes premières conclusions : **la graine pèse 0,7 %** (la courbe tient), **le morceau de test pèse ×10**. Sans eux, j'aurais livré une « loi » qui n'existe pas.

\## Livrables

- `reports/rapport-c8-echelle.md` — la fiche complète (courbe de données, courbe de
… [1121 caractères tronqués]

### Tour 13 — travaille sur le cerveau jusqu'à 18h00

*90 appels d'outils.* Actions notables :

- create_goal
- bash — Investigate the C9 exchange mechanism and engine flags
- bash — Check the forcing mechanisms and the MoE routing point
- bash — Read the flux format doc
- bash — Read the trace file format
- bash — Read the MoE router
- bash — Read the selection step and the token counter
- bash — Read both router call sites
- bash — Find the expert trace flag
- bash — Read the single-path trace writer and the token counter
- bash — Add the routing imposition machinery
- bash — Wire the imposition into the router and its call sites
- bash — Build after the routing changes
- bash — Declare the var, add tests, and run them
- … et 64 autres

**Synthèse produite :**

⏵ Objectif clos : voici le bilan de l'après-midi

**13/10, 12 h 57 → 17 h 02 — 7 commits, 42 pour la journée, arbre propre, 124 tests verts, passe complète à 37/39.** Les trois items nommés dans l'objectif sont faits, et **trois fois j'ai dû corriger ma propre conclusion** en cours de route.

\## C9 sur un modèle routé : le mécanisme, et un négatif

Il manquait le pendant de la capture (`DRAVE_TRACE_EXPERTS` écrivait déjà `couche cle e0 e1…`) : **`DRAVE_ROUTAGE_FORCER`** relit ce fichier et impose les experts, en gardant les poids du modèle pour les experts imposés.

- **L'invariant a d'abord été faux** : 37,2013 contre 37,1990 en s'imposant sa propre trace — la trace **trie** les experts, donc l'accumulation flottante change. `DRAVE_TRACE_EXPERTS_ORDRE=1` garde l'ordre de sélection → invariant **exact** (c'est le socle de toute la mesure).
- **Puis la mesure a menti** : imposer à A le routage de B à la dernière couche donnait **×0,81** — une amélioration de 19 % ! Les contrôles l'ont démonté : **tout** routage différent y bouge la perplexité de ±20-50 %, le **signe dépend du texte** (×0,81 · ×1,46 · ×1,26), l'aléatoire fait aussi bien ou mieux, et le sens inverse inverse l'ordre. **Pas de transfert latéral** — ce qui recoupe le « gain nul » de l'échange d'états.
- Ce qui reste vrai et intéressant : échanger *tout* le routage détruit le calcul (×92,6) mais **4× moins que l'aléatoire** — il porte donc un peu de structure commune, simplement inutilisable. Et la **couche 0** est de loin la plus sensible (×3,59).
- **Porte** `tools/porte-echange-experts.sh` : inerte par défaut, **exacte** sur son propre routage, vivante sur un étranger — **vue rouge** en retirant l'option d'ordre (54,4883 contre 54,5202).

\## Le critère des portes à aiguille : refait, et il tue l'effet

`porte-indice` comparait au **hasard** — un seuil qui dépend du texte. Elle construit maintenant une **question témoin** (même invite, même longueur, même position, mais qui ne désigne pas l'aiguille) et compare les deux distances sur le **même** magasin :

| botte de foin | indice réel | **témoin** | hasard |
|---|---:|---:|---:|
| versionnée | 482 | **459** | 370 |
| fenêtre qui passait le hasard | 315 | **1** | 381 |

**Le témoin égale ou bat l'indice réel** : ce que la porte mesurait n'est pas porté par le sens de la question. Les deux rouges restent, mais leur cause est désormais **structurelle et nommée**.

\## N4 : l'expérience demandée, et ce qu'elle impose

`tools/predictibilite_etats.py
… [2004 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/IA/outils/banc-io.py` | 2 | 2 |
| `/home/stephane/IA/outils/migrer-vers-raid.sh` | 1 | 0 |
| `/home/stephane/IA/outils/etat-raid.sh` | 1 | 0 |
| `/home/stephane/IA/outils/migration-phase2.sh` | 1 | 0 |
| `/home/stephane/.bashrc` | 0 | 4 |
| `/home/stephane/IA/README.md` | 1 | 9 |
| `/home/stephane/IA/docs/rapport-raid0-pour-le-depot.md` | 3 | 0 |
| `/home/stephane/IA/modeles-lourds/README.md` | 0 | 1 |
| `/home/stephane/IA/artefacts/README.md` | 0 | 1 |
| `/home/stephane/IA/outils/banc-numa-raid.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-raid0-nvme.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/docs/etat-cerveau.md` | 0 | 8 |
| `/home/stephane/GitHub/Qtrinet/REPRISE.md` | 0 | 1 |
| `/home/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md` | 0 | 1 |
| `/home/stephane/GitHub/Qtrinet/journal/2026-10-12_mesures.md` | 0 | 2 |
| `/home/stephane/IA/outils/banc-prelire.py` | 3 | 3 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-prelire-grappe.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/journal/2026-10-12_moteur.md` | 0 | 2 |
| `/home/stephane/GitHub/Qtrinet/tools/evincer-cache.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/banc-experts.py` | 1 | 7 |
| `/home/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs` | 0 | 4 |
| `/home/stephane/GitHub/Qtrinet/drave-core/src/model.rs` | 0 | 2 |
| `/home/stephane/GitHub/Qtrinet/drave-core/src/materiel.rs` | 0 | 1 |
| `/home/stephane/GitHub/Qtrinet/tools/porte-prechargement.sh` | 1 | 4 |
| `/home/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 1 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-s4-prechargement-moteur.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/docs/manques.md` | 0 | 2 |
| `/home/stephane/GitHub/Qtrinet/docs/strata-pour-drave.md` | 0 | 2 |
| `/home/stephane/GitHub/Qtrinet/tools/porte-m5-brouillon.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/docs/note-lecteurs-paralleles.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/construire-niah.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/porte-topologie.sh` | 0 | 2 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-chargement-paresseux.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-vram-transfert.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/porte-push-paresseux.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-niah-fragilite.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-passe-complete-13-octobre.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-design-H-sorties-precoces.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/porte-tableaux.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/porte-echange-experts.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/loi-fenetre-textes.sh` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect block devices, mounts and RAID status
- **T1** Show working dir, DSH env vars and home contents
- **T1** List RAID0 mount contents and sizes
- **T1** Inspect FastNVMe dir and fstab entries
- **T1** Read phase-1 migration script and logs
- **T1** List RAID0 content directories in detail
- **T1** Check RAID detail and NVMe SMART health
- **T1** Inspect shell env, AI cache variables and cache sizes
- **T1** Measure Ollama models, artefacts and large files on root
- **T1** Read RAID array state from sysfs
- **T1** Read migration READMEs and look for plan notes
- **T1** Inspect current project repo state
- **T1** Check tmp mounts, I/O tools and fstrim status
- **T1** Measure repo size, cargo target and tmp usage
- **T1** Check RAM, CPU and admin tool availability
- **T1** Locate large HDD test files and repo models
- **T1** Run I/O benchmark across all three storage tiers
- **T1** Run I/O benchmark across all three storage tiers
- **T1** Check kernel logs for real I/O errors
- **T1** Probe O_DIRECT alignment rules on both filesystems
- **T1** Re-check md error counters after benchmark
- **T1** Reproduce alignment failures with random offsets on btrfs
- **T1** Test whether btrfs compression causes O_DIRECT EIO
- **T1** Test determinism of DIO failures and buffered readability
- **T1** Cross-test shared versus per-thread descriptors
- **T1** Run corrected I/O benchmark on all tiers
- **T1** Check hardcoded target and model paths in project tools
- **T1** Inspect Ollama service configuration and model store
- **T1** Check Ollama override, model store, repos and K3 shards
- **T1** Check Ollama file permissions and duplicate model copies
- **T1** Create RAID layout, check cargo and LM Studio data
- **T1** Inspect unexpected target dir and LM Studio sizes
- **T1** Time clean release build with target on HDD
- **T1** Time clean release build with target on RAID
- **T1** Migrate HuggingFace cache to RAID
- **T1** Delete HF original and migrate ccache
- **T1** Migrate qwen3-30b GGUF with SHA-256 verification
- **T1** Test RAID status tool
- **T1** Run phase-2 migration in background
- **T1** Find output paths used by campaign tools
- … et 576 autres

## 4. Mesures et résultats marquants

- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /`
- **T1** `efivarfs                efivarfs  256K  107K  145K  43% /sys/firmware/efi/efivars`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /.snapshots`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /opt`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /home`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /root`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /srv`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /usr/local`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /var`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /home/stephane/FastNVMe`
- **T1** `/dev/nvme2n1p2          btrfs     828G  118G  709G  15% /var/lib/docker`
- **T1** `/dev/nvme2n1p1          vfat      2,0G  904M  1,2G  45% /boot/efi`
- **T1** `/dev/mapper/system-root btrfs      11T  8,8T  2,1T  81% /home/stephane/Data13TB`
- **T1** `/dev/md0                ext4      938G  684G  245G  74% /home/stephane/IA`
- **T1** `/dev/nvme2n1p2  828G  802G   26G  97% /`
- **T1** `/dev/md0        938G  684G  245G  74% /home/stephane/IA`
- **T1** `mmap du fichier en 27,97 ms (365,7 Go adressés)`
- **T1** `VmRSS: 265 Mo                        <- le mmap fonctionne parfaitement`
- **T1** `**16 ms par lecture de 264 octets.** C'est un seek sur disque mécanique`
- **T1** `(0,06 Go/s en aléatoire, mesuré). Or un jeton lit ~4 n-grammes × 2 couches`
- **T1** `d'engram : **128 ms par jeton** rien qu'en accès à la table.`
- **T1** `un disque mécanique, et le meilleur cas pour un NVMe (0,07 ms par page).`
- **T1** `* disque mécanique : **~210 Mo/s** en écriture soutenue (mesuré sur 81 Go),`
- **T1** `1,3 Go/s en pointe sur des zéros compressés — donc ~210 Mo/s pour de vrais poids ;`
- **T1** `* NVMe : **2,1 Go/s** en lecture (mesuré) ;`
- **T1** `# attendu : perplexité 15,2789 (identique au modèle d'origine, un seul fichier)`
- **T1** `[still running after 60000ms; moved to background job bash-16]`
- **T1** `raid0 md0 (4xNVMe)         1.98 Go/s     8180 i/s    113µs     7632 i/s    126µs (p95   168µs) QD32   45442 i/s    3.44 Go/s`
- **T1** `nvme2n1p2 (btrfs)          1.48 Go/s     5185 i/s    173µs     5766 i/s    148µs (p95   350µs) QD32   33094 i/s    1.19 Go/s`
- **T1** `sda2 HDD (btrfs LVM)       0.23 Go/s       89 i/s   9813µs       39 i/s  27418µs (p95 37416µs) QD32     195 i/s    0.24 Go/s`
- **T1** `O_DIRECT : 0 blocs en EIO sur 5000 échantillons (0.00 %)`
- **T1** `raid0 md0 (4xNVMe)       1.95 Go/s    7.45 Go/s    10058 i/s    92µs    57623 i/s   101µs    10035 i/s    92µs p95   131µs   2.86 Go/s  0`
- **T1** `nvme2n1p2 (btrfs)        1.15 Go/s    3.47 Go/s     9065 i/s   108µs    54430 i/s   122µs    12124 i/s   103µs p95   168µs   1.13 Go/s  0`
- **T1** `sda2 HDD (btrfs LVM)     0.27 Go/s    0.29 Go/s      108 i/s  8646µs      207 i/s 21323µs       39 i/s 27713µs p95 36141µs   0.35 Go/s  0`
- **T1** `/dev/mapper/system-root   11T  8,8T  2,1T  81% /home/stephane/Data13TB`
- **T1** `########## MIGRATION 2/3 : ccache (527 Mo) ##########`
- **T1** `/dev/nvme2n1p2  828G  112G  715G  14% /`
- **T1** `/dev/md0        938G  708G  221G  77% /home/stephane/IA`
- **T1** `capacité : 708Go utilisés / 938Go — 221Go libres (77 %)`
- **T1** `✓ sain, 77 % utilisé`
- **T1** `docs/numa-segregation.md:39:| NVMe | `nvme0n1`, 931 Go, **nœud 0** — monté `FastNVMe`, **97 % plein (29 Go libres)** | `/sys/block/.../numa_node`, `df` |`
- **T1** `docs/numa-segregation.md:279:(`FastNVMe`, 828 Go, **97 % plein, 29 Go libres**) :`
- **T1** `/dev/md0        938G  720G  209G  78% /home/stephane/IA`
- **T1** `/dev/md0        938G  724G  205G  79% /home/stephane/IA`
- **T1** `[still running after 60000ms; moved to background job bash-45]`
- **T1** `/dev/md0        938G  739G  189G  80% /home/stephane/IA`
- **T1** `sda : lecture 221 Mo/s   écriture 0 Mo/s`
- **T1** `/dev/md0        938G  747G  182G  81% /home/stephane/IA`
- **T1** `/dev/md0        938G  750G  179G  81% /home/stephane/IA`
- **T1** `/dev/md0        938G  756G  173G  82% /home/stephane/IA`
- **T1** `capacité : 766Go utilisés / 938Go — 162Go libres (83 %)`
- **T1** `✓ sain, 83 % utilisé`
- **T1** `/dev/nvme2n1p2           828G  112G  715G  14% /`
- **T1** `/dev/mapper/system-root   11T  8,9T  2,0T  82% /home/stephane/Data13TB`
- **T1** `/dev/md0                 938G  766G  162G  83% /home/stephane/IA`
- **T2** `> vérification de la chaîne : `tools/verifier_chaine_etat.py` (0,013 % et 0,006 %).`
- **T2** `> (2×32 Go par socket), et les deux Quadro restent en x16 avec NVLink.`
- **T2** `| RAM | 64 Go (2×32, canaux 0-1) | 64 Go (2×32, canaux 0-1) |`
- **T2** `| GPU | **2 × Quadro RTX 5000, x16, NVLink 25,78 Go/s** | Yeston AMD 6×mini-DP (affichage) |`
- **T2** `faire tomber les GPU en x8, mesuré à **6,5 Go/s** au lieu de ~13). Le bureau et`
- **T2** `écoule ~12-14 Go/s utiles par sens ; un array à 6-8 Go/s en occupe donc la moitié.`
- **T2** `Les mesures du dépôt donnent une pénalité de **3 à 4 %** pour traverser le QPI`
- **T2** `cpu0+mem0      1.80 Go/s    7.47 Go/s   (1 flux min/max 1.69/2.23 · 8 flux min/max 7.30/7.47)`
- **T2** `cpu1+mem1      2.22 Go/s    7.42 Go/s   (1 flux min/max 1.81/2.25 · 8 flux min/max 7.15/7.43)`
- **T2** `cpu0+mem1      2.11 Go/s    7.41 Go/s   (1 flux min/max 1.74/2.16 · 8 flux min/max 7.28/7.42)`
- **T2** `CPU  20 cœurs physiques · 40 threads logiques · 2 sockets NUMA · caches L1 32 Ko · L2 256 Ko · L3 25600 Ko`
- **T2** `[materiel] taille d'expert introuvable (couche 0) : le plan utilisera 9,95 Mo par expert, valeur de DeepSeek-V4.1`
- **T2** `· threads = 20 cœurs physiques (40 logiques détectés) — au-delà, la bande passante mémoire sature : 20 cœurs = 22,5 Go/s, 20 cœurs + hyperthreads = 18,9`
- **T2** `· lecteurs disque = 16 — le NVMe passe de 5,4 Go/s (1 lecteur) à 31,1 (16), soit ×6 ; c'est ce qui rend le chargement à la demande viable`
- **T2** `· cache d'experts VRAM = 21.1 Go — 31.1 Go libres moins 2 de réserve CUDA et 8 pour le commun ; la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM`
- **T2** `· NVLink détecté (25,8 Go/s, 2× le PCIe) : les échanges entre cartes passent par lui sans réglage`
- **T2** `· cache KV en 32 bits — à 512 jetons il pèse 0.0 Go en F16, soit 0 % de la RAM libre (123 Go)`
- **T2** `/dev/nvme2n1p2  828G  111G  716G  14% /home/stephane/FastNVMe`
- **T2** `[still running after 600000ms; moved to background job bash-75]`
- **T2** `perplexité 17.4702 sur`
- **T2** `deux nœuds        : perplexité 30.4363  (10.8 s)`
- **T2** `deux nœuds        : perplexité 30.4363  (11.0 s)`
- **T2** `deux nœuds        : perplexité 30.4363  (11.2 s)`
- **T2** `deux nœuds        : perplexité 30.4363  (11.4 s)`
- **T2** `deux régions / deux instances :   deux nœuds        : perplexité 42.5477  (6.1 s)`
- **T2** `deux nœuds        : perplexité 42.5477  (6.3 s)`
- **T2** `RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,`
- **T2** `**47,78 % contre 47,73 %**, soit **+0,05 point** sur 2 001 jetons : **dans le bruit**. Aux`
- **T2** `atteignable est donc **0,39 %** des paires (4,7 % des jetons × 2 couches sur 24), c'est-à-dire`
- **T2** `**Le chiffre à retenir** : entre la borne (12,6 %) et le gain atteignable (0,39 %), il y a un`
- **T2** `- **elle ne teste qu'un texte**, une graine et un type d'adaptateur (linéaire 896×896). Le chiffre`
- **T2** `220:**7. C8 — la tête entraînée généralise (÷540 même texte, ×5,7 du modèle sur un texte neuf avec 30 morceaux) ; reste l'échelle.** Décodabilité mesurée à 4, 8, 12, 16,`
- **T2** `[still running after 60000ms; moved to background job bash-85]`
- **T2** `be29ebc4 Machine : le raid0 de 4 NVMe est en service et mesuré — 7,45 Go/s à 8 lecteurs contre 1,95 à un (×3,8), QPI sans coût mesurable aux trois placements, DRAM-less confirmé en aléa QD1`
- **T2** `| 18:20 | `be29ebc4` | Machine : le raid0 de 4 NVMe est en service et mesuré — 7,45 Go/s à 8 lecteurs contre 1,95 à un (×3,8), QPI sans coût mesurable aux trois placements, DRAM-less confirmé en aléa `
- **T2** ``×3,8` · `7,45 Go``
- **T2** `/dev/nvme2n1p2           828G  111G  716G  14% /`
- **T2** `/dev/nvme2n1p2           828G  111G  716G  14% /home/stephane/FastNVMe`
- **T4** `3. Rendu par ton navigateur (Blink) : ~0,9 s pour 362 Ko, ~3,3 s pour 8,3 Mo.`
- **T5** `CPU: 532ms`
- **T6** `gguf.rs:78:/// Mesuré : charger 18,6 Go prend 6,8 s en mmap paresseux (2,7 Go/s) — proche du`
- **T6** `| **M5** | **décodage spéculatif** — aucune ligne de moteur | brouillon générique ×0,70 · paire alignée ×1,09 · brouillon minuscule **×1,52** | la latence du décodage ; mais le cahier des charges est `
- **T6** `| **M6** | **le moteur n'apprend pas** — il applique, mesure, sauve et recharge une matrice additive, mais ne touche jamais aux poids | notre seule règle locale est **réfutée** (transfert nul, −5 à −1`
- **T6** `**8,6 Mo/s sur disque dur** contre 243 Mo/s en séquentiel (÷28) — un préchargement`
- **T6** `| **N1** | **structure innée à l'échelle** — gratuite à 25 % à dim 384 (+1,0 %), coûteuse à 12,5 % (+13,7 %) **et à dim 512 (+6,7 %)** | E1 et m16, mesurés | un connectome inné viable demande un masqu`
- **T6** `| **N4** | **profondeur routée** (mixture-of-depths), **budget d'événements appris**, **quantification adaptée aux listes** | dessins évalués, **jamais entraînés** — et pour H la **borne est maintenan`
- **T6** `| **N5** | **mémoire d'un signal injecté** — le modèle n'en a aucune | sonde linéaire **et** non linéaire sur l'état de sortie : le signal **courant** est lisible (**R² 0,992**) mais celui d'il y a 8 `
- **T6** `===== source du chiffre 8,6 Mo/s vs 243 Mo/s =====`
- **T6** `docs/plan-cerveau-complet.md:211:  (0,210 ns par événement valorisé, 8,6 Mo/s en mmap sur disque dur, 3,4 ms par`
- **T6** `docs/modularisation.md:100:**deux lecteurs du même fichier de 63 Go font tomber le débit effectif à 8,6 Mo/s**`
- **T6** `docs/modularisation.md:101:(contre 243 Mo/s en séquentiel), et les deux tentatives de porte gpt-oss ont expiré`
- **T6** `docs/modele-pour-drave.md:25:| lecture mmap **8,6 Mo/s** sur disque dur contre 243 Mo/s en séquentiel (§ 12 bis) | le moteur lit par défauts de page : sur un plateau, une page aléatoire coûte ~5 ms | `
- **T6** `docs/modele-pour-drave.md:58:- **la lecture** : les paires doivent venir du disque. Mesuré le 9/10 : **8,6 Mo/s`
- **T6** `docs/modele-pour-drave.md:59:  en mmap sur disque dur contre 243 Mo/s en séquentiel** (`dd` direct) — soit ÷28.`
- **T6** `docs/modele-pour-drave.md:164:Sur disque dur, le moteur lit à **8,6 Mo/s** là où le disque donne 243 Mo/s : la`
- **T6** `docs/manques.md:24:**8,6 Mo/s sur disque dur** contre 243 Mo/s en séquentiel (÷28) — un préchargement`
- **T6** `/// parallèle — et c'est ce qui compte, parce que le NVMe passe de 5,4 Go/s à un`
- **T6** `/// lecteur à **31 Go/s à seize**.`
- **T6** `/// Mesuré : charger 18,6 Go prend 6,8 s en mmap paresseux (2,7 Go/s) — proche du`
- **T6** `/// Cette demande vise le débit parallèle, 31 Go/s.`
- **T6** `860-        // 40** (`Percent of CPU this job got: 99%`), avec 119 Ko lus en 47 s`
- **T6** `**deux lecteurs du même fichier de 63 Go font tomber le débit effectif à 8,6 Mo/s**`
- **T6** `(contre 243 Mo/s en séquentiel), et les deux tentatives de porte gpt-oss ont expiré`
- **T6** `25:| lecture mmap **8,6 Mo/s** sur disque dur contre 243 Mo/s en séquentiel (§ 12 bis) | le moteur lit par défauts de page : sur un plateau, une page aléatoire coûte ~5 ms | un modèle dont les poids a`
- **T6** `(mesuré : ×0,02 à vide, ×1,54 à 50 %, ×3,19 à densité 1). **Un modèle ad hoc doit`
- … (tronqué)

## 5. Erreurs rencontrées

18 sorties en erreur ou divergentes. Les premières :

- **T1** : ===== mdadm detail ===== sudo: a password is required ===== smart (nvme0..4) ===== --- nvme0n1 --- nvme1n1 --- nvme2n1 --- nvme3n1 --- nvme4n1 [exit code: 1]
- **T1** : ===== taille repo & target ===== 1,2G	. 16K	bench 980K	docs 2,5M	reports 16M	drave-core 99M	data 146M	journal ===== data/ ===== bench: total 16 drwxr-xr-x. 1 stephane stephane   40 25 sep 15:38 . drwx
- **T1** : support                 séq. lecture          aléa 4K QD1          aléa 512o QD1  séq. écriture Traceback (most recent call last):   File "/home/stephane/IA/outils/banc-io.py", line 144, in <module>  
- **T6** : ===== quand prelire_expert est-il arrivé ? ===== b2bc093b Detection materielle et heuristiques de configuration automatique  ===== le même pour la prélecture MoE (commentaire « Prélecture ») ===== ac8
- **T6** : ########## 1. RAID0 (l'array) ########## fichier : DeepSeek-V4.1-Flash-Q2.gguf (365.7 Go) — 2000 pages (8.2 Mo) par bras, 3 répétitions entrelacées, grappe 256 pages bras               Mo/s   détail  
- **T6** : ########## HDD (chiffre connu : 8,6 Mo/s au hasard · 243 Mo/s séquentiel en dd) ########## fichier trop petit (63.4 Go) pour 9 zones de 9 Gio — réduire --pages [exit code: 1]
- **T7** : --- --- PushMat : [exit code: 1]
- **T7** : demande         mural 0:33.15  ·  9,00 Go lus · défauts majeurs     60568 · calcul       s · ppl 799.8557   experts         mural 0:30.47  · 10,00 Go lus · défauts majeurs      4202 · calcul       s ·
- **T7** : [stderr]   File "<stdin>", line 15     PY''', '''print("  PORTE TENUE" if ok else "  PORTE ROUGE")            ^ SyntaxError: unterminated triple-quoted string literal (detected at line 16) bash: -c: l
- **T7** : test trace_globale::tests::la_v1_reste_lisible_et_perd_seulement_son_horodatage ... ok test trace_globale::tests::verifier_detecte_la_divergence_et_la_nomme ... ok test trace_globale::tests::refuse_un
- **T7** : bras populate ajouté [stderr] Traceback (most recent call last):   File "<string>", line 1, in <module>     import ast;ast.parse(open('/home/stephane/GitHub/Qtrinet/tools/banc-experts.py').read());pri
- **T7** : thread 'tests_vars::les_vars_lues_sont_completes' (852011) panicked at src/main.rs:8192:13: DRAVE_TAMPONS est lu dans le source mais absent de VARS_LUES : un ancien nom QT_TAMPONS resterait muet   fai
- **T8** : ---- tests_vars::les_vars_lues_sont_completes stdout ----  thread 'tests_vars::les_vars_lues_sont_completes' (863005) panicked at src/main.rs:8196:13: DRAVE_PUSH_TOT est lu dans le source mais absent 
- **T8** : vertes=0; rouges=0; liste_rouges="" echo "=== PASSE COMPLÈTE DES PORTES ($(printf '%s\n' $portes | grep -c . ) portes, borne ${DELAI} s) ===" echo "    journaux : $JOURNAUX" for g in $portes; do     n
- **T8** : [stderr] Traceback (most recent call last):   File "<stdin>", line 11, in <module> OSError: [Errno 22] Invalid argument [exit code: 1]

## 6. Commits

- Machine : le raid0 de 4 NVMe est en service et mesuré — 7,45 Go/s à 8 lecteurs contre 1,95 à un (×3,8), QPI sans coût mesurable aux trois placements, DRAM-less 
- Journal du 12/10 : le raid0 en service (trois commits dans la journée) — récit et chiffres dans le bloc notes du thème mesures" && git log --oneline -3 echo "==
- S4 : le préchargement par grappe mesuré hors du moteur — 1 230 Mo/s contre 29,43 à la demande sur l'array (×42), et 30,56 contre 0,56 sur le disque dur" -m "Le 
- Journal du 12/10 : S4 commence par la mesure du mecanisme (grappe x42 sur l'array), cinq commits dans la journee" && git log --oneline -3 echo "--- arbre :"; gi
- S4 : la prelecture parallele des experts entre dans le moteur — le calcul d'une passe tombe de 7,70 a 3,65 s (-53 %), perplexite identique ; l'idee de Strata (c
- M5/S1 : la porte du brouillon verifie ce qui est verifiable — le fichier declare ses 3 couches (cibles 37-39) et porte ses 75 tenseurs ; vue ROUGE sur un modele
- Docs : note de conception des lecteurs paralleles — le chiffre qui ouvre le chantier (pread par 8 fils : 3 995 Mo/s contre 1 126 a la demande), ce qui existe de
- S4 (suite) : la lecture sequentielle dans nos tampons — 6,22 Go lus et passe de 3,40 s contre 10,90 Go et 3,70 s pour les fils ; perplexite identique dans les q
- Chargement : la forme « listes » devient paresseuse — 26,95 s a 7,36 s (Qwen3-30B) et 6,85 s a 0,60 s (0,5B), sans deplacer un chiffre" -m "La forme PushMat eta
- VRAM : ce qui coute n'est pas le lien mais l'ALLOCATION — 11,72 ms par expert MXFP4 avec allocation contre 1,05 ms dans un tampon reutilise (91 % du cout), et 3
- Le fichier d'entree des trois portes a aiguille est VERSIONNE — un prerequis de mesure qui vit dans /tmp rend la mesure non reproductible" -m "porte-greffe, por
- Fiches : horodatages rectifies — l'heure se lit, elle ne se suppose pas (REPRISE.md § 1) ; mes trois fiches de la nuit portaient des heures estimees au lieu des
- La porte de la paresse : l'inference prend le chemin push (93 tenseurs construits a la demande), les passes --ppl aucun — meme texte gourmand, chargement 5,2x p
- Plan du cerveau : trois items soldes (array visible, lecteurs paralleles en tampons, chargement paresseux) et deux neufs (VRAM : allocation 37-91 % du cout ; le
- Manques : le manque de methode a deux pas faits et mesures — la prelecture parallele (calcul -53 %) puis les tampons sequentiels (6,22 Go / 3,40 s contre 10,90 
- VRAM : un pool de tampons dans le cache d'experts — -11,6 % a travail identique (memes 264 montages, perplexite 27736,1204 inchangee), et une fuite reparee (Mat
- Repères : la passe du 12/10 23h00 est consignée (36 portes, 34 vertes, 2 rouges nommes et instruits) — les valeurs des portes n'ont pas bouge" && git log --onel
- Le critere de porte-indice ne survit pas a une reconstruction de son entree : 2 fenetres sur 5 passent (1,21x et 1,69x mieux que le hasard), 3 echouent (jusqu'a
- Journal du 12/10 (theme moteur) : le recit de la nuit — quatre mesures, quatre changements (prelecture parallele, tampons sequentiels, chargement paresseux, poo
- Note des lecteurs paralleles : etat au 13/10 — les tampons sont dans le moteur et gagnent sur les octets ET sur le temps (6,22 Go / 3,40 s)" && git log --onelin
- Journal du 13/10 : renvoi vers le recit de la nuit (le travail a bascule apres minuit, les commits sont dates par git)" && git log --oneline -1
- La passe a attrape ma porte : elle lisait << chargees en Xs >> alors que le moteur imprime << 601.03ms >> sous la seconde — elle passait sur une machine lente e
- MADV_POPULATE_READ tranche : 2 121 Mo/s contre 2 077 pour madvise par tranches et 4 603 pour pread par 8 fils — il ne remplace pas les tampons (2,2x sous le dis
- Fiche des deux passes de la nuit : ce qu'elles ont attrape (quatre portes muettes qui dependaient de /tmp, et ma propre porte fragile a l'unite d'un nombre) et 
- Chargement : je corrige une affirmation d'hier soir — sur 32 jetons l'emprunt des blocs Q4_K est 0,63 % MOINS precis (33,9093 contre 33,6967), pas plus fidèle ;
- Dessin H : les sorties precoces mesurees (8 et 4) — le produit theorique monte a 16,96 % mais le routeur REEL y perd 0,30 point ; le facteur limitant est bien l
- Plan, item 6 (dessin H) : les sorties precoces sont mesurees — reponse non, chiffree (16,96 % au mieux a la sortie 8, mais -0,30 point de justesse pour un route
- Cinq outils de plus branches sur tools/_corpus.sh : la famille << prerequis dans /tmp >> est fermee (le corpus est regenere au lieu d'etre suppose)" && git log 
- La frontiere de la fenetre n'a pas de loi en N : garder la moitie des cles coute <=2 % sur TROIS textes (+0,5/+1,9/+0,8), garder le quart coute +5 a +49 % (fact
- Journal du 13/10 : la seconde moitie de la nuit (dessin H aux sorties precoces, la loi de la frontiere, POPULATE_READ tranche, la famille /tmp fermee, et ma por
- Passe de certification (03h59) : 35 vertes sur 37, et porte-push-paresseux VERTE dans la passe — la correction est verifiee dans les conditions ou le defaut eta
- Frontiere de la fenetre : SEPT textes au lieu de trois — N/2 tient partout (+0,5 a +2,1 %) et N/4 va de +2,8 a +49,2 % (facteur 17,6)" -m "Le meme reglage, sept
- Plan 6.7 : sept textes au lieu de trois (N/2 de +0,5 a +2,1 %, N/4 de +2,8 a +49,2 %)" && git log --oneline -1
- Les deux facons de depenser la moitie des cles se valent : fenetre 1024 pure (+0,5 a +2,1 %) et fenetre 512 + 512 puits (+0,3 a +2,1 %) sur les sept memes texte
- Plan 6.7 : les deux facons de depenser la moitie des cles se valent (fenetre pure ou fenetre + puits) — le partage est un parametre d'implementation" && git log
- Pool de tampons : neutre en temps (2,4 s avant, 2,3-2,4 apres) — et l'hypothese des 250 000 defauts de page par jeton est REFUTEE (glibc reutilise les blocs de 
- Docs : le pool de tampons est fait et NEUTRE en temps (hypothese refutee) — garde pour borner la memoire et rendre les allocations visibles ; le recouvrement re
- Plan, item 3 : la phrase melangeait deux mesures differentes (2,3 s de passe contre 3,05 s de calcul de la porte) — corrigee, et le recouvrement est dit a faibl
- Quatrieme passe (06h19) apres le pool de tampons : 35 vertes sur 37, memes deux rouges instruits, memes valeurs — et le pool est neutre en temps (mesure a part,
- Un tableau Markdown qui ne rend pas est un tableau qui n'existe pas : 17 lignes dans 9 fichiers corrigees, et une 38e porte (porte-tableaux.sh) pour empecher la
- Tableau interrompu : la citation C8 coupait le tableau des capacites en deux (sept lignes orphelines, C9 a C12bis) — citation deplacee apres, en-tete rendu au t
- C8 a l'echelle : la courbe monte encore (1032,58 -> 179,59 de 4 a 30 morceaux) mais un adaptateur NON LINEAIRE a donnees egales rend 376,01, soit 2,1x PIRE — la
- C8 : la profondeur de sortie est un levier bon marche des que le lecteur est entraine — 179,59 (16 couches) / 267,98 (8) / 534,91 (4) contre 449 500 a 24,7 MILL
- C8 : controles de robustesse — la graine pese 0,7 % (la courbe tient), le morceau de test pese x10 (17,35 sur m20 contre 179,59 sur m32) ; les valeurs absolues 
- C8 : les deux leviers (donnees, profondeur) se multiplient — le rapport 8/16 couches reste ~1,5 que l'on ait 4, 15 ou 30 morceaux (1,69 / 1,47 / 1,49)" && git l
- Journal du 13/10 : la matinee C8 — la donnee paie encore, la capacite non, la profondeur est bon marche des que le lecteur est entraine, et les deux leviers se 
- C8 : courbe de profondeur complete (4/8/12/16 couches : 535 / 268 / 206 / 180) — et je corrige ma propre affirmation : le rapport 8/16 n'est pas constant, il de
- Journal du 13/10 : courbe de profondeur a quatre points, et la correction de ma propre affirmation (le rapport depend du texte, 1,2 a 1,7)" && git log --oneline
- Note de conception : entrainer le chemin court (N4) — trois dessins du moins cher au plus cher, et cinq portes ecrites AVANT le code (invariant d'identite, temo
- C8 : la FORME de la courbe ne se transporte pas d'un texte a l'autre — de 15 a 30 morceaux, m32 gagne /1,45 et m20 gagne /22,8 (falaise) ; seule la direction (p
- C9 sur un modele route : echanger les choix d'experts ne transfere RIEN — et la mesure a d'abord menti (x0,81, un << gain >> de 19 % demonte par les controles :
- porte-indice : le controle apparie est fait, et il TUE l'effet — l'indice reel tombe a 482 jetons contre 459 pour le temoin (et 315 contre 1 sur la fenetre qui 
- Passe du 13/10 13h44 : 37 vertes sur 39 — porte-echange-experts et porte-tableaux y sont vertes, et le rouge de porte-indice a change de cause (il ne dit plus <
- Fenetre d'attention : la loi moyennee — a N=4096, N/2 coute +0,9 % (etendue 1,0 pt) et N/4 +4,1 % (1,5 pt), alors qu'a N=2048 le quart allait de +2,8 a +49,2 % 
- Journal du 13/10 : la passe a 37/39, la loi moyennee de la fenetre, et deux pieges mesures (--attn-sinks 0 qui n'est pas neutre, et mon propre pkill)" && git lo
- Fenetre : cinq textes a N=4096 au lieu de trois — la moitie des cles coute jusqu'a +3,0 % (pas <=2,1 %), le quart +3,2 a +9,3 % ; je corrige ma propre conclusio
- Un etat precoce predit un etat profond a R2 0,65 (identite 0,19) — mais les pas elementaires sont MIEUX predits (0,78 et 0,75), donc ~35 % de la variance profon

