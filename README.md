# Drave

**Un moteur d'inférence qui exécute les grands modèles comme des ÉVÉNEMENTS, pas comme des
matrices** : les GGUF sont lus **en place** (mmap, aucune copie, aucune requantification), les
projections se font en listes creuses ou en produit dense, et le calcul se **découpe en régions**
réparties sur plusieurs processus ou plusieurs machines.

- **Rust, `std` seul, zéro dépendance** — `drave-core/`, ~14 000 lignes, profil `release` = le
  binaire de mesure.
- Ce qui tourne : du 0,5 B au 120 B sur le CPU de cette machine, MoE compris, avec conversation,
  trace d'exécution, budgets déclarés et pannes nommées.
- Ce que ça vaut, tâche par tâche : la campagne du 8-9 octobre, **une fiche par expérience**,
  [`reports/campagne-benefices.md`](reports/campagne-benefices.md).

```bash
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --flux --prompt "Explique le ciel bleu en une phrase." \
    --n 64 --ctx 512 --threads 16 --temp 0
```

---

## Démarrer une session de travail

**Lire, dans cet ordre** (10 minutes, et tout le reste est en lien depuis là) :

1. [`REPRISE.md`](REPRISE.md) — la check-list de démarrage : ce qui doit être vert, les pièges de
   l'environnement, les règles de méthode ;
2. [`docs/etat.md`](docs/etat.md) — l'**index des modules** : pour chacun, sa roadmap, son état,
   sa prochaine action ;
3. [`journal/`](journal/README.md) — les **événements**, par jour et par thème (celui du jour
   d'abord) ;
4. [`docs/organisation-du-depot.md`](docs/organisation-du-depot.md) — **où écrire quoi**
   (`docs/` = fond et état, `reports/` = une fiche par expérience, `journal/` = les faits datés).

## Où est quoi

| besoin | document |
|---|---|
| l'état des douze capacités du cerveau distribué | [`docs/etat-cerveau.md`](docs/etat-cerveau.md) |
| les repères qui ne doivent pas bouger | [`docs/references-non-regression.md`](docs/references-non-regression.md) |
| ce que le dépôt **ne sait pas** faire (avec la mesure) | [`docs/manques.md`](docs/manques.md) |
| les plans et roadmaps | [`docs/plan-cerveau-complet.md`](docs/plan-cerveau-complet.md), [`docs/roadmap-drave.md`](docs/roadmap-drave.md), [`docs/modele-pour-drave.md`](docs/modele-pour-drave.md) |
| les mesures, une fiche par expérience | [`reports/`](reports/) · campagnes éclatées : [`reports/campagne-benefices/`](reports/campagne-benefices/), [`reports/toutes-langues/`](reports/toutes-langues/) |
| le vocabulaire | [`docs/glossaire.md`](docs/glossaire.md) |
| l'histoire du projet | [`docs/histoire.md`](docs/histoire.md) |

## Ce que le dépôt traque (et pourquoi il est écrit ainsi)

Le défaut le plus coûteux n'est pas un calcul faux : c'est **un réglage qui ne fait rien**, une
**mesure qui ne mesure rien**, une **porte qui ne peut pas échouer**. Chaque capacité est donc
livrée avec sa **porte** (l'invariant qui la vérifie), ses **tests**, sa **mesure** et sa
**documentation** — et une erreur corrigée reste écrite **à côté** de la valeur d'origine.

Les trois invariants : le crate reste `std` seul · le profil `release` est le binaire de mesure
(toute promotion se paie d'un passage des portes) · on ne laisse jamais l'arbre cassé.

## Vérifier l'arbre

```bash
cd drave-core && cargo test --release          # 122 tests
cd .. && tools/toutes-les-portes.sh            # toutes les portes, ~1 h, aucune sautée
# le nombre et les repères du jour : docs/references-non-regression.md
tools/porte-flux.sh                            # la porte de non-régression du calcul, ~2 min
```
