# Rétro Math’s : les calculs derrière les problèmes de Dudeney

La série *Rétro Math’s* du blog [blog.site2wouf.fr](https://blog.site2wouf.fr/) reprend un par un les 430 problèmes d’*Amusements in Mathematics* de Henry Ernest Dudeney (Londres, 1917 ; texte sur [Project Gutenberg](https://www.gutenberg.org/ebooks/16713)).

Quand un épisode affirme un résultat obtenu par programme, le programme est ici, avec de quoi le refaire. Un dossier par problème : 056, 081, 082, 083, 094, 101, 130, 142, 164, 194, 206, 210, 227, 244, 252, 263, 266, 269, 275, 276, 279, 343.

Python 3 ; Pillow et NumPy pour 130, 142 et 275 ; OR-Tools pour le solveur du 252 ; un compilateur C pour le 244 et le 343.

> ⚠️ **Ces dossiers contiennent les réponses.** Sur le blog, la solution n’arrive qu’en commentaire, quelques jours après l’article.

## 056 · WILSON'S POSER : huit personnes, et exactement trois façons

Un homme est à la fois l'oncle et le neveu d'un autre, sans aucun mariage dans les degrés prohibés. Dudeney donne une disposition, « la plus simple », et ajoute qu'« il y en a d'autres ». Le recensement de toutes les familles possibles répond :

- au sang seul, **sept** personnes suffiraient (deux dispositions, aucune à six), mais toutes deux exigent un mariage prohibé par alliance (la femme de son père, ou la fille de sa femme) ;
- avec la loi complète, il en faut **huit**, et il y a **trois** dispositions essentiellement différentes : la sienne (deux hommes épousent chacun la mère de l'autre), son reflet (deux hommes épousent chacun la fille de l'autre) et une troisième, mixte ;
- le résultat ne change pas selon que la sœur de l'épouse ou la veuve du frère sont permises ou non ;
- sans demi-frères, aucune solution jusqu'à huit personnes.

| Fichier | Rôle |
|---|---|
| `056/oncle.py` | Énumère les familles de n personnes (un sexe chacune, des parents pris parmi les précédentes), les ramène à une forme canonique et cherche l'oncle-neveu réciproque, au sang seul. Témoins : un frère qui épouse sa sœur doit être refusé, un oncle ordinaire ne doit pas compter comme réciproque. Environ 10 s. |
| `056/oncle2.py` | Ajoute les interdits d'alliance : les deux dispositions à sept tombent, il en reste trois à huit. Environ 35 s. |
| `056/oncle3.py` | Affiche les trois dispositions, situe celle de Dudeney, et refait le compte sous quatre variantes de la loi. Environ 3 min. |

## 081 · THE NINE COUNTERS : la réponse du livre n'est que troisième

Les chiffres 1 à 9, chacun une fois : (trois chiffres) × (deux chiffres) = (deux chiffres) × (deux chiffres), produit le plus grand possible. Le livre donne 5 568 (174 × 32 = 58 × 96). Il n'y a que **11** produits possibles ; le plus grand est **7 448 = 532 × 14 = 76 × 98**, et 7 008 = 584 × 12 = 73 × 96 bat aussi le livre.

| Fichier | Rôle |
|---|---|
| `081/jetons.py` | Essaie les 362 880 façons de poser les jetons, puis refait le compte par une seconde méthode (en partant des paires de deux chiffres) ; les deux doivent s'accorder. |

## 082 · THE TEN COUNTERS : ses deux réponses sont les deux bouts

Les jetons 0 à 9, chacun une fois, répartis entre deux multiplications de même produit ; le plus petit et le plus grand produit. Le partage est forcé, cinq jetons de chaque côté, ce que Dudeney ne dit pas : avec 4 et 6, ou 3 et 7, ou 2 et 8, les produits possibles des deux côtés ne se recouvrent jamais. Il y a 210 dispositions et 144 produits ; ses deux réponses sont exactement le plus petit et le plus grand, et chacune s'écrit de deux façons (le zéro final peut passer d'un facteur à l'autre).

| Fichier | Rôle |
|---|---|
| `082/jetons.py` | Le partage forcé, toutes les solutions, ses deux réponses, son raisonnement sur le plus petit produit (8 couples n, 2n possibles, le sien est le premier). Témoin : une disposition à deux zéros doit être refusée. Environ 6 s. |

## 083 · DIGITAL MULTIPLICATION : la somme maximale n'est pas 27 mais 30

Les chiffres 1 à 9, chacun une fois, en deux multiplications de même produit ; la plus petite et la plus grande somme des chiffres du produit. Il y a 59 solutions. Sa somme minimale (6) est juste et unique. Sa maximale ne l'est pas : il annonce 27 (9 × 654 = 18 × 327 = 5 886), or **7 × 984 = 56 × 123 = 6 888** donne **30**, et elle est unique elle aussi.

| Fichier | Rôle |
|---|---|
| `083/multiplication.py` | Toutes les permutations des neuf chiffres, coupées en quatre nombres de toutes les façons ; répartition des sommes ; ses deux réponses. Témoins : une égalité qui n'emploie pas les neuf chiffres doit être refusée. Environ 6 s. |

## 094 · THE DIGITAL CENTURY : sa réponse est la seule

Placer des signes entre 1 2 3 4 5 6 7 8 9, sans changer l'ordre, pour faire 100, avec le moins de signes possible. Dudeney trouve 123 − 45 − 67 + 89 et « ne pense pas qu'elle soit jamais battue ». Le recensement des 390 625 dispositions (rien, +, −, ×, ÷ entre deux chiffres, sans parenthèses) le confirme : 101 expressions valent 100, et **une seule** n'a que trois signes, la sienne. À quatre signes, il y en a exactement deux.

| Fichier | Rôle |
|---|---|
| `094/century.py` | Le recensement complet, calculé en fractions exactes. Il signale aussi une coquille de la transcription Gutenberg : la ligne « 123 + 4 − 5 + 67 − 8 − 9 » vaut 172 ; Dudeney avait écrit 123 + 4 − 5 + 67 − 89. |

## 101 · THE TRUSSES OF HAY : l'appariement est bien inutile, sauf avec quatre bottes

Cinq bottes pesées deux à deux de toutes les façons : dix nombres, sans savoir quelle pesée va avec quelle paire. Dudeney a raison, les cinq poids sont déterminés. Ce n'est pas vrai pour tout nombre de bottes : l'ambiguïté frappe 2, 4 et 8 bottes, les puissances de deux (Selfridge et Straus, 1958). Cinq pesées bien choisies suffiraient : 162 des 252 choix, ceux dont les paires relient toutes les bottes et ferment un cycle impair. Et parmi 80 erreurs de lecture simulées, une seule passe inaperçue : 115 lu 119.

| Fichier | Rôle |
|---|---|
| `101/bottes.py` | Reconstruction exhaustive puis en fractions exactes ; balayage de 2 à 8 bottes, éprouvé d'abord sur le témoin {1, 4, 6, 7} / {2, 3, 5, 8} ; les 252 choix de cinq pesées, deux critères comparés ; les 80 erreurs simulées. Instantané. |

## 130 · THE SCULPTOR'S PROBLEM : sa recette oublie une condition

Deux socles cubiques inégaux dont la somme des arêtes égale la somme des volumes. L'équation se réduit à x² − xy + y² = 1. La réponse de Dudeney est bien la plus petite (plus petit dénominateur 7, deux solutions à ce dénominateur), ses deux remarques préalables sont justes, sa loi des dénominateurs aussi. Mais sa recette à trois générateurs a > b > c ne marche que si **a = b + c** : sur 9 139 triplets, 8 774 ne donnent rien. Son exemple « plein de neuf » respecte la condition. Et la gravure dessine deux socles dans le rapport 1,27, quand la réponse exige 2,67.

| Fichier | Rôle |
|---|---|
| `130/socles.py` | Toutes les vérifications en fractions exactes, jusqu'au dénominateur 300 ; mesure de la gravure. Témoins : deux socles plus petits que le pied doivent être refusés, et le dénominateur 21 doit être signalé. N'imprime pas les fractions de la réponse. |
| `130/q130.png` | La gravure du livre (transcription Gutenberg, domaine public). |

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

## 164 · THE POTATO PUZZLE : la réponse est juste, la formule imprimée ne l'est pas

Combien de morceaux, au plus, avec six coups droits dans une tranche de pomme de terre ? Dudeney répond 22, et c'est juste. Mais la formule qu'il imprime, (n(n+1)+1)/2, donne 21,5 pour six coups : il manque 1 au numérateur, la bonne est (n(n+1)+2)/2. Et la gravure, six coups en quadrillage, ne fait que 16 morceaux, ce que cinq coups bien placés donnent déjà.

| Fichier | Rôle |
|---|---|
| `164/patate.py` | Trace n coupes qui se croisent deux à deux dans le disque et compte les morceaux sur un maillage fin, sans formule : 1, 2, 4, 7, 11, 16, 22, 29 pour 0 à 7 coups. Compte aussi la gravure (16). Témoin : trois coupes par un même point doivent perdre un morceau. |

Que ce soit le maximum tient en une phrase : la n-ième coupe croise au plus les n − 1 précédentes, donc traverse au plus n morceaux et en ajoute au plus n.

## 194 · THE GARDEN WALLS : chacun a autant de mur que le champ entier

Un champ circulaire, quatre chaumières sur un diamètre, trois murs ; même surface et même longueur de mur pour chacun. Sa construction (chaque mur fait de deux demi-cercles, de rayons k·R/4 et (4 − k)·R/4) donne bien quatre jardins égaux. Ce qu'il ne dit pas : les trois murs mesurent tous πR, et chaque locataire dispose de 2πR de mur, le périmètre du champ entier.

| Fichier | Rôle |
|---|---|
| `194/murs.py` | Longueurs des murs, et aire de chaque jardin mesurée sur un quadrillage de 3 000 × 3 000. Témoin : avec deux demi-cercles de même rayon, les aires doivent être refusées comme inégales. Environ 4 s. |

## 206 · THE KING AND THE CASTLES : ses deux affirmations sont exactes

Dix châteaux reliés par cinq murailles droites de quatre châteaux chacune ; combien de châteaux, au plus, peut-on mettre à l'abri, sans accès possible depuis le dehors sans franchir une muraille ? Dudeney répond deux, avec une seule figure. C'est le même objet que le n° 210 : un arrangement de cinq droites. Le nombre de châteaux à l'abri ne dépend que du type de la figure : 0, 1, 1, 1, 1 et 2 pour les six types. Deux est donc bien le maximum, une seule figure l'atteint (celle qui exige le damier 13 × 13 au n° 210), et l'étoile de la gravure n'en protège aucun.

| Fichier | Rôle |
|---|---|
| `206/chateaux.py` | Tire au hasard des milliers de jeux de cinq droites, reconstruit les régions du dessin (parcours des faces, région du dehors = aire signée minimale), compte les châteaux qui ne touchent pas le dehors, et classe le tout par type. Recoupe avec les figures du n° 210. |

## 210 · THE TEN COINS : le Compas sur 13 × 13, pas 17 × 12

Dix pièces en cinq lignes droites de quatre. Une telle figure est un arrangement de cinq droites : on énumère les droites du damier, pas les quadruplets de points. Dudeney classe six figures fondamentales et donne, d'après son carnet, le plus petit damier qui porte chacune ; pour le Compas, 17 × 12, en ajoutant « on peut les battre, mais je ne le crois pas ». Le balayage des damiers jusqu'à 13 × 13 trouve bien six types, et **le Compas tient sur 13 × 13** (169 cases contre 204). L'échiquier ordinaire, 8 × 8, porte trois types et non deux : le troisième, son carnet le place sur une planche plus grande.

| Fichier | Rôle |
|---|---|
| `210/dix4.py` | Les droites d'un damier, les arrangements de cinq droites dont les dix points tombent sur des cases, le type de chaque figure. |
| `210/dix5.py` | Balaie les damiers de 4 × 4 à 13 × 13 et donne, pour chaque type, les plus petits damiers qui le portent (environ 50 s). |
| `210/verifie.py` | Contrôle indépendant des 14 307 figures du damier 13 × 13 : dix cases distinctes, cinq alignements de quatre et pas d'autre. Témoin : une pièce déplacée d'une case doit être refusée. |

Réserve : le balayage s'arrête aux damiers de côtés 13 au plus.

## 227 · CENTRAL SOLITAIRE : 18 coups au lieu de 19

Le solitaire anglais à 33 trous, trou central vide au départ, une seule bille au centre à la fin, en le moins de coups possible (un coup = une bille qui enchaîne des sauts). Dudeney en fait 19 et ne pense pas qu'on puisse descendre plus bas ; **18 suffisent**. La littérature attribue les 18 coups à Ernest Bergholt, vers 1912 (non vérifié dans les sources d'époque). 17 est-il possible ? Question ouverte ici.

