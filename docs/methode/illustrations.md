# Les illustrations — SVG obligatoire, jamais d'ASCII art

> **Règle non négociable.** Un schéma, une architecture, un flux, un arbre, une carte : c'est un
> **fichier SVG**. **Jamais** d'ASCII art, jamais de boîtes en `┌─┬─┐`, jamais de flèches en
> `──►` dans un bloc de code. Un agent qui dessine en ASCII est en faute.
>
> **Pourquoi.** Un SVG se rend, se zoome, s'imprime, se cite et se vérifie ; l'ASCII art dépend de
> la police, casse au moindre changement de largeur et ne peut pas être validé. Le dépôt est lu par
> des humains **et** des agents : une illustration doit être un objet, pas une suite de caractères.

## Les quatre voies autorisées

1. **SVG direct** — un fichier `.svg` écrit à la main, avec `viewBox`.
2. **Mermaid → SVG** — source `.mmd` ; **docwatch** génère `<source>.mmd.svg` ; l'image Markdown
   pointe vers ce SVG.
3. **PlantUML → SVG** — source `.puml` ; **docwatch** génère `<source>.puml.svg`.
4. **Bloc inline** — un bloc ` ```plantuml ` ou ` ```mermaid ` **dans le Markdown** ; docwatch le rend
   en SVG mis en cache, sans fichier à côté. La source vit dans la page : elle se révise avec le texte.

Le **SVG généré n'a pas besoin d'être committé** : docwatch le produit à la demande. S'il est
présent, docwatch le régénère. `mmdc`/`plantuml` restent utiles pour prévisualiser en local, mais
ne sont pas nécessaires. Le source `.mmd`/`.puml` vit **à côté** de l'image ; un bloc inline n'a pas
de fichier séparé.

## Où et comment

- **Les concepts** : [`docs/schemas/`](../schemas/) — index et convention dans
  [`docs/schemas/README.md`](../schemas/README.md).
- **La synthèse** : [`docs/theorie/synthese/schemas/`](../theorie/synthese/schemas/) — les schémas des chapitres.
- Chaque SVG porte un **`viewBox`**, un **`<title>`**, un **`<desc>`**, et `role="img"` sur la
  racine.
- Les sources `.mmd`/`.puml` vivent à côté de l'image générée ; l'image Markdown pointe vers
  `<source>.svg`.
- Aucune ressource **externe** : pas de police distante, pas de script, pas d'image liée. Les
  couleurs et les polices sont dans le fichier.
- Les liens d'image sont **relatifs** : `schemas/mon-schema.svg` depuis `docs/`, ou
  `../schemas/mon-schema.svg` depuis `docs/theorie/synthese/`.
- Une image a un **texte alternatif** utile, pas « image ».
- Un concept = **une** illustration ; on réutilise un schéma existant plutôt que d'en créer un
  doublon.

> **L'échelle et la largeur.** Un Gantt (jours/semaines) va dans la
> [roadmap](../pilotage/roadmap.md#le-gantt-indicatif) ; [en-cours](../pilotage/en-cours.md) se pilote à
> l'heure et n'a pas d'axe de temps : un diagramme d'états ou un WBS sans date y est plus juste. Un
> diagramme large (1 500–2 000 px) est normal — les écrans sont en 4K.

## Ce qui est interdit

- les blocs de code **ASCII** qui dessinent une architecture, un flux, un arbre ou une carte ;
- les caractères de boîte `┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ │ ─` ;
- les flèches `──►`, `◄──`, `-->` alignées dans un bloc de code ;
- les liens d'image absolus ou externes ;
- un SVG sans `viewBox` ou sans titre.

## Vérifier

```bash
python3 tools/verifier_schemas.py
```

L'outil vérifie : l'absence d'ASCII art dans les documents, la validité XML des SVG, la présence
d'un `viewBox` et d'un titre, l'absence de ressources externes, les liens d'image relatifs et
existants, et le fait que chaque schéma est **référencé** quelque part. Il vérifie aussi que chaque
bloc **PlantUML inline** se rend (`plantuml` requis) ; Mermaid inline n'est pas vérifié ici, `mmdc`
demande un navigateur (`chrome-headless-shell`).
Une image `<source>.svg` peut être **absente** si la source `.mmd`/`.puml` existe : docwatch la génère.

## Améliorer un schéma existant

1. corriger les **chiffres périmés** (par exemple 46 → 49 portes) ;
2. ajuster le **`viewBox`** au contenu (pas de grande zone vide) ;
3. ajouter **`title`** et **`desc`** s'ils manquent ;
4. vérifier que le texte ne **déborde** pas de sa boîte (rendu à 900 px de large) ;
5. relancer `python3 tools/verifier_schemas.py` et `bash tools/porte-tableaux.sh`.

> *Un schéma qu'on ne peut pas valider est un schéma qu'on ne peut pas citer.*
