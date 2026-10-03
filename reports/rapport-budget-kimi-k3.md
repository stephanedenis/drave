# Kimi-K3 Q4 : ce qu'un jeton lit vraiment, et ce que ça impose

> Écrit le 03/10 (bloc 29) parce qu'un chiffre publié la veille était **faux par
> omission** : « un jeton lit ~35 Go de poids » ne comptait que les **experts**
> (`tools/analyse_octets_par_jeton.py`, écrit pour la question du MoE). Le total
> comprend aussi l'attention, les experts partagés et la tête — et c'est
> **87 Go par jeton**. Ce rapport donne la ventilation mesurée et ce qu'elle
> impose au placement.

## 1. La ventilation, mesurée sur 25 couches (de 93), par type

| | par couche (Mo) | × 93 couches (Go/jeton) |
|---|---|---|
| **attention** (q/k/v/o, `ssm_*`, compresseur) | 554 (KDA) · 327 (MLA) | **48,7** |
| **experts routés** (16 sur 896) | 0,25 Go | **24,7** |
| **experts partagés** (2, ×93) | 140 | **12,4** |
| scores résiduels + tête de sortie | 0,06 + 1,25 (hors couche) | 1,3 |
| **TOTAL** | 15,5 Go | **87,0** |

Deux surprises, et les deux comptent :

1. **L'attention pèse plus que les experts** (48,7 contre 24,7 Go). Elle est
   **dense** : chaque jeton lit *toutes* les matrices d'attention, alors qu'il ne
   lit que **16 experts sur 896**. Un schéma qui ne s'occupe que du MoE — grappes,
   cache d'experts, routage — laisse donc **56 % du trafic** de côté.
2. **Ce qui peut être résident est gros** : la partie dense (attention + experts
   partagés + tête) fait **62,3 Go**, et la partie routée **24,7 Go par jeton**.
   Sur cette machine (125 Go de RAM), **la partie dense tient en RAM**, et il
   reste ~60 Go pour les experts.

## 2. Les planchers, avec les débits mesurés

| placement | débit | s/jeton | commentaire |
|---|---|---|---|
| tout sur disque dur (200 Mo/s) | 0,2 Go/s | **435 s** | hors de question |
| tout sur NVMe (2,0 Go/s) | 2,0 Go/s | **43,5 s** | le modèle fait 1,5 To : il ne tient pas en cache |
| **dense en RAM, experts sur NVMe** | 20 Go/s + 2,0 Go/s | **2,4 + 12,4 = 14,8 s** | le partage « dense résident » ne suffit pas |
| tout en RAM (impossible ici : 1,5 To) | 20 Go/s | 4,4 s | borne inférieure absolue |
| deux nœuds, dense résident, experts sur 2 NVMe | 20 + 4 Go/s | **2,4 + 6,2 = 8,6 s** | le découpage divise la partie routée |
| bus PCIe vers GPU (6,5 Go/s) | 6,5 Go/s | 13,4 s | déplacer les poids à chaque jeton |

**Aucune de ces lignes n'est interactive** — et c'est le vrai résultat : pour un
modèle de cette classe, **le placement ne suffit pas, il faut de la
réutilisation**. Un jeton ne touche que 16 experts sur 896 (1,8 %) : si les mêmes
experts reviennent d'un jeton à l'autre, un cache les sert depuis la RAM, et le
trafic réel s'effondre. C'est *la* mesure qui manque, et c'est le jalon M6.

## 3. Ce que ça impose, dans l'ordre

1. **La partie dense (62 Go) doit être résidente.** Elle est lue intégralement à
   chaque jeton : la laisser sur disque coûte 300 s/jeton à elle seule. Sur cette
   machine elle tient en RAM — mais **pas** en même temps que les 341 Go de
   V4.1-Flash et les 284 Go de Kimi-K2.7 : le choix de ce qui vit en cache est un
   arbitrage, pas une évidence.
2. **Les experts doivent être cachés, pas seulement streamés.** 24,7 Go/jeton à
   2 Go/s = 12 s ; le même trafic depuis la RAM = 1,2 s. La différence *est* la
   mesure de réutilisation.
3. **Le découpage en grappes divise la partie routée, pas la partie dense.**
   Deux nœuds = deux caches d'experts et deux NVMe, mais les 62 Go de dense sont
   dupliqués (ou l'un des nœuds les sert à l'autre — c'est alors un flux de
   coupure de 62 Go par jeton, ce qui est pire).
4. **La granularité fine paie ici pour une raison précise** : elle permet de
   *sauter* des tranches. Sur un flux de 62 Go, économiser 10 % vaut 2,4 s/jeton.

## 4. Ce que ce rapport corrige

- « Un jeton lit ~35 Go » (`docs/plan-kimi-k3.md`, `docs/architecture-kimi-k3.md`,
  bloc 28) → **87 Go**, dont 24,7 d'experts routés et 62,3 de dense.
- « 2,669 Go de poids par jeton » pour V4-Flash (`reports/rapport-gpu-tandem-nvlink.md`,
  `reports/rapport-granularite-flux.md`) → **8,56 Go** (experts 1,87 · partagé 0,80
  · attention + tête 5,89). Le chiffre de 2,669 Go reste juste **pour les experts
  seuls**, et c'est ainsi qu'il faut l'étiqueter.
- L'outil `tools/analyse_octets_par_jeton.py` garde son rôle (les experts) ;
  `tools/budget_execution_locale.py` donne le **total** et les placements. Les
  deux disent dans leur sortie ce qu'ils comptent et ce qu'ils ne comptent pas —
  c'est ce qui manquait.
