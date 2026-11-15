# S — la page `/` ne sert pas la v7, le service ne tourne pas, et les 11 verdicts sont committés

> **Ligne de roadmap** : S · **Date** : 2026-11-15 · **HEAD parent mesuré** : `292c70b5`
> · **Sous-module `tools/structures`** : `389b99f` · **Verdict** : les **11 verdicts**
> a004–a009 sont **committés** (sous-module `389b99f`, pointeur parent `31ce36fd`) :
> **19/19 candidats, 11 acceptés, 8 exclus**. La page **`/`** **ne sert pas la v7** : elle
> charge **369 candidats stockés** (0 avec `profondeur`) et son rendu lit `niveau` ; la mesure
> v7 sur les mêmes **207 phrases** donne **359 candidats**, dont **99 à profondeur ≥ 3**. Le
> service S **n'est pas en écoute** : le port **8765** est tenu par un autre projet
> (`financemeteo`, pid 2725542), et un lancement de mesure sur **9000** répond 200. Le
> pare-feu **firewalld** est actif mais **non interrogeable sans root** ; le serveur écoute
> **127.0.0.1** par défaut. **Aucun fichier suivi de `tools/structures/` n'est modifié.**

**En trois lignes.** (1) Les 11 verdicts ne sont plus une dette : le sous-module est propre à
`389b99f`, le parent pointe dessus, et un clone voit **19 verdicts / 11 acceptés / 0 candidat
sans verdict**. (2) La page `/` est toujours **l'ancien banc plat** : **369/369** candidats
stockés sans `profondeur`, distribution des `niveau` **10 / 277 / 82** (0/1/2), alors que la v7
dynamique donne **2 / 37 / 221 / 84 / 13 / 2** et **99 candidats à ≥ 3**. (3) Le service n'est
pas lancé ; si on le lance, **8765 est déjà pris** et le pare-feu n'est pas le premier obstacle :
le défaut `--hote 127.0.0.1` est **local par construction**.

## Ce que cette fiche est, et n'est pas

- **Est** : la suite de [`rapport-coordination-s.md`](rapport-coordination-s.md). Elle constate
  l'effet du commit `389b99f`, mesure l'état réel de la page `/` et de `/paragraphes`, tranche
  la question du **service de la v7**, du **pare-feu** et de la **commande de lancement**, et
  liste ce qui reste à S.
- **N'est pas** : un patch, un commit de S, ni une modification de `tools/structures/`. Le
  serveur a été lancé **sur le port 9000** pour les mesures GET, puis **arrêté** ; aucun
  `POST`, aucune écriture dans le sous-module. `git -C tools/structures status --porcelain`
  est **vide** après les mesures.
- **Public** : la session S (prochaine action : décider la migration de `/`), le superviseur du
  chantier J4 et toute session qui doit **lancer** la page sans la confondre avec la v7.
- **Mesure** : `tools/structures` à `389b99f`, parent `292c70b5`, 2026-11-15 02 h 20 HNE ;
  **56 tests** du sous-module passent en 4,3 s (`Ran 56 tests … OK`).

## 1. Les 11 verdicts sont committés — la v1 est périmée

### 1.1 L'état mesuré

| mesure | valeur |
|---|---|
| sous-module `tools/structures` | **`389b99f`** (`S — LES 11 VERDICTS HUMAINS…`) |
| commit du sous-module | **1 file changed, 11 insertions(+)**, 2026-11-14 09:49 |
| parent `s/v7` | **`292c70b5`** (C1) |
| pointeur du parent | **`31ce36fd`** → `389b99f` (`git ls-tree HEAD tools/structures`) |
| fichier | `donnees/paragraphes-validations.jsonl`, **19 lignes** |
| statuts | **10 `resolu`, 1 `compatible`, 8 `exclu`**, 0 `double_sens` |
| acceptés | **11** (10 + 1) |
| exclus | **8** |
| paragraphes | **9/9** (a001–a009) |
| candidats | **19/19**, **0** sans verdict |
| notes | **0/19** |
| working tree du sous-module | **propre** (`git status --porcelain` vide) |
| `origin/master` du sous-module | **`389b99f`**, 0 avance / 0 retard |
| tests | **56/56** en 4,3 s |