| Fichier | Rôle |
|---|---|
| `227/plateau.py` | Le plateau dans la numérotation de Dudeney et un vérificateur qui ne connaît que les règles. |
| `227/rejeu.py` | Rejoue les 19 coups de Dudeney et les 18 coups, saut par saut. Témoin : deux coups permutés doivent être refusés. |

La solution a été trouvée par « rencontre au milieu » (recherche en arrière sur 6 coups depuis la bille finale, en avant sur 12 depuis le départ) ; ce programme de recherche n'a pas été conservé. Ce qui est établi ici, c'est que la suite de 18 coups est valide.

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

## 263 · KING ARTHUR'S KNIGHTS : sa solution est la seule

Arthur et six chevaliers, trois soirs, jamais deux fois le même voisin ; le premier soir en ordre alphabétique, puis Beleobus le plus près possible d'Arthur et Galahad le plus loin. Trois soirs de sept voisinages font 21 paires, toutes celles de sept convives : chaque paire sert exactement une fois. Huit arrangements seulement évitent toute répétition, et **un seul** met Beleobus à deux places et Galahad à trois les deux soirs : le sien.

| Fichier | Rôle |
|---|---|
| `263/arthur.py` | Les 360 dispositions de la table, les couples de soirées sans voisin répété, le critère d'Arthur pris au pire des deux soirs. Témoin : une soirée qui reprend un voisinage du premier soir doit être refusée. Instantané. |

