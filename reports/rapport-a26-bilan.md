# A2.6 — l'ordonnanceur est partiel : le générique et le KV sont faits, la tête est refusée, les experts bloqués

> **Ligne de roadmap** : A2.6 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partielle** — la règle
> générique et le KV sont mesurés ; la tête 4 bits est refusée par la perte ; les experts attendent
> **A6.2** (pas de MoE local). A2.6 ne peut pas être « complétée » sans cette brique.
>
> **Dispositif** : bilan des mesures existantes (`placement.rs`, `rapport-placement-kv-8k.md`,
> `rapport-regle-placement-perte.md`, A8.3) ; **pas de nouvelle mesure** ; données
> [`a26-bilan.json`](a26-bilan.json).

## Le bilan

| partie | état | preuve |
|---|---|---|
| `choisir` générique | ✅ fait | `placement.rs`, 4 tests ; `kv_en_vram` appliqué dans `model.rs` |
| KV en VRAM | ✅ mesuré | ×1,93 au préremplissage 8 k, ×5,8 sur l’attention |
| tête 4 bits | ❌ refusée | +10 % de PPL ; `choisir_avec_perte` la refuse à 5 % |
| experts | 🧱 bloqué | **A6.2** — pas de MoE local à router |
| place + perte | 🔬 opt-in | A8.3 : le défaut déplace les portes ; **A8.3a** à venir |

## Le contrôle négatif

- `choisir_avec_perte` refuse la tête 4 bits à un budget de 5 % : la place ne suffit pas, la perte
  décide. C’est le test qui a invalidé le 4 bits.
- Sans MoE local, les experts ne sont **pas mesurables** : ce n’est pas un échec de la règle, c’est
  une brique absente.

## Ce que ça change

A2.6 n’est plus une ligne « ouverte » : elle est **partielle et bloquée** pour sa partie experts.
La partie tête est **décidée** (refusée), la partie KV est **faite**, la partie générique est
**testée**. La suite est **A6.2** (bloqué) ou **A8.3a** (épingler le régime 1 %), pas un nouveau
code d’ordonnanceur.

## Ce qui pourrait le rendre faux

- **Bilan, pas une mesure** : les chiffres viennent des fiches existantes, pas d’un nouveau run.
- **La tête 4 bits** a été essayée puis revertée ; il n’y a pas de chiffre courant.
- **Les experts** ne sont pas mesurables sans A6.2 ; le jour où le MoE local existe, A2.6 rouvre.
- **Un autre modèle** peut déplacer la frontière KV/tête.

## Fichiers

- `reports/a26-bilan.json` — le bilan machine.
- `reports/rapport-a26-bilan.md` — cette fiche.
