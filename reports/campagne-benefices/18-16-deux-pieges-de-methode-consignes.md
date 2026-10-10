> Campagne : **campagne-benefices** · expérience **16**
> Titre : 16. Deux pièges de méthode, consignés
> Date réelle : **2026-10-08 23:38 HAE** (source : commit `bab38c7`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 16. Deux pièges de méthode, consignés

**Un cache qui survit à son correctif.** La mesure sémantique avec l'échelle
corrigée a d'abord rendu **exactement les chiffres publiés** (couche 0 : +0,0002 ;
couche 4 : +0,0156) — parce que le cache de vecteurs de `/tmp` datait de la
session précédente, **avant** le correctif du lecteur. Un cache qui ne porte pas
la version de l'outil qui l'a écrit fait mesurer l'ancien code avec le nouveau :
les fichiers ont été supprimés et la comparaison relancée à caches neufs.

**Une chaîne qui attend son marqueur dans le mauvais journal.** Les chaînes de
nuit sont sérialisées par des marqueurs écrits en fin de journal (un `pgrep` sur un
script pas encore lancé rend la main tout de suite — piège déjà consigné). La
chaîne « creux 512 » attendait `chaîne creux terminée` dans **son** journal (8)
alors que la chaîne « creux » l'écrit dans le **sien** (7) : elle a patienté deux
heures devant un GPU libre, et c'est le même défaut que les trois autres — un
instrument qui ne dit pas ce qu'il attend. Corrigé, et le marqueur est maintenant
nommé avec son fichier dans le commentaire de la garde.

**Un outil dont l'option `--cache` écrase les deux côtés.** Dans
`premiere_couche_semantique.py`, la même expression
`opt("--cache", "/tmp/pcs_a1")` sert aux DEUX dossiers comparés (A et B) : passer
`--cache X` fait donc écrire les deux jeux dans `X.moyenne.npz`, et la
comparaison oppose un dossier à lui-même. Sans `--cache`, les deux défauts sont
distincts et tout va bien — c'est pourquoi le piège ne s'était pas vu.

---