La v1 décrivait juste avant le commit : **8 verdicts committés**, **11 non committés**,
**4 acceptés** dans un clone à `523d8c1`. Ces chiffres sont **historiques** ; ils ne décrivent
plus l'état. Un clone à `389b99f` voit les **19** verdicts, et le contrôle négatif de la v1
(clone à `523d8c1` → 8 verdicts) n'a plus cours comme description du présent.

### 1.2 Les deux « 11 » ne se confondent pas

| ensemble | contenu | acceptés | exclus |
|---|---|---:|---:|
| les **11 verdicts du commit** (a004–a009) | 6 `resolu` + 1 `compatible` + 4 `exclu` | **7** | **4** |
| les **19 verdicts du fichier** (a001–a009) | 10 `resolu` + 1 `compatible` + 8 `exclu` | **11** | **8** |

Le commit porte bien **11 lignes**, mais **7 acceptées et 4 exclues** ; le total du fichier est
**11 acceptées et 8 exclues**. La v1 avait déjà signalé ce piège ; il reste vrai après le
commit. Le titre du commit dit « 19/19, 11 acceptés, 8 exclus », ce qui est le total, pas les
11 lignes ajoutées.

### 1.3 Ce que le commit ne répare pas

- **0 note** sur les 19 verdicts : un défaut de page et un choix humain restent indiscernables.
- Les référents enregistrés restent ceux de la v1 : **9/16 mappings uniques faux** (l'audit
  large compte **12/28 occurrences**), et le seul `compatible` est **a008**, le paragraphe à
  **0/5** référents justes.
- Le commit ne migre **pas** la page `/` ; il ne concerne que `/paragraphes`.

## 2. La page `/` : le service, pas la v7

### 2.1 Aucun service S n'est en écoute

| contrôle | résultat |
|---|---|
| processus `python3 … serveur.py` | **aucun** (`ps -eo pid,comm,args` filtré) |
| port **8765** | **occupé** par `python3 src/app.py --no-browser`, pid **2725542**, démarré le **14/11 16:13:37**, cwd `…/financemeteo` |
| ce que 8765 sert réellement | **`<title>Portefeuille iA — tableau de bord</title>`**, 174 051 o, HTTP 200 |
| port **9000** | **libre** avant la mesure ; le serveur de mesure y a répondu, puis a été arrêté |
| port **8771** | `docwatch` (autre outil), 127.0.0.1 |
| port **3080** | `dsh web` (autre outil), 0.0.0.0 |

**Conséquence immédiate** : `python3 serveur.py` **sans `--port`** ne peut pas démarrer sur
cette machine, puisque `8765` est déjà pris. Il ne faut **pas** faire `fuser -k 8765/tcp` :
cela tue le tableau de bord `financemeteo`, pas le serveur S.

### 2.2 Ce que `/` sert quand on le lance sur 9000

Commande de mesure (serveur arrêté après les GET) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures
PYTHONDONTWRITEBYTECODE=1 nohup python3 serveur.py --port 9000 --hote 127.0.0.1 \
  > /tmp/c2-serveur-9000.log 2>&1 &
```

Journal de démarrage : `banc de structures · http://127.0.0.1:9000 · 207 phrases`.

| route | code | contenu mesuré |
|---|---:|---|
| `GET /` | **200** | 2 350 o, `<title>Structures — le banc d'interprétations</title>` |
| `GET /api/phrases` | **200** | **207 phrases**, **369 candidats**, **150 validations** (lignes) |
| `GET /paragraphes` | **200** | 3 493 o |
| `GET /api/paragraphes` | **200** | **9 paragraphes**, **19 candidats**, **19 verdicts**, 169 segments |

