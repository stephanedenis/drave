> Campagne : **toutes-langues** · expérience **02**
> Titre : 2. La convention de traçage, unique et vérifiée
> Date réelle : **2026-10-05 23:50 HAE** (source : commit `1424c5d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 2. La convention de traçage, unique et vérifiée

```
--ctx 4096 · --couches 0:11 · --lot 1 · --n 0 · --trace-couches 0,10
```

- `--n 0` : ni la tête du professeur, ni les jetons qu'il génère. Le défaut de drave
  est `n = 32`, ce qui mettait **32 jetons inventés dans la trace**.
- `--trace-couches 0,10` : on n'écrit que l'entrée et la cible. Vérifié
  **bit-identique** au traçage complet, et **11× plus petit**.
- `--ctx 4096` : **11 % des langues étaient tronquées** à `ctx 2048` (16 sur 143 :
  ame ben blt boa bod ccp chr cpu csw div dzo **ell** fuf guj **hin**). Vérifié
  avant d'agir : `--ctx` ne change **rien** au calcul quand le texte tient — deux
  traces du même texte à 2048 et 4096 sont **bit-à-bit identiques**. Seul le
  contexte d'allocation change, donc le surcoût est nul.

**Pourquoi la troncature est grave** : sur un texte coupé, la « dernière position »
n'est plus la fin du texte, donc l'invariance inter-langue compare des **contenus
différents**. C'est un biais **silencieux** qui frappe exactement la métrique
mesurée.

---
