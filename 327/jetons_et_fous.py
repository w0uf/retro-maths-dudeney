#!/usr/bin/env python3
"""Rétro Math's — n° 326 A NEW COUNTER PUZZLE et n° 327 A NEW BISHOP'S PUZZLE (Dudeney, 1917).
Deux recherches en largeur, et le rejeu de ses deux suites.
    python3 jetons_et_fous.py   (environ 1 s)"""
from collections import deque
from itertools import combinations

print("=== 326 : deux jetons blancs (1, 2), deux rouges (9, 10), jamais un rouge et un blanc sur une même droite")
AR = [(4,2),(4,6),(8,6),(8,10),(2,3),(6,3),(6,7),(10,7),(3,1),(3,5),(7,5),(7,9)]
DR = [{1,3,6,8},{5,7,10},{2,4},{4,6,7,9},{2,3,5},{8,10}]
ORD = [[1,3,6,8],[5,7,10],[2,4],[4,6,7,9],[2,3,5],[8,10]]      # les droites, points dans l'ordre
def glissades(a, occ):
    out = set()
    for d in ORD:
        if a in d:
            i = d.index(a)
            for rng in (range(i+1, len(d)), range(i-1, -1, -1)):
                for j in rng:
                    if d[j] in occ: break
                    out.add(d[j])
    return out
def ok(W, R): return not any(d & W and d & R for d in DR)
def bfs326(alterne=False):
    s0 = (frozenset({1,2}), frozenset({9,10}), 0); but = (frozenset({9,10}), frozenset({1,2}))
    dist = {s0: 0}; nb = {s0: 1}; q = deque([s0]); fin = None
    while q:
        W, R, t = s = q.popleft()
        if (W, R) == but: fin = dist[s] if fin is None else fin
        if fin is not None and dist[s] >= fin: continue
        for camp in ((0, 1) if not alterne else (t,)):
            X = W if camp == 0 else R
            for a in X:
                for b in glissades(a, W | R):
                    X2 = X - {a} | {b}; W2, R2 = (X2, R) if camp == 0 else (W, X2)
                    if not ok(W2, R2): continue
                    v = (W2, R2, 1 - t if alterne else 0)
                    if v not in dist: dist[v] = dist[s] + 1; nb[v] = 0; q.append(v)
                    if dist[v] == dist[s] + 1: nb[v] += nb[s]
    fins = [s for s in dist if (s[0], s[1]) == but]
    return min(dist[s] for s in fins), sum(nb[s] for s in fins if dist[s] == min(dist[x] for x in fins)), len(dist)
R326 = bfs326()
print("minimum, nombre de solutions minimales, positions atteintes :", R326)
seq = "2-3 9-4 10-7 3-8 4-2 7-5 8-6 5-10 6-9 2-5 1-6 6-4 5-3 10-8 4-7 3-2 8-1 7-10".split()
W, R = {1,2}, {9,10}; bon = True
for m in seq:
    a, b = map(int, m.split('-')); X = W if a in W else R
    bon &= a in X and b in glissades(a, W | R); X.remove(a); X.add(b); bon &= ok(W, R)
print("sa suite :", len(seq), "coups, valide :", bon, "| arrivée :", sorted(W), sorted(R))
def rejoue326(seq):
    W, R = {1,2}, {9,10}
    for m in seq:
        a, b = map(int, m.split('-')); X = W if a in W else R
        if a not in X or b not in glissades(a, W | R): return False
        X.remove(a); X.add(b)
        if not ok(W, R): return False
    return (W, R) == ({9,10}, {1,2})
assert R326[:2] == (18, 256) and bon and rejoue326(seq)
assert not rejoue326(seq[1:2] + seq[:1] + seq[2:])     # temoin : ses deux premiers coups intervertis
assert not rejoue326(seq[:-1])                          # temoin : le dernier coup oublie

print("=== 327 : quatre fous noirs (1-4), quatre blancs (17-20), damier 4×5, coups alternés, les Blancs commencent")
LARG, HAUT = 4, 5
def lc(n): return divmod(n - 1, LARG)
def num(l, c): return l * LARG + c + 1
def rayons(n):
    l, c = lc(n); out = []
    for dl, dc in ((-1,-1),(-1,1),(1,-1),(1,1)):
        r = []; x, y = l + dl, c + dc
        while 0 <= x < HAUT and 0 <= y < LARG: r.append(num(x, y)); x += dl; y += dc
        out.append(r)
    return out
