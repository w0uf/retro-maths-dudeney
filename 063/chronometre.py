#!/usr/bin/env python3
"""Rétro Math's — n° 63 THE STOP-WATCH (Dudeney, 1917).
Trois aiguilles ; t en minutes après midi ; angles en degrés depuis le XII : heures t/2, minutes 6t, trotteuse 360t.
On cherche tous les instants (sur douze heures) où les trois écarts sont ceux de la gravure, dans un ordre ou dans
l'autre, puis on montre qu'une équidistance exacte est impossible. Calcul exact en fractions.
    python3 chronometre.py   (instantané)"""
from fractions import Fraction as F
from itertools import permutations
def ecarts(t):
    a = sorted([(t / 2) % 360, (6 * t) % 360, (360 * t) % 360])
    return sorted([a[1] - a[0], a[2] - a[1], 360 - a[2] + a[0]])
t0 = 9 * 60 + 5 + F(5, 11)                                  # 9 h 5 + 5/11 min
assert (t0 % 1) * 60 == 27 + F(3, 11)                       # trotteuse à 27 + 3/11 s
G = ecarts(t0)
print("écarts de la gravure :", [str(x) for x in G])
assert G == [109 + F(1, 11), 120, 130 + F(10, 11)]
def instants(gaps):
    """tous les t de [0, 720) où les écarts valent `gaps` : minutes - heures = 11t/2, trotteuse - heures = 719t/2"""
    out = set()
    for g1, g2, g3 in permutations(gaps):
        for alpha, beta in ((g1, g1 + g2), (g1 + g2, g1)):    # la trotteuse avant ou après l'aiguille des minutes
            for k in range(11):
                t = (2 * alpha + 720 * k) / F(11)
                if (F(719, 2) * t - beta) % 360 == 0 and 0 <= t < 720: out.add(t)
    return sorted(out)
S = instants(G)
print("instants :", [divmod(t, 60) for t in S])
t1 = 2 * 60 + 54 + F(6, 11)
assert S == [t1, t0] and ecarts(t1) == G
assert (t1 % 1) * 60 == 32 + F(8, 11) and t1 + 720 - t0 == 5 * 60 + 49 + F(1, 11)
# la seconde position est l'image de la première dans un miroir : angles 360 - θ
assert all(((360 - x) % 360) == y % 360 for x, y in zip((t0 / 2, 6 * t0, 360 * t0), (t1 / 2, 6 * t1, 360 * t1)))
# l'affirmation de Dudeney : jamais d'équidistance exacte (120, 120, 120)
assert instants([120, 120, 120]) == []
# témoins : la même recherche retrouve les instants où heures et minutes sont seules à 120° (ils existent)
assert any((11 * F(2 * 120 + 720 * k, 11) / 2) % 360 == 120 for k in range(11))
assert ecarts(F(4 * 60)) != G
print("contrôles : tout est conforme (témoins refusés)")
