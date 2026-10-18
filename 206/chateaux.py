#!/usr/bin/env python3
"""n° 206 THE KING AND THE CASTLES — Dudeney, Amusements in Mathematics (1917).

Dix chateaux relies par des murailles formant cinq droites de quatre chateaux.
Le roi veut le plus grand nombre possible de chateaux inaccessibles du dehors,
c'est-a-dire qu'on ne puisse atteindre sans franchir une muraille.

Dudeney : « deux chateaux (le plus grand nombre possible) » et « la disposition
donnee est la SEULE qui procure cela ».

Comme au n° 210, la figure est un arrangement de cinq droites en position
generale : leurs C(5,2)=10 intersections sont les chateaux, et chaque droite en
porte quatre.  Les murailles sont les 15 segments bornes (trois par droite).
Un chateau est « du dehors » s'il touche la face non bornee du dessin.
"""
import random, math
from itertools import combinations, permutations

def inter(L1, L2):
    (a1,b1,c1), (a2,b2,c2) = L1, L2          # ax + by = c
    d = a1*b2 - a2*b1
    if abs(d) < 1e-9: return None
    return ((c1*b2 - c2*b1)/d, (a1*c2 - a2*c1)/d)

def arrangement(rng):
    """cinq droites en position generale"""
    while True:
        L = [(math.cos(t), math.sin(t), rng.uniform(-1, 1))
             for t in [rng.uniform(0, math.pi) for _ in range(5)]]
        P = {}
        ok = True
        for i, j in combinations(range(5), 2):
            p = inter(L[i], L[j])
            if p is None: ok = False; break
            P[(i, j)] = p
        if not ok: continue
        pts = list(P.values())
        if any(math.dist(p, q) < 1e-3 for p, q in combinations(pts, 2)): continue
        return L, P

def type_figure(L, P):
    """ordre des points le long de chaque droite, forme canonique"""
    ordres = []
    for i in range(5):
        dx, dy = -L[i][1], L[i][0]
        pl = [(P[tuple(sorted((i, j)))], j) for j in range(5) if j != i]
        pl.sort(key=lambda t: t[0][0]*dx + t[0][1]*dy)
        ordres.append(tuple(j for _, j in pl))
    best = None
    for p in permutations(range(5)):
        o = []
        for i in range(5):
            s = tuple(p[x] for x in ordres[i])
            o.append(min(s, s[::-1]))
        c = tuple(sorted(o))
        if best is None or c < best: best = c
    return best

def faces(L, P):
    """les 15 segments, puis les faces du dessin ; renvoie les sommets du dehors"""
    som = sorted(P.values())
    idx = {p: k for k, p in enumerate(som)}
    aretes = set()
    for i in range(5):
        dx, dy = -L[i][1], L[i][0]
        pl = sorted((P[tuple(sorted((i, j)))] for j in range(5) if j != i),
                    key=lambda p: p[0]*dx + p[1]*dy)
        for a, b in zip(pl, pl[1:]):
            aretes.add(frozenset((idx[a], idx[b])))
    assert len(aretes) == 15, len(aretes)

    voisins = {k: [] for k in range(10)}
    for e in aretes:
        u, v = tuple(e); voisins[u].append(v); voisins[v].append(u)
    ang = {}
    for u in voisins:
        voisins[u].sort(key=lambda v: math.atan2(som[v][1]-som[u][1], som[v][0]-som[u][0]))
        for k, v in enumerate(voisins[u]): ang[(u, v)] = k

    vus, F = set(), []
    for e in aretes:
        for u, v in (tuple(e), tuple(e)[::-1]):
            if (u, v) in vus: continue
            face, a, b = [], u, v
            while (a, b) not in vus:
                vus.add((a, b)); face.append(b)
                k = ang[(b, a)]
                c = voisins[b][(k - 1) % len(voisins[b])]   # suivant dans le sens horaire
                a, b = b, c
            F.append(face)
    aire = lambda f: sum(som[f[i]][0]*som[f[(i+1) % len(f)]][1]
                         - som[f[(i+1) % len(f)]][0]*som[f[i]][1] for i in range(len(f)))/2
    A = [aire(f) for f in F]
    dehors = F[min(range(len(F)), key=lambda i: A[i])]
    return len(F), set(dehors)

rng = random.Random(1917)
trouve = {}
for essai in range(120000):
    L, P = arrangement(rng)
    nf, dehors = faces(L, P)
    if nf != 7: continue
    t = type_figure(L, P)
    dedans = 10 - len(dehors)
    trouve.setdefault(t, set()).add(dedans)
    if len(trouve) == 6 and essai > 40000: break

print("types d'arrangement rencontres :", len(trouve), " (au n° 210 : six)")
print()
for k, (t, d) in enumerate(sorted(trouve.items(), key=lambda kv: (max(kv[1]), kv[0])), 1):
    print("  type %d : chateaux a l'abri = %s" % (k, sorted(d)))
best = max(max(d) for d in trouve.values())
combien = sum(1 for d in trouve.values() if max(d) == best)
print()
print("nombre maximal de chateaux a l'abri :", best, " (Dudeney : deux ->", best == 2, ")")
print("types qui l'atteignent :", combien, " (Dudeney : un seul ->", combien == 1, ")")

# --- lien avec le n° 210 : quel damier minimal porte la figure gagnante ? ---
DAMIERS = {
 ((0,1,2,3),(0,1,2,4),(0,1,3,4),(0,2,3,4),(1,2,3,4)): "7 x 7",
 ((0,1,2,3),(0,1,2,4),(0,1,3,4),(0,4,3,2),(1,4,3,2)): "8 x 8",
 ((0,1,2,3),(0,1,4,3),(1,0,2,4),(2,4,0,3),(2,4,1,3)): "8 x 8",
 ((0,1,2,3),(0,3,4,1),(1,0,2,4),(2,3,1,4),(2,4,0,3)): "9 x 7",
 ((0,1,2,3),(0,1,2,4),(0,3,4,1),(0,3,4,2),(2,1,3,4)): "10 x 10",
}
print("\n=== Recoupement avec le n° 210 (les six figures fondamentales) ===")
for t, d in sorted(trouve.items(), key=lambda kv: max(kv[1])):
    print("   a l'abri : %d   plus petit damier connu : %s"
          % (max(d), DAMIERS.get(t, "13 x 13 (la sixieme)")))
