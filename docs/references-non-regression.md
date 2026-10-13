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
> n'a jamais été versionnée, `tools/niah_4096_0.5.txt` l'est désormais) et l'effet qu'elles
> mesurent — un indice extérieur qui tombe plus près de l'aiguille que le hasard — ne se reproduit
> pas sur elle (482 jetons contre 370). La porte documente elle-même que l'effet est **réel mais
> non robuste**.
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
| toutes les portes | `tools/toutes-les-portes.sh` | **34 vertes sur 36** (12/10 : les deux rouges sont la botte de foin régénérée), ≈75 min, aucune sautée |
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
