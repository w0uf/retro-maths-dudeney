#!/usr/bin/env python3
"""N° 275 THE SIXTEEN SHEEP : énumère toutes les façons de poser neuf claies sur les 24 cloisons intérieures du carré 4 × 4,
retient les dessins « propres » (chaque claie sépare deux enclos différents) et les classe selon les tailles des enclos,
puis, pour les enclos 6, 6 et 4, selon le nombre de claies déplacées par rapport au départ.
    python3 denombre.py"""
from itertools import combinations
from collections import Counter
# cases (r, c) ; arêtes intérieures : ('h', r, c) entre (r,c) et (r+1,c) ; ('v', r, c) entre (r,c) et (r,c+1)
A = [("h", r, c) for r in range(3) for c in range(4)] + [("v", r, c) for r in range(4) for c in range(3)]
cote = lambda e: ((e[1], e[2]), (e[1] + 1, e[2])) if e[0] == "h" else ((e[1], e[2]), (e[1], e[2] + 1))
init = {("h", 1, 0), ("h", 1, 1), ("h", 1, 2), ("h", 1, 3), ("v", 2, 0), ("v", 2, 2), ("h", 2, 1), ("h", 2, 2), ("v", 3, 1)}
def regions(murs):
    comp = {}; n = 0
    for r in range(4):
        for c in range(4):
            if (r, c) in comp: continue
            comp[(r, c)] = n; pile = [(r, c)]
            while pile:
                x = pile.pop()
                for e in A:
                    if e in murs: continue
                    a, b = cote(e)
                    y = b if a == x else a if b == x else None
                    if y is not None and y not in comp: comp[y] = n; pile.append(y)
            n += 1
    return comp, n
def propre(murs):
    comp, n = regions(murs); return comp, n, all(comp[cote(e)[0]] != comp[cote(e)[1]] for e in murs)
comp, n, ok = propre(init); print("départ :", len(init), "claies ;", sorted(Counter(comp.values()).values()), "; toutes utiles :", ok)
# énumération : les 3 régions d'abord (plus rapide) : toute partition propre = ensemble des arêtes entre régions différentes
sol = Counter(); ex = {}; total = 0; autres = Counter()
for murs in combinations(A, 9):
    m = set(murs); comp, n, ok = propre(m)
    if not ok: continue
    t = tuple(sorted(Counter(comp.values()).values())); autres[t] += 1
    if t == (4, 6, 6):
        k = 9 - len(m & init); sol[k] += 1; total += 1; ex.setdefault(k, sorted(m - init))
print("dessins propres à 9 claies selon les tailles :", dict(autres))
print("dessins 6, 6, 4 à 9 claies :", total, "; selon le nombre de claies déplacées :", sorted(sol.items()))
for k in sorted(ex): print("   ", k, "claies à poser en", ex[k])
