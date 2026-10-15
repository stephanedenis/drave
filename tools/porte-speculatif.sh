#!/bin/bash
# porte-speculatif.sh — LE RÉFLEXE PROPOSE, LE CERVEAU VÉRIFIE : la sortie NE CHANGE PAS.
#
# POURQUOI CETTE PORTE. Le décodage spéculatif est le seul mécanisme du dépôt qui **accélère sans
# rien changer** : le brouillon propose, le vérificateur ratifie, et la suite produite doit être
# **exactement** celle du cerveau seul. C'est une propriété **vérifiable** (et non une espérance) —
# et c'est la seule raison d'accepter un mécanisme dont le brouillon **se trompe**.
#
# Les quatre vérifications :
#   1. **L'INVARIANT** : la suite produite par le pilote est **identique, jeton pour jeton**, à celle
#      du cerveau seul sur la même invite — c'est tout l'intérêt : la sortie ne change pas ;
#   2. **LE TAUX EST RENDU** : le pilote publie un taux d'acceptation dans [0, 1] et des jetons par
#      vérification ≥ 1 (un taux absent ou hors bornes ferait passer un mécanisme mort pour vivant) ;
#   3. **LE TÉMOIN** : avec un brouillon **non entraîné** (la tête empruntée sur 8 des 24 couches),
#      le taux est **0 %** — c'est le contrôle, et il doit rester à zéro (mesuré : 0 sur 22
#      propositions) ;
#   4. **LE RÉFLEXE ENTRAÎNÉ EST RATIFIÉ** *(conditionnel)* : si le réflexe distillé est présent, son
#      taux doit être **strictement positif** sur une invite anglaise — sinon le mécanisme
#      n'apporte rien. Si le fichier est absent, la porte le **dit** et ne juge pas (comme
#      `--banc-vision` dit « pas de v.patch_embd.weight ») ;
#   5. **UN BROUILLON INVALIDE ÉCHOUE EN LE DISANT** : un chemin de modèle inexistant doit sortir en
#      erreur avec un message, jamais rendre une suite silencieusement fausse.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-/home/stephane/gpu-env/bin/python}
INVITE=${INVITE:-"The history of the city begins"}
N=${N:-8}
T=${T:-/tmp/porte-speculatif}
DISTILLE=${DISTILLE:-/tmp/n4/e5-distille.gguf}
ADAPTATEUR=${ADAPTATEUR:-/tmp/n4/e5-adaptateur.f32}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
mkdir -p "$T"

echo "porte du décodage spéculatif — « $INVITE » · $N jetons"

# ---- 1. l'invariant : la suite du pilote est celle du cerveau seul
$P tools/speculatif_drave.py --n "$N" --K 4 --invite "$INVITE" --json "$T/pilote.json" \
    --brouillon "$M --couches 0:8 --tete-partielle" > "$T/pilote.log" 2>&1 \
    || { echo "  ❌ le pilote a échoué :"; tail -3 "$T/pilote.log"; exit 1; }
INVITE_IDS=$(cat /tmp/speculatif-drave/invite.ids 2>/dev/null)
[ -n "$INVITE_IDS" ] || { echo "  ❌ l'invite tokenisée est introuvable"; exit 1; }
SEUL=$("$D" "$M" --infer --ids-file /tmp/speculatif-drave/invite.ids --n "$N" --ctx 512 \
       --threads 8 --temp 0 2>&1 | grep -oE "tokens générés : \[[0-9, ]*\]" \
       | grep -oE "[0-9]+" | tr '\n' ',')
$P - "$T/pilote.json" "$SEUL" <<'PY' || exit 1
import json, sys
r = list(json.load(open(sys.argv[1])).values())[0]
pilot = ",".join(str(x) for x in r["generes"]) + ","
seul = sys.argv[2]
if pilot != seul:
    sys.exit(f"  ❌ INVARIANT ROMPU : le pilote rend « {pilot} » et le cerveau seul « {seul} »")
print(f"  ✅ 1. INVARIANT tenu : {len(r['generes'])} jetons identiques au cerveau seul, "
      f"jeton pour jeton")
PY

# ---- 2. le taux est rendu et cohérent
$P - "$T/pilote.json" <<'PY' || exit 1
import json, sys
r = list(json.load(open(sys.argv[1])).values())[0]
t, j = r["taux_acceptation"], r["jetons_par_verification"]
if not (0.0 <= t <= 1.0):
    sys.exit(f"  ❌ taux d'acceptation hors bornes : {t}")
if j < 1.0:
    sys.exit(f"  ❌ moins d'un jeton par vérification : {j}")
if t != 0.0:
    sys.exit(f"  ❌ le brouillon NON ENTRAÎNÉ est ratifié ({t:.1%}) : le témoin devait rester à zéro")
print(f"  ✅ 2. le taux est rendu et cohérent ({t:.1%}) · {j:.2f} jeton(s) par vérification")
print(f"  ✅ 3. TÉMOIN : la tête empruntée (8 couches, non entraînée) n'est JAMAIS ratifiée")
PY

# ---- 4. le réflexe entraîné est ratifié (conditionnel : il vient d'un entraînement hors porte)
if [ -s "$DISTILLE" ] && [ -s "$ADAPTATEUR" ]; then
    $P tools/speculatif_drave.py --n 12 --K 4 --invite "$INVITE" --json "$T/distille.json" \
        --brouillon "$DISTILLE --couches 0:8 --tete-partielle --adaptateur-sortie $ADAPTATEUR" \
        > "$T/distille.log" 2>&1 \
        || { echo "  ❌ le pilote a échoué avec le réflexe distillé"; tail -3 "$T/distille.log"; exit 1; }
    $P - "$T/distille.json" <<'PY' || exit 1
import json, sys
r = list(json.load(open(sys.argv[1])).values())[0]
t = r["taux_acceptation"]
if t <= 0.0:
    sys.exit("  ❌ le réflexe ENTRAÎNÉ n'est jamais ratifié : le mécanisme n'apporte rien")
print(f"  ✅ 4. le réflexe DISTILLÉ est ratifié : {t:.1%} ({r['acceptes']}/{r['proposes']}) · "
      f"{r['jetons_par_verification']:.2f} jeton(s) par vérification")
PY
else
    echo "  ⚠️ 4. réflexe distillé absent ($DISTILLE) : la ratification n'est PAS mesurée ici"
    echo "     (elle l'est dans reports/rapport-speculatif-reflexe.md : 2,4 à 30 % à K = 4)"
fi

# ---- 5. un brouillon invalide échoue EN LE DISANT
$P tools/speculatif_drave.py --n 4 --K 2 --invite "$INVITE" \
    --brouillon "/tmp/nexiste-pas.gguf --couches 0:8" > "$T/invalide.log" 2>&1
[ "$?" -ne 0 ] || { echo "  ❌ un brouillon inexistant n'a pas échoué"; exit 1; }
grep -q "❌" "$T/invalide.log" || { echo "  ❌ l'échec n'est pas dit"; exit 1; }
echo "  ✅ 5. un brouillon inexistant échoue en le disant (aucune suite rendue)"
echo "  ✅ porte tenue (invariant exact · taux rendu · témoin à zéro · brouillon invalide refusé)"
exit 0
