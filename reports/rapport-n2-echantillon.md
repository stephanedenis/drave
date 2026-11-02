# N2.s — Ce que le meilleur modèle écrit : du français grammatical, des boucles et des collages

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le modèle de 34,3 M distillé
> (**3,6852** sur le wiki) écrit du **français grammatical** mais **boucle** en décodage glouton
> (« la commune de Saint-Germain-de-Commune… ») et **colle** des fragments sans cohérence à
> température 0,8. Une PPL de 3,69 ne fait pas un rédacteur : elle dit la prédiction locale, pas la
> cohérence.

## Le dispositif

- Modèle : `W34-g1` (34,3 M, distillé, N2.r), corpus wiki 186 Mo.
- Prompts : « La France est un pays », « Le chat de la voisine », « Dans les années 1950 »,
  « The history of ».
- Décodage : glouton (température 0) et échantillonné (T=0,8, top-k 40), 80 à 100 octets.

## Ce qui est mesuré

**Glouton** (déterministe) :

> « La France est un pays de la commune de Saint-Germain-de-Communes de la commune de
> Saint-Germain-de-Comté de Saint-Germai… »

> « Le chat de la voisine de la commune de Saint-Germain-de-Commune est située à au sud-est de
> Saint-G… »

**Échantillonné** (T=0,8, top-k 40) :

> « La France est un pays d'État sorti en 1985. Sa famille permet de la fin du Royaume de 1974 à
> la guerre de l'Institut de… »

## Lecture

Le glouton tombe dans une **boucle de gabarit** : le corpus wiki contient des milliers de phrases
« la commune de X est située à … », et le modèle, qui a vu 11 % du corpus, a mémorisé ce motif
local. Ce n'est plus le **saladier de mots** de N2.h (« de latinesplaronsesexinuiteux… ») : c'est du
français **grammatical** — mais qui ne dit rien.

À température 0,8, la boucle casse et le texte devient **fluent et incohérent** : « un pays d'État
sorti en 1985 », « la fin du Royaume de 1974 », des collages de faits wiki. C'est le comportement
attendu d'un modèle qui prédit l'octet suivant avec 34 M de paramètres et 20 Mo vus : **la
grammaire locale est apprise, le monde ne l'est pas**.

**Ce que ça dit de la PPL.** 3,69 est une bonne PPL de prédiction locale, et elle ne mesure pas la
cohérence. Le banc de génération (N4) ne doit pas conclure sur la PPL : il lui faut une **mesure
humaine** (ou un juge) — c'est exactement ce que la ligne S construit avec le banc de structures.

## Ce que ça change pour N2

- **La capacité et le corpus améliorent la prédiction, pas la rédaction.** Le prochain levier pour
  écrire n'est pas 60 M de paramètres : c'est **plus de texte** (et de meilleure qualité), ou un
  décodage/planification (le moteur de pensée, la restitution R31).
- **Les boucles de gabarit** sont un symptôme de **mémorisation locale** : un corpus plus divers
  (et moins de boilerplate) les réduirait — le déduplicateur les retire déjà en partie.
- La **génération contrôlée** (N4) reste un chantier ouvert : prompts, températures, répétition,
  cohérence — et un juge humain.

## Ce qui pourrait le rendre faux

- **Un seul modèle, deux réglages** : d'autres températures, top-p ou un répétition-pénalité
  donneraient d'autres textes.
- **Les prompts sont des débuts de phrase wiki** : un prompt hors distribution (dialogue, consigne)
  dirait autre chose — et le SFT (N4) n'est pas fait.
- **Le corpus est du wikitexte nettoyé** : les gabarits de commune y sont surreprésentés.

## Fichiers

- Modèle : `work/n2j/W34-g1.pt` ; outil : [`tools/generer_natif.py`](../tools/generer_natif.py).
- Contexte : [`n2-34m-distille`](rapport-n2-34m-distille.md), [`n2-capacite-34m`](rapport-n2-capacite-34m.md).
