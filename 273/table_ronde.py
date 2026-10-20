#!/usr/bin/env python3
"""Rétro Math's — n° 273 THE ROUND TABLE (Dudeney, 1917).
n personnes autour d'une table, (n − 1)(n − 2)/2 repas, et personne n'est jamais assis deux fois entre les deux
mêmes voisins. Contrôle des tables de Dudeney pour 4, 5 et 6, et recherche exhaustive des emplois du temps.
    python3 table_ronde.py   (environ 1 min)"""
import itertools
from collections import Counter
print("=== 273. Table ronde ===")
def triplets(cycle):
    n = len(cycle)
    return [(cycle[i], frozenset((cycle[i - 1], cycle[(i + 1) % n]))) for i in range(n)]
def valide(tables, n):
    vus = Counter(t for c in tables for t in triplets(c))
    return len(tables) == (n - 1) * (n - 2) // 2 and len(vus) == n * (n - 1) * (n - 2) // 2 and set(vus.values()) == {1}
D = {4: ["1234", "1342", "1423"],
     5: ["12345", "12453", "12534", "13254", "14235", "15243"],
     6: ["123645", "134256", "145362", "156423", "162534", "124563", "135624", "146235", "152346", "163452"]}
for n, t in D.items():
    print("   tables de Dudeney pour %d : %s" % (n, "justes" if valide([[int(x) for x in c] for c in t], n) else "FAUSSES"))
def cycles(n):
    for p in itertools.permutations(range(2, n + 1)):
        if p[0] < p[-1]: yield (1,) + p
def chercher(n, tout=False):
    cs = list(cycles(n)); tr = [frozenset(triplets(c)) for c in cs]
    but = (n - 1) * (n - 2) // 2; sols = []
    def rec(debut, pris, vus):
        if len(pris) == but:
            sols.append([cs[i] for i in pris]); return not tout
        for i in range(debut, len(cs)):
            if not (tr[i] & vus):
                if rec(i + 1, pris + [i], vus | tr[i]): return True
        return False
    rec(0, [], frozenset()); return len(cs), sols
R = {}
for n in (4, 5, 6):
    nb, sols = chercher(n, tout=True); R[n] = (nb, len(sols))
    print("   n=%d : %d tablees possibles, %d repas, %d emplois du temps" % (n, nb, (n-1)*(n-2)//2, len(sols)))
    print("      le premier :", " | ".join(" ".join(map(str, c)) for c in sols[0]))
    assert all(valide(s, n) for s in sols)
nb, sols = chercher(7); R7 = (nb, valide(sols[0], 7))
print("   n=7 : %d tablees, premier emploi du temps (%d repas) valide : %s" % (nb, len(sols[0]), valide(sols[0], 7)))
_, s5 = chercher(5, tout=True)
print("   n=5 : les deux emplois du temps se partagent les 12 tablees :", len(set(s5[0]) | set(s5[1])) == 12 and not set(s5[0]) & set(s5[1]))
print("      le second :", " | ".join(" ".join(map(str, c)) for c in s5[1]))
for n in (5, 6, 13): print("   n=%d : triplets %d, par repas %d, repas %d" % (n, n*(n-1)*(n-2)//2, n, (n-1)*(n-2)//2))

# --- contrôles
assert all(valide([[int(x) for x in c] for c in D[n]], n) for n in D)                 # ses tables pour 4, 5, 6
assert R == {4: (3, 1), 5: (12, 2), 6: (60, 36)} and R7 == (360, True)
assert len(set(s5[0]) | set(s5[1])) == 12 and not set(s5[0]) & set(s5[1])
assert 13 * 12 * 11 // 2 == 858 and 12 * 11 // 2 == 66                                 # le cas de 13 : 66 repas
# témoin : sa table pour 5 avec deux repas identiques est refusée
faux = [[int(x) for x in c] for c in D[5]]; faux[1] = faux[0]
assert not valide(faux, 5)
print("contrôles : tout est conforme (témoins refusés)")
