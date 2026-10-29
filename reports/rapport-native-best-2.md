# N0.15/N4.7 — le meilleur 2,6998, servi par le moteur natif

> **Objet.** Exporter le nouveau meilleur `drave-n0` (**PPL 2,6998**, contexte 129) en DRVM, vérifier
> la parité native et remplacer le modèle du service.

## Résultat

| mesure | valeur |
|---|---:|
| paramètres | **11 814 792** |
| PPL validation | **2,6998** |
| PPL native 1 996 octets | **54,1350** |
| PPL Python 1 997 octets | **54,1327** |
| écart | **0,0023** |
| latence service 53 octets | **650,1 ms** |
| texte | `La France est un pays de travail de route et le contr` |

- DRVM : `/tmp/n0-ctx129.drvm`, SHA `ac5149…`.
- CLI : `drave --drvm-serve /tmp/n0-ctx129.drvm 8769`.
- Top-5 natif **identique** à Python : espace 6,8601 ; `e` 6,3866 ; `.` 5,4702 ; `\n` 5,2625 ; `o` 4,6627.

## Lecture

- Le **meilleur** student est **exécutable** et **servi** par le moteur Rust.
- La parité des logits est **exacte** ; la PPL native de 1 996 octets diffère de **0,0023** (f32).
- Le texte est **plus cohérent** que les précédents : `La France est un pays de travail de route…`,
  au lieu de `payse de contenu de la couche 8`.
- **650 ms** pour 53 octets : le service paie le cache par requête, pas la qualité.

## Verdict

**N0.15/N4.7 — meilleur student servi** : PPL **2,6998**, parité native, **650 ms**, texte plus
structuré mais encore faux.

## Limites

- **Pas un assistant** : `La France est un pays de travail de route` reste incorrect.
- **PPL native 1 996 octets** non comparable à la validation.
- **Mono-thread**, sans auth par défaut, sans cache persistant.
- **Un seul prompt**.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-best-2.json`](native-best-2.json).
