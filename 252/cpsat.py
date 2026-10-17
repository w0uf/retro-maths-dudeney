#!/usr/bin/env python3
"""N° 252 A PUZZLE FOR MOTORISTS : longueur totale minimale des huit trajets sans carrefour commun.
Grille de 18 × 11 carrefours relevée sur la figure du livre ; solveur CP-SAT (OR-Tools : pip install ortools).
    python3 -u cpsat.py [borne] [secondes]     part du meilleur réseau connu (reseau_157.json) et le réécrit s'il trouve mieux"""
import sys
from ortools.sat.python import cp_model

W, H = 18, 11
M = dict(A=((12, 0), (12, 9)), B=((2, 2), (2, 10)), C=((7, 2), (17, 2)), D=((15, 2), (15, 10)), E=((8, 3), (17, 3)), F=((0, 7), (14, 7)), G=((0, 5), (12, 5)), H=((5, 0), (5, 9)))
N = [(x, y) for x in range(W) for y in range(H)]
arcs = [(a, (a[0] + dx, a[1] + dy)) for a in N for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= a[0] + dx < W and 0 <= a[1] + dy < H]
term = {v: k for k in M for v in M[k]}
borne = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] else None   # « longueur <= borne » pour un test de faisabilité

m = cp_model.CpModel()
X = {}
for k in M:
    s, t = M[k]
    for a, b in arcs:
        if b == s or a == t or (a in term and term[a] != k) or (b in term and term[b] != k): continue
        X[k, a, b] = m.NewBoolVar("")
    for v in N:
        out = [X[k, a, b] for a, b in arcs if a == v and (k, a, b) in X]
        inn = [X[k, a, b] for a, b in arcs if b == v and (k, a, b) in X]
        m.Add(sum(out) - sum(inn) == (1 if v == s else -1 if v == t else 0))
        m.Add(sum(inn) <= 1)
for v in N:   # un carrefour sert à une voiture au plus
    m.Add(sum(X[k, a, b] for k in M for a, b in arcs if b == v and (k, a, b) in X) <= 1)
LK = {}
for k in M:   # parité : sur une grille, un trajet a la parité de sa distance au plus court
    s, t2 = M[k]; d = abs(s[0] - t2[0]) + abs(s[1] - t2[1])
    e = m.NewIntVar(0, W * H, ""); LK[k] = sum(x for (kk, a, b), x in X.items() if kk == k)
    m.Add(LK[k] == d + 2 * e)
L = sum(X.values())
m.Add(L >= sum(abs(s[0] - t[0]) + abs(s[1] - t[1]) for s, t in M.values()))
if borne: m.Add(L <= borne)
m.Minimize(L)
import json, os
FICHIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reseau_157.json")
if os.path.exists(FICHIER):   # point de départ : le meilleur réseau déjà trouvé
    for k, p in json.load(open(FICHIER)).items():
        arcs_p = {(tuple(a), tuple(b)) for a, b in zip(p, p[1:])}
        for (kk, a, b), x in X.items():
            if kk == k: m.AddHint(x, (a, b) in arcs_p)
sv = cp_model.CpSolver(); sv.parameters.num_workers = 12; sv.parameters.max_time_in_seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1800
sv.parameters.log_search_progress = False
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self): print("  solution %d (borne inférieure %d) à %.0f s" % (self.ObjectiveValue(), self.BestObjectiveBound(), self.WallTime()), flush=True)
st = sv.Solve(m, CB())
print("statut", sv.StatusName(st), "; longueur", sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, "; borne inférieure", sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    vus = {}; meilleur = {}
    for k in sorted(M):
        nxt = {a: b for (kk, a, b), x in X.items() if kk == k and sv.Value(x)}
        p = [M[k][0]]
        while p[-1] != M[k][1]: p.append(nxt[p[-1]])
        for v in p: assert v not in vus; vus[v] = k
        meilleur[k] = p
        cycles = len(nxt) - (len(p) - 1)
        print("  ", k, len(p) - 1, "(plus court %d)" % (abs(M[k][0][0] - M[k][1][0]) + abs(M[k][0][1] - M[k][1][1])), "arcs hors trajet", cycles, p)
    json.dump(meilleur, open(FICHIER, "w"))
