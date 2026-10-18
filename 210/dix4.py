# -*- coding: utf-8 -*-
"""n° 210 — les six figures fondamentales, et le carnet de Dudeney.

Cinq droites en position generale se coupent en dix points, quatre par droite :
la figure cherchee est donc un ARRANGEMENT DE CINQ DROITES. Deux arrangements
sont de meme « type » quand les points se succedent dans le meme ordre le long
de chaque droite — c'est la classification moderne des arrangements de droites,
et c'est exactement ce que Dudeney appelle ses six figures fondamentales.
"""
import sys, time
from math import gcd
from itertools import combinations, permutations

def droites(m, n):
    pts = [(x, y) for x in range(m) for y in range(n)]
    vues = {}
    for a, b in combinations(pts, 2):
        dx, dy = b[0]-a[0], b[1]-a[1]
        g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
        if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
        x, y = a
        while 0 <= x-dx < m and 0 <= y-dy < n: x, y = x-dx, y-dy
        vues[(x, y, dx, dy)] = None
    D = []
    for d in vues:
        x, y, dx, dy = d
        pl = []
        i, j = x, y
        while 0 <= i < m and 0 <= j < n:
            pl.append((i, j)); i, j = i+dx, j+dy
        if len(pl) >= 4: D.append((d, frozenset(pl)))
    return D

def inter(d1, d2):
    (x1, y1, a1, b1), (x2, y2, a2, b2) = d1, d2
    det = a1*b2 - a2*b1
    if det == 0: return None
    t = (x2-x1)*b2 - (y2-y1)*a2
    if t % det: return None
    t //= det
    return (x1 + t*a1, y1 + t*b1)

def cherche(m, n, limite=None):
    D = droites(m, n)
    sols = []
    def rec(depart, choisies, points):
        if len(choisies) == 5:
            sols.append((list(choisies), dict(points))); return
        if limite and len(sols) >= limite: return
        for k in range(depart, len(D)):
            nouveaux = {}
            ok = True
            for j in choisies:
                p = inter(D[k][0], D[j][0])
                if p is None or p not in D[k][1] or p not in D[j][1]:
                    ok = False; break
                if p in points or p in nouveaux.values(): ok = False; break
                nouveaux[(min(j, k), max(j, k))] = p
            if not ok: continue
            choisies.append(k); points.update(nouveaux)
            rec(k+1, choisies, points)
            for c in nouveaux: points.pop(c)
            choisies.pop()
    rec(0, [], {})
    return D, sols

def type_figure(D, choisies, points):
    """ordre des points le long de chaque droite -> forme canonique"""
    lab = {l: i for i, l in enumerate(choisies)}
    ordres = []
    for l in choisies:
        (x, y, dx, dy) = D[l][0]
        pl = [(pt, autre) for (a, b), pt in points.items()
              if l in (a, b) for autre in [b if a == l else a]]
        pl.sort(key=lambda t: (t[0][0]*dx + t[0][1]*dy))
        ordres.append(tuple(lab[o] for _, o in pl))
    best = None
    for p in permutations(range(5)):
        o = []
        for i, l in enumerate(choisies):
            s = tuple(p[x] for x in ordres[i])
            o.append(min(s, s[::-1]))
        c = tuple(sorted(o))
        if best is None or c < best: best = c
    return best

types = {}
if __name__ == "__main__":
    print("=== Recherche par tailles de damier ===")
    for (m, n) in ((7,7),(8,8),(9,7),(9,8),(9,9),(10,8),(11,7),(11,8),(11,9)):
        t0 = time.time()
        D, S = cherche(m, n)
        vus = {}
        for ch, pts in S:
            t = type_figure(D, ch, pts)
            vus.setdefault(t, 0); vus[t] += 1
            if t not in types: types[t] = (m, n)
        print("  %2d x %-2d : %4d arrangements, %d type(s)   (%.0f s)"
              % (m, n, len(S), len(vus), time.time()-t0), flush=True)
    print()
    print("=== Les types rencontres, et le plus petit damier qui les porte ===")
    for i, (t, (m, n)) in enumerate(sorted(types.items(), key=lambda kv: kv[1]), 1):
        print("  type %d : apparait des le damier %d x %d" % (i, m, n))
    print("  nombre de types distincts trouves : %d" % len(types))
    print("  Dudeney annonce six figures fondamentales.")
