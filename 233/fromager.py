#!/usr/bin/env python3
"""Rétro Math's — n° 233 THE ECCENTRIC CHEESEMONGER (Dudeney, 1917).
Seize fromages en rang ; un fromage seul saute par-dessus exactement quatre fromages (une pile compte pour sa
hauteur) et se pose sur le tas suivant ; il faut finir en quatre piles de quatre. Rejeu de ses trois solutions, et
exploration complète des parties de douze coups.
    python3 fromager.py   (quelques secondes)"""
import itertools, math
from collections import Counter
print("=== 233. Fromager ===")
def jouer(coups, verbeux=False):
    """coups = [(fromage deplace, fromage vise)] ; numeros de fromages. Regle : on franchit
    exactement quatre FROMAGES (les piles comptent pour leur hauteur), on se pose sur le tas suivant."""
    pos = {k: k for k in range(1, 17)}                   # fromage -> case
    for a, b in coups:
        h = Counter(pos.values())
        if h[pos[a]] != 1: return "le %d n'est pas seul" % a
        s, c = pos[a], pos[b]; pas = 1 if c > s else -1
        franchis = sum(h[x] for x in range(s + pas, c, pas))
        if franchis != 4 or h[c] == 0 or h[c] >= 4: return "coup %d-%d : %d franchis" % (a, b, franchis)
        pos[a] = c
    h = Counter(pos.values())
    return sorted(h) if set(h.values()) == {4} else "piles %s" % dict(h)
def jouer_tas(coups):
    """Mauvaise lecture : une pile compte pour UN."""
    pos = {k: k for k in range(1, 17)}
    for a, b in coups:
        h = Counter(pos.values()); s, c = pos[a], pos[b]; pas = 1 if c > s else -1
        if sum(1 for x in range(s + pas, c, pas) if h[x]) != 4: return "echec au coup %d-%d" % (a, b)
        pos[a] = c
    return "passe"
S = {"extremites": "7-2 8-7 9-8 10-15 6-10 5-6 14-16 13-14 12-13 3-1 4-3 11-4",
     "13-14-15": "9-4 10-9 11-10 6-14 5-6 12-15 8-12 7-8 16-5 3-13 2-3 1-2",
     "3-5-12-14": "8-3 9-14 16-12 1-5 10-9 7-10 11-8 2-1 4-16 13-2 6-11 15-4"}
RES = {}
for nom, s in S.items():
    c = [tuple(map(int, x.split("-"))) for x in s.split()]; RES[nom] = (jouer(c), jouer_tas(c))
    print("   %s : piles sur les cases %s | lecture « une pile = un » : %s" % (nom, jouer(c), jouer_tas(c)))
# exploration complete sur les hauteurs
def suivants(e):
    for s in range(16):
        if e[s] != 1: continue
        for pas in (1, -1):
            f, c = 0, s + pas
            while 0 <= c < 16 and f < 4: f += e[c]; c += pas
            while 0 <= c < 16 and e[c] == 0: c += pas
            if f == 4 and 0 <= c < 16 and e[c] < 4:
                n = list(e); n[s] = 0; n[c] += 1; yield tuple(n), (s + 1, c + 1)
niveau = {tuple([1] * 16): 1}
for k in range(12):
    nv = Counter()
    for e, w in niveau.items():
        for n, _ in suivants(e): nv[n] += w
    niveau = nv
finales = {tuple(i + 1 for i, h in enumerate(e) if h == 4): w for e, w in niveau.items() if sorted(e)[-4:] == [4, 4, 4, 4]}
print("   dispositions finales atteignables : %d sur %d | parties gagnantes : %d" % (len(finales), math.comb(16, 4), sum(finales.values())))
for cible in ((1, 2, 15, 16), (4, 13, 14, 15), (3, 5, 12, 14), (1, 2, 3, 4), (7, 8, 9, 10), (1, 6, 11, 16), (4, 8, 12, 16)):
    print("     ", cible, finales.get(cible, 0), "parties")
sym = lambda t: tuple(sorted(17 - x for x in t))
print("   symetrie respectee :", all(sym(t) in finales for t in finales))
manq = sorted(t for t in itertools.combinations(range(1, 17), 4) if t not in finales)
print("   interdites : %d ; exemples %s" % (len(manq), manq[:12]))
print("   plus grand ecart entre deux piles voisines :", max(max(b - a for a, b in zip(t, t[1:])) for t in finales),
      "| plus petite derniere pile :", min(t[3] for t in finales), "| plus grande premiere :", max(t[0] for t in finales))
print("   quatre piles contigues atteignables :", [t for t in finales if t[3] - t[0] == 3])
print("   trois contigues :", sorted({t for t in finales if t[2] - t[0] == 2 or t[3] - t[1] == 2})[:40], len({t for t in finales if t[2] - t[0] == 2 or t[3] - t[1] == 2}))
print("   la plus facile / la plus rare :", max(finales.items(), key=lambda x: x[1]), min(finales.items(), key=lambda x: x[1]))

# --- contrôles
assert RES["extremites"][0] == [1, 2, 15, 16] and RES["13-14-15"][0] == [4, 13, 14, 15] and RES["3-5-12-14"][0] == [3, 5, 12, 14]
assert all(r[1] != "passe" for r in RES.values())                    # la lecture « une pile compte pour un » échoue
assert len(finales) == 190 and sum(finales.values()) == 77968
assert finales[(1, 2, 15, 16)] == 11200 and finales[(4, 13, 14, 15)] == 16 and finales[(3, 5, 12, 14)] == 1080
assert all(sym(t) in finales for t in finales) and [t for t in finales if t[3] - t[0] == 3] == []
# témoin : sa première solution avec deux coups intervertis est refusée
c = [tuple(map(int, x.split("-"))) for x in S["extremites"].split()]
assert not isinstance(jouer([c[1], c[0]] + c[2:]), list)
print("contrôles : tout est conforme (témoins refusés)")
