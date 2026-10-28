# N0.4 — GGUF ↔ DRVM : aller-retour identique au bit près

> **Objet.** DRVM est le format natif ; GGUF reste un **format d'import/export**. On convertit un
> vrai modèle Qwen2.5-0.5B Q4_0 (337 Mo, 290 tenseurs, tokenizer compris) en DRVM, puis on le
> reconvertit en GGUF.

## Résultats

| mesure | valeur |
|---|---:|
| tenseurs | **290** |
| bloc KV GGUF (tokenizer) | **5 931 951 o** |
| GGUF source | **337 Mo** |
| DRVM | **337 Mo** |
| **SHA-256 GGUF source** | `c8cd5f37…3d4919` |
| **SHA-256 GGUF retour** | `c8cd5f37…3d4919` |
| **identiques** | **oui, octet pour octet** |

## Lecture

- Le bloc de métadonnées GGUF (dont le tokenizer) est conservé **tel quel** dans un tenseur
  réservé `__gguf_kv` ; les 290 tenseurs sont copiés sans réencodage.
- L'aller-retour **GGUF → DRVM → GGUF** redonne **exactement le même fichier** : même SHA-256,
  même taille.
- Ce n'est pas une conversion de **sémantique** : DRVM ajoute un **graphe** et un **manifeste**,
  mais l'import GGUF reste un **blob** étiqueté `input`. La lecture native du graphe viendra avec
  N1/N2.

## Verdict

**N0.4 est atteint** : un GGUF réel se convertit en DRVM et revient **identique au bit près**. Le
format natif peut donc **importer** l'existant sans le perdre.

## Limites

- **Un seul modèle** (Qwen2.5-0.5B Q4_0).
- Le graphe DRVM d'un import GGUF est **un seul bloc `input`** : c'est un conteneur, pas encore
  une exécution native.
- **Pas de PPL** dans cette mesure : c'est une **fidélité d'octets**, pas une fidélité de calcul.

## Fichiers

- Code : [`tools/gguf_drvm.py`](../tools/gguf_drvm.py).
- Test : [`tools/cerveau/tests/test_gguf_drvm.py`](../tools/cerveau/tests/test_gguf_drvm.py).
- JSON : [`gguf-drvm.json`](gguf-drvm.json).
