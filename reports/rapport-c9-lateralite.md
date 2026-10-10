# C9 — latéralité : l'échange est exact, il ne crée pas de gain, et il récupère un jumeau dégradé à hauteur de sa moyenne

> Campagne : **cerveau** · expérience : deux instances jumelles, échange d'état à une couche
> Question : le plan (§ C9) demande deux jumeaux et un lien **homotopique par couche**, avec un
> invariant (« échange désactivé ⇒ identique au modèle seul ») et une validation honnête (« un gain
> de perplexité **ou** de robustesse — et si le gain est nul, le dire »). Alors : **l'échange
> apporte-t-il quelque chose, et quoi ?**
> Verdict : **trois résultats, dont deux négatifs et un explicable.**
> (1) **l'échange désactivé est EXACT** : un état imposé à la couche 12 puis les couches 12..24
> rendent **27,4964**, exactement la perplexité du modèle entier (64 jetons) ;
> (2) **deux jumeaux identiques qui s'échangent ne changent RIEN** (27,4964 = 27,4964, au bit
> près) : pas de gain gratuit, c'est la garde du plan ;
> (3) **un jumeau DÉGRADÉ est récupéré** (163,17 → 36,13) — mais le **contrôle** (le même bruit à
> moitié d'amplitude, qui est exactement ce que fait une moyenne) donne le **même chiffre**
> (36,1307, écart **0,000 %**) : **c'est une moyenne, pas une latéralité**.
> Date réelle : **2026-10-10 17:09 HAE** (heure lue sur la machine).
> Protocole : `tools/jumeaux.sh` (deux captures, cinq états imposés en format REFD, cinq
> perplexités) · porte : `tools/porte-jumeaux.sh`.

## 1. La mécanique : un état imposé, une couche, un échange

Le moteur sait **imposer un état d'entrée** (`DRAVE_ETAT_ENTREE=<fichier REFD>`) : les couches
`L..24` tournent alors en partant de cet état, position par position. Deux jumeaux, c'est donc
deux états à la couche `L` — et l'échange, c'est **ce qu'on écrit dans le fichier** : l'un, l'autre,
ou leur moyenne. Rien de nouveau dans le moteur n'a été nécessaire ; c'est la **structure** qui est
mesurée, pas un câblage.

| mesure (64 jetons, couche 12, bruit 10 % de la RMS) | perplexité |
|---|---|
| modèle entier (référence) | **27,4964** |
| vue A seule imposée (invariant du plan) | **27,4964** |
| deux jumeaux identiques, échangés | **27,4964** |
| jumeau A bruité (10 %) | 163,1678 |
| échange A↔A(bruité) — la moyenne | 36,1307 |
| **CONTRÔLE** : bruit à moitié d'amplitude | **36,1307** |

## 2. Le résultat qui compte : la fusion de deux vues VALIDES

L'expérience ci-dessus ne teste pas la latéralité : elle teste une **moyenne**. La vraie question
est ailleurs — deux jumeaux qui voient la **même chose autrement**. Ici : la vue **B** est capturée
avec `--attn-window 8` (attention fenêtrée), donc une vue **valide mais différente**, et moins
bonne seule.

| jetons notés | vue A | vue B (fenêtrée) | fusion A↔B | verdict |
|---|---|---|---|---|
| **31** (32 jetons) | 56,7642 | 59,3496 | **56,2222** | la fusion **bat les deux**… |
| **127** (128 jetons) | 14,6496 | 18,0113 | 15,3906 | …et ici elle est **ENTRE** les deux |

**Le premier chiffre était un artefact de 31 jetons notés.** C'est exactement le genre de résultat
qu'il ne faut pas publier sans le refaire plus long — et c'est pourquoi la porte **n'affirme rien**
sur ce cas : elle verrouille les invariants (exactitude, pas de gain entre jumeaux identiques,
récupération = moyenne) et laisse la fusion de vues à la fiche, avec ses deux mesures.

**Conclusion honnête pour C9** : sur ce modèle et cette tâche, **la fusion de deux vues ne bat pas
la meilleure des deux**. Le plan l'avait écrit d'avance (« le gain est probablement nul ») ; il est
maintenant **mesuré**, avec la raison : une moyenne d'états est une moyenne, et elle ne fabrique pas
d'information.

## 2 bis. Le coût COMPRESSÉ de l'échange : 8 bits pour ÷4 d'octets et +3,0 %

L'échange coûte 3 584 octets par pas et par couche en f32 dense — c'est le poste dominant. La
question qui décide de son usage réel : **combien peut-on compresser l'état échangé, et à quel
prix en perplexité ?** Mesure (64 jetons, couche 12, état quantifié par blocs de 32 canaux comme
le fait le moteur, puis imposé) :

| encodage de l'état échangé | octets / pas | ÷ | perplexité | prix |
|---|---|---|---|---|
| **f32 dense** (référence) | 3 584 | — | **27,4964** | — |
| **8 bits par bloc** (une échelle f32 par 32 canaux) | **896** | **÷4** | **28,3135** | **+3,0 %** |
| 4 bits par bloc | 448 | ÷8 | 32,0904 | +16,7 % |
| listes creuses k=128 (indice u16 + valeur i16) | 512 | ÷7 | 37,2395 | +35,5 % |
| listes creuses k=64 | 256 | ÷14 | 51,2747 | +86,5 % |
| listes creuses k=32 | 128 | ÷28 | 149,9882 | +446 % |

**Deux résultats, et le second recoupe une mesure indépendante :**

1. **l'échange utile coûte ÷4 d'octets pour +3,0 % de perplexité** (8 bits par bloc) — c'est le
   régime à retenir si l'on échange à chaque couche ;
2. **quantifier bat élaguer, encore** : à budget d'octets comparable (512 contre 896), les
   **listes creuses** k=128 coûtent **+35,5 %** là où les 8 bits coûtent **+3,0 %**. C'est la même
   conclusion que la campagne a tirée du **pont** entre deux régions (« à budget égal, quantifier
   bat élaguer de 83 % », fiche 25) — obtenue ici sur un **état échangé entre jumeaux**, par un
   autre protocole. Deux mesures indépendantes qui disent la même chose valent mieux qu'une.

## 3. Le coût, et ce qu'il faudrait pour que ça vaille

- **3 584 octets par pas et par couche échangée** en f32 dense (896 canaux × 4). Pour 24 couches et
  64 pas : **5,5 Mio** par séquence — c'est le poste dominant d'un jumeau, très au-dessus du
  transport sparse du dépôt (÷2,3 à ÷4 selon le mode) ;
- **ce qui rendrait la latéralité utile**, et qui n'est pas mesuré ici : des jumeaux qui voient des
  choses **différentes** (pas la même séquence sous deux attentions, mais deux **entrées** ou deux
  **mémoires** différentes), ou une **asymétrie de calcul** (une instance profonde, une courte).
  Échanger deux états qui décrivent la même chose ne peut pas enrichir l'un par l'autre ;
- **la variante la plus plausible** reste `--echange experts` (échanger des **choix** d'experts sur
  un modèle routé) : là, les deux instances pourraient réellement voir des choses différentes.

## 4. Protocole, pour rejouer

```bash
tools/jumeaux.sh 128 12 0.10      # 128 jetons, échange à la couche 12, bruit 10 %
tools/porte-jumeaux.sh            # les invariants seuls (64 jetons, ~2 min)
```

**Les deux pièges attrapés en écrivant ce banc**, et ils sont de la même famille (un instrument qui
ne dit rien au lieu de dire qu'il ne peut pas dire) :

1. la capture d'états **n'écrit rien** sans `--tete-partielle` : l'écriture est dans la branche qui
   applique la norme finale, donc `--couches 0:12` seul produit **zéro fichier** — et le banc lisait
   alors des fichiers absents ;
2. le format **REFD** indexe les positions par blocs de `ne[0] × ne[1]` : mettre le nombre de
   positions dans `ne[1]` fait un bloc de 32 × 896, et le moteur lit **tout le fichier comme un seul
   état** (panique `copy_from_slice`). L'en-tête correct est `ne = [canaux, 1, 1, 1]`.
