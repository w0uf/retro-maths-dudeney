#!/usr/bin/env python3
"""N° 244 THE FIFTEEN TURNINGS : rejeu indépendant, en Python, des trajets trouvés par verif_244.c.
Coordonnées (colonne, rangée), rangée 0 en haut ; la ville noire est (0, 4).
    python3 rejeu.py            rejoue l'exemple, le corrigé du livre et les 528 trajets de trajets_76.txt"""
import collections, os

def rejeu(pts):
    """Longueur du trajet ; lève une erreur si une règle n'est pas respectée."""
    assert pts[0] == (0, 4), "le trajet ne part pas de la ville noire"
    assert all(0 <= x <= 7 for p in pts for x in p), "sortie de la carte"
    routes, total = set(), 0
    for (c, r), (c2, r2) in zip(pts, pts[1:]):
        assert (c == c2) != (r == r2), "segment ni horizontal ni vertical"
        n = abs(c2 - c) + abs(r2 - r); dc, dr = (c2 - c) // n, (r2 - r) // n
        for i in range(n):
            e = frozenset(((c + i*dc, r + i*dr), (c + (i+1)*dc, r + (i+1)*dr)))
            assert e not in routes, "route reprise %s" % sorted(e)
            routes.add(e)
        total += n
    for a, b, d in zip(pts, pts[1:], pts[2:]):
        assert (a[0] == b[0]) != (b[0] == d[0]), "pas un tournant à angle droit"
    return total

def tournants(pts): return len(pts) - 2

exemple = [(0,4),(7,4),(7,0),(0,0),(0,7),(6,7),(6,1)]
livre = [(0,4),(7,4),(7,3),(0,3),(0,5),(6,5),(6,1),(1,1),(1,6),(5,6),(5,2),(2,2),(2,7),(4,7),(4,0),(3,0),(3,7)]
print("exemple de l'énoncé :", rejeu(exemple), "miles,", tournants(exemple), "tournants")
print("corrigé du livre    :", rejeu(livre), "miles,", tournants(livre), "tournants")

# témoin : un trajet fautif doit être refusé
try:
    rejeu(livre[:-1] + [(3, 1), (6, 1)]); print("ERREUR : le témoin fautif est accepté")
except AssertionError as e:
    print("témoin fautif refusé :", e)

ici = os.path.dirname(os.path.abspath(__file__))
vus, n = set(), collections.Counter()
for l in open(os.path.join(ici, "trajets_76.txt")):
    if "=" not in l or "," not in l: continue
    gauche, annonce = l.split("=")
    pts = tuple(tuple(map(int, x.split(","))) for x in gauche.split())
    assert rejeu(list(pts)) == int(annonce) == 76 and tournants(pts) <= 15
    vus.add(pts); n[tournants(pts)] += 1
print(len(vus), "trajets distincts de 76 miles, tous valides ; nombre de tournants :", dict(n))
print("ils finissent tous sur le bord du haut :", all(p[-1][1] == 0 for p in vus))
