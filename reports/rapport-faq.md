# B13 / D3 — la FAQ du produit : dix questions, dix réponses vérifiées

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **D3** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **10/10 réponses vérifiées** contre le code courant (`drave 0.1.0`) ;
> **contrôle négatif détecté** (deux affirmations fausses sont rejetées par le code).
>
> **La question.** Un utilisateur qui découvre le produit se pose dix questions concrètes :
> la langue, le hors-ligne, le coût, le tagger, le schéma, l'attachement, les spans
> inatteignables, la restitution, les limites, l'installation. La notice y répond-elle
> encore, ou répète-t-elle des chiffres d'hier ?
>
> **La réponse.** La section **§ 8** de [`docs/produit/README.md`](../docs/produit/README.md)
> porte les dix questions ; chacune est adossée à une commande, à une constante du code ou à
> un JSON de `reports/`, et **dix contrôles exécutables** les rejouent. Les dix passent. Le
> contrôle négatif est explicite : le CLI **refuse** `--langue de` (code 2) et le schéma v2
> **refuse** une annotation v1 — si ces deux refus disparaissaient, la FAQ serait fausse.
>
> **Le chiffre.** **10/10** réponses ; **26 cas** de schéma (dont le cas v1) ; **238/239**
> cibles d'attachement ; **46/46** surfaces et **46/46** formes canoniques ; **19/46** cadres
> de rôles exacts (dont **16** non vides), **F1 0,5270** ; **609 appels**, **22 299 tokens**,
> **155 s**, **~0,02 $** pour le tagger sur 612 phrases.
>
> **Dispositif** : [`tools/verifier_faq.py`](../tools/verifier_faq.py) (les dix contrôles, le
> contrôle négatif, `--json`), [`docs/produit/README.md`](../docs/produit/README.md) § 8 (la
> FAQ), [`reports/faq.json`](faq.json) (le relevé complet). Les chiffres restent dans leurs
> fiches : [`rapport-g017.md`](rapport-g017.md),
> [`rapport-restitution-v0.md`](rapport-restitution-v0.md),
> [`rapport-restitution-v1.md`](rapport-restitution-v1.md),
> [`rapport-restitution-v2.md`](rapport-restitution-v2.md),
> [`rapport-tagger-option.md`](rapport-tagger-option.md),
> [`rapport-audit-v10.md`](rapport-audit-v10.md).

## 1. Ce que la FAQ est — et n'est pas

C'est une **vérification de cohérence**, pas une mesure nouvelle. La FAQ ne revendique aucun
chiffre inédit : elle reprend les valeurs publiées et les **confronte au code**. Le
vérificateur :

- lance le CLI en local (`analyser`, `evaluer`, `evaluer --reel`, `restituer`, `--aide`,
  `--version`) ;
- lit les JSON de résultats déjà publiés (`pensee-tagger-option.json`,
  `pensee-audit-v10.json`, `pensee-g017.json`, `rapport-exemples-tagger.json`) ;
- inspecte le source (`tools/drave.py`, les schémas v1/v2) pour les constantes et les options
  qui existent — ou pas ;
- **n'appelle aucune API**, ne lit aucune clé, n'ouvre aucune socket. Le seul réseau du
  produit reste `--tagger`, et il n'est pas exercé ici.

La FAQ **ne prouve pas** que le tagger est bon, que les rôles sont justes ou que le produit
tient hors domaine : elle prouve que **ce qui est écrit** correspond à **ce que le code fait**
et aux **chiffres publiés** au 2026-11-15.

## 2. Les dix questions