**Le point dur** : dans `/api/phrases`, **0/369 candidats** portent `profondeur` ; les segments
ne portent que l'ancien `niveau`, dont la distribution des maxima est **10 / 277 / 82** pour
0 / 1 / 2. La page `/` charge les candidats **stockés** dans `phrases_generees.json`
(mtime **2026-11-02 20:35**), pas la sortie de `generateur.analyser`. C'est exactement le
négatif « 277/369 plats » de la fiche de banque partielle.

### 2.3 Pourquoi le rendu ne suffit pas à dire « v7 »

- `static/app.js:20` indente avec **`s.niveau`**, et `niveauDe()` (ligne 36) lit le `niveau`
  de la dernière validation ; il **ne lit jamais `profondeur`**.
- `static/paragraphes.js:20` indente aussi avec `s.niveau`, mais affiche
  **`s.profondeur ?? s.niveau`** : c'est la page qui montre la v7.
- `generateur._profondeur()` fait **`s.niveau = s.profondeur`** : une régénération complète par
  la v7 met les deux champs à la profondeur réelle, donc `app.js` afficherait la v7 **si et
  seulement si** `phrases_generees.json` était régénéré. Ajouter `profondeur` sans corriger
  `niveau` ne changerait **rien** à l'affichage de `/`.

### 2.4 `/paragraphes` est la seule fenêtre v7

| mesure | `/paragraphes` | page `/` |
|---|---:|---:|
| paragraphes / phrases | **9** | **207** |
| candidats | **19** | **369** |
| verdicts | **19** | **150** |
| segments avec `profondeur` | **169/169** | **0/369** |
| source des candidats | `generateur.analyser` à la volée | `phrases_generees.json` stocké |
| rendu | `profondeur ?? niveau` | `niveau` seul |

**Conclusion** : si « le service de la v7 » désigne **`/paragraphes`**, il fonctionne : 9/9,
19/19, 169/169 `profondeur`. S'il désigne **la page `/`**, il ne fonctionne pas : la page `/`
sert **l'ancien banc plat**, et la phrase « la page `/` sert la v7 » (note de la session
`e181ce02`, `semaine-autonome.md:41`) est une **projection**, pas l'état mesuré. Le contrôle
négatif est net : si `/` servait la v7, les 369 candidats stockés porteraient `profondeur` ;
**0/369** le font.

## 3. La mesure v7 sur les mêmes 207 phrases

Mesure rejouée à `389b99f` avec `mesure_arbre.mesurer()` (lecture seule, sans écrire
`donnees/mesure-arbre.json`) :

| mesure | page `/` (stocké) | v7 dynamique |
|---|---:|---:|
| phrases | 207 | **207** |
| candidats | **369** | **359** |
| segments | 2 414 | **2 308** |
| candidats à profondeur ≥ 3 | **0** | **99** (27,6 %) |
| distribution des profondeurs max | 10 / 277 / 82 (0/1/2) | **2 / 37 / 221 / 84 / 13 / 2** (0→5) |
| référents | non affichés sur `/` | **371 formes**, **294 avec candidat**, **77 sans** |
| phrases avec référent | — | **170/207** |

C'est le chiffre qui commande la reprise de la banque : **99 candidats profonds** existent dans
la mesure, **0** dans la vue affichée. La page `/` ne peut pas reprendre la validation tant
qu'elle montre l'ancien arbre ; la v7 est visible sur `/paragraphes`, pas sur `/`.

## 4. La migration : 5 verdicts à risque, ou 41 ?

### 4.1 Ce que la v1 comptait

La v1 liste **5 verdicts à risque si l'on régénère par index** : `p006-c2` (`compatible`),
`c023-c3` (`exclu`), `c056-c2` (`exclu`), `c056-c3` (`resolu`), `c064-c2` (`exclu`). Ce sont
les candidats qui **n'ont plus d'index** parce que la nouvelle liste est plus courte
(p006 2→1, c023 3→2, c056 3→1, c064 2→1). Le chiffre est juste **pour cette définition**.

