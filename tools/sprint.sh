#!/bin/bash
# Boxing temps réel d'un sprint de 2 h : démarrage, état, clôture avec la trame
# de cérémonie (revue · rétrospective · planning).
#
#   tools/sprint.sh start "<objectif du sprint>"
#   tools/sprint.sh status
#   tools/sprint.sh close
#   tools/sprint.sh list
#
# Le sprint vit dans `sprints/` : un fichier par sprint, et `COURANT` qui dit
# lequel tourne. La durée est de 2 h (SCRUM_DUREE pour un autre boxing, en
# secondes : SCRUM_DUREE=3600 pour une heure).
set -u
cd "$(dirname "$0")/.."
DUREE=${SCRUM_DUREE:-7200}
COURANT=sprints/COURANT

maintenant() { date +%s; }
hm() { date -d "@$1" +"%H:%M"; }
restant() { # secondes → « 1 h 07 »
    local s=$1
    if [ "$s" -lt 0 ]; then echo "dépassé de $(( -s / 60 )) min"; return; fi
    echo "$((s / 3600)) h $(printf %02d $(( (s % 3600) / 60 )))"
}

case "${1:-status}" in
start)
    objectif=${2:?"usage : sprint.sh start \"<objectif>\""}
    num=1
    [ -f "$COURANT" ] && num=$(( $(cut -d' ' -f1 "$COURANT") + 1 ))
    debut=$(maintenant); fin=$((debut + DUREE))
    slug=$(echo "$objectif" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | cut -c1-40 | sed 's/-$//')
    fic=$(printf "sprints/%02d-%s.md" "$num" "$slug")
    printf "%s %s %s\n" "$num" "$debut" "$fin" > "$COURANT"
    {
        printf "# Sprint %s — %s\n\n" "$num" "$objectif"
        printf -- "- **Début** : %s · **Fin prévue** : %s (boxing de %s min)\n" \
               "$(hm "$debut")" "$(hm "$fin")" "$((DUREE / 60))"
        printf -- "- **Objectif** : %s\n" "$objectif"
        printf -- "- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.\n\n"
    } > "$fic"
    echo "Sprint $num démarré à $(hm "$debut") → $(hm "$fin")  ·  $fic"
    ;;
status)
    [ -f "$COURANT" ] || { echo "aucun sprint en cours (sprint.sh start \"<objectif>\")"; exit 0; }
    read -r num debut fin < "$COURANT"
    m=$(maintenant)
    echo "── Sprint $num ─────────────────────────────────────────────"
    head -3 "sprints/$(printf '%02d' "$num")-"*.md | tail -1
    echo "   temps : $(hm "$m") · reste $(restant $((fin - m)))"
    echo "   commits depuis le début : $(git log --oneline --since="@$debut" | wc -l)"
    git log --oneline --since="@$debut" | sed 's/^/     /'
    ;;
close)
    [ -f "$COURANT" ] || { echo "aucun sprint en cours"; exit 0; }
    read -r num debut fin < "$COURANT"
    m=$(maintenant); fic=$(ls sprints/$(printf '%02d' "$num")-*.md)
    echo "=== clôture du sprint $num ($(hm "$debut") → $(hm "$m"), prévu $(hm "$fin")) ==="
    {
        printf "\n## Revue — ce qui est livré, mesuré\n\n"
        printf "Durée : %s min (boxing %s min). Commits : %s.\n\n" \
               "$(( (m - debut) / 60 ))" "$((DUREE / 60 ))" "$(git log --oneline --since="@$debut" | wc -l)"
        git log --format='- `%h` %s' --since="@$debut" | sed 's/^/  /'
        printf "\n## Rétrospective — garder / changer\n\n"
        printf -- "- **Garder** :\n- **Changer** :\n- **Doute** :\n"
        printf "\n## Planning — le sprint suivant\n\n"
        printf -- "| # | chantier | critère de succès |\n|---|---|---|\n| 1 |  |  |\n"
    } >> "$fic"
    rm -f "$COURANT"
    echo "trame écrite dans $fic — à compléter (revue chiffrée, rétro, planning)"
    ;;
list)
    for f in sprints/*.md; do [ -e "$f" ] || continue; head -1 "$f"; done
    ;;
*) echo "usage : sprint.sh {start \"<objectif>\"|status|close|list}"; exit 1 ;;
esac
