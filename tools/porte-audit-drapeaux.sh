#!/bin/bash
# porte-audit-drapeaux.sh — chaque drapeau du harnais laisse-t-il dans le FICHIER sa trace ?
#
# POURQUOI CETTE PORTE. Le dépôt a un audit des drapeaux du MOTEUR (« huit drapeaux analysés mais
# jamais appliqués »). Le harnais vient de coûter **trois résultats faux publiés** pour la même
# raison, et le 11/10 l'audit en a trouvé **deux de plus** :
#
#   · `--masque 0.25` ne masquait que les `nn.Linear` (5,8 % des poids) : l'occupation du fichier
#     valait **83,9 %** là où le drapeau annonçait 26 %. Les chiffres d'E1 et d'E2 décrivaient
#     l'attention seule, sans le dire ;
#   · `--croissance` héritait du même défaut, et son gradient était lu sur `mod.weight.grad` — qui
#     vaut `None` quand le poids est reparamétré, donc la croissance ne voyait **aucun** gradient.
#
# CE QU'ELLE VÉRIFIE : pour chaque drapeau, une propriété **lisible dans le fichier exporté**
# (occupation, ratio de signes), comparée à ce que le drapeau promet — et **comparative** quand un
# seuil absolu jugerait la théorie plutôt que le drapeau (la croissance se juge contre le même
# masque statique, pas contre un pourcentage deviné).
#
# CE QU'ELLE NE VÉRIFIE PAS : les drapeaux sans trace attendue dans les poids (`--kwta`,
# `--enseignant`/`--alpha-distill`), qui agissent sur le calcul. Les inclure ferait croire à une
# couverture qui n'existe pas.
#
# COÛT : sept entraînements de 200 pas + exports, ~2 min 30.
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
PAS=${PAS:-200}
T=${TRAVAIL:-/tmp/porte-audit-drapeaux}

for f in data/corpus_en.txt data/corpus_en_val.txt; do
    [ -s "$f" ] || { echo "  ❌ $f manquant : cette porte entraîne de petits modèles"; exit 2; }
done
$P -c "import torch, transformers" 2>/dev/null || { echo "  ❌ $P n'a pas torch/transformers"; exit 2; }
rm -rf "$T"; mkdir -p "$T"

timeout 1800 $P -u tools/audit_drapeaux_harnais.py --pas "$PAS" --sortie "$T" 2>&1 | tail -18
CODE=${PIPESTATUS[0]}
[ "$CODE" = 0 ] || { echo "❌ porte audit des drapeaux : ÉCHEC (code $CODE)"; exit "$CODE"; }

echo
echo "✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun"
echo "   se retrouve dans le fichier exporté, à la valeur annoncée."
