# Le cerveau Drave, faculté par faculté — et le modèle le plus efficient pour chacune

> **2026-10-14, 22 h 00 HAE** (heure lue sur la machine). Ce document est une **carte**, pas un
> plan : pour chaque faculté d'un cerveau, **le mécanisme que Drave emploie aujourd'hui**, **le
> chiffre qui le prouve**, et **son coût** — parce que « le plus efficient » veut dire : *à
> qualité donnée, le moins de paires, d'octets et de temps*. Ce qui n'est pas mesuré est écrit
> comme non mesuré, et ce qui manque est écrit comme un manque.
>
> Ce document ne remplace pas les autres : `docs/plan-cerveau-complet.md` porte les **douze
> capacités** (C1-C12), `docs/etat-cerveau.md` leur **état**, `docs/biologie-pour-drave.md` les
> expériences **E1-E9**, `docs/manques.md` ce qui **manque** (M1-M9, N1-N5). Ici, l'entrée est la
> **faculté**, pas la capacité : c'est la question « un cerveau, avec quoi ? ».

## 0. La carte en une table

| faculté | le mécanisme le plus efficient | le chiffre | coût | état |
|---|---|---|---|---|
| **perception** (entrées) | région frontière `--entree signal:F`, canal, gain, jeton | entrée constante ⇒ sortie constante, **au bit près** | **0 paire** | ✅ |
| **réflexes** | chemin court **entraîné** (LoRA couches basses + lecteur de sortie) | **÷1,47** (m32) et **÷1,24** (m20) à 8 couches, lus par le moteur | 0,07 % des poids | ✅ |
| **attention sélective** | **fenêtre + puits** (moitié des clés) | +0,4 % à +3,0 % selon le texte ; **÷2,67** de clés à 512 jetons | clés ÷2, paires ÷2 | ✅ |
| **mémoire de travail** | **tampon exact** `--memoire K` — et le réseau **ne l'apprend pas** (R² −1,09 → **−2,77** entraîné) | R² **1,000**, erreur nulle, poursuite de `v[t−8]` ; avec le tampon en entrée, le modèle gelé lit **+0,879** et l'entraîné **+0,964** | **0 paire de plus** | ✅ |
| **mémoire épisodique** | magasin adressable par contenu (hachage/LSH) | élagué **83 %**, rappel **96,3 %** à 50 % de dégradation, round-trip **exact** | **11 jetons sur 2 048** | ✅ |
| **consolidation** (sommeil) | rejeu → LoRA rang 8 sur 8 couches | **−16,4 %** en domaine sur des textes **jamais rejoués** ; **+1,3 %** hors domaine | 0,07 % des poids, 2 époques | ✅ |
| **modulation / arousal** | bus multi-canaux (statique, fichier, réseau) | canal neutre ⇒ empreintes **identiques** ; **aucun** signal scalaire n'améliore (négatif mesuré) | ~0 | 🟡 mécanique faite, signal non trouvé |
| **inhibition / E-I** | gain par couche (côté amplification) | gain 0,75 ⇒ **−11,5 %** ; l'**inhibition dégrade** ; le ratio cortical de signes coûte **+4,9 à +10,8 %** à l'entraînement | 0 | ✅ |
| **latéralité / corps calleux** | deux jumeaux, échange par couche | échange **exact**, gain **NUL** (36,1307 = 36,1307 : c'est une moyenne) | ÷2 de calcul | ✅ (résultat négatif) |
| **timing / conduction** | délai par lien (`delai_ms`) | 50 ms × 64 pas = **+3,1 s**, perplexité **inchangée** | loi **3,4 ms/token par ms** | ✅ |
| **horloges / asynchronie** | pas par région, `--pas-max` borné | un pas de retard coûte **×633** ⇒ on **ne réutilise jamais** un état ; gigue 40 % (local), 49 % (5 ms) | — | 🟡 premier pas |
| **cycles (boucles cortico-thalamiques)** | graphe récurrent déroulé, `recurrent` + délai | pas 1 **exact** (14,6496), puis **divergence** : 275,52 → 940,22 → **2 988,46** | **N pas × régions** exécutions | ✅ (capacité) / ❌ (utilité) |
| **budget / câblage minimisé** | budgets **octets, latence, paires** par lien | trois refus distincts : codes **6**, **8**, **9** | — | ✅ |
| **plasticité structurelle** | croissance locale des connexions | 8,1550 (croissance) contre 8,1827 (masque statique à densité égale) : **+0,3 %**, dans le bruit | — | 🟡 |
| **apprentissage local (Hebb)** | 5 variantes mesurées | la meilleure est **ne rien faire** (négatif) | — | ❌ |
| **langage / décodage** | le modèle + décodage spéculatif | brouillon minuscule **×1,52** ; TTFT **÷2,4** par le chemin court | — | 🟡 (M5) |
| **motricité / effecteurs** | `--sortie F` + réflexes | le signal **courant** est dans la sortie (R² 0,992) | 357,8 M paires/décision (complet) | 🟡 (tâche fermée) |
| **observabilité** | trace globale (`--trace-globale`) | **126 croisements**, aucune divergence ; 1 bit changé ⇒ **DIVERGENT** (code 3) | — | ✅ |
| **robustesse aux pannes** | registre de régions, refus nommés | panne de lien : **code 7**, jamais de résultat partiel | — | ✅ |

**Lecture** : neuf facultés sont **faites et chiffrées**, six sont **partielles** (le mécanisme
existe, la valeur n'est pas trouvée), une est un **résultat négatif** (la règle locale), et une
seule — la **consolidation dans le moteur** — dépend encore d'un outil hors moteur (torch).

## 1. Les trois mémoires, et laquelle choisir

Un cerveau a au moins trois mémoires, et Drave les a **toutes les trois**, avec des coûts très
différents — c'est le choix de conception le plus net de la carte :

| mémoire | ce qu'elle retient | mécanisme | coût | ce qu'elle ne fait pas |
|---|---|---|---|---|
| **de travail** (quelques pas) | les K derniers pas d'un signal | **tampon exact** (`--memoire K`), lu directement | **0 paire** | ne généralise pas : elle rend ce qui est entré |
| **épisodique** (la journée) | des épisodes entiers, adressables par contenu | magasin clé/valeur, hachage/LSH, écriture en **une passe** | 11 jetons sur 2 048 lus | **n'écrit rien dans les poids** — donc n'apprend pas |
| **sémantique** (les poids) | ce qui se répète | **consolidation** : rejeu → LoRA → poids | 0,07 % des poids | **spécialise** : +1,3 % hors domaine |

**Le classement d'efficience est net** : à court terme, un **tampon** bat tout (R² 1,000 pour
zéro paire) ; à moyen terme, un **magasin épisodique** bat la consolidation (aucun oubli, coût
local) ; à long terme, seule la **consolidation** met l'expérience dans les poids — et elle se
paie en généralité. La récurrence, elle, **ne retient pas** : mesurée deux fois (locale :
R² 0,906 → 0,112 ; et le cycle : divergence), elle **amplifie**.

## 2. Ce qui manque, faculté par faculté

| faculté manquante ou partielle | ce qui l'établit | ce que ça bloque |
|---|---|---|
| **apprentissage DANS le moteur** | la boucle est rejeu (moteur) → mise à jour (**torch**) → mesure (moteur) : manque **M6** | l'adaptation en ligne, et un cerveau qui se consolide sans nous |
| **mémoire de travail du MODÈLE** | le tampon est dans le **moteur** ; le modèle ne retient pas **et ne l'apprend pas** (−2,77 après 8 époques, `rapport-memoire-travail-n5.md`) | toute tâche qui demande de retenir *dans* le réseau — sauf à lui donner la structure, qu'il sait alors **lire** (+0,964) |
| **un signal de modulation qui améliore** | cinq règles locales et cinq modulateurs mesurés ; le meilleur est **ne rien faire** | la valeur, la récompense, l'attention apprise |
| **un cycle qui serve** | le cycle est exact au pas 1 et **diverge** ensuite, non entraîné | les boucles cortico-thalamiques *utiles* |
| **perception riche (vision, audio)** | les encodeurs (`bge-m3`) sont lisibles et **inexécutables** — manque **M4** | toute la famille multimodal |
| **un sommeil structuré** | la consolidation marche, mais **hors** du moteur et sans protocole de sommeil (quoi rejouer, quand s'arrêter) | un cycle veille/sommeil automatique |
| **la latéralité qui apporte** | l'échange est exact et le gain **nul** (mesuré deux fois : couches et experts) | une raison de dupliquer un hémisphère, à part la robustesse |

## 3. La règle d'efficience, en une phrase

> **Ce qui doit être retenu exactement demande une STRUCTURE (un tampon : 0 paire). Ce qui doit
> être retrouvé demande un MAGASIN (épisodique : 11 jetons sur 2 048). Ce qui doit être su
> demande des POIDS (consolidation : 0,07 % des poids, et une perte de généralité). Et ce qui
> doit être amplifié par le temps demande un CYCLE — qui, non entraîné, diverge.**

C'est la leçon que les mesures de ce dépôt donnent, et elle est contre-intuitive là où elle
compte : on cherche naturellement la mémoire **dans** le réseau (récurrence, état récurrent), et
les trois mesures de ce dépôt disent qu'elle est **à côté** — dans un tampon, dans un magasin, ou
dans une consolidation séparée.

## 4. Où chaque chiffre se vérifie

| faculté | fiche |
|---|---|
| réflexes, chemin court | [`rapport-n4-dessin-b.md`](../reports/rapport-n4-dessin-b.md) · [`rapport-n4-porte-execution.md`](../reports/rapport-n4-porte-execution.md) |
| consolidation | [`rapport-consolidation-c7.md`](../reports/rapport-consolidation-c7.md) |
| cycle C2 | [`rapport-cycle-c2.md`](../reports/rapport-cycle-c2.md) |
| récurrence locale | [`rapport-c2-recurrence.md`](../reports/rapport-c2-recurrence.md) |
| mémoire de travail, périphérie | [`rapport-c8-peripherie.md`](../reports/rapport-c8-peripherie.md), [`note-peripherie-c8.md`](note-peripherie-c8.md) |
| mémoire épisodique | fiches 24, 29, 30, 31 · `porte-episodique.sh`, `porte-indice.sh` |
| fenêtre et puits d'attention | [`rapport-fenetre-puits-attention.md`](../reports/rapport-fenetre-puits-attention.md) · [`rapport-loi-frontiere-fenetre.md`](../reports/rapport-loi-frontiere-fenetre.md) |
| bus de modulation | `porte-bus.sh`, `porte-bus-socket.sh` |
| E/I et gains | [`rapport-e4-ratio-signes.md`](../reports/rapport-e4-ratio-signes.md) |
| latéralité | [`rapport-c9-lateralite.md`](../reports/rapport-c9-lateralite.md) · [`rapport-c9-echange-experts.md`](../reports/rapport-c9-echange-experts.md) |
| délais, horloges, budgets | fiches 43, 44, 32, 42 · `porte-delais.sh`, `porte-horloge.sh`, `porte-budget.sh` |
| plasticité structurelle, règle locale | [`rapport-e1-e2-connectome-croissance.md`](../reports/rapport-e1-e2-connectome-croissance.md) |
| trace globale, pannes | `porte-trace.sh`, `porte-fusion.sh`, `porte-pannes.sh` |

**Ce que cette carte ne dit pas** : elle ne dit pas qu'un tel cerveau **bat** un transformeur sur
une tâche — aucune mesure de ce dépôt ne le dit, et le plan le dit lui-même (§ 5). Elle dit ce
qui **existe**, ce que ça **coûte**, et où sont les trous.
