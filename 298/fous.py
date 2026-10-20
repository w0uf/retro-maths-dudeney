#!/usr/bin/env python3
"""Rétro Math's — n° 297 BISHOPS—UNGUARDED et n° 298 BISHOPS—GUARDED (Dudeney, 1917).
Le moins de fous possible pour que toute case soit occupée ou attaquée ; puis la même chose, chaque fou étant gardé.
Les pièces font écran. On traite une couleur de cases à la fois (les deux sont indépendantes).
    python3 fous.py   (environ 3 s)"""
from itertools import combinations
from collections import Counter
N = 8
def cases(couleur): return [(r, c) for r in range(N) for c in range(N) if (r + c) % 2 == couleur]
def attaque(s, occ):
    out = set()
    for dr, dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
        r, c = s[0]+dr, s[1]+dc
        while 0 <= r < N and 0 <= c < N:
            out.add((r, c))
            if (r, c) in occ: break
            r += dr; c += dc
    return out
def analyse(couleur, k):
    C = cases(couleur); tout = set(C); dom = []; gard = []
    for S in combinations(C, k):
        occ = set(S); A = set()
        att = {s: attaque(s, occ) for s in S}
        for s in S: A |= att[s]
        if (A | occ) == tout:
            dom.append(S)
            if all(any(s in att[t] for t in S if t != s) for s in S): gard.append(S)
    return dom, gard
print("portée d'un fou seul selon sa case :", sorted(Counter(len(attaque((r, c), set())) for r in range(N) for c in range(N)).items()))
res = {}
for k in range(1, 7):
    d0, g0 = analyse(0, k); d1, g1 = analyse(1, k)
    res[k] = (d0, g0, d1, g1)
    print("%d fous sur une couleur : couvrantes %d / %d ; couvrantes et toutes gardées %d / %d" % (k, len(d0), len(d1), len(g0), len(g1)), flush=True)
    if g0 and k >= 5: break
k1 = min(k for k in res if res[k][0]); k2 = min(k for k in res if res[k][1])
print("n° 297 : minimum par couleur", k1, "→", 2*k1, "fous ; dispositions :", len(res[k1][0]), "×", len(res[k1][2]), "=", len(res[k1][0]) * len(res[k1][2]))
nong = [S for S in res[k1][0] if not any(t in attaque(s, set(S)) for s in S for t in S if t != s)]
nong1 = [S for S in res[k1][2] if not any(t in attaque(s, set(S)) for s in S for t in S if t != s)]
print("   dont aucun fou gardé :", len(nong), "×", len(nong1), "=", len(nong) * len(nong1))
print("n° 298 : minimum par couleur", k2, "→", 2*k2, "fous ; dispositions :", len(res[k2][1]), "×", len(res[k2][3]), "=", len(res[k2][1]) * len(res[k2][3]))
# ses deux diagrammes (rangée depuis le haut, colonne)
d297 = [(3, c) for c in range(8)]
d298 = [(3,1),(3,2),(3,3),(3,5),(3,6),(4,1),(4,2),(4,3),(4,5),(4,6)]
def controle(S):
    occ = set(S); att = {s: attaque(s, occ) for s in S}; A = set(S)
    for s in S: A |= att[s]
    return len(A) == 64, all(any(s in att[t] for t in S if t != s) for s in S), not any(s in att[t] for s in S for t in S if t != s)
print("diagramme 297 (huit fous sur la 4e rangée) : couvre, tous gardés, aucun gardé =", controle(d297))
print("diagramme 298 (lecture du schéma en texte) : couvre, tous gardés, aucun gardé =", controle(d298), len(d298))
# fous alignés sur une rangée : lesquelles conviennent ?
print("huit fous sur une même rangée, couvre ? par rangée :", [controle([(r, c) for c in range(8)])[0] for r in range(8)])
# autres tailles
for n in range(2, 9):
    N = n; best = None
    for k in range(1, 6):
        if analyse(0, k)[0]: best = k; break
    b1 = next(k for k in range(1, 6) if analyse(1, k)[0]) if n > 1 else 0
    print("damier", n, ": minimum de fous couvrants =", best + b1)
    assert best + b1 == n
N = 8
# --- ce que disent les articles
from collections import Counter as _C
assert sorted(_C(len(attaque((r, c), set())) for r in range(8) for c in range(8)).items()) == [(7, 28), (9, 20), (11, 12), (13, 4)]
assert (k1, k2) == (4, 5) and not res[3][0] and not res[3][2] and not res[4][1]   # 8 fous ; 10 fous gardes
assert len(res[4][0]) * len(res[4][2]) == 11664 and len(res[5][1]) * len(res[5][3]) == 10816
assert controle(d297)[0] and controle(d298)[:2] == (True, True)
assert [controle([(r, c) for c in range(8)])[0] for r in range(8)] == [False, False, False, True, True, False, False, False]
# sa variante du 298 : les deux fous centraux du groupe de six (colonne c), « qui ne servent qu'a proteger » : le haut monte d'une case, le bas descend d'une case
var = [x for x in d298 if x[1] != 2] + [(2, 2), (5, 2)]
assert controle(var)[:2] == (True, True)
# temoins : son diagramme prive d'un fou ne couvre plus ; les huit fous du 297 ne sont pas tous gardes
assert not any(controle([x for x in d298 if x != y])[:2] == (True, True) for y in d298)
assert controle(d297)[1] is False
print("controles : tout est conforme (temoins refuses)")
