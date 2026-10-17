# Rétro Math’s : les calculs derrière les problèmes de Dudeney

La série *Rétro Math’s* du blog [blog.site2wouf.fr](https://blog.site2wouf.fr/) reprend un par un les 430 problèmes d’*Amusements in Mathematics* de Henry Ernest Dudeney (Londres, 1917 ; texte sur [Project Gutenberg](https://www.gutenberg.org/ebooks/16713)).

Quand un épisode affirme un résultat obtenu par programme, le programme est ici, avec de quoi le refaire. Un dossier par problème.

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

## Licence

Code sous licence AGPL-3.0. Les énoncés de Dudeney sont dans le domaine public.
