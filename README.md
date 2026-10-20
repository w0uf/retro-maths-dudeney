# Rétro Math’s : les calculs derrière les problèmes de Dudeney

La série *Rétro Math’s* du blog [blog.site2wouf.fr](https://blog.site2wouf.fr/) reprend un par un les 430 problèmes d’*Amusements in Mathematics* de Henry Ernest Dudeney (Londres, 1917 ; texte sur [Project Gutenberg](https://www.gutenberg.org/ebooks/16713)).

Quand un épisode affirme un résultat obtenu par programme, le programme est ici, avec de quoi le refaire. Un dossier par problème : 001, 018, 032, 046, 056, 060, 065, 078, 079, 081, 082, 083, 086, 088, 090, 093, 094, 101, 111, 118, 127, 128, 130, 132, 134, 136, 137, 140, 142, 150, 152, 157, 161, 164, 188, 194, 206, 210, 218, 219, 224, 227, 238, 244, 247, 250, 252, 263, 266, 268, 269, 275, 276, 279, 283, 286, 295, 296, 297, 298, 301, 309, 310, 343, 345, 363, 365, 371, 375, 377, 385, 387, 390, 396, 401, 404, 414, 415, 419.

Python 3 ; Pillow et NumPy pour 130, 142, 157 et 275 ; shapely pour le 152 ; OR-Tools pour le solveur du 252 ; un compilateur C pour le 224, le 244 et le 343.

> ⚠️ **Ces dossiers contiennent les réponses.** Sur le blog, la solution n’arrive qu’en commentaire, quelques jours après l’article.

## 001 · A POST-OFFICE PERPLEXITY : l'arithmétique laisse deux réponses, la grammaire une

Une couronne de timbres : des timbres à 2 d, six fois plus à 1 d, le reste à 2 d ½. En demi-pence, 16x + 5z = 120 n'a que **deux** solutions entières, (0, 0, 24) et (5, 30, 8). La première est exclue par l'énoncé (« donnez-moi *des* timbres à deux pence ») ; reste celle de Dudeney : 5, 30 et 8 timbres.

| Fichier | Rôle |
|---|---|
| `001/timbres.py` | Balayage complet. Témoins : trois commandes fausses, dont (5, 30, 9), doivent être refusées. Le script de l'atelier ayant été perdu, celui-ci le refait. Instantané. |

## 018 · THE MARKET WOMEN : la coquille est dans la transcription, pas chez Dudeney

Le nombre de marchandes est le nombre de diviseurs de la recette en farthings. Avec 2 s. 2 1/4 d. (édition de 1917) : 105 farthings, 8 diviseurs, 8 marchandes, comme au corrigé. Avec 2 s. 2 1/2 d. (transcription de Project Gutenberg) : 106 farthings, 4 marchandes seulement, et le corrigé ne tient plus. Si l'on admet les demi-livres, le nombre double (16) ; les quarts de livre, il triple (24). Entre 2 s. et 2 s. 6 d., les recettes donnent de 2 à 16 marchandes.

| Fichier | Rôle |
|---|---|
| `018/marchandes.py` | Diviseurs des deux recettes, variantes en demi-livres et quarts, balayage de la tranche. Témoins : 12 doit avoir six diviseurs, 13 deux. Instantané. |

## 032 · THE EXCURSION TICKET PUZZLE : son nombre exige le double florin

Payer 19 s 9 d (948 farthings) avec la monnaie courante du royaume : Dudeney annonce 458 908 622 façons sans donner sa méthode. On ne retrouve son nombre qu'en comptant le **double florin** (4 s, frappé de 1887 à 1890, jamais démonétisé) ; sans lui, on obtient 357 549 696. Son tableau de la monnaie rendue (douze pièces, du farthing au souverain) est exact aux douze lignes, et sa formule (n + 1)² pour le bronze aussi.

| Fichier | Rôle |
|---|---|
| `032/billets.py` | Programmation dynamique sur les farthings, pour plusieurs jeux de pièces ; sa formule du bronze ; son tableau. Témoins : le calcul est recoupé par une énumération directe sur de petites sommes, et une version fautive (qui compte les ordres de paiement) doit être refusée. Environ 1 s. |

## 046 · MARY AND MARMADUKE : aucune solution en mois entiers

Ses âges, 29 ans 2/5 et 19 ans 3/5, sont la seule solution ; en comptant par années ou par mois entiers, il n'y en a aucune, en cinquièmes ou en soixantièmes d'année, la sienne seulement. Entre 55 et 75 ans pour la somme annoncée, quatre valeurs seulement (59, 64, 69, 74) donnent des âges entiers : son 63 n'en est pas.

| Fichier | Rôle |
|---|---|
| `046/ages.py` | Recherche des âges à différents pas de temps, balayage des sommes. Témoin positif : la somme 64 doit donner des âges entiers. Instantané. |

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

## 060 · THE WAPSHAW'S WHARF MYSTERY : l'indice de la trotteuse est calibré

Les aiguilles des heures et des minutes se superposent onze fois en douze heures, toutes les 12/11 h ; une seule de ces superpositions tombe entre la 49ᵉ et la 50ᵉ seconde : 4 h 21 min 49 1/11 s, la réponse de Dudeney. Les onze tombent sur des secondes espacées de 60/11, donc au plus une par seconde : n'importe quelle seconde aurait suffi. Une seule tombe sur une seconde entière (midi) : les trois aiguilles ne sont ensemble qu'à midi et à minuit.

| Fichier | Rôle |
|---|---|
| `060/montre.py` | Les onze superpositions en fractions exactes, contrôle des angles. Témoin : 4 h 21 min 49 s pile ne doit pas passer le contrôle. Instantané. |

## 065 · THE RAILWAY STATION CLOCK : deux réponses, et un parallélisme impossible

Les aiguilles sont opposées et parallèles à une diagonale d'un mur de 71 pi 9 po sur 10 pi 4 po. Elles sont opposées onze fois en douze heures ; **deux** de ces instants conviennent, images l'un de l'autre dans un miroir (le mur a deux diagonales), et Dudeney n'en donne qu'un. Surtout, le parallélisme ne peut pas être exact : il faudrait hauteur/longueur = tan(π/22), irrationnel (théorème de Niven). Son mur s'en approche à 48,6 secondes d'arc.

| Fichier | Rôle |
|---|---|
| `065/horloge.py` | Les onze instants en fractions exactes, l'écart à la diagonale, la hauteur exacte qu'il faudrait, la marge de tolérance. Témoin : un mur carré ne doit désigner aucun instant. Instantané. |

## 078 · ODD AND EVEN DIGITS : sa somme est la seule

Écrire avec les impairs, puis avec les pairs, deux sommes égales (entiers et fractions propres, chaque chiffre une fois). Sur toutes les écritures possibles des deux groupes, une seule valeur est commune : la sienne, 84 1/3. Côté impairs elle s'écrit de deux façons (79 + 5 + 1/3 et 75 + 9 + 1/3), côté pairs d'une seule (84 + 2/6). Sans fraction, c'est impossible (preuve par neuf : 25 et 20 n'ont pas le même reste). Hors de l'article : les décimaux finis, que l'énoncé n'exclut pas, ne donnent aucune solution non plus.

