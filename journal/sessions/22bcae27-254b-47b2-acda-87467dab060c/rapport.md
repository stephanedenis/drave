# Session 22bcae27 — Étude de Qtrinet-bootstrap.md

| | |
|---|---|
| Identifiant | `22bcae27-254b-47b2-acda-87467dab060c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-25 11:56 |
| Durée | 52.2 h |
| Tours | 35 |
| Messages | 801 |
| Appels d'outils | 822 |
| Fichiers touchés | 65 |
| Commandes | 597 |
| Sous-agents | 1 |
| Commits | 26 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — Implémenter l'inférence complète de Qwen2.5-0.5B dans qtrinet-core (Rust std seul) : forward Qwen2 (RMSNorm, RoPE, GQA + cache KV, MLP SwiGLU, lm_head), tokenizer BPE byte-level qwen2, génération autoregressive et échantillonnage ; valider l'égalité token à token contre la référence numpy (src/trans
… [89 caractères tronqués]
- **complete** — Implémenter l'inférence complète de Qwen2.5-0.5B dans qtrinet-core (Rust std seul) : forward Qwen2 (RMSNorm, RoPE, GQA + cache KV, MLP SwiGLU, lm_head), tokenizer BPE byte-level qwen2, génération autoregressive et échantillonnage ; valider l'égalité token à token contre la référence numpy (src/trans
… [89 caractères tronqués]
- **create** — Mener la campagne d'expériences sur l'exécution événementielle du modèle préentraîné Qwen2.5-0.5B : (1) imposer une parcimonie d'activation à l'inférence (seuil et k-WTA) sans aucun entraînement et mesurer la frontière (parcimonie, perplexité, événements/token) ; (2) rendre l'attention exprimable en
… [267 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — Étudie Qtrinet-bootstrap.md

**Tour 2** — le nvlink est bien présent entre les 2 cartes rtx. Consulte et enrichit /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/ au besoin pour consolider les connaissances et outils pour la carte. Une seconde carte peut être ajoutée pour tester la distribution de charge localement, dautres peuvent s'ajouter à l'externe au besoin.

**Tour 3** — nouveau cable branché

**Tour 4** — assure-toi que le bon logiciel est installé car on a changé les hdd de machine depuis leur installation (les fichiers d'installation sont encore dans mon home)

**Tour 5** — comment aller chercher la licence, j'ai oublié

**Tour 6** — quel type :  Choose a row         Web Description Maintainance Expiration License Expiration  Quartus® Prime Software 90-Day Evaluation (Standard and Pro Editions) (License: EVALUATION-LIC) 2026-12-25 2026-12-24  Agilex™ 5 E-Series FPGA Software Enablement (License: SW-AGILEX-5E) 2027-09-25 2027-09-25  Agilex™ 3 C-Series FPGA Software Enablement (License: SW-AGILEX-3) 2027-09-25 2027-09-25  Questa … [1670 caractères tronqués]

**Tour 7** — downloads LR-193822_License.dat

**Tour 8** — commencons par quantifier en trinaire/multi un petit modèle minimal pour tester le principe

**Tour 9** — un modèle quantifié peut-il être élagué en matrice assez creuse pour prendre une approche par événement?

**Tour 10** — en fonctionnant par événement on peut multiplier le nombre de noeuds pour émuler plus de précision

**Tour 11** — l'activation doit être mesurée à la volée et construire la liste d'activation en cascade. Est-ce pensable sur en mode  cpu

**Tour 12** — les listes d'activations doivent être triés et dédupliqués avant d'être appliquées

**Tour 13** — peut-on optimiser le modèle à la conversion afin de faire des grappes afférentes et efferentes naturelles et diviser en plusieurs sous-modèles connectés?

**Tour 14** — go

**Tour 15** — un modèle populaire efficacement quantifié est sur combien de bits? Peut-on émuler les valeurs quantifiées en répétant l'adresse d'activation autant de fois que sa valeur ? C'est à dire que si on est en adressage relatif, on aura une suite de zéros correspondant à la valeur quantifié du modèle d'origine, sans aucune pertes de qualité.

**Tour 16** — essaie sur 8 bits pour vois si on peut avoir une perfection

**Tour 17** — le but n'est pas de compresser le modèle 8bit, mais simplement de le faire opérer en mode listes (où les deltas d'adresses peuvent avoir jusqu'à 127 répétion de zéros) ce qui nous affranchit des gpus

**Tour 18** — Comme on est sur des listes d'événements en cascade, on aura un débit variable en fonction des activations. As-tu des tests standards légers pour éprouver notre implémentation et mesurer sa qualité et performance sur cpu avec des modèles qui auraient été impensables en architecture llm traditionelle?

**Tour 19** — 40 cores au repos...

**Tour 20** — les cores cpu semblent au repos...

**Tour 21** — go pour rust, on pourra optimiser les listes!

**Tour 22** — oui

**Tour 23** — fais les 4 optimisations

**Tour 24** — peut-on dire que ça permet de faire fonctionner des modèles 4 bits sur cpu efficacement?

**Tour 25** — fpga maintenant

**Tour 26** — lecteur ddr3 (listes de connexions, trains d'événements, listes d'activations)

**Tour 27** — est-ce qu'on traite les couches de neurones séparément dans notre architecture?

**Tour 28** — aurait-on des gains en modèle hybride fpga + cpus + gpus en exploitant les points forts de chaque ressource pour des tâches optimales si la communication n'est pas une entrave significative (listes d'événements aidant)

**Tour 29** — continue

**Tour 30** — bilan complet de nos implantations multi hardwate?

**Tour 31** — peut-on avoir un stream de listes d'Activation post traitement (traité sur une autre coeur et autre ressource)qui permettrait d'apprendre de ces log d'activité (principe de hebb pour créer de nouveau noeuds)?

**Tour 32** — on doit donc journaliser en vue d'une version ultérieure du modèle et le construire/entrainer en parallèle avec les ressources inutilisées et comparer les résultats. l'idée est d'apprendre avec moins de couches de neuronnes, faires des grappes de différentes architectures selon l'expertise ou même passer en mode récursif certaines portions. on a donc des flux de données d'activation qui nous perme … [423 caractères tronqués]

**Tour 33** — automatise l'enregistrement de toutes nos sessions dsh pour ce projet car les traces sont importantes. ensuite crée un document de vision de programme de recherche afin d'avoir un roadmap clair vers un agi pouvant fonctionner localement et on enchaine avec la plomberie d'apprentissage.

**Tour 34** — /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal doit inclure un automatisme qui produit un .md pour chaque session avec tous les détails qui permettent de reconstituer l'essence de la session et démontrer le travail accompli, étape par étape. Continue ensuite avec le balayage systématique des appariements croisés.

**Tour 35** — attention pour ne pas se perdre à copier les autres et ne pas empiéter non plus sur mon autre programme de recherche https://github.com/stephanedenis/neuronspikes nous voulons ici continuer notre expérience avec des modèles préentrainés qui ont fait leur preuves et appliquer des techniques proche des SNN afin de les exécuter de façon radicalement différente. Nous évaluons les opportunités qui émer … [146 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Étudie Qtrinet-bootstrap.md

*37 appels d'outils.* Actions notables :

- glob
- bash — List working directory contents
- read
- web_search
- web_fetch
- ask_user_question

**Synthèse produite :**

⏵ Clôture de l'étude

Pas de souci — l'étude est livrée telle quelle. Le récapitulatif en trois lignes, si vous devez n'en retenir qu'un peu :

1. **La carte est identifiée et déjà bien outillée** (Storey Peak / Stratix V GS D5, 4 Go DDR3, 2 × QSFP+ 40G, 2 × PCIe Gen3 x8) : un design de référence, un driver Linux et une IP DMA à 6,5 Go/s existent publiquement et ne demandent qu'à être réutilisés.
2. **Le CSR + bit-slicing est une inversion architecturale** : ~17 bits/poids contre 2 bits en ternaire dense, sur un système dont le plafond est la DDR3 (9,66 Go/s mesurés). Le calcul ne pèse que ~4 % du FPGA ; le projet est un projet mémoire, pas un projet de PE.
3. **L'anneau 40 G est la seule brique non démontrée** de la plateforme (aucun exemple QSFP+ publié) et, de surcroît, il n'est pas le goulot (~0,1 % du temps de décodage). À 2 bits/poids, un 7B tient dans une seule carte : commencez par 4 répliques indépendantes, l'anneau viendra plus tard, si un modèle > 16 Go l'exige.

Le document reste une bonne vision d'ensemble ; ce sont ses chiffres et son ordre de priorité qui doivent être corrigés. Dites-moi quand vous voulez attaquer la version corrigée ou un livrable précis.

### Tour 2 — le nvlink est bien présent entre les 2 cartes rtx. Consulte et enrichit /home/stephane/Data13TB/stephane/GitHub/FPGA-Str … [211 caractères tronqués]

*65 appels d'outils.* Actions notables :

- bash — List top-level contents and sizes
- glob
- read
- bash — Count lines and show git history
- web_search
- bash — Check installed EDA tools, distro, GPU/NVLink status
- web_fetch
- bash — Inventory installed Quartus editions and versions
- bash — Test network access and inspect PCIe topology
- bash — Inspect FPGA card link status and host platform
- bash — Check Quartus device database and missing libraries
- bash — Read PCIe link state from sysfs
- bash — Check whether Quartus 23.1 Standard supports Stratix V
- bash — Compare device databases across Quartus installs
- … et 37 autres

**Synthèse produite :**

⏵ Bilan final de l'enrichissement du dépôt

\## Ce que le sudo a permis de trancher

**Vous aviez raison sur NVLink** — je l'ai vérifié à la source : `nvidia-smi nvlink -s` renvoie **25,781 Go/s sur Link 0 de chaque GPU**, et `nvidia-smi topo -m` confirme `GPU0 ↔ GPU1 : NV1`. J'avais tort, c'est corrigé et enregistré dans la doc (c'est même la liaison la plus rapide de la machine : 4× le PCIe ×16, 5× le QSFP+).

Puis, avec les droits root :

| Découverte | Détail |
|---|---|
| **2ᵉ carte possible en local** | **Slot2_CPU2 est libre** (×16 Gen3, NUMA 1) — exactement ce que vous envisagiez. Les 2 GPU sont sur CPU1/NUMA0, les FPGA sur CPU2/NUMA1. |
| **Carte** | `a1:00.0`, Microsoft `1414:b101`, **firmware d'usine**, Gen3 ×8, aucun driver, bits `CorrErr+`/`UnsupReq+` collants. Le port amont est ×16 : le ×8 vient de l'endpoint d'usine. |
| **Quartus ne démarrait pas du tout** | `libnsl.so.1` (glibc moderne) et `libgthread-2.0.so.0` (glib 2.88) manquants sur Tumbleweed. **Corrigé sans toucher au système** : extraction depuis Leap 15.6 dans `~/fpga-compat`. → `Quartus Prime Shell 21.1.1 Build 850 Standard Edition` démarre. |
| **La bonne édition** | Seul `~/intelFPGA/21.1` contient la famille `stratixv`. `altera_pro/26.1` = **Pro** (ne supporte pas Stratix V) et `intelFPGA_std/23.1` = **Lite** (non plus) — le README disait Pro 26.1, c'était bloquant. |
| **Licence** | `LR-171690_License.dat` existe mais est lié à `HOSTID=b8ca3a840e66`, alors que `Hauru` a `64006a551b97` / `64006a551b60`. Features anciennes (`quartus_red_black`, `6AF7_*`), expiration 2026.09 → **inutilisable ici**. |
| **USB** | Votre câble **est** détecté : le port `usb3-port13` est en état `default` (adressé mais non configuré) alors que tous les ports libres sont `not attached`. Le cycle d'alimentation du port n'a rien changé. Le noyau ne réessaie jamais après un `-71`. |

\## Dépôt enrichi — commit `a5bf139`

```
docs/carte-storey-peak.md   référence matérielle vérifiée (specs, horloges 644,53 MHz,
                            pins QSFP, IDCODE JTAG, pièges)
docs/toolchain.md           éditions Quartus, libs de compat, licence, chaîne JTAG
docs/multicartes.md         1→2→4 cartes : slots, voies, NUMA, ring 40G, data vs tensor
docs/journal-bringup.md     journal daté de tous les constats du jour
tools/host_check.sh         diagnostic complet hôte+carte en une commande
tools/quartus_env.sh        environnement Quartus 21.1 (à sourcer)
tools/setup_compat_libs.sh  rend Quartus exécutable (sans sudo)
… [1413 caractères tronqués]

### Tour 3 — nouveau cable branché

*19 appels d'outils.* Actions notables :

- job_output
- bash — Check USB state after new cable
- bash — Check JTAG tooling and free the FTDI from ftdi_sio
- bash — Install OpenOCD and scan the JTAG chain
- bash — Test OpenOCD without root and check Pro device support
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/jtag_scan.sh`
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/jtag_program_svf.sh`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/journal-bringup.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/toolchain.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/device/5SGSKF40I3LNAC.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/device/5SGSKF40I3LNAC.md`
- … et 5 autres

**Synthèse produite :**

⏵ Bilan du jalon JTAG

\## ✅ C'était le câble — et la chaîne JTAG est validée

Avec le nouveau câble, le FT232H s'énumère **sur le même port 13** :

```
Bus 003 Device 044: ID 0403:6014 FT232H Single HS USB-UART/FIFO IC
usb3-port13: state=configured
```

Et le scan JTAG répond :

```
Info : JTAG tap: auto0.tap tap/device found: 0x029070dd (mfg: 0x06e (Altera), part: 0x2907)
   TapName        Enabled  IdCode     Expected   IrLen
 0 auto0.tap         Y     0x029070dd 0x029070dd    10
```

**Trois bonnes surprises au passage :**

1. **Aucun root nécessaire** — OpenOCD détache lui-même `ftdi_sio` via libusb. Pas besoin de `modprobe -r`, pas de règle udev.
2. **Le driver JTAG maison pour Quartus n'est plus indispensable** : on peut programmer via un fichier **SVF**, ce qui évite `jtagd` et toute compilation de driver.
3. **`/dev/ttyUSB0` reste disponible** en parallèle → le port série du Nios est utilisable (devops.lol avait dû bricoler un UART sur les broches I2C d'un QSFP ; ici le FT232H le donne directement).

**Vérification faite aussi** : Pro 26.1 ne contient que `10nm` et `cyclone10gx` dans ses devices → confirmation que **Stratix V = Quartus Standard 21.1 uniquement**.

\## Commité (`81a3cd2`)

```
tools/jtag_scan.sh          scan de la chaîne JTAG (testé, sans root)
tools/jtag_program_svf.sh   programmation SRAM via SVF (à valider avec un bitstream)
docs/journal-bringup.md     §5 résolu (câble) + §5bis JTAG
docs/toolchain.md           §4 réécrit : OpenOCD-first, piège câble, mode SVF sans risque
device/5SGSKF40I3LNAC.md    étape 0 terminée
README.md                   état de la carte + prochaines étapes
```

Le journal note le réflexe à garder : `error -71` + port figé en `default` = **problème physique**, et comme le noyau ne réessaie jamais, le périphérique reste invisible dans `lsusb` — on croit à tort que rien n'est branché.

\## Il ne reste qu'un blocage : la licence

Tout le reste de la chaîne est prêt (Quartus démarre, JTAG répond, la carte est là en Gen3 ×8). Pour compiler, il faut un `.dat` pour le NIC **`64006a551b97`**. Le `LR-171690` trouvé dans `Downloads` est lié à `b8ca3a840e66` (une autre machine ?) et expire ce mois-ci.

Trois pistes, dans l'ordre :
1. **Redemander une licence** au centre de licences Altera pour ce NIC (voie *no-cost*).
2. Si `b8ca3a840e66` est une autre de vos machines, y déplacer ce fichier.
3. **Lancer l'interface graphique Quartus 21.1** : elle ouvre la boîte « License Setup Required » qui propose « *acquire no-cost li
… [613 caractères tronqués]

### Tour 4 — assure-toi que le bon logiciel est installé car on a changé les hdd de machine depuis leur installation (les fichiers d' … [39 caractères tronqués]

*51 appels d'outils.* Actions notables :

- bash — Locate Quartus installers in home directories
- bash — Verify Quartus 21.1 installation integrity
- bash — Verify Stratix V part data and 23.1 edition
- bash — Check for missing libraries and installer contents
- bash — Read install log and component inventory
- bash — Query Quartus for Stratix V device availability
- bash — List available Stratix V parts and installer components
- bash — Run Tcl part list query from file
- bash — List exact F40 package variants for the D5
- bash — Check whether the custom part exists in the device database
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/toolchain.md`
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k1.qsf.template`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k2.qsf.template`
- … et 32 autres

**Synthèse produite :**

⏵ Bilan : un seul point administratif bloque désormais les deux chaînes

\## Le flow de simulation est réparé — il s'arrête maintenant sur la licence

Côté technique, tout est vert : `vlog` et `vopt` compilent le RTL **sans aucune erreur**. Il ne reste que le *checkout* de licence :

```
\# ** License Issue: Invalid host. (/home/stephane/.altera.quartus/questa_lic.dat)
\# ** Error: Unable to checkout 'intelqsimstarter' license.
```

\### Le fin mot de l'histoire sur les deux séquelles du changement de disques

Votre ancien `.bashrc` (resté dans le miroir `Data13TB/stephane/`) contenait ces deux lignes qui manquent au nouveau :

```bash
export PATH="$PATH:$QUARTUS_ROOTDIR/bin:$HOME/altera_pro/26.1/questa_fse/bin"
export SALT_LICENSE_SERVER="$SALT_LICENSE_SERVER;/home/stephane/.altera.quartus/questa_lic.dat"
```

