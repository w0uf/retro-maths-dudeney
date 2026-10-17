#!/usr/bin/env python3
"""Relit la planche du n° 142 aux pixels seuls : épaisseur de chaque couture, morceaux reconstitués, puis contrôle
(4 morceaux de 5 cases superposables, case grise à part, les 4 pavent la croix). Position des panneaux : fichier json de la planche.
    python3 relire.py planche.png planche.json"""
import sys, os, json, io, contextlib, runpy
import numpy as np
from PIL import Image
ici = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(ici, "decoupages.py"))
Q, libre, pave_croix, sym = G["Q"], G["libre"], G["pave_croix"], None
im = np.array(Image.open(sys.argv[1]).convert("L"))
pan = json.load(open(sys.argv[2]))
def lire(im, p):
    """Case gardée et morceaux d'un panneau, lus aux pixels."""
    x0, y0, C = p["x0"], p["y0"], p["case"]
    def epais(xa, ya, xb, yb):          # largeur d'encre noire au milieu d'une couture, mesurée en travers
        mx, my = int((xa + xb) / 2), int((ya + yb) / 2)
        prof = im[my, mx - 6:mx + 7] if xa == xb else im[my - 6:my + 7, mx]
        return int((prof < 100).sum())
    gris = [v for v in Q if 150 < im[int(y0 + v[0] * C + C / 2), int(x0 + v[1] * C + C / 2)] < 200]
    assert len(gris) == 1, gris
    voisins = {v: [] for v in Q}
    for (r, c) in Q:
        for (dr, dc) in ((0, 1), (1, 0)):
            w = (r + dr, c + dc)
            if w not in Q: continue
            e = epais(x0 + (c + 1) * C, y0 + r * C, x0 + (c + 1) * C, y0 + (r + 1) * C) if dc else epais(x0 + c * C, y0 + (r + 1) * C, x0 + (c + 1) * C, y0 + (r + 1) * C)
            if e <= 2: voisins[(r, c)].append(w); voisins[w].append((r, c))
    vu, morceaux = set(gris), []
    for v in sorted(Q):
        if v in vu: continue
        pile, m = [v], {v}; vu.add(v)
        while pile:
            x = pile.pop()
            for y in voisins[x]:
                if y not in vu: vu.add(y); m.add(y); pile.append(y)
        morceaux.append(frozenset(m))
    ok = len(morceaux) == 4 and all(len(m) == 5 for m in morceaux) and len({libre(m) for m in morceaux}) == 1 and pave_croix(morceaux[0], True) > 0
    conforme = gris[0] == tuple(p["F"]) and set(morceaux) == {frozenset(map(tuple, m)) for m in p["morceaux"]}
    return gris[0], morceaux, ok, conforme
lus = []
for p in pan:
    F, morceaux, ok, conforme = lire(im, p); lus.append((F, morceaux))
    print(" ", p["legende"], "| case gardée", F, "| morceaux lus", sorted(len(m) for m in morceaux), "| valide", ok, "| conforme au calcul", conforme)
# témoin : on efface une coupe du panneau 1 (trait épais entre deux morceaux) ; la relecture doit refuser le panneau
p = pan[0]; x0, y0, C = int(p["x0"]), int(p["y0"]), p["case"]
piece = {tuple(v): i for i, m in enumerate(p["morceaux"]) for v in m}
(r, c) = next(v for v in sorted(piece) if (v[0], v[1] + 1) in piece and piece[(v[0], v[1] + 1)] != piece[v])
t = im.copy(); x = x0 + (c + 1) * C
t[y0 + r * C + 3:y0 + (r + 1) * C - 2, x - 4:x + 5] = 255; t[y0 + r * C:y0 + (r + 1) * C + 1, x] = 0
F, morceaux, ok, conforme = lire(t, p)
print("témoin (coupe effacée entre", (r, c), "et", (r, c + 1), ") : morceaux lus", sorted(len(m) for m in morceaux), "| valide", ok, "→", "refusé" if not ok else "ERREUR : accepté")
# les sept sont-ils distincts aux symétries du patchwork près ?
def canon(F, part):
    out = []
    for mir in range(2):
        for q in range(4):
            def g(x):
                r, c = x
                if mir: c = 4 - c
                for _ in range(q): r, c = c, 4 - r
                return (r, c)
            out.append((g(F), tuple(sorted(tuple(sorted(g(x) for x in m)) for m in part))))
    return min(out)
print("découpages distincts aux symétries près :", len({canon(F, m) for F, m in lus}))
