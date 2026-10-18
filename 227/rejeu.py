#!/usr/bin/env python3
"""N° 227 CENTRAL SOLITAIRE : rejeu, saut par saut, de la solution de Dudeney (19 coups) et d'une solution en 18 coups.
Un coup = une bille qui enchaîne un ou plusieurs sauts. Départ : trou central (17) vide ; arrivée : une seule bille, au 17.
Numérotation de Dudeney, voir plateau.py.
    python3 rejeu.py"""
from plateau import rejoue

DUDENEY = [[19,17],[16,18],[29,17,19],[30,18],[27,25],[22,24,26],[31,23],[4,16,28],[7,9],[10,8],[12,10],[3,11],[18,6],
           [1,3,11],[13,27,25],[21,7,9],[33,31,23],[10,8,22,24,26,12,10],[5,17]]
DIX_HUIT = [[5,17],[8,10],[1,9],[16,4],[11,9],[13,11],[28,16],[21,23],[24,22,8,10,12],[3,1,9,23],[26,24,22],[7,21,23],
            [27,13,11],[33,25],[18,30],[31,33,25],[6,18,16,28,30,18],[19,17]]

def juge(nom, coups):
    r = rejoue(coups)
    ok = r == [17]
    print("%-22s %2d coups, %2d sauts → %s" % (nom, len(coups), sum(len(c) - 1 for c in coups),
          "une seule bille, au centre" if ok else "refusé : %s" % r))
    return ok

assert juge("Dudeney", DUDENEY)
assert juge("solution en 18 coups", DIX_HUIT)
# témoin : on intervertit deux coups de la solution en 18 ; le rejeu doit refuser
t = DIX_HUIT[:]; t[0], t[1] = t[1], t[0]
assert not juge("témoin (2 coups permutés)", t)
