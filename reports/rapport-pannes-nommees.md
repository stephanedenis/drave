# C11 — la panne du pair est nommée au pas et en octets

> **Ligne de roadmap** : C11 (moteur) · **Date** : 2026-10-29 · **Verdict** : ✅ **la rouge est
> qualifiée et corrigée** — le chemin « pair absent » nomme maintenant la **région**, le **pas**
> et les **octets**, comme le chemin « pair tué ». `porte-pannes` sort **verte**.
>
> **Dispositif** : `tools/porte-pannes.sh`, Qwen2.5-0.5B Q8_0, topologie à deux régions ;
> données [`pannes-nommees.json`](pannes-nommees.json).

## Le défaut

Le chemin `TcpStream::connect` en échec imprimait :

```
[pannes] PANNE : le pair local → 127.0.0.1:61083 est INJOIGNABLE (…)
```

Il nommait l’**adresse**, pas la **région**, et ne disait ni le pas ni les octets. La porte
échouait sur « la panne ne dit pas où elle est survenue » — à raison.

## Le correctif

```
[pannes] PANNE sur le lien local → d : le pair 127.0.0.1:61083 est INJOIGNABLE (…) au pas 0
(0 octets échangés). … Vérifiez que le nœud écoute (--flux-serveur …).
```

## Ce qui est mesuré

| cas | région | pas | octets | code | temps |
|---|---|---:|---:|---:|---:|
| pair tué | d | **95** | **349 980** | **7** | — |
| pair absent | d | **0** | **0** | **7** | **2 s** |
| nominal | — | — | — | 0 | PPL 33,0156 |

La porte **exit 0** : la panne est nommée, aucune perplexité n’est rendue, le pair absent ne
pend pas.

## Le contrôle négatif

- **Code 7** dans les deux pannes — un script peut distinguer la panne d’une borne (5) ou d’un
  budget (6).
- **Aucune perplexité** dans les sorties de panne : un graphe amputé n’est pas une version
  approchée du même calcul.
- **2 s** pour le pair absent : pas d’attente indéfinie.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; le pas 95 dépend de l’instant du `kill`.
- **Le pair absent** est testé sur localhost, pas sur un réseau réel.
- **La panne tuée** peut tomber à un autre pas selon la machine.
- **Pas de reprise** : la porte vérifie l’arrêt, pas la récupération.

## Ce que ça change

`porte-pannes` passe de **rouge** à **verte** ; la famille C11 est qualifiée. Les deux rouges
structurelles restent `porte-indice` et `porte-melange`. A8.0 reste à 17/33.

## Fichiers

- `drave-core/src/main.rs` — message de panne complet.
- `tools/porte-pannes.sh` — la porte.
- `reports/pannes-nommees.json` — les mesures.
- `reports/rapport-pannes-nommees.md` — cette fiche.