### 4.2 Ce que la v2 mesure en plus

En prenant la signature exacte de la v1 — `(texte, type, rôle)` des segments, dans l'ordre —
et en la comparant aux candidats v7 des **mêmes phrases** :

| mesure | valeur |
|---|---:|
| verdicts de la banque | **150 lignes / 147 paires uniques** |
| paires dont la signature v7 existe | **106/147** |
| paires dont la signature v7 **n'existe pas** | **41/147** |
| lignes concernées (3 révisions) | **44** |
| dont candidats **sans index** (les 5 de la v1) | **5** |
| dont candidats **au même index mais contenu changé** | **36** |

Les **41 paires** sont réparties sur **18 phrases** : p001–p007 (14 paires), c002 (2), c004
(2), c009 (3), c011 (2), c013 (3), c020 (3), c023 (3), c043 (2), c056 (3), c064 (2), c065 (2).
Les **5 sans index** sont exactement celles de la v1 ; les **36 autres** existent à un index
qui contient désormais **un autre candidat**.

**Conséquence, et c'est la correction importante** : une migration **par index** ne perd pas 5
verdicts, elle en **perd 5 et en recolle 36 au mauvais candidat** — le pire des deux, parce que
le journal ne le dit pas. Une migration **par signature** ne « sauve » pas les 41 : elle
préserve les **106** qui ont un correspondant et laisse les **41** sans correspondance. C'est
la bonne sémantique (pas de faux lien), mais ce n'est pas « 0 verdict perdu ». La v1 disait
« 0 verdict perdu (les 5 à risque sont remappés) » : c'est faux pour les 36.

**Ce que cela impose** : soit garder l'ancien banc pour `/` (les 150 verdicts restent valides
sur l'ancien arbre), soit migrer les 106 et **mettre les 41 en quarantaine** pour re-jugement
explicite. Il n'y a pas de migration automatique qui conserve les 41 : leur contenu a changé.

### 4.3 Le contrôle de la signature

Le compte **41** est stable si l'on retire le rôle de la signature (texte + type), et si l'on
ne garde que le texte : les 41 candidats ont changé de **segments**, pas seulement de rôle.
Le compte **5** est stable comme « candidats sans index ». Les deux chiffres sont donc
reproductibles, mais ils ne mesurent pas la même chose ; il faut citer **5 sans index** et
**41 sans correspondance**, pas l'un pour l'autre.

### 4.4 Les 11 verdicts de `/paragraphes` ne sont pas dans ce lot

Les **41** sont des verdicts de la **banque `/`** (`donnees/validations.jsonl`). Les **19**
verdicts de `/paragraphes` (`paragraphes-validations.jsonl`) sont un autre journal : ils sont
committés à `389b99f`, la page les régénère à la volée et les rend **19/19**. La migration de
`/` ne doit pas être confondue avec le commit des 11 verdicts ; elle ne les menace pas.

## 5. Le pare-feu réseau

### 5.1 Ce qui est mesuré

| contrôle | résultat |
|---|---|
| service | **firewalld actif** (`ActiveState=active`, `SubState=running`) et **enabled** |
| démarré | **2026-11-03 19:34:02 EST**, pid **2062** |
| `firewall-cmd --state` (utilisateur) | **timeout**, code **124** ; `busctl` : `Connection timed out` |
| `nft list ruleset` | **`Operation not permitted`** |
| `iptables -L -n` | **`can't open lock file /run/xtables.lock: Permission denied`** |
| `journalctl -u firewalld` | **aucune entrée visible** (permissions) |
| `sudo -n true` | **mot de passe requis** ; aucun sudo sans mot de passe |
| ports en écoute | 22 (sshd), 25, 3080 (`dsh web`), 8765 (financemeteo, **127.0.0.1**), 8771 (docwatch), etc. |