| Fichier | Rôle |
|---|---|
| `078/chiffres.py` | Toutes les écritures des deux groupes, valeurs communes, cas sans fraction et variante décimale. Témoin : deux groupes de même reste modulo 9 ({1, 8} et {2, 7}) doivent, eux, se rencontrer sans fraction. Instantané. |

## 079 · THE LOCKERS PUZZLE : son compte et sa table sont exacts, et la table dit plus qu'il ne voit

Trois additions abc + def = ghi à neuf chiffres distincts. Il y a 544 additions (à l'ordre des termes près) et 115 totaux, de 356 à 981 ; le casier du milieu n'a que trois totaux possibles, les siens, et son compte de 3 072 dispositions est exact (1 × 3 × 2 classes, × 8³ échanges de colonnes). Sa table « chiffre omis → somme des chiffres du total » est exacte sur les 544 additions ; elle entraîne une loi qu'il n'énonce pas : 2·S(total) = 45 − d − 9c, donc **une retenue exactement si le chiffre omis est pair, deux s'il est impair**.

| Fichier | Rôle |
|---|---|
| `079/casiers.py` | Recensement des additions, les trois casiers, le compte de 3 072, la clause sur le zéro, sa table et la loi des retenues. Témoins : une addition qui emploie deux fois le 5 doit être refusée, une table où l'on échange deux lignes doit être contredite. Instantané. |

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

## 086 · QUEER MULTIPLICATION : 87 solutions avec 6, et seuls 3, 6 et 9 marchent

Un multiplicande de huit chiffres et un multiplicateur d'un chiffre prennent les neuf chiffres une fois, et le produit aussi. Dudeney donne une solution pour 6 ; il y en a 87. Avec 3 il y en a 336, avec 9, 144, et avec 2, 4, 5, 7, 8 aucune : la preuve par neuf impose que le carré du multiplicateur soit multiple de 9. Les trois multiplicateurs de son énoncé sont donc les trois seuls possibles.

| Fichier | Rôle |
|---|---|
| `086/multiplication.py` | Les 40 320 arrangements pour chaque multiplicateur de 2 à 9 ; contrôle de ses trois exemples. Témoins : sa réponse avec deux chiffres permutés doit être refusée. Instantané. |

## 088 · DIGITAL DIVISION : sa règle « de même le 1 » est fausse

Les neuf chiffres en deux nombres dont l'un divise l'autre : 89 solutions pour les quotients 2 à 9, toutes de la forme 4 chiffres / 5 chiffres. Ses huit couples sont valides et sont bien les plus petits ; son analyse par racines numériques et ses éliminations sur le 5 et le 6 sont exactes. Mais un numérateur peut finir par 1 : 16 des 89 solutions le font, dont sa propre réponse 6381/57429 pour le quotient 9.

| Fichier | Rôle |
|---|---|
| `088/division.py` | Toutes les solutions, ses huit couples, les racines numériques, ses règles d'élimination, les contre-exemples à la règle du 1. Témoins : deux partages faux doivent être refusés ; une force brute sur toutes les coupures possibles des neuf chiffres retrouve les mêmes 89 solutions. Instantané. |

## 090 · THE CENTURY PUZZLE : onze, et cent n'a rien de privilégié

100 = entier + fraction avec les neuf chiffres : il y a exactement onze écritures, ce sont exactement les siennes, et sa loi des racines numériques est exacte (les neuf chiffres font 45, donc a + b + c est multiple de 9). Sur les cibles de 1 à 200, cent n'arrive qu'au **36ᵉ rang** ; le champion est 89, avec 36 écritures, puis 71 (31) et 26 (29).

| Fichier | Rôle |
|---|---|
| `090/siecle.py` | Recherche exhaustive, ses onze écritures, ses racines numériques, ses éliminations, le classement des cibles de 1 à 200. Témoins : trois écritures fausses (mauvais dénominateur, mauvaise valeur, chiffres répétés) doivent être refusées. Environ 40 s. La première version n'essayait que des parties entières d'un ou deux chiffres, ce qui sous-comptait les cibles au-delà de 100 et plaçait cent au 34ᵉ rang. |

## 093 · THE MYSTIC ELEVEN : sa réponse maximale dépend de la règle que « peu de gens savent »

Nombres de neuf chiffres distincts divisibles par 11 : il y en a 296 640 ; le plus petit est 102 347 586, le plus grand 987 652 413, comme chez Dudeney. Il précise que peu de gens savent que la règle vaut aussi quand la différence des rangs est un multiple de 11 ; sa propre réponse maximale en dépend (différence 11) : avec une différence nulle seulement, on s'arrêterait à 987 645 230.

| Fichier | Rôle |
|---|---|
| `093/onze.py` | Force brute sur les 10 × 9! arrangements, le plus grand à différence nulle. Témoins : deux nombres non divisibles doivent être refusés par la règle des rangs, et la règle doit concorder avec la division sur 200 000 nombres consécutifs. Environ 6 s. |

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

## 111 · REAPING THE CORN : deux aires trop faibles d'un millième, et d'où elles viennent

La valeur exacte est 24 + 16√2 perches carrées. Son côté intérieur (4.8284) et son aire en acres (.2914) sont justes ; ses deux aires sont trop faibles d'un millième (46.626 pour 46.627, 23.313 pour 23.314). Elles s'expliquent : 4.8284 au carré donne 23.3134, d'où 23.313, et le double de 23.313 fait exactement 46.626.

| Fichier | Rôle |
|---|---|
| `111/moisson.py` | Calcul à trente chiffres, arrondis comparés aux siens, origine des deux aires. Témoin : le grand côté arrondi (6.8284) au carré ne redonne pas son nombre. Instantané. |

## 118 · CIRCLING THE SQUARES : six dispositions, et la règle 4n + 6 est un théorème

Dix cases en cercle, quatre nombres donnés ; pour deux voisines, la somme des carrés égale celle des deux opposées. L'écart des carrés de deux cases opposées est donc constant (192), au signe près ; ses cinq paires sortent des factorisations de 192, et il y a exactement **six** façons de compléter le cercle, comme il le dit. Sa remarque finale, « le nombre de cases doit être de la forme 4n + 6 », est exacte : le signe de l'écart alterne, donc la moitié du nombre de cases doit être impaire.

| Fichier | Rôle |
|---|---|
| `118/cercle.py` | Les paires, le balayage complet des dispositions, 260 = 16² + 2² = 14² + 8². Une recherche directe, qui n'emploie que la condition, trouve des cercles de 6 et 10 cases et aucun de 4, 8 ou 12 (nombres distincts jusqu'à 60). Témoin : deux cases voisines échangées doivent être refusées. Instantané. |

## 127 · SIMPLE DIVISION : le plus grand diviseur est aussi le seul

