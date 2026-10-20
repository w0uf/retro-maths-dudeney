#!/usr/bin/env python3
"""Rétro Math's — n° 338 THE BOARD IN COMPARTMENTS (Dudeney, 1917). Échiquier coupé en quatre
compartiments (3×4, 5×4, 3×4, 5×4) ; tour fermé du cavalier qui épuise chaque compartiment avant d'en changer.
Cases : (rangée depuis le haut, colonne).
    python3 compartiments.py   (environ 1 min, pour les tours fermés de 3×10 et 3×12)"""
RES = {}
from collections import Counter, defaultdict
from itertools import permutations
SAUTS = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
def voisins(cases):
    S = set(cases)
    return {x: [(x[0]+a, x[1]+b) for a, b in SAUTS if (x[0]+a, x[1]+b) in S] for x in S}
def chemins(cases):
    """tous les chemins hamiltoniens orientés : Counter{(début, fin): nombre}"""
    V = voisins(cases); n = len(V); res = Counter()
    def rec(x, vus, d):
        if len(vus) == n: res[(d, x)] += 1; return
        for y in V[x]:
            if y not in vus: vus.add(y); rec(y, vus, d); vus.discard(y)
    for d in V: rec(d, {d}, d)
    return res
def cycles(h, l):
    cases = [(i, j) for i in range(h) for j in range(l)]; V = voisins(cases); n = h*l; nb = 0
    def rec(x, vus):
        nonlocal nb
        if len(vus) == n: nb += (0, 0) in V[x]; return
        for y in V[x]:
            if y not in vus: vus.add(y); rec(y, vus); vus.discard(y)
    rec((0, 0), {(0, 0)})
    return nb // 2            # chaque tour fermé est parcouru dans les deux sens
rect = lambda l0, c0, h, l: [(l0+i, c0+j) for i in range(h) for j in range(l)]

print("=== les affirmations générales de l'énoncé")
for h, l in ((3,4),(4,4),(3,3),(2,5),(2,6),(3,5),(4,5)):
    r = chemins(rect(0, 0, h, l)); RES[("ch", h, l)] = sum(r.values()); print("damier %d×%d : %d chemins complets orientés" % (h, l, sum(r.values())))
for h, l in ((5,6),(3,10),(3,8),(4,6),(4,7),(3,12)):
    RES[(h, l)] = cycles(h, l); print("damier %d×%d (%d cases) : %d tours fermés" % (h, l, h*l, RES[(h, l)]), flush=True)

print("=== les quatre compartiments")
COMP = {'HG': rect(0,0,4,3), 'HD': rect(0,3,4,5), 'BG': rect(4,0,4,3), 'BD': rect(4,3,4,5)}
CH = {k: chemins(v) for k, v in COMP.items()}
for k in COMP:
    ext = Counter(); 
    for (d, f), n in CH[k].items(): ext[d] += n
    print(k, ": chemins orientés", sum(CH[k].values()), "| cases de départ possibles :", sorted(ext))
    print("     couples (début, fin) distincts :", len(CH[k]))
def saut(a, b): return (abs(a[0]-b[0]), abs(a[1]-b[1])) in ((1,2),(2,1))
tot = 0; ext_utilisees = defaultdict(Counter); par_ordre = Counter()
for ordre in permutations(['HD', 'BG', 'BD']):                # on part de HG : cycles orientés
    o = ('HG',) + ordre
    # produit sur les extrémités, par programmation dynamique le long du cycle
    for (d0, f0), n0 in CH['HG'].items():
        etat = {f0: n0}
        for k in o[1:]:
            nv = Counter()
            for f, n in etat.items():
                for (d, g), m in CH[k].items():
                    if saut(f, d): nv[g] += n * m
            etat = nv
        s = sum(n for f, n in etat.items() if saut(f, d0))
        tot += s; par_ordre[o] += s
print("tours fermés orientés qui épuisent chaque compartiment :", tot, "→ tours non orientés :", tot // 2)
for o, n in par_ordre.items(): print("   ordre", '→'.join(o), ":", n)
# les cases d'entrée et de sortie réellement utilisées
usage = Counter(); paires = Counter()
def explore(o):
    for (d0, f0), n0 in CH[o[0]].items():
        def rec(i, f, mult, ext):
            if i == 4:
                if saut(f, d0):
                    for e in ext: usage[e] += mult
                    paires[tuple(sorted(tuple(sorted(p)) for p in zip(ext[::2], ext[1::2])))] += mult
                return
            for (d, g), m in CH[o[i]].items():
                if saut(f, d): rec(i+1, g, mult*m, ext + [d, g])
        rec(1, f0, n0, [d0, f0])
for ordre in permutations(['HD', 'BG', 'BD']): explore(('HG',) + ordre)
print("cases servant d'entrée ou de sortie (nombre de tours orientés) :")
for x in sorted(usage): print("   ", x, usage[x])
print("jeux d'extrémités distincts :", len(paires))
for p, n in paires.items(): print("   ", p, n)

# --- ce que dit l'article
assert RES[("ch", 3, 4)] == 16 and RES[("ch", 4, 5)] == 164
assert all(RES[("ch", h, l)] == 0 for h, l in ((4,4),(3,3),(2,5),(2,6),(3,5)))
assert RES[(5, 6)] == 8 and RES[(3, 10)] == 16 and RES[(3, 12)] == 176 and RES[(3, 8)] == RES[(4, 6)] == RES[(4, 7)] == 0
assert tot // 2 == 36 and len(paires) == 4 and all(n == 18 for n in paires.values())
assert all(usage[x] == 72 for x in ((3,1),(3,3),(4,1),(4,3)))          # ses quatre cases etoilees, dans tous les tours
assert par_ordre[('HG','BG','HD','BD')] == par_ordre[('HG','BD','HD','BG')] == 36 and sum(par_ordre.values()) == 72
# temoins : deux cases voisines ne sont pas un saut de cavalier ; un saut de cavalier l'est
assert not saut((3, 0), (3, 1)) and saut((3, 0), (4, 2))
print("controles : tout est conforme (temoins refuses)")
