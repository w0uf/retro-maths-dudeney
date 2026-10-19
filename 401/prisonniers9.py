# -*- coding: utf-8 -*-
"""n° 401 EIGHT JOLLY GAOL BIRDS — Dudeney, 1917.

Neuf cellules en carre de trois sur trois, huit prisonniers numerotes et une
cellule vide ; on ne peut passer que dans la cellule libre voisine.  Il faut
que les numeros forment un carre magique, en un minimum de deplacements.

Depart :   1 2 3 / 4 . 5 / 6 7 8

Dudeney : huit carres magiques (une seule figure a symetrie pres), dont
quatre seulement sont atteignables, dont deux en dix-neuf coups, et dans
l'un des deux le prisonnier n° 3 ne bouge jamais.
"""
from collections import deque
from itertools import permutations

DEPART = (1,2,3,4,0,5,6,7,8)
VOIS = {0:(1,3), 1:(0,2,4), 2:(1,5), 3:(0,4,6), 4:(1,3,5,7),
        5:(2,4,8), 6:(3,7), 7:(4,6,8), 8:(5,7)}
LIGNES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def magique(g):
    s = {sum(g[i] for i in L) for L in LIGNES}
    return len(s) == 1

cibles = set()
for p in permutations(range(9)):
    if magique(p): cibles.add(p)
print("carres magiques possibles (la cellule vide comptant pour zero) :", len(cibles))
if cibles:
    c = sorted(cibles)[0]
    s = sum(c[i] for i in LIGNES[0])
    print("  somme commune :", s)
    for r in range(3): print("   ", " ".join(str(x) if x else "." for x in c[3*r:3*r+3]))
print("  Dudeney annonce huit facons ->", len(cibles) == 8)

# --- parcours en largeur depuis le depart ------------------------------
dist = {DEPART: 0}; pere = {DEPART: []}
f = deque([DEPART])
while f:
    e = f.popleft()
    v = e.index(0)
    for w in VOIS[v]:
        g = list(e); g[v], g[w] = g[w], g[v]; g = tuple(g)
        if g not in dist:
            dist[g] = dist[e]+1; pere[g] = [(e, e[w])]; f.append(g)
        elif dist[g] == dist[e]+1: pere[g].append((e, e[w]))
print("\npositions atteignables :", len(dist), "sur", 362880)

att = {c: dist[c] for c in cibles if c in dist}
print("carres magiques atteignables :", len(att), " (Dudeney : quatre ->", len(att) == 4, ")")
print("  leurs distances :", sorted(att.values()))
mini = min(att.values())
print("  minimum de deplacements :", mini, " (Dudeney : dix-neuf ->", mini == 19, ")")
opt = [c for c, d in att.items() if d == mini]
print("  carres atteints en ce minimum :", len(opt), " (Dudeney : deux ->", len(opt) == 2, ")")

def chemins(e):
    if not pere[e]: return [[]]
    out = []
    for p, qui in pere[e]:
        for ch in chemins(p): out.append(ch + [qui])
    return out

print("\n=== Qui peut rester dans sa cellule ? ===")
for c in opt:
    sols = chemins(c)
    jamais = set(range(1, 9))
    for ch in sols: jamais &= (set(range(1, 9)) - set(ch))
    bougent_tous = [ch for ch in sols if len(set(ch)) == 8]
    print("  carre :", " / ".join(" ".join(str(x) if x else "." for x in c[3*r:3*r+3]) for r in range(3)))
    print("     %d suites optimales | prisonniers qui ne bougent dans AUCUNE : %s"
          % (len(sols), sorted(jamais) if jamais else "aucun"))
    par = {}
    for ch in sols:
        immobiles = tuple(sorted(set(range(1, 9)) - set(ch)))
        par.setdefault(immobiles, 0)
        par[immobiles] += 1
    print("     immobiles possibles :", {k: v for k, v in sorted(par.items())})

print("\n=== Ses deux suites imprimees ===")
S1 = [5,3,2,5,7,6,4,1,5,7,6,4,1,6,4,8,3,2,7]
S2 = [4,1,2,4,1,6,7,1,5,8,1,5,6,7,5,6,4,2,7]
def joue(suite):
    e = DEPART
    for x in suite:
        v = e.index(0)
        cible = [w for w in VOIS[v] if e[w] == x]
        if not cible: return None
        w = cible[0]
        g = list(e); g[v], g[w] = g[w], g[v]; e = tuple(g)
    return e
for nom, S in (("premiere", S1), ("seconde", S2)):
    fin = joue(S)
    print("  sa %s suite : %d coups, jouable : %s, magique : %s, immobiles : %s"
          % (nom, len(S), fin is not None, magique(fin) if fin else False,
             sorted(set(range(1,9)) - set(S))))
    if fin:
        for r in range(3): print("     ", " ".join(str(x) if x else "." for x in fin[3*r:3*r+3]))
mesu = []
for c in opt: mesu += chemins(c)
print("\n  mes deux suites optimales (les seules) :")
for ch in mesu: print("    ", ch)
print("  identiques aux siennes :", sorted(map(tuple, mesu)) == sorted([tuple(S1), tuple(S2)]))

# --- temoins -----------------------------------------------------------
print("\n=== Temoins ===")
t1 = S1[:-1]
t2 = S1[:4] + [S1[5], S1[4]] + S1[6:]
for nom, t in (("sa premiere suite sans le dernier coup", t1), ("deux coups intervertis", t2)):
    fin = joue(t)
    print("  %-40s -> %s" % (nom, "coup illegal" if fin is None else
          ("ACCEPTEE" if magique(fin) else "pas de carre magique")))
    assert fin is None or not magique(fin)
print("  le depart n'est pas magique :", not magique(DEPART))
assert not magique(DEPART) and len(cibles) == 8 and len(att) == 4 and mini == 19 and len(opt) == 2
assert sorted(att.values()) == [19, 19, 23, 25] and sorted(map(tuple, mesu)) == sorted([tuple(S1), tuple(S2)])
