#!/usr/bin/env python3
"""n° 279 THE BARRELS OF BALSAM — Dudeney, Amusements in Mathematics (1917).

Dix tonneaux numerotes 1 a 10, en deux rangees de cinq ; aucun tonneau ne
doit se trouver a droite ni au-dessous d'un tonneau de moindre valeur.
Combien de rangements ?

Dudeney repond 42, par la formule C(2n,n)/(n+1) — les nombres de Catalan —
et donne 5 pour six tonneaux en deux rangees de trois.  Il ne dit rien de
la raison : « This is quite easy to solve for any number of barrels — if
you know how. »
"""
from itertools import permutations
from math import comb, factorial

def valide(grille, lignes, colonnes):
    for r in range(lignes):
        for c in range(colonnes):
            v = grille[r*colonnes + c]
            if c+1 < colonnes and grille[r*colonnes+c+1] < v: return False
            if r+1 < lignes and grille[(r+1)*colonnes+c] < v: return False
    return True

def force_brute(lignes, colonnes):
    n = lignes*colonnes
    return sum(1 for p in permutations(range(1, n+1)) if valide(p, lignes, colonnes))

print("=== Force brute, deux rangees ===")
for c in range(1, 6):
    fb = force_brute(2, c)
    cat = comb(2*c, c)//(c+1)
    print("  %2d tonneaux, %d par rangee : %6d   Catalan %6d   %s"
          % (2*c, c, fb, cat, "ok" if fb == cat else "DESACCORD"))

print("\n=== Ses deux reponses ===")
print("  dix tonneaux, cinq par rangee :", force_brute(2, 5), " (il dit 42)")
print("  six tonneaux, trois par rangee :", force_brute(2, 3), " (il dit 5)")

# --- la formule des equerres, qui donne toutes les formes --------------
def equerres(forme):
    """nombre de tableaux standards de la forme donnee (formule des equerres)"""
    n = sum(forme)
    conj = [sum(1 for l in forme if l > j) for j in range(forme[0])]
    p = 1
    for i, l in enumerate(forme):
        for j in range(l):
            p *= (l - j) + (conj[j] - i) - 1
    return factorial(n)//p

print("\n=== Deux rangees, jusqu'a vingt-quatre tonneaux ===")
for c in range(1, 13):
    print("   %2d par rangee : %12d" % (c, equerres([c, c])),
          "   (Catalan ok)" if equerres([c,c]) == comb(2*c,c)//(c+1) else " DESACCORD")

print("\n=== Et s'il y avait trois rangees ? (il n'en parle pas) ===")
for c in range(1, 9):
    print("   %2d par rangee, %2d tonneaux : %12d" % (c, 3*c, equerres([c, c, c])))
print("\n  controle force brute, 3 rangees de 3 :", force_brute(3, 3))
print("  neuf tonneaux en trois rangees de trois :", equerres([3,3,3]))
print("  dix tonneaux en deux rangees de cinq   :", equerres([5,5]))
print("  -> meme nombre :", equerres([3,3,3]) == equerres([5,5]))

# --- la raison : le scrutin ------------------------------------------
print("\n=== Pourquoi Catalan : le depouillement d'un scrutin ===")
print("  lire 1,2,...,2n ; noter H si le tonneau va en haut, B s'il va en bas.")
print("  la condition equivaut a : a tout instant, autant ou plus de H que de B.")
def scrutin(n):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, avance):
        if avance < 0: return 0
        if i == 2*n: return 1 if avance == 0 else 0
        return f(i+1, avance+1) + f(i+1, avance-1)
    return f(0, 0)
for c in range(1, 8):
    print("   %2d par rangee : chemins %6d   tableaux %6d" % (c, scrutin(c), equerres([c,c])))
