# -*- coding: utf-8 -*-
"""Le jeu complet : vingt-huit dominos en ligne droite.
Dudeney : 7 959 229 931 520, « la methode de resolution est tres complexe ».

Meme decomposition que pour les quinze : circuits eulriens du polygone,
puis insertion des doubles, puis rupture du cercle.
On valide d'abord la chaine de calcul sur le cas a quinze dominos.
"""
from array import array
import time

def circuits_fixes(S):
    """nombre de parcours fermes partant du sommet 0, empruntant chaque arete
    du graphe complet a S sommets une fois et une seule, et revenant en 0"""
    aretes = [(a, b) for a in range(S) for b in range(a+1, S)]
    E = len(aretes)
    inc = [[] for _ in range(S)]
    for i, (a, b) in enumerate(aretes):
        inc[a].append((i, b)); inc[b].append((i, a))
    f = array('q', [0]) * 0
    f = array('q', bytes(8 * (1 << E) * S))
    f[0*S + 0] = 1
    for m in range(1 << E):
        base = m*S
        for v in range(S):
            x = f[base + v]
            if not x: continue
            for (i, w) in inc[v]:
                if m >> i & 1: continue
                f[(m | 1 << i)*S + w] += x
    return f[((1 << E) - 1)*S + 0], E

t0 = time.time()
for S, nd, nom in ((5, 15, "double-quatre"), (7, 28, "double-six")):
    n0, E = circuits_fixes(S)
    passages = (S-1)//2            # chaque sommet est traverse (degre/2) fois
    cycl = n0 // passages
    # un double x-x s'insere a l'un des passages du circuit par le sommet x :
    # il y a donc « passages » choix par double, et non deux comme on pourrait
    # le croire en lisant le cas du double-quatre (ou passages vaut justement 2)
    doubles = passages ** S
    total = cycl * doubles * nd
    print("  polygone a %d sommets (%d aretes) :" % (S, E))
    print("     parcours fermes au depart du sommet 0 : %d" % n0)
    print("     circuits distincts (a rotation pres)  : %d" % cycl)
    print("     x %d^%d = %d pour les doubles, x %d pour rompre le cercle"
          % (passages, S, doubles, nd))
    print("     -> %s dominos en ligne : %d" % (nd, total))
    print("     (%.0f s)" % (time.time()-t0), flush=True)
print()
print("  Dudeney : 126 720 pour le double-quatre, 7 959 229 931 520 pour le jeu complet.")
assert total == 7959229931520
