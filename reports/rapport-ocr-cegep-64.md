# D — le corpus CEGEP à 64 documents est contaminé : DOC2 (val) est un quasi-doublon du train

> **Ligne de roadmap** : D · **Date** : 2026-11-04 · **Verdict** : ⛔ **le re-split 64 (2/1/1) est
> contaminé** — **DOC2**, placé en **val**, a **18/20 fenêtres de 500 o** déjà dans l'ancien train
> (**17 001 o contigus**, offsets 4 026 047 → 4 044 047) ; **DOC1** (train) est un quasi-doublon
> intra-train (**24/26** fenêtres, une fenêtre de **8 188 o exacte**). Le contrôle **8 Ko exact est
> à 0** et **ne le voit pas** (les deux scans du même document ont été OCRisés deux fois, le texte
> diffère légèrement). ✅ **le corpus propre à 62 documents est prêt et vérifié** :
> `work/ocr/cegep64/propre/` — 60 anciens + **Choquette** (6 p) + **Assurance** (1 p), DOC1/DOC2
> écartés ; 8 Ko 0, 500 o 0, val/test anciens intacts.
>
> **Dispositif** : `tools/verifie_contamination.py` (fenêtres de 8 192 o) + contrôle exact de
> fenêtres de 500 o (pas de 1 000) ; corpus `data/corpus_ocr_cegep/` (état 15 h 57) ; corpus propre
> préparé ; données [`ocr-cegep-64.json`](ocr-cegep-64.json). Aucun run GPU.

## 1. Ce que le hub a fait, et ce que ça donne

Le hub a **appendé** les 4 documents OCR au corpus CEGEP, puis **re-splitté** 2/1/1
(Choquette + DOC1 → train, DOC2 → val, Assurance → test), en préservant les anciens splits au
préfixe (hashes du manifeste : `6d53a023…`, `dd605833…`, `1c9ab734…` — vérifiés). Le corpus passe
à **64 documents** (55/5/4), **2 031 p**, 4 462 978 car.

Le contrôle **8 Ko entre splits** donne **0 doublon** (train 546 tronçons ; val 4/0 ; test 2/0) —
et son **contrôle négatif** aussi est bon : une fenêtre de val injectée dans une copie du train
est retrouvée (**1 doublon, 25 %**). Le « 8 Ko 0 » est donc vrai… et pourtant le corpus n'est pas
propre.

## 2. La fuite que le 8 Ko ne voit pas

Le même document a été **scanné/OCRisé deux fois** (copie `.pdf` déjà dans les 60, copie `.PDF`
majuscule) : les deux textes diffèrent légèrement, donc aucune fenêtre de 8 Ko n'est identique —
mais des pans entiers le sont à 500 o près.

| document | split | fenêtres 500 o dans l'ancien train | preuve |
|---|---|---:|---|
| **DOC2** | **val** | **18/20** | **17 001 o contigus**, offsets 4 026 047 → 4 044 047 |
| **DOC1** | train | **24/26** | 22 001 o contigus ; **1 fenêtre de 8 188 o exacte** : `train[4 447 324:4 455 512] == train[4 007 429:4 015 617]` |
| Choquette | train | 0/8 | neuf |
| Assurance | test | 0/2 | neuf |

**La baseline du corpus 60 est 0/13 (val) et 0/11 (test)** : la fuite DOC2 est **introduite par
l'ajout**, pas préexistante. DOC1 est dans le train : c'est de la duplication intra-train, pas une
fuite de split — mais elle gonfle le corpus de 22 p qui existent déjà.

> Le mode **ligne** du script (par défaut) donne 168/207 lignes de val dans le train : ce sont des
> **en-têtes de formulaires** répétés (Cisco), pas des fenêtres de 8 Ko. Ne pas le lire comme une
> fuite ; l'unité du dépôt pour le texte intégral est la fenêtre de 8 Ko, et le contrôle de
> quasi-duplication est le 500 o.

