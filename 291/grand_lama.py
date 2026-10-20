#!/usr/bin/env python3
"""Rétro Math's — n° 291 THE GRAND LAMA'S PROBLEM (Dudeney, 1917). Couper l'échiquier en quatre parts de même
forme, de seize cases, chacune contenant une des quatre gemmes (posées sur la grande diagonale : a8, b7, c6, d5).
Inventaire des découpes « en moulin » (parts déduites l'une de l'autre par quart de tour).
Reprend l'inventaire de quatre_cavaliers.py (n° 339), copié dans ce dossier.
    python3 grand_lama.py   (environ 1 s)"""
import os
import io, contextlib
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quatre_cavaliers.py')).read()
src = src.split("tr = lambda P")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
GEMMES = [(0,0),(1,1),(2,2),(3,3)]
def quart(P, g):
    """dans quelle part (0..3) tombe la case g, la part k étant P tournée k fois"""
    x = g
    for k in range(4):
        if x in P: return (4 - k) % 4
        x = rot(x)
bons = []
for P in parts:
    q = [quart(P, g) for g in GEMMES]
    if len(set(q)) == 4: bons.append(P)
print("découpes en moulin :", len(parts), "| celles qui donnent une gemme à chaque part :", len(bons))
tr = lambda P: frozenset((c, r) for r, c in P)
cl = {min(tuple(sorted(P)), tuple(sorted(tr(P)))) for P in bons}
print("à retournement près (miroir par la diagonale des gemmes) :", len(cl))
# la solution du livre : quatre bras de spirale. La part qui contient le coin (0,0) :
def affiche(P):
    for r in range(8): print("     ", ''.join('#' if (r, c) in P else '.' for c in range(8)))
spirale = frozenset([(0,c) for c in range(8)] + [(r,7) for r in range(1,7)] + [(6,6),(6,5)])   # essai : haut puis droite
print("une spirale simple (rangée du haut + colonne de droite…) est-elle une part valable ?", spirale in set(parts), "| donne une gemme par part :", spirale in set(bons))
# toutes les solutions, classées par « allure » : nombre de cases de bord
from collections import Counter
for P in sorted(bons, key=lambda P: sorted(P))[:0]: affiche(P)
# gemmes ailleurs : combien de découpes pour d'autres dispositions de 4 gemmes sur la diagonale ?
import itertools
diag = [(i, i) for i in range(8)]
res = {}
for G in itertools.combinations(diag, 4):
    n = sum(1 for P in parts if len({quart(P, g) for g in G}) == 4)
    res[G] = n
print("quatre gemmes sur la grande diagonale, toutes dispositions : nombre de découpes possibles")
for G, n in sorted(res.items(), key=lambda x: x[1]): print("   ", [g[0] + 1 for g in G], n)

# --- ce que dit l'article : une seule decoupe, la spirale du livre (part du coin a8, relevee sur sa gravure)
LIVRE = frozenset([(r, 0) for r in range(7)] + [(6, c) for c in range(1, 6)] + [(3, 5), (4, 5), (5, 5), (3, 4)])
assert len(LIVRE) == 16 and len(parts) == 1191 and len(bons) == 2 and len(cl) == 1 and LIVRE in set(bons)
assert res[tuple(GEMMES)] == 2 and sum(1 for n in res.values() if n == 0) == 12 and max(res.values()) == 666
assert res[((2,2),(3,3),(4,4),(5,5))] == 560
# temoins : la spirale « simple » essayee plus haut est refusee ; la part du livre privee d'une case aussi
assert spirale not in set(bons) and (LIVRE - {(3, 4)}) | {(2, 4)} not in set(bons)
print("controles : tout est conforme (temoins refuses)")
