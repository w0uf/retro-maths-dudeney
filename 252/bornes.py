#!/usr/bin/env python3
"""N° 252 : bornes inférieures par sous-groupes de voitures.
Pour un groupe de voitures, l'optimum exact (les autres voitures ignorées, sauf leurs terminus, toujours interdits)
minore la part de ce groupe dans le total ; une partition des huit voitures donne donc une borne inférieure du total.
    python3 -u bornes.py 4      (groupes de 4 : 70 calculs de 30 min au plus, sur 12 processus)"""
import itertools, os, sys
from ortools.sat.python import cp_model

W, H = 18, 11
M = dict(A=((12, 0), (12, 9)), B=((2, 2), (2, 10)), C=((7, 2), (17, 2)), D=((15, 2), (15, 10)), E=((8, 3), (17, 3)), F=((0, 7), (14, 7)), G=((0, 5), (12, 5)), H=((5, 0), (5, 9)))
N = [(x, y) for x in range(W) for y in range(H)]
arcs = [(a, (a[0] + dx, a[1] + dy)) for a in N for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= a[0] + dx < W and 0 <= a[1] + dy < H]
term = {v: k for k in M for v in M[k]}

def optimum(groupe, temps=600, workers=2):
    m = cp_model.CpModel(); X = {}
    for k in groupe:
        s, t = M[k]
        for a, b in arcs:
            if b == s or a == t or (a in term and term[a] != k) or (b in term and term[b] != k): continue
            X[k, a, b] = m.NewBoolVar("")
        for v in N:
            out = [X[k, a, b] for a, b in arcs if a == v and (k, a, b) in X]
            inn = [X[k, a, b] for a, b in arcs if b == v and (k, a, b) in X]
            m.Add(sum(out) - sum(inn) == (1 if v == s else -1 if v == t else 0)); m.Add(sum(inn) <= 1)
        d = abs(s[0] - t[0]) + abs(s[1] - t[1]); e = m.NewIntVar(0, W * H, "")
        m.Add(sum(x for (kk, a, b), x in X.items() if kk == k) == d + 2 * e)
    for v in N:
        m.Add(sum(X[k, a, b] for k in groupe for a, b in arcs if b == v and (k, a, b) in X) <= 1)
    m.Minimize(sum(X.values()))
    sv = cp_model.CpSolver(); sv.parameters.num_workers = workers; sv.parameters.max_time_in_seconds = temps
    st = sv.Solve(m)
    return int(sv.BestObjectiveBound() + 0.5), st == cp_model.OPTIMAL

K = sorted(M)
def un(g): return g, optimum(g, temps=1800, workers=1)

if __name__ == "__main__":
    taille = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    from multiprocessing import Pool
    opt = {}
    with Pool(12) as pool:
        for g, r in pool.imap_unordered(un, list(itertools.combinations(K, taille))):
            opt[g] = r; print(" ", "".join(g), r, flush=True)
    import json; json.dump({"".join(g): r for g, r in opt.items()}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bornes_%d.json" % taille), "w"))
    # meilleure partition (groupes de la taille donnée, plus des singletons à leur distance au plus court)
    def seul(k): s, t = M[k]; return abs(s[0] - t[0]) + abs(s[1] - t[1])
    best = (0, None)
    def parts(reste, acc, val):
        global best
        if not reste:
            if val > best[0]: best = (val, acc)
            return
        k = reste[0]
        parts(reste[1:], acc + [(k,)], val + seul(k))
        for g in opt:
            if g[0] == k and all(x in reste for x in g):
                parts([x for x in reste if x not in g], acc + [g], val + opt[g][0])
    parts(K, [], 0)
    print("meilleure borne par partition en groupes de %d :" % taille, best)