| # | question | réponse (chiffre vérifié) | contrôle |
|---:|---|---|---|
| 1 | **Quelles langues ?** | détection `de`/`es`, `und` sous le seuil ; `--langue` limité à `fr`/`en` ; `--langue de` → code 2 ; 398 profils UDHR (0,9687) | `q1_langue` |
| 2 | **Hors ligne ?** | socket interdite : analyse code 0 ; module réseau non importé ; `--tagger` sans clé → code 4, `stdout` vide | `q2_hors_ligne` |
| 3 | **Combien ça coûte ?** | défaut : 0 $ d'API ; tagger : **609 appels**, **22 299 tokens**, **155 s**, **~0,02 $** ; 3 exemples : **441 tokens**, **3,7 s** | `q3_cout` |
| 4 | **Que change `--tagger` ?** | POS seul : **95,75 %** contre **86,25 %** (612) ; **95,00 %** contre **88,91 %** (réel 452) ; ponctuation **25/25** | `q4_tagger` |
| 5 | **Quel schéma ?** | `drave.annotation` **v2**, v1 lue ; **6 cas**, **26** avec `--gold 20`, **0 échec** ; v2 refuse v1 | `q5_schema` |
| 6 | **L'attachement ?** | **238/239** cibles (**0,9958**) ; **1,0000** sur les spans prédits ; top-k **0,9874** ; hasard **1,67 %** ; audit **42,14 %** / **0,908 %** | `q6_attachement` |
| 7 | **Les spans inatteignables ?** | **1** : `g017`, SUB **[9:28]** attendue / **[9:38]** prédite ; règle rejetée (F1 **0,7901**, couverture **0,9916**) ; réel **183/184** | `q7_span_inatteignable` |
| 8 | **La restitution ?** | v0 **46/46** surfaces, strict **0,1087** ; v1 **46/46** canonique ; v2 **19/46** cadres (**16** non vides), **F1 0,5270** | `q8_restitution` |
| 9 | **Les limites ?** | pas de génération, serveur, RSN, local, classement, calibration, `--langue-forcee`, garantie hors domaine ; `--sortie`/`--mode`/`--strict` → code 2 | `q9_limites` |
| 10 | **L'installation ?** | `drave 0.1.0`, Python **3.10** (grammaire), `python3 -S` code 0, **0** dépendance, gold versionnés | `q10_installation` |

## 3. Le dispositif

```bash
python3 tools/verifier_faq.py            # résumé : 10/10 + contrôle négatif
python3 tools/verifier_faq.py --json     # le relevé de reports/faq.json
python3 tools/verifier_faq.py --autotest # vérifie que le contrôle négatif échoue bien
```

Le script tourne depuis la racine, en UTF-8, sans réseau. Il construit son environnement
« sans clé » en retirant `DEEPSEEK*` et `DSH_*` et en vidant `HOME` : le test du code 4 ne
peut pas emprunter une clé de la machine. Pour le hors-ligne, il exécute le CLI dans un
interpréteur où `socket.socket` et `socket.create_connection` **lèvent** : l'analyse doit
rendre 0, et `tools.llm.deepseek` doit rester absent de `sys.modules`.

Le relevé [`faq.json`](faq.json) contient, pour chaque question, le bloc `observe` (les
valeurs réellement lues), `ok` et `erreur` (vide si tout passe). Le champ `controle_negatif`
dit quelles affirmations fausses ont été rejetées.

## 4. Les sorties observées

| contrôle | valeur observée |
|---|---|
| détection | `Der Hund schläft.` → `de` ; `El perro duerme.` → `es` ; `Élodie sourit.` → `und`, aussi avec `--langue fr` |
| indice CLI | `--langue de` → **2** ; choix `fr`, `en` |
| hors ligne | socket interdite → **0** ; `tools.llm.deepseek` importé → **False** |
| tagger sans clé | code **4**, `stdout` **vide**, message « dépendance absente … hors ligne » |
| coût | **609** appels, **22 299** tokens, **155,6 s**, **159** requêtes réseau, **~0,02 $** |
| POS | **0,8625 → 0,9575** (612) ; **0,8891 → 0,9500** (452) ; `PONCT` **25/25** |
| schéma | **6/6** cas, **26/26** avec `--gold 20`, versions **[1, 2]**, `v1_lue`, `v2_refuse_v1` |
| attachement | **238/239** labels, **0,9958**, exact sur span **1,0000**, top-k **0,9874** |
| contrôles négatifs | cible au hasard **0,0167** ; candidat aléatoire **0,4214** ; permutation **0,00908** |
| `g017` | gold **[9:28]**, prédit **[9:38]**, cible `said` juste ; règle **rejetée** |
| restitution v0 | **46/46** surfaces, miroir strict **0,1087**, **46** contrôles négatifs détectés |
| restitution v1 | **46/46** canonique, strict **0,1087**, **395** segments, **315** cibles |
| restitution v2 | **19/46** cadres exacts, **16** non vides, **F1 0,5270**, **198/198** spans, **46/46** rendus |
| installation | `drave 0.1.0`, `python3 -S` **0**, grammaire **3.10**, **0** paquet externe |

