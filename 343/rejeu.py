# -*- coding: utf-8 -*-
"""Rejeu independant des suites de coups du n° 343."""
DEPART = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
C      = [6,9,4,15,1,12,7,10,8,5,14,3,13,2,11,0]

def rejoue(coups, depart=None):
    g = list(depart or DEPART)
    v = g.index(0)
    for m in coups:
        try: p = g.index(m)
        except ValueError: return None, "homme %d inconnu" % m
        if abs(p//4 - v//4) + abs(p % 4 - v % 4) != 1:
            return None, "l'homme %d n'est pas voisin de la cellule vide" % m
        g[v], g[p] = g[p], 0; v = p
    return g, None

SIEN = [12,11,15,12,11,8,4,3,2,6,5,1,6,5,10,15,8,4,3,2,5,10,15,8,4,3,2,5,10,15,
        8,4,12,11,3,2,5,10,15,6,1,8,4,9,8,1,6,4,9,12,2,5,10,15,4,9,12,2,5,3,11,
        14,2,5,14,11]
NOTRE = [15,11,7,6,2,3,6,7,10,2,3,6,7,8,12,15,11,14,2,3,8,12,15,10,3,8,5,9,8,5,
         9,1,6,9,12,7,4,15,10,3,14,11]

def montre(g):
    return "\n".join("   " + " ".join("%2s" % (x if x else "**")
                     for x in g[4*r:4*r+4]) for r in range(4))

for nom, suite in (("Dudeney", SIEN), ("le solveur", NOTRE)):
    g, err = rejoue(suite)
    print("=== %s : %d coups ===" % (nom, len(suite)))
    if err: print("   COUP ILLICITE :", err); continue
    print(montre(g))
    print("   arrive bien a la position C :", g == C)
    print()
print("gain : %d coups" % (len(SIEN) - len(NOTRE)))
