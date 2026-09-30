# Session du 30/09 — index des chantiers

Trois créneaux : 10h06–11h42 (time-box de 2 h), 11h46–15h00 puis 15h07–18h00
(autonomie et parallélisme). Les commits, les campagnes de mesure lourdes et les
relectures déléguées sont comptés dans le journal ; ce document est l'index des
chantiers, pas le décompte. Chaque chiffre a son rapport ; ceci est l'index.

## Ce qui est livré

| chantier | résultat | rapport |
|---|---|---|
| **Calcul réparti fidèle** | écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, 9,5146 à 1 024 | `rapport-phase3-reparti.md` |
| **Préremplissage par LOTS** (mode 3) | 256 jetons en **4 lots** (ou 1 seul) → 0,00e0 ; **18× plus rapide** qu'un flux par jeton sur un lien à 20 ms | `rapport-prefill-reparti.md` |
| **Transport en listes** | dense 3 663 octets → **1 629** par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons | `rapport-transport-liste.md` |
| **où mettre les bits du cache KV** | à taille ÉGALE : clés f32 + valeurs int8 **+0,023 %** contre **+3,01 %** pour l'inverse (facteur **130**) ; 4 bits : +0,46 % contre **+385 %** (facteur **840**) | `rapport-placement-bits-kv.md` |
| **Format de trace v2/v3** | 132 396 736 → **66 370 408** (sans perte) → **45 079 930** octets (+0,074 % de perplexité) | `rapport-compacite-trace.md` |
| **Colab prêt** | dépôt en un fichier (4,5 Mo), notebook, recette, tunnel — vérifié de bout en bout | `colab/README.md` |
| **Drapeaux ignorés** | **46 sur 110** l'étaient dans au moins un mode ; neuf corrigés, tableau de bord `--options-actives` ajouté | `rapport-drapeaux-ignores.md` |
| **Cohérence des documents** | 80 affirmations vérifiées, 38 périmées, 15 contradictoires — corrigées, plus deux bugs de protocole trouvés par la lecture | `rapport-coherence-docs.md` |

## Les défauts trouvés, et par qui

Sur les **vingt-deux défauts corrigés** (deux relectures adversariales comprises,
la seconde attaquant les correctifs de la première), **dix-sept n'ont pas été
trouvés par un banc** mais par une relecture :

- `forward` ignorait la plage de couches (le pilote calculait tout, le pair
  recalculait tout par-dessus) — trouvé en lisant, mesuré ensuite : ×11,2 ;
- la norme finale appliquée deux fois ;
- un en-tête de lot d'UN octet trop long (corps décalé, f32 valides mais faux) —
  trouvé par la spécification déléguée ;
- l'échappement d'indice écrit sur 4 octets et lu sur 2 — trouvé par la relecture
  croisée des documents ;
- `VERSION_FLUX` restée à 3 avec un en-tête passé de 39 à 79 octets ;
- le compteur de listes manquantes aveugle en rejeu par lots (le garde-fou ajouté
  une heure plus tôt ne servait à rien) ;
- les clés de trace incohérentes selon `--lot` (une trace écrite dans un mode était
  illisible dans l'autre) ;
- `--keep` ignoré en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
  flux — la classe « analysé mais jamais appliqué », huit fois ;
- et, dans mes propres correctifs : un tableau de bord qui montrait l'état d'AVANT
  les affectations, un plafond qui ne couvrait qu'une des quatre allocations
  pilotées par le réseau (16 Gio sur une trame de 83 octets), une trame forgée qui
  tuait le nœud, un envoi qui paniquait encore sur un pair fermé.

Leçon de méthode, écrite parce qu'elle a coûté deux fois : **un banc qui passe ne
prouve pas qu'il mesure ce qu'on croit**. Mon premier « rejeu v3 = 19,3885 » était
un faux positif — la trace n'était pas chargée du tout — et ce sont les compteurs
de rejeu qui l'ont démasqué. De même, le chiffre 19,3045 de la table de
non-régression ne s'est pas reproduit : il vaut 19,5633.

## Ce qui n'a pas été fait

- **Noyau GPU de top-k** (phase 1.1) : les trois heures sont allées au transport,
  aux formats et aux garde-fous. Les deux Quadro sont libres, le cadre existe.
- **Mode 4 — lot en listes** : chaque état en liste creuse au lieu de f32 dense
  (÷2,3 sur le fil). Spécifié, pas écrit ; le moteur refuse maintenant explicitement
  de faire semblant (`--flux-blocs --lot 8` le dit au lieu de l'ignorer).
- **Lot en f16, clés en f16 à 8 192** : deux mesures lancées et en cours à l'heure
  d'écrire ; les lignes du rapport de placement se remplissent seules.
- **Démonstration Colab** : tout est prêt côté code, la manipulation demande le
  compte de l'utilisateur (notebook + tunnel).

## Portes, à l'heure d'écrire

Qwen ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** · gpt-oss avec
`DRAVE_GPU=1` = **15,1667** · `cargo test` **13/13** · dépôt propre, quarante
commits, machine rendue.
