#!/bin/bash
# sonde-passe-k3.sh — OÙ PASSE LE TEMPS d'une passe complète Kimi-K3 ?
#
# LA QUESTION OUVERTE, recopiée de `REPRISE.md` :
#
#   « la passe complète coûte 2,95 s par couple (couche, jeton) contre 0,75 s à
#     chaud — quatre fois plus — et réduire de 25 % les experts lus ne change
#     rien. Hypothèse non mesurée : la DISPERSION (~144 lectures par couple ×
#     ~10 ms de déplacement). Le pas pour trancher : `majflt` et le temps
#     d'attente disque sur une passe complète. »
#
# CE QUE CETTE SONDE RELÈVE, et pourquoi ces grandeurs-là :
#
#   l'ÉTAT du processus      « R » = il travaille, « D » = il est bloqué en
#                          attente d'entrées-sorties, « S » = il dort. C'est le
#                          substitut retenu parce que `delayacct_blkio_ticks`
#                          (champ 42 de /proc/PID/stat) vaut **zéro** sur cette
#                          machine : la comptabilité de délai du noyau n'y est
#                          pas active. Un zéro muet ferait conclure « aucune
#                          attente disque » — un chiffre qui ne mesure rien doit
#                          être remplacé, pas cité.
#   utime+stime            le temps CPU réellement travaillé ;
#   majflt / minflt        les défauts de page majeurs comptent les lectures
#                          servies par le disque SI le fichier est projeté en
#                          mémoire. Un moteur qui lit par `pread` n'en produit
#                          aucun — et c'est en soi une information.
#   read_bytes             les octets réellement sortis du bloc, à comparer à la
#                          taille du modèle — donc le nombre de balayages ;
#   diskstats              le temps où CHAQUE disque a été occupé. Les valeurs
#                          sont CUMULÉES depuis le démarrage : prendre « le plus
#                          grand » désigne le disque le plus ancien, pas le plus
#                          actif. On journalise donc tous les périphériques et on
#                          calcule les deltas par périphérique après coup.
#
# Rien n'est déduit : tout est relevé, et le verdict est un rapport de temps.
#
# Usage : tools/sonde-passe-k3.sh [couches] [intervalle_s]
set -u
cd "$(dirname "$0")/.."

K3=${K3:-/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf}
COUCHES=${1:-93}
INTERVALLE=${2:-1}
IDS=${IDS:-3638,275,1309,3140}
D=./drave-core/target/release/drave
J=${J:-/tmp/sonde_k3.csv}

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }
[ -s "$K3" ] || { echo "modèle absent : $K3"; exit 2; }

echo "# modèle    : $K3"
echo "# taille    : $(du -sh "$(dirname "$K3")" 2>/dev/null | cut -f1)"
echo "# couches   : $COUCHES · ids $IDS · échantillonnage ${INTERVALLE}s"

: > "$J"
echo "t,etat,utime_cs,stime_cs,minflt,majflt,blkio_cs,rss_ko,swap_ko,read_o,rchar_o,disques" >> "$J"

T0=$(date +%s)
DRAVE_K3_PASSE=$COUCHES DRAVE_K3_IDS="$IDS" \
    "$D" "$K3" --k3-essai > /tmp/sonde_k3_moteur.log 2>&1 &
PID=$!

while kill -0 "$PID" 2>/dev/null; do
    if [ -r "/proc/$PID/stat" ]; then
        # `comm` peut contenir espaces et parenthèses : on coupe après la
        # DERNIÈRE parenthèse fermante, ce qui décale tous les indices de 2.
        L=$(sed 's/.*) //' "/proc/$PID/stat")
        ETAT=$(awk '{print $1}' <<< "$L")
        read -r _ _ _ _ _ _ _ MINF MAJF _ _ UT ST _ <<< "$L"
        BLKIO=$(awk '{print $40}' <<< "$L")   # champ 42 d'origine
        RSS=$(awk '/VmRSS/{print $2}' "/proc/$PID/status" 2>/dev/null)
        SWAP=$(awk '/VmSwap/{print $2}' "/proc/$PID/status" 2>/dev/null)
        IO=$(awk '/^read_bytes/{r=$2} /^rchar/{c=$2} END{print (r?r:0), (c?c:0)}' "/proc/$PID/io" 2>/dev/null)
        DS=$(awk '{printf "%s:%s:%s;", $3, $13, $14}' /proc/diskstats)
        echo "$(( $(date +%s) - T0 )),$ETAT,$UT,$ST,${MINF:-0},${MAJF:-0},${BLKIO:-0},${RSS:-0},${SWAP:-0},${IO% *},${IO#* },$DS" >> "$J"
    fi
    sleep "$INTERVALLE"
done
wait "$PID"; CODE=$?
FIN=$(( $(date +%s) - T0 ))

echo "# passe terminée en ${FIN} s (code $CODE)"
python3 - "$J" "$FIN" "$COUCHES" <<'PY'
import sys, collections
lignes = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith(('t,', '#'))]
fin, couches = int(sys.argv[2]), int(sys.argv[3])
if len(lignes) < 2:
    print("# aucune mesure exploitable"); raise SystemExit
