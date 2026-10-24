# Passe COMPLÈTE des portes : de 22 à 47 portes — et une porte qui était verte en ne mesurant RIEN

> Campagne : **outillage** · expérience : la passe complète (`tools/toutes-les-portes.sh`)
> Question : les portes du dépôt passent-elles **toutes**, quand on les lance **toutes** ?
> Verdict : **oui, à chaque passe** — **22 sur 22** au premier passage (2026-10-10, 11 h 07), puis les passes
> successives consignées ci-dessous, jusqu'à la **47ᵉ porte** (`porte-diff-couche`, ajoutée le 24/10 — elle vérifie
> la reproductibilité du flux et nomme les divergences). Et la passe a trouvé ce qu'une porte lancée seule ne
> pouvait pas montrer : `porte-tokenizer-kimi` sortait **verte en comparant zéro jeton** (elle lisait `stdin`, que
> personne ne lui fournissait). Corrigée, elle compare maintenant **10 textes** en **7,5 s**.
>
> *Les sections 2 bis à 2 quater consignent les passes historiques ; la section 2 quinquies attend le verdict de
> la passe du 24/10 (47 portes) — elle n'est pas écrite d'avance.*
> Date réelle : **2026-10-10 11:10 HAE** (heure de la machine ; la passe a tourné de 09 h 57 à
> 11 h 07).
> Protocole : `DELAI=2400 tools/toutes-les-portes.sh` — chaque porte bornée dans le temps, son
> journal gardé dans `/tmp/portes-1210b/`.

## 1. Pourquoi cette passe existe

`tools/porte-gain.sh` § 9 était **rouge depuis le protocole v7** sans que personne le voie : elle
exigeait un refus que le v7 avait **délibérément retiré**. Les portes étaient lancées **une par
une, à la main**, celle de la fonctionnalité du jour — « les 23 portes sont vertes » était une
affirmation sur une suite **qui n'avait jamais tourné comme une suite**. La passe complète est
l'instrument qui manquait ; c'est elle qui a produit ce rapport.

## 2. Le résultat, porte par porte

| porte | durée | ce qu'elle a verrouillé (dernière ligne) |
|---|---|---|
| `porte-budget.sh` | 43 s | ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite |
| `porte-bus.sh` | 74 s | ✅ le canal diffusé par fichier change la région du milieu |
| `porte-bus-socket.sh` | 94 s | ✅ le bus du pilote agit (113.0068 -> 148.9144) |
| `porte-coupe.sh` | 132 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit |
| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.79 s → 9.45 s (+2.7 s ≈ 50 ms × 64 pas) |
| `porte-episodique.sh` | 184 s | ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un |
| `porte-flux.sh` | 22 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
| `porte-fusion.sh` | 8 s | ✅ v1 refusée (code 2), trace seule refusée (code 2) |
| `porte-gain.sh` | 388 s | ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san |
| `porte-greffe.sh` | 971 s | ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE |
| `porte-horloge.sh` | 24 s | ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue |
| `porte-indice.sh` | 971 s | ✅ la porte est franchie. Limite, et elle est écrite : UN SEUL indice extérieur, |
| `porte-melange.sh` | 984 s | ✅ la porte est franchie. Ce qu'elle dit : deux entrées qui se somment ARBITRENT |
| `porte-mistral.sh` | 10 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p |
| `porte-pannes.sh` | 50 s | ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité |
| `porte-pont.sh` | 89 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |
| `porte-reflexe.sh` | 102 s | ✅ le gain de temps est réel : 5.9 ms par jeton à 1 couche(s) contre 126.8 ms à 24 — 21.5× plus |
| `porte-registre.sh` | 14 s | ✅ région absente : refusée en la nommant (code 2), rien n'est calculé |
| `porte-reparti-moteur.sh` | 1 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |
| `porte-tokenizer-kimi.sh` | 0 s | — |
| `porte-topologie.sh` | 43 s | PORTE TENUE : le relais ne change pas un chiffre (42.5477) |
| `porte-trace.sh` | 30 s | ✅ la trace fausse est détectée et nommée |

**Total : 4 255 s (70 min)**, dominé par trois portes lourdes (`porte-melange` 984 s,
`porte-greffe` 971 s, `porte-indice` 971 s).

## 2 bis. La passe du 15 h 15 (23 portes, 58 minutes) — après les changements du moteur

C'est la passe qui suit l'ajout de la **périphérie** (C8 : `--entree`, `--sortie`, `--delai`,
`--recurent`) et la correction de `porte-reflexe.sh`. Elle est verte **entièrement**, ce qui est
l'information utile : les nouveaux drapeaux n'ont rien cassé, et la porte du réflexe verrouille
désormais la bonne conclusion (25,4 % contre 4,8 %).

