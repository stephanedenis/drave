# E1 — la FAQ dans le sommaire et les liens : 9 ancres, 5 liens, 0 mort

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **E1** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **la FAQ est au sommaire**, ses **5 liens** et les **9 ancres** du
> sommaire résolvent, **0 lien mort** ; le contenu des **dix réponses n'a pas bougé**
> (sha256 identique).
>
> **La question.** La FAQ (D3) vit dans [`docs/produit/README.md`](../docs/produit/README.md)
> § 8, mais le document n'avait **pas de sommaire** et la FAQ n'était listée ni dans le
> « Où aller ensuite » du document ni dans la table **Produit** de
> [`docs/README.md`](../docs/README.md). Les liens de la section étaient-ils vivants ?
>
> **La réponse.** Un **sommaire de neuf entrées** est ajouté en tête du document ; sa
> **huitième entrée** est la FAQ. La section § 8 est atteignable depuis le sommaire, depuis
> le « Où aller ensuite » et depuis `docs/README.md`. Les **cinq liens** de la section
> (`tools/verifier_faq.py`, `reports/rapport-faq.md`, `reports/faq.json`, `exemples.md`,
> `reports/rapport-g017.md`) existent ; les **neuf ancres** du sommaire pointent vers un
> titre réel. Aucun lien mort.
>
> **Le chiffre.** **9/9 ancres** valides · **5/5 liens** de la section § 8 valides ·
> **0** lien mort · **1** ligne FAQ dans `docs/README.md` · **995/1000** mots (budget T1) ·
> **0** réponse modifiée (sha256 `8855b475…` avant **et** après).
>
> **Dispositif** : [`tools/verifier_liens_faq.py`](../tools/verifier_liens_faq.py)
> (neuf ancres, cinq liens, contrôle négatif, `--json`, `--autotest`) ;
> [`reports/faq-sommaire.json`](faq-sommaire.json) (le relevé complet) ;
> [`docs/produit/README.md`](../docs/produit/README.md) (le sommaire et § 8) ;
> [`docs/README.md`](../docs/README.md) (la ligne FAQ). Les réponses restent celles de
> [`reports/rapport-faq.md`](rapport-faq.md) et [`reports/faq.json`](faq.json).

## 1. Ce qui a changé

| fichier | changement | preuve |
|---|---|---|
| [`docs/produit/README.md`](../docs/produit/README.md) | un **sommaire** de neuf entrées avant § 1 ; § 8 en **gras** | 9/9 ancres valides |
| [`docs/produit/README.md`](../docs/produit/README.md) § 9 | une ligne **FAQ** dans « Où aller ensuite » | 3 liens valides |
| [`docs/README.md`](../docs/README.md) | une ligne **FAQ** dans la table **Produit** | ancre `#8-faq--dix-questions` valide |
| [`tools/verifier_liens_faq.py`](../tools/verifier_liens_faq.py) | le vérificateur (nouveau) | `--autotest` ✅ |

Les **dix réponses** de § 8 ne sont pas touchées : la fiche ne réécrit aucun chiffre, aucun
argument, aucune commande. Aucune ligne de § 8 n'apparaît dans le diff ; l'empreinte le
confirme (§ 6).

## 2. Le sommaire

Le document n'en avait pas ; il en a un, court, qui suit les neuf sections :

| # | entrée | ancre | état |
|---:|---|---|---|
| 1 | À qui s'adresse le produit | `#1-à-qui-sadresse-le-produit` | ✅ |
| 2 | Ce que le produit fait | `#2-ce-que-le-produit-fait` | ✅ |
| 3 | Comment l'utiliser — cinq exemples réels | `#3-comment-lutiliser--cinq-exemples-réels` | ✅ |
| 4 | Ce que le produit ne fait pas encore | `#4-ce-que-le-produit-ne-fait-pas-encore` | ✅ |
| 5 | Performance | `#5-performance` | ✅ |
| 6 | Garanties | `#6-garanties` | ✅ |
| 7 | Le CLI livré — contrat et manques | `#7-le-cli-livré--contrat-et-manques` | ✅ |
| **8** | **FAQ — dix questions** | `#8-faq--dix-questions` | ✅ |
| 9 | Où aller ensuite | `#9-où-aller-ensuite` | ✅ |

**Lecture.** L'ancre suit la règle GitHub (minuscules, ponctuation retirée, espaces →
tirets, tirets doublés autour du tiret cadratin) ; le vérificateur calcule les ancres des
titres du document et les compare, il ne se contente pas de compter les liens.

## 3. Les liens de la section § 8

