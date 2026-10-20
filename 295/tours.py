#!/usr/bin/env python3
"""Rétro Math's — n° 295 THE EIGHT ROOKS et n° 296 THE FOUR LIONS (Dudeney, 1917).
    python3 tours.py   (environ 2 s)
Tours non gardées qui couvrent le damier : n! ; et le compte « à retournements
près » que Dudeney déclare non encore déterminé pour l'échiquier."""
from itertools import permutations, combinations
from math import factorial
from collections import Counter

def images(p):
    """les 8 images d'une permutation (p[l] = colonne de la tour de la ligne l)"""
    n = len(p); pts = [(l, p[l]) for l in range(n)]
    T = [lambda l,c:(l,c), lambda l,c:(c,n-1-l), lambda l,c:(n-1-l,n-1-c), lambda l,c:(n-1-c,l),
         lambda l,c:(l,n-1-c), lambda l,c:(n-1-l,c), lambda l,c:(c,l), lambda l,c:(n-1-c,n-1-l)]
    out = []
    for t in T:
        q = [0]*n
        for l,c in pts:
            a,b = t(l,c); q[a] = b
        out.append(tuple(q))
    return out
NOMS = ["identité","quart de tour","demi-tour","trois quarts","miroir vertical","miroir horizontal","diagonale","antidiagonale"]

def classes(n):
    vus = set(); tailles = Counter(); fixes = [0]*8; reps = []
    for p in permutations(range(n)):
        im = images(p)
        for k in range(8): fixes[k] += im[k] == p
        if p in vus: continue
        orb = set(im); vus |= orb; tailles[len(orb)] += 1; reps.append(min(orb))
    return len(reps), dict(sorted(tailles.items())), fixes, sorted(reps)

SUITE = []
for n in range(1, 9):
    k, t, f, reps = classes(n); SUITE.append(k)
    assert sum(f) % 8 == 0 and sum(f)//8 == k            # Burnside recoupe le comptage direct
    print(n, "n! =", factorial(n), "| à symétrie près :", k, "| orbites par taille :", t)
    print("   points fixes", dict(zip(NOMS, f)))
    if n == 4: REPS4 = [''.join(str(c+1) for c in r) for r in reps]; print("   les 7 du n° 296 :", [''.join(str(c+1) for c in r) for r in reps])

# « Obviously there must be a rook in every row and every column » : contrôle exhaustif
def controle(n):
    cases = [(l,c) for l in range(n) for c in range(n)]
    ok = dom = 0
    for S in combinations(cases, n):
        L = {l for l,_ in S}; C = {c for _,c in S}
        if not all(l in L or c in C for l,c in cases): continue
        dom += 1
        # gardée = une autre tour sur sa ligne ou sa colonne (la plus proche la garde)
        if len(L) == n and len(C) == n: ok += 1
        else:
            assert any(sum(1 for x in S if x[0]==s[0])>1 or sum(1 for x in S if x[1]==s[1])>1 for s in S)
    return dom, ok
CTRL = []
for n in range(2, 7):
    dom, ok = controle(n); CTRL.append(ok == factorial(n) and dom == 2*n**n - factorial(n))
    print("damier", n, ": dispositions couvrantes", dom, "(formule 2n^n − n! =", 2*n**n - factorial(n), ") dont sans tour gardée", ok, "= n! :", ok == factorial(n))
print("échiquier : 2·8^8 − 8! =", 2*8**8 - factorial(8), "; part des non gardées :", factorial(8)/(2*8**8 - factorial(8)))


# --- ce que disent les articles
assert factorial(8) == 40320                       # n° 295, son compte
assert SUITE == [1, 1, 2, 7, 23, 115, 694, 5282]   # 5 282 a symetrie pres, « pas encore determine » en 1917
assert all(CTRL)                                   # son « evidemment », damiers 2 a 6
assert REPS4 == ["1234", "1243", "1324", "1342", "1432", "2143", "2413"]   # n° 296 : sa liste, dans son ordre
assert {len(set(images(tuple(int(x)-1 for x in r)))) for r in REPS4} == {2, 4, 8}
# temoins : la division par huit tombe juste et donne un faux compte ; une disposition gardee est refusee
assert 24 % 8 == 0 and 24 // 8 != SUITE[3] and 40320 // 8 != SUITE[7]
def non_gardee(S):
    return all(sum(1 for x in S if x[0] == s[0]) == 1 and sum(1 for x in S if x[1] == s[1]) == 1 for s in S)
assert non_gardee([(0, 1), (1, 3), (2, 0), (3, 2)]) and not non_gardee([(0, 0), (0, 1), (0, 2), (0, 3)])
print("controles : tout est conforme (temoins refuses)")
