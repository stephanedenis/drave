# N4.5 — le meilleur student derrière le service natif

> **Objet.** Servir le **meilleur** `drave-n0` (PPL validation **2,708**, N2.19) et vérifier que le
> moteur natif le lit, le génère et le sert.

## Résultat

| mesure | valeur |
|---|---:|
| PPL validation | **2,708** |
| PPL native 1 076 octets | **45,2822** |
| PPL Python 1 076 octets | **45,2765** |
| latence service 53 octets | **589,2 ms** |
| texte | `La France est un payse de reprise — et c'est un cha` |

- DRVM : `/tmp/n0-best.drvm`, exporté depuis `/tmp/drave-n0-prof20k-5.pt`.
- CLI : `drave --drvm-serve /tmp/n0-best.drvm 8768`.
- Vérification : `curl -X POST /generer?n=32`.

## Lecture

- Le **meilleur** student est **exécutable** et **servi** par le moteur Rust.
- La PPL native de 1 076 octets est **45,28**, très au-dessus de la validation **2,708** : c'est
  toujours un texte **sans contexte**, pas la même mesure.
- Le texte généré est **moins absurde** que celui du student 3,58 : `payse de reprise — et c'est un cha`.
- **589 ms** pour 53 octets, cohérent avec N4.3.

## Verdict

**N4.5 — meilleur student servi** : PPL validation **2,708**, service **589 ms**, texte encore faux
mais plus structuré.

## Limites

- **Pas un assistant** : `payse` au lieu de `pays`.
- **PPL native de 1 076 octets** non comparable à la validation.
- **Mono-thread**, sans auth.
- **Un seul prompt**.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-best-service.json`](native-best-service.json).