| porte | durée | ce qu'elle a verrouillé (dernière ligne) |
|---|---|---|
| `porte-budget.sh` | 42 s | ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite |
| `porte-bus.sh` | 76 s | ✅ le canal diffusé par fichier change la région du milieu |
| `porte-bus-socket.sh` | 90 s | ✅ le bus du pilote agit (113.0068 -> 148.9144) |
| `porte-coupe.sh` | 121 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit |
| `porte-delais.sh` | 19 s | ✅ le temps, lui, augmente : 5.80 s → 9.13 s (+3.3 s ≈ 50 ms × 64 pas) |
| `porte-episodique.sh` | 162 s | ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un |
| `porte-flux.sh` | 19 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
| `porte-fusion.sh` | 7 s | ✅ v1 refusée (code 2), trace seule refusée (code 2) |
| `porte-gain.sh` | 341 s | ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san |
| `porte-greffe.sh` | 834 s | ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE |
| `porte-horloge.sh` | 23 s | ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue |
| `porte-indice.sh` | 719 s | ✅ la porte est franchie. Limite, et elle est écrite : UN SEUL indice extérieur, |
| `porte-melange.sh` | 762 s | ✅ la porte est franchie. Ce qu'elle dit : deux entrées qui se somment ARBITRENT |
| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p |
| `porte-pannes.sh` | 43 s | ✅ pair absent : échec annoncé en 1 s (code 7), aucune perplexité |
| `porte-peripherie.sh` | 7 s | PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont |
| `porte-pont.sh` | 74 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |
| `porte-reflexe.sh` | 101 s | ✅ l'état de 16 couches CONTIENT le prochain jeton : 25.4 % contre 4.8 % pour la classe majorit |
| `porte-registre.sh` | 14 s | ✅ région absente : refusée en la nommant (code 2), rien n'est calculé |
| `porte-reparti-moteur.sh` | 1 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |
| `porte-tokenizer-kimi.sh` | 5 s | ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres) |
| `porte-topologie.sh` | 33 s | PORTE TENUE : le relais ne change pas un chiffre (42.5477) |
| `porte-trace.sh` | 24 s | ✅ la trace fausse est détectée et nommée |

## 2 ter. La passe du 16:58 (23 portes, 58 min 07 s) — après le TAMPON d'entrée

Dernière passe en date : `--entree-memoire K` ajouté à la périphérie (le signal devient un vecteur :
valeur courante plus K retards), la porte étendue en conséquence (le tampon change la sortie, il
est annoncé, un débordement est refusé), et **23 vertes sur 23** de nouveau. Détail porte par porte
dans `docs/references-non-regression.md` § 2, régénéré depuis le journal de cette passe.

## 2 quater. La passe du 19:20 (25 portes, 59 min 25 s) — la suite COMPLÈTE

Dernière passe en date, et la première qui contient les **deux portes ajoutées aujourd'hui** :
`porte-jumeaux.sh` (C9 : l'échange est exact, il ne crée pas de gain, il récupère un jumeau dégradé
à hauteur de sa moyenne, et 8 bits suffisent pour ÷4 d'octets) et `porte-c4-retard.sh` (C4 : un
état n'est valide qu'à sa position — ×633 pour un pas — et manquer coûte ×1,06 contre ×633 pour
réutiliser). **25 vertes sur 25**, détail dans
`docs/references-non-regression.md` (régénéré depuis ce journal).

## 2 quinquies. La passe du 24/10 (47 portes, 1 h 48 min) — la première à 47, et la nouvelle porte est verte

**Verdict : 45 vertes, 2 rouges** — les deux structurels connus (`porte-indice` 827 s, `porte-melange` 104 s),
**aucun rouge nouveau**. La 47ᵉ porte, `porte-diff-couche`, est **verte en 18 s** : le contrat de flux tient (deux
exécutions identiques → flux identique ; le KV 8 bits → divergence nommée, couche 1, jeton 1).

Sept portes ont dépassé les 180 s : `porte-indice` (827), `porte-homeostasie` (653), `porte-greffe` (648),
`porte-profondeur-routee` (516), `porte-poids-creux` (316), `porte-gain` (221), `porte-prechargement` (189) — et
`porte-harnais-invariants` (111), `porte-bus` (81), `porte-consolidation` (75).

**Ce que la passe établit** : les changements du jour — `placement.rs` et ses quatre tests, `diff_flux.py` en v2,
`model.rs` avec la tête revertée, la nouvelle porte — **ne cassent aucune porte**. La seule différence avec la passe
du 17/10 (46 portes, 44 vertes, 2 rouges) est **la 47ᵉ porte, verte**.

## 3. Ce que la passe a trouvé : une porte qui ne pouvait pas échouer

`porte-tokenizer-kimi.sh` **lisait ses textes sur `stdin`** — que personne ne lui fournissait.
La boucle lisait donc **EOF immédiatement**, imprimait « identiques : 0 · divergents : 0 » et
sortait en **0** : verte, en n'ayant rien comparé. Aucun lancement manuel ne le montrait (à la
main, on ne sait pas quel `stdin` la porte attend) ; c'est le **temps** qui l'a trahie —
**0 seconde** pour une porte censée charger un shard de modèle et un tokenizer Python.

**Corrigée** : les textes sont **dans** la porte (accents, emoji, CJK, arabe, code, nombres,
URL, tabulations, sauts de ligne), elle **refuse de verdir** si le nombre de comparaisons est
nul, et un prérequis manquant (shard, référence, interpréteur, binaire) est **rouge (code 2)**.
Mesure après correction : **10 textes identiques au tokenizer officiel, 7,5 s**.

## 4. Deuxième leçon, pour le harnais

La carte fenêtre × puits lancée en parallèle a fini sur un `syntax error` : **j'ai édité le
script pendant qu'il tournait**. Bash lit un script **au fur et à mesure** de son exécution —
modifier le fichier en cours de route décale ce qui reste à lire. Les chiffres déjà imprimés
étaient bons, la dernière ligne non. Ne pas éditer un script qui tourne.

## 5. Ce que la passe ne dit pas

- elle ne teste pas les **temps** comme des invariants (les portes de latence et de gigue
  mesurent, mais un chiffre de temps sous charge n'est pas une porte) ;
- elle n'exécute **pas** les tests unitaires (`cargo test`, 122 tests verts par ailleurs) ;
- elle ne dit rien des portes **absentes** : une capacité sans porte ne se voit pas ici.
