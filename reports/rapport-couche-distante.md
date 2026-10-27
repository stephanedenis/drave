# A7.6 — une couche exécutée à distance : logits identiques au bit près

> **Objet.** A7.5 transportait la grappe sparse. A7.6 exécute **une couche réelle** (Qwen2.5-0.5B,
> couche 12) dans un **second processus** TCP, le client gardant le reste du modèle, et compare
> **logits**, **perplexité** et **coût réseau**.

## Dispositif

- **Qwen2.5-0.5B-Instruct**, 24 couches, hidden **896**, vocab **151 936**.
- Couche **12** retirée du client et chargée seule côté serveur (14,9 M paramètres).
- Client : embeddings, couches 0–11, couches 13–23, norme, `lm_head`.
- Transport **TCP loopback**, en-tête 38 o, hidden + positions + cos/sin ; **dense** et **sparse**.
- 3 invites, 2 répétitions ; GPU 0, fp32, `sdpa`.

## Fidélité

| mesure | valeur |
|---|---:|
| bits identiques | **3 / 3 invites** |
| ΔPPL corpus | **+0** (7,162066 local et distant) |
| argmax identique | **1,0** |
| top-1024 identique | **1,0** |
| KL moyenne | **0,0** |

## Coût

| mesure | valeur |
|---|---:|
| RTT couche médian | **4,052 ms** |
| calcul serveur médian | 2,584 ms |
| forward complet médian | 51,665 ms |
| ping loopback | 0,150 ms |
| octets par jeton | **4 105 o** |
| débit | **3 987,6 jetons/s** |
| mémoire client libérée | **56,9 Mio** |

## Le négatif du sparse

Le hidden state réel est **dense** : `taux_zeros = 0`. Le masque sparse coûte donc **1 bit par
valeur** sans rien économiser. Résultat : **sparse/dense = 1,027×**, c'est-à-dire **2,7 % plus
cher**. Le gain de A7.5 venait du flux **synthétique à 20 % de zéros** ; il **ne se reproduit pas**
sur la couche réelle.

## Contrôles négatifs

- **RoPE mise à zéro** : logits **diff max 5,08**, argmax **0,90**, PPL **+0,35** — la position est
  bien nécessaire.
- **Serveur CPU fp32** et **bfloat16** : non exécutés dans cette passe (`--sans-negatifs`).

## Verdict

**A7.6 est mesuré** : une couche réelle peut être exécutée dans un second processus avec des
**logits identiques au bit près**, à **4,05 ms** de RTT et **4 105 o/jeton**. Le **sparse** n'aide
pas sur un hidden dense ; il faut le **compresseur** (quantification, top-k) avant le transport.

## Limites

- **Une seule couche**, préfill, batch 1, **pas de cache KV**.
- Serveur et client sur le **même GPU** (loopback) : ce n'est pas un WAN.
- Pas de **gain de vitesse** : le forward complet reste à 51,7 ms ; le coût est le transport.
- Les négatifs CPU/bfloat16/eager ne sont pas dans ce JSON (`--sans-negatifs`).

## Fichiers

- Code : [`tools/couche_distante.py`](../tools/couche_distante.py).
- JSON : [`couche-distante.json`](couche-distante.json).
