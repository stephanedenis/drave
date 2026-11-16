# Fiche du modèle natif — `drave-n0-rope` (34,3 M)

> **Ce que cette fiche est.** La **carte d'identité** du modèle natif : ce qu'il est, sur quoi il a
> été entraîné, ce qu'il sait faire, ses limites, sa licence et son usage prévu. Elle ne remplace
> pas les mesures : elle les **situe**. Les chiffres renvoient à leurs fiches.

## 1. Identité

| champ | valeur |
|---|---|
| nom | **`drave-n0-rope`** (le checkpoint `mix1024-60k`) |
| paramètres | **34 301 224** |
| architecture | `drave-n0` : **d_model 384**, **6 blocs**, **4 têtes**, la **MoE** (8 experts, `expert_hidden` 512, top-2, k-WTA 0,25), la **pensée** (2 pas `tanh`), les têtes précoces (blocs 1, 3, 5), le pont de région |
| positions | **RoPE** |
| tokenizer | **octets** (vocab 256) — pas de BPE |
| contexte | **1 024** octets |
| fichier | le `.pt` (`work/n2ac/mix1024-60k.pt`) et le **DRVM** (`work/n2ac/mix1024-60k.drvm`, **130,9 Mo**, `inspect` **sans torch**) |

## 2. L'entraînement

| champ | valeur |
|---|---|
| corpus | `data/wiki_mix/propre/train.txt` — **1,017 Go** (des articles de la Wikipédia française, le « propre ») |
| ratio | **29,7 octets/paramètre** (au-delà de la loi de Chinchilla, 20) |
| pas | **30 000**, le lot 8, la séquence 1 024, le lr 0,0003 |
| durée | **13 331 s** (~3,7 h, CPU) |
| perte finale | **1,025** |
| validation | **PPL 2,40** sur 65 536 jetons (`val.txt`) |

**La provenance du corpus.** Des articles de la Wikipédia française (CC-BY-SA) — le corpus est
**hors dépôt** (`data/`, gitignoré) et sa licence **suit celle de la source** : toute
redistribution du modèle doit créditer la Wikipédia et partager à l'identique.

## 3. Ce qu'il sait faire (mesuré)

- **Modéliser** : PPL **2,40** (byte-level) — il connaît les régularités du français écrit.
- **Produire des mots** : **0,87** de mots valides en greedy (contre 0,34 au hasard) —
  [`banc-generation.json`](banc-generation.json).
- **Repérer les verbes** : **6,9 GV** par génération (contre 2,3 au hasard) —
  [`banc-grammaticalite.json`](banc-grammaticalite.json).

## 4. Ce qu'il ne sait pas faire (mesuré)

- **Composer une phrase** : la cohérence s'arrête au prompt + ~3 mots ; en greedy, un trigramme est
  répété **15 fois** ; en échantillonnage, des **pseudo-mots** apparaissent.
- **Tenir la glu grammaticale** : **0,335** de classes fermées (contre 0,79 au hasard) — des mots
  de contenu sans les déterminants et les prépositions.
- **Suivre une consigne** : le SFT de N4.6 mémorisait (24/24 vus, **0/4 tenus**).
- **Générer vite** : **36 octets/s** (byte-level, CPU).

## 5. L'usage prévu

**Ce qu'il peut faire dès aujourd'hui, sans promesse** : le **scoring** d'un texte (la PPL), les
**représentations** (les états internes, les têtes), la **lecture** (le prochain octet), et
l'**expérimentation** (le DRVM, la distillation).

**Ce qu'il ne peut pas faire** : écrire un texte, répondre, traduire, résumer. **Ne pas l'exposer
comme un assistant** : le banc de génération le dit (les collages).

## 6. Les conditions d'usage (le runtime)

- **torch** est nécessaire pour le `.pt` (absent de l'environnement de production ; installé en
  `/tmp/venv-natif` pour les bancs) ; le **DRVM** se lit sans torch, mais son **calcul** est torch.
- Le **GPU est réservé à Drave** (la règle 11) : l'inférence sur CPU est le chemin.
- Le checkpoint vit dans `work/n2ac/` (hors dépôt) : il n'y a pas de distribution versionnée.

## 7. Les limites de cette fiche

- Elle décrit **un** checkpoint (`mix1024-60k`) ; les autres (le 34 M absolu, le 21 M, le 11 M)
  ont leurs propres chiffres.
- Les mesures viennent de **20 prompts** et de **136 générations** : un échantillon.
- La licence du modèle n'est **pas** déclarée dans le dépôt : elle dépend de la source du corpus.

## 8. Fichiers

- [`rapport-banc-generation.md`](rapport-banc-generation.md) — le banc de génération.
- [`rapport-natif-exploitable.md`](rapport-natif-exploitable.md) — ce qui manque (chiffré).
- `work/n2ac/mix1024-60k.pt.json` — la configuration et la validation de l'entraînement.
- `work/n2ac/mix1024-60k.drvm` — le conteneur (130,9 Mo).