179, reste 164, comme au corrigé. En essayant tous les diviseurs de 2 à 2 312, aucun autre ne laisse quatre restes égaux. Les trois différences entre voisins suffisent (elles donnent le même pgcd que ses six), et les quatre nombres sont des multiples de 179 diminués de 15. En descendant depuis 700, il faut 522 essais pour tomber sur 179.

| Fichier | Rôle |
|---|---|
| `127/division.py` | Pgcd des différences, essai direct de tous les diviseurs. Témoins : {7, 12, 17} doit donner 5, {7, 12, 18} rien. Instantané. |

## 128 · A PROBLEM IN SQUARES : le défi de la raison 23 relevé

Trois carrés en progression arithmétique de raison 5, puis 7, puis 13 : ses réponses sont exactes, et sa remarque (en entiers, la raison est toujours multiple de 24) aussi, d'où les fractions. Trois carrés rationnels de raison d, c'est un triangle rectangle rationnel d'aire d : d est un nombre congruent. Pour son défi, la raison 23, on trouve trois nombres à dix chiffres sur le dénominateur 144 613 560, issus du triangle engendré par m = 156², n = 133².

| Fichier | Rôle |
|---|---|
| `128/planches.py` | Ses trois réponses en fractions exactes, le balayage des raisons entières, le triangle d'aire 23 et sa progression. Témoins : une réponse altérée d'une unité et un triangle mal recopié doivent être refusés. Instantané. |

## 130 · THE SCULPTOR'S PROBLEM : sa recette oublie une condition

Deux socles cubiques inégaux dont la somme des arêtes égale la somme des volumes. L'équation se réduit à x² − xy + y² = 1. La réponse de Dudeney est bien la plus petite (plus petit dénominateur 7, deux solutions à ce dénominateur), ses deux remarques préalables sont justes, sa loi des dénominateurs aussi. Mais sa recette à trois générateurs a > b > c ne marche que si **a = b + c** : sur 9 139 triplets, 8 774 ne donnent rien. Son exemple « plein de neuf » respecte la condition. Et la gravure dessine deux socles dans le rapport 1,27, quand la réponse exige 2,67.

| Fichier | Rôle |
|---|---|
| `130/socles.py` | Toutes les vérifications en fractions exactes, jusqu'au dénominateur 300 ; mesure de la gravure. Témoins : deux socles plus petits que le pied doivent être refusés, et le dénominateur 21 doit être signalé. N'imprime pas les fractions de la réponse. |
| `130/q130.png` | La gravure du livre (transcription Gutenberg, domaine public). |

## 132 · THE NINE TREASURE BOXES : 3 360, la plus petite et la seule

Neuf coffres carrés en trois progressions de même raison, le premier contenant au plus douze doublons. 3 360 est la plus petite raison qui porte trois progressions de trois carrés, et elle en porte exactement trois, les siennes. Sans la clause des douze doublons, il y a une infinité de réponses (multiplier les racines par k) et plusieurs familles indépendantes (43 680, 127 680…) ; avec elle, une seule raison du balayage convient.

| Fichier | Rôle |
|---|---|
| `132/coffres.py` | Toutes les progressions de trois carrés aux racines jusqu'à 4 000, classées par raison et par famille. Témoin : un coffre altéré d'une unité doit être refusé. Environ 1 s. |

## 134 · THE BANKER'S PUZZLE : le polynôme d'Euler, et la livre en est la borne

Le banquier dépose 40 pièces, le client en ajoute de 1 à 40, le banquier fait transférer le carré du nombre précédent : le total vaut m² + m + 41, premier pour les 40 coups. La clause « pas plus d'une livre » est exactement la borne du polynôme (m = 40 donne 41²), et seuls les dépôts 1, 2, 4, 10, 16, 40 rendent la recette infaillible (nombres chanceux d'Euler) ; seul 40 couvre la livre.

| Fichier | Rôle |
|---|---|
| `134/banquier.py` | Les 40 coups, le polynôme, la recherche des dépôts possibles. Témoins : les dépôts 39, 41 et 16 doivent échouer, 41 pièces ajoutées doivent faire perdre, le test de primalité doit refuser 1681 et 91. Instantané. |

## 136 · THE SULTAN'S ARMY : sa règle du facteur 2 n'est écrite qu'à moitié

Le plus petit effectif rangeable en deux carrés parfaits de douze façons. Sa réponse est la plus petite, ses douze paires sont exactes et complètes, ses lois sur les premiers 4n + 1 et 4n − 1 passent. Mais sa règle « doubler ne change rien, sauf quand cela double un carré » oublie le versant symétrique : doubler le double d'un carré fait perdre une façon (50 → 100). Telle qu'il l'écrit : 316 contre-exemples sous 200 000 ; complétée : aucun.

| Fichier | Rôle |
|---|---|
| `136/sultan.py` | Crible des décompositions jusqu'à 400 000, ses lois une à une, sa réponse et ses douze paires (le nombre n'est pas imprimé), la variante avec le carré nul. Témoins : les comptes de son texte (130, 25, 50, 15) faits à la main. Instantané. |

## 137 · A STUDY IN THRIFT : une coquille dans son tableau

Ses six nombres sont exactement les six premiers nombres à la fois carrés et triangulaires après 1 ; carrés, triangles et décompositions en trois triangles sont justes. Mais pour 1225, « deux triangles de côtés 36 et 34 » fait 1261 : il faut 35 et 34 (ou 45 et 19). La récurrence a(n) = 34 a(n−1) − a(n−2) + 2 tient, et sa phrase « tout entier est somme d'au plus trois triangulaires » (théorème d'Eureka de Gauss) est vérifiée jusqu'à 200 000.

| Fichier | Rôle |
|---|---|
| `137/epargne.py` | Son tableau ligne par ligne, la suite des carrés triangulaires, la récurrence, le théorème d'Eureka jusqu'à 200 000. Témoin : le contrôle doit refuser la ligne de 1225, et elle seule. Environ 5 s. |

## 140 · FIND ADA'S SURNAME : solution unique, et la clause « environ le quart » est inutile

Chaque dépense est le carré du métrage, et chaque mère dépense 405 farthings de plus que sa fille. 405 = 3⁴ × 5 ne se factorise en m² − d² que de **cinq** façons, une par mère. La solution est unique et c'est la sienne (Ada Smith, Annie Brown, Emily Jones, Mary Robinson, Bessie Evans) ; elle le reste quand on retire la clause « environ le quart » (rapport réel 0,2385).

| Fichier | Rôle |
|---|---|
| `140/ada.py` | Les cinq couples, la recherche avec et sans la clause. Témoins : Ada et Emily échangées doivent être refusées ; un écart mal converti (404 farthings) ne doit plus donner cinq couples. Instantané. |

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

## 150 · DISSECTING A MITRE : aucun escalier ne carre la mitre

La découpe américaine en quatre morceaux, fondée sur l'escalier, donne 72 × 73½ et non un carré : Dudeney a raison, et sa réparation (petit côté 61 + 5/7) est exacte. Plus fort : un rectangle de grand côté 84 glissé d'un cran sur n marches ne devient carré que si le petit côté vaut 84 (n − 1)²/n² ; la mitre impose 63, strictement entre n = 7 et n = 8, donc **aucun** nombre de marches ne convient. Le côté du carré, 42√3, est incommensurable avec celui de la mitre.

