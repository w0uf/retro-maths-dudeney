#!/usr/bin/env python3
"""Controle independant du nombre N de systemes de Kirkman d'ordre 15 etiquetes.

Premiere route (kirkman_orbites.py) : double comptage et orbites -> N.
Seconde route, ici : on engendre des systemes au hasard, on les repartit en
classes d'isomorphisme, on calcule |Aut| de chacune par PROPAGATION, et
        N = somme des 15!/|Aut|.
Si les deux routes donnent le meme nombre, il n'y a plus de doute.
"""
import random, math, time
from itertools import combinations

N = 15
def journees(used):
    res = []
    def rec(rest, cour, u):
        if not rest: res.append(tuple(cour)); return
        a = (rest & -rest).bit_length() - 1
        for t, bm, pm in PP[a]:
            if bm & rest != bm or pm & u: continue
            rec(rest ^ bm, cour + [t], u | pm)
    rec((1 << N) - 1, [], used)
    return res
IDX = {}; k = 0
for a in range(N):
    for b in range(a+1, N): IDX[(a,b)] = k; k += 1
def pm_(t): return (1<<IDX[(t[0],t[1])])|(1<<IDX[(t[0],t[2])])|(1<<IDX[(t[1],t[2])])
PP = [[] for _ in range(N)]
for t in combinations(range(N), 3):
    bm = (1<<t[0])|(1<<t[1])|(1<<t[2])
    for p in t: PP[p].append((t, bm, pm_(t)))

def systeme(rng):
    def rec(jour, used, jours):
        if jour == 7: return jours
        js = journees(used); rng.shuffle(js)
        for c in js:
            u = used
            for t in c: u |= pm_(t)
            r = rec(jour+1, u, jours + [c])
            if r: return r
        return None
    return rec(0, 0, [])

def tiers(S):
    th = [[None]*N for _ in range(N)]
    for j in S:
        for a, b, c in j:
            th[a][b]=th[b][a]=c; th[a][c]=th[c][a]=b; th[b][c]=th[c][b]=a
    return th

def morphismes(S, T, un_seul=False):
    """toutes les bijections envoyant la resolution S sur la resolution T"""
    thS, thT = tiers(S), tiers(T)
    CT = {frozenset(j) for j in T}
    f = [-1]*N; inv = [-1]*N; sols = []
    def propage(pile, faits):
        while pile:
            a = pile.pop()
            for b in range(N):
                if b == a or f[b] < 0: continue
                c = thS[a][b]; img = thT[f[a]][f[b]]
                if f[c] >= 0:
                    if f[c] != img: return False
                else:
                    if inv[img] >= 0: return False
                    f[c] = img; inv[img] = c; faits.append(c); pile.append(c)
        return True
    def rec():
        p = next((x for x in range(N) if f[x] < 0), None)
        if p is None:
            if all(frozenset(tuple(sorted(f[x] for x in t)) for t in j) in CT
                   for j in S):
                sols.append(tuple(f))
                return un_seul
            return False
        for q in range(N):
            if inv[q] >= 0: continue
            f[p] = q; inv[q] = p; faits = [p]
            if propage([p], faits):
                if rec(): return True
            for x in faits: inv[f[x]] = -1; f[x] = -1
        return False
    rec()
    return sols

rng = random.Random(2026)
familles = []
t0 = time.time()
for essai in range(60):
    S = systeme(rng)
    if S is None: continue
    if not any(morphismes(S, R, un_seul=True) for R in familles):
        familles.append(S)
        print("  classe %d (tirage %d, %.0f s)" % (len(familles), essai+1,
              time.time()-t0), flush=True)
print("classes d'isomorphisme trouvees : %d   (%.0f s)"
      % (len(familles), time.time()-t0))

F = math.factorial(15)
tot = 0
print()
for i, S in enumerate(familles, 1):
    a = len(morphismes(S, S))
    tot += F // a
    print("  classe %d : |Aut| = %-5d -> %d systemes etiquetes" % (i, a, F//a))
print()
print("  N (somme) = %d" % tot)
print("  N (orbites) = 404756352000")
print("  les deux routes coincident :", tot == 404756352000)
