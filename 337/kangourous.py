#!/usr/bin/env python3
"""Rétro Math's — n° 337 THE FOUR KANGAROOS (Dudeney, 1917). Quatre cavaliers aux quatre coins ;
chacun fait un circuit fermé de 16 sauts ; aucune case visitée deux fois ; aucun ne franchit la médiane horizontale.
Chaque moitié 4×8 doit donc se partager en deux circuits de 16 cases, un par coin.
    python3 kangourous.py   (environ 3 s)"""
import sys
from collections import Counter
SAUTS = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
def graphe(cases):
    S = set(cases); return {x: [(x[0]+a, x[1]+b) for a, b in SAUTS if (x[0]+a, x[1]+b) in S] for x in S}
def circuits_par(V, depart, n):
    """ensembles de n cases portant un circuit fermé passant par `depart` → nombre de circuits (non orientés)"""
    res = Counter()
    def rec(x, vus, k):
        if k == n:
            if depart in V[x]: res[frozenset(vus)] += 1
            return
        for y in V[x]:
            if y not in vus: vus.add(y); rec(y, vus, k+1); vus.discard(y)
    rec(depart, {depart}, 1)
    return {k: v // 2 for k, v in res.items()}
def partage(H, L, c1, c2, n):
    cases = [(r, c) for r in range(H) for c in range(L)]; V = graphe(cases); tout = frozenset(cases)
    A = circuits_par(V, c1, n); B = circuits_par(V, c2, len(cases) - n)
    sol = [(a, A[a], B[tout - a]) for a in A if (tout - a) in B]
    return A, B, sol
A, B, sol = partage(4, 8, (0, 0), (0, 7), 16)
print("moitié 4×8 : ensembles de 16 cases portant un circuit par le coin gauche :", len(A), "| circuits :", sum(A.values()))
print("partages de la moitié en deux circuits de 16 (un par coin) :", len(sol), "| en comptant les tracés :", sum(x*y for _, x, y in sol))
for a, x, y in sol:
    print("   circuits gauche/droite :", x, y, "| symétrique gauche-droite :", frozenset((r, 7-c) for r, c in a) == frozenset((r, c) for r in range(4) for c in range(8)) - a)
    for r in range(4): print("     ", ''.join('G' if (r, c) in a else 'D' for c in range(8)))
n1 = sum(x*y for _, x, y in sol)
print("solutions pour l'échiquier entier (haut et bas indépendants) : partages", len(sol)**2, "| tracés", n1*n1)
# la « meilleure idée » qu'il écarte : chaque kangourou dans son quart 4×4
print("quart 4×4 : circuit fermé de 16 par le coin :", len(circuits_par(graphe([(r, c) for r in range(4) for c in range(4)]), (0, 0), 16)))
# et sans la contrainte de la médiane : partages de l'échiquier en 4 circuits de 16, un par coin — trop vaste ; on donne la moitié verticale

# --- ce que dit l'article
assert len(A) == 55123 and len(sol) == 1 and sol[0][1:] == (8, 8) and n1 * n1 == 4096
motif = ["GDGDGDGD", "GDGDGDGD", "DGDGDGDG", "DGDGDGDG"]
assert [''.join('G' if (r, c) in sol[0][0] else 'D' for c in range(8)) for r in range(4)] == motif
# temoins : le quart 4x4 ne porte aucun circuit (son « meilleure idee » ecartee) ; un circuit de 16 sur
# le domaine trouve est accepte, et le meme domaine avec deux cases echangees avec le voisin est refuse
assert len(circuits_par(graphe([(r, c) for r in range(4) for c in range(4)]), (0, 0), 16)) == 0
G = sol[0][0]; faux = (G - {(0, 2)}) | {(0, 1)}
assert G in A and faux not in A
print("controles : tout est conforme (temoins refuses)")