## 266 · A TENNIS TOURNAMENT : son défi à huit couples relevé, six couples impossible

Double mixte, quatre couples, deux courts, trois jours, personne ne joue deux fois avec ni contre la même personne. La grille de Dudeney est juste, et sa perfection est forcée : les comptes tombent au bord (12 partenariats sur 12, 24 oppositions sur 24), donc personne ne peut jamais jouer avec ni contre son conjoint. Il lance un défi : huit couples, quatre courts, sept jours. Une grille existe ; elle est dans `266/tennis8.json`. Le schéma tournant qui marche à quatre échoue à huit, et **six couples est impossible**. Dix couples : non conclu.

| Fichier | Rôle |
|---|---|
| `266/tennis.py` | Audit de sa grille, puis essai du schéma tournant à huit couples (échoue, sur les 105 appariements). |
| `266/tennis8.py` | Recherche générale à huit couples ; écrit `tennis8.json`. Environ 15 s. |
| `266/verifie.py` | Vérificateur indépendant, sans code commun avec la recherche, appliqué à sa grille et à `tennis8.json`. Témoins : deux dames échangées entre deux courts, et un jour rejoué, doivent être refusés. |
| `266/tennisn.py` | La même recherche pour 4, 6, 8 et 10 couples : 6 est impossible (recherche complète, 0,1 s), 10 épuise son budget de 40 millions de nœuds sans conclure (environ 5 min). |

