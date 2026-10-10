> Campagne : **campagne-benefices** · expérience **02**
> Titre : 2. Les deux familles de tâches que Drave ne couvre pas
> Date réelle : **2026-10-08 21:32 HAE** (source : commit `89ae2c3`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 2. Les deux familles de tâches que Drave ne couvre pas

Constatées, et consignées comme manques — pas comme résultats :

| famille | état | ce qui manque |
|---|---|---|
| **embeddings / recherche** | `bge-m3` (BERT, 24 couches, vocab 250 002) est **lisible en en-tête** mais **inexécutable** | le moteur exige `blk.0.attn_norm.weight` et une attention causale ; il n'a ni encodeur bidirectionnel ni pooling |
| **décodage spéculatif** | `eagle3-gpt-oss-120b` (0,84 Go, 1 couche) présent sur le disque | aucune notion de brouillon dans le moteur (`grep eagle brouillon specul` = 0) — et la mesure par le moteur (§ 1 bis) ajoute une condition que le code ne peut pas lever : **le brouillon doit partager le post-entraînement de sa cible**, sinon il n'accepte rien (0,88 jeton sur 8). Le chantier commence par un entraînement, pas par une option |

Ce sont les deux seules familles demandées par un usage courant qui manquent au
relevé : tout le reste (langage, génération, contexte long, code, raisonnement,
MoE, multilingue, lots, gros-modèle-sur-petite-machine) est couvert.

---
