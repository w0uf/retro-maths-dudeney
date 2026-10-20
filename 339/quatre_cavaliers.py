#!/usr/bin/env python3
"""Rétro Math's — n° 339 THE FOUR KNIGHTS' TOURS (Dudeney, 1917). Couper l'échiquier en quatre
parts superposables de sorte que chacune porte un tour fermé du cavalier.
On énumère ici toutes les découpes « en moulin » (les quatre parts se déduisent l'une de l'autre par quart de tour).
    python3 quatre_cavaliers.py   (environ 1 s)"""
import sys
from collections import Counter
sys.setrecursionlimit(10000)
N = 8
rot = lambda x: (x[1], N-1-x[0])
def orbite(x):
    o = [x]
    for _ in range(3): o.append(rot(o[-1]))
    return frozenset(o)
ORB = {(r, c): min(orbite((r, c))) for r in range(N) for c in range(N)}
SAUTS = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
def tours(P):
    S = set(P); V = {x: [(x[0]+a, x[1]+b) for a, b in SAUTS if (x[0]+a, x[1]+b) in S] for x in S}
    if any(len(v) < 2 for v in V.values()): return 0
    d = min(S); nb = 0; n = len(S)
    def rec(x, vus):
        nonlocal nb
        if len(vus) == n: nb += d in V[x]; return
        for y in V[x]:
            if y not in vus: vus.add(y); rec(y, vus); vus.discard(y)
    rec(d, {d}); return nb // 2
def chemins_ouverts(P):
    S = set(P); V = {x: [(x[0]+a, x[1]+b) for a, b in SAUTS if (x[0]+a, x[1]+b) in S] for x in S}; n = len(S); nb = 0
    def rec(x, vus):
        nonlocal nb
        if len(vus) == n: nb += 1; return
        for y in V[x]:
            if y not in vus: vus.add(y); rec(y, vus); vus.discard(y)
    for d in S: rec(d, {d})
    return nb
# énumération des parts connexes : une case par orbite, contenant le coin (0,0)
vues = set(); parts = []
def pousse(P, orbs, front):
    if len(P) == 16:
        k = frozenset(P)
        if k not in vues: vues.add(k); parts.append(k)
        return
    front = list(front)
    for i, x in enumerate(front):
        if ORB[x] in orbs: continue
        P2 = P | {x}; k = frozenset(P2)
        if (k, ) in vues: continue
        vues.add((k, ))
        nv = [y for y in ((x[0]+1,x[1]),(x[0]-1,x[1]),(x[0],x[1]+1),(x[0],x[1]-1)) if 0 <= y[0] < N and 0 <= y[1] < N and y not in P2]
        pousse(P2, orbs | {ORB[x]}, set(front) | set(nv))
pousse({(0,0)}, {ORB[(0,0)]}, {(0,1),(1,0)})
print("découpes en moulin (parts connexes de 16 cases contenant un coin) :", len(parts))
tr = lambda P: frozenset((c, r) for r, c in P)             # miroir diagonal : garde le coin (0,0)
classes = {min(tuple(sorted(P)), tuple(sorted(tr(P)))) for P in parts}
print("   à retournement près :", len(classes))
bons = []
for P in parts:
    t = tours(P)
    if t: bons.append((P, t))
print("parts portant un tour fermé du cavalier :", len(bons), "| nombre de tours par part :", Counter(t for _, t in bons))
for P, t in bons:
    print("   tours :", t, "| parcours ouverts orientés :", chemins_ouverts(P))
    for r in range(N): print("     ", ''.join('#' if (r, c) in P else '.' for c in range(N)))
carre = frozenset((r, c) for r in range(4) for c in range(4))
print("le carré 4×4 est une part en moulin :", carre in set(parts), "| tours fermés :", tours(carre), "| parcours ouverts :", chemins_ouverts(carre))
avec_chemin = sum(1 for P in parts if chemins_ouverts(P))
print("parts portant au moins un parcours complet (ouvert) :", avec_chemin)

# --- ce que dit l'article
if __name__ == "__main__":
    SIENNE = frozenset((r, c) for r, l in enumerate(["######..", "#####...", ".####...", "...#...."]) for c, x in enumerate(l) if x == "#")
    assert len(parts) == 1191 and len(classes) == 596 and avec_chemin == 34
    assert len(bons) == 2 and all(t == 1 for _, t in bons) and tr(bons[0][0]) == bons[1][0]   # une part et son miroir
    assert SIENNE in {P for P, _ in bons} and tours(SIENNE) == 1                            # la sienne, tour unique
    # temoins : le carre 4x4 (sa « meilleure idee ») ne porte aucun tour ; sa part privee d'un coin et completee ailleurs non plus
    assert tours(carre) == 0
    faux = (SIENNE - {(0, 5)}) | {(4, 3)}
    assert tours(faux) == 0
    print("controles : tout est conforme (temoins refuses)")
