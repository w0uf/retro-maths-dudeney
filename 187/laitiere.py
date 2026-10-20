# -*- coding: utf-8 -*-
"""Rétro Math's — n° 187 THE MILKMAID PUZZLE (Dudeney, 1917).
Le point de la berge où puiser : construction par le symétrique du tabouret, confrontée à une recherche numérique
sans hypothèse, sur des prés tirés au hasard ; puis la variante rivière + haie.
    python3 laitiere.py   (instantané)"""
import math, random
random.seed(187)
def d(a, b): return math.dist(a, b)
print("=== 1. Le miroir : berge y = 0 ===")
for _ in range(5):
    S = (random.uniform(0, 3), random.uniform(.5, 4)); D = (random.uniform(4, 9), random.uniform(.5, 4))
    f = lambda x: d(S, (x, 0)) + d((x, 0), D)
    lo, hi = -5, 15
    for _ in range(200):
        a, b = lo + (hi-lo)/3, hi - (hi-lo)/3
        if f(a) < f(b): hi = b
        else: lo = a
    A = (S[0], -S[1]); xB = A[0] + (D[0]-A[0]) * (0-A[1]) / (D[1]-A[1])
    ang1 = math.degrees(math.atan2(S[1], abs(S[0]-xB))); ang2 = math.degrees(math.atan2(D[1], abs(D[0]-xB)))
    assert abs(lo - xB) < 1e-6 and abs(f(lo) - d(A, D)) < 1e-9 and abs(ang1 - ang2) < 1e-6
    assert f(xB + .5) > f(xB) and f(xB - .5) > f(xB)            # témoin : un autre point de la berge est plus long
    print("   minimum numerique x=%.6f | construction x=%.6f | longueur %.6f = droite A-porte %.6f | angles %.3f et %.3f"
          % (lo, xB, f(lo), d(A, D), ang1, ang2))
print("=== 3. Riviere y = 0 puis haie x = H ===")
for _ in range(4):
    H = 10; S = (random.uniform(0, 3), random.uniform(.5, 4)); D = (random.uniform(4, 9), random.uniform(.5, 4))
    best = min((d(S, (x/200, 0)) + d((x/200, 0), (H, y/200)) + d((H, y/200), D), x/200, y/200)
               for x in range(0, 2001, 4) for y in range(0, 1001, 4))
    S2 = (S[0], -S[1]); D2 = (2*H - D[0], D[1])
    assert d(S2, D2) - 1e-9 <= best[0] < d(S2, D2) + 1e-3
    assert d(S, D2) != d(S2, D2)                                 # témoin : sans le symétrique du tabouret, la longueur diffère
    print("   balayage %.4f | droite entre les deux symetriques %.4f" % (best[0], d(S2, D2)))
print("contrôles : tout est conforme (témoins refusés)")
