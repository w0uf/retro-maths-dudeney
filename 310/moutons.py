#!/usr/bin/env python3
"""Rétro Math's — n° 310 THE THREE SHEEP (Dudeney, 1917). Trois moutons (dames)
sur 16 enclos : chaque enclos occupé ou en ligne avec un mouton. Toutes ses
affirmations, à symétrie près, avec et sans blocage.
    python3 moutons.py   (instantané)"""
from itertools import combinations
N = 4
C = [(l, c) for l in range(N) for c in range(N)]
def aligne(a, b): return a != b and (a[0]==b[0] or a[1]==b[1] or abs(a[0]-b[0])==abs(a[1]-b[1]))
def entre(a, b):
    dl = (b[0]>a[0])-(b[0]<a[0]); dc = (b[1]>a[1])-(b[1]<a[1]); x = (a[0]+dl, a[1]+dc); out = []
    while x != b: out.append(x); x = (x[0]+dl, x[1]+dc)
    return out
def couvre(S, blocage):
    for x in C:
        if x in S: continue
        if not any(aligne(s, x) and not (blocage and any(e in S for e in entre(s, x))) for s in S): return False
    return True
T = [lambda l,c:(l,c), lambda l,c:(c,N-1-l), lambda l,c:(N-1-l,N-1-c), lambda l,c:(N-1-c,l),
     lambda l,c:(l,N-1-c), lambda l,c:(N-1-l,c), lambda l,c:(c,l), lambda l,c:(N-1-c,N-1-l)]
def canon(S): return min(tuple(sorted(t(*x) for x in S)) for t in T)
def orbite(S): return {tuple(sorted(t(*x) for x in S)) for t in T}
def nom(S): return ''.join(sorted("ABCDEFGHIJKLMNOP"[l*4+c] for l, c in S))
def libres(S): return not any(aligne(a, b) for a, b in combinations(S, 2))
R = {}
for blocage in (False, True):
    print("=== blocage" if blocage else "=== simple alignement")
    for k in (2, 3):
        oui, non = {}, {}
        R[(blocage, k)] = (oui, non)
        for S in combinations(C, k):
            (oui if couvre(S, blocage) else non).setdefault(canon(S), set()).add(S)
        print(k, "moutons : couvrantes", len(oui), "familles /", sum(len(v) for v in oui.values()), "dispositions ; non couvrantes",
              len(non), "familles /", sum(len(v) for v in non.values()), "; total", sum(len(v) for v in oui.values())+sum(len(v) for v in non.values()))
        print("   couvrantes sans deux moutons en ligne :", [nom(f) for f in oui if libres(f)])
        print("   non couvrantes sans deux moutons en ligne :", [nom(f) for f in non if libres(f)])
        if k == 2: print("   les familles couvrantes à deux :", [nom(f) for f in oui])
        if k == 3:
            from collections import Counter
            print("   tailles des familles couvrantes :", dict(Counter(len(v) for v in oui.values())), "non couvrantes :", dict(Counter(len(v) for v in non.values())))
            # par paire : combien de troisièmes moutons
            premier = Counter()
            for f in oui: premier[f[0]] += 1
            print("   CEL :", nom(canon(((0,2),(1,0),(2,3)))), "couvre ?", couvre(((0,2),(1,0),(2,3)), blocage), "libres ?", libres(((0,2),(1,0),(2,3))))
# combien de dispositions un mouton seul / le minimum
print("un mouton couvre tout ?", any(couvre((x,), False) for x in C))
# cases jamais utiles, case la plus fréquente
from collections import Counter
cnt = Counter(x for S in combinations(C, 3) if couvre(S, False) for x in S)
print("fréquence des enclos dans les dispositions couvrantes :"); 
for l in range(4): print("  ", [cnt[(l, c)] for c in range(4)])

# --- ce que dit l'article (memes nombres avec ou sans blocage)
for b in (False, True):
    oui, non = R[(b, 3)]
    assert (len(oui), len(non)) == (47, 30)
    assert sum(len(v) for v in oui.values()) + sum(len(v) for v in non.values()) == 560
    assert sorted(nom(f) for f in R[(b, 2)][0]) == ["AK", "BN", "FG"]
    assert sorted(nom(f) for f in oui if libres(f)) == ["AGN", "AHO"]
    perd = [f for f in non if libres(f)]
    assert len(perd) == 1 and nom(((0,2),(1,0),(2,3))) == "CEL" and canon(((0,2),(1,0),(2,3))) == perd[0]
# l'exemple de la gravure, D E O, couvre
D, E, O = (0, 3), (1, 0), (3, 2)
assert couvre((D, E, O), False) and couvre((D, E, O), True)
# temoin : C E L, sa perdante, est bien refusee ; deux moutons en coin oppose (A, P) aussi
assert not couvre(((0,2),(1,0),(2,3)), False) and not couvre(((0,0),(3,3)), False)
print("controles : tout est conforme (temoins refuses)")
