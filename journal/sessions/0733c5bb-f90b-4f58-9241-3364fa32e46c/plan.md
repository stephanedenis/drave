# Plan de session — N2, le natif : 200 000 pas et la fenêtre

> **Mandat ouvert** le 2026-11-02 16 h 20 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ N2) —
> la session reprend le programme **N2** (le natif, GPU) après la clôture de `0b0a6a0d`.
> Le heartbeat est celui de l'état.

- **Session** : `0733c5bb-f90b-4f58-9241-3364fa32e46c`
- **Rôle** : **N2 — le natif, GPU** : le compute sur le mélange 1 Go, puis la fenêtre
  native (R1.1/R1.2 côté N2), les fiches et les contrôles négatifs.
- **Périmètre** : N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2,
  courbe de longueur), R1.1/R1.2 mesurés depuis N2
- **Fichiers réservés** : `data/`, `tools/corpus*`, `reports/n2-*`, `reports/rapport-n2-*`,
  `work/n2*`, `journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/`
- **Heartbeat** : 2026-11-02 18:50 HAE
- **Objectif final** : trancher la question ouverte de N2 — **les 200 000 pas sur le mélange
  1 Go font-ils passer sous 2,5 sans perdre le français ?** — puis **R1.1/R1.2** : un schéma
  de position **relatif** reproduit-il par construction le gain des positions aléatoires, et
  la courbe 129→512 devient-elle plate à coût de domaine nul ?
- **Ambition** : que le programme N cesse de demander « plus de texte ? » et réponde
  « plus de pas, quelle architecture de position, quelle fenêtre » — chaque réponse portée par
  une mesure, un contrôle négatif et une fiche.
- **Stratégie** : 1) lancer les 200 k pas à recette constante (34,3 M, canal, positions
  aléatoires) sur `data/wiki_mix` et laisser tourner ; 2) pendant le run, préparer le banc
  R1.1/R1.2 (positions relatives) sur le second GPU ; 3) mesurer à budget constant, contrôle
  par permutation et courbe de longueur joints ; 4) fiche + JSON + état + commit explicite.
- **Reprise** : `0b0a6a0d` a clos N2.ac (3,4902 / 6,0283 / 8,3352 / 9,0525) ; la note de
  passage [`rapport-n2-fenetre-r1`](../../../reports/rapport-n2-fenetre-r1.md) fixe ce que
  R1.1/R1.2 doivent tester. Rien à rouvrir de N2.aa — le corpus n'est pas le levier.
- **Ce qui tourne** : les **200 000 pas** sur `data/wiki_mix/propre` (GPU 0, `work/n2ac/mix-200k.log`,
  ~57 ms/pas, fin attendue 19 h 30) ; le banc **R1.1/R1.2** (RoPE) sur le GPU 1 — R1.1 mesurée
  (3,2545 à 1 000 octets, 0,97× la PPL à 129), R1.2 à octets constants (3,0107, −0,24) ; reste le
  contrôle « depuis zéro » (initialisation figée, deux schémas).
- **Prochaine action** : la mesure des cinq PPL du run de 200 k à sa sortie, puis fiche + état +
  commit ; le contrôle depuis zéro ; la clôture.
- **État** : actif
