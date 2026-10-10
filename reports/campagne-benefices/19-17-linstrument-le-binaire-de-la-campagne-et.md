> Campagne : **campagne-benefices** · expérience **17**
> Titre : 17. L'instrument : le binaire de la campagne était plus VIEUX que ses correctifs
> Date réelle : **2026-10-09 01:55 HAE** (source : commit `69cf405`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 17. L'instrument : le binaire de la campagne était plus VIEUX que ses correctifs

**Le fait.** `drave-core/target/release/drave` portait la date du 8 octobre 11 h 00.
Trois commits touchant `drave-core/src` sont **postérieurs** : `8de0612` (11 h 08,
`--ids-file` ignoré en mode réparti), `ddebb6b` (23 h 26, tokenizers SentencePiece),
`9cdfbd7` (00 h 05, le banc des encodages qui plantait sur les K-quants). Les
correctifs existaient donc dans les sources et **pas dans le binaire qui a mesuré
la campagne** — ils avaient été compilés à part (`CARGO_TARGET_DIR=/tmp/target-spm`)
pour ne pas déranger la campagne en cours, et jamais promus.

**La preuve, en une commande.** Le même texte, les deux binaires :

| binaire | « The river carries the logs to the mill » |
|---|---|
| celui de la campagne (8/10 11 h 00) | **31 jetons**, recolle `"Therivercarriesthelogstothemill"` |
| celui des correctifs (`/tmp/target-spm`, 00 h 02) | **8 jetons**, recolle `" The river carries the logs to the mill"` |

**Ce qui est touché, et ce qui ne l'est pas.** Seuls les modèles à tokenizer
**SentencePiece** (Mistral, Codestral, Llama, Gemma). Tous les autres — Qwen,
Qwen3-MoE, gpt-oss, V4 — sont en BPE byte-level, chemin qui n'a pas changé. Et le
dépôt porte la vérification : `--tokenize` imprime un contrôle de réversibilité, et
les six journaux de tokenisation de la campagne disent lesquels sont valides :

| modèle | contrôle de réversibilité (journal de la campagne) |
|---|---|
| Qwen2.5-0.5B · R1-1,5B · R1-14B · Qwen3-30B-A3B · gpt-oss-120B | **texte reconstruit identique ✅** |
| codestral-22B | **DIVERGE** — l'instrument a signalé lui-même sa propre ligne |

**Ce que cela change dans ce rapport** : la ligne « codestral-22B » de la grille
(§ 3) porte **35 657**, chiffre mesuré sur un texte dont les espaces étaient
mangés, et **117,91** après correctif — c'est le corrigé qui est retenu, et il a
été obtenu avec le binaire corrigé. Les fichiers d'identifiants en cache
(`ids_codestral-22B.txt`) sont, eux, **empoisonnés** : ils ont été produits par le
binaire périmé et doivent être refaits, pas réutilisés.

**Deux corrections de code sont nées de ce constat :**
1. le contrôle de réversibilité distingue maintenant l'écart d'**un espace de tête**
   — la convention `add_dummy_prefix` de SentencePiece, qui faisait afficher
   « DIVERGE à l'octet 0 » sur *tous* les modèles SPM pour un octet de convention —
   d'une **vraie** perte d'information, qui reste signalée comme telle ;
2. `DRAVE_SANS_EMPRUNT=1` devient obligatoire pour toute comparaison dense/listes :
   sans lui on compare deux schémas de quantification, pas deux chemins
   d'exécution (§ 22).

**Les correctifs sont maintenant PROMUS** (9 octobre, 5 h 46) : `cargo build
--release` refait, les **77 tests passent**, et le contrôle qui avait révélé le
problème donne le résultat attendu — Codestral découpe « The river carries the logs
to the mill » en **8 jetons** au lieu de 31, et recolle le texte exact. La porte de
répartition à deux nœuds a été **rejouée avec ce binaire** : perplexité 3,6064,
écart de flux **0.00e0**, porte tenue.

**La leçon de méthode** : un correctif non promu est un correctif qui n'existe pas,
et un cache d'identifiants ne porte pas la version de l'outil qui l'a écrit. Les
deux pièges du § 16 sont de la même famille — et celui-ci est le plus coûteux,
parce qu'il ne se voyait que sur un modèle sur six.

---
