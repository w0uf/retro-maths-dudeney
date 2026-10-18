#!/usr/bin/env python3
"""N° 343 : contrôle de l'optimalité de taquin.c. Une recherche en largeur, sans heuristique, donne la vraie distance
de toutes les positions à 18 coups au plus du départ ; on en tire 500 au hasard et taquin.c doit trouver exactement cette distance.
    gcc -O2 -o taquin taquin.c && python3 controle_taquin.py"""
import os, random, subprocess
DEPART = tuple(list(range(1, 16)) + [0])
dist, front = {DEPART: 0}, [DEPART]
for d in range(1, 19):
    nouv = []
    for s in front:
        v = s.index(0); r, c = divmod(v, 4)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= r + dr < 4 and 0 <= c + dc < 4:
                p = (r + dr) * 4 + c + dc; t = list(s); t[v], t[p] = t[p], 0; t = tuple(t)
                if t not in dist: dist[t] = d; nouv.append(t)
    front = nouv
print(len(dist), "positions à 18 coups au plus, distance exacte connue")
random.seed(343)
ech = random.sample(sorted(dist), 500)
ici = os.path.dirname(os.path.abspath(__file__))
out = subprocess.run([os.path.join(ici, "taquin")], input="\n".join(" ".join(map(str, s)) for s in ech) + "\n", capture_output=True, text=True).stdout.split("\n")
faux = [(s, dist[s], int(l.split()[0])) for s, l in zip(ech, out) if int(l.split()[0]) != dist[s]]
print("500 positions tirées (distances de %d à %d) : taquin.c donne la distance exacte pour %d" % (min(dist[s] for s in ech), max(dist[s] for s in ech), 500 - len(faux)))
assert not faux, faux[:3]
