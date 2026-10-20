#!/usr/bin/env python3
"""Rétro Math's — n° 333 THE QUEEN'S JOURNEY (Dudeney, 1917). La dame part de sa case (d1),
cinq coups, ne repasse sur aucune case, ne croise jamais sa trace : distance maximale ?
Unité : 2 pouces d'un centre de case au suivant. Cases : (colonne 0-7, rangée 0-7), d1 = (3, 0).
    python3 voyage_dame.py   (environ 2 min : les 64 cases de départ sont essayées)"""
import sys
from math import sqrt
from collections import Counter
D = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
R2 = sqrt(2)
def cherche(depart, coups, croisement=True):
    best = []          # (droits, diagonaux, chemin)
    res = Counter(); ex = {}
    def rec(pos, k, vis, coins, nd, ng, chemin, dern):
        if k == coups:
            res[(nd, ng)] += 1; ex.setdefault((nd, ng), chemin); return
        for d in D:
            if dern is not None and (d == dern or d == (-dern[0], -dern[1])): continue   # un coup = un changement de direction
            x, y = pos; v2 = set(); c2 = set(); n = 0
            while True:
                nx, ny = x + d[0], y + d[1]
                if not (0 <= nx < 8 and 0 <= ny < 8) or (nx, ny) in vis or (nx, ny) in v2: break
                if d[0] and d[1]:
                    coin = (min(x, nx), min(y, ny))            # le coin commun aux quatre cases
                    if croisement and (coin in coins or coin in c2): break
                    c2 = c2 | {coin}
                v2 = v2 | {(nx, ny)}; x, y = nx, ny; n += 1
                diag = bool(d[0] and d[1])
                rec((x, y), k + 1, vis | v2, coins | c2, nd + (0 if diag else n), ng + (n if diag else 0), chemin + [(x, y)], d)
    rec(depart, 0, {depart}, frozenset(), 0, 0, [depart], None)
    return res, ex
nom = lambda p: "abcdefgh"[p[0]] + str(p[1] + 1)
L = lambda k: 2 * k[0] + 2 * R2 * k[1]
TRI = {}
for croisement in (True, False):
    res, ex = cherche((3, 0), 5, croisement)
    tri = TRI[croisement] = sorted(res, key=L, reverse=True); NB = TRI.setdefault('nb', {}); NB[croisement] = (sum(res.values()), res[tri[0]], res[tri[1]])
    print("=== avec interdiction de croiser sa trace" if croisement else "=== si l'on autorisait le croisement (cases jamais revisitées)")
    print("trajets de cinq coups :", sum(res.values()))
    for k in tri[:6]:
        print("  %.4f pouces = %d pas droits + %d pas diagonaux, %d trajets, ex. %s" % (L(k), k[0], k[1], res[k], '-'.join(nom(p) for p in ex[k])))

# --- ce que dit l'article
from math import isclose
t = TRI[True]
assert TRI['nb'][True] == (718948, 1, 1)
assert t[0] == (17, 12) and isclose(L(t[0]), 34 + 24 * R2) and L(t[0]) > 67.9      # d1-h1-a8-h8-h2-c7
assert t[1] == (24, 7) and isclose(L(t[1]), 48 + 14 * R2) and L(t[1]) < 67.8       # d1-h1-h8-a1-a8-g8, « la plupart »
assert L(t[2]) < 67 and isclose(L(t[0]) - L(t[1]), 10 * R2 - 14)
assert L(TRI[False][0]) > 73                                                         # sans la regle du croisement
# temoin : le trajet le plus long sans la regle croise sa trace, il doit etre absent de la recherche avec la regle
assert TRI[False][0] not in cherche((3, 0), 5, True)[0]
# moins de coups : le debut du trajet « de la plupart » (d1-h1-h8-a1-a8) est le meilleur en quatre coups, et seul
r4, e4 = cherche((3, 0), 4)
m4 = max(r4, key=L)
assert r4[m4] == 1 and '-'.join(nom(p) for p in e4[m4]) == "d1-h1-h8-a1-a8"
r3, e3 = cherche((3, 0), 3)
assert isclose(L(max(r3, key=L)), L((11, 7))) and (11, 7) in r3   # d1-h1-h8-a1 : 41,80, parmi les meilleurs
# toutes les cases de depart
meilleur = {}
for x in range(8):
    for y in range(8):
        r, _ = cherche((x, y), 5); meilleur[(x, y)] = max(L(k) for k in r)
pire = min(meilleur.values())
assert isclose(pire, L(t[0])) and sorted(nom(p) for p in meilleur if isclose(meilleur[p], pire)) == ["a4", "a5", "d1", "d8", "e1", "e8", "h4", "h5"]
assert isclose(meilleur[(0, 0)] - pire, 6)                                           # depuis un coin : six pouces de plus
print("pire depart : %.2f pouces (d1, e1 et leurs six images) ; depuis un coin : %.2f" % (pire, meilleur[(0, 0)]))
print("controles : tout est conforme (temoins refuses)")
