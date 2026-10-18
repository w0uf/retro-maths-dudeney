#!/usr/bin/env python3
"""N° 164 THE POTATO PUZZLE : combien de morceaux, au plus, avec n coups de couteau droits dans une tranche ?
On ne suppose aucune formule : on trace n cordes dans un disque et l'on compte les morceaux sur un maillage fin,
chaque point étant classé par le côté où il se trouve de chaque coupe (deux points du même morceau ont le même classement).
Pour le maximum, toutes les cordes se coupent deux à deux à l'intérieur, jamais trois au même point.
    python3 patate.py"""
import random, math
import numpy as np

N = 1400
y, x = np.mgrid[-1:1:N * 1j, -1:1:N * 1j]
dedans = x * x + y * y < 1

def morceaux(droites):
    """Nombre de morceaux du disque découpé par les droites (a, b, c) : a x + b y = c, compté sur le maillage."""
    code = np.zeros(x.shape, dtype=np.int64)
    for k, (a, b, c) in enumerate(droites):
        code |= ((a * x + b * y > c).astype(np.int64) << k)
    vus, aires = np.unique(code[dedans], return_counts=True)
    return int((aires > 30).sum())          # on ignore les miettes de quelques pixels collées aux coupes

def en_position_generale(n, rng):
    """n droites qui se coupent deux à deux dans le disque, à bonne distance du bord et les unes des autres."""
    while True:
        D = [(math.cos(t), math.sin(t), rng.uniform(-.35, .35)) for t in (rng.uniform(0, math.pi) for _ in range(n))]
        P = []
        for (a1, b1, c1), (a2, b2, c2) in ((D[i], D[j]) for i in range(n) for j in range(i + 1, n)):
            det = a1 * b2 - a2 * b1
            if abs(det) < .15: break
            P.append(((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det))
        else:
            if all(px * px + py * py < .8 for px, py in P) and all(math.dist(p, q) > .06 for i, p in enumerate(P) for q in P[i + 1:]):
                return D

rng = random.Random(164)
print("coups  morceaux  (formule du livre (n(n+1)+1)/2 ; formule juste (n(n+1)+2)/2)")
for n in range(8):
    m = morceaux(en_position_generale(n, rng))
    print("  %d     %3d       %5.1f ; %d" % (n, m, (n * (n + 1) + 1) / 2, (n * (n + 1) + 2) // 2))
    assert m == (n * (n + 1) + 2) // 2

# la gravure : six coups en quadrillage, trois parallèles dans chaque sens
grille = [(1, 0, c) for c in (-.4, 0, .4)] + [(0, 1, c) for c in (-.4, 0, .4)]
print("la gravure (3 coups × 3 coups) :", morceaux(grille), "morceaux ; cinq coups bien placés en donnent déjà", morceaux(en_position_generale(5, rng)))
# témoin : trois droites concourantes ; le compte doit perdre un morceau
print("témoin (3 coups par un même point) :", morceaux([(math.cos(t), math.sin(t), 0) for t in (0, 1, 2)]), "morceaux au lieu de 7")