**Le pare-feu est donc actif mais son jeu de règles n'est pas observable sans root.** Cette fiche ne
prétend pas que le port 8765 est « fermé » ou « ouvert » : elle constate qu'aucun service S
n'écoute, que le seul 8765 est **loopback** et appartient à un autre projet, et que la requête
de pare-feu échoue pour l'utilisateur.

### 5.2 Ce qui bloque l'accès réseau, dans l'ordre

1. **Le service n'est pas lancé** : aucun `serveur.py` S en écoute.
2. **Le port 8765 est pris** par `financemeteo` ; le lancement par défaut échouerait.
3. **Le serveur écoute 127.0.0.1 par défaut** (`serveur.py`, `--hote`), donc même un pare-feu
   ouvert ne le rendrait pas accessible depuis une autre machine.
4. **Le pare-feu** n'est un obstacle que si l'on passe à `--hote 0.0.0.0` ; il faut alors
   ouvrir le port en root, et le démon ne répond pas à l'utilisateur pour l'instant.

### 5.3 Si l'on veut exposer la page

**Option recommandée pour un seul utilisateur distant** — tunnel SSH, aucun changement de
pare-feu :

```bash
# sur la machine cliente
ssh -L 9000:127.0.0.1:9000 stephane@192.168.1.101
# puis, sur la cliente : http://127.0.0.1:9000/
```

