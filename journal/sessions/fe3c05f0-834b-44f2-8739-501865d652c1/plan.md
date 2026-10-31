# Plan de session — R4.4, l'OCR et sa parité

> **Mandat ouvert** le 2026-10-31 18 h 00 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) — le heartbeat est celui de
> l'état ; la session le met à jour à chaque cycle.

- **Session** : `fe3c05f0-834b-44f2-8739-501865d652c1`
- **Rôle** : **R4.4, l'OCR et sa parité** — **sans GPU**, les deux GPU étant réservés par N2.
- **Périmètre** : R4.4 — l'encodeur visuel : installer l'OCR sans root, le brancher sur le graphe
  R0.1 (mêmes régions, mêmes offsets, confiance dans la provenance), mesurer le **WER**, la
  **parité** des réponses et les **contrôles négatifs** sur 10 pages. Ne pas toucher à N2 :
  `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`, ni lancer `toutes-les-portes.sh`.
- **Fichiers réservés** : `work/ocr/`, `tools/installer_ocr.sh`, `tools/graphe_document_ocr.py`,
  `tools/mesurer_ocr.py`, `tools/porte-ocr.sh`, `reports/r44-*`,
  `docs/implantation/encodeur-visuel.md`, `journal/sessions/fe3c05f0-…/`.
- **Heartbeat** : 2026-10-31 18:00
- **Prochaine action** : la fiche, le journal, la roadmap, le commit — puis les **scans réels**.
- **État** : en cours