c = [l.split(',', 11) for l in lignes]
n = lambda i, k: int(c[i][k])
HZ = 100.0
pre, der = 0, len(c) - 1
cpu = ((n(der, 2) + n(der, 3)) - (n(pre, 2) + n(pre, 3)))/HZ
etats = collections.Counter(x[1] for x in c)
tot_n = sum(etats.values())
# /proc/PID/io compte en OCTETS, pas en kilo-octets : lire 11486765056 et
# l'annoncer « en Go » après division par 2**20 donnait 10 954 Go.
read_go = (n(der, 9) - n(pre, 9))/2**30
rchar_go = (n(der, 10) - n(pre, 10))/2**30

def disques(i):
    d = {}
    for e in c[i][11].split(';'):
        if not e:
            continue
        p = e.split(':')
        if len(p) == 3:
            d[p[0]] = (int(p[1]), int(p[2]))
    return d

d0, d1 = disques(0), disques(-1)
delta = sorted(((d1[k][0]-d0.get(k, (0, 0))[0],
                 d1[k][1]-d0.get(k, (0, 0))[1], k) for k in d1), reverse=True)

print(f"\n# {'durée de la passe':<36}{fin:>10} s")
print(f"# {'CPU travaillé (utime+stime)':<36}{cpu:>10.0f} s   ({cpu/fin:>5.1%})")
print(f"# {'échantillons en état D (E/S)':<36}{etats.get('D', 0):>10}"
      f"   ({etats.get('D', 0)/tot_n:>5.1%} du temps)")
print(f"# {'échantillons en état R (travail)':<36}{etats.get('R', 0):>10}"
      f"   ({etats.get('R', 0)/tot_n:>5.1%})")
print(f"# {'échantillons en état S (sommeil)':<36}{etats.get('S', 0):>10}"
      f"   ({etats.get('S', 0)/tot_n:>5.1%})")
print(f"# {'octets lus (bloc)':<36}{read_go:>10.2f} Go")
print(f"# {'octets demandés (rchar)':<36}{rchar_go:>10.2f} Go")
print(f"# {'défauts de page majeurs':<36}{n(der, 5)-n(pre, 5):>10}")
print(f"# {'RSS max':<36}{max(int(x[7]) for x in c)/2**20:>10.2f} Go")
print(f"# {'swap max':<36}{max(int(x[8]) for x in c)/2**20:>10.2f} Go")
if delta:
    occ, pond, nom = delta[0]
    print(f"# {'disque le plus sollicité':<36}{nom:>10}")
    print(f"# {'   occupé':<36}{occ/1000:>10.0f} s   ({occ/1000/fin:>5.1%})")
    print(f"# {'   occupé, pondéré par les files':<36}{pond/1000:>10.0f} s"
          f"   ({pond/1000/fin:>5.1%})")
paires = couches*4
print(f"# {'couples (couche, jeton)':<36}{paires:>10}")
print(f"# {'secondes par couple':<36}{fin/paires:>10.3f} s")
if read_go > 0:
    print(f"# {'débit de lecture effectif':<36}{read_go/(fin/3600):>10.1f} Go/h")

import re
try:
    m = open('/tmp/sonde_k3_moteur.log').read()
    lg = [float(x) for x in re.findall(r"de chargement \+\s*([0-9]+) ms de calcul", m)]
    ch = [float(x) for x in re.findall(r":\s*([0-9]+) ms de chargement \+", m)]
    annonce = re.findall(r"passe complète : ([0-9]+) ms au total", m)
    if ch and lg:
        print(f"\n# {'couches mesurées par le moteur':<36}{len(ch):>10}")
        print(f"# {'   chargement (somme)':<36}{sum(ch)/1000:>10.1f} s")
        print(f"# {'   calcul (somme)':<36}{sum(lg)/1000:>10.1f} s")
        print(f"# {'   calcul par couple':<36}{sum(lg)/1000/max(len(lg)*4,1):>10.3f} s")
    if annonce:
        print(f"# {'passe annoncée par le moteur':<36}{float(annonce[-1])/1000:>10.1f} s")
except Exception as e:
    print(f"# sortie moteur illisible : {e}")

print("\n# VERDICT")
part_d = etats.get('D', 0)/tot_n
debit = read_go/(fin/3600)
attendu = read_go*2**30/(debit*1e9) if debit > 0 else 0
occ_disque = (delta[0][0]/1000/fin) if delta else 0
if occ_disque > 0.7 and cpu < 0.4*fin:
    print(f"#   LE DISQUE. `{delta[0][2]}` est occupé {occ_disque:.0%} du temps et le CPU ne")
    print(f"#   travaille que {cpu/fin:.0%} : le temps de la passe est le temps de LIRE les")
    print(f"#   octets au débit du disque. Vérification : {read_go:.1f} Go à {debit/3600:.0f} Mo/s")
    print(f"#   demandent {attendu:.0f} s, et la passe en a duré {fin}.")
    print("#   Conséquence : toute réduction d'OCTETS LUS se traduit en temps, et")
    print("#   tout disque supplémentaire aussi. Le calcul, lui, n'est pas la limite.")
elif cpu > 0.7*fin:
    print("#   Le CPU. Le processus travaille la majorité du temps : réduire les")
    print("#   lectures ne peut pas suffire, c'est le calcul qu'il faut regarder.")
else:
    print("#   Aucun des deux ne domine nettement — lire les chiffres ci-dessus avant")
    print("#   de conclure quoi que ce soit.")
PY
echo "# journal brut : $J · sortie moteur : /tmp/sonde_k3_moteur.log"
