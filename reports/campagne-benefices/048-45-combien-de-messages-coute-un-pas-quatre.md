> Campagne : **campagne-benefices** · expérience **45**
> Titre : 45. Combien de MESSAGES coûte un pas ? Quatre — et c'est l'en-tête écrit à part
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 45. Combien de MESSAGES coûte un pas ? Quatre — et c'est l'en-tête écrit à part

Le protocole écrit la trame en **deux fois** : `s.write_all(&tete)?` puis `s.write_all(&corps)?`.
Sur un lien qui facture **par message** (et non par octet), ces deux écritures se paient deux
fois. La question est donc chiffrable : **combien de messages par pas le protocole coûte-t-il ?**

**Protocole** : le proxy ajoute un délai **par message**, on mesure le pas médian, et la pente
donne le nombre équivalent de messages.

| délai par message | pas médian | pente (messages équivalents) |
|---|---|---|
| 0 ms | 14,87 ms | — |
| 2 ms | 23,35 ms | **4,24** |
| 5 ms | 34,93 ms | **4,01** |
| 10 ms | 44,83 ms | **3,00** |

**Trois lectures :**

1. **à petit délai, un pas coûte ~4 messages** : en-tête **et** corps, à l'aller **et** au retour.
   Le chiffre recoupe exactement les deux `write_all` de chaque direction — la mesure ne fait que
   confirmer ce que le code fait, mais elle le **chiffre** ;
2. **la pente DÉCROÎT avec le délai** (4,24 → 3,00) : ce n'est pas le protocole qui change, c'est
   le **proxy**, qui endort après chaque `recv` et laisse donc le système regrouper plusieurs
   écritures quand le délai est grand. La mesure donne donc un **majorant** du nombre de messages
   par pas, et c'est le petit délai qui est le plus fidèle ;
3. **conséquence chiffrée, et elle est actionnable** : si l'en-tête et le corps étaient écrits en
   **une seule** fois, le pas paierait ~2 messages au lieu de ~4 — soit, sur un lien à
   5 ms/message, **≈ 25 ms au lieu de ≈ 35 ms**, une économie de **~29 % de la durée du pas** qui
   ne touche ni le calcul ni les octets, seulement le **nombre d'envois**.

**LA FUSION A ÉTÉ FAITE, ET ELLE PAIE** : les trois émetteurs (jeton, lot dense, lot en listes)
écrivent désormais **une seule trame** — en-tête et corps concaténés. Mesure avant/après, aux deux
mêmes délais par message :

| délai/message | AVANT | **APRÈS** | gain |
|---|---|---|---|
| 2 ms | 23,35 ms | **19,06 ms** | **−18,4 %** |
| 5 ms | 34,93 ms | **27,98 ms** | **−19,9 %** |

**La pente retombe aussi** : (27,98 − 14,87) / 5 = **2,62 messages** au lieu de 4,01 — le pas
retrouve le nombre d'envois que le protocole décrit vraiment (un aller, un retour), le reste étant
le regroupement du proxy lui-même.

**Ce que ce gain est, et ce qu'il n'est pas** : **−20 % de la durée d'un pas** sur un lien qui
facture **par message**, sans toucher ni au calcul, ni aux octets, ni au résultat — la
vérification le confirme : `porte-flux.sh` reste **vert**, les cinq modes donnent exactement les
mêmes écarts (0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3). C'est **le seul levier de ce sprint
qui accélère sans rien coûter** — et il vient d'une mesure, pas d'une intuition.

**Et le gain est FIXE PAR ÉCHANGE, ce qui change ce qu'il représente.** Mesuré sur le même lien
(5 ms/message) en **mode 3 (lots de 8 jetons)** :

| mode | ce qu'un échange transporte | temps par échange | gain de la fusion |
|---|---|---|---|
| 0 (un jeton) | 896 canaux | 27,98 ms | **−20 %** |
| 3 (8 jetons) | 28 772 octets | 130,2 ms (dont 99,8 de calcul local) | **≈ −8 %** |

Le gain est le **même en millisecondes** (~10 ms : deux messages en moins à 5 ms), donc il
**pèse relativement moins** quand l'échange transporte plus. Autrement dit : **la fusion paie
d'autant plus que les pas sont petits** — et c'est précisément le régime du décodage, jeton par
jeton, celui où la latence domine.

**Ce qu'il ne dit pas** : le gain est nul sur un lien qui facture **au débit** (où deux écritures
coûtent les mêmes octets). La question « message ou octet ? » est celle de l'opérateur, pas du
protocole — mais le protocole, lui, ne doit pas **ajouter** de messages sans raison.
