# A7.5 — la grappe sur le réseau : fidélité exacte, 4,44× moins d'octets

> **Objet.** A7.4 mesurait le **volume** du flux sparse (masque + valeurs). A7.5 le **transporte**
> entre deux processus par TCP loopback, vérifie la **fidélité**, et mesure la **latence**.

## Dispositif

- Flux synthétique **4 jetons × 448 canaux**, **356 non-nuls** (19,9 %).
- Format **K3RL v2** : masque **par jeton**, 1 bit par canal, puis les valeurs `f32`.
- Contrôle **dense** : masque plein, toutes les valeurs.
- Deux processus, **TCP 127.0.0.1**, **5 essais** ; le serveur renvoie `OK`.

## Résultats

| mesure | valeur |
|---|---:|
| flux dense | **7 416 o** |
| flux sparse | **1 672 o** |
| rapport | **4,44×** |
| fidélité (cases exactes) | **1 792 / 1 792 = 100 %** |
| réseau, messages identiques | **5 / 5** |
| latence loopback moyenne | **0,125 ms** |
| latence min / max | 0,073 / 0,186 ms |

## Lecture

- Le flux sparse **passe le réseau sans perte** : les 1 792 cases sont reconstruites, y compris
  les zéros.
- Le **volume** est **4,44×** plus faible que le dense ; c'est du même ordre que le **4,22×**
  d'A7.4 (20 % de non-nuls).
- La **latence loopback** est de **0,125 ms** : elle mesure le **transport local**, pas un WAN.
- Le **coût réseau** est donc dominé par les **octets**, pas par le protocole.

## Ce que ça ne dit pas

- **Loopback** seulement : la latence **WAN** n'est pas mesurée.
- Pas de **modèle** derrière le flux : c'est un transport de **forme**, pas une couche exécutée à
  distance.
- Le **masque par jeton** coûte `ntok × h` bits ; le format A7.4 utilisait un masque par canal.
- Le gain dépend du taux de non-nuls : à 100 %, le sparse est **plus cher** que le dense.

## Verdict

**A7.5 est mesuré** : le flux sparse traverse le réseau **sans perte**, à **4,44× moins d'octets**
et **0,125 ms** de latence loopback. C'est le **transport** de la grappe ; l'exécution d'une couche
distante reste un chantier distinct.

## Fichiers

- Code : [`tools/grappe_reseau.py`](../tools/grappe_reseau.py).
- Test : [`tools/cerveau/tests/test_grappe_reseau.py`](../tools/cerveau/tests/test_grappe_reseau.py).
- JSON : [`grappe-reseau.json`](grappe-reseau.json).