| Fichier | Rôle |
|---|---|
| `150/mitre.py` | Sa réfutation et sa réparation en fractions exactes, la formule générale de l'escalier. Témoin : 84 × 432/7 sur 7 marches doit donner un carré ; la mitre n'en donne aucun de 2 à 2 000 marches. Instantané. |

## 152 · ANOTHER JOINER'S PROBLEM : sa règle vaut pour toutes les tailles

Sa construction (reporter la moitié du grand côté du triangle, scier B F et B E) refaite en coordonnées sur huit triangles de taille croissante, jusqu'à près de deux fois le côté du carré : les deux traits sont toujours égaux et perpendiculaires, la découpe donne toujours cinq morceaux, deux restent en place, et un programme range les trois autres dans le carré final sans en retourner aucun. Quand le triangle a l'aire du carré, elle dégénère en trois morceaux.

| Fichier | Rôle |
|---|---|
| `152/menuisier.py` | Découpe et assemblage pour chaque taille (shapely). Témoin : l'assembleur doit ranger deux demi-carrés dans le carré, et refuser un 0,6 et un 0,5. Environ une seconde. |

## 157 · THE TABLE-TOP AND STOOLS : la découpe est exacte, et le maître pouvait gagner

Un plateau rond découpé en huit pièces pour faire deux tabourets percés d'un trou. La découpe de Dudeney tient à un seul nombre : des cordes à R·sin(π/8). Le bois est conservé au dernier chiffre (le trou vaut (π − 2√2)R²/4), ses trois affirmations comparatives sont vraies, et la gravure montre que le maître d'école a pris un cercle intérieur de rayon R/2. Mais avec un cercle de rayon inférieur à 0,370 R, le maître aurait fait un trou plus petit que l'élève, sans changer sa méthode.

| Fichier | Rôle |
|---|---|
| `157/tabouret.py` | Reconstruction des deux découpes, conservation du bois, intégration numérique du trou, mesure des gravures, comparaison des trous. Témoin : avec des cordes mal placées, les pièces ne se raccordent pas. Pillow et NumPy. |
| `157/q157.png`, `157/a157b.png` | Les gravures de l'énoncé et de la solution (transcription Gutenberg, domaine public). |

## 161 · THE BETSY ROSS PUZZLE : le nombre d'or sort du pliage

Le pli impose dix sommets espacés de 36°, alternativement pointes et creux ; le coup de ciseaux ne règle que la profondeur des creux. L'étoile régulière exige un rapport creux/pointe de cos 72°/cos 36° = 1/φ² = 0,381966… : c'est le seul qui aligne les côtés des branches, et l'angle au sommet vaut alors 36°.

| Fichier | Rôle |
|---|---|
| `161/etoile.py` | Les dix sommets, le rapport, l'alignement des côtés, l'angle de la pointe. Témoins : des creux à 0,30, 0,38, 0,385 et 0,50 doivent désaligner les branches. Instantané. |

## 164 · THE POTATO PUZZLE : la réponse est juste, la formule imprimée ne l'est pas

Combien de morceaux, au plus, avec six coups droits dans une tranche de pomme de terre ? Dudeney répond 22, et c'est juste. Mais la formule qu'il imprime, (n(n+1)+1)/2, donne 21,5 pour six coups : il manque 1 au numérateur, la bonne est (n(n+1)+2)/2. Et la gravure, six coups en quadrillage, ne fait que 16 morceaux, ce que cinq coups bien placés donnent déjà.

| Fichier | Rôle |
|---|---|
| `164/patate.py` | Trace n coupes qui se croisent deux à deux dans le disque et compte les morceaux sur un maillage fin, sans formule : 1, 2, 4, 7, 11, 16, 22, 29 pour 0 à 7 coups. Compte aussi la gravure (16). Témoin : trois coupes par un même point doivent perdre un morceau. |

Que ce soit le maximum tient en une phrase : la n-ième coupe croise au plus les n − 1 précédentes, donc traverse au plus n morceaux et en ajoute au plus n.

## 188 · THE BALL PROBLEM : le cube donne le même nombre que la sphère, et ce n'est pas un hasard

Six boules autour d'une boule au sol, et une sphère de diamètre 6 a une aire égale à son volume (π disparaît). Le cube de côté 6 aussi : pour tout solide circonscrit à une sphère, V = S·r/3, donc aire = volume revient à un rayon inscrit de 3, quelle que soit la forme. Vérifié sur la sphère, le cube, le tétraèdre et l'octaèdre réguliers, le cylindre.

| Fichier | Rôle |
|---|---|
| `188/boule.py` | Les deux réponses, le tableau des cinq solides. Témoin : le pavé 4 × 6 × 12 a lui aussi aire = volume (288), mais sans sphère inscrite ; la loi ne s'y applique pas. Instantané. |

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

## 218 · THE VICTORIA CROSS PUZZLE : six solutions en 18 coups, et sa curiosité des 28 coups ne coûte rien

Huit lettres de VICTORIA sur une croix de neuf cases, à faire tourner pour amener le V sur un bras noir. Sa remarque de parité est exacte, le minimum est 18 coups, il y a exactement six solutions optimales, sa séquence imprimée en est une, et ses trois traits communs se vérifient sur les six. Sa phrase « A VICTOR! A VICTOR! A VICTOR I! » (22 coups) arrive à bon port. Mais il présente comme coûteuse (28 coups) une solution où seuls les I passent par le centre : deux des six solutions optimales le font déjà, dont la sienne.

| Fichier | Rôle |
|---|---|
| `218/victoria.py` | Parcours en largeur des 181 440 positions, parité, solutions optimales, sa phrase mnémotechnique, la contrainte du centre. Témoins : sa séquence avec deux coups intervertis, ou sans le dernier coup, doit être refusée. Environ 1 s. |

## 219 · THE LETTER BLOCK PUZZLE : 23 coups, et un seul chemin optimal

Le taquin 3 × 3 à huit lettres. Ses 23 coups sont légaux et aboutissent ; 23 est le minimum, et il n'existe qu'**un** chemin optimal, le sien. Le petit taquin a 181 440 positions accessibles (la moitié de 9!) et un diamètre de 31 coups, atteint par deux positions.

| Fichier | Rôle |
|---|---|
| `219/taquin.py` | Rejeu de sa suite, parcours en largeur, comptage des chemins optimaux, diamètre. Témoins : sa suite avec deux coups intervertis, ou sans le dernier, doit être refusée. Instantané. |

## 224 · THE MOTOR-GARAGE PUZZLE : 43 coups, à deux coups du pire

