# -*- coding: utf-8 -*-
"""« et la solution generale » : pour quels nombres de couples la grille
existe-t-elle ?  n couples, n/2 courts, n-1 jours (n est donc pair)."""
import sys, time, json
sys.setrecursionlimit(20000)

def couplages(el):
    if not el: yield (); return
    a = el[0]
    for i in range(1, len(el)):
        for r in couplages(el[1:i] + el[i+1:]): yield ((a, el[i]),) + r

def grille(N, budget=40_000_000):
    APP = list(couplages(tuple(range(N))))
    JOURS = N - 1
    hh, ff, hf, part, sol = set(), set(), set(), set(), []
    n = [0]; stop = [False]
    def cherche(d):
        if stop[0]: return False
        if d > JOURS: return True
        for P in (APP if d > 1 else [APP[0]]):
            if any(p in hh for p in P): continue
            if remplir(d, P, 0, {}, [], [], [], []): return True
            if stop[0]: return False
        return False
    def remplir(d, P, k, prises, ah, af, ahf, apart):
        n[0] += 1
        if n[0] > budget: stop[0] = True; return False
        if k == len(P):
            hh.update(ah); ff.update(af); hf.update(ahf); part.update(apart)
            sol.append((P, dict(prises)))
            if cherche(d+1): return True
            sol.pop()
            for x in ah: hh.discard(x)
            for x in af: ff.discard(x)
            for x in ahf: hf.discard(x)
            for x in apart: part.discard(x)
            return False
        i, j = P[k]
        for wi in range(N):
            if wi == i or wi in prises or (i, wi) in part or (i, wi) in apart: continue
            for wj in range(N):
                if wj == j or wj == wi or wj in prises: continue
                if (j, wj) in part or (j, wj) in apart: continue
                a = (i, j); b = (wi, wj) if wi < wj else (wj, wi)
                c1 = (i, wj); c2 = (j, wi)
                if c1[0] == c1[1] or c2[0] == c2[1]: continue
                if a in hh or a in ah or b in ff or b in af: continue
                if c1 in hf or c1 in ahf or c2 in hf or c2 in ahf: continue
                pr = dict(prises); pr[wi] = i; pr[wj] = j
                if remplir(d, P, k+1, pr, ah+[a], af+[b], ahf+[c1, c2],
                           apart+[(i, wi), (j, wj)]): return True
                if stop[0]: return False
        return False
    t0 = time.time()
    ok = cherche(1)
    return ok, stop[0], n[0], time.time()-t0, list(sol)

for N in (4, 6, 8, 10):
    ok, arrete, noeuds, dt, sol = grille(N)
    etat = "TROUVEE" if ok else ("budget epuise" if arrete else "IMPOSSIBLE")
    print("%2d couples (%d courts, %d jours) : %-14s  %10d noeuds  %6.1f s"
          % (N, N//2, N-1, etat, noeuds, dt), flush=True)
