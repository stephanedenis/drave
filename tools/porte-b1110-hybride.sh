#!/bin/bash
# porte-b1110-hybride.sh — B11.10b : l'indice de jeu strippé route les ambiguës.
set -u
cd "$(dirname "$0")/.."
PY=${PY:-/home/stephane/gpu-env/bin/python}
PYTHONPATH=tools "$PY" - <<'PY' || exit 1
from jeux.hybride import lit_avec_indice
from jeux.codecs.base import lit

cases = {
    "A1 au morpion": ("morpion", True),
    "d4 au go": ("go", True),
    "b6-c5 aux dames": ("dames", True),
    "E4 aux échecs": ("echecs", True),
}
ok = 0
for texte, (jeu, lu) in cases.items():
    l = lit_avec_indice(texte)
    if l.jeu != jeu:
        raise SystemExit(f"  ❌ {texte!r} : jeu {l.jeu} (attendu {jeu})")
    if l.ok != lu:
        raise SystemExit(f"  ❌ {texte!r} : ok={l.ok} (attendu {lu})")
    ok += int(l.ok)
    print(f"  ✅ {texte!r} → {l.jeu} · lu={l.ok} · {l.erreurs[:1] or l.rsn.corps}")
if ok != 4:
    raise SystemExit(f"  ❌ {ok}/4 lues (attendu 4/4 ; E4 = requête de case)")
for s in ("A1", "E4", "d4", "b6-c5"):
    if lit(s).ok:
        raise SystemExit(f"  ❌ {s} lu sans indice")
print("  ✅ sans indice : 4/4 refusées")
for s, jeu in (("e2e4", "echecs"), ("2D", "cartes")):
    l = lit(s)
    if not l.ok or l.jeu != jeu:
        raise SystemExit(f"  ❌ contrôle {s!r} : ok={l.ok} jeu={l.jeu}")
print("  ✅ e2e4/2D non touchés")
print("PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case")
PY