Douze emplacements reliés en arbre (plan relevé sur la gravure), huit voitures ; une voiture se déplace d'aussi loin qu'elle veut par des cases libres, et il faut échanger les deux rangées. Sa séquence de 43 coups est légale et aboutit, et 43 est l'optimum exact ; il y a 99 264 séquences optimales (« there are other ways »). Les 19 958 400 positions sont toutes accessibles, et la plus éloignée du départ est à 45 coups : sa demande est à deux coups du maximum, et seules 3 986 positions sont aussi loin ou plus loin.

| Fichier | Rôle |
|---|---|
| `224/garage.c` | Parcours en largeur jusqu'au but (`gcc -O2 garage.c`). Environ 12 s, 330 Mo de mémoire. |
| `224/garage2.c` | Parcours complet : positions accessibles, répartition par distance, nombre de séquences optimales. Environ 13 s, 490 Mo. |
| `224/garage3.c` | Exemples de positions à 45 coups. Environ 12 s, 330 Mo. |
| `224/garage_verif.py` | Rejeu de sa séquence. Témoins : sans le dernier coup, avec deux coups intervertis, ou avec 6-H au lieu de 6-G, elle doit être refusée. Recoupement indépendant du C : les niveaux 0 à 4 du parcours, recalculés en Python, donnent 1, 8, 55, 250, 712. |

## 227 · CENTRAL SOLITAIRE : 18 coups au lieu de 19

Le solitaire anglais à 33 trous, trou central vide au départ, une seule bille au centre à la fin, en le moins de coups possible (un coup = une bille qui enchaîne des sauts). Dudeney en fait 19 et ne pense pas qu'on puisse descendre plus bas ; **18 suffisent**. La littérature attribue les 18 coups à Ernest Bergholt, vers 1912 (non vérifié dans les sources d'époque). 17 est-il possible ? Question ouverte ici.

| Fichier | Rôle |
|---|---|
| `227/plateau.py` | Le plateau dans la numérotation de Dudeney et un vérificateur qui ne connaît que les règles. |
| `227/rejeu.py` | Rejoue les 19 coups de Dudeney et les 18 coups, saut par saut. Témoin : deux coups permutés doivent être refusés. |

La solution a été trouvée par « rencontre au milieu » (recherche en arrière sur 6 coups depuis la bille finale, en avant sur 12 depuis le départ) ; ce programme de recherche n'a pas été conservé. Ce qui est établi ici, c'est que la suite de 18 coups est valide.

## 238 · ARRANGING THE JAM POTS : dix-sept échanges, n moins le nombre de cycles

Le rangement est lu sur la gravure ; la lecture se contrôle par son texte (seuls 13 et 19 sont à leur place). Le minimum d'échanges vaut n moins le nombre de cycles : 24 − 7 = 17, sa réponse, et ses dix-sept échanges, rejoués un par un, trient bien les pots. Il fait le calcul sans nommer le principe ; la formule est vérifiée par force brute sur toutes les permutations de 2 à 6 éléments (872 cas). Seuls 4,1 % des rangements possibles sont aussi faciles ou plus faciles que le sien.

| Fichier | Rôle |
|---|---|
| `238/pots.py` | Lecture de la gravure, cycles, ses dix-sept échanges, la formule contre la force brute, la loi du nombre de cycles. Témoins : sans son dernier échange, les pots ne sont pas triés ; une gravure mal lue (13 et 14 échangés) contredit son texte ; la force brute refuse la formule naïve « n − points fixes ». Environ 1 s. |

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

## 247 · INSPECTING A MINE : le problème du facteur chinois, 45 ans avant son nom

Vingt puits en quadrillage 5 × 4, trente et une galeries. Sa tournée de 36 stades parcourt les 31 galeries et en refait exactement cinq, celles qu'il nomme. 36 est le minimum (couplage minimal des dix nœuds impairs), et une tournée optimale finit en Q ou en S. Partir d'un nœud impair donnerait 35, comme il le dit. C'est le problème que Guan Meigu posera en 1962.

| Fichier | Rôle |
|---|---|
| `247/mine.py` | Le graphe, les nœuds impairs, le couplage minimal pour chaque arrivée, sa tournée rejouée. Témoins : sa tournée privée d'un puits, ou de ses trois derniers stades, doit être refusée. Instantané. |

## 250 · THE GRAND TOUR : la conclusion est juste, l'argument ne la prouve pas

La carte se ramène à une grille 4 × 6, A et Z aux coins opposés, de même couleur : aucun itinéraire ne passe une fois par chaque ville (0, par énumération). Avec sa faille (l'homme peut *entrer* une fois dans A), il y a 43 itinéraires, et tous reviennent en A aussitôt après l'avoir quitté, comme il l'affirme. Mais son coloriage ne l'impose pas : il permettrait des retours après 3 ou 5 villes, et ce n'est que l'énumération qui les exclut.

| Fichier | Rôle |
|---|---|
| `250/grand_tour.py` | Coloriage, énumération des itinéraires, les 43 avec la faille, les circuits que le coloriage n'exclut pas. Témoin : vers le coin de l'autre couleur, le même compteur doit trouver des itinéraires (47). Instantané. |

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

## 268 · THE PEAL OF BELLS : 24 sonneries à quatre cloches, et sa promesse à cinq est tenue

Une sonnerie juste : toutes les permutations une fois, aucune cloche ne saute de plus d'une place, jamais trois coups de suite à la première ni à la dernière place, et la sonnerie boucle. Sa sonnerie de quatre cloches est juste ; il y en a 24 au départ de 1234, 12 à lecture inverse près, 8 en identifiant aussi le miroir des places. Il dit en avoir construit à cinq et six cloches sans les donner : une recherche aveugle ne trouve rien en milliards de nœuds, mais en imposant la symétrie des vraies méthodes (la sonnerie se reproduit 24 rangées plus loin, les cloches renommées par un cycle d'ordre 5), une sonnerie de cinq cloches sort en un dixième de seconde. Six cloches : non tranché.

| Fichier | Rôle |
|---|---|
| `268/cloches.py` | Contrôle de sa sonnerie, recensement des sonneries justes de quatre cloches et de leurs classes. Instantané. |
| `268/cloches5sym.py` | Recherche d'une sonnerie de cinq cloches sous la symétrie d'ordre 5 ; écrit `peal5.json`. Instantané. |
| `268/peal5.json` | La sonnerie de cinq cloches trouvée (120 rangées). |
| `268/verifie.py` | Vérificateur indépendant des quatre règles. Témoins : deux rangées éloignées interverties, une rangée répétée, sa sonnerie à moitié lue à l'envers, une cloche trois fois en tête doivent être refusées ; la même sonnerie commencée ailleurs doit passer, et l'interversion des rangées 10 et 11 aussi (elle donne une autre sonnerie juste). |

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

## 283 · THE FIFTEEN DOMINOES : 126 720, et son nombre à treize chiffres est exact

