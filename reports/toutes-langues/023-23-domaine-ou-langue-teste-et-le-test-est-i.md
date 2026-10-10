> Campagne : **toutes-langues** · expérience **23**
> Titre : 23. Domaine ou langue ? — testé, et le test est INCOMPLET
> Date réelle : **2026-10-06 07:36 HAE** (source : commit `e8ae5a2`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 23. Domaine ou langue ? — testé, et le test est INCOMPLET

Hypothèse testée : « certains mots et groupes de mots sont spécifiques à leur domaine ;
ils sont plus communs à leur domaine qu'à leur langue. »

Le traçage par unité offre les deux axes : **même unité entre langues** (`S_langue`)
et **unités différentes dans une même langue** (`S_domaine`). 18 langues, 10 unités.

| couche | S_langue | S_domaine | lecture |
|---|---:|---:|---|
| 0 | 0,4894 | **0,9872** | la langue l'emporte |
| 8 | 0,6132 | **0,8578** | la langue l'emporte |
| 10 | 0,5806 | **0,7916** | la langue l'emporte |

**Des contenus différents dans une même langue se ressemblent plus (0,86) que le
même contenu dans des langues différentes (0,61).**

### Le défaut de mon expérience, et il est décisif

**Les dix unités de l'UDHR sont toutes du MÊME DOMAINE** — le droit humain.
« Contenus différents » n'est donc **pas** « domaines différents ». Mon test compare
du *contenu différent dans un domaine unique* à du *même contenu entre langues*.

**Ce qu'il établit** : dans un domaine unique, la langue pèse plus que le contenu.
**Ce qu'il n'établit pas** : que la langue pèse plus que le domaine.

**L'hypothèse reste donc NON TESTÉE, pas réfutée.**

### Ce qu'il faudrait pour la tester

Des données **appariées entre langues ET couvrant plusieurs domaines**. Ce que
j'ai ne le permet pas :

| corpus | apparié ? | multi-domaine ? |
|---|---|---|
| UDHR (392 langues) | **oui** | **non** — un seul domaine |
| Wikipedia (6 langues) | non | oui |
| Romeo, Gutenberg | oui | non — une œuvre |

Pistes : articles Wikipedia **liés entre langues** (liens interlangues, absents de
mon corpus), ou **manuels traduits** (droit, médecine, biologie) en plusieurs
langues. Aucune n'est disponible sur disque aujourd'hui.


---
