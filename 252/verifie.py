#!/usr/bin/env python3
"""N° 252 A PUZZLE FOR MOTORISTS : contrôle indépendant des réseaux, sans solveur.
Huit voitures vont chacune de sa maison à son église sur la grille des rues (18 × 11 carrefours, relevée sur la figure du livre) ;
deux trajets ne doivent jamais passer par le même carrefour. On compte les tronçons d'un carrefour au suivant.
    python3 verifie.py                 contrôle le réseau du livre (159), reseau_157.json, et la borne 121 de bornes_4.json"""
import json, os
W, H = 18, 11
M = dict(A=((12, 0), (12, 9)), B=((2, 2), (2, 10)), C=((7, 2), (17, 2)), D=((15, 2), (15, 10)), E=((8, 3), (17, 3)), F=((0, 7), (14, 7)), G=((0, 5), (12, 5)), H=((5, 0), (5, 9)))

def deplie(coins):
    """Liste des carrefours d'un trajet donné par ses coins."""
    n = [coins[0]]
    for (a, b), (c, d) in zip(coins, coins[1:]):
        assert (a == c) != (b == d), "segment en biais"
        m = abs(c - a) + abs(d - b); n += [(a + (c - a) // m * i, b + (d - b) // m * i) for i in range(1, m + 1)]
    return n

def controle(nom, trajets):
    vus, tot = {}, 0
    for k, p in sorted(trajets.items()):
        p = [tuple(v) for v in p]
        assert {p[0], p[-1]} == set(M[k]), "%s ne relie pas sa maison à son église" % k
        for a, b in zip(p, p[1:]): assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, "%s saute un carrefour" % k
        for v in p:
            assert 0 <= v[0] < W and 0 <= v[1] < H, "%s sort de la carte" % k
            assert v not in vus, "%s et %s se croisent en %s" % (k, vus[v], v)
            vus[v] = k
        tot += len(p) - 1
    print(nom, ": trajets valides, aucun carrefour commun ; total", tot, "tronçons ;", " ".join("%s %d" % (k, len(p) - 1) for k, p in sorted(trajets.items())))
    return tot

livre = dict(A=[(12,0),(6,0),(6,4),(9,4),(9,3),(14,3),(14,5),(16,5),(16,9),(12,9)], B=[(2,2),(2,10)], C=[(7,2),(7,1),(13,1),(13,0),(17,0),(17,2)], D=[(15,2),(15,4),(17,4),(17,10),(15,10)],
             E=[(8,3),(8,2),(14,2),(14,1),(16,1),(16,3),(17,3)], F=[(0,7),(1,7),(1,1),(3,1),(3,7),(14,7)], G=[(0,5),(0,0),(4,0),(4,6),(11,6),(11,5),(12,5)], H=[(5,0),(5,5),(10,5),(10,4),(13,4),(13,6),(15,6),(15,8),(5,8),(5,9)])
livre = {k: deplie(v) for k, v in livre.items()}
ici = os.path.dirname(os.path.abspath(__file__))
assert controle("réseau du livre", livre) == 159
assert controle("réseau trouvé  ", json.load(open(os.path.join(ici, "reseau_157.json")))) == 157
print("plus courts trajets, chacun seul :", sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in M.values()))

# témoin : on fait passer B par un carrefour de F ; le contrôle doit refuser
t = dict(livre); t["B"] = deplie([(2, 2), (2, 7), (1, 7), (1, 8), (2, 8), (2, 10)])
try: controle("témoin", t); print("ERREUR : le témoin fautif est accepté")
except AssertionError as e: print("témoin fautif refusé :", e)

# borne inférieure : chaque groupe résolu à l'optimum (true) minore sa part dans tout réseau valide
b = json.load(open(os.path.join(ici, "bornes_4.json")))
for g in ("ADEF", "BCGH"): assert b[g][1], g
print("borne inférieure : ADEF", b["ADEF"][0], "+ BCGH", b["BCGH"][0], "=", b["ADEF"][0] + b["BCGH"][0])
