# Le rejeu des fenêtres : chaque tranche rejouait le même échantillon — 110 000 pas ne valent pas 900 Mo de données neuves

> **Ligne de roadmap** : N (le natif) · **Date** : 2026-11-21 (nuit) · **Verdict** : ⚠️ **défaut
> trouvé** — les chaînes d'entraînement repartaient le compteur de fenêtres à **zéro** à chaque
> tranche : le tirage Van der Corput rendait donc **les mêmes fenêtres** à chaque tranche. La preuve
> est dans les journaux : la perte du **pas 1** des tranches successives de `p1` est **5,6107 →
> 1,2005 → 1,0917 → 1,0316** — elle porte sur le **même premier lot** et ne baisse que parce que le
> modèle s'améliore. Un « 110 000 pas » en onze tranches = **onze passes sur le même échantillon de
> 80 000 fenêtres** (~82 Mo), pas 900 Mo de données fraîches.
>
> **Correctif** : `--compteur-suite` (opt-in) — le point de contrôle sauve `pas_cumules`, et
> `--init` le reprend ; `--decalage` permet un décalage explicite. Validé : un pas 1 à 5,6844 sans
> reprise devient **5,5582** avec reprise (fenêtres différentes), et `pas_cumules` passe de 3 à 5.
> **Opt-in pour ne pas changer sous les runs de la nuit** (tous les bras partagent le même
> échantillonneur, la comparaison reste honnête — mais l'étiquette « 110k » est à corriger).

## Ce que le défaut change aux lectures

1. **La taille du corpus ne joue pas le rôle qu'on croyait** : à pas fixe, le nombre de fenêtres
   distinctes est `pas × lot` (80 000 par tranche de 10 000 pas), et il est **rejoué** à chaque
   tranche. Un corpus plus gros change la **diversité** des fenêtres tirées, pas la quantité vue.
   C'est cohérent avec le résultat de la veille (palier 1 3,69 Go ≈ `wiki_big` 0,83 Go) — mais pour
   une autre raison que « le volume n'achète pas » : **aucun des deux n'a consommé son corpus**.
2. **Les époques calculées dans la fiche de la nuit sont fausses** : 0,244 « époque » pour le palier 1
   à 110 000 pas suppose un parcours séquentiel qui n'a pas eu lieu.
3. **Les comparaisons restent valides entre bras** (même échantillonneur, même schéma), et les
   améliorations mesurées (wikitext2 9,5 → 7,2 pour `p2` en 10 tranches) sont réelles — mais elles
   mesurent surtout **plus d'optimisation sur le même échantillon**, pas plus de données.
4. **La variance mesurée hier (±1,8 %)** reste valide : elle compare des bras qui rejouent tous le
   même schéma.

## Ce qui pourrait le rendre faux

- Le correctif n'est **pas** encore utilisé dans un run complet : il est validé sur un run jouet
  (deux fois deux pas, CPU) ; un vrai run à `--compteur-suite` reste à faire.
- `pas × lot` fenêtres distinctes par tranche : si un run ne fait **qu'une** tranche, il voit bien
  `pas × lot` fenêtres neuves — le défaut ne concerne que les **chaînes**.
- Le tirage Van der Corput est quasi uniforme sur tout le corpus : l'échantillon de 80 000 fenêtres
  couvre tout le corpus de façon stratifiée, mais **0,002 %** des positions.

## La suite

1. Relancer le palier 1 (ou `wiki_big`) avec `--compteur-suite` sur 110 000 pas — un vrai run de
   données neuves, pour trancher la question du volume.
2. Corriger la fiche de la nuit (époques) et la note de la sélection.
3. Vérifier les autres chaînes (`bench/chaine_nuit.sh`, `work/n4/*.sh`) : toutes doivent passer
   `--compteur-suite` (ou un `--decalage`) sous peine de rejouer.

## Voir aussi

- [la nuit du palier 1](rapport-nuit-palier1-110k.md) · [la variance](rapport-variance-graines.md) ·
  [la sélection](rapport-selection-contenu.md) · [l'entraîneur](../tools/entrainer_native.py)