**Option réseau local** — lier toutes les interfaces et ouvrir le port (root requis ; **non
testé ici**, et `firewall-cmd` devra d'abord répondre) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures
PYTHONDONTWRITEBYTECODE=1 python3 serveur.py --hote 0.0.0.0 --port 9000

# dans un autre terminal, en root, si firewalld répond :
sudo firewall-cmd --add-port=9000/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

Puis `http://192.168.1.101:9000/` ou `http://192.168.1.155:9000/`. **Ne pas** ouvrir 8765 :
il est déjà occupé ; **ne pas** tuer le processus 2725542.

## 6. La commande de lancement

### 6.1 Local (le cas mesuré)

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures
PYTHONDONTWRITEBYTECODE=1 python3 serveur.py --port 9000
```

- `--hote` vaut **127.0.0.1** par défaut ; `--port` vaut **8765** par défaut, mais 8765 est pris.
- `PYTHONDONTWRITEBYTECODE=1` évite d'écrire `__pycache__` dans le sous-module ; sans cela, le
  `git status` peut se salir.
- URLs : `http://127.0.0.1:9000/` (banc) et `http://127.0.0.1:9000/paragraphes` (v7).

### 6.2 Vérification

```bash
curl -s -o /dev/null -w 'GET / %{http_code}\n' http://127.0.0.1:9000/
curl -s http://127.0.0.1:9000/api/phrases | python3 -c \
  'import json,sys; d=json.load(sys.stdin); print(len(d["phrases"]), "phrases", sum(len(p["candidats"]) for p in d["phrases"]), "candidats")'
curl -s http://127.0.0.1:9000/api/paragraphes | python3 -c \
  'import json,sys; d=json.load(sys.stdin); print(len(d["paragraphes"]), "paragraphes", sum(len(p["candidats"]) for p in d["paragraphes"]), "candidats")'
```

Attendu : `GET / 200`, **207 phrases / 369 candidats** pour `/api/phrases`, **9 paragraphes /
19 candidats** pour `/api/paragraphes` — c'est exactement ce que la mesure a rendu.

### 6.3 Arrêt

```bash
# arrêter le serveur lancé sur 9000 (remplacer <pid> par celui affiché au démarrage)
kill <pid>
# ou, si l'on est sûr que c'est le bon port :
fuser -k 9000/tcp
```

**Ne jamais** faire `fuser -k 8765/tcp` sans vérifier : c'est le port de `financemeteo`.

### 6.4 Réseau local

```bash
PYTHONDONTWRITEBYTECODE=1 python3 serveur.py --hote 0.0.0.0 --port 9000
```

Voir § 5.3 pour le pare-feu et le tunnel. Le serveur imprime
`banc de structures · http://0.0.0.0:9000 · 207 phrases` ; l'URL réelle est
`http://192.168.1.101:9000/` (ou `.155`).

## 7. Ce qui reste à S

| # | chantier | état mesuré | prochaine action |
|---:|---|---|---|
| 1 | **Page `/` en v7** (A1) | `work/banque-v7/` **absent** ; `phrases_generees.json` du **02/11** (200 phrases / 355 candidats, 0 `profondeur`) ; `app.js` lit `niveau` | décider : **garder l'ancien banc** ou **régénérer** ; si régénération, signature + **106 conservés** + **41 en quarantaine** ; ne pas migrer par index |
| 2 | **Référents** (A2) | **9/16** mappings uniques faux (12/28 occurrences), **0 note** ; a008 = 0/5 | corriger les 14 occurrences / 12 formes, avec note ; forcer la résolution avant le verdict |
| 3 | **Rétro-traduction** (A3) | **0/9**, aucun harnais FR→EN→FR ; `DEEPSEEK_API_KEY` et `DEEPSEEK_KEY_FILE` **absents de l'env** ; fichier `~/.config/drave/deepseek.key` **présent** (36 o, 0600, 03/11), **non testé** | écrire `work/retro-traduction/` (9 prompts, 18 appels), passer la clé par `DEEPSEEK_KEY_FILE`, mesurer chrF + 2 relectures |
| 4 | **Couverture de la banque** | **74/207** phrases complètes (35,7 %), **133** sans verdict, **147/369** candidats, **1 note**, **1 annotateur** | reprendre après la migration (point 1) ; second lecteur, double-codage |
| 5 | **Docs S** | la v1 et `semaine-autonome.md:41` disaient **8 verdicts** / **11 non committés** / « `/` sert la v7 » ; `en-cours` et `roadmap` sont mis à jour par cette fiche | vérifier que `/` non v7 et 41 à re-juger restent la ligne S |
| 6 | **Service / pare-feu** | aucun service S ; 8765 pris ; firewalld actif non interrogeable ; défaut loopback | lancer sur **9000** ; tunnel SSH ou ouverture root ; ne pas toucher 8765 |
| 7 | **71 langues** | lexique **B7** (35 concepts, 1 433 couples), **0/71** testée comme référents ; UDHR = **456 langues** | retirer « 71 langues de l'UDHR » du plan S, ou annoter l'UDHR |
| 8 | **Branche / pointeur** | à la mesure : sous-module `389b99f` poussé (`origin/master`, 0/0) ; parent `s/v7` = `292c70b5`, **1 commit d'avance** sur `origin/s/v7` (C1, pas S) ; cette fiche ajoute C2 | pousser / merger `s/v7` quand les autres sessions sont au repos |

**Le point de décision n° 1** est le seul qui bloque la reprise de la banque `/` : tant que `/`
sert les 369 candidats du 02/11, l'humain rejuge l'ancien arbre plat. Le correctif v7 est
visible sur `/paragraphes`, mais la banque de phrases est sur `/`. La migration n'est pas un
simple `git add` : c'est un choix de données (106 conservés, 41 re-jugés) et un changement de
`phrases_generees.json` — donc une écriture dans `tools/structures/`, qui n'appartient pas à
cette fiche.

## 8. Ce qui pourrait rendre cette fiche fausse

- **Le port 8765 se libère** (ou `financemeteo` s'arrête) : la commande par défaut redevient
  utilisable ; les mesures de § 2.1 changent.
- **Quelqu'un lance le serveur S** entre-temps : « aucun service en écoute » n'est vrai qu'à
  l'instant mesuré. Le serveur de mesure sur 9000 a été arrêté.
- **Le pare-feu change** ou root devient disponible : `firewall-cmd` peut répondre et montrer
  des ports ouverts ; cette fiche ne prouve pas l'état des règles, seulement l'échec de la
  lecture utilisateur.
- **Le sous-module bouge** : `389b99f`, les 19 lignes, les 359 candidats, les 99 à ≥3, les
  304/65/55/10 et les 41 dépendent de ce commit. Un commit S qui régénère `phrases_generees.json`
  change tous ces chiffres.
- **La signature change de convention** : le compte **5 sans index** est stable ; le compte
  **41 sans correspondance** utilise `(texte, type, rôle)`. Il est stable en texte seul et en
  texte + type, mais une autre définition (par exemple avec `attachement`) pourrait le
  déplacer. Le point robuste est : **les 5 ne sont pas les 41**.
- **La migration garde l'ancien banc** : si S décide de ne pas migrer `/`, les 41 verdicts ne
  sont pas « à risque » ; ils restent valides sur l'ancien arbre. La fiche décrit le risque
  **conditionnel** à une régénération.
- **Les tests passent, mais pas la passe complète des portes** : 56/56 tests du sous-module,
  pas la passe complète des portes du parent. Un rouge de porte n'est pas couvert ici.
- **La clé DeepSeek** : le fichier existe, mais aucun appel n'a été fait ; il peut être expiré
  ou invalide. La rétro-traduction reste non mesurée.
- **Les 150 verdicts** sont un seul annotateur, une seule journée ; les taux d'acceptation ne
  sont pas une accuracy.
- **La mesure de `/`** a été faite sur **9000**, pas sur 8765 ; c'est le même code et les mêmes
  données, mais l'URL du service décrit est différente.

## 9. Fichiers lus, non modifiés

- `tools/structures/serveur.py`, `generateur.py`, `mesure_arbre.py`
- `tools/structures/static/app.js`, `static/paragraphes.js`, `static/index.html`
- `tools/structures/donnees/phrases.json`, `phrases_generees.json`, `paragraphes.json`
- `tools/structures/donnees/paragraphes-validations.jsonl`, `validations.jsonl`
- `tools/structures/tests/` (lus/exécutés : **56 tests**, aucun fichier suivi modifié)
- `tools/structures/.git` (HEAD, status, remote)
- `reports/rapport-coordination-s.md`, `rapport-etat-s.md`, `rapport-s-paragraphes.md`,
  `pensee-etat-s.json`
- `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `docs/pilotage/chantiers.md`,
  `docs/pilotage/semaine-autonome.md`
- `tools/llm/deepseek.py`, `tools/structures/llm.py` (lecture de la clé)
- `~/.config/drave/deepseek.key` (taille et permissions seulement, contenu non lu)
- `/proc`, `ss`, `systemctl`, `firewall-cmd`, `nft`, `iptables` (lecture seule)

**Aucune écriture dans `tools/structures/`** : le sous-module est resté propre
(`git status --porcelain` vide) ; le serveur de mesure a été arrêté ; aucun `POST` n'a été
envoyé.

## 10. Références

- [rapport-coordination-s.md](rapport-coordination-s.md) — la v1, avant le commit.
- [rapport-etat-s.md](rapport-etat-s.md) — l'audit 19/19, la page `/` et les référents.
- [rapport-s-paragraphes.md](rapport-s-paragraphes.md) — les neuf paragraphes d'Alice.
- [rapport-s-fait-divers.md](rapport-s-fait-divers.md) — la v7 (61/61, 144/144).
- [rapport-s-banque-partielle.md](rapport-s-banque-partielle.md) — le négatif « 277/369 plats ».
- [en-cours.md](../docs/pilotage/en-cours.md) — l'état S mis à jour.
- [roadmap.md](../docs/pilotage/roadmap.md) — la ligne S et la file « jamais en attente ».
- [serveur.py](../tools/structures/serveur.py) — le service, ses routes et ses défauts.
- [app.js](../tools/structures/static/app.js) — le rendu de `/` (`niveau`).
- [paragraphes.js](../tools/structures/static/paragraphes.js) — le rendu de `/paragraphes`
  (`profondeur ?? niveau`).
