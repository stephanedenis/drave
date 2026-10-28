# Journal des décisions de la roadmap — 30/09 → 27/10

> **Ce que ce fichier est.** L'historique des décisions qui ont façonné la roadmap : le renommage,
> le recentrage sur les flots, les jeux symboliques, B10–B12 et la remise en cohérence documentaire.
> **Chargement :** journal — **ne pas charger par défaut** ; la roadmap courante est
> [`docs/roadmap.md`](../../docs/roadmap.md).

## Les décisions

- **30/09** — le renommage Qtrinet → Drave ; le moteur Rust *est* l'architecture par listes.
- **07/10** — la passe K3 est liée au **disque** (133 Mio/s, 87,6 % d'occupation) ; le levier est la taille du lot.
- **22/10** — le périmètre entrée-sortie est **arrêté au français inclus** ; l'étage 2 devient le chantier principal.
- **23/10** — la vision est **recentrée sur les flots** (ce document) ; les deux programmes avancent en parallèle.
- **24/10** — le **moteur** et l'**intelligence** sont poussés jusqu'où le matériel le permet : la passe complète
  est **45/47** (aucun rouge nouveau), la carte du raisonnement a **trois courbes complètes** et la sonde **sature dès
  le 1,5 B** ; le pic du 32 B et le 14 B l24 sont **bloqués par la VRAM** (le premier coûte 10-20 h ; le second a été
  mesuré depuis), la prose scientifique manque de **corpus**. Ce qui reste est **nommé**, pas oublié.
- **25/10** — les **jeux symboliques** : la **RSN-jeu** (112 items, **100 %** au niveau 4, **33/33** paires,
  **0 collision**) et la **logique** (perft échecs/dames, morpion exact, mats, politique des cartes) ; la **pensée**
  est invariante sur **5/5** jeux. Le MCTS du go est **faible à 60 playouts** (1/3) : négatif nommé, pas caché.
- **27/10** — **B10–B12** : protocole sémantique (encodeur **0,426** ; décodeur **négatif**), base typée
  (codec **100 %**, natif **59,8 / 40,7**, **surface 33/79**), modules cerveau-langage (M1 **528/528**, M2
  **98,6 / 93,2**, M8 **96,48 %**). La **documentation** est remise en cohérence (compteurs
  **49/8/172/241/52**, chemins archivés, revue étendue) : la théorie et l'état redescendent dans `docs/`.
