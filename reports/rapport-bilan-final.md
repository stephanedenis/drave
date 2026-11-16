# Bilan final — Drave 0.1.0, 16 novembre 2026
> **En une ligne.** Le bloc linguistique s'**installe** (éditable, roue, historique), **démarre en 3 commandes**, publie un **JSON v2** mesuré, passe **10 000 mots en 0,82 s** (α **1,076**, ×**4,9**), **refuse proprement** (0/1/3/4/5), a une **CI 10/10** et une **passe de portes fraîche** — avec ses négatifs nommés et trois décisions ouvertes.

## 1. Installable — trois voies
- **Éditable** : `pip install -e .` → `drave 0.1.0` (3,35 s ; **12** tests d'empaquetage) ; Python ≥ 3.10, **0** dépendance d'exécution.
- **Roue** : `dist/drave-0.1.0-py3-none-any.whl` (2 055 192 o, gold et profils dedans), installée hors dépôt ; **mêmes JSON** qu'au dépôt ; sans les gold, `evaluer` → **4**.
- **Historique** : `python3 tools/drave.py …` depuis la racine, intact ; sans installation, `drave` → **127**, sans trace.

## 2. Démarrage — 3/3, ~14 s
```bash
git clone https://github.com/stephanedenis/drave.git && cd drave
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
drave --version && drave analyser "Le chat dort." && drave evaluer
```
Clone public : **3/3**, JSON **5 899 octets**, 20 étiquettes ; **sans** `tools/structures` → sortie dégradée (voir § 6) ; dépôt : **6 179 octets**.

## 3. API du JSON
- Schéma **`drave.annotation` v2**, v1 lue, **8** champs racine ; candidats en objets `{span, cible, source}`, rôles dans un vocabulaire **fermé de 8**.
- **2 139** objets, **1 295/1 295** cibles choisies, **0** span faux ; **21 → 8** rôles, **0** hors table ; `role="predicat"` → **711**, `"prédicat"` → **0** ; rôle inventé → `RoleHorsVocabulaire`.

## 4. Performance
- **10 000 mots : 3,991 → 0,816 s** (×**4,89** ; **12 259** mots/s), α **1,552 → 1,076**, quadratique **+0,00077** ; mémoire **+0,5 Mio** (127,4 Mio).
- **612/452 JSON identiques au bit près**, diff vide ; un seul texte littéraire.

## 5. Codes, CI, portes
- **Codes** : `0` succès · `1` autre erreur (`--strict` sous 0,70) · `3` refus (texte vide) · `4` clé/fichier/gold absent · `5` usage ; `stdout` vide et pas de trace.
- **CI** : `.github/workflows/ci.yml`, matrice **3.10/3.13**, 5 étapes ×2 = **10/10 vertes** ; test cassé → **1**, job arrêté (**2/2**) ; `act` absent, preuve **locale** seulement.
- **Portes** : `work/portes/passe-1611/` — **86 portes, 82 vertes, 4 rouges** au relevé : `indice`, `melange` (structurelles tolérées), `sessions` (heartbeat) et `tableaux` (lien transitoire de ce bilan) ; **84/2 après vérification ciblée** ; registre lu par code de sortie.

## 6. Négatifs nommés
- **Clone public dégradé** : sans `tools/structures`, attachement **88,70 %** (contre 99,58 %) ; F1 **81,88 %** n'est pas un gain.
- **Or de rôles humain absent** : le gold S est écrit par les mêmes règles ; gold v2 **20/46**, F1 **0,5406** ; **144/144** n'est pas une validation indépendante.
- **Linéarité mesurée sur un seul texte** (Alice, littéraire) ; **roue** non isolée (`--no-build-isolation`), non signée, hors PyPI, dépend du sous-module.
- **Neuronal strict = `MockNeuronal`**, plancher **POS seul** ; **confiance des profils non calibrée** ; **CI locale** sans run GitHub ; **tag** `exploitable-2026-11-16` sur `ae3c24f2`, pas sur ce bilan ; compteurs vivants.

## 7. Ce qu'il reste à décider
- **`--tagger auto`** : prototype **opt-in** mesuré (30/30), défaut hors ligne inchangé ; décider : le passer par défaut ou le laisser opt-in.
- **Or de rôles (J4)** : double codage indépendant, kappa ≥ 0,80, or permuté ; c'est le seul négatif produit qui ne soit pas une limite de mesure.
- **Panini** : **26 signatures V14** manquantes (calibration **42/44**, rejeu **27/60**) ; sans elles, le rejeu n'est pas un test.
**Suite.** L'état et la roadmap suivent ; le tag reste sur `ae3c24f2` ; la prochaine mesure est **J4**. Fiches : [bilan 2](rapport-bilan-exploitable-2.md) · [CI](rapport-ci.md) · `work/portes/passe-1611/registre.txt` · [JSON](rapport-bilan-final.json).
