# Thèmes du journal

> Généré par `tools/journal_auto.py` — c'est la **règle de classement** des fichiers
> `journal/AAAA-MM-JJ_<thème>.md`. Un commit (ou une étape de session) est classé par
> le **premier** thème dont un mot-clé apparaît dans son texte ; à défaut, par les
> **chemins** touchés ; à défaut, en `divers`. Pour changer le classement, éditer la
> table `THEMES` du script et relancer : rien d'autre n'est à toucher.

| thème | ce qu'il couvre | mots-clés | chemins |
|---|---|---|---|
| `attention` | Attention, fenêtre, puits | attention, fenêtre, fenetre, puits, sinks, attn-, softmax, swa, kv | model.rs |
| `memoire` | Mémoire épisodique, consolidation, greffe | mémoire, memoire, épisodique, episodique, greffe, consolid, rappel, indice, magasin, c6, c7, clé, cle | episodique.rs |
| `distribue` | Régions, flux, protocoles, budgets, pannes | topologie, région, region, nœud, noeud, flux, bus, latence, budget, panne, registre, trace, protocole, v7, v8, paires, message, gigue, réparti, reparti, relais, découpage, decoupage, lien | topologie.rs, trace_globale.rs, bus.rs, flux.rs |
| `modele` | Modèles, entraînement, parcimonie, biologie | modèle, modele, entraîn, entrain, distill, parcimonie, poids, échelle, echelle, biolog, e1, e2, e3, e4, e5, e6, e7, e8, e9, log-normal | entrainer_moteur.py, biologie |
| `moteur` | Moteur : chargement, calcul, listes, quantification | moteur, gguf, listes, quantif, noyau, gpu, threads, mmap, lots, profil, débit, debit | gguf.rs, model.rs, main.rs |
| `mesures` | Campagnes et mesures | campagne, mesure, perplexité, perplexite, carte, banc, benchmark, aiguille | reports/ |
| `portes` | Portes et vérifications | porte, portes, vérification, verification, tests, gate | tools/porte-, toutes-les-portes |
| `docs` | Documentation, état, conventions | document, doc, readme, glossaire, rangement, convention, état, etat, journal, organisation, manques | docs/, README.md |
| `outils` | Outils et harnais | outil, script, harnais, hook, générateur, generateur | tools/ |
| `divers` | Ce qui ne rentre dans aucun thème | — | — |
