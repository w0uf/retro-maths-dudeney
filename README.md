# Rétro Math’s : les calculs derrière les problèmes de Dudeney

La série *Rétro Math’s* du blog [blog.site2wouf.fr](https://blog.site2wouf.fr/) reprend un par un les 430 problèmes d’*Amusements in Mathematics* de Henry Ernest Dudeney (Londres, 1917 ; texte sur [Project Gutenberg](https://www.gutenberg.org/ebooks/16713)).

Quand un épisode affirme un résultat obtenu par programme, le programme est ici, avec de quoi le refaire. Un dossier par problème : 142, 244, 252, 275.

Python 3 ; Pillow et NumPy pour 142 et 275 ; OR-Tools pour le solveur du 252 ; un compilateur C pour le 244.

> ⚠️ **Ces dossiers contiennent les réponses.** Sur le blog, la solution n’arrive qu’en commentaire, quelques jours après l’article.

## 244 · THE FIFTEEN TURNINGS : quand Python bat Dudeney

Soixante-quatre villes en carré, huit par huit, à un mile l’une de l’autre. Le voyageur part de la ville noire (bord gauche, cinquième rangée en partant du haut), fait quinze tournants au plus et ne reprend jamais une route. Jusqu’où peut-il aller ?

- **Le livre :** 70 miles.
- **Le maximum :** **76 miles**, atteint par 528 trajets, qui font tous exactement quinze tournants et finissent tous sur le bord du haut.

Par exemple, en (colonne, rangée), rangée 0 en haut :

```
0,4 → 7,4 → 7,3 → 0,3 → 0,5 → 7,5 → 7,6 → 1,6 → 1,1 → 7,1 → 7,2 → 0,2 → 0,0 → 6,0 → 6,7 → 2,7 → 2,0
```

| Fichier | Rôle |
|---|---|
| `244/verif_244.c` | Recherche exhaustive en C, avec élagage par une borne supérieure (les plus longues portions de routes encore libres). |
| `244/trajets_76.txt` | Sa sortie : les 528 trajets de 76 miles. |
| `244/rejeu.py` | Rejeu indépendant en Python : vérifie route par route l’exemple de l’énoncé (37), le corrigé du livre (70) et les 528 trajets. Un trajet fautif sert de témoin et doit être refusé. |
| `244/controle_petits.py` | Contrôle de l’élagage : de 0 à 8 tournants, une recherche Python sans aucun élagage retrouve le même maximum et le même nombre de trajets que le programme C. |

```sh
cd 244
gcc -O2 -o verif_244 verif_244.c
./verif_244 15 76 76 > trajets_76.txt   # environ 50 s ; redonne le fichier à l’identique
python3 rejeu.py
python3 controle_petits.py              # environ 40 s
```

Usage du programme C : `verif_244 <tournants> <seuil> [affichage]` compte les trajets d’au moins `<seuil>` miles et donne le maximum ; avec un troisième argument, il affiche les trajets d’au moins cette longueur.

Maxima obtenus : 5 tournants → 38 (l’exemple de Dudeney en fait 37), 6 → 43, 7 → 48, 8 → 53, 13 → 70, 14 → 73, 15 → 76.

Nous ne savons pas si ce dépassement du livre a déjà été publié ailleurs. Signalez-le-nous si c’est le cas.

## 142 · THE SILK PATCHWORK : les sept découpages

Un patchwork en croix de 21 carrés. Il faut garder un carré entier et découper le reste en quatre morceaux identiques, en suivant les coutures, qui forment une croix grecque. Dudeney donne un découpage ; il y en a **sept** (aux symétries du patchwork près) : trois avec le carré gardé au centre, quatre avec le carré gardé au bord.

| Fichier | Rôle |
|---|---|
| `142/decoupages.py` | Énumère tous les découpages et retrouve celui du livre. Sans dépendance. |
| `142/planche.py` | Dessine la planche des sept découpages directement à partir du calcul (Pillow, police DejaVu). |
| `142/planche.png`, `142/planche.json` | La planche publiée sur le blog (composée pour la série, **pas une figure du livre**) et la position de ses panneaux. |
| `142/relire.py` | Relit la planche aux pixels seuls : reconstitue les morceaux de chaque panneau, vérifie qu’ils redonnent le calcul et que les sept sont distincts. Témoin : une coupe effacée doit faire refuser le panneau. |

```sh
cd 142
python3 decoupages.py
python3 planche.py planche.png        # redonne la planche au pixel près
python3 relire.py planche.png planche.json
```

## 252 · A PUZZLE FOR MOTORISTS : 157 tronçons au lieu de 159

Huit automobilistes vont chacun de sa maison à son église, sans que deux trajets passent jamais par le même carrefour. Le réseau du livre totalise **159** tronçons. CP-SAT (OR-Tools) en trouve un de **157**. Le minimum n’est pas prouvé : une borne par groupes de voitures montre qu’il faut au moins **121** tronçons.

| Fichier | Rôle |
|---|---|
| `252/verifie.py` | Contrôle indépendant, sans solveur : réseau du livre (159), réseau trouvé (157), témoin fautif refusé, borne 121. |
| `252/reseau_157.json` | Les huit trajets du réseau de 157, carrefour par carrefour (colonne, rangée). |
| `252/cpsat.py` | Le modèle CP-SAT : flot par voiture, un carrefour par voiture au plus, parité des trajets. |
| `252/bornes.py`, `252/bornes_4.json` | Optimum exact de chaque groupe de quatre voitures (les autres ignorées) ; la meilleure partition, ADEF (62) + BCGH (59), donne 121. |

```sh
cd 252
python3 verifie.py
pip install ortools
python3 -u cpsat.py "" 600             # repart du réseau de 157 ; réécrit reseau_157.json s’il trouve mieux
python3 -u bornes.py 4                  # long : 70 calculs de 30 min au plus
```

Toute amélioration en dessous de 157, ou toute borne au-dessus de 121, est bienvenue.

## 275 · THE SIXTEEN SHEEP : les six dessins du corrigé sont justes

Seize moutons enfermés par neuf claies ; en déplaçant 2, 3, 4, 5, 6 puis 7 claies, il faut obtenir trois enclos de 6, 6 et 4 moutons. Dudeney donne six dessins, les claies déplacées en trait épais. Relus aux pixels sur la gravure de 1917, ils sont tous justes : neuf claies, enclos de 6, 6 et 4, et autant de traits épais que le numéro du dessin.

| Fichier | Rôle |
|---|---|
| `275/figures_du_livre.png` | Les six dessins du corrigé (gravure du livre, domaine public). |
| `275/relire_figures.py` | Mesure l’encre de chaque cloison, reconstitue les enclos et juge chaque dessin. Deux témoins doivent être refusés : le départ lui-même, et le dessin 2 avec une claie effacée. |

Pour les dessins 4 et 6, le bord du carré est donné à la main dans le script : la détection automatique s’y trompe.

```sh
cd 275
python3 relire_figures.py
```

## Licence

Code sous licence AGPL-3.0. Les énoncés de Dudeney sont dans le domaine public.
