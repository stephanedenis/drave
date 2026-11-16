# La copie de secours de S, pour l'intégration continue

`tools/structures` est un **sous-module** dont l'URL versionnée est un **chemin local**
(`/home/stephane/.../drave-structures`) : un runner GitHub hébergé ne peut pas le récupérer.
Or `test_produit.py`, `porte-produit.sh` et l'autotest ont besoin du **générateur S** et du
**gold de l'analyseur** pour rendre les rôles (`agent`, `predicat`) et les cibles.

Ce dossier porte donc une **copie de secours**, utilisée uniquement quand le sous-module est
absent :

| fichier | source | sha256 |
|---|---|---|
| `generateur.py` | `tools/structures/generateur.py` (commit `648adce`) | `ca2d8823e9a6df2f2d6009de30402ea5ced04d84dd371faa7b16ccc2c99279c4` |
| `donnees/gold-analyseur.json` | `tools/structures/donnees/gold-analyseur.json` (commit `648adce`) | `4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879` |

Le workflow les copie dans `tools/structures/` **avant** `pip install -e .`, seulement si
`tools/structures/generateur.py` manque. Quand le sous-module est présent (poste de
développement), il est la **source** et la copie n'est pas utilisée.

## Tenir la copie à jour

```bash
python3 tools/verifie_structures_secours.py        # compare, code 1 si dérive
cp tools/structures/generateur.py .github/ci/structures/generateur.py
cp tools/structures/donnees/gold-analyseur.json .github/ci/structures/donnees/gold-analyseur.json
```

Le vérificateur ne peut pas comparer sans le sous-module ; il le dit alors et sort en **2**.
C'est une copie de secours assumée, pas une seconde source : toute modification de S doit être
répercutée ici, sinon un run GitHub testerait une version différente du générateur.
