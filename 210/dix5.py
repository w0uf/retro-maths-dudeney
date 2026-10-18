# -*- coding: utf-8 -*-
"""n° 210 — le carnet de Dudeney, damier par damier.

Il note : la Fleche tient sur 7x7 (et de trois facons), l'Entonnoir sur 8x8,
l'Etoile exige 9x7, le Clou 11x7, les Ciseaux 11x9, le Compas 17x12 —
« du moins ce sont les meilleurs resultats consignes dans mon carnet ; on peut
les battre, mais je ne le crois pas ».

On balaie toutes les tailles et l'on note, pour chaque type de figure, les
damiers MINIMAUX qui le portent.
"""
import sys, time
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dix4 import droites, inter, cherche, type_figure

MAX = 13
types = {}
print("=== Balayage ===")
for m in range(4, MAX+1):
    for n in range(4, m+1):
        D, S = cherche(m, n)
        if not S: continue
        vus = set()
        for ch, pts in S: vus.add(type_figure(D, ch, pts))
        for t in vus: types.setdefault(t, []).append((m, n))
        print("  %2d x %-2d : %4d arrangements, %d type(s)" % (m, n, len(S), len(vus)),
              flush=True)

print()
print("=== Pour chaque type, les damiers MINIMAUX ===")
for i, (t, L) in enumerate(sorted(types.items(), key=lambda kv: min(kv[1])), 1):
    mini = [b for b in L if not any(c != b and c[0] <= b[0] and c[1] <= b[1]
                                    for c in L)]
    print("  type %d : %s" % (i, ", ".join("%dx%d" % b for b in sorted(mini))))
print("  types trouves jusqu'a %dx%d : %d" % (MAX, MAX, len(types)))
