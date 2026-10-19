# -*- coding: utf-8 -*-
"""n° 219 THE LETTER BLOCK PUZZLE — le taquin à huit lettres.
Départ  G E F / H C B / D _ A     Arrivée  A B C / D E F / G H _
Dudeney annonce 23 coups, « le moins possible »."""
from collections import deque

DEPART  = "GEFHCBD A".replace(" ", "_")
ARRIVEE = "ABCDEFGH_"
VOISINS = {i: [j for j in (i-3, i+3, i-1, i+1)
               if 0 <= j < 9 and not (i % 3 == 0 and j == i-1)
               and not (i % 3 == 2 and j == i+1)] for i in range(9)}

def coups(e):
    v = e.index("_")
    for j in VOISINS[v]:
        l = list(e); l[v], l[j] = l[j], "_"
        yield e[j], "".join(l)

# ── 1. la suite de coups de Dudeney ──────────────────────────────────────
SUITE = "A B F E C A B F E C A B D H G A B D H G D E F".split()
e = DEPART
for k, lettre in enumerate(SUITE, 1):
    suite = {L: s for L, s in coups(e)}
    if lettre not in suite:
        print("coup %d impossible : %s" % (k, lettre)); break
    e = suite[lettre]
else:
    print("les %d coups de Dudeney sont tous légaux" % len(SUITE))
    print("position finale :", e, "| conforme :", e == ARRIVEE)

# ── 2. le minimum, par exploration en largeur ────────────────────────────
vu = {DEPART: 0}; f = deque([DEPART])
while f:
    x = f.popleft()
    if x == ARRIVEE: break
    for _, y in coups(x):
        if y not in vu: vu[y] = vu[x] + 1; f.append(y)
print()
print("minimum réel :", vu[ARRIVEE], "coups   (Dudeney annonce 23)")

# ── 3. combien de chemins de longueur minimale ? ─────────────────────────
n = vu[ARRIVEE]
dist = {}; f = deque([ARRIVEE]); dist[ARRIVEE] = 0
while f:
    x = f.popleft()
    for _, y in coups(x):
        if y not in dist: dist[y] = dist[x] + 1; f.append(y)
chemins = {DEPART: 1}
niveau = [DEPART]
for k in range(n):
    suiv = {}
    for x in niveau:
        for _, y in coups(x):
            if dist[y] == dist[x] - 1:
                suiv[y] = suiv.get(y, 0) + chemins[x]
    chemins = suiv; niveau = list(suiv)
print("chemins optimaux distincts :", chemins.get(ARRIVEE, 0))

# ── 4. le taquin 3x3 tout entier ─────────────────────────────────────────
print()
print("positions atteignables depuis l'arrivée :", len(dist), "(sur 9! =", 362880, ")")
diam = max(dist.values())
print("position la plus éloignée : %d coups" % diam)
loin = [p for p, d in dist.items() if d == diam]
print("   il y en a", len(loin), ":", loin)

# ── 5. témoins : une suite fautive doit être refusée ─────────────────────
def rejoue(suite):
    e = DEPART
    for L in suite:
        s = {x: y for x, y in coups(e)}
        if L not in s: return None
        e = s[L]
    return e
t1 = SUITE[:3] + [SUITE[4], SUITE[3]] + SUITE[5:]
t2 = SUITE[:-1]
print()
print("témoin, deux coups intervertis :", "refusé" if rejoue(t1) != ARRIVEE else "ACCEPTÉ")
print("témoin, dernier coup oublié    :", "refusé" if rejoue(t2) != ARRIVEE else "ACCEPTÉ")
assert rejoue(SUITE) == ARRIVEE and rejoue(t1) != ARRIVEE and rejoue(t2) != ARRIVEE
assert vu[ARRIVEE] == 23 and chemins.get(ARRIVEE) == 1 and len(dist) == 181440 and diam == 31 and len(loin) == 2