## 3. Le corpus propre 62, prêt et vérifié

`work/ocr/cegep64/propre/` : ancien train **exact** + **Choquette** + **Assurance** ; DOC1 et DOC2
**écartés** ; val/test **anciens intacts** (comparabilité de l'évaluation).

| split | octets | SHA-256 |
|---|---:|---|
| train | **4 440 987** | `f57154df3ca5ecbd487c649c9177fddc7b4ffc2073f3488b8a2d1ad436d3da47` |
| val | **12 536** | `dd605833f27eab63df46de3437b1e74b479c2c3abcd6ea683365647063ccd0e1` |
| test | **10 524** | `1c9ab73459c1e44ae7c1e23e46210091c54a5be360df698bdad150e9c1153b84` |

- **62 documents** (55/4/3), **1 989 p**, **4 418 407 car.** ;
- préfixe train = hash du manifeste `6d53a023…` ; jonction `…oup 360\n\nChoquette` (aucun mot collé) ;
- **8 Ko : 0** (train 543 tronçons ; val 2/0 ; test 2/0 ; recouvrement éval vide) ;
- **500 o : 0/13 et 0/11** — exactement la baseline du corpus 60.

## 4. La restauration, au hub

`data/` est réservé par N2 ; la commande exacte est :

```
cp work/ocr/cegep64/propre/train.txt data/corpus_ocr_cegep/train.txt
cp work/ocr/cegep64/propre/val.txt   data/corpus_ocr_cegep/val.txt
cp work/ocr/cegep64/propre/test.txt  data/corpus_ocr_cegep/test.txt
```

Hashes attendus : `f57154df…`, `dd605833…`, `1c9ab734…` (ci-dessus). Le corpus 64 contaminé peut
être conservé sous `work/ocr/cegep64/contamine-15h57/` pour l'histoire.

## 5. Contrôle négatif et ce qui pourrait rendre ce résultat faux

- **Contrôle négatif du 8 Ko** : fenêtre de 8 192 o de val injectée dans une copie du train →
  **1 doublon trouvé** (25 % des tronçons de val). Le 0 du corpus n'est pas un 0 de complaisance.
- **Contrôle négatif du 500 o** : Choquette et Assurance, deux documents neufs, donnent **0** ;
  DOC1/DOC2 donnent 24/26 et 18/20 — le contrôle sépare bien.
- **Ce qui pourrait le rendre faux** : le 500 o est un contrôle **exact**, pas un détecteur de
  paraphrase ; une réécriture ou un OCR très différent passerait. La baseline ne couvre que
  val/test contre train, pas la duplication intra-train ancienne. Les pages et caractères sont
  dérivés des manifestes, pas recomptés page à page. Le corpus 62 n'est pas déployé : tant que le
  hub n'a pas restauré, `data/` reste l'état 64 contaminé.

## 6. Ligne d'état proposée

> **D — contaminé, à restaurer** : les 8 `.PDF` OCRisés ; **2 neufs** (Choquette 6 p, Assurance
> 1 p), **2 quasi-doublons écartés** (DOC1 22 p, DOC2 20 p) ; le re-split 2/1/1 plaçait **DOC2 en
> val** avec **18/20 fenêtres de 500 o** déjà dans le train (17 001 o contigus ; 8 Ko exact 0 mais
> **insuffisant**) ; corpus propre **62 documents** prêt et vérifié (`work/ocr/cegep64/propre/`,
> SHA `f57154df…`), restauration à appliquer ; [fiche](./rapport-ocr-cegep-64.md).

## 7. Fichiers

- `reports/ocr-cegep-64.json` — le manifeste (états 64 et 62, contrôles, restauration).
- `reports/rapport-ocr-cegep-64.md` — cette fiche.
- `work/ocr/cegep64/propre/` — le corpus 62 prêt (non versionné).
- `work/ocr/cegep64/controle/` — le contrôle négatif (non versionné).
