#!/usr/bin/env python3
"""Rétro Math's — n° 301 THE EIGHT STARS (Dudeney, 1917). Huit étoiles (dames) sans
alignement, cases des deux grandes diagonales interdites, une étoile imposée.
    python3 etoiles.py   (instantané)"""
from itertools import permutations
from collections import Counter
N = 8
S = [p for p in permutations(range(N)) if all(abs(p[i]-p[j]) != j-i for i in range(N) for j in range(i+1, N))]
print("solutions des huit dames :", len(S))
def images(p):
    pts = [(l, p[l]) for l in range(N)]
    T = [lambda l,c:(l,c), lambda l,c:(c,N-1-l), lambda l,c:(N-1-l,N-1-c), lambda l,c:(N-1-c,l),
         lambda l,c:(l,N-1-c), lambda l,c:(N-1-l,c), lambda l,c:(c,l), lambda l,c:(N-1-c,N-1-l)]
    out = set()
    for t in T:
        q = [0]*N
        for l, c in pts:
            a, b = t(l, c); q[a] = b
        out.add(tuple(q))
    return out
fam = {}
for p in S: fam.setdefault(min(images(p)), set()).add(p)
print("familles :", len(fam), "tailles", dict(Counter(len(v) for v in fam.values())))
diag = lambda p: sum(1 for l in range(N) if p[l] == l or p[l] == N-1-l)
print("solutions selon le nombre d'étoiles sur les grandes diagonales :", dict(sorted(Counter(diag(p) for p in S).items())))
L = [p for p in S if diag(p) == 0]
print("hors diagonales :", len(L), "| familles :", [(''.join(str(c+1) for c in f), len(v)) for f, v in fam.items() if diag(f) == 0])
avec = [p for p in L if p[1] == 7]          # l'étoile imposée : 2e rangée, 8e colonne
print("avec l'étoile de la gravure :", [''.join(str(c+1) for c in p) for p in avec])
print("sa figure 1 = 58417263 ?", (4,7,3,0,6,1,5,2) in avec, "| sa figure 2 = 35281746 :", (2,4,1,7,0,6,3,5) in L, len(images((2,4,1,7,0,6,3,5))))
occ = Counter((l, p[l]) for p in L for l in range(N))
print("nombre de solutions permises passant par chaque case :")
for l in range(N): print("  ", ' '.join(str(occ.get((l, c), 0)) if not (l == c or l + c == N-1) else '#' for c in range(N)))
print("cases qui fixent une solution unique :", sum(1 for v in occ.values() if v == 1), "; cases à 2 :", sum(1 for v in occ.values() if v == 2), "; cases libres jamais utilisées :", 64 - 16 - len(occ))
# autres tailles : dames hors des deux diagonales
AUTRES = []
for n in range(4, 11):
    c = 0
    def pose(l, cols, d1, d2):
        global c
        if l == n: c += 1; return
        for k in range(n):
            if k == l or k + l == n-1: continue
            if k in cols or (l-k) in d1 or (l+k) in d2: continue
            pose(l+1, cols|{k}, d1|{l-k}, d2|{l+k})
    pose(0, frozenset(), frozenset(), frozenset())
    print("damier", n, ": solutions hors diagonales", c); AUTRES.append(c)

# --- ce que dit l'article
assert len(S) == 92 and avec == [(4, 7, 3, 0, 6, 1, 5, 2)]          # une seule solution : sa figure 1
assert len(L) == 12 and sorted(len(v) for f, v in fam.items() if diag(f) == 0) == [4, 8]
assert dict(Counter(diag(p) for p in S)) == {0: 12, 1: 32, 2: 48}     # aucune n'en pose trois
symetriques = [f for f, v in fam.items() if len(v) < 8]
assert len(fam) == 12 and len(symetriques) == 1 and (2, 4, 1, 7, 0, 6, 3, 5) in fam[symetriques[0]]
assert AUTRES == [2, 0, 4, 0, 12, 8, 12]
# temoins : une solution des huit dames qui touche une diagonale, et une disposition qui s'attaque, sont refusees
assert diag((0, 4, 7, 5, 2, 6, 1, 3)) > 0 and (0, 4, 7, 5, 2, 6, 1, 3) in S and (0, 4, 7, 5, 2, 6, 1, 3) not in L
assert (0, 1, 2, 3, 4, 5, 6, 7) not in S
print("controles : tout est conforme (temoins refuses)")
