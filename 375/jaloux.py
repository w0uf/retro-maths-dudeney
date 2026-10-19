# -*- coding: utf-8 -*-
"""n° 375 FIVE JEALOUS HUSBANDS — cinq couples, un canot de trois places.
Aucune femme ne doit se trouver, dans le canot ou sur une rive, en compagnie
d'un homme (ou d'hommes) sans que son mari soit présent."""
from collections import deque
from itertools import combinations

def sur(hommes, femmes, n):
    """cette assemblée est-elle convenable ?"""
    for i in range(n):
        if (femmes >> i) & 1 and not (hommes >> i) & 1:   # femme sans son mari
            if hommes: return False                        # ...et il y a un homme
    return True

def minimum(n, place):
    tous = (1 << n) - 1
    depart = (tous, tous, 0)                   # (hommes à gauche, femmes à gauche, canot)
    arrivee = (0, 0, 1)
    vu = {depart: 0}; f = deque([depart])
    while f:
        H, F, c = f.popleft()
        d = vu[(H, F, c)]
        # qui est du côté du canot ?
        Hc = H if c == 0 else tous ^ H
        Fc = F if c == 0 else tous ^ F
        hs = [i for i in range(n) if (Hc >> i) & 1]
        fs = [i for i in range(n) if (Fc >> i) & 1]
        for k in range(1, place+1):
            for nh in range(0, k+1):
                for gh in combinations(hs, nh):
                    for gf in combinations(fs, k-nh):
                        mh = sum(1 << i for i in gh); mf = sum(1 << i for i in gf)
                        if not sur(mh, mf, n): continue         # le canot
                        if c == 0: H2, F2 = H ^ mh, F ^ mf
                        else:      H2, F2 = H | mh, F | mf
                        if not sur(H2, F2, n): continue         # rive gauche
                        if not sur(tous ^ H2, tous ^ F2, n): continue  # rive droite
                        e = (H2, F2, 1-c)
                        if e not in vu:
                            vu[e] = d + 1
                            if e == arrivee: return d + 1
                            f.append(e)
    return None

print("cinq couples, canot de trois :", minimum(5, 3), "traversées  (Dudeney : onze)")
print()
print("couples | canot 2 | canot 3 | canot 4 | canot 5")
for n in range(2, 8):
    ligne = []
    for p in (2, 3, 4, 5):
        r = minimum(n, p)
        ligne.append("%7s" % (r if r is not None else "—"))
    print("   %2d   |%s" % (n, "|".join(ligne)))
print()
print("(un tiret : la traversée est impossible, quelles que soient les manœuvres)")

# ── et sans jalousie ? ─────────────────────────────────────────────────
print()
import math
for n, p in ((5, 3),):
    gens = 2*n
    trav = 2*math.ceil((gens - p)/(p - 1)) + 1
    print("sans jalousie, %d personnes et un canot de %d : %d traversées"
          % (gens, p, trav), " (Dudeney : neuf)")
print("la jalousie coûte donc exactement deux traversées de plus.")

# ── jusqu'où peut-on aller ? un seuil, pas une loi ──────────────────────
# (une première lecture de la table, sur trois points, suggérait « au plus
# 2p - 1 couples pour un canot de p places » ; c'est faux dès p = 4.)
import sys
LOIN = "--loin" in sys.argv            # jusqu'à 14 couples (environ 19 min)
nmax = 14 if LOIN else 10
print()
print("canot de 2 et de 3 places : à partir de combien de couples est-ce impossible ?")
for p in (2, 3):
    res = [(n, minimum(n, p)) for n in range(2, 9)]
    passe = [n for n, r in res if r is not None]
    print("   canot de %d : passent %s ; impossibles %s"
          % (p, passe, [n for n, r in res if r is None]))
    assert passe == list(range(2, 2*p))
print("canot de 4 et 5 places : plus de limite (essayé jusqu'à %d couples%s)"
      % (nmax, "" if LOIN else " ; --loin pour aller à 14"))
for p in (4, 5):
    res = [(n, minimum(n, p)) for n in range(2, nmax + 1, 2)]
    print("   canot de %d : %s" % (p, ", ".join("%d couples en %d" % x for x in res)))
    assert all(r is not None for n, r in res)

# ── témoins ─────────────────────────────────────────────────────────────
print()
print("témoins : une femme seule avec l'autre homme est refusée :", not sur(0b10, 0b01, 2))
print("          un couple seul est accepté :", sur(0b01, 0b01, 2))
print("          des femmes seules entre elles sont acceptées :", sur(0, 0b111, 3))
assert not sur(0b10, 0b01, 2) and sur(0b01, 0b01, 2) and sur(0, 0b111, 3)
assert minimum(5, 3) == 11 and minimum(3, 2) == 11 and minimum(4, 2) is None
