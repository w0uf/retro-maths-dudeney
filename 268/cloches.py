# -*- coding: utf-8 -*-
"""n° 268 THE PEAL OF BELLS — Dudeney, Amusements in Mathematics (1917).

Une sonnerie « juste » de n cloches :
  (a) chaque permutation des n cloches sonnee une fois et une seule ;
  (b) aucune cloche ne se deplace de plus d'une place a la fois ;
  (c) aucune cloche ne reste plus de deux coups de suite a la premiere
      place ni a la derniere ;
  (d) le dernier changement doit se raccorder au premier (la sonnerie boucle).
"""
import sys
from itertools import permutations
sys.setrecursionlimit(100000)

SIENNE = """1 2 3 4/2 1 4 3/2 4 1 3/4 2 3 1/4 3 2 1/3 4 1 2/3 1 4 2/1 3 2 4/
3 1 2 4/1 3 4 2/1 4 3 2/4 1 2 3/4 2 1 3/2 4 3 1/2 3 4 1/3 2 1 4/
2 3 1 4/3 2 4 1/3 4 2 1/4 3 1 2/4 1 3 2/1 4 2 3/1 2 4 3/2 1 3 4"""
SIENNE = [tuple(int(x) for x in l.split()) for l in SIENNE.replace("\n","").split("/")]

def changements(n):
    """les facons de passer d'une rangee a la suivante : produits d'echanges
    de places voisines, deux a deux disjoints, au moins un echange"""
    out = []
    def rec(i, pris):
        if i >= n-1:
            if pris: out.append(tuple(pris))
            return
        rec(i+1, pris)                      # la place i ne bouge pas
        rec(i+2, pris + [i])                # on echange les places i et i+1
    rec(0, [])
    return out

def applique(p, ch):
    q = list(p)
    for i in ch: q[i], q[i+1] = q[i+1], q[i]
    return tuple(q)

def verifie(peal, n):
    ok = {}
    ok["toutes les permutations, une fois chacune"] = (
        sorted(peal) == sorted(permutations(range(1, n+1))))
    CH = set(changements(n))
    ok["aucune cloche ne bouge de plus d'une place"] = all(
        any(applique(peal[i], c) == peal[(i+1) % len(peal)] for c in CH)
        for i in range(len(peal)))
    ok["le dernier changement se raccorde au premier"] = any(
        applique(peal[-1], c) == peal[0] for c in CH)
    for place, nom in ((0, "premiere"), (n-1, "derniere")):
        col = [p[place] for p in peal]
        run, maxi = 1, 1
        for i in range(1, 2*len(col)):
            if col[i % len(col)] == col[(i-1) % len(col)]: run += 1; maxi = max(maxi, run)
            else: run = 1
        ok["pas plus de deux coups de suite a la %s place" % nom] = maxi <= 2
    return ok

print("=== La sonnerie imprimee par Dudeney, pour quatre cloches ===")
for k, v in verifie(SIENNE, 4).items():
    print("   %-48s : %s" % (k, "oui" if v else "NON"))

# --- combien de sonneries justes pour quatre cloches ? ------------------
def cherche(n, toutes=True, limite=None):
    CH = changements(n)
    depart = tuple(range(1, n+1))
    sols = []
    vu = {depart}
    chemin = [depart]
    def run_ok(place):
        col = [p[place] for p in chemin]
        return not (len(col) >= 3 and col[-1] == col[-2] == col[-3])
    def rec():
        if limite is not None and len(sols) >= limite: return
        if len(chemin) == len(vu) == __import__("math").factorial(n):
            if any(applique(chemin[-1], c) == depart for c in CH):
                col0 = [p[0] for p in chemin]; coln = [p[n-1] for p in chemin]
                for col in (col0, coln):
                    if col[-2] == col[-1] == col[0] or col[-1] == col[0] == col[1]:
                        return
                sols.append(list(chemin))
            return
        for c in CH:
            q = applique(chemin[-1], c)
            if q in vu: continue
            chemin.append(q); vu.add(q)
            if run_ok(0) and run_ok(n-1): rec()
            chemin.pop(); vu.discard(q)
            if limite is not None and len(sols) >= limite: return
    rec()
    return sols

s4 = cherche(4)
print("\n=== Toutes les sonneries justes de quatre cloches ===")
print("   partant de 1 2 3 4 :", len(s4), "sonneries")
print("   la sienne y figure :", SIENNE in s4)

# --- combien sont essentiellement differentes ? ------------------------
def renverse(p):
    """la sonnerie lue a l'envers, ramenee au depart 1 2 3 4"""
    q = list(reversed(p))
    i = q.index(tuple(range(1, len(p[0])+1)))
    return q[i:] + q[:i]
classes = set()
for s in s4:
    classes.add(min(tuple(s), tuple(renverse(s))))
print("   a lecture inverse pres :", len(classes))
miroir = lambda p: tuple(tuple(reversed(r)) for r in p)
def norm(s):
    cands = []
    for t in (tuple(s), tuple(renverse(s))):
        for u in (t, miroir(t)):
            v = list(u)
            i = v.index(tuple(range(1, len(s[0])+1)))
            cands.append(tuple(v[i:] + v[:i]))
    return min(cands)
print("   en identifiant aussi le miroir des places :", len({norm(s) for s in s4}))

# --- cinq cloches : voir cloches5sym.py et verifie.py ---------------------
# Une recherche aveugle comme celle-ci, lancee sur cinq cloches, ne trouve rien
# en plusieurs milliards de noeuds ; il faut imposer la symetrie des vraies
# methodes de sonnerie (cloches5sym.py).
assert all(verifie(SIENNE, 4).values()) and SIENNE in s4
assert len(s4) == 24 and len(classes) == 12 and len({norm(s) for s in s4}) == 8
