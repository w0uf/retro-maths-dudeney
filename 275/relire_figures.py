#!/usr/bin/env python3
"""N° 275 THE SIXTEEN SHEEP : relecture, aux pixels, des six dessins du corrigé de Dudeney (figures_du_livre.png, gravure de 1917).
Seize moutons dans un carré 4 × 4, enfermés au départ par neuf claies. Pour chaque dessin n (2 à 7), Dudeney déplace n claies
(traits épais) pour obtenir trois enclos de 6, 6 et 4 moutons, toujours avec neuf claies. On mesure l'encre de chaque cloison.
    python3 relire_figures.py"""
import os
from collections import Counter
import numpy as np
from PIL import Image

# cases (r, c) ; cloisons intérieures : ('h', r, c) entre (r, c) et (r+1, c) ; ('v', r, c) entre (r, c) et (r, c+1)
A = [("h", r, c) for r in range(3) for c in range(4)] + [("v", r, c) for r in range(4) for c in range(3)]
cote = lambda e: ((e[1], e[2]), (e[1] + 1, e[2])) if e[0] == "h" else ((e[1], e[2]), (e[1], e[2] + 1))
init = {("h", 1, 0), ("h", 1, 1), ("h", 1, 2), ("h", 1, 3), ("v", 2, 0), ("v", 2, 2), ("h", 2, 1), ("h", 2, 2), ("v", 3, 1)}   # le départ

def regions(murs):
    comp, n = {}, 0
    for r in range(4):
        for c in range(4):
            if (r, c) in comp: continue
            comp[(r, c)] = n; pile = [(r, c)]
            while pile:
                x = pile.pop()
                for e in A:
                    if e in murs: continue
                    a, b = cote(e)
                    y = b if a == x else a if b == x else None
                    if y is not None and y not in comp: comp[y] = n; pile.append(y)
            n += 1
    return comp

def juge(nom, murs, epais):
    comp = regions(murs)
    utiles = all(comp[cote(e)[0]] != comp[cote(e)[1]] for e in murs)    # aucune claie inutile au milieu d'un enclos
    tailles = sorted(Counter(comp.values()).values())
    print("  %-10s claies %d ; enclos %s ; claies toutes utiles %s ; épaisses %d, toutes hors du départ %s ; fines = claies du départ %s"
          % (nom, len(murs), tailles, utiles, len(epais), epais <= set(A) - init, (murs - epais) <= init))
    return tailles == [4, 6, 6] and utiles and len(murs) == 9 and epais == murs - init

ici = os.path.dirname(os.path.abspath(__file__))
im = np.array(Image.open(os.path.join(ici, "figures_du_livre.png")).convert("L")) < 110
cadres = {2: (0, 0, 200, 195), 3: (200, 0, 400, 195), 4: (400, 0, 600, 195), 5: (0, 200, 200, 395), 6: (200, 200, 400, 395), 7: (400, 200, 600, 395)}
CORRIGES = {4: (10, 188, 12, 190), 6: (8, 188, 12, 189)}   # bord du carré relevé à la main : la détection automatique s'y trompe

print("témoin, le départ lui-même :", "accepté (ERREUR)" if juge("départ", set(init), set()) else "refusé")
def lire(im, n):
    """Cloisons présentes et cloisons épaisses du dessin n, lues aux pixels."""
    x0, y0, x1, y1 = cadres[n]
    sub = im[y0:y1, x0:x1]
    cols, rows = sub.sum(0), sub.sum(1)
    xs = [i for i, v in enumerate(cols) if v > 0.64 * sub.shape[0]]; ys = [i for i, v in enumerate(rows) if v > 0.64 * sub.shape[1]]
    L, R, T, B = CORRIGES.get(n, (min(xs), max(xs), min(ys), max(ys)))
    cw, ch = (R - L) / 4, (B - T) / 4
    mesure = {}                                     # cloison -> (épaisseur du trait, part de la cloison couverte d'encre)
    for r in range(3):
        for c in range(4):
            y = T + (r + 1) * ch; band = sub[int(y - 6):int(y + 7), int(L + c * cw + cw * .25):int(L + (c + 1) * cw - cw * .25)]
            mesure[("h", r, c)] = (band.any(1).sum(), band.mean(1).max())
    for r in range(4):
        for c in range(3):
            x = L + (c + 1) * cw; band = sub[int(T + r * ch + ch * .25):int(T + (r + 1) * ch - ch * .25), int(x - 6):int(x + 7)]
            mesure[("v", r, c)] = (band.any(0).sum(), band.mean(0).max())
    murs = {e for e, (w, cov) in mesure.items() if cov > 0.3}
    epais = {e for e in murs if mesure[e][0] >= 5}
    return murs, epais, (L, T, cw, ch)

for n in cadres:
    murs, epais, _ = lire(im, n)
    ok = juge("dessin %d" % n, murs, epais)
    print("    → valide :", ok, "; nombre de claies épaisses = numéro du dessin :", len(epais) == n)

# témoin aux pixels : on efface à la gomme une claie fine du dessin 2 ; la relecture doit refuser le dessin
murs, epais, (L, T, cw, ch) = lire(im, 2)
e = sorted(murs - epais)[0]; t = im.copy(); x0, y0 = cadres[2][:2]
if e[0] == "h": y = int(y0 + T + (e[1] + 1) * ch); t[y - 6:y + 7, int(x0 + L + e[2] * cw + 3):int(x0 + L + (e[2] + 1) * cw - 3)] = False
else: x = int(x0 + L + (e[2] + 1) * cw); t[int(y0 + T + e[1] * ch + 3):int(y0 + T + (e[1] + 1) * ch - 3), x - 6:x + 7] = False
m2, e2, _ = lire(t, 2)
print("témoin, dessin 2 avec la claie", e, "effacée :", "accepté (ERREUR)" if juge("témoin", m2, e2) else "refusé")