| libellé | cible | fichier | état |
|---|---|---|---|
| `tools/verifier_faq.py` | `../../tools/verifier_faq.py` | `tools/verifier_faq.py` | ✅ |
| `reports/rapport-faq.md` | `../../reports/rapport-faq.md` | `reports/rapport-faq.md` | ✅ |
| `reports/faq.json` | `../../reports/faq.json` | `reports/faq.json` | ✅ |
| `exemples.md` | `exemples.md` | `docs/produit/exemples.md` | ✅ |
| `rapport-g017.md` | `../../reports/rapport-g017.md` | `reports/rapport-g017.md` | ✅ |

**5/5** fichiers existent ; **0** lien mort. Les trois liens ajoutés au « Où aller
ensuite » (l'ancre § 8, `rapport-faq.md`, `faq.json`) sont les mêmes cibles, déjà vérifiées
ci-dessus.

## 4. La ligne FAQ de `docs/README.md`

La table **Produit** gagne une ligne :

```
| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées contre le code |
```

L'ancre est valide et le budget T1 est tenu : **995 mots / 1000**. La ligne n'existait pas
avant E1 ; `docs/README.md` ne citait que `produit/README.md` et `produit/exemples.md`.

## 5. Le contrôle négatif

Le vérificateur ne se contente pas de confirmer : il injecte **deux liens faux** dans un
bloc de test et vérifie qu'ils sont rejetés.

| lien injecté | attendu | détecté |
|---|---|---|
| `../../reports/rapport-e1-inexistant.md` | fichier absent | ✅ |
| `#section-qui-nexiste-pas` | ancre absente | ✅ |
| `README.md#8-faq--dix-questions` | lien valide conservé | ✅ (non rejeté) |

`python3 tools/verifier_liens_faq.py --autotest` sort **0** : les deux faux liens sont
détectés, le vrai ne l'est pas. Sans ce contrôle, un vérificateur qui répondrait toujours
« ✅ » passerait pour bon.

## 6. Ce qui n'a pas changé

La section § 8 est hachée **avant** et **après** l'édition :

| moment | sha256 de § 8 | lignes |
|---|---|---|
| D3, avant E1 | `8855b475faef9079ecadcf9f5426cca62965160403f5542ecc1bc209e6912364` | 110 |
| E1, après | `8855b475faef9079ecadcf9f5426cca62965160403f5542ecc1bc209e6912364` | 110 |

**Identique.** Le vérificateur porte cette empreinte (`sha256_d3`) et échoue si § 8 bouge :
c'est le garde-fou « ne change pas le contenu des réponses ». Les ajouts sont **hors** de la
section : un sommaire avant § 1, une ligne dans § 9, une ligne dans `docs/README.md`.

## 7. Ce qui pourrait rendre cette fiche fausse

1. **Un fichier cité déménage ou est renommé** (`rapport-faq.md`, `faq.json`,
   `rapport-g017.md`, `exemples.md`, `verifier_faq.py`) : le lien meurt ; relancer
   `python3 tools/verifier_liens_faq.py`.
2. **Un titre du document change** : son ancre change ; le sommaire pointe alors vers une
   ancre morte (le vérificateur le voit, le rendu GitHub le montre).
3. **La règle d'ancre de GitHub change** (ponctuation, tirets, accents) : les neuf ancres
   calculées ici ne sont plus celles du rendu. Le vérificateur suit la règle connue au
   2026-11-15 ; à revérifier si GitHub la modifie.
4. **`docs/README.md` dépasse 1000 mots** : la ligne FAQ tient aujourd'hui à **995** ; une
   ligne ajoutée sans retrait ferait échouer `tools/taille_documents.py` (T1).
5. **Le sommaire est retiré ou § 8 déplacé** : la ligne FAQ et son ancre pointent dans le
   vide ; le vérificateur échoue.
6. **La section § 8 est éditée** (même une virgule) : l'empreinte change et le contrôle
   « contenu inchangé » passe à `false`. C'est voulu pour E1 ; une modification
   volontaire de la FAQ demande de mettre à jour `SHA256_FAQ_D3`.

## 8. Où lire la suite

- la **FAQ** : [`docs/produit/README.md`](../docs/produit/README.md) § 8 ;
- le **sommaire** : le même document, en tête ;
- l'**index de la documentation** : [`docs/README.md`](../docs/README.md) ;
- le **relevé** : [`faq-sommaire.json`](faq-sommaire.json) ;
- le **vérificateur** : [`tools/verifier_liens_faq.py`](../tools/verifier_liens_faq.py) ;
- la **fiche de la FAQ** : [`rapport-faq.md`](rapport-faq.md) · [`faq.json`](faq.json).
