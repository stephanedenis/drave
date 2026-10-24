# A7.4 — la grappe déportée : le flux ne transporte plus les zéros

> Mesure du 24/10/2026. Le format du relais (`K3RL`) passe en **version 2** : un **masque** d'un bit par canal + les
> valeurs non nulles, au lieu d'un `f32` par canal (`Relais`, `drave-core/src/kimi_k3.rs`).

## Les résultats

| | |
|---|---:|
| le flux **dense** (v1), 4 jetons × 448 canaux | **7 196 o** |
| **le flux de la grappe (v2)**, ~20 % de non-nuls | **1 704 o** |
| le rapport | **4,22× moins** |

**La porte du flux rend les mêmes chiffres** : le mode 3 (lot dense `f32`) donne **60,8135 / 60,8135** — exactement la
référence d'avant le format v2. Le transport ne paie plus les zéros, et le calcul ne change pas d'un chiffre.

## Ce que ça dit

- **La grappe déportée est mesurée** : le flux de la grappe coûte **4,22× moins** que le flux plein, et la sortie est
  **identique** (le round-trip du test est exact, la porte du flux rend 60,8135).
- **La version 1 reste lisible** : le format ne casse pas les fichiers existants — `lire` lit les deux versions.
- **Le coût est dans les zéros** : la v2 paie 1 bit + 4 octets par canal non nul — les 79 % de zéros ne coûtent plus
  que 1/32 de leur ancien prix.

## Ce que ça ne dit pas

- Le test synthétique a **20 %** de non-nuls ; la vraie grappe en a **21 %** (A7.3) — le ratio réel sera du même ordre,
  pas identique.
- Le gain **réseau** réel (la latence, la bande passante) n'est pas mesuré : c'est le **volume** qui l'est.
- La `pile` (le cache KV) reste **dense** dans le format : c'est le flux d'**activations** que la v2 allège.
