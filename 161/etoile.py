# -*- coding: utf-8 -*-
"""n° 161 THE BETSY ROSS PUZZLE — plier un disque de papier et obtenir, d'UN
seul coup de ciseaux, une étoile à cinq branches.

Le pli : le disque en deux, puis la moitié (180°) en cinq secteurs de 36°,
repliés en accordéon. Un trait droit dans le coin plié donne, une fois déplié,
une figure à dix sommets alternés — les pointes à la distance a du centre, les
creux à la distance b. Reste à savoir quel trait donne la VRAIE étoile."""
from decimal import Decimal as D, getcontext
import math
getcontext().prec = 40

print("le demi-disque fait 180°, divisé en cinq parts :", 180/5, "degrés")
print("le coin plié fait donc 36°, et la figure dépliée a dix sommets,")
print("espacés de 36°, alternativement pointes et creux.")

# ── quel rapport creux/pointe donne l'étoile régulière {5/2} ? ───────────
r_sur_R = math.cos(math.radians(72)) / math.cos(math.radians(36))
phi = (1 + 5**0.5) / 2
print()
print("rapport creux/pointe d'une étoile régulière : cos72°/cos36° = %.9f" % r_sur_R)
print("   1/phi²                                    = %.9f" % (1/phi**2))
print("   les deux coïncident :", abs(r_sur_R - 1/phi**2) < 1e-12)
print("   soit, en sens inverse : la pointe est %.6f fois plus loin que le creux"
      % (1/r_sur_R))

# ── contrôle : la figure obtenue est-elle bien l'étoile régulière ? ──────
def sommets(a, b):
    """les dix sommets, pointes à la distance a, creux à la distance b"""
    p = []
    for k in range(10):
        d = a if k % 2 == 0 else b
        ang = math.radians(36*k)
        p.append((d*math.cos(ang), d*math.sin(ang)))
    return p

def alignes(p, q, r, tol=1e-9):
    return abs((q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])) < tol

for nom, b in (("étoile régulière", r_sur_R), ("creux trop près", 0.30),
               ("creux trop loin", 0.50)):
    p = sommets(1.0, b)
    # dans un pentagramme, le côté d'une pointe prolonge celui d'une autre :
    # les sommets 0 (pointe), 1 (creux) et 4 (pointe) sont alignés
    print("   %-18s b = %.6f → sommets 0, 1 et 4 alignés : %s"
          % (nom, b, alignes(p[0], p[1], p[4])))

# ── et l'angle de la pointe ─────────────────────────────────────────────
p = sommets(1.0, r_sur_R)
import itertools
def angle(o, u, v):
    ux, uy = u[0]-o[0], u[1]-o[1]; vx, vy = v[0]-o[0], v[1]-o[1]
    c = (ux*vx+uy*vy)/((ux*ux+uy*uy)**.5 * (vx*vx+vy*vy)**.5)
    return math.degrees(math.acos(max(-1, min(1, c))))
print()
print("angle au sommet d'une pointe : %.4f °  (l'étoile à cinq branches : 36°)"
      % angle(p[0], p[1], p[9]))

assert abs(r_sur_R - 1/phi**2) < 1e-12 and abs(angle(p[0], p[1], p[9]) - 36) < 1e-9
assert alignes(sommets(1, r_sur_R)[0], sommets(1, r_sur_R)[1], sommets(1, r_sur_R)[4])
assert not any(alignes(sommets(1, b)[0], sommets(1, b)[1], sommets(1, b)[4]) for b in (0.30, 0.50, 0.38, 0.385))
print("temoins : creux a 0,30, 0,38, 0,385 et 0,50 refuses ; seul 1/phi² aligne les branches")
