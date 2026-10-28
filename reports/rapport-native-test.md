# N0.11 — test Rust de la passe avant native

> **Objet.** Ne plus dépendre d'un script Python pour vérifier l'exécution native : une petite
> fixture DRVM est versionnée et un test Rust la charge, l'exécute et vérifie les logits.

## Dispositif

- Fixture : `drave-core/tests/fixtures/tiny_n0.drvm`, **36 Ko**, **7 754** paramètres.
- Architecture minuscule : `d=8`, 1 bloc, 2 têtes, 2 experts, fenêtre 8, 1 pas de pensée.
- Test : `native::tests::execute_une_petite_fixture_drvm`.
- Vérifications : 256 logits, tous finis ; génération de 4 octets après `AB`.

## Résultat

```text
test native::tests::execute_une_petite_fixture_drvm ... ok
test result: ok. 2 passed; 0 failed; 133 filtered out
```

- Le test **ne dépend pas** de `/tmp` ni d'un checkpoint externe.
- Il couvre `Drvm::open`, `Native::open`, `forward` et `generer`.

## Lecture

- La passe avant native est maintenant **testée par le crate**, pas seulement par un script.
- La fixture est **petite** : elle teste la mécanique, pas la qualité.
- Le test vérifie la **forme** et la **finitude**, pas la parité numérique.

## Verdict

**N0.11 est atteint** : test Rust autonome de la passe avant native.

## Limites

- **Une seule fixture**, un seul chemin.
- **Pas de valeurs golden** : le test ne compare pas à des logits attendus.
- La parité multi-prompt reste le script Python N0.8.

## Fichiers

- Test : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- Fixture : [`drave-core/tests/fixtures/tiny_n0.drvm`](../drave-core/tests/fixtures/tiny_n0.drvm).
