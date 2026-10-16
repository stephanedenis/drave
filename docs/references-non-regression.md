> **2026-10-11 06 h 30 HAE** (heure lue sur la machine). Ces valeurs sont les **verdicts imprimés
> par la passe complète des portes** (`tools/toutes-les-portes.sh`, **34 vertes sur
> 34**, 85 min 8 s). Elles ne sont pas recopiées de mémoire : elles sortent du journal de la
> passe. **Une modification du chemin d'exécution qui déplace l'un de ces chiffres a changé le
> calcul** — il faut alors relancer la porte, comprendre, et écrire à côté de l'ancienne valeur
> (jamais à sa place).
>
> Détail complet : `reports/rapport-passe-complete-portes.md`.
> Les mesures de campagne (perplexités, budgets, latences) sont dans `reports/` — une fiche par
> expérience — et non ici : ce fichier ne porte que ce qu'une **porte** vérifie.
>
> **Passe du 2026-10-12 à 23 h 00** (**36 portes, 34 vertes, 2 rouges**, ~74 min) : les valeurs
> ci-dessous **n'ont pas bougé** — les changements de la nuit (prélecture parallèle, lecture
> séquentielle dans nos tampons, chargement paresseux) ne déplacent aucun chiffre, et
> `porte-flux.sh` l'a vérifié après chacun. Les **deux rouges sont nommés et instruits** :
> `porte-indice` et `porte-melange` lisent une botte de foin **régénérée** (celle de la campagne
> n'a jamais été versionnée, `tools/niah_4096_0.5.txt` l'est désormais). Leur critère — un indice
> extérieur qui tombe plus près de l'aiguille que le hasard — **ne survit pas à la
> reconstruction** : mesuré sur **cinq fenêtres** du même corpus, **deux passent** (1,21× et 1,69×
> mieux que le hasard) et **trois échouent** (jusqu'à 2,13× pire). Détail et recommandations :
> [`reports/rapport-niah-fragilite.md`](../reports/rapport-niah-fragilite.md) — le critère est
> marginal par construction, et ces deux rouges ne disent **rien** de l'état du moteur.
>
> **Passe du 2026-10-15 à 22 h 40** (**46 portes, 44 vertes, 2 rouges**, ~96 min) — **la première
> passe à 46 portes** : `porte-homeostasie` (E9 : ×0 rend le modèle, l'activité est monotone,
> la dominance de ×0,6 est reproduite) entre dans la passe, et `porte-vision` y vérifie ses
> **deux** nouvelles étapes (couches 1, 15 et 31 **en isolation** à 6,3e-06, et le
> **projecteur** à 0,71 %). Les deux rouges restent les structurels (`porte-indice`,
> `porte-melange`), et **aucune valeur de porte n'a bougé**.
>
> **Passe du 2026-10-15 à 18 h 20** (**45 portes, 43 vertes, 2 rouges**, ~92 min) — **la première
> passe où `porte-vision` vérifie les DEUX nouvelles étapes** : les couches 1, 15 et 31 **en
> isolation** (6,3e-06) et le **projecteur** (0,71 %). Les deux rouges restent les structurels
> (`porte-indice`, `porte-melange`).
>
> **Passe du 2026-10-15 à 16 h 19** (**45 portes, 43 vertes, 2 rouges**, ~86 min) : les deux rouges
> sont les structurels, et `porte-vision` y est verte (étapes 1 à 5). L'étape 6 — le **projecteur**
> — a été ajoutée **après** cette passe et elle est verte au premier passage (**0,71 %**, la
> quantification) : la porte vérifie maintenant les **couches profondes en isolation** (6,3e-06)
> ET le projecteur.
>
> **Passe du 2026-10-15 à 11 h 21** (**45 portes, 43 vertes, 2 rouges**, ~80 min) — **la 45ᵉ porte
> (`porte-vision`) y est verte du premier coup** : elle vérifie le **refus** d'un modèle sans tour
> de vision, les **formes** du modèle (256 × 1280 et 64 × 1536) et **mesure** la tour **sans la
> juger** — en **disant** que l'embedding de patchs n'a **pas** pu être comparé (la référence
> numpy n'accepte que l'image 28 × 28 et ses attentes de format ont dérivé). Les deux rouges
> restent les structurels (`porte-indice`, `porte-melange`), et **aucune valeur de porte n'a
> bougé**.
>
> **Passe du 2026-10-15 à 09 h 38** (**44 portes, 42 vertes, 2 rouges** *après correction*,
> ~70 min) : après les changements de moteur pour la **vision** (MLP à deux matrices, fenêtre
> locale conditionnelle, biais des LayerNorm, écriture des jetons d'image, `DRAVE_VISION_COUCHES`).
> **Un troisième rouge est apparu, et il était de MA faute** : `porte-tableaux` refusait un tableau
> de `reports/rapport-sommeil-selection.md` (séparateur à **6** cellules pour un en-tête à **5**) —
> corrigé dans la minute, porte repassée **verte** (`✅ 460 fichier(s)`). **Le piège, et il est noté
> ici : j'avais lancé la porte en la pipant dans `tail`, et je lisais « 460 fichier(s) examiné(s) »
> comme un succès — c'était la ligne qui SUIT l'échec, et le code de sortie était celui de `tail`.**
> Une porte ne se lit pas par sa dernière ligne, ni à travers un tuyau.
>
> **Passe du 2026-10-15 à 06 h 27** (**44 portes, 42 vertes, 2 rouges**, ~75 min) — **le meilleur
> état du dépôt** : après la correction de **reproductibilité du harnais** (la graine était posée
> après le tirage des LoRA : deux exécutions identiques rendent maintenant le même nombre **au bit
> près**). `porte-prechargement`, qui avait rendu un rouge d'**instabilité** à 04 h 30, est **verte**
> en passe complète avec ses **trois** répétitions (tampons 10,60 s contre fils 11,55 s).
> `porte-consolidation` et `porte-speculatif` sont vertes aussi. Il ne reste que **les deux rouges
> structurels** (`porte-indice` : 482 contre 459 pour le témoin ; `porte-melange` : l'état de A ne
> rend pas le code).
>
> **Passe du 2026-10-15 à 04 h 30** (**44 portes, 41 vertes, 3 rouges**, ~74 min) : la 44ᵉ porte
> (`porte-speculatif`, l'invariant du décodage spéculatif) y est **verte du premier coup** (8 jetons
> identiques au cerveau seul, témoin à 0 %, réflexe distillé ratifié à 30,0 %). Les deux rouges
> structurels sont les mêmes (`porte-indice`, `porte-melange`). **Le troisième rouge était une
> INSTABILITÉ de mesure, et elle est corrigée** : `porte-prechargement` a rendu « tampons plus
> lents que fils » (12,48 s contre 10,95 s) pendant la passe, puis **PORTE TENUE relancée seule**
> (10,45 s contre 13,06 s, puis 10,36 s contre 11,15 s). La cause est nommée : la comparaison
> porte sur la **médiane de DEUX** répétitions, donc un seul chargement lent (cache de pages
> écrasé par 44 portes qui lisent des modèles) décide — le second échantillon des tampons était
> le plus rapide des quatre. La porte prend maintenant **trois** répétitions (la médiane est le
> point du milieu) et elle est repassée **verte**. Ce n'est pas la porte qui a été affaiblie,
> c'est la mesure qui a été renforcée.
>
> **Passe du 2026-10-15 à 02 h 20** (**43 portes, 41 vertes, 2 rouges**, ~70 min) : après les
> outils de la nuit (distillation E5, `--lora-depart`, fusion **sommaire** de plusieurs LoRA,
> cible de changement, `politique-budget.sh`). Les deux rouges sont **les mêmes** (`porte-indice` :
> 482 contre 459 pour le témoin ; `porte-melange` : l'état de A ne rend pas le code) et **aucune
> valeur de porte n'a bougé** (`porte-flux` : 61,9920 / 60,8135).
>
> **Passe du 2026-10-15 à 00 h 01** (**43 portes, 41 vertes, 2 rouges**, ~64 min) : après la
> **nuit du cerveau** (C2, C7, N5, E5, la boucle complète). Les **trois nouvelles portes** y sont
> vertes : `porte-cerveau` (les quatre facultés **composent** : chacune agit encore quand les
> autres sont allumées, quatre sorties distinctes, déterminisme au bit près), `porte-consolidation`
> (LoRA nul ⇒ GGUF identique au bit) et `porte-cycle-c2` (chaîne de régions exacte 0,00e0, pas 1
> exact, borné, coût dit, déterministe). Les deux rouges sont **les mêmes** (`porte-indice` : 482
> contre 459 pour le témoin ; `porte-melange` : l'état de A ne rend pas le code), et **aucune valeur
> de porte n'a bougé** (`porte-flux` : 61,9920 / 60,8135).
>
> **Passe du 2026-10-14 à 21 h 43** (**42 portes, 40 vertes, 2 rouges**, ~64 min) : après le **cycle C2**
> (validateur qui accepte un cycle si un lien est `recurrent` et retardé ; pilote `tools/derouler.py` ;
> capture d'état sur un nœud intermédiaire) et la **consolidation** (LoRA fusionné, `porte-consolidation`).
> Les deux nouvelles portes y sont **vertes** : `porte-cycle-c2` (chaîne de régions exacte 0,00e0, pas 1
> exact, borné, coût dit, trajectoire déterministe) et `porte-consolidation` (LoRA nul ⇒ GGUF identique
> au bit, aléatoire ⇒ visible, lecteur ⇒ hors fichier). Les deux rouges sont les mêmes qu'avant
> (`porte-indice` : 482 contre 459 pour le témoin ; `porte-melange` : l'état de A ne rend pas le code).
> **Aucune valeur de porte n'a bougé** (`porte-flux` : 61,9920 / 60,8135).
>
> **Passe du 2026-10-14 à 14 h 55** (**40 portes, 38 vertes, 2 rouges**, ~75 min) : après la
> **porte d'exécution de N4** (le moteur applique un adaptateur de sortie appris :
> `--adaptateur-sortie`, quatre fins de plage ; et `tools/exporter_gguf_dense.py` écrit un GGUF
> dense Qwen2). Les deux rouges sont **les mêmes qu'avant**, avec la même cause structurelle
> (`porte-indice` : l'indice extérieur tombe à 482 jetons contre 459 pour le témoin ; `porte-melange`
> : l'état de A ne rend pas le code de A). **Aucune valeur de porte n'a bougé** — `porte-flux`
> rend ses cinq modes aux références (61,9920 / 60,8135). La **40ᵉ porte** y est verte du premier
> coup (`porte-adaptateur-sortie`, 58 s) : elle vérifie que le fichier réécrit rend **les mêmes
> chiffres** (7,4242 et 4 481 378,8799), que l'adaptateur = identité ne change **rien** (0,00e0),
> qu'une demi-échelle — que la norme ne peut pas absorber — **change** le chiffre (×2,9), et que
> les trois cas invalides rendent **code 2**. Fiche :
> [`reports/rapport-n4-porte-execution.md`](../reports/rapport-n4-porte-execution.md).
>
> **Passe du 2026-10-13 à 13 h 44** (**39 portes, 37 vertes, 2 rouges**, ~82 min) : après l'échange
> d'experts (C9) et le **nouveau critère** de `porte-indice` (contrôle apparié). Les deux rouges
> sont les mêmes qu'avant, mais celui de `porte-indice` a **changé de cause** : il ne dit plus
> « moins bien que le hasard » mais « pas mieux que le **témoin** » — une comparaison qui ne dépend
> plus du texte. `porte-echange-experts` et `porte-tableaux` y sont **vertes**.
>
> **Porte ajoutée le 2026-10-13 à 13 h 20** : `porte-echange-experts.sh` (le routage imposé est
> inerte par défaut, **exact** sur son propre routage — l'invariant qui fonde toute la mesure C9 —
> et vivant sur un routage étranger). Vue **rouge** en retirant `DRAVE_TRACE_EXPERTS_ORDRE=1`
> (54,4883 contre 54,5202). Fiche :
> [`reports/rapport-c9-echange-experts.md`](../reports/rapport-c9-echange-experts.md). Elle n'était
> pas encore dans une passe complète au moment de ce relevé.
>
> **Porte ajoutée le 2026-10-13 à 08 h 40** : `porte-tableaux.sh` (vérifie que chaque tableau
> Markdown du dépôt a le même nombre de cellules partout — une seule ligne fautive fait rendre tout
> le tableau comme du texte, et le texte reste visible, donc le défaut est muet). Vue **rouge** sur
> deux défauts volontaires. Fiche :
> [`reports/rapport-tableaux-casses.md`](../reports/rapport-tableaux-casses.md). Elle n'était pas
> encore dans une passe complète au moment de ce relevé.
>
> **Passe du 2026-10-13 à 06 h 19** (**37 portes, 35 vertes, 2 rouges**, ~71 min) : après le **pool
> des tampons de lecture** (seul changement moteur depuis la précédente). Mêmes deux rouges, mêmes
> valeurs ; `porte-prechargement` et `porte-push-paresseux` vertes. Le pool est **neutre en temps**
> — c'est mesuré à part (`reports/rapport-pool-tampons.md`), pas déduit de cette passe.
>
> **Passe du 2026-10-13 à 03 h 59** (**37 portes, 35 vertes, 2 rouges**, ~72 min) : les deux rouges
> sont **les mêmes** que ci-dessous (le critère d'indice extérieur, marginal par construction), et
> **`porte-push-paresseux` y est verte** — c'est la passe précédente qui l'avait attrapée, et
> celle-ci vérifie la correction **dans les conditions où le défaut était apparu**. Les valeurs
> des portes n'ont pas bougé.
>
> **Passe du 2026-10-13 à 01 h 13** (**37 portes, 34 vertes, 3 rouges**, ~68 min) : les deux
> premiers rouges sont ceux de la botte de foin (voir ci-dessus) ; le troisième était **la porte
> elle-même** — `porte-push-paresseux` lisait `chargées en …s` alors que le moteur imprime `…ms`
> quand le chargement descend sous la seconde : elle passait sur une machine lente et échouait sur
> une machine rapide. **Corrigée à 02 h 25** (unité lue, refus de mesurer sur du vide) et revue
> **verte** seule ; l'état réel de cette passe est donc **35 vertes sur 37**, les deux rouges
> restants étant instruits. *C'est la passe qui l'a attrapée, pas une relecture.*
>
> **Passe du 10/10 à 22 h 27** (28 portes, 28 vertes, 73 min 21 s) : les six portes ajoutées
> ensuite y sont **mesurées à part** — `porte-sauvegarde-modele`, `porte-occupation-elagage`,
> `porte-harnais-invariants`, `porte-audit-drapeaux`, `porte-occupation-moteur`,
> `porte-poids-creux` — et **toutes vertes**, chacune **vue ROUGE** avec son défaut rallumé.
>

## 1. Ce qui se vérifie en une commande

| quoi | commande | attendu |
|---|---|---|
| tests unitaires | `cargo test --release` (dans `drave-core/`) | **122 verts** |
| le serveur de documentation | `tools/serveur-doc.py` (port 8787) | `tools/serveur-doc.py` · [`docs/en-cours.md`](../docs/en-cours.md) — il **ne juge rien** : il rend les documents et affiche « en ce moment », écrit à la main à chaque round |
| toutes les portes | `tools/toutes-les-portes.sh` | **46 portes** (`porte-reflexe` garde en plus, depuis le 16/10, l'**assemblage** du réflexe : le refus de l'adaptateur sans tête partielle, l'**invariant d'identité** et la mesure de l'accord ; 46ᵉ : `porte-homeostasie`, E9 ; `porte-cycle-c2` garde en plus la **bornitude** du cycle et **mesure λ**) ; dernière passe : **43 vertes sur 45** (15/10 11 h 21), ≈80 min, aucune sautée — les deux rouges sont **structurels** et connus (`porte-indice`, `porte-melange`) · ⚠ **ne jamais lire une porte à travers un `tail`** : sa dernière ligne suit l'échec, et le code de sortie est celui du tuyau |
| une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |

## 2. Les repères imprimés par chaque porte

| porte | durée | ce qu'elle vérifie, chiffré (passe du 2026-10-11 06:30) |
|---|---|---|
| `porte-audit-drapeaux.sh` | 149 s | ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun |
| `porte-budget.sh` | 42 s | ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite |
| `porte-bus.sh` | 75 s | ✅ le canal diffusé par fichier change la région du milieu |
| `porte-bus-socket.sh` | 88 s | ✅ le bus du pilote agit (113.0068 -> 148.9144) |
| `porte-c4-retard.sh` | 60 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |
| `porte-coupe.sh` | 125 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit |
| `porte-delais.sh` | 20 s | ✅ le temps, lui, augmente : 6.43 s → 9.75 s (+3.3 s ≈ 50 ms × 64 pas) |
| `porte-episodique.sh` | 166 s | ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un |
| `porte-flux.sh` | 20 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
| `porte-fusion.sh` | 7 s | ✅ v1 refusée (code 2), trace seule refusée (code 2) |
| `porte-gain.sh` | 351 s | ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san |
| `porte-greffe.sh` | 829 s | ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE |
| `porte-harnais-invariants.sh` | 105 s | ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage |
| `porte-horloge.sh` | 27 s | ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue |
| `porte-indice.sh` | 770 s | ✅ la porte est franchie. Limite, et elle est écrite : UN SEUL indice extérieur, |
| `porte-jumeaux.sh` | 77 s | PORTE TENUE : l'échange est exact, il ne crée pas de gain entre jumeaux identiques, il |
| `porte-melange.sh` | 805 s | ✅ la porte est franchie. Ce qu'elle dit : deux entrées qui se somment ARBITRENT |
| `porte-memoire.sh` | 7 s | PORTE TENUE : la mémoire retient les K derniers signaux HORS du réseau, exactement, sans |
| `porte-mistral.sh` | 9 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p |
| `porte-occupation-elagage.sh` | 50 s | ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté |
| `porte-occupation-moteur.sh` | 44 s | ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à |
| `porte-pannes.sh` | 45 s | ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité |
| `porte-peripherie.sh` | 9 s | PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont |
| `porte-poids-creux.sh` | 354 s | ✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité — paires divisées sur |
| `porte-pont.sh` | 75 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |
| `porte-profondeur-routee.sh` | 558 s | ✅ porte profondeur routée : 16 couches contre 24 sur 8192 jetons de corpus.ids, |
| `porte-recurrence.sh` | 10 s | PORTE TENUE : la boucle existe, elle est déterministe, elle ne coûte aucune paire, son zéro |
| `porte-reflexe.sh` | 106 s | ✅ l'état de 16 couches CONTIENT le prochain jeton : 25.4 % contre 4.8 % pour la classe majorit |
| `porte-registre.sh` | 14 s | ✅ région absente : refusée en la nommant (code 2), rien n'est calculé |
| `porte-reparti-moteur.sh` | 0 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |
| `porte-sauvegarde-modele.sh` | 45 s | ✅ porte sauvegarde du modèle : la perte de validation est la MÊME aux quatre étapes |
| `porte-tokenizer-kimi.sh` | 5 s | ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres) |
| `porte-topologie.sh` | 36 s | PORTE TENUE : le relais ne change pas un chiffre (42.5477) |
| `porte-trace.sh` | 25 s | ✅ la trace fausse est détectée et nommée |

## 3. Les trois invariants qui ne sont pas des chiffres

1. **Le crate reste `std` seul, zéro dépendance** — toute dépendance ajoutée est un refus, pas
   une négociation ;
2. **le profil `release` est le binaire de MESURE** : toute promotion dans le chemin
   d'exécution se paie d'un passage des portes (`porte-flux.sh` au minimum, cinq modes, ~2 min) ;
3. **on ne laisse jamais l'arbre cassé** : une tentative qui échoue se **renverse** (et la
   tentative est écrite dans le journal), elle ne reste pas à moitié appliquée.

## 4. Où sont les autres chiffres

- **mesures par expérience** : `reports/` (une fiche par fichier ; les campagnes éclatées en
  dossiers avec index, `reports/campagne-benefices/`, `reports/toutes-langues/`) ;
- **état des capacités** : `docs/etat-cerveau.md` et `docs/etat.md` ;
- **ce qui manque** : `docs/manques.md` (avec la mesure qui l'établit) ;
- **journal des événements** : `journal/AAAA-MM-JJ.md` (index du jour) et ses fichiers de thème.
