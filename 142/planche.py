#!/usr/bin/env python3
"""N° 142 : planche des sept découpages, dessinée directement à partir du calcul de decoupages.py (ce n'est pas une figure du livre).
Coutures en trait fin, coupes en trait épais, case gardée en gris. La planche est relue ensuite par relire.py.
    python3 planche.py planche.png      (écrit aussi planche.json, positions des panneaux pour relire.py)"""
import sys, os, json, io, contextlib, runpy
from PIL import Image, ImageDraw, ImageFont
ici = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(ici, "decoupages.py"))
orb, livre, sym = G["orb"], G["livre"], G["sym"]
livre_forme = G["libre"](livre[0])
cle_livre = sym([frozenset(p) for p in livre], (2, 2))
cases = []
for (F, part), (f0, forme) in orb.items():
    if (F, part) == cle_livre: F, part = (2, 2), [frozenset(p) for p in livre]   # celui du livre, dans le sens du livre
    cases.append((0 if F == (2, 2) and set(map(frozenset, part)) == set(map(frozenset, livre)) else 1 if F == (2, 2) else 2, F, [sorted(p) for p in part], forme))
cases.sort(key=lambda z: (z[0], len(z[3]) != 5 or z[3] != ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1)), z[1], z[2]))
assert len(cases) == 7 and sum(1 for c in cases if c[0] == 0) == 1

SERIF = "DejaVuSerif-Bold.ttf"   # police DejaVu, à installer si besoin (paquet fonts-dejavu)
C, M = 34, 26                     # côté d'une case, marge autour d'un patchwork
P = 5 * C + 2 * M                 # largeur d'un patchwork avec marge
LEG = 44
W, H = 4 * P + 40, 2 * (P + LEG) + 120
im = Image.new("L", (W, H), 255); d = ImageDraw.Draw(im)
fT, fS, fN = ImageFont.truetype(SERIF, 24), ImageFont.truetype(SERIF, 15), ImageFont.truetype(SERIF, 14)
def centre(txt, y, f):
    d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=0)
centre("THE SILK PATCHWORK — les sept découpages", 14, fT)
centre("Planche composée pour Rétro Math’s d’après le calcul, pas une figure du livre", 46, fS)
Q = G["Q"]
pos = []
for i in range(7):
    ligne, col = (0, i) if i < 3 else (1, i - 3)
    x = 20 + col * P + (P / 2 if ligne == 0 else 0); y = 80 + ligne * (P + LEG)
    pos.append((x, y))
dessins = []
for i, (cat, F, part, forme) in enumerate(cases):
    x0, y0 = pos[i][0] + M, pos[i][1] + M
    piece = {}
    for k, p in enumerate(part):
        for v in p: piece[tuple(v)] = k
    piece[tuple(F)] = "F"
    r, c = F
    d.rectangle((x0 + c * C, y0 + r * C, x0 + (c + 1) * C, y0 + (r + 1) * C), fill=175)
    for (r, c) in Q:                                  # coutures : trait fin partout
        d.rectangle((x0 + c * C, y0 + r * C, x0 + (c + 1) * C, y0 + (r + 1) * C), outline=0, width=1)
    for (r, c) in Q:                                  # coupes : trait épais entre deux morceaux différents, et le bord
        for (dr, dc, seg) in ((0, 1, ((c + 1, r), (c + 1, r + 1))), (1, 0, ((c, r + 1), (c + 1, r + 1))), (0, -1, ((c, r), (c, r + 1))), (-1, 0, ((c, r), (c + 1, r)))):
            v = (r + dr, c + dc)
            if v not in Q or piece[v] != piece[(r, c)]:
                (a, b), (e, f) = seg
                d.line((x0 + a * C, y0 + b * C, x0 + e * C, y0 + f * C), fill=0, width=5)
    leg = ("%d. Le découpage du livre" % (i + 1)) if cat == 0 else ("%d. Au centre, en équerres" % (i + 1)) if forme != livre_forme else ("%d. Au centre, autre placement" % (i + 1)) if cat == 1 else ("%d. Case gardée au bord" % (i + 1))
    d.text((pos[i][0] + (P - d.textlength(leg, font=fN)) / 2, y0 + 5 * C + 12), leg, font=fN, fill=0)
    dessins.append(dict(F=list(F), morceaux=part, x0=x0, y0=y0, case=C, legende=leg))
centre("Trait épais : coupe le long d’une couture. Case grise : le carré gardé entier.", H - 34, fS)
im.save(sys.argv[1])
json.dump(dessins, open(sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace(".png", ".json"), "w"))
print("planche", im.size, ":", [x["legende"] for x in dessins])