## 5. Le contrôle négatif

Le vérificateur ne se contente pas de confirmer : il vérifie que le code **rejette** deux
affirmations fausses.

| affirmation fausse | ce que le code fait | détecté |
|---|---|---|
| « le CLI accepte `--langue de` » | `analyser … --langue de` sort **2** (usage invalide) | ✅ |
| « le schéma v2 accepte une annotation v1 » | `verifier_schema_produit.py` publie `v2_refuse_v1: true` | ✅ |

Si l'une des deux tombait, `controle_negatif.detecte` serait `false` et le script sortirait 1 :
c'est le garde-fou contre une FAQ qui se contenterait de répéter le code.

## 6. Ce qui pourrait rendre ces réponses fausses

1. **Le code change sans la FAQ.** Les contrôles lisent des constantes et des sorties : si
   `--langue`, les codes de sortie, la fusion `--tagger`, les choix de `--partition` ou la
   forme de `--roles` changent, le vérificateur échoue — et la FAQ doit être réécrite.
2. **Le modèle ou le prix de l'API change.** `deepseek-chat` est le modèle **demandé** ;
   `deepseek-flash` est souvent **renvoyé**. Les **~0,02 $** sont une estimation datée du
   15/11 sur 612 phrases, pas un tarif garanti ; le cache peut rejouer une réponse ancienne.
3. **Le gold ou les JSON de résultats bougent.** Les valeurs **238/239**, **19/46**,
   **0,5270**, **0,9958** sont lues dans les JSON courants. Si une mesure ultérieure les
   change **et** que le vérificateur est mis à jour en même temps, la FAQ peut rester
   silencieusement en retard : c'est pourquoi la fiche renvoie à chaque fiche source.
4. **Le corpus ou les gold manquent.** `data/` est hors dépôt ; les gold sont versionnés,
   mais un clone incomplet fait échouer les contrôles (et c'est voulu).
5. **La date.** La FAQ est vérifiée au **2026-11-15** ; une réponse « vérifiée » un autre jour
   n'a pas la même valeur. Relancer `tools/verifier_faq.py` avant de la citer.

## 7. Ce que la FAQ ne prouve pas

Elle ne prouve **pas** la qualité linguistique : le tagger peut rester dépendant du modèle du
jour, les rôles de la v2 restent à **F1 0,5270**, l'attachement est **in-sample**, et un texte
hors domaine peut baisser sans que le JSON change de forme. Elle ne prouve pas non plus que
les **398 langues** sont disponibles dans le CLI : elles sont dans le bloc, pas dans l'interface.
Enfin, elle ne remplace pas les fiches : chaque chiffre garde son dispositif, son contrôle
négatif et ses conditions de lecture dans `reports/`.

## 8. Où lire la suite

- la **FAQ** : [`docs/produit/README.md`](../docs/produit/README.md) § 8 ;
- le **relevé** : [`faq.json`](faq.json) ;
- le **vérificateur** : [`tools/verifier_faq.py`](../tools/verifier_faq.py) ;
- les **fiches sources** : [`g017`](rapport-g017.md),
  [`restitution v0`](rapport-restitution-v0.md),
  [`restitution v1`](rapport-restitution-v1.md),
  [`restitution v2`](rapport-restitution-v2.md),
  [`tagger`](rapport-tagger-option.md), [`audit v10`](rapport-audit-v10.md),
  [`schéma v2`](rapport-schema-v2.md).
