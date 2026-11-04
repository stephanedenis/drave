# Plan de session — D, les données : les 8 `.PDF` restants

> **Mandat du 2026-11-04 15 h 25 HNE**, après la clôture de N3 dans la même session
> (`81fa1a86`, `39b7ef00`). La frontière du graphe est **A2.6, N2, N4** : tous GPU, et le
> claim `n2-jour` tient encore les deux cartes ; la passe du hub est due. La session prend
> donc la seule ligne **CPU** restante de « Ce qui reste » : la **limite nommée** de D.
>
> **Cycle précédent** : **N3 clos** — 17/17 portes vertes, inventaire exécutable, deux
> conditions nommées ([fiche](../../../reports/rapport-n3-inventaire.md)) ; intégré par le hub.

- **Session** : `aeafe951-9c3d-4bb5-8af7-0246a4f3d51d`
- **Rôle** : **D — les données** : clore la limite « 8 scans `.PDF`, 58 p » du fonds CEGEP —
  ceux que `rglob("*.pdf")` manquait parce que l'extension est en majuscules.
- **Périmètre** : OCR des 8 `.PDF` du fonds CEGEP, qualification au texte natif, déduplication,
  manifeste et fiche de résultat.
- **Fichiers réservés** : `reports/rapport-ocr-pdf-restants.md`,
  `reports/ocr-pdf-restants.json`, `work/ocr/restants*`, `tools/ocr_pdf.py` (lecture seule),
  `journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/`.
- **Heartbeat** : 2026-11-04 15:26 EST
- **Prochaine action** : **qualifier les 8 scans** parmi les 30 `.PDF` (texte natif
  < 50 car/page), les OCRiser avec la liste explicite, puis mesurer et écrire la fiche.
- **État** : actif
- **Plan** : 1) plan + claim cpu1 ; 2) détection sur le texte intégral (contrôle : un `.PDF`
  natif doit être exclu) ; 3) OCR `--liste` (8 ouvriers) ; 4) dédup + 8 Ko + manifeste ;
  5) fiche + JSON ; 6) ligne d'état proposée au hub, commit explicite.
- **Ambition** : que la dernière limite nommée de D soit **mesurée**, pas reprise de mémoire —
  le parcours insensible à la casse est un défaut d'inventaire, pas une fatalité.
- **Stratégie** : la qualification précède l'OCR (aucun scan supposé) ; le contrôle négatif
  est un `.PDF` **natif** qui doit rester hors liste et une **paire de doublons** qui doit
  donner le même texte ; les chiffres viennent du manifeste, pas du récit.
- **Objectif final** : 8 scans qualifiés, OCRisés, dédupliqués, mesurés (pages, caractères,
  8 Ko, temps), fiche et JSON ; la ligne de D close dans l'état par le hub.
