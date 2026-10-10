> Campagne : **campagne-benefices** · expérience **23**
> Titre : 23. Ce qui reste à mesurer (état de la file, 9 octobre 16 h)
> Date réelle : **2026-10-09 15:55 HAE** (source : commit `505ed18`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 23. Ce qui reste à mesurer (état de la file, 9 octobre 16 h)

**Tout ce que la campagne devait mesurer est mesuré**, et chaque famille a sa ligne
au § 0 bis. Ce qui reste ouvert n'est pas de la mesure en retard, c'est du **travail
identifié** — et il est consigné dans [`docs/manques.md`](manques.md) plutôt que dans
une liste d'attente :

| ce qui reste | où c'est écrit |
|---|---|
| huit manques du **moteur** (noyau de listes pour les experts, noyau de listes sur GPU, lot et hyper-connexions, encodeurs, décodage spéculatif, apprentissage embarqué, qualité des modèles > RAM, défaut de sauvegarde du modèle log-normal) | `docs/manques.md` § 1 |
| quatre manques du **modèle** (structure innée à l'échelle, deux axes à l'échelle, règle locale, trois dessins inédits jamais entraînés) | `docs/manques.md` § 2 |
| douze capacités d'**architecture** pour porter un cerveau, en six phases à portes mesurées | `docs/plan-cerveau-complet.md` |
| la **courbe lecture ↔ qualité** complète, y compris à dim 512 | § 5 quater, complété à 16 h 30 |
| la **modularisation** (espace de travail Cargo, profil d'itération, verrous par ressource) | `docs/modularisation.md` |

**Ce que la fenêtre a établi, en une ligne par famille** : le verdict du § 0 bis.
**Ce qu'elle a coûté en corrections** : cinq pièges de méthode (§ 16, § 17), dont un
binaire plus vieux que ses correctifs et une porte qui ne pouvait pas passer.
**Ce qu'elle laisse** : un modèle dont le coût se choisit à la conception (÷4 pour
+1 %, ÷8 pour +4 %), et un plan — pas une promesse — pour le reste.

---