RAY = {n: rayons(n) for n in range(1, 21)}
def attaques_croisees(W, B):
    occ = W | B
    for X, Y in ((W, B), (B, W)):
        for a in X:
            for r in RAY[a]:
                for t in r:
                    if t in occ:
                        if t in Y: return True
                        break
    return False
def bfs327(alterne=True):
    s0 = (frozenset({17,18,19,20}), frozenset({1,2,3,4}), 0); but = (frozenset({1,2,3,4}), frozenset({17,18,19,20}))
    dist = {s0: 0}; nb = {s0: 1}; q = deque([s0]); fin = None; pred = {s0: None}
    while q:
        W, B, t = s = q.popleft()
        if (W, B) == but and fin is None: fin = dist[s]; arrivee = s
        if fin is not None and dist[s] >= fin: continue
        occ = W | B
        for camp in ((t,) if alterne else (0, 1)):
            X = W if camp == 0 else B
            for a in X:
                for r in RAY[a]:
                    for b in r:
                        if b in occ: break
                        X2 = X - {a} | {b}; W2, B2 = (X2, B) if camp == 0 else (W, X2)
                        if attaques_croisees(W2, B2): continue
                        v = (W2, B2, 1 - t if alterne else 0)
                        if v not in dist: dist[v] = dist[s] + 1; nb[v] = 0; q.append(v); pred[v] = (s, a, b)
                        if dist[v] == dist[s] + 1: nb[v] += nb[s]
    fins = [s for s in dist if (s[0], s[1]) == but]
    if not fins: return None
    m = min(dist[s] for s in fins); ch = []; s = min(fins, key=lambda x: dist[x])
    while pred[s]: s, a, b = pred[s]; ch.append("%d-%d" % (a, b))
    return m, sum(nb[s] for s in fins if dist[s] == m), len(dist), ' '.join(reversed(ch))
r = R327 = bfs327(True); print("alternés : minimum", r[0], "coups ; solutions minimales", r[1], "; positions", r[2]); print("   une solution :", r[3])
r = L327 = bfs327(False); print("ordre libre : minimum", r[0], "coups ; solutions minimales", r[1], "; positions", r[2])
blanc = "18-15 17-8 19-14 15-5 8-3 14-9 5-10 9-19 10-4 20-10 3-9 10-13 19-16 16-1 9-6 13-7 6-3 7-2".split()
noir  = "3-6 4-13 2-7 6-16 13-18 7-12 16-11 12-2 11-17 1-11 18-12 11-8 2-5 5-20 12-15 8-14 15-18 14-19".split()
W, B = {17,18,19,20}, {1,2,3,4}; bon = True; n = 0
for mb, mn in zip(blanc, noir):
    for X, m in ((W, mb), (B, mn)):
        a, b = map(int, m.split('-')); occ = W | B
        legal = a in X and any(b in r and not any(t in occ for t in r[:r.index(b) + 1]) for r in RAY[a])
        X.remove(a); X.add(b); n += 1
        if not legal or attaques_croisees(W, B): bon = False; print("   coup fautif n°", n, m)
print("sa suite :", n, "coups, valide :", bon, "| arrivée :", sorted(W), sorted(B))
assert bon and n == 36 and (W, B) == ({1,2,3,4}, {17,18,19,20})
assert R327[:2] == (36, 307570) and L327[0] == 36
def rejoue327(blanc, noir):
    W, B = {17,18,19,20}, {1,2,3,4}
    for mb, mn in zip(blanc, noir):
        for X, m in ((W, mb), (B, mn)):
            a, b = map(int, m.split('-')); occ = W | B
            if not (a in X and any(b in r and not any(t in occ for t in r[:r.index(b) + 1]) for r in RAY[a])): return False
            X.remove(a); X.add(b)
            if attaques_croisees(W, B): return False
    return (W, B) == ({1,2,3,4}, {17,18,19,20})
assert rejoue327(blanc, noir)
assert not rejoue327(["17-15"] + blanc[1:], noir)            # temoin : 17-15 n'est pas un coup de fou
assert not rejoue327(blanc[1:2] + blanc[:1] + blanc[2:], noir)  # temoin : ses deux premiers coups blancs intervertis
print("controles : tout est conforme (temoins refuses)")
