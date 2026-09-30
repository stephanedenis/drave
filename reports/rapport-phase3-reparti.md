# Phase 3 — le calcul réparti redevient fidèle

**En une ligne** : deux processus qui se passent des flux calculent maintenant
**exactement** la même perplexité qu'un seul — écart **0,00e0** — après deux
corrections qui n'étaient pas celle que je croyais.

## Le banc

Deux processus, localhost, modèle Qwen2.5-0.5B-Q8_0, 12 couches chacun, contexte
256. Le pilote garde les couches 0..12, le nœud moteur applique 12..24 et renvoie
le flux ; le pilote norme, applique la tête et note la perplexité. La référence
est le même modèle calculé entièrement en local. Reproductible :

```bash
./drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 45733 &
./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
        --couches-locales 12 --limit 40 --ctx 256
```

40 jetons suffisent à trancher : la locale vaut 144,8289, et un découpage fidèle
doit redonner ce chiffre, pas un chiffre « proche ».

## Le défaut que je croyais, et le défaut réel

Je suis parti d'une hypothèse lue dans le code : le nœud moteur reçoit
`fin = n_layer`, donc `forward` applique la norme finale (`couche_fin >= n_layer`)
et le pilote la réapplique ensuite. Double norme. La correction (un drapeau
`flux_brut`) a bien amélioré les choses — **1 621,7 → 693,4** — mais pas assez :
le facteur restait 4,8 contre la référence. Une hypothèse juste qui n'explique pas
tout, c'est une hypothèse incomplète, pas une explication.

Le vrai défaut était à trois lignes de là : **`forward` bouclait sur
`0..cfg.n_layer`** au lieu de `couche_debut..couche_fin`. Le pilote calculait donc
les 24 couches, envoyait l'état final, et le nœud moteur recalculait les 24
couches par-dessus. `forward_lot` et `forward_mla` respectaient déjà la plage ;
`forward` était l'exception — le mode d'échec « le drapeau est analysé mais jamais
appliqué » que ce dépôt a déjà rencontré cinq fois (`--pin`, `--moe-topk`,
`--attn-window`, `--attn-sinks`).

## Les trois états, mesurés

| état | locale | répartie | écart |
|---|---|---|---|
| avant correction | 144,8289 | 1 621,7239 | ×11,2 |
| après la norme seule | 144,8289 | 693,4492 | ×4,8 |
| après la plage de couches | 144,8289 | **144,8289** | **0,00e0** |

Égalité exacte, et pas seulement petite : le transport est du f32, donc rien
n'est arrondi en chemin — le découpage ne devrait pas changer un bit, il ne le
change pas. Vérifié aussi sur 200 jetons (199 flux servis), même égalité.

## Ce que ça établit, et ce que ça n'établit pas

Établi : le contrat « une liste suffit à continuer le calcul » tient **entre deux
processus**, pas seulement en rejeu local ; la séparation en nœuds ne coûte
aucune fidélité ; la norme finale a une règle écrite (`flux_brut`).

Pas établi : le coût. Aujourd'hui le flux voyage en **f32 dense, 3 604 octets par
flux** (20 d'en-tête + 896 × 4) — soit 3,2 ko par couche d'état, alors que le
disque sait déjà écrire la même information en **6 octets par neurone actif**.
C'est le prochain chantier (3.2) : faire voyager la LISTE, pas le vecteur dense,
et mesurer octets par jeton × latence.
