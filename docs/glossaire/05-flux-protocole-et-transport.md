# 5. Flux, protocole et transport

> **Famille 5 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 5. Flux, protocole et transport

**Colab · notebook · tunnel** — Google Colab est un runtime distant gratuit, choisi
pour la démonstration de la phase 3.4 ; comme il n'accepte aucune connexion
entrante, il faut un tunnel (`cloudflared`, `ssh -R`, Tailscale). Le kit est dans
`colab/` (`docs/colab-reparti.md:1-21`, `:70-84`).
**Réf.** : [colab.research.google.com](https://colab.research.google.com/) ;
[tunnel Cloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/).

**Contrat d'activation (`Act`)** — L'ensemble des réglages qui changent les
chiffres calculés : niveaux de quantification, seuil, top-k, renormalisation, et les
sept top-k par projection, plus `attn_topk`, `qk_topk`, `moe_topk`. Ils **voyagent
dans l'en-tête** parce que sans eux le pair distant ne calculerait pas la même
chose — et « le client impose les siens au serveur »
(`docs/format-flux.md:100-109`, `:187`).

**Corps (payload) · en-tête** — Un message de flux = un **en-tête** de taille fixe
(79 octets en v5, `TAILLE_TETE`, verrouillé par `assert_eq!`) suivi d'un **corps**
variable. L'en-tête porte la magie, la version, le mode, la plage de couches, la
position, le compte `n`, l'échelle et le contrat d'activation ; le corps porte les
données du mode (`docs/format-flux.md:88-116`,
`docs/plan-mode4-lot-listes.md:54-55`). Un octet de trop dans l'en-tête décale tout
le corps en silence : c'est le bug le plus coûteux du chantier.

**Couche source (entrée d'attention / entrée de FFN)** — Convention d'encodage
d'une liste : un numéro de couche inférieur à 1 000 désigne l'entrée de
l'attention, supérieur ou égal à 1 000 l'entrée du FFN de la couche
`numéro − 1000`. Un seul champ porte donc deux points de trace
(`docs/format-flux.md:27-28`).

**DRVF (Drave Flux)** — Le format binaire du dépôt, à quatre usages : trace
d'exécution, rejeu, transport réseau, analyse. Un fichier commence par la magie
`DRVF` et une version (1, 2 ou 3) ; le transport utilise la même famille
d'encodage, en protocole v5 (`docs/format-flux.md:1-24`,
`docs/plan-deepseek41-complet.md:17`).

**`flux_brut` · norme finale** — Règle de responsabilité : un flux qui circule est
un **résidu brut** ; la normalisation finale n'appartient qu'au nœud qui possède la
tête de sortie, et s'applique **une fois**. Confondre « ma plage va jusqu'à la
dernière couche » et « je dois normer » a coûté la fidélité du découpage (798,3 au
lieu de 18,2) (`docs/format-flux.md:167-174`, `docs/roadmap.md:244-249`).

**Lot (mode 3) · lot en listes (mode 4)** — Le *lot* transporte `t` états d'un coup
en f32 dense, sans perte, pour que le préremplissage ne paie qu'un aller-retour par
lot (écart mesuré 0,00e0). Le *lot en listes* transporte les mêmes `t` états
encodés comme le mode 2 (échelles par bloc, valeurs i8) : 1,5 ko par jeton au lieu
de 3,5, soit **÷2,3 contre le lot dense** — le rapport de mise en œuvre écrit
« ÷2,2 » et précise que le gain n'est que de 1,07× contre le mode 2 par jeton — pour
un écart de 3,03e-2 (`docs/plan-prefill-reparti.md:1-15`,
`docs/format-flux.md:117-134`, `reports/rapport-mode4-lot-listes.md:30-35`).

**Magie (nombre magique)** — Constante en tête de fichier ou de message qui permet
de reconnaître le format : `0x44525631`, soit les octets `DRV1`, pour le protocole
de flux. Une magie absente signale une désynchronisation du flux d'octets
(`docs/format-flux.md:92`).

**Modes 0 à 4** — Les cinq modes du protocole v5 : **0** dense f32, **1** liste
quantifiée (i16 + une échelle), **2** listes à échelle par bloc (i8, écarts),
**3** lot dense, **4** lot en listes. Le mode 1 est « le format du disque, à
l'octet près » ; le mode 0 est le seul sans perte avec le mode 3
(`docs/format-flux.md:93-116`). Un mode inconnu est refusé **avant** lecture du
corps.

**Nagle · ACK différé · `TCP_NODELAY`** — Nagle est l'algorithme TCP qui retient
les petites écritures en espérant en grouper d'autres ; l'ACK différé retarde
l'accusé de réception. Ensemble, ils faisaient payer **97,6 ms par jeton** au banc
réparti au lieu de 15,9 ms de calcul ; `set_nodelay(true)` ramène l'attente à
16,1 ms (`docs/roadmap.md:113`, `docs/colab-reparti.md:30`).
**Réf.** : RFC 896, [rfc-editor.org/rfc/rfc896](https://www.rfc-editor.org/rfc/rfc896.html) ;
manuel `tcp(7)`, [man7.org](https://man7.org/linux/man-pages/man7/tcp.7.html).

**Nœud moteur · pilote · pair** — Dans la démonstration répartie, le **pilote**
garde les N premières couches (`--ppl-reparti <hôte:port> --couches-locales N`) et
le **nœud moteur** sert le reste (`--flux-serveur <port>`) ; le *pair* est
l'homologue vu par le protocole. Les deux nœuds doivent charger le **même GGUF** :
la dimension ne voyage pas (`docs/colab-reparti.md:70-102`,
`docs/format-flux.md:126-129`).

**Plafond (`PLAFOND_FLUX`, `verifier_taille`)** — Garde-fou de sûreté : toute taille
annoncée par un message est vérifiée **avant** l'allocation correspondante, contre
un plafond de 256 Mo ; un cumul est vérifié état par état. Sans lui, un en-tête
corrompu provoquerait un épuisement mémoire au lieu d'une erreur de protocole
(`docs/plan-mode4-lot-listes.md:183-232`).

**Position (compteur global de jeton)** — Champ de la trace qui compte les jetons
**globalement**, pas la place dans la fenêtre de contexte. Ce détail a coûté un
bug : avec la position dans la fenêtre, deux fenêtres réécrivaient les mêmes clés
et le rejeu rendait 356 694 au lieu de 17,43 (`docs/format-flux.md:75-86`).

**Protocole v5** — Version courante du protocole d'échange réseau : en-tête de
79 octets, cinq modes, contrat d'activation complet, refus immédiat d'un pair
incompatible en nommant les deux versions. Règle écrite dans le code : **un nouveau
mode ⇒ une nouvelle version** (`docs/format-flux.md:88-155`,
`docs/plan-mode4-lot-listes.md:150-181`).

**Sentinelle 0xFFFF** — Marque de fin facultative d'un fichier de trace
(`u16` valant 0xFFFF) ; la fin de fichier suffit, mais la sentinelle est écrite par
la version 1 (`docs/format-flux.md:35`).

**Trace de flux, versions 1 à 3** — v1 : indices `u32` + valeurs `i16` (6,02 octets
par neurone actif) ; v2 : indices par écarts `u8` + valeurs `i16` (3,01 octets, sans
perte, **défaut**) ; v3 : valeurs `i8` + échelle `f16` par bloc de 32 (≈2,08 octets
pour 21 630 645 actifs, avec perte, `DRAVE_TRACE_BLOCS=1`). Le rejeu par lots
n'accepte pas la v3, et le dit (`docs/format-flux.md:32-73`).

---

**Tranche de liste (unité d'échange)** — Granularité du contrat d'échange : un
en-tête (couche, source, échelle, bits) plus des paires (destination, valeur). La
vision en fait l'unité de travail autonome : « distribuer, c'est router des
listes » (`docs/vision.md:146-166`).

**Version (du format et du protocole)** — Trois numérotations coexistent et il faut
les distinguer : la **trace** est en version 1/2/3 (`DRAVE_TRACE_BLOCS`), le
**protocole réseau** en version 5, et le fichier GGUF a sa propre version d'en-tête.
Un refus de version est prononcé **avant** toute interprétation du corps
(`docs/format-flux.md:20-24`, `:143-153`).

