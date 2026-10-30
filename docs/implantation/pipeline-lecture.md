# Le pipeline de lecture (R0.6) — de la question à la réponse citée

> **Ligne de roadmap** : R0.6 · **Code** : `tools/lecture.py` · **Porte** : `tools/porte-lecture.sh`
> **Dépend de** : R0.1 (le document), R0.2 (le contrôleur), R0.3 (le banc).

## 1. Le besoin

R0.1 a donné le manifeste, R0.2 le contrôleur, R0.3 le banc — et R0.4/R0.5 ont mesuré les
limites (une tête apprise ne bat pas BM25 ; un routeur global ne transfère pas). Il manquait
l'**assemblage** : une commande qui prend un document et une question, et rend une réponse
**avec sa source**, dans un budget, avec une trace **rejouable**. Sans elle, les trois briques
restent des mesures, pas un lecteur.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | un document (chemin), une question, un budget (fraction du document), un lecteur |
| **sortie** | la réponse **ou** un refus motivé, la source (région, offset, sha), la trace, le coût |
| **budget** | le coût est en **octets lus** ; il ne dépasse jamais la fraction demandée |
| **provenance** | la réponse porte sa région, son `start`, son `octets`, son `prov` ; les octets cités sont **vérifiables** dans le flux |
| **rejeu** | aucune horloge, aucun aléa : deux exécutions rendent le **même JSON** (hors durée) |
| **refus** | si le meilleur score est sous le **seuil** (1,0), la réponse est « insuffisant » — le pipeline ne rend pas un passage au hasard |
| **cascade** | `--lecteur cascade` : étage 1 span/extractif, étage 2 le modèle si la **confiance** est sous le seuil — la relecture comme **changement de modalité** (R06 v4) |
| **calibration** | `--calibration FICHIER` : le seuil vient d'un fichier daté (`tools/calibrer.py`), pas d'une ligne de commande — la politique est publiée et reproductible (R06 v6) |

**Sortie** (extrait) :

```json
{"document": "…", "source_sha256": "…", "question": "…", "lecteur": "extractif",
 "budget": {"fraction": 0.3, "octets": 3132, "total": 10441},
 "trace": {"evenements": [...], "octets_lus": 2516, "passages_lus": 19, "raison": "…"},
 "reponse": {"trouve": true, "texte": "Le mode dense coûte 3 663 octets…",
             "region": "r00032", "start": 8015, "octets": 324, "score": 8.956, "prov": {...}},
 "duree_s": 0.02}
```

## 3. Les trois régimes

| régime | quand | ce que ça rend | coût |
|---|---|---|---|
| **extractif** (défaut) | la question partage ses mots avec le document | le passage qui répond, avec sa citation | ~0 |
| **modèle** (`--lecteur modele`) | la question est une **paraphrase** (R0.3 durci) | une réponse générée, le 0,5 B sur GPU | ~1,9 s |
| **refus** | le meilleur score est sous le seuil | « insuffisant », avec le score | ~0 |

Le choix par défaut est l'**extractif** : sur 249 questions lexicales il donne 0,72–1,00, et il
ne coûte rien. Le modèle ne s'appelle **que** quand le refus indique que la question ne partage
rien avec le document — c'est la leçon de R0.3 : pour une valeur numérique, rendre le passage
bat générer.

## 4. Ce que la porte vérifie

| contrôle | ce qu'il prouve |
|---|---|
| réponse connue trouvée | le chemin nominal |
| **budget tenu** | `octets_lus ≤ fraction × total` |
| **provenance** | les octets cités sont exactement dans le flux |
| **rejeu** | deux exécutions → même JSON |
| **refus** | une question hors sujet ne reçoit pas de réponse |
| **closed-book** | budget nul → aucune réponse |

## 5. Ce qui est mesuré

| régime | mesure | chiffre |
|---|---|---|
| **pilote** (20 questions main) | acceptées · justes · provenance | 19/20 · **12/20 = 0,600** · 19/19 |
| **hors sujet** (10 questions) | refus | **10/10** |
| **paraphrases** (8 questions) | extractif · modèle | **3/8** · **7/8** |
| **rejeu** | deux exécutions | identique |

**Le seuil 1,0** attrape les questions qui ne partagent **rien** avec le document (score 0,00).
Un seuil plus haut (3,8) séparait, sur le document du pilote, les réponses justes (3,94–11,08) du
faux positif hors sujet (3,56) — mais **mesuré sur 84 paraphrases, il refusait 32 % des questions
et coûtait 6,7 points** pour un refus gagné sur dix. Rejeté. L'échelle BM25 brute ne se transporte
pas d'un document à l'autre (la leçon de R0.5) : le seuil s'expose et se calibre par corpus. Détail
et limites : `reports/rapport-r06-pipeline.md`.

## 6. Ce qui pourrait le rendre faux

- **le seuil (1,0) est calibré** sur `format-flux.md` : une question réelle y score ~9, une
  question hors sujet 0,00 ; sur un document au vocabulaire pauvre, le seuil pourrait refuser
  une vraie question. Il est exposé (`--seuil`) et doit être calibré par corpus ;
- **le refus est lexical** : une paraphrase légitime est refusée par l'extractif — c'est
  voulu (elle doit passer au modèle), mais l'utilisateur doit le savoir ;
- **le modèle n'a pas de refus** : il répond toujours ; sa réponse n'a pas de provenance ;
- **le budget en octets** ignore le coût CPU réel (découpage, score) ;
- **les offsets** sont ceux du flux reconstruit (régions concaténées), pas du fichier source :
  la provenance `prov` donne le fichier d'origine, l'offset donne le flux.

## 7. Voir aussi

- [Le graphe de document](document-graph.md) — le manifeste et ses trois contrôles.
- [Le contrôleur de lecture](lecteur-controleur.md) — la politique et la trace.
- [Le banc de lecture](banc-lecture.md) — ce que les lecteurs valent, mesuré.