Le fichier de licence Questa (`intelqsimstarter`, valide jusqu'en **2027.01**) était donc resté dans l'ancien home, et la variable n'était plus définie → `Invalid license environment`. J'ai copié le fichier dans `~/.altera.quartus/` et remis l'export dans `tools/quartus_env.sh`.

**Mais le vrai obstacle est ailleurs** : les **deux** licences portent `HOSTID=b8ca3a840e66`, un MAC qui **n'existe sur aucune interface de cette machine** :

| | |
|---|---|
| NIC réels de cette tour | `64:00:6a:55:1b:60` (I217-LM), `64:00:6a:55:1b:97` (I210) |
| Adaptateurs USB / WiFi | **aucun** |
| MAC des licences | `b8:ca:3a:84:0e:66` — **absent** |

Ces licences ont donc été émises **pour un autre poste**. Le T3600 mentionné dans votre doc de device est le suspect le plus probable — d'où ma question : **`b8:ca:3a:84:0e:66`, est-ce le T3600 ?**

\### Vos options

1. **Si ce MAC est celui du T3600** → les deux licences y sont valides ; il suffit de lancer les outils là-bas (mais alors sans la carte, qui est dans le T7910...).
2. **Re-héberger les licences** sur le NIC de cette machine (`64006a551b60`) via le centre de licences Altera. C'est de toute façon nécessaire : la licence Quartus `LR-171690` **expire ce mois-ci (2026.09)**.
3. Si un **adaptateur Ethernet USB / dock** portant ce MAC existe dans vos affaires, le rebrancher suffirait — mais rien de tel n'est détecté actuellement.

\### État de la chaîne complète

| Maillon | État |
|---|---|
| Quartus Prime Standard 21.1.1 | ✅ installé, vérifié complet (1 344 parts Stratix V, 0 lib manquante) |
| QSF / device | ✅ corrigé (`5SGSMD5K1F40C1` — le part custom n'existe pas dans la base) |
| JTAG | ✅ validé, IDCODE `0x029070dd
… [481 caractères tronqués]

### Tour 5 — comment aller chercher la licence, j'ai oublié

*9 appels d'outils.* Actions notables :

- web_fetch
- web_search
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/install_license.sh`
- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/toolchain.md`
- bash — Test the license installer script
- bash — List all license features to determine coverage
- bash — Inspect license header and commit the guide
- bash — Confirm hostname and NIC history

**Synthèse produite :**

⏵ Réponse : la procédure exacte pour récupérer une licence

\## Votre licence est identifiée — et elle est morte

L'en-tête du fichier `LR-171690_License.dat` raconte toute l'histoire :

```
\# Issued 15 June 2026
\# Primary Machine Name-hauru              ← votre machine
\# Primary Machine ID-NIC ID B8CA3A840E66  ← un NIC qui n'existe plus
\# 1 Quartus® Prime Software 90-Day Evaluation (Standard and Pro Editions)
\# - License Expires 12-Sep-2026            ← expirée depuis 13 jours
```

C'était donc une **évaluation de 90 jours** couvrant Quartus Prime **Standard et Pro** + Questa. Deux problèmes : elle a **expiré le 12 septembre**, et son NIC (`B8CA3A840E66`) ne correspond plus aux NIC actuels de `Hauru` (`64006a551b60` / `64006a551b97`).

\## La procédure (Self Service Licensing Center)

**Adresse : <https://www.altera.com/SSLC>** — connexion avec votre compte Altera (celui du 15 juin ; un code de vérification arrive par courriel).

1. **Corriger le NIC ID.** Menu *Computers and License Files* → onglet *All Computers* → vous devez y retrouver la fiche `hauru` avec l'ancien NIC `B8CA3A840E66`. Remplacez le *Primary Computer ID* par **`64006a551b60`**.
   > 💡 **Astuce** : les changements de NIC ID sont **limités à 3** par période de maintenance. Comme l'ancienne fiche ne sert plus à rien, préférez **créer une nouvelle fiche** (bouton *New*) — par ex. `Hauru-2026`, *Computer Type* = NIC ID, *License Type* = **FIXED**, *Primary Computer ID* = `64006a551b60`. Il n'y a pas de fonction « supprimer », mais rien n'oblige à réutiliser l'ancienne.
2. **Demander la licence.** L'évaluation étant expirée, il faut soit une **nouvelle évaluation** (menu *Licenses* → cherchez l'option d'évaluation / *Evaluate*), soit une licence au titre de votre maintenance.
3. **Affecter** la licence à la nouvelle fiche : *Licenses* → *License Reports* → vue *New Licenses* → clic sur le nom `L-…` → crayon à droite de *Primary Computer* → sélectionner la fiche → *Save*.
4. **Générer** : bouton **Generate License** en haut à droite → vérifier que le bon NIC apparaît → **Generate**. Le `.dat` **arrive par courriel**.
5. **Installer** — j'ai préparé l'outil :

```bash
bash tools/install_license.sh ~/Downloads/LR-xxxxxx_License.dat
source tools/quartus_env.sh
```

Il vérifie le HOSTID avant de copier et place le fichier au bon endroit (`license.dat` pour Quartus, `questa_lic.dat` pour Questa). Testé : sur votre ancienne licence il refuse net avec le bon diagnostic.

\## Si le SSLC ne vous laisse p
… [1346 caractères tronqués]

### Tour 6 — quel type :  Choose a row         Web Description Maintainance Expiration License Expiration  Quartus® Prime Software 90 … [1950 caractères tronqués]

*2 appels d'outils.* Actions notables :

- edit `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/quartus_env.sh`
- bash — Update license env handling and document SSLC row choice

**Synthèse produite :**

⏵ Confirmation de l'outillage et récapitulatif des clics

L'outillage est prêt et testé (commit `f151184`) :

```
SALT_LICENSE_SERVER = ~/.altera.quartus/questa_lic.dat;~/.altera.quartus/license.dat
```

Les deux fichiers sont désormais consultés par Questa, et le garde-fou HOSTID continue de signaler les anciennes licences liées à `b8ca3a840e66` — il s'arrêtera de râler dès que les nouvelles seront en place.

\## Récapitulatif : ce que vous cliquez

1. SSLC → **Computers and License Files** → **New** : nom `Hauru-2026`, *Computer Type* = **NIC ID**, *License Type* = **FIXED**, *Primary Computer ID* = **`64006a551b60`** → *Save*.
2. SSLC → **Licenses** → **License Reports** → *New Licenses* → clic sur `EVALUATION-LIC` → crayon à côté de *Primary Computer* → sélectionner `Hauru-2026` → *Save* → **Generate License**.
3. Revenir dans *New Licenses* → même chose pour **`SW-QUESTA`** (Questa FPGA Starter Edition) → **Generate**.
4. Les deux `.dat` arrivent **par courriel** → les enregistrer dans `~/Downloads/`.
5. Me les faire installer (ou le faire vous-même) :

```bash
bash tools/install_license.sh ~/Downloads/<evaluation>.dat    # → license.dat
bash tools/install_license.sh ~/Downloads/<questa>.dat       # → questa_lic.dat (auto-détecté)
source tools/quartus_env.sh
```

Ensuite, dans l'ordre : `make sim2` (validation immédiate de la chaîne de simulation restaurée), puis `quartus_map` sur le Kernel 1 — le premier vrai test Stratix V, et enfin le bringup DDR3/DMA.

**Un seul point de vigilance** : l'évaluation est de **90 jours** (jusqu'au 24 décembre). Largement de quoi faire tout le bringup, mais si le projet doit tourner au-delà, il faudra une licence achetée — autant le savoir maintenant.

Dites-moi quand les fichiers sont téléchargés, je m'occupe de l'installation et je lance les vérifications.

### Tour 7 — downloads LR-193822_License.dat

*31 appels d'outils.* Actions notables :

- bash — Locate and inspect the new license file
- bash — Install license and run first Stratix V synthesis
- bash — Run full Quartus compile flow for Kernel 1
- bash — Test simulation with the new license
- bash — Set aside stale Questa license and check compile progress
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k2.qpf`
- bash — Create project files and check gitignore
- bash — Inspect tracked Questa artifacts and compile progress
- bash — Restore Questa log and update gitignore
- bash — Restore original log and check compile stages
- bash — Recover original log and check compile stages
- bash — Fix gitignore hygiene and check fitter progress
- job_output
- bash — Extract resource and timing reports
- … et 14 autres

**Synthèse produite :**

⏵ Bilan du jalon : licence OK, bitstream Stratix V produit

\## 🎉 La chaîne complète fonctionne — du RTL au bitstream

La licence `LR-193822` est valide (émise pour `Hauru2` / NIC `64006A551B60`, jusqu'au **24 décembre 2026**), et la première compilation complète pour Stratix V est passée :

```
Info (293000): Quartus Prime Full Compilation was successful. 0 errors, 6 warnings
Fitter Status : Successful
```

| Mesure | Kernel 1 (`v14_l2_distance`) |
|---|---|
| Device | `5SGSMD5K1F40C1` ✅ |
| **ALM** | **238 / 172 600** (< 1 %) |
| Registres | 131 |
| **DSP** | **13 / 1 590** |
| M20K | 0 / 2 014 |
| **Setup slack** | **−3,056 ns** → **fmax ≈ 124 MHz** (cible 200 MHz) |
| Hold slack | +0,147 ns ✅ |
| **Bitstream** | **`nipada_k1.sof` — 25 Mo, prêt à programmer** |

\### Trois bugs de flow trouvés et corrigés au passage

1. **Les `.qpf` manquaient** — sans eux, `quartus_sh --flow compile` refuse de démarrer. Les deux sont maintenant versionnés.
2. **2 205 avertissements → 6** : les délais d'E/S n'avaient pas de borne `-min`. Au passage je me suis trompé de syntaxe (`-min`/`-max` sont des *drapeaux*, pas des options à valeur) — l'erreur `Error (332000)` a été attrapée et corrigée, c'est la relance qui l'a validée.
3. `tb/qrun.log` était suivi par git alors que c'est un artefact de run → désuivi (le fichier reste sur disque).

\### Le vrai enseignement technique

**Le chemin critique ne tient pas 200 MHz** : −3,056 ns de slack ⇒ ~124 MHz. C'est le premier résultat de timing réel du projet, et le prochain chantier RTL (retiming/pipelining du Kernel 1), pas un problème d'outillage. En l'état, le kernel fonctionnerait à ~124 MHz au lieu des 200 MHz visés — soit 62 % de la performance espérée.

\## Deux choses à décider

**1. La licence Questa (bloquant pour `make sim`)** — il manque la feature `intelqsimstarter`, absente de l'évaluation Quartus. Il faut générer au SSLC la ligne **`SW-QUESTA` (Questa* - FPGA Starter Edition)**, sur la même fiche `Hauru2`. Puis :

```bash
bash tools/install_license.sh ~/Downloads/<questa>.dat   # → questa_lic.dat
```

**2. Programmer la carte** — `nipada_k1.sof` existe, mais **je ne le programmerais pas tel quel** : le kernel n'a aucune affectation de broches (548 pins placés au hasard par le fitter), et piloter des broches arbitraires sur une carte où passent PCIe, DDR3 et QSFP n'est pas prudent. Deux options propres :

- **Option sûre** : récupérer d'abord le design de référence (`bash tools/fetch_reference_design.sh`) pour disposer
… [590 caractères tronqués]

### Tour 8 — commencons par quantifier en trinaire/multi un petit modèle minimal pour tester le principe

*22 appels d'outils.* Actions notables :

- bash — Check Qtrinet repo and Python ML environment
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/ternary.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/tiny_model.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/roofline.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_quantify.py`
- bash — Run the ternary quantification experiment
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/tiny_model.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/ternary.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_quantify.py`
- bash — Re-run the quantification experiment after fixes
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_quantify.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_quantify.py`
- bash — Run the corrected quantification experiment
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/ternary.py`
- … et 8 autres

**Synthèse produite :**

⏵ Bilan du test de principe

\## Le principe est validé — et chiffré

Le MLP minimal est **réellement entraîné** (76,07 %, numpy pur, aucune dépendance ML) puis quantifié. Trois résultats qui décident de la suite.

\### 1. Le chemin entier est **exact** — le principe « aucun DSP » tient

| Mesure | Valeur |
|---|---|
| Écart entier vs flottant, couche 1 | **4,2e-07** |
| Écart entier vs flottant, couche 2 | **1,9e-06** |
| Accuracy chemin entier (poids ternaires + activations int8) | 49,22 % |
| Accuracy chemin flottant, mêmes poids quantifiés | 49,71 % |

L'écart, c'est de l'arrondi flottant, rien d'autre. Des additions/soustractions sur des poids ternaires reproduisent le calcul. Détail matériel confirmé au passage : **le biais s'ajoute à la remise à l'échelle**, hors du réseau de MAC — c'est ce qui évite d'élargir l'accumulateur (il tient largement en int32).

\### 2. Le ternaire a posteriori ne marche pas — mais ce n'est pas le ternaire qui est en cause

| Format | b/poids | Accuracy | Δ |
|---|---|---|---|
| float32 | 32 | 76,07 % | — |
| int8 | 8 | 76,27 % | +0,2 |
| int4 | 4 | 74,12 % | −2,0 |
| **ternaire 1,58 b** | **2** | **49,71 %** | **−26,4** |
| multi 2 plans | 4 | 73,44 % | −2,6 |
| multi 4 plans | 8 | 75,98 % | −0,1 |

**C'est le résultat le plus important** : quantifier un modèle float en ternaire après coup le détruit. Les modèles BitNet b1.58 fonctionnent parce qu'ils sont **entraînés** avec la contrainte — pas parce que le ternaire est magique. La question « le ternaire suffit-il ? » ne se tranche donc pas sur un modèle existant : il faut un entraînement ternaire (straight-through estimator).

Bonne nouvelle en revanche : le **découpage en plans dégrade très progressivement** — à 4 plans on est à −0,1 pt. C'est la voie pour réutiliser un modèle 4 bits sans réentraîner.

\### 3. Le CSR du cahier des charges, chiffré

| Encodage | Ternaire | 4 plans |
|---|---|---|
| dense (1 bit/plan) | **2,0 b/poids** | **4,0 b/poids** |
| bitmap + signe | — | 8,0 b/poids |
| **CSR par plan (le CDC)** | **10,1 b/poids** | **61,8 b/poids** |

**5 à 15× le trafic mémoire.** Mon audit le disait qualitativement ; c'est maintenant mesuré.

\### 4. Ce que ça donne sur la carte

| Modèle | Encodage | tok/s (1 carte) |
|---|---|---|
| 7B | ternaire dense 2 b | **5,5** |
| 7B | 4 bits | 2,8 |
| 7B | ternaire CSR | 0,6 |

Et le chiffre qui structure tout le reste : **312 voies de MAC suffisent** (≈ 9 400 ALM, **5 % du FPGA**) pour saturer les 9,66 Go/s de la DDR3 à 12
… [1461 caractères tronqués]

### Tour 9 — un modèle quantifié peut-il être élagué en matrice assez creuse pour prendre une approche par événement?

*10 appels d'outils.* Actions notables :

- web_search
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/sparsity.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_sparsity.py`
- bash — Run the sparsity and event-driven experiment
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_sparsity.py`
- bash — Regenerate sparsity report with caveats
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- bash — Commit the sparsity and event-driven analysis

**Synthèse produite :**

⏵ Réponse : oui, mais pas par CSR — et le seuil est chiffrable

\## Oui — et le seuil de rentabilité tient à un détail qu'on oublie

**Un poids ternaire non nul ne porte qu'un signe : 1 bit.** Toute l'information est dans le *fait* qu'il soit non nul, pas dans sa valeur. Donc l'encodage événementiel naturel n'est pas « indice + valeur » comme le CSR, c'est :

> **bitmap (1 bit/poids) + signe (1 bit par non-nul) = `1 + d` bits/poids**

où `d` est la densité. À comparer aux 2 bits du code dense : le bitmap n'est **jamais pire**, et il est égal à 2 bits seulement en densité 100 %.

\### Les seuils, calculés par le modèle de coût

| Comparaison | Égalité à | Gagnant en dessous |
|---|---|---|
| **bitmap vs dense** | **100 %** | **bitmap — toujours** |
| CSR 16 b vs dense | 11,8 % | CSR |
| CSR 32 b vs dense | **6,1 %** | CSR |
| CSR 32 b vs bitmap | 3,1 % | CSR |

➡️ **Le CSR n'est rentable que sous ~6 % de densité** (indice 32 bits) — soit >94 % de zéros. Or la littérature situe l'élagage *one-shot* des LLM à **50-60 %** (SparseGPT, Wanda), et la forme supportée par le matériel est le **2:4 structuré = 50 %**. Le régime où le CSR gagnerait est hors d'atteinte pour un modèle généraliste.

\### Ce que dit notre modèle (mesuré)

```
densité naturelle du ternaire     : 26,3 %   ← 73,7 % de zéros, sans aucun élagage
activations non nulles (ReLU)     : 52,8 %
événements réels (poids ∧ act.)   : 13,9 %
```

Le ternaire **est déjà creux par construction**. À cette densité, le bitmap donne **×1,58** de débit : un 7B passe de **5,5 → 8,7 tok/s** par carte. Le 2:4 structuré, lui, donne 1,50 b/poids → 7,4 tok/s.

\### Mais le vrai obstacle n'est pas le poids — c'est l'activation

Un événement n'existe que si le poids **et** l'activation sont non nuls (13,9 % ici). Or avec un flux creux, il faut *aller chercher* l'activation à un index arbitraire, alors qu'en dense elle est diffusée dans l'ordre (gratuit). Le coût :

- fenêtre de lecture de 64 activations + multiplexeur 64:1 ≈ **21 LUT par voie**
- 312 voies → **≈ 3 400 ALM, soit 2 % du FPGA** — payable
- plus un décodeur de bitmap + encodeur de priorité, et des **FIFO élastiques** (flux à débit variable)

C'est là que passe la complexité, pas dans le calcul.

\## Le compromis que je recommanderais

| Approche | b/poids | Gain | Complexité |
|---|---|---|---|
| Dense 2 bits | 2,00 | — | nulle (déjà validée) |
| **2:4 structuré** | **1,50** | ×1,33 | **faible** — positions implicites, 0 flux variable |
| 1:4 structuré | 1,25 | 
… [1575 caractères tronqués]

### Tour 10 — en fonctionnant par événement on peut multiplier le nombre de noeuds pour émuler plus de précision

*12 appels d'outils.* Actions notables :

- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/tiny_model.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_precision.py`
- bash — Run the sparsity-buys-precision experiment
- bash — Fix Pareto marking and re-run
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/encoding.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_encoding.py`
- bash — Run the signed-lists encoding experiment
- bash — Compute realistic-width encoding costs and crossover
- bash — Exact encoding cost measurement on realistic rows
- bash — Fix report with realistic-width measurement
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- bash — Commit the structural encoding analysis

**Synthèse produite :**

⏵ Synthèse : les trois idées convergent en une seule architecture

\## Oui — et c'est votre intuition la plus forte jusqu'ici

**Pourquoi ça marche** : avec des poids ±1, la valeur n'existe plus. Deux listes triées de destinations par source (les « + », les « − »), et l'appartenance à la liste *est* le signe. Il ne reste que de la **position** — la matrice devient un **graphe biparti signé**, et l'inférence devient une traversée de graphe. C'est l'« adressage relationnel » du cahier des charges, mais poussé jusqu'au bout : le CSR du CDC gardait encore un `data` de 2 bits. Vous venez de le supprimer.

**Ce qui rend l'idée payante**, c'est que les listes sont *triées* : on encode des **écarts**, pas des indices. Sans ça, un indice complet coûte plus cher que le bitmap qu'il remplace.

\### Mesure exacte (lignes de 4 096 poids)

| Densité | bitmap+signe | **listes signées** | gain | tok/s 7B | vs dense 2 b |
|---|---|---|---|---|---|
| 50 % | 1,500 | 1,838 | 0,82× | 6,0 | ×1,09 |
| 25 % | 1,250 | 1,306 | 0,96× | 8,5 | ×1,53 |
| **12,5 %** | 1,125 | **0,871** | **×1,29** | 12,7 | **×2,30** |
| **5 %** | 1,050 | **0,476** | **×2,21** | **23,2** | **×4,20** |
| 2 % | 1,020 | 0,251 | ×4,06 | 44,0 | ×7,96 |
| 1 % | 1,010 | 0,151 | ×6,71 | 73,3 | ×13,28 |

**Bascule vers 20 % de densité** : au-dessus le bitmap gagne (écarts trop courts), en dessous les listes gagnent et l'écart se creuse très vite.

\### Le croisement qui compte

En confrontant avec les mesures de précision (`run_precision.py`) :

| Architecture | b/poids | Accuracy | tok/s 7B |
|---|---|---|---|
| Ternaire **dense** (le CDC) | 2,00 | 49,7 % | 5,5 |
| Ternaire **creux 5 % + listes signées** | **0,476** | **59,1 %** | **23,2** |

**Plus précis ET 4,2× plus rapide.** Ce n'est pas un compromis, c'est un double gain — parce que le ternaire dense gaspille ses bits sur les zéros.

\### Ce que ça déplace

Le décodeur reste **LUT-only** (un accumulateur d'écarts + une FIFO, aucun DSP — la contrainte tient). En revanche la **collecte d'activation devient totalement irrégulière** : chaque événement vise un indice arbitraire. C'est là que passe toute la difficulté, exactement le point que j'avais identifié dans l'audit initial. Et il reste **un facteur 1,65** disponible : l'entropie des positions vaut 0,288 b/poids à 5 % contre 0,476 pour les listes.

\## L'architecture qui émerge des trois échanges

```
Poids ±1  →  deux listes signées triées  →  écarts  →  accumulateur LUT
             (plus aucune valeur stocké
… [1404 caractères tronqués]

### Tour 11 — l'activation doit être mesurée à la volée et construire la liste d'activation en cascade. Est-ce pensable sur en mode  c … [2 caractères tronqués]

*8 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_cpu.py`
- bash — Benchmark CPU bandwidth, scatter, and event-driven layer
- bash — Check compiler and memory configuration
- bash — Compile and run the C/OpenMP benchmark
- bash — Save benchmark and fix CPU projection
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- bash — Commit the AER/CPU feasibility study
- bash — Add AER section to README and amend commit

**Synthèse produite :**

⏵ Réponse : oui — et la mesure dit que c'est **la première chose à écrire**

\## Vous avez décrit l'AER, et ça résout le problème

Ce que vous proposez est exactement l'**Address Event Representation** du neuromorphique : au lieu de *tirer* l'activation à un indice arbitraire, on *pousse*. Chaque source active émet un événement, sa liste de destinations se lit **séquentiellement** (flux idéal depuis la DDR), et on disperse `acc[dest] += signe · x[src]`.

L'accès aléatoire ne disparaît pas, il **se déplace** : de l'entrée (l'activation, large et non bornée) vers la sortie (l'accumulateur). Et là, tout change : 4096 accumulateurs × 24 bits = **12 Kio**, ça tient dans les M20K. Le hasard devient *local*.

\## Mesuré sur le CPU (C/OpenMP, 16 threads)

| Test | 1 th | 8 th | **16 th** | 32 th |
|---|---|---|---|---|
| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |
| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |
| **Écarts + dispersion** | 0,87 | 4,55 | **7,79** | 6,79 |

Deux enseignements :
- **Le décodage par écarts est quasi gratuit** — le noyau complet va *plus vite* que la dispersion pure (le flux de deltas est séquentiel, il pipeline mieux que des indices aléatoires).
- La dispersion **sature vers 8 threads** : c'est l'accès aléatoire à l'accumulateur qui limite, pas la bande passante. Les accumulateurs par thread évitent toute contention.

\## La projection qui tranche

| Cible | ms/token | tok/s |
|---|---|---|
| CPU, borné bande passante (28,7 Go/s) | 14,5 | 68,9 |
| CPU, borné noyau (7,79 G év/s) | 44,9 | **22,3** |
| 1 carte FPGA | 43,1 | **23,2** |
| **4 cartes FPGA** (modèle réparti) | 10,8 | **92,8** |

**Une carte FPGA ≈ ce CPU** — par des chemins opposés : le CPU a 3× la bande passante mais bute sur sa cadence d'événements ; la carte a des voies à revendre mais bute sur sa DDR3 à 9,66 Go/s.

**Donc l'argument du FPGA n'est pas la carte, c'est l'agrégation** : 4 cartes = 4 mémoires indépendantes et 4 jeux de voies → 4× le débit, là où le CPU est plafonné par ses contrôleurs mémoire. C'est **exactement l'argument du ring** que vous portez depuis le début — mais il ne se justifie qu'à partir de 2-4 cartes.

\## Ce que ça implique concrètement

**Écrivez d'abord l'implémentation CPU.** Elle est immédiate — aucun bitstream, aucun DMA, aucun JTAG, aucune licence. Et elle apporte trois choses :

1. **Le modèle d'or** : la sémantique exacte des événements (quels non-nuls, dans quel ordre, quelles échelles) que le RTL devra reproduire bit 
… [1430 caractères tronqués]

### Tour 12 — les listes d'activations doivent être triés et dédupliqués avant d'être appliquées

*2 appels d'outils.* Actions notables :

- bash — Benchmark sorted+deduplicated accumulation vs scatter
- bash — Commit the sort/dedup analysis

**Synthèse produite :**

⏵ Réponse : l'exigence est juste, mais pas pour la raison de vitesse — voici ce que dit la mesure

\## Ce que la mesure contredit

| Variante | Cadence | Écritures |
|---|---|---|
| (a) Dispersion (1 écriture/événement) | 3,36 G év/s | 50 000 000 |
| **(b) Trié + replié (1 écriture/destination)** | **3,89 G év/s** (+16 %) | **4 111** |
| (c) Coût du tri (radix 2 passes) | 0,06 G év/s = **838 ms** | — |
| (rappel) Ordre naturel, écarts décodés | **7,79 G év/s** | — |

Le repliement divise les écritures par **12 000**… et ne gagne que **16 %**. Les écritures n'étaient donc pas le goulot : le coût est dans le **traitement par événement** (charger, comparer, brancher, additionner) et dans l'accès L1. Et le tri coûte **838 ms** là où l'accumulation en coûte 15 — environ **50× plus cher que ce qu'il rapporte**.

\## Mais votre exigence reste valable — sur le FPGA, pas sur le CPU

C'est le point important : **sur un CPU, la dispersion est gratuite** (le L1 a un store buffer, un forwarding, une détection de conflits — tout ça en silicium depuis 30 ans). **Sur le FPGA, cette dispersion est à construire** : pour faire `acc[dst] += v` avec plusieurs événements par cycle, il faut soit bancariser l'accumulateur avec hachage par destination, soit un réseau d'arbitrage. C'est exactement le mur que j'avais signalé.

Donc la mesure CPU ne se transpose pas : elle dit « ne triez pas **sur CPU** », elle ne dit pas « la dispersion est gratuite **dans le FPGA** ». Sur le FPGA, la propriété « une écriture par destination » vaut bien plus cher, parce qu'elle transforme un accès arbitraire en **balayage séquentiel** — et ça, c'est de la logique en moins, pas en plus.

\## Les trois formes correctes de votre exigence

1. **Ordre naturel d'abord** : l'ordre par source (listes de deltas) donne **7,79 G év/s**, le meilleur résultat mesuré — sans aucun tri. Le flux de poids reste séquentiel, les deux petits vecteurs (x : 4 Kio, acc : 12 Kio) tiennent en mémoire locale.

2. **Multi-plans : décaler, pas fusionner.** Pour le plan *b*, la contribution vaut `x[src] << b`. L'accumulation les somme **naturellement** — aucun dédoublonnage n'est nécessaire, un seul accumulateur suffit. C'est le cas où votre intuition semblait la plus nécessaire, et où elle se dissout.

3. **Compartiments par destination plutôt que tri** — pour les cas où le dédoublonnage est vraiment requis : fusion de sommes partielles venant de plusieurs cartes (le ring), ou déterminisme du résultat. Là, un **réseau de combinais
… [1234 caractères tronqués]

### Tour 13 — peut-on optimiser le modèle à la conversion afin de faire des grappes afférentes et efferentes naturelles et diviser en  … [33 caractères tronqués]

*8 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_clusters.py`
- bash — Run the clustering experiment
- bash — Fix budget comparison and ring traffic computation
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_clusters.py`
- bash — Fix syntax and re-run clustering experiment
- bash — Fix display bug, regenerate, and commit clustering results
- bash — Verify the clustering report content

**Synthèse produite :**

⏵ Réponse : oui — et la mesure dit que ça ne coûte rien

\## Le résultat, à budget égal

| | Non-nuls | Accuracy | Coût des positions |
|---|---|---|---|
| **4 grappes pures (0 % couplage)** | **346** | **74,12 %** | **0,39 b/poids** |
| Meilleur dense au même budget (32→7→10, 311 params) | 311 | **74,12 %** | — |
| Dense complet (sans structure) | 708 | 76,07 % | 0,79-1,31 b/poids |
| Ternaire dense (le CDC d'origine) | 2688 | 49,71 % | 2,00 b/poids |

**Imposer 4 grappes ne coûte exactement rien** : 74,12 % contre 74,12 % pour le meilleur modèle dense de même budget. On ne perd pas de précision, on change la *forme* du même budget.

\## La double dividende, chiffrée

Grouper les destinations **raccourcit les écarts** : 2,40 au lieu de 3,43 entre non-nuls consécutifs. Résultat direct sur l'encodage :

```
grappes pures   : 0,39 b/poids  →  74,12 % d'accuracy
motif aléatoire : 0,79-1,31     →  76,07 %
ternaire dense  : 2,00          →  49,71 %
```

**5× moins de bande passante que le ternaire dense, et 24 points d'accuracy en plus.** Les deux effets vont dans le même sens : moins de trafic *et* des positions moins chères.

\## Le ring n'est pas la raison (et je corrige mon calcul précédent)

Ce qui traverse le ring, ce sont les **activations** — les poids restent résidents. Mesuré : **0 à 55 µs/token** selon le couplage, face à **~45 ms** de calcul. Le ring n'est jamais le goulot. La valeur des grappes est dans le **coût d'encodage** et la **partitionnabilité**, pas dans le trafic réseau.

\## Le protocole est décisif

La structure doit être imposée **pendant l'entraînement** (masque fixe). Appliquée après coup, elle coûte cher : l'élagage en blocs perdait **11 points** à densité égale dans mon test précédent. Le modèle s'adapte à sa structure s'il est entraîné avec elle, il la subit sinon. **C'est ça, « optimiser le modèle à la conversion » : la grappe est une décision d'entraînement, pas une conséquence de l'élagage.**

\## Ce que ça fait converger

Vos quatre idées des derniers échanges s'emboîtent ici :

| Idée | Ce que les grappes lui apportent |
|---|---|
| Listes signées (valeur éliminée) | Écarts **2,40 au lieu de 3,43** → positions 2× moins chères |
| Listes d'activation triées/dédupliquées | Confinées à la grappe → **petites, naturellement ordonnées, aucun tri global** |
| Approche par événement | Les événements d'une grappe restent dans sa plage → collecte locale |
| Découpage en sous-modèles | La frontière de grappe **est** la frontière de carte → p
… [1683 caractères tronqués]

### Tour 14 — go

*9 appels d'outils.* Actions notables :

- bash — Check HuggingFace access and find small GGUF models
- bash — Download Qwen2.5-0.5B GGUF model
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/gguf_min.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_real_clusters.py`
- job_output
- bash — Run structural analysis on the real model
- bash — Fix GGUF bool parsing and re-run analysis
- bash — Fix circularity with cross-validation and random baseline
- bash — Add verdict to report and commit the real-model analysis

**Synthèse produite :**

⏵ Réponse : non — et c'est un résultat utile

\## Le verdict, rigoureusement établi

Grappes apprises par k-means sur les features de la dimension cachée de la **couche 0**, puis testées sur les couches 1-3 (validation croisée), avec une partition aléatoire comme référence :

| Grappes | Couche 0 (apprise) | Couches 1-3 (test) | Aléatoire | Test / aléatoire |
|---|---|---|---|---|
| G = 4 | 27,4 % | **27,5 %** | **27,5 %** | **1,00×** |
| G = 8 | 15,3 % | **15,2 %** | **15,1 %** | **1,00×** |

**Aucune information ne passe d'une couche à l'autre.** Il n'y a pas de grappes le long de la dimension cachée. Et le gain d'encodage par réordonnancement est de **1,00×** — cohérent : il n'y a rien à réordonner.

**Mon premier test était circulaire** (grappes apprises sur les matrices que je mesurais ensuite) et laissait croire à un effet de 1,56×. C'était l'effet mécanique du « max sur G parts » — une partition aléatoire le reproduit à l'identique. Corrigé avant de conclure.

\## Ce qu'un vrai modèle expose quand même

1. **Une hétérogénéité de magnitude massive** : dans `attn_output`, **95,9 %** des poids sont sous 5 % du maximum (73,8 % dans `ffn_gate`). C'est le phénomène des poids aberrants — le levier de l'**élagage avec calibration** (SparseGPT), pas de la clustérisation.
2. **Une structure explicite par têtes (GQA)** : 14 têtes de requête pour 2 têtes KV (groupement **7:1**), et l'énergie par tête va de **1,4 % à 28,5 %** (uniforme : 7,1 %) — un facteur **20** de spécialisation. Les têtes sont quasi orthogonales (similarité moyenne 0,020). **Ça, c'est une grappe naturelle — et elle est déjà là.**

\## La conséquence pour l'architecture

Le découpage en sous-modèles **ne peut pas révéler une structure qui n'existe pas : il doit l'imposer à l'entraînement.** Et c'est une bonne nouvelle, parce que l'essai précédent a montré que l'imposer :

- **ne coûte rien** : 74,12 % contre 74,12 % pour le meilleur dense à budget égal ;
- **divise le coût des positions par deux** : 0,39 contre 0,79-1,31 b/poids.

Autrement dit : la grappe est un **choix de conception**, pas une propriété à découvrir. Le pipeline se fige donc :

```
1. PLAN DE GRAPPES     imposé (pas révélé) — les têtes GQA sont un point d'appui gratuit
2. ENTRAÎNEMENT        ternaire + masque de grappes + élagage calibré (outliers)
3. ENCODAGE            listes signées par grappe, écarts courts → 0,39 b/poids
4. AFFECTATION         une grappe = une carte, poids résidents, ring pour les frontières
```

\## Pourqu
… [1055 caractères tronqués]

### Tour 15 — un modèle populaire efficacement quantifié est sur combien de bits? Peut-on émuler les valeurs quantifiées en répétant l … [216 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — List available quantizations
- bash — Fix Q4_0 nibble layout and add raw level extraction
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_value_encoding.py`
- bash — Download Q4_0 and run the unary encoding analysis
- bash — Separate quantization types and include address costs
- bash — Add hybrid encoding and re-run
- bash — Commit the unary encoding analysis
- bash — Rewrite contradictory verdict and commit
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_value_encoding.py`
- bash — Regenerate consistent report and commit

**Synthèse produite :**

⏵ Réponse aux deux questions

\## 1. Sur combien de bits sont les modèles populaires ?

| Niveau | Format type | Bits/poids réels | Usage |
|---|---|---|---|
| **4 bits** | **Q4_K_M**, Q4_0, AWQ, GPTQ | **~4,5-4,8** | **le standard de fait** |
| 5-6 bits | Q5_K_M, Q6_K | ~5,7-6,6 | quand la qualité prime |
| 8 bits | Q8_0 | ~8,5 | référence quasi sans perte |
| 2-3 bits | Q2_K, Q3_K, IQ3 | ~2,6-3,4 | compression extrême, avec perte |
| 1,58 bit | BitNet b1.58 | 1,58 | **modèles entraînés** en ternaire |

Le consensus post-entraînement est à **4 bits**. Descendre plus bas sans perte exige d'entraîner avec la contrainte.

\## 2. Votre idée — et elle gagne

**Mon premier verdict était faux, deux fois** : j'avais (a) mélangé des tenseurs Q8_0 dans la moyenne (`E[|v|] = 15,57` — impossible puisque |v| ≤ 8), et (b) supposé une distribution uniforme des valeurs (`E[|v|] ≈ 7,5`). Corrigé, voici la mesure sur Qwen2.5-0.5B Q4_0 :

```
Q4_0 : 344 M poids, densité 87,1 %,  E[|v|] = 3,02   E[popcount] = 1,39
       27,2 % des non-nuls valent ±1, 22,4 % ±2, 17,0 % ±3…
```

**Pourquoi `E[|v|] = 3,02` et non 7,5** : l'échelle Q4_0 est fixée par le **maximum du bloc**, donc la grande majorité des poids tombent sur les petits niveaux. **Le code 4 bits gaspille ses bits** — il paie 4 bits pour une valeur qui vaut presque toujours 1, 2 ou 3.

\### Le coût complet (adresses incluses)

| Stratégie | bits/poids | opérations/poids |
|---|---|---|
| dense positionnel (4 bits) | 4,00 | 0,87 |
| creux positionnel (4 b + adresse) | 4,36 | 0,87 |
| **creux unaire (votre idée)** | **2,63** | 2,63 |
| creux plans (popcount) | 2,08 | 1,21 |
| **creux HYBRIDE** | **1,85** | **0,98** |

**Votre idée bat le code dense : 2,63 contre 4,00 b/poids**, sans aucune perte de qualité. Et sa forme hybride — que vos chiffres suggèrent — fait mieux encore : **1,85 b/poids, soit ×2,17**, avec **0,98 opération par poids contre 0,87** en dense. Quasi gratuit en calcul aussi.

L'hybride, c'est votre principe poussé à sa conclusion :
- **|v| = 1 → unaire, donc gratuit** : l'adresse *seule* porte la valeur (c'est exactement l'encodage « listes signées » déjà mesuré à 0,39 b/poids)
- **|v| ≥ 2 → plans binaires** : `popcount(v)` au lieu de `v`, donc on passe de l'unaire au positionnel *pour les opérations* au lieu du stockage

Le seuil analytique reste vrai sur une distribution uniforme (l'unaire perd à partir de 4 bits), mais **les distributions réelles sont concentrées sur les petites valeurs** — et là votre i
… [1412 caractères tronqués]

### Tour 16 — essaie sur 8 bits pour vois si on peut avoir une perfection

*6 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_8bit_perfection.py`
- bash — Analyze 8-bit model entropy and lossless limits
- bash — Vectorize the 8-bit analysis and run
- bash — Fix leftover histogram reference and run
- bash — Compare level entropy between 4-bit and 8-bit models
- bash — Verify Kraft violation, add correction, commit

**Synthèse produite :**

⏵ Réponse : à 8 bits, la perfection est **déjà là** — il n'y a rien à récupérer

\## Mesure sur Q8_0 (494 M poids, 169 matrices)

| | Valeur |
|---|---|
| Niveaux distincts utilisés | **255 / 256** |
| Niveaux les plus fréquents | `+127` (1,6 %), `−127` (1,6 %), puis ~0,8 % par niveau |
| Densité | 99,2 % |
| **Entropie des niveaux** | **7,648 b/poids** |
| **Huffman réel** | **7,671 b/poids** |
| **Gain maximal sans perte** | **×1,046** |

Et à 4 bits, même verdict : entropie **3,731** contre 4 bits fixes → **×1,07**.

**La raison est structurelle** : un quantificateur bien réglé répartit ses poids sur **tous** ses niveaux. Cette quasi-uniformité *est* ce qui maximise l'entropie — autrement dit, **les bits sont déjà bien dépensés**. On ne compresse pas la sortie d'un bon quantificateur. La « perfection » à 8 bits n'est pas à conquérir : elle est le point de départ.

Détail révélateur : les deux niveaux les plus fréquents sont **±127**, soit la saturation. Le quantificateur écrête les poids aberrants — encore une fois, il fait son travail.

\## Je dois retracter mon ×2,17

Mon modèle de coût omettait deux choses :

1. **Le coût de désambiguïsation** — « quel plan ? où s'arrêtent les répétitions ? ». La preuve est nette : un code de longueur `v−1` pour `v ∈ 1..8` viole l'**inégalité de Kraft** :

```
E[|v|] = 3,022  →  code unaire annoncé = 2,022 bits
entropie de la distribution          = 2,682 bits
Σ 2^(−l)                             = 1,992  > 1   →  CODE INVALIDE
```

Un code dont la longueur moyenne passe **sous l'entropie** ne peut pas être décodable. Il manquait un marqueur.

2. **Le signe** — gratuit uniquement dans l'encodage à deux listes signées, pas ailleurs.

Correctement chiffré, l'encodage structurel retombe à **~3,5-4,4 b/poids**, soit **pas mieux que le code 4 bits fixe**. Le vrai plancher est l'entropie : 3,731 b/poids à 4 bits, 7,648 à 8 bits.

\## Ce qui survit — et c'est le vrai enseignement

| Situation | Entropie | Gain structurel possible |
|---|---|---|
| 8 bits, quantifié a posteriori | 7,65 / 8 | **×1,05 — rien** |
| 4 bits, quantifié a posteriori | 3,73 / 4 | **×1,07 — rien** |
| Ternaire **entraîné** | log₂3 = 1,58 | le signe devient gratuit |
| Grappes **imposées** | dépend du motif | ÷2 sur les positions |

**Le plafond est toujours l'entropie.** Sur un modèle quantifié après coup, la source est déjà quasi i.i.d. et presque uniforme : il n'y a pas de structure à exploiter. Les gains n'existent que quand la structure est **appris
… [1240 caractères tronqués]

### Tour 17 — le but n'est pas de compresser le modèle 8bit, mais simplement de le faire opérer en mode listes (où les deltas d'adress … [79 caractères tronqués]

*2 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_list_mode.py`
- bash — Run the list-mode execution analysis

**Synthèse produite :**

⏵ Réponse : oui, mais **pas sous forme unaire** — et l'idée débloque quelque chose d'important

\## Les chiffres sur le vrai Q8_0 (494 M poids)

| Mode | additions/poids | bits de flux/poids | ALM/voie | Voies pour saturer la DDR3 |
|---|---|---|---|---|
| multiplieur (référence GPU) | 0,99 | 8,00 | ~200 (DSP) | — |
| **décalage-addition** | **3,10** | **8,00** | **~31** | **242** |
| **unaire (suites de zéros)** | **42,45** | **42,45** | ~267 | **3 307** |

**Le mode unaire coûte 13,7× plus d'opérations *et* de flux, pour exactement le même résultat.** Et il ne rentre pas dans le FPGA : 3 307 voies × 267 ALM = **883 000 ALM, soit 5× tout le device**.

Projection sur 7 G poids :

| Support | 8 bits positionnel | unaire |
|---|---|---|
| 1 carte FPGA | 1,4 tok/s | 0,26 tok/s |
| 4 cartes | 5,5 tok/s | 1,04 tok/s |
| CPU | 4,1 tok/s | 0,77 tok/s |

Des suites de 127 zéros = 127 cycles par poids. Le débit s'effondre.

\## Mais votre intuition débloque quelque chose de plus important

**La bonne forme, c'est le décalage-addition** : la valeur reste positionnelle (8 bits groupés), et la multiplication par `v` se fait par **une addition décalée par bit à 1** — soit `popcount(v) = 3,13` additions par poids. **Aucun multiplieur. Aucun cœur tensoriel. Aucun GPU.**

Et voici le point qui change le projet :

> **La contrainte « aucun DSP » du cahier des charges n'exige pas des poids ternaires.**

Le décalage-addition fonctionne pour **n'importe quelle largeur entière**. On peut donc exécuter un modèle **8 bits ou 4 bits déjà quantifié**, sans réentraînement, sans DSP, sans GPU. Le CDC s'imposait le ternaire pour éviter les multiplieurs — c'était une contrainte inutilement forte.

Vérification matérielle : ~31 ALM par voie (accumulateur 24 bits + décalage + séquenceur), **242 voies pour saturer la DDR3** → 7 500 ALM, **4 % du FPGA**. Ça tient largement.

\## Ce que ça donne, honnêtement

| Modèle 7B | 1 carte | 4 cartes | CPU |
|---|---|---|---|
| **8 bits** (sans réentraînement) | 1,4 tok/s | 5,5 tok/s | 4,1 tok/s |
| **4 bits** | 2,8 tok/s | 11 tok/s | 8 tok/s |
| **ternaire + grappes** (0,39 b/poids) | 23 tok/s | 92 tok/s | 22 tok/s |

Le mode listes rend le 8 bits **exécutable** sans GPU — mais pas **rapide** : il reste borné par la mémoire. L'avantage du FPGA reste dans le régime bas bits.

\## Et le lien avec tout le reste

Le modèle ternaire est exactement le **mode unaire pris à sa limite** : tous les non-nuls valent ±1, donc `|v| = 1` → **une seule addition, aucu
… [801 caractères tronqués]

### Tour 18 — Comme on est sur des listes d'événements en cascade, on aura un débit variable en fonction des activations. As-tu des te … [181 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Inspect model architecture details
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/bpe_np.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/transformer_np.py`
- bash — Test GGUF metadata and BPE tokenizer
- bash — Fix tokenizer regex and test round-trip
- bash — Test the Qwen2 numpy forward pass
- bash — Profile the forward pass sections
- bash — Test matmul layouts and batching

**Synthèse produite :**

⏵ Trouvé : la projection finale (896→152k) coûte 620 ms à elle seule. C'est un problème de disposition mémoire

### Tour 19 — 40 cores au repos...

*24 appels d'outils.* Actions notables :

- bash — Diagnose BLAS threading configuration
- bash — Identify the BLAS library in use and alternatives
- bash — Test LD_PRELOAD OpenBLAS speedup
- bash — Test forward speed with OpenBLAS and download WikiText-2
- bash — Fix dataset download and test thread counts
- bash — Profile individual forward operations
- bash — Instrument the actual forward loop
- bash — Diagnose memory bandwidth and NUMA effects
- bash — Test NUMA binding and thread effects on forward
- bash — Compare isolated vs in-loop performance in one process
- bash — Measure CPU time vs wall time in the forward
- bash — Bisect the forward to localize the slowness
- bash — Check for denormal values in activations
- bash — Test the denormal hypothesis in silu and softmax
- … et 10 autres

**Synthèse produite :**

⏵ Réponse : les tests standards sont en place, et la mesure contredit une prémisse

\## 1. Les tests standards légers — implémentés

**Qualité** (le moins cher en premier) :

| Test | Coût | Notre état |
|---|---|---|
| **Perplexité WikiText-2** | 358 ko de texte | ✅ **implémenté : PPL = 20,29** |
| LAMBADA, PIQA, ARC-easy, HellaSwag, WinoGrande | quelques milliers de QCM | à ajouter (protocole BitNet b1.58) |
| TinyStories | très petits modèles | optionnel |

La PPL de **20,29** sur 4088 tokens tombe exactement dans la fourchette attendue d'un Qwen2.5-0.5B (15-25) : **mon implémentation numpy est validée** — sans torch, sans transformers, sans aucun paquet ML.

**Performance** :

| Métrique | Protocole standard | Notre spécifique |
|---|---|---|
| Débit prompt / génération | `llama-bench` pp512 / tg128 | — |
| **Latence** | TTFT, ITL en p50/p95/p99 | **distribution du nombre d'événements/token** |
| Bande passante | Go/s vs optimum borné mémoire | événements/s vs maximum théorique |

\## 2. La mesure qui contredit la prémisse

Vous supposiez un débit variable selon les activations. Voici ce que dit le vrai modèle :

```
activations exactement nulles : 0,00 %   (entrée MLP comme sortie de SiLU)
événements par token          : 354,88 M
écart-type / moyenne          : 0,0 %
max / min                     : 1,00
densité des poids (Q8_0)      : 100 %
```

**Le débit est parfaitement constant.** Pourquoi : SiLU et softmax sont des fonctions lisses — aucune activation ne tombe *exactement* à zéro. La cascade émet donc toujours le même nombre d'événements. La variance ne peut venir que des poids, et un modèle quantifié n'a pas de poids nuls.

C'est une **bonne nouvelle pour l'ingénierie** (un débit constant est bien plus simple à dimensionner) mais cela déplace la question : **le débit variable doit être produit, pas espéré.**

\## 3. D'où viennent alors les modèles « impensables en dense » ?

Ce sont exactement ceux qui **produisent** la parcimonie d'activation :

| Modèle | Pourquoi le dense ne peut pas | Ce que ça donne |
|---|---|---|
| **Ultra-creux à l'échelle** (1 % de densité) | 99 % des FLOPs gaspillés | débit ×100 |
| **Couches massivement larges** (10¹² entrées) | le tenseur dense n'existe pas | représentable seulement en listes |
| **Graphe structuré** — votre graphe NIPADA (1753 nœuds, 20 k arêtes) | les cœurs tensoriels exigent des formes régulières | le calcul **est** un parcours de graphe |
| **Routage conditionnel** (MoE extrême) | chaque token activ
… [2216 caractères tronqués]

### Tour 20 — les cores cpu semblent au repos...

*11 appels d'outils.* Actions notables :

- bash — Check swap, cgroup limits and disk type
- bash — Monitor process memory and page faults during forward
- bash — Isolate matmuls from the rest of the forward
- bash — Compare matmuls alone vs full forward
- bash — Test whether fresh arrays cause the slowdown
- bash — Bisect operations inside the combined loop
- bash — Check dtype and shape evolution in the loop
- bash — Bisect where float64 appears
- bash — Fix the float64 promotion and measure the speedup
- bash — Re-run the harness with the fix
- bash — Commit the float64 promotion fix

**Synthèse produite :**

⏵ Résolu — et c'est votre observation qui a mis sur la piste

\## « Les cores au repos » était exactement le symptôme

Le processeur **ne calculait pas, il convertissait**. Voici la chaîne :

```python
sc = np.einsum(...) / np.sqrt(self.head_dim)
                       └── np.sqrt(64) renvoie un np.float64
```

En numpy 2 (règle NEP 50), un `float` Python est un **scalaire faible** — il ne change pas le dtype du tableau. Mais un **scalaire numpy** (`np.float64`) est **fort** : il promeut tout.

```
sc / sqrt(64)  →  float64
   → masque + scores : float64
   → softmax : float64  →  einsum sortie : float64
   → h : float64   (le tenseur caché entier)
```

Résultat : le tenseur caché dérive en float64, et **chaque matmul doit reconvertir à la volée les 17 Mo de poids float32 → float64**, en calculant à demi-largeur SIMD. Soit ≈ 2 Go de conversion par forward.

\### Ce que ça expliquait — tout, d'un coup

| Symptôme observé | Explication |
|---|---|
| Coût **constant** par appel (3,9 s pour 5 tokens, 5,7 s pour 128) | la conversion porte sur les **poids** (taille fixe), pas sur les tokens |
| **4 cœurs sur 40** occupés | la conversion est une passe mémoire, pas du calcul parallèle |
| 0,6 Go/s effectifs au lieu de 18 | aller-retour float32↔float64 |
| Les mêmes matmuls **isolés** 20-40× plus rapides | dans mes tests, l'entrée était déjà float32 pure |
| Retirer n'importe quelle opération ne changeait rien | le coupable était la **promotion**, pas une opération |

\## Le correctif et son effet

```python
sc = np.einsum("thd,shd->hts", q, k) * (1.0 / math.sqrt(self.head_dim))
                                       └── float Python = scalaire faible
```

| | Avant | Après |
|---|---|---|
| Forward 5 tokens | 4 038 ms | **132 ms** (×30) |
| Forward 128 tokens | 5 655 ms | 1 000 ms |
| Génération | 0,2 tok/s | **5,5 tok/s** (×27) |
| Harnais | 34 ms/token | **11,6 ms/token** |

Et j'ai ajouté un **garde-fou** : le forward lève une `TypeError` si le tenseur caché n'est plus en float32. Plus aucune promotion silencieuse ne passera.

\## Les résultats du harnais (avec le correctif)

```
Perplexité WikiText-2 : 24,77 (fenêtres 256) — 20,29 en fenêtres 512
Événements/token      : 354,88 M — variance 0,0 %, max/min = 1,00
Activations nulles    : 0,00 %
```

La perplexité valide l'implémentation numpy complète (lecteur GGUF + tokenizer BPE + forward Qwen2, aucun paquet ML). Et la conclusion de fond tient : **le débit est parfaitement constant** sur un transformer standard — l
… [934 caractères tronqués]

### Tour 21 — go pour rust, on pourra optimiser les listes!

*11 appels d'outils.* Actions notables :

- bash — Check Rust toolchain availability
- bash — Create the Rust crate manifest
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/gguf.rs`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/list.rs`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- bash — Build the Rust crate
- bash — Fix format string and rebuild
- bash — Run the Rust engine on the real model
- bash — Show the event engine benchmark results
- bash — Write crate README and commit

**Synthèse produite :**

⏵ Moteur Rust livré et mesuré sur le vrai modèle

\## Ça tourne — et le débit variable est enfin là

```
GGUF ouvert en 223 ms — 290 tenseurs
architecture : qwen2 · 24 couches · hidden 896 · intermédiaire 4864
```

\### 1. Le moteur d'événements (Qwen2.5-0.5B, 16 threads)

| Densité activations | Sources actives | Événements | G év/s | ms/appel |
|---|---|---|---|---|
| 0 % | 0 | 0 | — | 0,484 |
| 5 % | 245 | 217 851 | 0,59 | **0,370** |
| 25 % | 1 217 | 1 082 120 | 2,16 | 0,501 |
| 50 % | 2 433 | 2 163 317 | 3,40 | 0,636 |
| 100 % | 4 864 | 4 325 087 | **4,66** | 0,928 |

**Deux choses importantes ici :**

- **Le débit varie réellement avec les activations** (0,37 → 0,93 ms, soit ×2,5) — c'est exactement ce que la cascade permet et qu'un moteur dense ne sait pas faire.
- **Contrôle `listes vs dense` : IDENTIQUE ✅** — le moteur est exact, pas approximatif.

Et un chiffre à corriger tout de suite : **0,484 ms même à densité nulle**. C'est le coût fixe du lancement des threads et de la réduction. C'est le premier poste à optimiser (pool persistant) — il écrase tout en dessous de 10 % de densité.

\### 2. Les tailles d'encodage, mesurées sur les vraies matrices

| Encodage | b/poids | Perte ? |
|---|---|---|
| dense 8 bits | 8,000 | non (référence) |
| **bitmap + signe** | **1,992** | oui (ternarise) |
| creux k=4 | 4,970 | oui |
| creux k=8 | 8,939 | **non** |
| listes signées + écarts | 7,975 | non |

Verdict sans ambiguïté : **sur une matrice dense, aucun encodage ne bat le dense 8 bits**. Le bitmap+signe à 1,99 b/poids est spectaculaire… mais il jette la magnitude. Et les listes signées coûtent 7,98 b/poids parce que l'écart moyen vaut 1,0 — un varint par poids.

C'est la **confirmation indépendante**, en Rust et sur le vrai modèle, de l'analyse Python : les listes ne gagnent que sous ~20 % de densité. **La sparsité doit être produite, pas espérée.**

\### 3. Shift-and-add : honnête, et ce n'est pas pour le CPU

| | Temps | |
|---|---|---|
| multiplication i8×i8 | 2,5 ms | — |
| décalages + additions (3,12 add/poids) | 110,7 ms | **×44** |

Résultat **identique**, mais 44× plus lent : la multiplication entière est vectorisée SIMD, la boucle de décalages est scalaire et imprévisible. **Le CPU n'est pas la cible du shift-and-add** — c'est le FPGA, où le multiplieur coûte des DSP et où l'additionneur décalé coûte quelques ALM.

\## Ce que je propose d'optimiser maintenant

Par ordre de gain attendu :

1. **Pool de threads persistant** → supprimer le plancher de 0
… [745 caractères tronqués]

### Tour 22 — oui

*15 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs`
- bash — Add sign positions to the bitmap encoding
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/list.rs`
- bash — Update main.rs and rebuild
- bash — Fix compile errors and rebuild
- bash — Fix Copy impl and worker accumulator handling
- bash — Run the optimized engine benchmark
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs`
- bash — Rebuild and re-run the benchmark
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs`
- bash — Rebuild with the varint fix and run
- bash — Update README and commit the optimizations

**Synthèse produite :**

⏵ Les deux optimisations sont en place et mesurées

\## Le gain, par densité

| Densité | Événements | avant | **après** | ms/appel | gain |
|---|---|---|---|---|---|
| 0 % | 0 | — | — | **0,049** | **×10** |
| 1 % | 43 560 | 0,11 G év/s | **0,84** | 0,052 | ×7,5 |
| 5 % | 217 851 | 0,54 | **2,95** | 0,074 | ×5,5 |
| 10 % | 433 035 | 1,07 | **4,02** | 0,108 | ×3,8 |
| 25 % | 1 082 120 | 2,31 | **4,91** | 0,220 | ×2,1 |
| 100 % | 4 325 087 | 5,77 | **5,80** | 0,746 | ×1,0 |

**Contrôle : `pool OK | scoped OK | bitmap OK`** — les trois chemins donnent le même résultat que le produit dense.

\## Ce que chaque optimisation attaque

- **Le pool persistant** attaque le coût **fixe** : 0,484 ms → **0,049 ms**. C'est exactement ce qu'il fallait, parce que ce coût fixe écrasait le régime creux — celui qui nous intéresse. D'où le **×8,5 à 1 % de densité**, et un plancher divisé par 10.
- **Les décodeurs rapides** attaquent le coût **par événement** : pic à **5,80 G événements/s** (contre 4,66), soit **75 % du banc C de référence** (7,79 G) — lequel utilisait des écarts à largeur fixe, donc plus faciles à décoder que nos varints.

Et le résultat qui valide toute l'architecture :

> **Le débit varie de ×15** entre densité nulle (0,049 ms) et densité pleine (0,746 ms).
> Le débit variable de la cascade n'est plus une hypothèse — il est mesuré.

\## Détail intéressant : varint vs bitmap

| | Vitesse (100 %) | Taille |
|---|---|---|
| listes varint | **5,80 G év/s** | 7,97 b/poids |
| bitmap + signes | 4,07 G év/s | **1,99 b/poids** |

Le varint gagne en **vitesse** (le chemin rapide « un octet » est très efficace sur une matrice dense), le bitmap gagne en **taille** (4× plus compact). À densité faible, les deux se rejoignent (0,84 vs 0,85). Donc : **bitmap pour le stockage, varint pour l'exécution** — ou un format hybride qui bascule selon la densité de la ligne, ce que le moteur sait déjà faire.

\## Un bug attrapé par le contrôle de justesse

Mon « chemin rapide » varint ne consommait pas le premier octet des varints **multi-octets** : dès qu'un écart dépassait 127 (soit 1 % de densité et moins), le décodage partait en vrille et débordait du tampon. Le contrôle `listes vs dense` l'a signalé immédiatement. C'est précisément pour ça qu'il faut garder une vérification de justesse dans le banc.

\## Où on en est, et ce qui reste

```
4,66 G év/s  →  5,80 G év/s   (pic)
0,484 ms     →  0,049 ms      (plancher)
```

Le plancher de 0,049 ms est maintenant dominé par la **réductio
… [788 caractères tronqués]

### Tour 23 — fais les 4 optimisations

*101 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs`
- bash — Add FusedSign, update main.rs, and build
- bash — Fix the three compile errors
- bash — Run the fully optimized engine
- bash — Cap the touched-destination tracking and re-run
- bash — Compare fused vs two-list decoders in the pool
- bash — Fix scope error and run the dual-decoder comparison
- bash — Fix accumulator clearing and re-run
- bash — Fix the reduction window and re-run
- bash — Diagnose which decoder diverges
- bash — Unify the touched bookkeeping and re-run
- bash — Re-run benchmark twice for variance
- bash — Inspect repo state before documenting
- bash — Check gitignore and engine structure
- … et 79 autres

**Synthèse produite :**

⏵ Inférence complète livrée et validée. Bilan

**Ça tourne.** Qwen2.5-0.5B-Instruct Q8_0 génère du texte sur le CPU de cette machine, sans GPU, sans BLAS, sans aucune dépendance — 2 319 lignes de Rust, `std` seul, zéro avertissement.

```
<|im_start|>user
Give the first five prime numbers, separated by commas.<|im_end|>
<|im_start|>assistant
3, 5, 7, 11, 13<|im_end|>
```

| | |
|---|---|
| Génération | **10,5 tok/s** (16 threads), TTFT 75–95 ms |
| Événements/token | 352,8 M à 3,9 G év/s — le forward est **entièrement** borné par les événements |
| Mémoire | 1,27 Go (0,71 Go de listes), chargement 6,3 s |
| Justesse | **16 tokens sur 16 identiques** à la référence numpy float32 |
| Perplexité WikiText-2 | **24,90** contre **25,00** pour numpy + OpenBLAS |
| Référence | 132 ms/token pour numpy+OpenBLAS (40 threads) contre **95 ms** ici (16 threads) |

**Le chiffre qui compte pour le projet** — même modèle, même quantification, mêmes tokens, seule change la façon de parcourir les poids :

| | mémoire | tok/s |
|---|---|---|
| Listes d'événements | 0,71 Go (1,44 o/poids) | 10,52 |
| Matrice dense int8 | 0,49 Go (1,06 o/poids) | 11,42 |

**L'architecture événementielle coûte 8 %** — alors qu'elle lit 36 % de mémoire en plus, décode des varint et disperse dans 16 accumulateurs avant réduction. Le pari matériel tient : le FPGA ne paie aucun de ces coûts, et n'a pas de multiplieur du tout.

Trois choses que je dois te signaler franchement :

1. **Mon portage Python du pré-tokenizer Qwen2 était faux** (5 écarts : `Musicnotes.com` → `. com` au lieu de `.com`, `a\n\nb`, `(?i:)` absent…). Le tokenizer Rust livré est conforme au motif exact — 737/737 contre un moteur regex Perl, plus 13 468 cas de fuzz. Conséquence : **la perplexité de 20,29 publiée plus tôt devra être reprise** ; elle a été calculée avec le tokenizer approximatif. La comparaison 24,90 vs 25,00 reste valide (même suite d'identifiants des deux côtés).
2. **Le dense a d'abord été 20 % plus lent** (8,5 tok/s) — sa boucle de produit scalaire était limitée par une chaîne d'accumulation i64 unique. Déroulée 4×, elle passe à 11,4. La comparaison publiée oppose deux implémentations soignées, pas un cheval de trait à un pur-sang. Et sur AVX2 un noyau dense écrit à la main irait plus loin : la dispersion n'est pas vectorisable.
3. **Le débit variable reste hors d'atteinte** : 352 M événements par token, à tous les tokens, parce qu'un LLM dense n'a jamais d'activation nulle. C'est le point qui décide de l'avenir
… [122 caractères tronqués]

### Tour 24 — peut-on dire que ça permet de faire fonctionner des modèles 4 bits sur cpu efficacement?

*18 appels d'outils.* Actions notables :

- bash — Generalize head to Q4_0 and test
- bash — List available models
- bash — Run Q4_0 through the event engine
- bash — Check tensor types in the Q4 file
- bash — Add Q4_1 support and run the 4-bit model
- bash — Compare list sizes and memory Q8 vs Q4
- bash — Add weight pruning flag
- bash — Check Q4 PPL progress
- bash — Wait for Q4 perplexity
- bash — Clean benchmark: Q8 vs Q4 vs pruning levels
- bash — Split forward vs head cost by pruning level
- bash — Split forward vs head, fixed quoting
- bash — Instrument forward phases
- bash — Profile after pruning
- … et 4 autres

**Synthèse produite :**

⏵ Réponse courte : non. Voici pourquoi, chiffres en main

**Non — pas par ce chemin.** J'ai fait tourner le Q4_0 (fichier mixte Q4_0/Q4_1, j'ai dû ajouter le support Q4_1) dans exactement le même moteur :

| | Q8_0 | Q4_0/Q4_1 | écart |
|---|---|---|---|
| Fichier GGUF | 506 Mo | 337 Mo | **−33 %** |
| Listes en mémoire | 0,71 Go | 0,63 Go | **−11 %** |
| Événements/token | 352,7 M | 312,5 M | −12 % |
| Débit | 10,33 tok/s | 11,78 tok/s | +14 % |
| **Perplexité** | **24,90** | **27,83** | **+12 % de perte** |

Le fichier perd un tiers de sa taille, notre représentation n'en gagne que **11 %** : chaque événement coûte `varint(écart) + i8(valeur)` ≈ 2 octets, **quelle que soit la précision de la source**. Le 4 bits est élargi à 8 bits au chargement, et la vitesse suit le *nombre d'événements*, pas le nombre de bits. On échange 12 % de perplexité contre 11 % de mémoire : mauvais marché. Même avec un empaquetage idéal (1 octet d'écart + 1 nibble), on serait à 1,5 o/événement contre 0,56 o/poids en Q4 dense — 2,7× plus gros, parce qu'à 99 % de densité **chaque poids a besoin de son octet d'écart**.

Mais en creusant j'ai trouvé autre chose, qui est plus important que la réponse :

**Le coût d'un événement n'est pas constant.** En élaguant par magnitude :

| poids gardés | événements | tok/s | débit/événement |
|---|---|---|---|
| 100 % | 352,7 M | 10,33 | 3,56 G év/s |
| 25 % | 89,5 M | 15,64 | 1,43 G év/s |
| 10 % | 35,6 M | 21,40 | **0,88 G év/s** |

**10× moins d'événements ne donnent que 2× de vitesse.** Deux causes identifiées :

1. **Localité.** À pleine densité, 8 événements consécutifs tombent dans la même ligne de cache — une transaction pour huit. À 10 %, chaque événement touche une ligne différente. Un élagage **contigu** (fenêtre de destinations par source — la forme exacte que produiraient tes grappes efférentes) est **30 % plus rapide à événements égaux** : 17,91 contre 13,77 tok/s.
2. **La taille de l'accumulateur — le résultat le plus important.** Chaque worker tient `n_out` entiers 64 bits (39 Ko pour 4864 sorties). Sur des événements épars, **ajouter des threads ralentit** :

| threads | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| matvec, 100 % des poids | 186,6 ms | 120,6 | 99,1 | **90,4 ms** |
| matvec, 10 % des poids | **31,3 ms** | 35,7 | 40,6 | 52,9 ms ❌ |

À 32 workers il faut 1,2 Mo d'accumulateurs : ils débordent le L2 de chaque cœur et chaque écriture part en L3.

**Conséquence pour la carte :** le dimensionnement de l'accumulateur sur 
… [544 caractères tronqués]

### Tour 25 — fpga maintenant

*88 appels d'outils.* Actions notables :

- bash — Recon: FPGA repo, card, simulators, Quartus
- bash — Check sudo, packages, existing RTL
- bash — Check Questa SE, build tools, network
- bash — Find Questa, download iverilog source
- bash — Build iverilog from source
- bash — Check for pre-generated lexer or flex binary
- bash — Start flex+iverilog build in background
- bash — Check iverilog build status
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_pe.sv`
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_pe.sv`
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_pe.sv`
- bash — Check iverilog build completion
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/gen_events.py`
- bash — Generate hardware event stream from real model
- … et 74 autres

**Synthèse produite :**

⏵ Première brique matérielle posée et vérifiée. Bilan

**Le PE événementiel existe, il tourne sur les vraies données du modèle, et il est synthétisé sur la vraie puce.**

**Vérification** — iverilog 13.0, que j'ai dû **construire depuis les sources** (flex puis iverilog, aucune licence requise : c'est ce qui débloque tout, Questa étant toujours en attente). Le flux de test n'est pas synthétique : `tools/gen_events.py` lit le GGUF de Qwen2.5-0.5B et produit les listes par source, quantifiées exactement comme le moteur logiciel.

| Sources | Mots | Résultat |
|---|---|---|
| 1 → 16 | 4 837 → 77 275 | ✅ aucune divergence |
| **64 × 4 864 destinations** | **308 919** | ✅ **aucune divergence** |
| Banc 2 PE + arbre de réduction | — | ✅ |

**Quatre bugs réels trouvés par la simulation** — tous invisibles à la lecture :

1. Lecture BRAM enregistrée **deux fois** → donnée décalée d'un étage.
2. `a2_q` continuait d'avancer après l'armement de `v3_q` → **chaque valeur partait à l'adresse de l'événement suivant** ; l'adresse 0 ne recevait jamais rien.
3. `x_load` perdait la priorité face à un événement du même cycle → la liste suivante repartait de l'adresse précédente (première destination à 4864 au lieu de 0).
4. La valeur n'était pas mémorisée dans le cas d'échappement.

**Synthèse** (Quartus 21.1, 5SGSMD5K1F40C1) :

| | ALMs | DSP | M20K | fmax |
|---|---|---|---|---|
| PE, décalages + additions | **176** | **0** | 5 | 112,5 MHz |
| PE, avec multiplieur | 115 | 1 | 5 | 112,2 MHz |
| **Banc de 32 PE** | **6 498** (4 %) | **0** | 384 (19 %) | **177 MHz** |

➡️ **La contrainte « aucun DSP » du CDC coûte +61 ALMs et pas un hertz** : le chemin critique n'est pas le multiplieur. Et la propriété qui simplifie tout est structurelle : les adresses d'une liste étant strictement croissantes, le pipeline d'accumulation (lecture BRAM → addition → écriture) **n'a jamais d'aléa** — 1 événement par cycle, sans contournement, sans arbitrage.

**La roofline, qui est le vrai résultat :**

| Ressource | Limite |
|---|---|
| ALMs | 850 PE |
| M20K | 167 PE |
| **DDR3 : 9,66 Go/s ÷ 2 octets/événement** | **27 PE** |

**Une carte sature sa propre mémoire avec 27 PE — 3 % de sa logique, 16 % de sa mémoire.** Une carte ≈ 4,8 G événements/s ≈ un CPU 20 cœurs (3,9 G mesurés). Le gain n'est donc **pas dans la cadence brute de la puce** : il est dans le watt par événement et dans la mise à l'échelle par cartes. C'est le lecteur DDR3, pas le PE, qui décidera du débit réel — et il n'est pas en
… [565 caractères tronqués]

### Tour 26 — lecteur ddr3 (listes de connexions, trains d'événements, listes d'activations)

*53 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/pack_lists.py`
- bash — Build the DDR3 memory image
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_reader.sv`
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/pack_lists.py`
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_reader.sv`
- write `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_reader.sv`
- bash — Fix line index and add list padding
- bash — Inspect the push registers
- bash — Fix declaration and check remaining error
- bash — Look at line 145
- bash — Fix enum cast, rebuild image
- bash — Write memory model and run end-to-end test
- bash — Add wait state and rerun end-to-end
- bash — Trace the reader FSM
- … et 39 autres

**Synthèse produite :**

⏵ Lecteur DDR3 livré et vérifié de bout en bout. Bilan

**La chaîne complète tourne** : image DDR3 → lecteur → FIFO → trains d'événements → PE → accumulateur, sur les vraies listes du modèle.

| Test | Résultat |
|---|---|
| 8 sources × 512 destinations | ✅ 4 080 événements, aucune divergence |
| **64 sources × 4 864 destinations** | ✅ **309 020 événements, aucune divergence** |

**Les trois structures que tu as nommées**, produites depuis le GGUF par `tools/pack_lists.py` :

- **Listes d'activations** — la suite des sources actives, au même format de mot de 16 bits que les connexions ; un seul décodeur pour les deux.
- **Table des offsets** — un mot de 64 bits par source portant début *et* fin : une seule lecture, jamais à cheval sur une rafale.
- **Listes de connexions** — le train d'événements de chaque source, transmis au PE **sans décodage** : le format en mémoire est déjà celui que le PE consomme.

Répartition entre lecteurs par **phase** (`une entrée sur N_READER`) : aucun arbitre, aucune communication, aucun état partagé.

**Ce qui a décidé du débit** — mesures successives sur les 309 020 événements :

| Version | Cycles | Évt/cycle |
|---|---|---|
| FIFO 64 mots, requête entre deux poussées | 446 086 | 0,69 |
| + double tampon | 446 086 | 0,69 |
| + FIFO 256 mots | 446 086 | 0,69 |
| **+ requête émise *pendant* la poussée** | **359 579** | **0,86** |

Ni la taille de la FIFO ni le double tampon ne changeaient quoi que ce soit : **la latence mémoire s'ajoutait au lieu de se recouvrir**. Une fois la requête suivante émise pendant la poussée, −24 % de cycles, et 86 % de la capacité du PE.

**Quatre bugs trouvés par la simulation** : états de traitement exécutés *pendant* la latence (interblocage), en-tête écrasé par les 4 derniers coups de la rafale, table capturant le dernier coup au lieu du premier, et origine d'indice à 0 au lieu de −1 (toutes les sources décalées d'une position). Plus un contrat à documenter : `done` signale la fin des *requêtes*, pas la fin du *travail* — il faut attendre que FIFO et pipeline soient vides avant de lire le banc.

**Et une correction que je dois te signaler.** Synthèse : lecteur **1 202 ALMs**, 4 M20K, 0 DSP, **109,9 MHz**. Une voie complète = 1 378 ALMs, 16 M20K.

| | estimation précédente | réalité |
|---|---|---|
| Voies pour saturer la DDR3 | 27 | **44** |
| Logique | 3 % | **35 %** |
| Mémoire | 16 % | **35 %** |

J'avais compté les PE seuls. **Le lecteur coûte sept fois plus de logique que l'unité de calcul*
… [584 caractères tronqués]

### Tour 27 — est-ce qu'on traite les couches de neurones séparément dans notre architecture?

*2 appels d'outils.* Actions notables :

- bash — Inspect how layers are handled in the code
- bash — Measure non-matvec cost vs context length

**Synthèse produite :**

⏵ Réponse étayée : oui, strictement — et c'est presque gratuit, sauf pour l'attention

**Oui, strictement, à tous les niveaux.** Voici ce que le code fait réellement :

**Logiciel** — `model.rs` fait **7 produits matriciels par couche** (`wq`, `wk`, `wv`, `wo`, `wgate`, `wup`, `wdown`) × 24 couches = **168 appels au moteur par token**. Chaque appel est une matrice, avec sa propre remise en forme d'accumulateur (`ensure_width`, déclenché presque à chaque fois puisque les largeurs alternent 896 → 128 → 896 → 4864), et sa propre construction de liste d'activations. Les couches sont parcourues en séquence stricte.

**Matériel** — `pack_lists.py` produit **une image mémoire par tenseur**. Le lecteur fait un en-tête, une table, une liste d'activations par matrice, puis s'arrête. **Il n'existe aucun séquenceur** : rien ne parcourt les 168 matrices.

**Ce qui n'est dans l'architecture à aucun niveau** — et c'est le vrai contenu de ta question :

| Étape | Où elle tourne | Coût mesuré (contexte 64) |
|---|---|---|
| RMSNorm, RoPE, softmax, SiLU, résidus | code hôte, **float**, mono-thread | 1,4 ms sur 96 ms |
| 168 produits matriciels | moteur d'événements | **94,6 ms (98 %)** |
| Chemin retour (accumulateur → liste d'activations) | **n'existe pas** | — |

Donc aujourd'hui le FPGA calcule *une matrice*. Il ne calcule pas *une couche*, et encore moins un modèle.

**Est-ce que la séparation coûte cher ? Non, mesuré.** Le surcoût par matrice (en-tête + table + liste d'activations) représente ~0,6 % du trafic des listes pour une couche de 0,5 B, et en logiciel le coût par appel est invisible : les 72 produits matriciels d'attention coûtent 8,1 ms, les 96 du MLP 86,5 ms, tous deux exactement à la cadence d'événements du moteur. **La séparation est essentiellement gratuite** — bonne nouvelle, parce que c'est elle qui rend le cluster possible.

**Deux choses qu'elle expose, en revanche :**

**1. On peut fusionner les matrices qui partagent leur entrée.** `q`/`k`/`v` consomment tous `hn` ; `gate`/`up` aussi. Une seule marche d'activations, un seul accumulateur avec décalage de destinations → 168 appels deviennent 96. Le gain de débit est négligeable (le nombre d'événements est identique), mais le séquenceur devient deux fois plus simple.

**2. L'attention n'est pas une liste pré-stockable.** Ses poids sortent d'un softmax calculé à l'exécution : ils ne peuvent pas vivre en DDR3 comme listes de connexions. Et elle croît **linéairement avec le contexte** :

| Contexte | 64 |
… [1121 caractères tronqués]

### Tour 28 — aurait-on des gains en modèle hybride fpga + cpus + gpus en exploitant les points forts de chaque ressource pour des tâc … [98 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Check GPU capabilities and tools
- bash — Benchmark GPU on our three workloads
- bash — Compile with unsupported-compiler override and run
- bash — Look for an older host compiler
- bash — Compile with g++-15 and run the benchmark
- bash — Compile header-free CUDA benchmark
- bash — Try including math.h first
- bash — Run Numba GPU benchmark
- bash — Fix kernel and rerun GPU benchmark
- bash — Minimal test of int8 multiply in Numba CUDA
- bash — Isolate the GEMV typing error
- bash — Cast to int32 and rerun
- bash — Run bandwidth and scatter measurements
- bash — Measure GPU memory bandwidth correctly
- … et 1 autres

**Synthèse produite :**

⏵ Mesures faites. Le résultat bouscule la prémisse du projet — je te le donne tel quel

**nvcc était là** (CUDA 13). Le conflit d'en-têtes avec gcc 16 m'a forcé à passer par Numba, mais les chiffres sont là — et ils changent la conclusion.

**Ce que j'ai mesuré sur cette machine :**

| Ressource | Débit | Sur notre modèle 0,5 B |
|---|---|---|
| **GPU** (RTX 5000) — bande passante | **380 Go/s** | 494 Mo de poids = **1,3 ms/token → 770 tok/s** (dense int8) |
| **GPU** — dispersion d'événements (atomics) | **18,1 G évts/s** | 352,8 M évts = **19,6 ms → 51 tok/s** (mode listes) |
| **CPU** (16 threads) — moteur d'événements | 3,9 G évts/s | 95 ms → 10,5 tok/s |
| **FPGA** (1 carte, projeté) | 4,83 G évts/s | 73 ms → 13,7 tok/s |

**Le fait qui décide de tout : la DDR3 de la carte fait 9,66 Go/s, la mémoire du GPU 380 Go/s — 39× plus.** Or nos listes d'événements sont **portables** : le GPU les consomme telles quelles (18 G évts/s de dispersion, mesuré). À partir de là, l'événementiel ne donne aucun avantage de débit au FPGA : les deux lisent les mêmes octets, et le GPU lit 39× plus vite.

Même par watt, le GPU gagne : 230 W ÷ 18 G évts/s = 12,8 nJ/événement, contre 8,3 nJ pour le FPGA… sauf que le GPU en fait 4× plus par seconde, donc **par token** : 0,44 J pour le GPU contre 2,9 J pour la carte.

**Là où tu as entièrement raison : la communication n'est pas l'entrave, et c'est la liste qui le garantit.** Ce qui traverse, c'est l'activation (896 × 2 o = 1,8 Ko) et la somme partielle (19 Ko) par matrice — soit **3,5 Mo par token sur PCIe = 0,5 ms**, contre 20 à 95 ms de calcul. **Les listes de connexions ne bougent jamais** : ce sont les kilo-octets qui circulent, pas les méga-octets. Aucune architecture dense ne fait ça.

**Donc l'hybride justifié n'est pas celui qu'on imaginait :**

- **GPU** : tout, tant que le modèle tient dans 16 Go — attention (dense, dépendante des données, croissante avec le contexte), normes, tête, échantillonnage *et* les projections. C'est lui qui gagne sur les trois axes.
- **FPGA** : seulement hors du régime « avec GPU » — c'est-à-dire la contrainte du CDC — ou comme **tranche mémoire** pour un modèle qui ne tient pas dans 16 Go : sa DDR3 (9,66 Go/s) bat le PCIe (6,5 Go/s mesuré) de 1,5×, et les listes rendent chaque tranche auto-descriptive.
- **CPU** : l'orchestration, l'échantillonnage, et **les 125 Go de RAM** — le plus grand réservoir de la machine.

**Et le chiffre que je retiens pour la suite** : le moteur CPU lit 706 Mo p
… [569 caractères tronqués]

### Tour 29 — continue

*26 appels d'outils.* Actions notables :

- bash — Inspect decoder and measure delta-run distribution
- bash — Add 4-event SWAR batch path and test
- bash — Compare batch vs scalar decoder, best of 3
- bash — Revert batch and profile with perf
- bash — Try i32 accumulators for the push path
- bash — Complete i32 accumulator and measure
- bash — Fix initializer and measure i32 accumulator
- bash — Disassemble the hot event loop
- bash — Locate the function in the binary
- bash — Dump accumulate_common disassembly
- bash — Extract the hot loop from the disassembly
- bash — Dump the accumulate_common body
- bash — Replace touched-list clearing with span clearing
- bash — Disable touched writes entirely and measure
- … et 12 autres

**Synthèse produite :**

⏵ Gain obtenu, validé, commité. Bilan

**+35 % de débit**, et c'était bien le gain le moins cher du projet — zéro matériel, une seule structure de données supprimée.

| Version | tok/s | matvec + MLP |
|---|---|---|
| liste des destinations touchées | 10,96 | 92,2 ms |
| + accumulateur i32 | 11,38 | 92,2 ms |
| **sans la liste (borne haute cumulative)** | **14,74** | **69,4 ms** |

int16 : 10,0 → **14,92 tok/s**. Le débit par événement passe de 3,6 à **5,3 G évts/s**.

**La cause** : pour ne vider que les destinations réellement écrites, l'accumulateur tenait une liste alimentée à **chaque événement** — une comparaison, une écriture, une mise à jour de longueur, ~6 micro-opérations par événement. Or vider l'accumulateur entier par fenêtre coûte **0,2 % du temps de token**. On payait 45 % du temps des matvecs pour économiser 0,2 %.

**Tout est vérifié, pas supposé** :
- Perplexité WikiText-2 : **24,8995 — inchangée au chiffre près**
- Tokens générés : identiques à la référence numpy (16/16)
- Banc des trois décodeurs : **14/14 IDENTIQUE** sur les 7 densités

**Deux bugs que la suppression a révélés**, tous deux attrapés par les bancs :
1. Les chemins fusion et 2-listes écrivent dans un accumulateur i64, le mode push dans un i32 — et la réduction lisait toujours le second. Symptôme : « DIVERGENT au rang 0 : 0 vs 3513 », la réduction d'un accumulateur jamais écrit.
2. Vider la seule fenêtre du travail précédent ne suffit pas : **si elle rétrécit**, des valeurs plus anciennes survivent au-delà. D'où la borne haute *cumulative* par worker. Symptôme : divergence au rang 895, la dernière destination.

**Deux pistes essayées et écartées par la mesure** — je les note parce qu'elles paraissaient évidentes :
- Décodeur par paquets de 4 événements d'un mot de 64 bits (98,7 % des événements sont des suites d'écart 1) : **−28 %**. Contre-intuitif, vérifié deux fois.
- Accumulateur i32 seul (39 Ko → 19 Ko, pour tenir dans le L1) : **+4 %**, dans le bruit. L'accumulateur n'était pas le facteur limitant.

**Ce qui reste** : 10,4 Go/s utilisés sur les 28,7 Go/s mesurés → **2,8× avant d'être borné par la mémoire**. Et un renversement à noter : à 14,8 tok/s le moteur d'événements est maintenant **plus rapide que le noyau dense int8** (11,4 tok/s) sur la même machine — l'argument « le mode liste coûte 8 % » du rapport précédent est périmé, il faut le relire à l'envers.

Le prochain facteur 2,8 demandera autre chose que du micro-réglage : soit le tuilage de la dimension de sort
… [138 caractères tronqués]

### Tour 30 — bilan complet de nos implantations multi hardwate?

*4 appels d'outils.* Actions notables :

- bash — Gather exact repo state
- bash — Fresh CPU measurements for the assessment
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/bilan-multi-materiel.md`
- bash — Link bilan from README and commit

**Synthèse produite :**

⏵ Bilan consolidé et commité. Voici l'essentiel

\## Ce qui a été construit

| Cible | Livrable | Vérification |
|---|---|---|
| **CPU** | `qtrinet-core` — **2 547 lignes de Rust, `std` seul, 0 dépendance** : GGUF, tokenizer BPE, forward Qwen2, génération, perplexité | tokens identiques à la référence numpy, perplexité identique, **14/14** au banc |
| **FPGA** | `event_pe`, `event_engine`, `event_reader` + bancs + modèle DDR3 + empaqueteur — **1 924 lignes** | **309 020 événements réels, aucune divergence** ; synthétisé sur la vraie puce |
| **GPU** | micro-bancs des deux primitives | mesuré sur les cartes |

Outil reconstruit au passage : **iverilog compilé depuis les sources** — c'est ce qui débloque la vérification RTL sans licence Questa.

\## Un token du 0,5 B Q8

| Implémentation | ms/token | tok/s | |
|---|---|---|---|
| numpy float32 + OpenBLAS (40 threads) | 132 | 7,6 | mesuré |
| CPU, noyau dense int8 | 68 | 14,7 | mesuré |
| **CPU, moteur d'événements** | **63** | **15,8** | **mesuré** |
| FPGA, 1 carte, 51 voies | ~73 | ~13,7 | *projeté* |
| GPU, mode listes | ~19,5 | ~51 | *déduit* |
| **GPU, dense int8** | **~1,3** | **~770** | *déduit* |

| Ressource | Débit | Énergie/événement |
|---|---|---|
| CPU | 5,3 G évts/s | ~57 nJ |
| FPGA | 4,83 G évts/s *(limite DDR3)* | **~8,3 nJ** |
| GPU | **18,1 G évts/s** | ~12,7 nJ |

\## Les trois verdicts

**CPU — la référence, et elle tient.** 15,8 tok/s en arithmétique entière, sans BLAS ni GPU : le moteur d'événements **bat maintenant le noyau dense** sur la même machine. Il reste 2,8× de marge avant la limite mémoire.

**FPGA — vérifié, synthétisé, pas compétitif sur le débit.** Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 % de la M20K. Son vrai argument est l'énergie (7× mieux que le CPU) et l'absence de multiplieur — **176 ALMs, 0 DSP, et pas un hertz de perte** face à la version à DSP. Mais face au GPU : **38× plus lent sur les mêmes octets**, parce que sa DDR3 fait 9,66 Go/s contre 380.

**GPU — il gagne sur les trois axes** : plus rapide, meilleur par événement que le CPU, et il consomme les mêmes listes sans reformatage. **Il n'existe pas, sur cette machine, de régime où le FPGA batte le GPU.**

\## Ce que les listes règlent vraiment

Un seul point du cahier des charges, mais il est réel : **les poids ne bougent jamais**. Ce qui traverse, c'est l'activation — 896 × 2 octets par matrice, **3,5 Mo par token** sur PCIe, soit 0,5 ms contre 63 à 95 ms de calcul. C'est ce 
… [1414 caractères tronqués]

### Tour 31 — peut-on avoir un stream de listes d'Activation post traitement (traité sur une autre coeur et autre ressource)qui permet … [88 caractères tronqués]

*18 appels d'outils.* Actions notables :

- bash — Locate the FFN gate computation for the tap
- bash — Implement the Hebbian tap
- bash — Add Hebbian CLI and prepare the corpus
- bash — Locate the declarations
- bash — Fix duplicate arg insertion
- bash — Inspect the offending block
- bash — Remove stray args and test the Hebbian tap
- bash — Fix and verify the Hebbian tap works
- bash — Remove the last stray line
- bash — Test the Hebbian tap end to end
- bash — Fix quantile and measure the tap cost
- bash — Analyse what the Hebbian trace contains beyond the weights
- bash — Test whether Hebbian node directions are already in W's row space
- bash — Test the nonlinear residual directions
- … et 4 autres

**Synthèse produite :**

⏵ Capteur construit, mesuré, et sa limite tranchée sur données réelles

**Oui pour le flux et la ressource séparée. Non pour les nœuds sur 69 % du modèle** — et ce n'est pas une opinion, c'est un argument de rang vérifié.

\## Le capteur

Je l'ai branché : `--hebbian L --hebb-q Q` accumule `H[o][i] += y[o]·x[i]` **uniquement pour les sorties qui déchargent** (le principe neuromorphique : seuls les neurones qui tirent apprennent). Il ne touche jamais au calcul.

| | 1 025 tokens réels, couche 12, 10 % des sorties |
|---|---|
| sans capteur | 96,75 s |
| avec capteur | 99,64 s |
| **surcoût** | **+3,0 %** |

499 175 activations capturées, soit exactement les 10 % demandés. **Sur un autre cœur, c'est gratuit** — la machine en a 24 inutilisés pendant l'inférence. Le flux existe déjà (c'est lui qui pilote le moteur), sa copie coûte 7 Ko par matrice. Sur FPGA, le point de mesure est une FIFO sur le réseau de réduction.

\## Ce que contient la trace

Elle **n'est pas** une redite des poids :
- **R² = 0,845** par `W·C` → **15,5 % de l'énergie hors de la prédiction linéaire**
- Spectre **très concentré** : 46,2 % de l'énergie sur la première valeur singulière, contre 0,44 % pour `W`. La co-activation vit dans un sous-espace de faible dimension, les poids sont presque isotropes.

\## La limite

| Direction testée | Part dans l'espace des lignes de `W` |
|---|---|
| trace, directions 0 à 2 | **100,00 %** |
| résidu non linéaire, directions 0 à 4 | **100,00 %** |

Et `ffn_gate` a un rang de **896 sur 896 dimensions d'entrée** : l'espace des lignes *est* l'espace entier. Donc **tout nouveau nœud linéaire est une combinaison linéaire des nœuds existants** — sa pré-activation est une fonction linéaire des pré-activations existantes, et avec la même non-linéarité il n'ajoute rien.

\## Où ça a du sens, en revanche

Le critère est net : **le rang des lignes est-il inférieur à la dimension d'entrée ?**

| Projection | Forme | Rang | Nœud linéaire neuf ? |
|---|---|---|---|
| `ffn_gate`, `ffn_up` | 4 864 × 896 | **896** | ❌ zéro dimension |
| `attn_q`, `attn_output` | 896 × 896 | ~853 | ❌ |
| `attn_k` | 128 × 896 | 127 | ✅ **769 directions** |
| `attn_v` | 128 × 896 | 128 | ✅ **768 directions** |
| `ffn_down` | 896 × 4 864 | 893 | ✅ **3 971 directions** |

**69,2 % des poids sont dans des projections saturées, 30,8 % dans des projections ouvertes.** La création de nœuds hebbiens a un sens sur `k`, `v` et `down` — aucun sur `gate`, `up`, `q`, `output`.

**Et la vraie piste n'est 
… [895 caractères tronqués]

### Tour 32 — on doit donc journaliser en vue d'une version ultérieure du modèle et le construire/entrainer en parallèle avec les ress … [703 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Add per-token activation and loss logging
- bash — Run the logging experiment
- bash — Check the loss accumulation code
- bash — Verify the logged data
- bash — Test whether difficulty clusters in activation space
- bash — Cross-validate the predictability of loss from activations
- bash — Measure parallel evaluation capacity
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-programme-evolutif.md`
- bash — Commit the evolutionary program assessment

**Synthèse produite :**

⏵ J'ai instrumenté le programme et mesuré ses prémisses une par une

**Point (1) — la traçabilité : acquise, et elle ne coûte rien.** Le point clé : **il ne faut pas journaliser les événements.** Les poids sont statiques et les événements en sont une fonction déterministe — journaliser les *listes d'activations* suffit à rejouer intégralement le calcul. **1,2 Mo/token au lieu de 706 Mo**, +3,0 % de surcoût. J'ai implémenté la journalisation : 2048 vecteurs d'entrée de couche + la perte de chaque token, pertes cohérentes avec la perplexité au chiffre près.

**Point (2) — les grappes : deux usages, un seul tient.**

| | Mesure |
|---|---|
| η² (variance de perte expliquée par la grappe) | 6,2 % |
| Écart grappe la plus dure / plus facile | **7,1×** |
| **Corrélation des pertes par grappe, apprise → testée** | **r = +0,573** (K=32), +0,232 (K=128) |
| R² hors échantillon | **+0,007** |
| Lecture **linéaire** de la perte depuis les activations | **R² < 0** à toute régularisation |

Les motifs difficiles **existent et se reproduisent** (r = 0,57 d'une moitié à l'autre) — ta prémisse est vérifiée dans son principe. Mais ils **expliquent moins de 1 % de la variance** : la difficulté est à 99 % propre au token, et plus on affine les grappes, plus ça se dégrade (0,57 → 0,23) — la signature du bruit pris pour de la structure.

En revanche, l'autre usage des grappes paie déjà, et c'est mesuré : réorganiser les listes pour que les neurones **co-actifs soient contigus** donne **+30 % de débit** (17,91 contre 13,77 tok/s à événements égaux). Là, les grappes sont un levier d'architecture réel — sur la disposition mémoire, pas sur la structure de difficulté.

**Point (3) — les nouveaux nœuds : les cibles sont mesurables.** La rétroaction négative doit viser **30,8 % des poids** (projections ouvertes : `attn_k` 127/896, `attn_v` 128/896, `ffn_down` 896/4864) et les **401 856 monômes quadratiques** hors du span linéaire. Sur les 69,2 % saturés, tout nœud linéaire est une combinaison des existants — vérifié à 100,00 %.

**Point (4) — les versions concurrentes : la capacité est chiffrée.** ~**100 évaluations de modèle par heure** sur les threads libres (98/h à 4 threads par variante, 83/h à 8), soit 2 400 par jour. Une boucle évolutive a un vrai budget. Détail contre-intuitif : allouer *moins* de threads par variante donne un meilleur débit global.

\## Deux idées de ton programme que notre architecture sert particulièrement

**Les experts** : un expert qui ne tire pas coûte *
… [1232 caractères tronqués]

### Tour 33 — automatise l'enregistrement de toutes nos sessions dsh pour ce projet car les traces sont importantes. ensuite crée un d … [166 caractères tronqués]

*17 appels d'outils.* Actions notables :

- bash — Investigate DSH session storage and automation options
- bash — Inspect session storage size and format
- bash — Inspect the session JSONL schema
- bash — Inspect message payloads
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/archive_sessions.py`
- bash — Run the archiver and inspect the digest
- bash — Fix digest header and install automation
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md`
- bash — Implement the patch loading mechanism
- bash — Create patch generator and test patches
- bash — Validate the patch plumbing with null and cross tests
- bash — Wire patch into PPL mode and validate
- bash — Test patch scale sensitivity
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-greffon.md`
- … et 3 autres

**Synthèse produite :**

⏵ Les trois chantiers sont livrés et vérifiés

\## 1. Archivage automatique des sessions — **en place, et il a déjà tourné**

DSH expose exactement ce qu'il fallait : `DSH_SESSION_JSONL` pointe la trace brute (10 Mo compressés, 24 Mo décompressés pour cette session). `tools/archive_sessions.py` produit dans `journal/sessions/` :

- **`<id>/digest.md`** — relecture versionnable : 34 tours, 696 messages, 722 appels d'outils, résultats tronqués, compactages, objectifs. **858 Ko, régénéré à chaque passage** (donc idempotent, et le diff git ne montre que le nouveau).
- **`<id>/session.jsonl.zstd`** — la trace brute exacte, conservée sur disque, **hors git** (binaire, volumineuse).
- **`MANIFEST.md`** — table des sessions avec volumes, empreintes, compteurs.

**Automatisation double** : un hook git `pre-commit` (le journal accompagne le code, il ne le suit pas) **et** une tâche cron horaire (la trace avance même sans commit). Le hook a tourné sur ce commit même — le digest contient déjà les appels d'outils de ce tour.

Un détail qui compte : les traces ne sont pas un luxe, c'est **ce qui ne se reconstitue pas depuis le code** — le raisonnement, les mesures, et les erreurs.

\## 2. Document de vision — `docs/programme-recherche.md`

Feuille de route en quatre étapes, chacune avec une **porte chiffrée** qui décide de continuer ou d'abandonner :

| Étape | Porte |
|---|---|
| **A** — Boucle sans rétropropagation (0-3 mois) | +1 % de perplexité sur texte retenu, ajustement <1 h — **ou** 1,3× plus rapide à qualité égale par réorganisation contiguë |
| **B** — Architecture évolutive (3-12 mois) | 2× moins cher à perplexité égale, ou 10 % de perplexité en moins à coût égal |
| **C** — Spécialisation et mémoire (an 1-2) | apprendre un fait à l'inférence et le retenir sur 10 000 tokens sans oubli catastrophique |
| **D** — Boucle autonome (an 2-5) | courbe de capacité monotone sur ≥100 cycles, produite par le système lui-même |

Le document contient une section **« ce que la mesure interdit d'espérer »** — les trois résultats de ce projet qui ferment des portes, plutôt que de les ignorer : les motifs récurrents expliquent **moins de 1 %** de la difficulté, un nœud linéaire ne peut **rien** ajouter à 69,2 % des poids, le FPGA **ne bat pas** le GPU. Avec un critère d'arrêt honnête : si l'étape A échoue après 10⁴ candidats, la thèse « on apprend sans gradient sur ce substrat » est falsifiée.

\## 3. Plomberie d'apprentissage — `--patch`, **validée**

```
a = silu(u · x) · (v ·
… [1463 caractères tronqués]

### Tour 34 — /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal doit inclure un automatisme qui produit un .md pour chaque sessi … [203 caractères tronqués]

*22 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py`
- bash — Generate session reports and inspect structure
- bash — Verify all report sections
- bash — Tighten extraction and neutralize embedded headings
- bash — Refine extraction and regenerate
- bash — Wire report generation into the archiver
- bash — Commit the session report automation
- bash — Validate patch semantics with a neuron duplication
- bash — Rank neurons by their correlation with token loss
- bash — Run the neuron gain sweep
- bash — Test global FFN gain — coarser granularity
- bash — Extend the gain sweep on the tuning set
- bash — Fine gain curve on the tuning set
- bash — Verify the gain on held-out data
- … et 6 autres

**Synthèse produite :**

⏵ Étude terminée et commitée. Voici ce qu'elle change

**Deux constats qui nous concernent directement.**

**1. Ils ont résolu par construction le problème qui nous bloque.** Nous avons mesuré que les activations d'un LLM dense ne sont **jamais** exactement nulles — notre débit est donc constant et l'argument « on ne paie que ce qui s'active » reste théorique. Un réseau à spikes **impose** cette parcimonie : le neurone LIF de SpikeGPT décharge à **R̂ = 0,15**, soit **6,7× moins d'événements** dans notre moteur. Notre architecture événementielle est mieux adaptée aux modèles à spikes qu'aux modèles quantifiés denses — c'est un renversement de perspective.

**2. Nous appliquons déjà le principe de Spikingformer sans l'avoir cherché.** Leur correction du défaut structurel de Spikformer/SpikeGPT tient à un **échange d'ordre** : garder le flux résiduel en accumulation et rendre discrète l'entrée de chaque couche linéaire. C'est exactement notre `forward` — `x = o + down` reste flottant, et chaque produit matriciel reçoit un vecteur d'activation quantifié int8. Le principe « spike-driven » est déjà respecté ; nous discrétisons à 8 bits au lieu d'1.

**L'astuce décisive, et elle est contre-intuitive** : l'**alignement séquence = temps** de SpikeGPT. Chez Spikformer, la parcimonie est *par pas de temps* et il en faut T — le gain net est R̂×T, pas R̂. En alignant la dimension séquence sur la dimension temporelle, SpikeGPT travaille à T = 1 effectif et encaisse vraiment les 6,7×. Pour nous, cela veut dire : un modèle **récurrent** à spikes, pas un transformeur à spikes.

**La réponse à notre trou le plus sérieux** vient de Spikformer : l'attention `SN(Q·Kᵀ·V·s)` supprime le softmax (les spikes sont non négatifs, il est redondant), se calcule avec des ET logiques et des additions — **aucune multiplication** — et devient **décomposable** : `Kᵀ·V` d'abord, soit O(N·d²) au lieu de O(N²·d). Consommation théorique de l'attention : **0,594 µJ contre 77-88 µJ**. Et surtout : elle devient **exprimable en événements**. C'est la brique à implémenter après la boucle d'apprentissage.

**Trois autres astuces** : le neurone LIF à état (une mémoire scalaire par neurone, `β = 0,5`, seuil 1, reset 0) ; **BatchNorm au lieu de LayerNorm** — ils rapportent que LN ne s'applique pas aux SNN ; et l'**embedding binaire** par Heaviside, sinon le premier tenseur reste flottant et contamine tout.

**La projection chiffrée** : un modèle à R̂ = 0,15 donnerait ~53 M événements par token au lieu d
… [955 caractères tronqués]

### Tour 35 — attention pour ne pas se perdre à copier les autres et ne pas empiéter non plus sur mon autre programme de recherche htt … [426 caractères tronqués]

*76 appels d'outils.* Actions notables :

- create_goal
- bash — Read the activation quantizer
- bash — Implement threshold and k-WTA activation sparsity
- bash — First threshold sparsity sweep
- bash — Get full output including event counts
- bash — Measure the full sparsity-quality frontier
- bash — Run the k-WTA sweep
- bash — Fix the k-WTA index inversion and re-measure
- bash — Fine sweep around the k-WTA optimum
- bash — k-WTA sweep on the 1024-token tuning set
- bash — Verify k-WTA on the held-out set
- bash — Implement and test homeostatic renormalization
- bash — Retest renormalization with the flag not last
- bash — Measure the real throughput gain from sparsity
- … et 62 autres

**Synthèse produite :**

⏵ Encore un négatif : retirer les contrôles de bornes **ralentit** (1,8 %). Je reviens au code sûr

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/carte-storey-peak.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/multicartes.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/setup_compat_libs.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/quartus_env.sh` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/toolchain.md` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/host_check.sh` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/device/5SGSKF40I3LNAC.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/journal-bringup.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/README.md` | 1 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/fetch_reference_design.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/.gitignore` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/jtag_scan.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/jtag_program_svf.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k1.qsf.template` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k2.qsf.template` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tb/Makefile` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/install_license.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k2.qpf` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/qsf/nipada_k1.sdc` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/ternary.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/tiny_model.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/roofline.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_quantify.py` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/sparsity.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_sparsity.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_precision.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/encoding.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_encoding.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_cpu.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_clusters.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/gguf_min.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_real_clusters.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_value_encoding.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_8bit_perfection.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_list_mode.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/bpe_np.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/transformer_np.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/run_harness.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/gguf.rs` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/list.rs` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs` | 4 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-optimisations.md` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_pe.sv` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/gen_events.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tb/tb_event_pe.sv` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_engine.sv` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/rapport-pe-evenementiel.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/pack_lists.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/rtl/event_reader.sv` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/rapport-lecteur-ddr3.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/bilan-multi-materiel.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-capteur-hebbien.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-programme-evolutif.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/archive_sessions.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-greffon.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/comparaison-spiking.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-imposee.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attention-creuse.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-parcimonie.md` | 1 | 0 |

### Sous-agents lancés

- tour 23 — Rust BPE tokenizer for Qwen2

### Commandes exécutées (échantillon)

- **T1** List working directory contents
- **T2** List top-level contents and sizes
- **T2** Count lines and show git history
- **T2** Check installed EDA tools, distro, GPU/NVLink status
- **T2** Inventory installed Quartus editions and versions
- **T2** Test network access and inspect PCIe topology
- **T2** Inspect FPGA card link status and host platform
- **T2** Check Quartus device database and missing libraries
- **T2** Read PCIe link state from sysfs
- **T2** Check whether Quartus 23.1 Standard supports Stratix V
- **T2** Compare device databases across Quartus installs
- **T2** Look for Stratix V device data and container tooling
- **T2** Download and inspect key reference design files
- **T2** Extract module list and pin assignments from reference design
- **T2** Detect graphical askpass mechanisms and sudo state
- **T2** Test sudo popup and read PCIe slot capabilities
- **T2** Collect detailed PCIe capabilities and slot info
- **T2** Locate libnsl package and diagnose Quartus binary deps
- **T2** Extract libnsl locally and test Quartus startup
- **T2** Verify Stratix V part support and run test synthesis
- **T2** Hunt for the FTDI JTAG interface on USB
- **T2** Fetch libgthread compat library and retry synthesis
- **T2** Kernel-level USB forensics for the FTDI device
- **T2** Install 64-bit libgthread and retry synthesis
- **T2** Determine whether license is tool-wide or device-specific
- **T2** Start live USB kernel log watcher in background
- **T2** Validate the three new tool scripts
- **T2** Inspect USB root hub port controls
- **T2** Read electrical state of every USB port
- **T2** Explore the hinted directories for license and installs
- **T2** Inspect license file features and host ID
- **T2** Power-cycle USB port 13 to force re-enumeration
- **T2** Validate scripts and internal doc links
- **T2** Commit knowledge base and tooling
- **T3** Check USB state after new cable
- **T3** Check JTAG tooling and free the FTDI from ftdi_sio
- **T3** Install OpenOCD and scan the JTAG chain
- **T3** Test OpenOCD without root and check Pro device support
- **T3** Make scripts executable and test jtag_scan
- **T3** Commit JTAG milestone
- … et 557 autres

## 4. Mesures et résultats marquants

- **T2** `CPU(s) scaling MHz:                      97%`
- **T2** `Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-`
- **T2** `CPU(s) scaling MHz:                      98%`
- **T4** `/dev/nvme0n1p2  828G  243G  586G  30% /home`
- **T4** `Creating uninstaller 25%`
- **T4** `Creating uninstaller 50%`
- **T4** `Creating uninstaller 75%`
- **T4** `Creating uninstaller 100%`
- **T7** `Info (21062): Implemented 13 DSP elements`
- **T7** `# SDC — Kernel 1 : v14_l2_distance @ 200 MHz`
- **T7** `Logic utilization (in ALMs) : 251 / 172,600 ( < 1 % )`
- **T7** `Total pins : 548 / 864 ( 63 % )`
- **T7** `Total block memory bits : 0 / 41,246,720 ( 0 % )`
- **T7** `Total RAM Blocks : 0 / 2,014 ( 0 % )`
- **T7** `Total DSP Blocks : 13 / 1,590 ( < 1 % )`
- **T7** `Total HSSI STD RX PCSs : 0 / 36 ( 0 % )`
- **T7** `Total HSSI 10G RX PCSs : 0 / 36 ( 0 % )`
- **T7** `Total HSSI GEN3 RX PCSs : 0 / 36 ( 0 % )`
- **T7** `Total HSSI PMA RX Deserializers : 0 / 36 ( 0 % )`
- **T7** `Total HSSI STD TX PCSs : 0 / 36 ( 0 % )`
- **T7** `Total HSSI 10G TX PCSs : 0 / 36 ( 0 % )`
- **T7** `Total HSSI GEN3 TX PCSs : 0 / 36 ( 0 % )`
- **T7** `Total HSSI PMA TX Serializers : 0 / 36 ( 0 % )`
- **T7** `Total HSSI PIPE GEN1_2s : 0 / 36 ( 0 % )`
- **T7** `Total HSSI GEN3s : 0 / 36 ( 0 % )`
- **T7** `Total PLLs : 0 / 72 ( 0 % )`
- **T7** `Total DLLs : 0 / 4 ( 0 % )`
- **T7** `# SDC — Kernel 2 : v14_graph_dijkstra @ 200 MHz`
- **T7** `121:| ALM | **238 / 172 600** (< 1 %) |`
- **T7** `126:| Setup slack | **−3,056 ns** → fmax ≈ **124 MHz** (cible 200 MHz) |`
- **T7** `138:3. ~~Synthèse K1~~ ✅ — `.sof` produit. **Reste : tenir 200 MHz** (slack −3,056 ns, fmax ≈ 124 MHz).`
- **T8** `accuracy float = 8.79 %  (3.9 s)`
- **T8** `float32 (référence)              32.00 b/poids   acc=  8.79 %`
- **T8** `int8 (signe-magnitude)            8.00 b/poids   acc=  8.69 %`
- **T8** `int4 (signe-magnitude)            4.00 b/poids   acc=  8.50 %`
- **T8** `ternaire 1,58 b (dense 2 b)       2.00 b/poids   acc=  8.89 %`
- **T8** `multi 2 plans ternaires           4.00 b/poids   acc=  8.40 %`
- **T8** `multi 3 plans ternaires           6.00 b/poids   acc=  8.50 %`
- **T8** `multi 4 plans ternaires           8.00 b/poids   acc=  9.08 %`
- **T8** `accuracy float = 76.07 %  (5.0 s)`
- **T8** `float32 (référence)              32.00 b/poids   acc= 76.07 %`
- **T8** `int8 (signe-magnitude)            8.00 b/poids   acc= 76.27 %`
- **T8** `int4 (signe-magnitude)            4.00 b/poids   acc= 74.12 %`
- **T8** `ternaire 1,58 b (dense 2 b)       2.00 b/poids   acc= 49.71 %`
- **T8** `multi 2 plans ternaires           4.00 b/poids   acc= 73.44 %`
- **T8** `multi 3 plans ternaires           6.00 b/poids   acc= 74.12 %`
- **T8** `multi 4 plans ternaires           8.00 b/poids   acc= 75.98 %`
- **T8** `erreur max = 3.72e-01 | accuracy entier = 47.75 % (flottant 49.71 %)`
- **T8** `modèle minimal — ternaire dense 2 b       0.0 Mo      0.000 ms/token  13989862.4 tok/s     312 voies     9360 ALM`
- **T8** `modèle minimal — multi 4 bits (1 b/plan)       0.0 Mo      0.000 ms/token  6994931.2 tok/s     156 voies     4680 ALM`
- **T8** `modèle minimal — multi 4 bits (bitmap+signe)       0.0 Mo      0.000 ms/token  3497465.6 tok/s      78 voies     2340 ALM`
- **T8** `modèle minimal — int8                    0.0 Mo      0.000 ms/token  3497465.6 tok/s      78 voies     2340 ALM`
- **T8** `modèle minimal — ternaire CSR (CDC)       0.0 Mo      0.001 ms/token  1645866.2 tok/s      37 voies     1110 ALM`
- **T8** `7B — ternaire 2 b                     1750.0 Mo    181.159 ms/token       5.5 tok/s     312 voies     9360 ALM`
- **T8** `7B — 4 bits                           3500.0 Mo    362.319 ms/token       2.8 tok/s     156 voies     4680 ALM`
- **T8** `7B — ternaire CSR                    14875.0 Mo   1539.855 ms/token       0.6 tok/s      37 voies     1110 ALM`
- **T8** `70B — ternaire 2 b                   17500.0 Mo   1811.594 ms/token       0.6 tok/s     312 voies     9360 ALM`
- **T8** `70B — 4 bits                         35000.0 Mo   3623.188 ms/token       0.3 tok/s     156 voies     4680 ALM`
- **T8** `70B — ternaire CSR                  148750.0 Mo  15398.551 ms/token       0.1 tok/s      37 voies     1110 ALM`
- **T8** `erreur max = 1.86e-06 | accuracy entier = 49.22 % (flottant 49.71 %)`
- **T8** `2. **La quantification ternaire *post-entraînement* coûte cher** : 76.1 % → 49.7 % (-26.4 pt). Ce n'est PAS un verdict contre BitNet : les modèles ternaires (b1.58) sont *entraînés* avec la contrainte`
- **T8** `3. **Le découpage en plans (multi-bits) dégrade progressivement** : 4 plans → 76.0 % (-0.1 pt). C'est la voie naturelle pour réutiliser un modèle 4 bits existant sans réentraînement.`
- **T8** `5. **Tout le projet est borné par la DDR3**, pas par le calcul : à 124 MHz il ne faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. 96 % du device reste disponible pour `
- **T9** `accuracy float          : 76.07 %`
- **T9** `accuracy ternaire       : 49.71 %`
- **T9** `densité naturelle       : 26.3 % des poids sont non nuls`
- **T9** `activations non nulles  : 52.8 % (ReLU)`
- **T9** `100.0%    26.3%   49.71%      2.00      1.26      4.48      8.69   ×1.58`
- **T9** `75.0%    19.8%   49.41%      2.00      1.20      3.36      6.52   ×1.67`
- **T9** `50.0%    13.2%   45.31%      2.00      1.13      2.24      4.35   ×1.77`
- **T9** `25.0%     6.6%   52.93%      2.00      1.07      1.12      2.17   ×1.88`
- **T9** `12.5%     3.3%   50.00%      2.00      1.03      0.56      1.08   ×1.94`
- **T9** `6.2%     1.6%   50.49%      2.00      1.02      0.28      0.54   ×1.97`
- **T9** `3.1%     0.9%   47.66%      2.00      1.01      0.15      0.28   ×1.98`
- **T9** `densité 24.0 %  accuracy 48.73 %  coût 1.50 b/poids  gain ×1.33`
- **T9** `bitmap vs dense2   : égalité à d = 100.0 %  → bitmap gagne en dessous`
- **T9** `csr32 vs dense2   : égalité à d =   6.1 %  → csr32 gagne en dessous`
- **T9** `csr16 vs dense2   : égalité à d =  11.8 %  → csr16 gagne en dessous`
- **T9** `csr32 vs bitmap   : égalité à d =   3.1 %  → csr32 gagne en dessous`
- **T9** `csr16 vs bitmap   : égalité à d =   6.2 %  → csr16 gagne en dessous`
- **T9** `=== projection 7B (1 carte, DDR3 9,66 Go/s) ===`
- **T9** `100.0%       5.5        5.5        0.6        0.3      7.4`
- **T9** `26.3%       5.5        8.7        2.5        1.3      7.4`
- **T9** `50.0%       5.5        7.4        1.3        0.7      7.4`
- **T9** `25.0%       5.5        8.8        2.6        1.3      7.4`
- **T9** `12.5%       5.5        9.8        5.2        2.7      7.4`
- **T9** `6.2%       5.5       10.4       10.4        5.4      7.4`
- **T9** `1. **Oui, un modèle ternaire est déjà creux** — ici 26.3 % de non-nuls, sans aucun élagage. C'est le point de départ, pas une contrainte ajoutée.`
- **T9** `3. **Le CSR, lui, est disqualifié** : rentable seulement sous 6 % (indice 32 b) ou 12 % (indice 16 b) de densité — un régime que les LLM n'atteignent pas sans s'effondrer.`
- **T9** `4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *et* l'activation sont non nuls (ici 13.9 % d'événements réels). Récupérer l'activation à un inde`
- **T9** `5. **Recommandation** : garder le dense 2 bits comme chemin nominal (simple, déterministe, déjà validé) et ajouter un **encodage bitmap + signe** là où la densité est faible. Le saut de blocs entièrem`
- **T9** `- La courbe précision ↔ élagage est **bruitée** : le modèle ne pèse que 2688 poids et son accuracy ternaire (49.7 %) laisse peu de marge de mesure. Les variations observées (±4 pt) sont dans le bruit `
- **T9** `- La densité naturelle (26.3 %) est propre à ce modèle. Un modèle **entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : le gain du bitmap y serait de ×1,2 à ×1,4, pas ×`
- **T9** `- La littérature (SparseGPT, Wanda) situe l'élagage non structuré *one-shot* des LLM à 50-60 % sans réentraînement, et le 2:4 structuré (50 %) est la forme matériellement supportée. **Au-delà de ~90 %`
- **T10** `accuracy float (référence) : 76.07 %`
- **T10** `creux 1 bits d=0.125        1     8.4%     1.08    60.06%      10.2 *`
- **T10** `creux 1 bits d=0.250        1    16.8%     1.17    64.84%       9.5 *`
- **T10** `creux 2 bits d=0.125        2    11.8%     1.24    65.04%       8.9 *`
- **T10** `creux 1 bits d=0.500        1    26.6%     1.27    48.63%       8.7 *`
- **T10** `creux 3 bits d=0.125        3    12.3%     1.37    67.29%       8.1 *`
- **T10** `creux 2 bits d=0.250        2    24.0%     1.48    70.41%       7.5 *`
- **T10** `creux 4 bits d=0.125        4    12.4%     1.50    67.48%       7.4 *`
- **T10** `creux 3 bits d=0.250        3    24.8%     1.74    71.09%       6.3 *`
- **T10** `creux 2 bits d=0.500        2    49.3%     1.99    72.17%       5.6 *`
- **T10** `creux 4 bits d=0.250        4    24.9%     2.00    71.09%       5.5 *`
- **T10** `creux 8 bits d=0.125        8    12.5%     2.00    67.87%       5.5 *`
- **T10** `dense 1 bits (ternaire)     1   100.0%     2.00    49.71%       5.5 *`
- **T10** `dense 2 bits                2   100.0%     2.00    73.44%       5.5 *`
- **T10** `creux 3 bits d=0.500        3    50.0%     2.50    74.22%       4.4 *`
- **T10** `creux 4 bits d=0.500        4    50.0%     3.00    76.07%       3.7 *`
- **T10** `dense 3 bits                3   100.0%     3.00    74.12%       3.7 *`
- **T10** `creux 8 bits d=0.250        8    25.0%     3.00    71.68%       3.7 *`
- **T10** `dense 4 bits                4   100.0%     4.00    75.98%       2.8 *`
- **T10** `creux 8 bits d=0.500        8    50.0%     5.00    76.27%       2.2 *`
- **T10** `dense 8 bits                8   100.0%     8.00    76.37%       1.4 *`
- **T10** `creux 1 bits d=0.500        1    26.6%     1.27    48.63%       8.7`
- **T10** `creux 4 bits d=0.125        4    12.4%     1.50    67.48%       7.4`
- **T10** `creux 4 bits d=0.250        4    24.9%     2.00    71.09%       5.5`
- **T10** `creux 8 bits d=0.125        8    12.5%     2.00    67.87%       5.5`
- **T10** `dense 1 bits (ternaire)     1   100.0%     2.00    49.71%       5.5`
- … (tronqué)

## 5. Erreurs rencontrées

75 sorties en erreur ou divergentes. Les premières :

- **T2** : === LIEN PCIe (sysfs, sans root) === current_link_speed     = 8.0 GT/s PCIe current_link_width     = 8 max_link_speed         = 8.0 GT/s PCIe max_link_width         = 8 secondary_bus_number   =  vendo
- **T2** : [POPUP: saisissez le mot de passe] === TOUS les événements USB depuis le boot (fin de log) === [ven sep 25 11:52:23 2026] [ T684749] hid-generic 0003:04F2:2159.00ED: hiddev99,hidraw5: USB HID v1.10 De
- **T2** : === libs 64 bits en place === /home/stephane/fpga-compat/lib64/libnsl.so.1 /home/stephane/fpga-compat/usr/lib64/libgthread-2.0.so.0 /home/stephane/fpga-compat/usr/lib64/libgthread-2.0.so.0.7800.3  ===
- **T2** : === licence requise pour l'outil ou pour Stratix V ? test Cyclone V === Error (292025): License file is not specified.  === fichiers de licence présents sur le système ? === /home/stephane/.altera.qua
- **T2** : ############ TEST host_check.sh ############  === MACHINE === Precision Tower 7910 0215PR CPU(s):                                  40 Model name:                              Intel(R) Xeon(R) CPU E5-2
- **T4** : === options de quartus_sh liées aux devices ===  === test : quartus_sh --list_parts === Error (23024): Unknown long option --list_parts. Refer to --help for legal options  Usage: ------   === test : r
- **T4** : === requête Tcl : parties Stratix V connues === Info: Command: quartus_sh -t "puts PARTLIST_BEGIN; foreach p [get_part_list -family Stratix" "V] { if {[string match 5SGSMD5* ]} { puts  } }; puts PARTL
- **T4** : === syntaxe host_check.sh === OK  === QSF : plus aucune référence au device custom ? === qsf/nipada_k1.sdc:2:# Stratix V GS 5SGSKF40I3LNAC qsf/nipada_k2.sdc:2:# Stratix V GS 5SGSKF40I3LNAC qsf/nipada_
- **T4** : === cocotb réellement installé ? === Traceback (most recent call last):   File "<string>", line 1, in <module> (cocotb-config absent du PATH)  === quartus_sh depuis le script d'env (test final) === ⚠ 
- **T4** : === imports des testbenches === from cocotb.clock import Clock from cocotb.triggers import RisingEdge, ClockCycles from pathlib import Path import cocotb import json import math  === modules python pr
- **T4** : === installation cocotb 2.0.1 + pytest en mode utilisateur ===  === vérification ===   cocotb importé, version 2.0.1   pytest 9.1.1   -rwxr-xr-x. 1 stephane stephane 166 25 sep 12:40 /home/stephane/.l
- **T4** : === toutes les interfaces réseau et leurs MAC ===   docker0        ca:03:02:a7:01:2c  down   enp0s25        64:00:6a:55:1b:60  up   enp6s0         64:00:6a:55:1b:97  up   virbr0         52:54:00:08:5d
- **T4** : === syntaxe === OK  === exécution : le contrôle HOSTID doit alerter === ⚠  Aucune licence configurée → 'Error (292025): License file is not specified.'    Obtenir le fichier de licence Quartus Prime S
- **T5** : syntaxe OK  === test avec la licence liée à un autre poste (doit refuser) === ==> Analyse de /home/stephane/Data13TB/stephane/Downloads/LR-171690_License.dat     HOSTID   : b8ca3a840e66     features :
- **T7** : SALT_LICENSE_SERVER = /home/stephane/.altera.quartus/questa_lic.dat;/home/stephane/.altera.quartus/license.dat  ########## SIMULATION KERNEL 2 (Bellman-Ford) ########## COCOTB_TEST_MODULES=tb_v14_grap

## 6. Commits

- Moteur d'événements : les 2 décodeurs sont exacts, mesures consolidées  Le chemin « 2 listes » ne tenait pas de liste de destinations touchées : il vidait l'acc
- Moteur d'événements : les 2 décodeurs sont exacts, mesures consolidées  Le chemin « 2 listes » ne tenait pas de liste de destinations touchées : il vidait l'acc
- Moteur : fenêtre de réduction exacte, pool borné, exactitude aux 7 densités  Trois défauts structurels corrigés, chacun découvert par une mesure fausse :  1. La
- Inférence complète en Rust : Qwen2.5-0.5B sans GPU, sans BLAS, sans dépendance  Le moteur d'événements exécute un vrai LLM de bout en bout : tokenizer BPE Qwen2
- Mode dense de comparaison : l'architecture evenementielle coute 8 % sur CPU  Meme modele, meme quantification (int8 par ligne), memes activations (int16), memes
- Inférence Rust : zéro avertissement, exemple de sortie, mode dense documenté  - DenseQ8::dot réutilisé dans le worker (fin de la duplication) - champs morts ret
- 4 bits : non, et la raison est plus intéressante que la réponse  Q4_0/Q4_1 (fichier mixte, ajout du support Q4_1) dans le même moteur : - fichier 337 Mo au lieu
- README : reponse courte sur le 4 bits et le cout par evenement" && git log --oneline | head -1
- PE evenementiel : RTL verifie sur donnees reelles et synthetise sur Stratix V  Premiere brique materielle du projet : acc[adresse] += x x poids depuis un flux d
- PE evenementiel : RTL verifie sur donnees reelles et synthetise sur Stratix V  Premiere brique materielle du projet : acc[adresse] += x x poids depuis un flux d
- Verification du banc multi-PE et de l'arbre de reduction  tb/tb_event_engine.sv : deux PE pilotes avec le meme flux (la reduction doit valoir 2x l'accumulation 
- Lecteur DDR3 : listes de connexions, trains d'evenements, listes d'activations  Chaine complete verifiee de bout en bout : image DDR3 -> lecteur -> FIFO -> trai
- Lecteur : le chemin critique n'est pas l'arithmetique d'adresse  Hypothese testee : pre-calculer lists_ptr + (cur >> 2) dans un registre pour sortir le decalage
- Moteur : +35 % en supprimant la liste des destinations touchees  Le moteur lisait 706 Mo/token en 95 ms (7,4 Go/s sur 28,7 disponibles) : il n'etait pas borne p
- Bilan multi-materiel : CPU, FPGA, GPU  Consolide les trois implementations avec leurs chiffres mesures, deduits ou projetes, explicitement etiquetes :  - CPU (m
- Capteur hebbien : +3,0 % de surcout, et une limite mathematique verifiee  Branche un accumulateur de co-activation H[o][i] += y[o]*x[i] sur une projection, pour
- Journalisation des activations et evaluation du programme evolutif  Ajoute la journalisation par token : vecteur d'entree d'une couche + perte du token suivant.
- Archivage des sessions, programme de recherche, plomberie d'apprentissage  TROIS LIVRABLES.  1. ARCHIVAGE AUTOMATIQUE DES SESSIONS DSH    tools/archive_sessions
- Rapport de session automatique : reconstitution de l'essence et du travail  journal/ contient desormais, pour chaque session, genere automatiquement : - session
- Comparaison avec SpikeGPT, Spikformer et Spikingformer  Etude des trois references neuromorphiques et comparaison point par point avec notre architecture. Sourc
- Parcimonie imposee a l'inference : la frontiere mesuree  Campagne sur Qwen2.5-0.5B Q8_0 PREENTRAINE, sans aucun entrainement, avec deux jeux de 1024 tokens (A p
- Attention creuse : le trou se referme, et par le haut  Une seule modification a l'inference, sans reentrainement : ne garder que les k plus grands scores par re
- Attention creuse : correction -- le gain est en qualite, pas en temps  J'avais annonce une attention \"meilleure, moins chere et listable\". La mesure corrige l
- Campagne parcimonie : synthese et configuration gagnante  CONFIGURATION RETENUE (verifiee sur les deux jeux, dont B tenu a l'ecart) : attention a 32 cles + proj
- Attention : divisee par deux par la vectorisation, a perplexite identique  En cherchant pourquoi le top-k ne gagnait pas de temps, j'ai trouve un cout bien plus
- Engine : les controles de bornes ne sont pas le goulot (mesure A/B)  Hypothese : les deux controles de bornes par evenement (data[p], data[p+1]) couteraient plu