Les quinze dominos du double-quatre en ligne : 126 720 façons, par énumération directe. Sa décomposition 264 × 2⁵ × 15 se retrouve : 528 circuits eulériens du pentagone depuis un sommet fixe, comptés deux fois parce que chaque circuit repasse deux fois par ce sommet, soit 264. Pour le jeu complet de 28, son 7 959 229 931 520 est exact (programmation dynamique sur les 2²¹ ensembles d'arêtes de K₇) ; mais le facteur des doubles y est 3⁷, et non 2⁷ : le « 2 » est le nombre de passages par chaque sommet. Les jeux au double impair ne s'alignent jamais.

| Fichier | Rôle |
|---|---|
| `283/dominos.py` | Énumération directe pour les doubles-deux, -trois et -quatre, les circuits du pentagone. Témoins : le double-deux doit donner 12, le double-trois 0 ; le faux facteur 2⁷ donnerait 465 835 130 880. Environ 3 s. |
| `283/dominos28.py` | Comptage des circuits eulériens de K₅ et K₇ par programmation dynamique, puis insertion des doubles et rupture du cercle. Environ 1 s. |

## 286 · PAINTING THE DIE : 48 marquages, mais deux dés seulement

Son compte de 48 marquages (6 × 4 × 2) est exact, mais il compte des dés tenus en main. Les 24 rotations du cube ramènent les 48 marquages à **deux** dés, images l'un de l'autre dans un miroir : aucune rotation ne fait passer de l'un à l'autre.

| Fichier | Rôle |
|---|---|
| `286/de.py` | Les 48 marquages, les 24 rotations construites, les orbites, le sens (déterminant des faces 1, 2, 3). Témoins : un marquage avec 1 face à 2 doit être refusé, un miroir doit changer de dé et aucune rotation ne le doit. Instantané. |

## 295 · THE EIGHT ROOKS : le nombre qu'il disait « pas encore déterminé »

Huit tours qui tiennent tout l'échiquier sans qu'aucune en garde une autre : 8! = 40 320, comme au corrigé. Son « évidemment une tour par rangée et par colonne » est contrôlé par l'essai complet sur les damiers de 2 à 6. Le compte à retournements et réflexions près, qu'il déclare non déterminé et difficile, est **5 282**, obtenu deux fois : en rangeant les dispositions par familles, et par le lemme de Burnside (40 320, 12, 384, 12, 0, 0, 764 et 764 dispositions fixes). Diviser par huit ne marche pas : 44 familles n'ont que deux membres, 418 en ont quatre. Suite de 1 à 8 cases de côté : 1, 1, 2, 7, 23, 115, 694, 5 282.

| Fichier | Rôle |
|---|---|
| `295/tours.py` | Familles et Burnside pour les côtés 1 à 8, contrôle exhaustif de son « évidemment ». Témoins : une rangée pleine de tours (qui se gardent) est refusée, et 40 320 / 8 ne redonne pas 5 282. Environ 2 s. |

## 296 · THE FOUR LIONS : sa liste est celle des plus petits représentants

Quatre lions sur 4 × 4, un par rangée et par colonne, à retournements près : 7 familles, comme au corrigé, et sa liste (1234, 1243, 1324, 1342, 1432, 2143, 2413) est exactement, et dans l'ordre, celle du plus petit représentant de chaque famille. Le piège : 24 / 8 = 3 tombe juste et c'est faux, car une seule famille (1342) a huit membres ; les autres en ont quatre ou deux.

| Fichier | Rôle |
|---|---|
| `296/tours.py` | Le même programme que le 295 (la partie « côté 4 »). Mêmes témoins. Environ 2 s. |

## 297 · BISHOPS—UNGUARDED : huit fous, et seulement sur les deux rangées du milieu

La portée d'un fou vaut 7 sur les 28 cases du bord, 9 sur 20 cases, 11 sur 12, 13 sur les 4 du centre. Les deux couleurs étant indépendantes, on cherche par couleur : 3 fous n'y suffisent jamais, 4 oui, d'où **8** fous, comme au corrigé ; 108 × 108 = 11 664 dispositions, dont 72 × 72 = 5 184 sans aucun fou gardé. Huit fous alignés ne couvrent l'échiquier que sur la 4e ou la 5e rangée. Sur les damiers de 2 à 8, le minimum est toujours le côté.

| Fichier | Rôle |
|---|---|
| `297/fous.py` | Essai complet par couleur, pièces faisant écran ; contrôle de ses deux diagrammes (297 et 298). Témoins : son diagramme du 298 privé d'un fou quelconque est refusé ; les huit fous alignés ne sont pas tous gardés. Environ 3 s. |

## 298 · BISHOPS—GUARDED : dix fous, son diagramme et sa variante

Chaque case tenue et chaque fou gardé : aucune disposition de 4 fous par couleur ne convient, il en faut 5, soit **10**, comme au corrigé ; 104 × 104 = 10 816 dispositions. Son diagramme (4e et 5e rangées, colonnes b, c, d, f, g) est valable, et sa variante aussi : les deux fous du milieu du groupe de six, qui « ne servent qu'à protéger », l'un monté d'une case, l'autre descendu.

| Fichier | Rôle |
|---|---|
| `298/fous.py` | Le même programme que le 297. Mêmes témoins. Environ 3 s. |

## 301 · THE EIGHT STARS : une seule solution, et c'est la sienne

Des 92 solutions des huit dames, 12 évitent les deux grandes diagonales (32 en posent une dame, 48 deux, aucune trois), et une seule passe par l'étoile imposée : 5 8 4 1 7 2 6 3, son diagramme. Les 12 forment deux familles, de 8 et de 4 aspects, comme il le dit ; celle de 4 (3 5 2 8 1 7 4 6) est la seule famille symétrique des 12 familles des huit dames. Chaque case permise est sur 1, 2 ou 3 solutions ; 16 cases donnent une solution unique. Damiers de 4 à 10, diagonales interdites : 2, 0, 4, 0, 12, 8, 12 solutions.

| Fichier | Rôle |
|---|---|
| `301/etoiles.py` | Filtrage des 92 solutions, familles, carte des cases, autres tailles. Témoins : une solution des huit dames qui touche une diagonale est écartée, une disposition qui s'attaque aussi. Instantané. |

## 309 · THE FORTY-NINE COUNTERS : quatre découpages en tout

Son carré est valable (jamais deux lettres ni deux chiffres pareils sur une ligne, une colonne ou une diagonale, petites diagonales comprises). Chaque lettre y occupe une solution des sept dames. Sur les 40 solutions des sept dames, il n'y a que **4** façons d'en prendre sept qui recouvrent le damier ; dans chacune, une lettre se décale du même nombre de colonnes (2, 3, 4 ou 5) à chaque rangée. Lettres et chiffres compatibles : 12 couples, soit 304 819 200 carrés en nommant lettres et chiffres de toutes les façons. Le sien : lettres au pas de 2, chiffres au pas de 4. Damiers de 4, 6 et 8 : aucun découpage ; de 5 : deux.

| Fichier | Rôle |
|---|---|
| `309/jetons49.py` | Contrôle de son carré, recherche exhaustive des découpages, couples compatibles. Témoin : son carré avec deux jetons de la première colonne échangés est refusé. Instantané. |

## 310 · THE THREE SHEEP : son tableau et ses cinq remarques

Trois moutons sur seize enclos, chaque enclos occupé ou en ligne avec un mouton : 47 familles à retournements près, et son tableau de quatorze lignes les donne toutes, sans doublon. Ses cinq remarques tiennent : 30 familles perdantes ; 320 + 240 = 560 dispositions en tout ; 3 façons avec deux moutons (AK, BN, FG) ; 2 gagnantes sans moutons en ligne (AGN, AHO) ; une seule perdante dans ce cas, C E L. Que les moutons se masquent ou non (dames qui font écran), les nombres sont les mêmes.

| Fichier | Rôle |
|---|---|
| `310/moutons.py` | Essai complet des dispositions, familles, avec et sans écran. Témoins : C E L et le couple A, P sont refusés ; l'exemple de la gravure (D, E, O) est accepté. Instantané. |

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

## 345 · THE TWO PAWNS : 2 100, retrouvé sans sa méthode

Deux pions à leurs deux bords, jouant l'un ou l'autre jusqu'à la 8e rangée : la récurrence position par position donne **2 100** suites, comme au corrigé, et ses quatre cas (aucun double pas, l'un, l'autre, les deux) font 924 + 462 + 462 + 252. Sans le double pas, on aurait C(12, 6) = 924.

| Fichier | Rôle |
|---|---|
| `345/pions.py` | Récurrence, ses quatre cas en coefficients binomiaux. Témoin : la même récurrence sans double pas doit donner 924, et pas 2 100. Instantané. |

## 363 · THE DOCTOR'S QUERY : 40 contre 1, et l'agitation ne sert à rien

Un quart d'once d'alcool versé dans l'eau, puis un quart d'once du mélange reversé : le flacon d'alcool finit à 400/41 d'alcool pour 10/41 d'eau, 40 contre 1, reflet exact de l'autre flacon. Il y a toujours autant d'eau dans l'alcool que d'alcool dans l'eau, quelles que soient les quantités, dès que chaque flacon retrouve son volume ; et cela tient même si l'on reverse un quart d'once de composition quelconque.

| Fichier | Rôle |
|---|---|
| `363/medecin.py` | Le calcul en fractions exactes, trois autres jeux de quantités, quatre compositions du retour. Témoin : si l'on ne reverse qu'un huitième d'once, l'égalité doit tomber. Le script de l'atelier ayant été perdu, celui-ci le refait. Instantané. |

## 365 · NEW MEASURING PUZZLE : onze est le minimum, et le second tonneau est indispensable

Deux récipients de dix pintes pleins, une mesure de 5 et une de 4 : mettre 3 pintes dans chacune des deux mesures. Ses onze transvasements sont le minimum, et il y a exactement 11 solutions en onze coups (à l'échange des deux grands récipients près). Avec un seul grand récipient, de 10 ou de 20 pintes : impossible.

| Fichier | Rôle |
|---|---|
| `365/mesures.py` | Parcours en largeur des situations, comptage des chemins optimaux, son tableau vérifié ligne à ligne, variantes à un seul récipient. Témoin : une ligne de tableau qui ne vide ni ne remplit doit être refusée. Instantané. |

## 371 · GOLD PACKING IN RUSSIA : le règlement rend la réponse unique

800 lingots de 12,5 × 11 × 1 pouces dans une caisse à fond carré, remplie exactement, avec au plus douze lingots sur chant. Sa caisse est remplie exactement, avec 8 lingots sur chant. Le volume permet cinq côtés ; deux sont impossibles par un argument élémentaire, et les deux autres se remplissent aussi, mais avec 96 lingots sur chant chacun. Sans la clause du règlement, le problème aurait trois solutions.

| Fichier | Rôle |
|---|---|
| `371/lingots.py` | Remplissages vérifiés case par case sur une grille au demi-pouce, côtés possibles, preuves d'impossibilité, caisses rivales. Témoins : un lingot retiré, puis un lingot décalé, doivent faire échouer le remplissage. Instantané. |

## 375 · FIVE JEALOUS HUSBANDS : onze traversées, et un seuil à quatre places

Cinq couples, un canot de trois places, aucune femme avec un autre homme sans son mari, ni sur les rives ni dans le canot : 11 traversées au minimum, comme Dudeney ; sans jalousie, 9 suffiraient. Pour la suite, ce n'est pas une loi mais un seuil : un canot de 2 places porte au plus 3 couples, un canot de 3 places au plus 5 (cinq couples sont donc pile au plafond), et à partir de 4 places il n'y a plus de limite.

| Fichier | Rôle |
|---|---|
| `375/jaloux.py` | Parcours en largeur des états (qui est sur quelle rive, où est le canot), table des minimums de 2 à 7 couples et de 2 à 5 places, le seuil. Témoins : une femme seule avec l'autre homme doit être refusée, des femmes seules entre elles acceptées. Environ 15 s ; `--loin` pousse les canots de 4 et 5 places jusqu'à 14 couples (environ 19 min) : 14 couples passent en 25 traversées avec 4 places, en 21 avec 5. |

## 377 · STEALING THE CASTLE TREASURE : onze coups, et tout tient à une incise

Une poulie, deux paniers, l'homme (195 lb), le jeune homme (105), le garçon (90) et le coffre (75), écart maximal 15 lb pour un humain qui descend. Onze manipulations est bien le minimum, et il y a 8 suites optimales. Si la limite valait aussi pour le coffre descendant seul, ce serait impossible : tout tient à l'incise « quoiqu'elle n'abîmât pas le bien volé ». La règle de chargement, elle, ne change rien.

| Fichier | Rôle |
|---|---|
| `377/panier.py` | Parcours en largeur sous trois lectures de la règle, sa suite vérifiée coup par coup, comptage des suites optimales, variante sans règle de chargement. Témoin : l'homme qui descend seul doit être refusé. Instantané. |

## 385 · "STRAND" PATIENCE : 56 coups, son record de 62 est battu

Deux piles de neuf cartes, quatre places vides ; une carte se pose sur une place vide ou sur la valeur immédiatement supérieure, et il faut échanger piques et trèfles. Dudeney : « 62 moves… This is my record; perhaps the reader can beat it. » Le plus court chemin parmi les 308 196 positions atteintes fait 56 coups, et aucun n'est plus court. Le modèle est validé de deux façons : ses remarques de l'énoncé (quatre cartes en 7 coups avec quatre places, en 9 avec trois, deux cartes au plus avec deux) sont retrouvées, et sa partie de 62 coups, écrite en blocs (« 4 C up on 5 D (9) »), se rejoue bloc par bloc avec exactement ses décomptes.

| Fichier | Rôle |
|---|---|
| `385/patience.py` | Parcours en largeur jusqu'à l'échange, et ses remarques sur les piles ; écrit `partie_56.txt`. Environ 3 s. |
| `385/partie_56.txt` | La partie de 56 coups. |
| `385/rejoue.py` | Rejeu indépendant, coup par coup. Témoins : sans le dernier coup, deux coups intervertis qui dépendent l'un de l'autre, une carte posée sur une valeur non voisine, un coup de trop doivent être refusés ; deux coups indépendants intervertis doivent passer. |
| `385/dudeney62.py` | Rejeu de sa partie de 62 coups, chaque bloc compté par le plus court chemin et comparé au sien. Témoin : un bloc compté 8 au lieu de 9 doit faire échouer le rejeu. |

## 387 · THE VILLAGE CRICKET MATCH : sa réponse tient à une hypothèse muette

Quatre courses apparemment complètes, « trois courtes » à chaque bout : Dumkins ne marque rien ; trois courses, « deux courtes » à chaque bout : Struggles marque un point. En essayant toutes les répartitions des arrivées bonnes et courtes, ses deux réponses sont les seules **si chaque batteur finit sa dernière course dans un pli**, ce que Dudeney suppose sans l'écrire. Sans cette condition, les annonces des arbitres laissent 16 façons de courir dans le premier cas, 9 dans le second, avec des issues différentes.

| Fichier | Rôle |
|---|---|
| `387/cricket.py` | Toutes les répartitions, avec et sans l'hypothèse. Témoins : sans aucune course courte, quatre allers simples ramènent chacun chez soi et trois les font changer de bout. Instantané. |

## 390 · THE HORSE-RACE PUZZLE : 12, 15, 20, et un bookmaker imaginaire

Cotes de 4, 3 et 2 contre 1 : miser 12, 15 et 20 livres rapporte 13 livres quel que soit le vainqueur, comme il le dit. Le pari sûr n'existe que parce que les probabilités implicites (1/5, 1/4, 1/3) totalisent 47/60, moins que 1 ; avec un livre juste, le gain garanti est nul, et avec une marge, il n'y en a aucun.

| Fichier | Rôle |
|---|---|
| `390/course.py` | Son exemple à 5 livres, la résolution exacte, trois livres de cotes comparés. Témoin : 12 / 15 / 21 doit donner des gains inégaux. Instantané. |

## 396 · A MATCH MYSTERY : ses treize répartitions, et l'exception qu'il omet

Trente allumettes en trois tas, qui prend la dernière perd (Nim « misère ») : le calcul direct du jeu, sans théorie, retrouve exactement ses treize répartitions gagnantes. Sa règle des puissances de deux (le ou exclusif de Bouton, 1901) est exacte, sauf dans les positions où chaque tas ne contient qu'une allumette ; il signale « 1 et 1 » dans son dialogue, mais pas dans l'énoncé de la règle, et le dernier coup de sa propre partie d'exemple (1, 1, 1) est justement celui que sa règle déconseille. Le mot « inégaux » de l'énoncé est superflu.

| Fichier | Rôle |
|---|---|
| `396/allumettes.py` | Le jeu calculé par récursion, la règle confrontée au calcul, le nombre de répartitions selon le total (1, 4, 13, 40 pour 6, 14, 30, 62), sa partie d'exemple. Témoins : (16, 13, 1) doit être perdante pour qui la laisse, et (1, 1) gagnante pour qui joue. Instantané. |

## 401 · EIGHT JOLLY GAOL BIRDS : ses deux suites sont les seules

Taquin 3 × 3 à former en carré magique : 8 carrés possibles, 4 atteignables (parité du taquin), minimum 19 coups, deux carrés atteints en 19 ; les deux autres coûtent 23 et 25. Chacun des deux carrés à 19 coups n'a qu'une seule suite optimale, et ce sont exactement les deux qu'il imprime ; dans l'une, le prisonnier n° 3 ne bouge pas.

| Fichier | Rôle |
|---|---|
| `401/prisonniers9.py` | Les carrés magiques, parcours en largeur des 181 440 positions, toutes les suites optimales, ses deux suites rejouées. Témoins : sa suite sans le dernier coup, ou avec deux coups intervertis, doit être refusée. Environ 1 s. |

## 404 · THE SIBERIAN DUNGEONS : les 14 déplacements de Mr. Wotherspoon sont un minimum

Seize prisonniers doivent former un carré magique dans un carré de cellules, chacun ne bougeant que par des cellules vides. Dudeney donne la solution en 14 déplacements d'un lecteur et se dit « confident that it cannot be improved upon », sans le démontrer. Sur les 7 040 carrés magiques d'ordre 4, un prisonnier mal placé bouge au moins une fois : un carré qui en laisse k en place demande au moins 16 − k déplacements. Les 13 carrés qui en laissent trois ou quatre ne se forment ni en 13 ni en 14 ; parmi ceux qui en laissent deux, un seul se forme en 14, celui du corrigé. 14 est donc le minimum, et il n'y a qu'un carré pour l'atteindre.

| Fichier | Rôle |
|---|---|
| `404/cachots.py` | Rejeu des 14 déplacements, recensement des carrés magiques, preuve du minimum. Témoins : au départ, le prisonnier 16, muré par 8 et 15, ne doit pas pouvoir sortir ; le carré du corrigé doit se former en 14 et pas en 13. Une dizaine de secondes. |

## 414 · WHO WAS FIRST? : la balle doit battre le son

À un mille, la lumière met 5,4 millionièmes de seconde, le son de 4,9 s (0 °C) à 4,7 s (20 °C). L'ordre du corrigé suppose que la balle tienne en moyenne plus de 340 m/s sur tout le mille (15 °C), ce que Dudeney ne dit pas.

| Fichier | Rôle |
|---|---|
| `414/balle.py` | Temps de la lumière et du son selon la température (formule usuelle de la vitesse du son dans l'air sec). Témoins : 331,3 m/s à 0 °C et 343 m/s à 20 °C. Instantané. |

## 415 · A WONDERFUL VILLAGE : vrai partout ? non, pas au Japon en hiver

Le soleil est plus proche à midi qu'à son lever de R cos z, où z est sa distance zénithale à midi. Avec R = 3 959 milles, l'écart ne dépasse 3 000 milles que si z < 40,7°. La réponse de Dudeney suppose le soleil au zénith : au Japon, elle est fausse une partie de l'année (Tokyo : 157 jours sur 365 ; Sapporo : 194), et elle n'est vraie toute l'année qu'en dessous d'environ 17° de latitude.

| Fichier | Rôle |
|---|---|
| `415/village.py` | Le seuil, l'écart selon la date, le nombre de jours par latitude (déclinaison approchée par une sinusoïde). Témoins : à l'équateur, vraie 365 jours, au pôle, aucun. Instantané. |

## 419 · THE FIVE PENNIES : « à égale distance » est impossible au sens propre

Le déterminant de Cayley-Menger de cinq points deux à deux à la même distance vaut −5 : ils ne tiennent pas dans l'espace. Celui de quatre vaut 4 : ils ne tiennent pas dans un plan. Les pennies ne se touchent tous que grâce à leur forme plate, pas par leurs centres.

| Fichier | Rôle |
|---|---|
| `419/pennies.py` | Déterminants exacts (fractions). Témoins : quatre sommets d'un carré et cinq sommets d'un cube doivent donner 0. Instantané. |

## Licence

Code sous licence AGPL-3.0. Les énoncés de Dudeney sont dans le domaine public.