## 269 · THREE MEN IN A BOAT : un tableau parfait, deux nombres faux

Quinze rameurs, sept jours, cinq canots de trois chaque jour, jamais deux fois les mêmes compagnons, jamais deux fois le même canot pour un homme, et le moins de canots possible : les quinze écolières de Kirkman, plus une couche. Son tableau est un système de Kirkman parfait (au premier jour, le texte imprime « DBF » pour DEF), et ses **10 canots sont optimaux**. Mais :

- son « 455 puissance 7 » compte des bordées, pas des répartitions : un jour donné, il y a 1 401 400 façons de répartir les hommes ;
- son « 15 567 552 000 solutions » vaut 2 × 15!/168, soit deux fois le nombre de façons de renommer les hommes de **sa propre** solution ; le nombre de systèmes de Kirkman d'ordre 15 étiquetés est **404 756 352 000** ;
- son tableau est l'espace projectif PG(3,2) : ses 35 bordées en sont les 35 droites.

| Fichier | Rôle |
|---|---|
| `269/rameurs.py` | Contrôle du tableau, nombre chromatique du graphe des conflits entre bordées (10, donc 10 canots au moins), 120 autres systèmes tirés au hasard (10 aussi), et le calcul de 455⁷ contre 1 401 400⁷ (environ 20 min). |
| `269/kirkman_orbites.py` | Le nombre exact de systèmes étiquetés, par double comptage et orbites des secondes journées (environ 16 min). |
| `269/sept_classes.py` | Contrôle par une autre route : tirages au hasard, classement par isomorphisme, groupes d'automorphismes (12, 12, 24, 24, 21, 168, 168) ; la somme des 15!/|Aut| redonne le même total (environ 7 min). |
| `269/pg32.py` | Trouve la numérotation des hommes par les vecteurs de quatre bits qui fait de chaque bordée une droite de PG(3,2). Témoin : après un échange de Pasch, le système couvre toujours chaque paire une fois, mais n'a plus de numérotation projective. |

Le passage historique « le problème peut désormais être considéré comme généralement résolu » est discuté dans l'article : le cas général n'est démontré qu'en 1968 (Ray-Chaudhuri et Wilson).

## 275 · THE SIXTEEN SHEEP : la série de Dudeney est complète, et ses dessins sont justes

Seize moutons enfermés par neuf claies ; en déplaçant 2, 3, 4, 5, 6 puis 7 claies, il faut obtenir trois enclos de 6, 6 et 4 moutons. Dudeney donne six dessins, les claies déplacées en trait épais. Relus aux pixels sur la gravure de 1917, ils sont tous justes : neuf claies, enclos de 6, 6 et 4, et autant de traits épais que le numéro du dessin.

