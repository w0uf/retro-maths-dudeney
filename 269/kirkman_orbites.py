#!/usr/bin/env python3
"""Le nombre de systemes de Kirkman d'ordre 15 ETIQUETES — calcul exact.

Idee : compter deux fois les couples (systeme, journee) donne
        7 N = 1 401 400 c          ->  N = 200 200 c
ou c = nombre de systemes contenant une journee fixee P1.

Puis, en comptant les couples (systeme contenant P1, seconde journee) :
        6 c = somme sur Q des n_Q
ou Q parcourt les 132 192 secondes journees possibles et n_Q est le nombre de
systemes contenant P1 et Q. Or n_Q ne depend que de l'ORBITE de Q sous le
stabilisateur de P1 (groupe d'ordre 3!^5 x 5! = 933 120). Il suffit donc de
traiter quelques representants.
"""
import sys, time
from itertools import combinations

N = 15
IDX = {}; k = 0
for a in range(N):
    for b in range(a+1, N): IDX[(a,b)] = k; k += 1
def pmask(t):
    return (1<<IDX[(t[0],t[1])]) | (1<<IDX[(t[0],t[2])]) | (1<<IDX[(t[1],t[2])])
TR = [(t, (1<<t[0])|(1<<t[1])|(1<<t[2]), pmask(t))
      for t in combinations(range(N), 3)]
PP = [[] for _ in range(N)]
for t, bm, pm in TR:
    for p in t: PP[p].append((t, bm, pm))

def journees(used):
    res = []
    def rec(rest, cour, u):
        if not rest: res.append(tuple(cour)); return
        a = (rest & -rest).bit_length() - 1
        for t, bm, pm in PP[a]:
            if bm & rest != bm or pm & u: continue
            rec(rest ^ bm, cour + [t], u | pm)
    rec((1<<N)-1, [], used)
    return res

def masque(c):
    u = 0
    for t in c: u |= pmask(t)
    return u

P1 = ((0,1,2),(3,4,5),(6,7,8),(9,10,11),(12,13,14))
U1 = masque(P1)

t0 = time.time()
Q = journees(U1)
print("secondes journees possibles : %d   (%.1f s)" % (len(Q), time.time()-t0), flush=True)

# ── orbites sous le stabilisateur de P1 ───────────────────────────────
def applique(perm, c):
    return tuple(sorted(tuple(sorted(perm[x] for x in t)) for t in c))
gens = []
# permutations a l'interieur d'un groupe
for g in range(5):
    a, b, cc = 3*g, 3*g+1, 3*g+2
    p = list(range(N)); p[a], p[b] = p[b], p[a]; gens.append(p)
    p = list(range(N)); p[a], p[b], p[cc] = p[b], p[cc], p[a]; gens.append(p)
# permutations des groupes
p = list(range(N))
for i in range(3): p[i], p[3+i] = p[3+i], p[i]
gens.append(p)
p = [0]*N
for g in range(5):
    for i in range(3): p[3*g+i] = 3*((g+1) % 5) + i
gens.append(p)

pos = {c: i for i, c in enumerate(Q)}
parent = list(range(len(Q)))
def trouve(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def unir(x, y):
    x, y = trouve(x), trouve(y)
    if x != y: parent[x] = y
t0 = time.time()
for i, c in enumerate(Q):
    for g in gens:
        j = pos.get(applique(g, c))
        if j is not None: unir(i, j)
orbites = {}
for i in range(len(Q)): orbites.setdefault(trouve(i), []).append(i)
print("orbites de secondes journees : %d   (%.1f s)"
      % (len(orbites), time.time()-t0), flush=True)
for r, o in orbites.items():
    print("   orbite de taille %d" % len(o))

# ── pour chaque representant, le nombre de systemes ───────────────────
def complete(used, mini, reste):
    """nombre de facons de completer avec « reste » journees croissantes"""
    if reste == 0: return 1
    n = 0
    for c in journees(used):
        if c <= mini: continue
        n += complete(used | masque(c), c, reste-1)
    return n

total = 0
print()
for r, o in sorted(orbites.items(), key=lambda kv: -len(kv[1])):
    rep = Q[o[0]]
    t0 = time.time()
    n = complete(U1 | masque(rep), (), 5)
    print("  orbite de %6d : n_Q = %d   (%.1f s)" % (len(o), n, time.time()-t0),
          flush=True)
    total += len(o) * n
c = total // 6
print()
print("6c = %d   ->   c = %d" % (total, c))
print("N = 200 200 x c = %d" % (200200*c))
print("Dudeney annonce   15 567 552 000")
print("egaux :", 200200*c == 15567552000)
