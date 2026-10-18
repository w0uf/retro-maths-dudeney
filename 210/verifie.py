#!/usr/bin/env python3
"""N° 210 THE TEN COINS : contrôle indépendant des figures trouvées par dix4.py sur le damier 13 × 13.
Chaque figure doit être formée de dix cases distinctes du damier, alignées quatre par quatre sur cinq droites,
sans autre alignement de quatre ; et le Compas (type 6) doit bien y figurer.
    python3 verifie.py"""
from itertools import combinations
import dix4

def aligne(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) == (q[1] - p[1]) * (r[0] - p[0])
def juge(pts, m, n):
    pts = list(pts)
    if len(set(pts)) != 10 or not all(0 <= x < m and 0 <= y < n for x, y in pts): return False
    lignes = [q for q in combinations(pts, 4) if all(aligne(q[0], q[1], r) for r in q[2:])]
    return len(lignes) == 5 and all(sum(p in l for l in lignes) == 2 for p in pts)   # chaque pièce sur deux droites

D, S = dix4.cherche(13, 13)
types = {dix4.type_figure(D, ch, pts) for ch, pts in S}
print(len(S), "figures sur 13 × 13 ;", len(types), "types")
assert all(juge(pts.values(), 13, 13) for ch, pts in S)
print("toutes valides : dix pièces, cinq droites de quatre")
ch, pts = S[0]; faux = list(pts.values()); faux[0] = (faux[0][0] + 1 if faux[0][0] < 12 else faux[0][0] - 1, faux[0][1])
print("témoin (une pièce déplacée d'une case) :", "accepté (ERREUR)" if juge(faux, 13, 13) else "refusé")
