# Le graphe de document — régions, offsets, partition

> **Ce que ce document est.** La **spécification** du manifeste de graphe de document (R0.1) :
> ce qu'est un flux, ce qu'est une région, et les trois contrôles qui rendent la découpe
> vérifiable. Le code est `tools/graphe_document.py` ; la porte est `tools/porte-document.sh` ;
> les résultats mesurés vivent dans `reports/`, jamais ici.
>
> **Chargement** : lire § 2 et § 5 pour coder contre le manifeste ; le reste est la justification.

## 1. Le besoin

Le modèle ne voit qu'un flux d'octets : il ne peut pas dire « lis le titre, saute la section 3,
compare les colonnes ». Il faut une représentation du document qui (a) survive au rejeu, (b)
serve de champ de lecture au contrôleur (R0.2), et (c) se **vérifie** sans modèle. Un graphe
qu'on ne peut pas vérifier n'est pas une découpe, c'est une impression.

## 2. Deux espaces, et il ne faut pas les confondre

| espace | ce qu'il indexe | qui l'utilise |
|---|---|---|
| **le flux** | le texte extrait, en **octets UTF-8** ; c'est ce que le lecteur lit | les spans des régions, le contrôleur, le banc |
| **la source** | la provenance dans le fichier d'origine : `page` (PDF), `bloc` (HTML/DOCX/EPUB), `offset` (Markdown) | l'audit, la citation (R32), la relecture (R22) |

Les offsets sont en **octets**, jamais en caractères : un accent coûte deux octets, et c'est
précisément la confusion qu'un contrôle doit attraper. Un span `[start, end)` désigne
`flux_bytes[start:end]`.

## 3. Le manifeste

```json
{
  "version": 1,
  "source":     {"chemin": "…", "sha256": "…", "octets": 0, "format": "pdf", "langue": "fr"},
  "extraction": {"outil": "graphe_document.py", "version": 1, "plat": false},
  "flux":       {"octets": 0, "sha256": "…"},
  "regions":    [{"id": "r00000", "type": "titre", "texte": "…",
                  "start": 0, "end": 0, "sha256": "…", "ordre": 1, "prov": {"page": 1}}],
  "stats":      {"regions": 0, "types": {}}
}
```

| champ | rôle |
|---|---|
| `source.sha256` | la découpe est attachée au fichier exact : si la source change, le manifeste est invalide |
| `extraction` | quel outil, quelle version, et si c'est un contrôle négatif (`plat`) |
| `flux` | la longueur et le SHA-256 de la concaténation : le manifeste se vérifie seul |
| `regions` | la partition, dans l'**ordre de lecture** (`ordre` est une permutation 1..N) |
| `prov` | la provenance source, non vide pour chaque région |
| `stats` | le décompte par type, pour la porte |

Le vocabulaire des types est **fermé** : `titre`, `section`, `paragraphe`, `liste`, `tableau`,
`code`, `maths`, `figure`, `legende`, `note`, `blanc`. Le type `blanc` est émis par le cœur
(un `\n` entre deux régions), jamais par un parseur : c'est ce qui permet à la partition d'être
exacte sans que chaque parseur ait à gérer les séparateurs.

**Le manifeste ne porte aucun horodatage.** Deux exécutions sur le même fichier doivent donner
le même SHA-256 canonique : c'est ce qui rend le rejeu vérifiable.

## 4. Les six invariants

1. **Partition** — les spans sont contigus, commencent à 0 et couvrent tout le flux : chaque
   octet appartient à exactement une région.
2. **Hash** — `sha256(region.texte)` se recalcule, et `flux_bytes[start:end]` est exactement
   `region.texte.encode("utf-8")`.
3. **Ordre** — `ordre` est une permutation de 1..N ; pour une page à deux colonnes, il ne les
   entrelace pas.
4. **Types** — un type du vocabulaire, jamais vide (sauf `blanc`, qui vaut exactement `\n`).
5. **Provenance** — chaque région porte un `prov` non vide.
6. **Rejeu** — deux découpes du même fichier donnent la même empreinte.

## 5. Les trois contrôles, et ce que chacun attrape

| contrôle | ce qu'il prouve | ce qu'il attrape |
|---|---|---|
| **partition** (§ 4.1–4.2) | la découpe est **interne** : tout est couvert, rien n'est inventé | un offset faux, un trou, un doublon de région |
| **fidélité** | le flux contre une extraction **indépendante** : au moins 99 % des mots communs | un extracteur qui perd du texte ou qui en ajoute |
| **rejeu** | la sortie est déterministe | un horodatage, un ordre de dictionnaire, un chemin absolu |

L'extraction indépendante dépend du format : `pypdf` pour le PDF (contre `pdftotext`),
`pandoc -t plain` pour le DOCX/EPUB, `lxml` pour le HTML, **la source elle-même** pour le
Markdown. Ce dernier cas est le plus strict — et c'est celui qui a attrapé le plus de fautes :
le contenu des fragments `code` est verbatim (`<hôte:port>` y est du texte, pas une balise), les
marqueurs de liste ne sont pas lus, les commentaires HTML ne sont pas rendus.

**Contrôles négatifs** — ils doivent **échouer** :

- **texte plat** : le même flux en une seule région `paragraphe`. La porte exige ≥ 6 types sur
  le corpus ; le texte plat en donne un. Il prouve que la porte voit la structure.
- **PDF deux colonnes** : la colonne gauche doit sortir entièrement avant la droite, sans
  alternance. Il prouve que l'ordre de lecture n'est pas l'ordre du fichier.
- **notes hors corps** : le texte d'une note ne doit pas être recopié dans un paragraphe. Il
  prouve que la note est une région, pas une ligne comme les autres.

## 6. Les formats et leur extracteur

| format | extraction | provenance | connu pour |
|---|---|---|---|
| Markdown | lecture directe | `offset` octet de la ligne | source du dépôt, donc contrôle le plus strict |
| HTML | DOM (`lxml`) | `bloc` (indice DOM) | ordre du DOM = ordre de lecture |
| PDF | `pdftotext -bbox-layout` | `page` (1-based) | colonnes par distribution des x, notes par hauteur de ligne |
| DOCX, EPUB, ODT | `pandoc -t gfm` puis le lecteur Markdown | `bloc` | un seul lecteur de blocs pour trois formats |

**Un format, un extracteur, un contrôle.** On ne code pas un extracteur de PDF : on lit les
coordonnées que poppler donne déjà, et on le vérifie contre `pypdf`.

## 7. Ce que le graphe ne fait pas

- **pas de mise en page** : une région porte du texte et un ordre, pas une position à l'écran ;
- **pas de tableaux PDF** : un tableau non balisé reste du texte. Mieux vaut ne pas revendiquer
  un `tableau` que l'inventer — le bloc tableaux (R4.1) le traitera ;
- **pas d'OCR** : une page scannée n'a pas de texte, donc pas de graphe (R4.4) ;
- **pas de sémantique** : le graphe dit « ceci est un titre », pas « ce titre est important ».

## 8. Voir aussi

- [La fiche R01](../pilotage/backlog/R01-graphe-document.md) — le contrat, la porte, les contrôles.
- [La lecture rapide](../theorie/lecture-rapide.md) — pourquoi la structure est le premier levier.
- [La porte document](../../tools/porte-document.sh) — 50 pages, partitions exactes, contrôles négatifs.
