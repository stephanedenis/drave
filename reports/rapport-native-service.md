# N4.2 — service local : `drave-n0` derrière HTTP

> **Objet.** Exposer `drave-n0` comme service local minimal, sans dépendance : `GET /sante`,
> `POST /generer`. Ce n'est pas un service de production.

## Dispositif

- Modèle : `/tmp/drave-n0-distille.pt`, **11 469 192** paramètres, CPU.
- Serveur : [`tools/serveur_natif.py`](../tools/serveur_natif.py), `ThreadingHTTPServer` stdlib.
- Adresse : **127.0.0.1:8765**.
- Génération **greedy**, déterministe, verrou global (un seul modèle).

## Résultat

```text
GET /sante
{"ok": true, "parametres": 11469192}

POST /generer {"prompt":"La France est un pays","n":48}
{"prompt": "La France est un pays", "octets": 69,
 "texte": "La France est un pays de la couche 1 (le plafond de la porte de la co"}
```

- **69 octets** produits, dont le prompt ; le modèle s'arrête au premier saut de ligne.
- Le service répond, le modèle est chargé une fois.

## Lecture

- Le service **fonctionne** : santé, génération, JSON, sans framework.
- La **qualité** reste celle de N4.1 : cohérente quelques mots, puis dérive.
- **Pas d'authentification**, **pas de cache KV**, **pas de limite de concurrence** : ce n'est pas
  exposable au-delà de la machine locale.
- Le verrou global sérialise les générations : sûr, lent.

## Verdict

**N4.2 — service local : atteint techniquement**. La porte N4 (« usage utile ») n'est pas atteinte :
le modèle ne produit pas de réponse fiable.

## Limites

- **Un seul modèle**, **CPU**, **greedy**.
- **Pas de cache KV** : chaque octet refait la passe avant.
- **Pas d'auth**, **pas de TLS**, **pas de quotas**.
- **Pas de test automatisé** du serveur ; vérification manuelle `curl`.

## Fichiers

- Code : [`tools/serveur_natif.py`](../tools/serveur_natif.py).
- JSON : [`native-service.json`](native-service.json).
