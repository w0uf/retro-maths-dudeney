# -*- coding: utf-8 -*-
"""n° 385 « STRAND » PATIENCE — la partie la plus courte.
Deux piles de neuf cartes, quatre places vides ; une carte se pose sur une place
vide ou sur une carte de valeur immediatement superieure. But : echanger les
piques et les trefles. Dudeney : « 62 moves... This is my record; perhaps the
reader can beat it. »
    python3 patience.py          (quelques secondes)
Ecrit la partie trouvee dans partie_56.txt, a cote du script."""
import os, time
from collections import deque

DEP = (("9D", "8S", "7D", "6S", "5D", "4S", "3D", "2S", "1D"),
       ("9H", "8C", "7H", "6C", "5H", "4C", "3H", "2C", "1H"), (), (), (), ())
BUT0 = ("9D", "8C", "7D", "6C", "5D", "4C", "3D", "2C", "1D")
BUT1 = ("9H", "8S", "7H", "6S", "5H", "4S", "3H", "2S", "1H")

def v(c): return int(c[0])

def coups(e):
    """tous les coups permis. Deux coups inutiles sont omis : poser sur une place
    vide une carte deja seule sur la sienne, et bouger un 9 (il est au fond de sa
    pile, il n'en sort que seul, et rien ne peut le recevoir)."""
    for i, p in enumerate(e):
        if not p or p[-1][0] == "9": continue
        c = p[-1]
        for k, q in enumerate(e):
            if k == i: continue
            if (q and v(q[-1]) == v(c) + 1) or (not q and len(p) > 1):
                n = list(e); n[i] = p[:-1]; n[k] = q + (c,)
                yield (c, q[-1] if q else None), tuple(n)

def cle(e):
    """les piles 0 et 1 gardent leur 9 ; les quatre places vides sont interchangeables"""
    return (e[0], e[1], tuple(sorted(e[2:])))

def plus_courte():
    par = {cle(DEP): None}; f = deque([DEP])
    while f:
        e = f.popleft()
        if e[0] == BUT0 and e[1] == BUT1:
            ch, k = [], cle(e)
            while par[k]: k, m = par[k]; ch.append(m)
            return ch[::-1], len(par)
        for m, n in coups(e):
            k = cle(n)
            if k not in par: par[k] = (cle(e), m); f.append(n)
    return None, len(par)

def deplacer_pile(n, places):
    """plus petit nombre de coups pour porter une pile de n cartes sur une place
    vide, avec `places` places vides en tout ; None si c'est impossible"""
    base = tuple(str(x) + "X" for x in range(9, n, -1))     # la pile repose sur des cartes plus hautes
    pile = tuple(str(x) + "Y" for x in range(n, 0, -1))
    dep = (base + pile,) + ((),) * places
    vus = {dep: 0}; f = deque([dep])
    while f:
        e = f.popleft()
        if e[0] == base and pile in e[1:]: return vus[e]
        for _, s in coups(e):
            s = (s[0],) + tuple(sorted(s[1:]))
            if s not in vus: vus[s] = vus[e] + 1; f.append(s)
    return None

if __name__ == "__main__":
    print("Ses remarques de l'enonce (une pile portee sur une place vide) :")
    for k in (4, 3, 2):
        print("   %d places vides : " % k + ", ".join(
            "%d cartes en %s" % (n, deplacer_pile(n, k) if deplacer_pile(n, k) is not None else "impossible") for n in range(1, 7)))
    assert deplacer_pile(4, 4) == 7 and deplacer_pile(4, 3) == 9
    assert deplacer_pile(2, 2) and deplacer_pile(3, 2) is None
    t = time.time(); ch, nb = plus_courte()
    print("\nPartie la plus courte : %d coups (%d positions examinees, %.0f s) ; Dudeney : 62"
          % (len(ch), nb, time.time() - t))
    txt = " ; ".join("%s sur %s" % (c, cible or "place vide") for c, cible in ch)
    print(txt)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "partie_56.txt"), "w").write(txt + "\n")
    assert len(ch) == 56
