#!/usr/bin/env python3
"""Rétro Math's — n° 345 THE TWO PAWNS (Dudeney, 1917).
Deux pions blancs sur leur case de depart, aux deux bords de l'echiquier ; de combien de facons
peuvent-ils aller tous deux a la 8e rangee, coup par coup, un seul pion jouant a chaque coup ?
Recurrence position par position, sans reprendre sa methode.
    python3 pions.py"""
from functools import lru_cache
from math import comb
@lru_cache(None)
def suites(a, b):       # rangées des deux pions (2..8)
    if a == 8 and b == 8: return 1
    t = 0
    for x, autre, pos in ((a, b, 0), (b, a, 1)):
        if x < 8:
            for pas in ((1, 2) if x == 2 else (1,)):
                y = x + pas
                t += suites(y, autre) if pos == 0 else suites(autre, y)
    return t
print("345 : suites de coups pour deux pions =", suites(2, 2))

assert suites(2, 2) == 2100
# ses quatre cas : aucun double pas, l'un ou l'autre, les deux
assert comb(12, 6) + 2 * comb(11, 5) + comb(10, 5) == 2100 == 924 + 462 + 462 + 252
# temoin : sans double pas, la recurrence doit donner C(12, 6) = 924 et pas 2 100
@lru_cache(None)
def simples(a, b):
    if a == 8 and b == 8: return 1
    return (simples(a + 1, b) if a < 8 else 0) + (simples(a, b + 1) if b < 8 else 0)
assert simples(2, 2) == 924 != 2100
print("controles : 2 100 = 924 + 462 + 462 + 252 ; sans double pas, 924 (temoin)")
