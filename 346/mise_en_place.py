#!/usr/bin/env python3
"""Rétro Math's — n° 346 SETTING THE BOARD (Dudeney, 1917).
Les pièces sont des objets distincts : échanger deux pions blancs donne une autre mise en place.
Son calcul refait étape par étape, et la règle qui le fonde recontrôlée par énumération sur une petite armée.
    python3 mise_en_place.py   (instantané)"""
from itertools import permutations
from math import factorial, prod

def mises_en_place(effectifs):
    """nombre de façons de poser des pièces toutes distinctes sur leurs cases, chaque type sur les cases de son type"""
    return prod(factorial(k) for k in effectifs)

camp = mises_en_place([8, 2, 2, 2, 1, 1])          # pions, tours, cavaliers, fous, dame, roi
print("un camp :", camp, "| les deux :", camp ** 2, "| avec les deux poses du plateau :", 2 * camp ** 2)
assert camp == 40320 * 2 * 2 * 2 == 322560
assert camp ** 2 == 104044953600 and 2 * camp ** 2 == 208089907200
ans = 2 * camp ** 2 / (365.25 * 24 * 3600)
print("à une mise en place par seconde : %.0f ans" % ans)
assert round(ans) == 6594

# recontrole de la regle par enumeration directe : une petite armee de pieces numerotees (3 pions, 2 tours, 1 roi)
# posee sur ses six cases ; on compte les permutations qui respectent le type de chaque case
pieces = ["P1", "P2", "P3", "T1", "T2", "R"]
cases = ["P", "P", "P", "T", "T", "R"]
direct = sum(1 for p in permutations(pieces) if all(x[0] == c for x, c in zip(p, cases)))
assert direct == mises_en_place([3, 2, 1]) == 12
# temoins : celui qui oublie de retourner le plateau n'a que la moitie ; celui qui confond les pieces semblables n'a qu'une pose
assert camp ** 2 == 2 * camp ** 2 // 2 != 208089907200
assert len({tuple(x[0] for x in p) for p in permutations(pieces) if all(x[0] == c for x, c in zip(p, cases))}) == 1
print("controles : tout est conforme (temoins refuses)")
