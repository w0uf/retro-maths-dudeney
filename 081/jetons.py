#!/usr/bin/env python3
"""N° 81 THE NINE COUNTERS : les chiffres 1 à 9, chacun une fois. D'un côté un nombre de trois chiffres multiplié par un nombre
de deux chiffres, de l'autre deux nombres de deux chiffres multipliés entre eux : les deux produits doivent être égaux.
Quel est le plus grand produit possible ? Le livre répond 5 568 (174 × 32 = 96 × 58).
    python3 jetons.py"""
from itertools import permutations
from collections import defaultdict

# méthode 1 : les 9! = 362 880 façons de poser les jetons
sol = defaultdict(set)
for p in permutations("123456789"):
    a, b, c, d = int("".join(p[0:3])), int("".join(p[3:5])), int("".join(p[5:7])), int("".join(p[7:9]))
    if a * b == c * d: sol[a * b].add((a, b, tuple(sorted((c, d)))))

# méthode 2, écrite autrement : pour chaque paire de deux chiffres, chercher le produit comme (trois chiffres) × (deux chiffres)
sol2 = defaultdict(set)
for c in range(12, 99):
    for d in range(c + 1, 99):
        n = c * d
        for b in range(12, 99):
            if n % b == 0 and 100 <= n // b <= 999:
                s = "%d%d%d%d" % (n // b, b, c, d)
                if sorted(s) == list("123456789"): sol2[n].add((n // b, b, (c, d)))
assert sol == sol2, "les deux méthodes ne s'accordent pas"

print(len(sol), "produits possibles, du plus grand au plus petit :")
for n in sorted(sol, reverse=True):
    print("  %5d =" % n, " ; ".join("%d × %d = %d × %d" % (a, b, c, d) for a, b, (c, d) in sorted(sol[n])))
rang = sorted(sol, reverse=True).index(5568) + 1
print("la réponse du livre, 5 568, arrive au rang", rang, "; le maximum est", max(sol))
assert 5568 in sol and (174, 32, (58, 96)) in sol[5568]   # témoin : la solution du livre doit être trouvée
