# -*- coding: utf-8 -*-
"""n° 150 DISSECTING A MITRE — Dudeney, 1917.

La mitre est un carre prive d'un de ses quatre quartiers.  Il s'agit de la
decouper en cinq morceaux qui forment un carre parfait.  Dudeney commence
par demolir une solution en QUATRE morceaux publiee en Amerique, fondee sur
le « principe de l'escalier ».
"""
from fractions import Fraction as F
from math import isqrt, sqrt

COTE = 84                      # les trois grands cotes de la mitre
aire = COTE*COTE - (COTE//2)**2
print("=== La mitre ===")
print("  carre de %d moins un quartier de %d :" % (COTE, COTE//2), COTE*COTE, "-", (COTE//2)**2, "=", aire)
print("  rectangle equivalent en trois morceaux :", COTE, "x", aire//COTE,
      "->", COTE*(aire//COTE) == aire)
cote_carre = sqrt(aire)
print("  cote du carre cherche : racine de %d = %.4f" % (aire, cote_carre))
print("  soit exactement 42 racine de 3 :", abs(cote_carre - 42*sqrt(3)) < 1e-9)
print("  rapport au cote de la mitre : racine de 3 sur 2 — un nombre irrationnel.")

print("\n=== Sa demolition de la solution americaine ===")
a, b = F(84), F(63)
h, w = F(21, 2), F(12)
print("  rectangle de depart : %s x %s" % (a, b))
print("  marches : %s de haut, %s de large" % (h, w))
a2, b2 = a - w, b + h
print("  apres avoir descendu d'une marche : %s x %s" % (a2, b2))
print("  aire conservee :", a*b == a2*b2, "(%s = %s)" % (a*b, a2*b2))
print("  est-ce un carre ?", a2 == b2, " -> Dudeney a raison : c'est un oblong")
print("  et il tombe a %.4f pour cent du carre en cote" % (100*abs(float(a2)-cote_carre)/cote_carre))

print("\n=== Sa reparation : quel rectangle l'escalier saurait-il carrer ? ===")
print("  avec des marches de largeur %s sur un cote de %s, il y a %s marches." % (w, a, a/w))
n = a/w
bb = a*(n-1)**2/n**2
print("  pour que l'escalier donne un carre, le petit cote devrait valoir %s" % bb)
print("  Dudeney annonce 61 + 5/7 :", bb == F(432,7), "->", bb, "=", float(bb))
print("  verification : %s x %s = %s = %s au carre" % (a, bb, a*bb, isqrt(int(a*bb))))
print("     (le petit cote augmente de %s, soit 10 + 2/7)" % F(72,7))
print("     resultat : %s x %s" % (a - w, bb + F(72,7)))

print("\n=== Le principe de l'escalier, en general ===")
print("  un rectangle a x b coupe en n marches et glisse d'un cran devient")
print("  a(n-1)/n  x  bn/(n-1) ; c'est un carre si et seulement si b = a(n-1)^2/n^2.")
for n2 in range(2, 10):
    bb2 = F(84)*(n2-1)**2/n2**2
    print("     %d marches : il faudrait b = %-10s  (soit %.3f)" % (n2, bb2, float(bb2)))
print("  la mitre impose b = 63 : aucune de ces valeurs.")

# temoins et controles
print("\n=== Controles ===")
def glisse(a, b, n):
    """rectangle a x b coupe en n marches, glisse d'un cran"""
    return a*(n-1)/n, b*n/(n-1)
x, y = glisse(F(84), F(432, 7), 7)
print("  temoin positif : 84 x 432/7 a 7 marches ->", x, "x", y, "carre :", x == y)
x, y = glisse(F(84), F(63), 7)
print("  la mitre a 7 marches ->", x, "x", y, "carre :", x == y)
carres = [n2 for n2 in range(2, 2001) if (lambda u: u[0] == u[1])(glisse(F(84), F(63), n2))]
print("  nombres de marches de 2 a 2000 qui carrent la mitre :", carres or "aucun")
assert glisse(F(84), F(432, 7), 7)[0] == glisse(F(84), F(432, 7), 7)[1] and not carres
assert (a - w, b + h) == (72, F(147, 2)) and aire == 5292
