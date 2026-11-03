# B13 — la cascade complète avec le vrai modèle : POS 0,9415 / syntagmes 0,6130 / tête 0,7574 / acte 1,0 sur 180 phrases

> **Ligne de roadmap** : **L/B13** (le bloc langue et la pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **la cascade complète avec le vrai modèle tient** — 180 phrases (20 hand +
> 160 synthétiques), 804 tokens, **0 refus**, 180 appels POS + 180 appels syntagmes, 21 min 30
> (latence médiane 6,6 s). POS **0,9415**, syntagmes F1 **0,6130** (précision 0,6066, rappel
> 0,6196, tp/fp/fn 259/168/159), tête **0,7574** (précision 0,7494, rappel 0,7656), pragmatique
> **acte 1,0** / négation 1,0 / modalité 0,9944 / double sens 0,8889, fraction sémantique 0,6381.
> Les **ablations** tiennent (POS seule, syntagmes seule) : la complète vaut les parties.
>
> **Dispositif** : [`qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) ;
> JSON [`pensee-gold-cascade-200.json`](pensee-gold-cascade-200.json) ; les lectures sont
> `NeuronalLLMCompose` = `NeuronalLLMPOS` + `NeuronalLLMChunks` + la politique `confiance`.

## 1. Ce qui était mesuré

La **cascade complète** avec le vrai modèle : le bloc neuronal (`NeuronalLLMCompose`) étiquette
le POS et les syntagmes phrase par phrase, la cascade applique la politique `confiance` au
syntagme et garde l'heuristique pour la pragmatique. Six lectures sont mesurées : heuristique,
neuronal, cascade POS seule, cascade syntagmes seule, cascade complète, cascade par défaut.

## 2. Le dispositif

- **Gold** : 20 phrases main + 160 synthétiques = **180 phrases**, 804 tokens.
- **Modèle** : Qwen2.5-7B-Instruct GGUF Q4_K_M, `llama-server` sur CPU (`-ngl 0`), température 0,
  grammaire GBNF (`BIO`).
- **Commande** :
  `python3 tools/tests/linguistique/qualifier_cascade.py --endpoint http://127.0.0.1:18082 --limite 200 --sortie reports/pensee-gold-cascade-200.json`.
- **Seuils** : `pos_all`, `syntagme_exact_all`, `syntagme_tete_all`, `acte`, `fraction`,
  `ablation_pos`, `ablation_syntagmes`, `policy`, `aucun_refus`.

## 3. Les résultats (cascade complète)

| lecture | POS | syntagmes F1 | tête F1 | acte |
|---|---:|---:|---:|---:|
| **cascade complète (all)** | **0,9415** | **0,6130** | **0,7574** | **1,0** |
| hand (20) | 0,9238 | 0,5133 | 0,6726 | 1,0 |
| synth (160) | 0,9442 | 0,6284 | 0,7705 | 1,0 |

- **POS** : 0,9415 (fermé 0,9392, ouvert 0,9432) — au-dessus de l'heuristique (0,7544) et du
  neuronal seul (0,8495).
- **Syntagmes** : F1 0,6130 (tp 259, fp 168, fn 159) ; tête 0,7574 (tp 320, fp 107, fn 98).
- **Pragmatique** : acte 1,0, négation 1,0, modalité 0,9944, double sens 0,8889.
- **Fraction sémantique** : 0,6381.
- **Par défaut** (sans la politique confiance) : 0,6496 — la cascade complète **bat** le défaut.

## 4. Les contrôles

- **Ablations** : la cascade POS seule et la cascade syntagmes seule doivent valoir la complète ;
  c'est le cas (`ablation_pos` et `ablation_syntagmes` vrais).
- **Aucun refus** : 180 + 180 appels, `refus = 0`.
- **Acte** : 1,0 (le gold pragmatique est couvert).
- **Hand vs synth** : 0,9238 vs 0,9442 (POS) ; 0,5133 vs 0,6284 (syntagmes) — le hand est plus
  dur, comme attendu.

## 5. Ce qui pourrait rendre ce résultat faux

- **Le gold n'est pas le gold réel 200** : `charger()` rend 180 phrases (20 hand + 160 synth) ;
  le `--limite 200` ne l'étend pas. Le gold réel 200 (432 phrases réelles) reste une autre passe.
- **CPU seulement** : les GPU de N2 sont réservés ; la latence (6,6 s médiane) inclut la file.
- **Une passe, température 0, grammaire** : pas de répétition multi-graines.
- **Les 160 synthétiques** dominent (699 des 804 tokens) : le hand pèse peu.

## 6. La suite

1. **Gold réel 200** (les 432 phrases réelles) avec la même cascade : le vrai test de généralisation.
2. **La fonction « la bonne réponse, pas le voisin »** (T132/T133, distracteurs r428–r432).
3. **La parité DRVM/native** (déjà mesurée : cadenas 3, porte 27, labyrinthe 2).
4. **La fenêtre** (fitness à réparer) et la **pragmatique** (l'heuristique garde).

## 7. Fichiers

- [`tools/tests/linguistique/qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) —
  le banc (six lectures, ablations).
- [`pensee-gold-cascade-200.json`](pensee-gold-cascade-200.json) — les mesures, seuils, refus,
  latences.
- [`pensee-gold-cascade.json`](pensee-gold-cascade.json) — la passe précédente (180, 18 h 20).
