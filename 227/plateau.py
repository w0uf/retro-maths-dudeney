# -*- coding: utf-8 -*-
"""n° 227 CENTRAL SOLITAIRE — Dudeney 1917. Le solitaire anglais a 33 trous.
Numerotation de Dudeney (lignes de haut en bas, le centre est le 17) :
            1  2  3
            4  5  6
      7  8  9 10 11 12 13
     14 15 16 17 18 19 20
     21 22 23 24 25 26 27
           28 29 30
           31 32 33
"""
TROUS = {}
n = 1
for r, cols in enumerate(((2,3,4),(2,3,4),(0,1,2,3,4,5,6),(0,1,2,3,4,5,6),
                          (0,1,2,3,4,5,6),(2,3,4),(2,3,4))):
    for c in cols:
        TROUS[n] = (r, c); n += 1
POS = {v: k for k, v in TROUS.items()}
assert TROUS[17] == (3, 3) and n == 34

def sauts():
    """(depart, saute, arrivee) pour tous les sauts possibles du plateau."""
    out = []
    for a, (r, c) in TROUS.items():
        for dr, dc in ((0,1),(0,-1),(1,0),(-1,0)):
            m, b = (r+dr, c+dc), (r+2*dr, c+2*dc)
            if m in POS and b in POS:
                out.append((a, POS[m], POS[b]))
    return out
SAUTS = sauts()
VOISIN = {}
for a, m, b in SAUTS: VOISIN.setdefault(a, []).append((m, b))

def rejoue(coups, depart_vide=17, bavard=False):
    """coups : liste de listes de trous, ex. [[19,17],[16,18],[29,17,19],…]"""
    plateau = {t: True for t in TROUS}
    plateau[depart_vide] = False
    for i, chaine in enumerate(coups, 1):
        for a, b in zip(chaine, chaine[1:]):
            m = [m for m, bb in VOISIN.get(a, []) if bb == b]
            if not m:
                return "coup %d : %d → %d n'est pas un saut du plateau" % (i, a, b)
            m = m[0]
            if not plateau[a]:  return "coup %d : le trou %d est vide" % (i, a)
            if not plateau[m]:  return "coup %d : rien à sauter en %d" % (i, m)
            if plateau[b]:      return "coup %d : l'arrivée %d est occupée" % (i, b)
            plateau[a] = plateau[m] = False; plateau[b] = True
        if bavard:
            print("   après le coup %2d : %d pions" % (i, sum(plateau.values())))
    restants = [t for t in TROUS if plateau[t]]
    return restants