| Fichier | Rôle |
|---|---|
| `275/denombre.py` | Essaie toutes les façons de poser neuf claies (environ 40 s) : 88 dessins font des enclos de 6, 6 et 4, avec 2 à 7 claies déplacées (2, 6, 12, 24, 28 et 16 dessins). |
| `275/figures_du_livre.png` | Les six dessins du corrigé (gravure du livre, domaine public). |
| `275/relire_figures.py` | Mesure l’encre de chaque cloison, reconstitue les enclos et juge chaque dessin. Deux témoins doivent être refusés : le départ lui-même, et le dessin 2 avec une claie effacée. |

Pour les dessins 4 et 6, le bord du carré est donné à la main dans le script : la détection automatique s’y trompe.

```sh
cd 275
python3 denombre.py
python3 relire_figures.py
```

## 276 · THE EIGHT VILLAS : tout est juste, et 365 à symétrie près

Huit villas autour d'un carré, neuf occupants par côté. Son total (2 035), son détail coin par coin et sa formule générale (n² + 3n + 2)(n² + 3n + 3)/6 sont exacts. La démonstration qu'il ne donne pas : en groupant selon le plus grand de deux coins opposés, le total vaut Σ (2k + 1)(n + 1 − k)². Et à rotation et reflet près, il reste **365** arrangements.

| Fichier | Rôle |
|---|---|
| `276/villas.py` | Force brute jusqu'à n = 15 contre sa formule et sa table, son détail coin par coin, la somme qui donne la formule, Burnside et énumération directe des orbites. Témoins : une formule altérée doit être rejetée ; pour n = 1, 7 arrangements et 3 à symétrie près, comptés à la main. Instantané. |

## 279 · THE BARRELS OF BALSAM : sa réponse et sa formule sont justes

Dix tonneaux numérotés de 1 à 10 en deux rangées de cinq, les numéros croissants le long de chaque rangée et de chaque colonne : combien de façons ? Sa réponse et sa formule C(2n, n)/(n + 1) sont exactes. Ce sont les nombres de Catalan, et neuf tonneaux en trois rangées de trois donnent le même compte que dix en deux rangées de cinq.

| Fichier | Rôle |
|---|---|
| `279/balsam.py` | Force brute sur les 10! ordres, formule des équerres jusqu'à 24 tonneaux, bijection avec le dépouillement d'un scrutin, et le cas 3 × 3. |

## 343 · EXERCISE FOR PRISONERS : 42 coups au lieu de 66

Un taquin de quinze prisonniers à ranger en parcours de cavalier, coin inférieur droit vide, avec le plus d'hommes possible au repos et le moins de coups possible. Les comptes de Dudeney sont exacts (80 arrangements, 40 atteignables, 2 hommes au repos au plus), mais sa liste de paires contient une coquille (5-13 au lieu de 5-15), il ne trouve que 4 des **9** cibles, et ses **66** coups sont battus : **42** suffisent, et 42 est optimal.

| Fichier | Rôle |
|---|---|
| `343/prisonniers.py` | Parcours de cavalier, parité, hommes au repos ; écrit les 9 cibles dans `cibles.txt`. |
| `343/taquin.c` | Solveur optimal du taquin 4 × 4 (IDA*, distance de Manhattan et conflits linéaires) ; donne 48, 50, 50, 42, 50, 50, 54, 52, 54 coups pour les 9 cibles. |
| `343/controle_taquin.py` | Contrôle de l'optimalité : une recherche en largeur sans heuristique donne la distance exacte de 920 893 positions ; sur 500 tirées au hasard, `taquin.c` doit trouver exactement cette distance. |
| `343/rejeu.py` | Rejoue coup par coup les 66 coups de Dudeney et les 42 du solveur. |

```sh
cd 343
gcc -O2 -o taquin taquin.c
python3 prisonniers.py && ./taquin < cibles.txt     # environ 12 s
python3 controle_taquin.py
python3 rejeu.py
```

Correction du 18/10/2026 : la première version de `taquin.c` comptait 2 coups de plus par paire de tuiles inversées dans une ligne, ce qui surestime quand trois tuiles sont inversées. `controle_taquin.py` l'a pris en défaut (3 positions sur 300 résolues en 18 coups au lieu de 16). Le calcul corrigé redonne les mêmes nombres pour les 9 cibles, dont 42.

## Licence

Code sous licence AGPL-3.0. Les énoncés de Dudeney sont dans le domaine public.
