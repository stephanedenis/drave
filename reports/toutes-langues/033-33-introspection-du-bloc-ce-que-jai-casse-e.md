> Campagne : **toutes-langues** · expérience **33**
> Titre : 33. Introspection du bloc — ce que j'ai cassé, et ce que j'ai appris sur ma propre mesure
> Date réelle : **2026-10-06 10:30 HAE** (source : commit `c36bb6b`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 33. Introspection du bloc — ce que j'ai cassé, et ce que j'ai appris sur ma propre mesure

Le mandat demande des rétrospectives en mode **introspection** et des revues en mode
**adverse autonome**. Voici l'une et l'autre, appliquées à ce bloc.

### 33.1 Trois erreurs, toutes les trois de ma part

**1. J'ai cassé la chaîne en ajoutant une fonctionnalité.** En donnant une constante
de temps par neurone (§28), j'ai correctement propagé `a_neur` dans `nait`,
`recalcule` **et** `compacte` — et j'ai écrit un commentaire expliquant précisément
pourquoi il fallait le propager partout. Puis je ne l'ai pas fait dans
`pont_parallele.py`, qui recopie la généalogie à la main. **Deux sections entières
sont mortes** (Romeo, Wikipedia), et je ne l'ai vu qu'une heure plus tard en lisant
un log que je n'avais pas relu. Le commentaire juste à côté du code fautif était le
mien.

*Leçon retenue, appliquée* : `recalcule` **refuse** désormais une généalogie
désynchronisée au lieu de planter obscurément ou — pire — de calculer en silence
avec la mauvaise dynamique.

**2. J'ai transcrit un tableau trié dans un ordre qui ne l'était pas.** Une analyse
intermédiaire a produit des corrélations entièrement fausses (−0,042 au lieu de
−0,754). Le tableau était trié par norme, l'index par ordre du cache. Corrigé en
faisant calculer les corrélations **là où l'indexation est cohérente**, et en
écrivant désormais les tables en CSV indexé par nom.

**3. J'ai lancé deux fois un calcul long sans `setsid`.** Le premier est mort avec
le shell ; le second aussi. Deux mesures perdues, dont une que j'ai dû réécrire plus
légère (2 192 colonnes → 1 296). La règle est maintenant explicite : **tout calcul
de plus de quelques minutes passe par `setsid`/`disown` ou par un job géré.**

### 33.2 La revue adverse : le chiffre de tête ne disait pas ce que je croyais

C'est le point le plus grave, et il n'est pas technique.

Depuis le début, l'apport du pont est mesuré **contre la constante témoin**. Ce
témoin est trop faible : il ne dit rien de ce qu'une lecture directe de l'entrée
apporterait. En le remplaçant par le bon témoin (§29), on découvre que **40 neurones
récurrents valent +0,007 au-dessus d'une simple régression sur la couche 0 du
professeur.** Le chiffre de tête (0,7430 contre 0,7207) reste exact, mais il ne
qualifie pas le pont : il qualifie surtout ce que la couche 0 contient déjà.

**Je n'ai pas choisi ce témoin par malhonnêteté — je ne l'ai pas remis en question
pendant des heures.** Un chiffre qui monte est un chiffre qu'on ne va pas déranger.
C'est exactement le biais que la consigne « toute affirmation non mesurée n'est pas
une affirmation » cherche à corriger, et il a fallu une question de côté (pourquoi
`dzo` est-il la pire paire ?) pour tomber dessus.

### 33.3 Ce qui a bien fonctionné, et pourquoi

**Le profil par langue.** C'est le seul outil qui a produit des résultats
inattendus à répétition : la fidélité EST le témoin constant (r = 0,977), l'apport
est prédit par la fragmentation (R² 0,67), les langues « non servies » étaient
servies depuis le début. Aucun de ces faits n'était visible dans une moyenne.

**Les prédictions écrites avant la mesure.** Elles ont été réfutées trois fois
(pesée 1/norme², multi-échelle comme cause principale, effet plus fort à faible
fragmentation). Trois réfutations valent mieux que trois confirmations : elles
disent que la mesure n'est pas un rituel.

**Le garde-fou `TERMINE` avec `grep -qx`.** Après la leçon du sous-chaîne, aucune
étape de la chaîne ne s'est déclenchée trop tôt.

### 33.4 Ce que je ne sais toujours pas

- **Pourquoi `amh` décroche à la couche 8** (8 unités sur 10). Piste ouverte.
- **Si l'avantage de l'entrée est de nature ou de capacité.** Le §31 le soutient
  sans le trancher : à capacité comparable, le réservoir reste derrière, mais
  l'égalisation n'est pas exacte.
- **Si notre invariance supérieure à celle du professeur** (0,9701 contre 0,6471)
  est un gain ou un effondrement déguisé.
- **Ce qu'un réservoir beaucoup plus large ajoute** par-dessus l'entrée : la mesure
  est relancée, elle a déjà échoué deux fois.

### 33.5 La question de fond, posée sans détour

La mission est un **modèle n-couches récurrent** capable de répondre au premier
niveau abstrait d'un gros modèle. Les mesures de ce bloc disent que, tel qu'il est
construit, ce modèle **n'ajoute presque rien** à une régression sur l'entrée du
professeur. Ce n'est pas une raison d'arrêter : c'est la mesure qui dit où le
travail n'est pas. Ajouter des couches n'achète rien (§29.4) ; ajouter des neurones
achète peu et mal (§31) ; viser la couche 8 plutôt que la 10 achète +0,0495 (§30).

**La piste que ces chiffres désignent n'est pas la taille du réservoir, c'est ce
qu'on lui donne à lire.** Il ne voit que `e_t` et sa propre récurrence. Or
l'information qui compte pour la cible est manifestement présente dans l'entrée, et
le réservoir la détruit au lieu de la structurer. La prochaine question n'est donc
pas « combien de neurones », mais **« quelle fenêtre d'entrée, et pour quelle
transformation »**.


---
