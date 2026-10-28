# N4.1 — génération avec `drave-n0` : cohérente 12 octets, puis du bruit

> **Objet.** Première usage visible : générer des octets depuis un prompt avec le student distillé
> (`/tmp/drave-n0-distille.pt`, PPL **3,295** sur le français).

## Dispositif

- Modèle : `drave-n0`, **11 469 192** paramètres, byte-level.
- Prompt : `La France est un pays`.
- Génération **greedy** (`temperature=0`), **160** octets, **déterministe**.
- Code : [`tools/generer_natif.py`](../tools/generer_natif.py).

## Sortie

```text
La France est un pays de la couche 1 (le plafond de la porte de la couche 0 et le plus grand (le plus grand que le contexte de latinesplaronsesexinuiteuxin-cloraratesenouxitetrnsons
```

## Lecture

- Les **12 premiers octets** sont cohérents : `La France est un pays`.
- Ensuite le modèle **dérive** : répétitions, mots inventés, ponctuation qui s'effondre.
- Ce n'est **pas** un assistant : c'est un modèle de **prochain octet** de 11,47 M, avec **3,295** de
  PPL sur le français, pas une alignement instruction.
- La génération est **déterministe** : même prompt, même sortie.

## Verdict

**N4.1 — première usage : atteint techniquement**, mais la **qualité** n'est pas celle d'un assistant.
La porte N4 (« chat utile ») est **très loin**.

## Limites

- **Greedy** seulement ; pas de top-k/température mesurés.
- **160 octets** ; la dérive apparaît vite.
- **Pas de cache KV** : chaque octet refait la passe avant.
- **Aucun alignement** instruction.

## Fichiers

- Code : [`tools/generer_natif.py`](../tools/generer_natif.py).
- JSON : [`native-generation.json`](native-generation.json).
