#!/usr/bin/env python3
"""Rétro Math's — n° 25 CHINESE MONEY (Dudeney, 1917).
Un ching-chang vaut deux pence plus quatre quinzièmes de ching-chang : c = 2 + 4c/15, d'où c = 30/11 penny.
Onze pièces rondes valent 15 ching-changs, onze carrées 16, onze triangulaires 17 : en onzièmes de ching-chang,
une pièce ronde vaut 15, une carrée 16, une triangulaire 17. La demi-couronne (30 pence) vaut 11 ching-changs,
soit 121 onzièmes ; la couronne, 242.
    python3 ching_chang.py   (instantané)"""
from fractions import Fraction as F
c = F(2) / (1 - F(4, 15))
assert c == F(30, 11) and c == 2 + F(4, 15) * c
assert F(30) / c == 11                                    # la demi-couronne vaut onze ching-changs

def rendus(N):
    """toutes les façons (r, s, t) : r rondes, s carrées, t triangulaires, de valeur exacte N onzièmes"""
    return [(r, s, t) for r in range(N // 15 + 1) for s in range(N // 16 + 1) for t in range(N // 17 + 1)
            if 15 * r + 16 * s + 17 * t == N]
demi, couronne = rendus(121), rendus(242)
print("demi-couronne :", demi)
print("couronne      :", couronne)
assert demi == [(7, 1, 0)]                                # une seule façon : sept rondes et une carrée
assert len(couronne) == 9 and sum(1 for x in couronne if all(x)) == 6
assert [x for x in couronne if not all(x)] == [(0, 13, 2), (14, 2, 0), (15, 0, 1)]
# l'étau du commentaire : N/17 <= nombre de pièces <= N/15
for N, L in ((121, demi), (242, couronne)):
    assert all(F(N, 17) <= sum(x) <= F(N, 15) for x in L)
assert {sum(x) for x in demi} == {8} and {sum(x) for x in couronne} == {15, 16}
# témoins : huit pièces rondes (120 onzièmes) ne font pas le compte ; une recherche qui oublierait
# les pièces triangulaires ne trouverait qu'une façon pour la couronne, au lieu de neuf
assert (8, 0, 0) not in demi and 15 * 8 != 121
assert [x for x in couronne if x[2] == 0] == [(14, 2, 0)]
print("contrôles : tout est conforme (témoins refusés)")
