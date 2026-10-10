> Campagne : **campagne-benefices** · expérience **33**
> Titre : 33. Pannes de lien (C11) : nommées, avec un code distinct, et sans résultat partiel
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 33. Pannes de lien (C11) : nommées, avec un code distinct, et sans résultat partiel

Le plan prévoyait, pour une région perdue, une politique `best-effort` où « la région est
sautée, l'écart est annoncé ». **La mesure oblige à refuser cette sémantique** : un modèle
dont on saute douze couches ne calcule pas une version approchée du même résultat, il
calcule **un autre modèle** — et l'« écart » annoncé serait un écart entre deux choses
différentes. La seule conduite honnête est de **s'arrêter en disant tout**.

Ce qui est implémenté, et mesuré par `tools/porte-pannes.sh` (3 cas) :

| cas | mesure |
|---|---|
| exécution nominale | perplexité **33,0156**, code **0** |
| **pair tué en cours de route** | `PANNE sur le lien local → d : le pair a fermé avant de rendre son état… L'exécution s'arrête **au pas 12** (**43 968 octets** échangés jusque-là). AUCUNE perplexité n'est rendue` · code **7** |
| **pair absent** | `PANNE : le pair local → 127.0.0.1:61342 est INJOIGNABLE (Connection refused)` · code **7**, en **2 s**, aucune perplexité |

Le code de sortie est **distinct** : 5 = borne de pas (C4), 6 = budget dépassé (C10),
**7 = panne de lien**. Un script peut donc distinguer les trois causes d'arrêt.

**Deux défauts trouvés en écrivant la porte**, tous les deux dans le moteur :
1. un pair absent faisait **paniquer** le pilote (`expect("connexion au nœud moteur")`,
   code 134 illisible) — au lieu de nommer le lien et de ne rien rendre. Corrigé ;
2. la porte elle-même attendait `client connecté` dans le journal du nœud pour tuer le
   pair : fragile, et elle échouait pour une raison qui n'était pas celle qu'elle mesure
   (port en TIME_WAIT, pilote qui calcule 10 s de référence locale avant de se connecter).
   Elle chronomètre maintenant la mort, et juge sur le code et le message.

**Ce qui reste du plan §3.2 sur les pannes, et qui n'est PAS fait** : la reprise. Un pair
qui revient n'a plus son cache KV, donc continuer serait faux ; reprendre proprement
demanderait de rejouer le préfixe (checkpoint/restart), ce qui n'existe pas.
