"""n° 312 THE FIVE CRESCENTS OF BYZANTIUM : cinq croissants qui « surveillent » toutes les dalles (comme cinq dames),
et le plus grand tapis carré qui n'en recouvre aucun, même en partie."""
from itertools import combinations
C = [(x, y) for y in range(8) for x in range(8)]
def vus(p):
    x, y = p
    return {(a, b) for a, b in C if a == x or b == y or a - b == x - y or a + b == x + y}
V = {p: vus(p) for p in C}
dom = [s for s in combinations(C, 5) if len(set().union(*(V[p] for p in s))) == 64]
print("placements de cinq croissants qui surveillent tout le dallage :", len(dom))
DUD = {(2, 0), (1, 1), (0, 2), (7, 6), (6, 7)}
print("le sien en fait partie :", tuple(sorted(DUD)) in {tuple(sorted(s)) for s in dom})
# 1) tapis posé droit, sur les joints : le plus grand carré k×k sans croissant
def droit(s):
    best = 0
    for k in range(8, 0, -1):
        for x in range(9 - k):
            for y in range(9 - k):
                if not any(x <= a < x + k and y <= b < y + k for a, b in s): return k
    return 0
from collections import Counter
cd = Counter(droit(s) for s in dom)
print("tapis droit : côté maximal selon les placements :", sorted(cd.items()))
# 2) tapis à 45°, sommets au milieu des quatre bords (aire 32, la moitié) : dalles qu'il ne touche pas du tout
def hors_losange(a, b):
    """la dalle [a,a+1]×[b,b+1] est hors du losange |x-4| + |y-4| < 4 (bord compris : on tolère le contact)"""
    return min(abs(x - 4) + abs(y - 4) for x in (a, a + 1) for y in (b, b + 1)) >= 4
libres = [p for p in C if hors_losange(*p)]
print("dalles hors du tapis à 45° :", len(libres))
L = [s for s in dom if all(p in libres for p in s)]
print("placements compatibles avec ce tapis :", len(L), [sorted(s) for s in L])
# témoin : un placement surveillant tout mais avec un croissant sous le tapis doit être refusé
t = next(s for s in dom if not all(p in libres for p in s))
print("témoin refusé :", not all(p in libres for p in t))
# quatre croissants ne suffisent jamais
quatre = sum(1 for s in combinations(C, 4) if len(set().union(*(V[p] for p in s))) == 64)
print("placements de QUATRE croissants qui surveillent tout :", quatre)
from math import comb; print("placements de cinq croissants en tout :", comb(64, 5))
assert len(dom) == 4860 and len(L) == 4 and quatre == 0 and max(cd) == 5
