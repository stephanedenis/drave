# Le corpus v2 est promu et épinglé : 6,90 Go dans `data/`, manifeste `9861fb39…`

> **Ligne de roadmap** : N (le palier 1) / D · **Date** : 2026-11-18 · **Verdict** : ✅ le corpus
> dédupliqué par ligne entre dans `data/` : `data/wiki_mix_v2/train.txt`, **6 900 585 097 o**
> (6,43 Gio), **63 438 199 lignes**, sha256 **`e3112a84…`**, manifeste d'épingle **`9861fb39…`**.
> La validation reste **`data/wiki_mix/propre/val.txt`** (`fbddef91…`, l'épingle v1) : c'est elle qui
> rend les deux corpus comparables.
>
> **Dispositif** : `tools/dedup_lignes.py` (8,042 % des octets retirés, 161 s, idempotent) →
> `work/dedup/train-lignes.txt` → copie dans `data/wiki_mix_v2/` → `tools/epingle_corpus.py`.

## L'épingle

| fichier | sha256 | octets | lignes |
|---|---|---:|---:|
| `data/wiki_mix_v2/train.txt` | `e3112a84…` | 6 900 585 097 | 63 438 199 |
| `data/wiki_mix/propre/val.txt` (validation) | `fbddef91…` | 10 330 112 | 24 498 |

Manifeste : [`corpus-epingle-v2.json`](corpus-epingle-v2.json) (`9861fb39…`). Le `--verifie` de
l'outil recalcule les empreintes en ~30 s (6,9 Go).

## Ce que ce corpus est, et n'est pas

- **Est** : les 7,50 Go de `data/corpus_wiki_fr_texte/` **moins** les 8,042 % d'octets dupliqués
  (28,005 % des lignes), les lignes vides préservées ; 2,15 M d'articles Wikipédia FR, CC-BY-SA.
- **N'est pas** : plus divers que v1 — **~98 % Wikipédia** ; l'écart de **diversité** (livres FR)
  reste ouvert, et c'est lui que le palier 1 doit fermer, pas le volume.
- **Ne remplace pas** v1 : les deux corpus vivent côte à côte, v1 (1,017 Go) pour la comparabilité
  historique, v2 (6,90 Go) pour le palier 1.

## Le contrôle

- **Idempotence** mesurée : la 2ᵉ passe sur la sortie écarte **0 ligne** et rend le même sha256.
- **La copie est vérifiée** par l'épingle (recalcul du sha256 sur les 6,9 Go).
- **Le chargeur a été réparé** pour tenir 6,9 Go en mémoire bornée : `torch.frombuffer` (uint8)
  au lieu de `torch.tensor(list(b))` — contrôle : la PPL du checkpoint r4 sur le val épinglé rend
  **3,0628**, exactement la valeur enregistrée dans `r4.pt.json` (bit-identique sur le chemin des
  données).

## Ce qui pourrait le rendre faux

- **Le corpus v2 n'a pas de validation propre** : la PPL se mesure sur le val de v1, qui appartient
  au même univers (Wikipédia) — la comparaison v1/v2 est fair, la généralisation hors Wikipédia non.
- **La déduplication par ligne ne voit pas** les quasi-doublons (un mot changé, un reflow) ni les
  collisions 64 bits (~4,4 × 10⁻⁵ attendues).
- **Le tri éditorial n'est pas fait** : les lignes courtes (80 o et +) pèsent 2,59 % du fichier.

## Ce que ça change

Le palier 1 a sa donnée : **6,90 Go épinglés**, chargeables sans exploser la mémoire. Les deux runs
de la nuit (150 M sur v2 et sur v1, à pas égal) diront si le corpus plus grand paie — c'est le
premier test du plan « la donnée d'abord » avec un corpus de taille palier.

## Voir aussi

- [le dédup par ligne](rapport-dedup-lignes.md) · [l'épingle v1](rapport-corpus-epingle.md) ·
  [les données](rapport-donnees-inventaire.md) · [le manifeste](corpus-epingle-v2.json)
