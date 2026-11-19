# A2.6 — la règle des experts est branchée (trace sous opt-in) : 1,10 Go/jeton, 6,99 Go/s, 156,9 ms → VRAM

> **Ligne de roadmap** : A2.6 (les experts et la tête) · **Date** : 2026-11-19 · **Verdict** : ✅
> **branchée** — sous `DRAVE_PERTE_MAX` (l'opt-in du KV), la construction du moteur appelle la règle
> et imprime la trace sur le vrai 30B : `experts : 1.10 Go/jeton · 8 lecteurs · bande 6.99 Go/s ·
> 156.9 ms/jeton → VRAM (VRAM libre 14.57 Go, RAM libre 68.72 Go, budget 1000.0 ms)`. **Sans
> l'opt-in, aucune trace et le défaut ne bouge pas.** 146 tests, les cinq portes A2.6 vertes.
>
> **Dispositif** : `placement::octets_experts(total, n_expert, n_expert_used)` (arithmétique pure,
> testée) · `model::octets_experts_par_jeton(g, couches, n, n_used)` (somme des trois tenseurs
> `ffn_*_exps` par couche via `Gguf::octets_tensor`) · la trace au site de construction, après
> `libre_vram` · `qwen3-30b-a3b-Q4_K_M.gguf`, `--ppl --ctx 512 --limit 8`.

## Ce que le branchement fait, et ne fait pas

**Fait** : la règle **voit** le vrai modèle (le helper scanne les tenseurs d'experts du fichier),
**calcule** ce qu'un jeton lit (1,10 Go), **applique** la bande mesurée (6,99 Go/s à 8 lecteurs),
**nomme** le coût (156,9 ms/jeton) et le support (VRAM), et **refuserait** en le disant si le budget
ne passait pas (le message est testé).

**Ne fait pas** : la **décision**. Le cache VRAM/RAM des experts reste réglé par
`DRAVE_GPU_EXPERTS_GO` / `DRAVE_EXPERTS_RAM` ; la règle n'est pas encore le chemin de décision
(elle l'est pour le KV depuis A5.3). C'est la différence entre « branchée » et « décide ».

## Les contrôles

- **Le défaut ne bouge pas** : même commande sans `DRAVE_PERTE_MAX` → **aucune trace**, même chemin.
- **Le chiffre est la mesure** : la trace rend **1,10 Go/jeton** et **156,9 ms**, les valeurs du
  rapport de la bande (1,097 Go ; 156,95 ms) — le helper scanne donc les bons tenseurs.
- **La porte** `porte-a2.6-experts` nomme les cinq tests (bande, coût, refus, VRAM, trace) ;
  `porte-flux`, `porte-pont`, `porte-coupe`, `porte-echange-experts` sont **vertes** : le chemin de
  chargement n'a pas bougé, l'invariant du routage non plus.
- **146 tests** (`cargo test`) : 145 + `les_octets_des_experts_sont_par_jeton`.

## Ce qui pourrait le rendre faux

- **Les clusters** : quand les experts sont dans des fichiers séparés (`cluster-XX.gguf`), le scan
  du seul fichier principal rend **0** — la trace serait muette ou fausse. À couvrir avant de s'en
  servir comme décision.
- **L'opt-in est partagé avec le KV** : `DRAVE_PERTE_MAX` change aussi la précision du KV (int8) ;
  la trace des experts est un effet de bord de cet opt-in, pas un drapeau propre.
- **La trace ne décide pas** : un déplacement du défaut (le cache experts) reste à faire, et il
  faudra les portes du régime 1 % pour l'épinger.

## Ce que ça change

A2.6 n'est plus « une règle écrite et testée mais muette dans le moteur » : elle est **appelée**,
elle **parle** sur le vrai modèle, et son refus est prêt. La décision (le cache experts réglé par la
règle) et la consolidation des trois tables de bandes de `materiel.rs` restent les deux pas suivants.

## Voir aussi

- [la bande des experts](rapport-a2.6-bande-experts.md) · [la règle](rapport-a2.6-bande-experts.md#la-règle-sait-chiffrer-les-experts-18-11-après-la-mesure) ·
  [le backlog A2.6](../docs/pilotage/backlog/A2.6-ordonnanceur.md) · [le mode d'emploi](../docs/pilotage/backlog/A2.6-ordonnanceur.md#le-branchement-mode-demploi-relevé-le-19-11)

## La décision (19/11, 12 h) — le cache des experts passe par la règle

Le second pas est fait : sous `DRAVE_PERTE_MAX`, la création du **cache VRAM des experts** est
soumise à `choisir_experts` (les mêmes octets/jeton, la même bande, le même budget de 1 s). Si la
règle rend **VRAM** — le cas sur cette machine, 156,9 ms < 1 s — le cache est créé comme avant ; si
elle **refuse**, le cache n'est pas créé et le message nommé dit pourquoi. Sans l'opt-in, le
comportement reste celui des drapeaux (`DRAVE_GPU_EXPERTS`, `DRAVE_GPU_EXPERTS_GO`).

Testé sur le 30B avec `DRAVE_GPU_EXPERTS=1 DRAVE_GPU_EXPERTS_GO=2 DRAVE_PERTE_MAX=1` : une seule
trace `experts : 1.10 Go/jeton · … → VRAM` puis `[gpu] cache d'experts : budget 2.0 Go`. Les cinq
portes A2.6 restent **vertes**, 146 tests. Restent : les **clusters** (le scan du seul fichier
principal rend 0) et la consolidation des trois tables de bandes de `materiel.rs`.

## Les deux dernières pièces (19/11, 16 h 40)

- **Les bandes** : `materiel::cout_par_jeton` ne porte plus ses trois constantes (VRAM 84,9, RAM
  22,5 **morte**, NVMe **31**) — il lit `placement::BANDE_*` et la bande **mesurée** des experts
  (7,0 Go/s à 8 lecteurs). Le coût estimé du 30B passe d'environ **160 à 231 ms** : la différence
  est celle du pread à 16 lecteurs (31 Go/s), qui n'est pas le chemin par défaut. Aucune fiche ne
  citait ce chiffre (vérifié par recherche).
- **Les clusters** : quand le scan du fichier principal rend **0** (modèle en clusters), la règle
  **ne tranche pas** — un message le dit et les drapeaux restent maîtres, au lieu d'une trace à
  0 Go/jeton. Lire réellement les clusters (leurs fichiers) reste à faire.
- 146 tests, `porte-a2.6-experts` et `porte-ressources` vertes.
