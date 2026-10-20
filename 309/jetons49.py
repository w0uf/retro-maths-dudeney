#!/usr/bin/env python3
"""Rétro Math's — n° 309 THE FORTY-NINE COUNTERS (Dudeney, 1917). 49 jetons A1…G7 en carré : aucune lettre ni
aucun chiffre deux fois sur une même rangée, colonne ou diagonale (au sens de l'échiquier).
Chaque lettre occupe donc une solution des « sept dames », et de même chaque chiffre.
    python3 jetons49.py   (instantané)"""
from itertools import permutations
import sys
def dames(n):
    return [p for p in permutations(range(n)) if all(abs(p[i]-p[j]) != j-i for i in range(n) for j in range(i+1, n))]
def partitions(n):
    """toutes les façons de couvrir le damier par n solutions des n dames deux à deux disjointes"""
    S = dames(n); masks = [sum(1 << (r*n+p[r]) for r in range(n)) for p in S]
    par_case = {}
    for i, m in enumerate(masks):
        par_case.setdefault((m & -m).bit_length() - 1, None)
    tout = (1 << n*n) - 1; res = []
    contient = [[i for i, m in enumerate(masks) if m >> c & 1] for c in range(n*n)]
    def rec(occ, choix):
        if occ == tout: res.append(tuple(choix)); return
        c = (~occ & tout); c = (c & -c).bit_length() - 1          # première case libre
        for i in contient[c]:
            if not masks[i] & occ: choix.append(i); rec(occ | masks[i], choix); choix.pop()
    rec(0, [])
    return S, masks, res
sol = """A1 B2 C3 D4 E5 F6 G7
F4 G5 A6 B7 C1 D2 E3
D7 E1 F2 G3 A4 B5 C6
B3 C4 D5 E6 F7 G1 A2
G6 A7 B1 C2 D3 E4 F5
E2 F3 G4 A5 B6 C7 D1
C5 D6 E7 F1 G2 A3 B4"""
G = [l.split() for l in sol.split("\n")]
def valide(G):
    n = len(G)
    for k in (0, 1):
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        if (a, b) < (c, d) and G[a][b][k] == G[c][d][k] and (a == c or b == d or abs(a-c) == abs(b-d)): return False, (a, b, c, d, k)
    return len({x for l in G for x in l}) == n*n, None
print("sa disposition :", valide(G))
# structure de sa solution : d'une rangée à la suivante, de combien de cases glisse la lettre A ? le chiffre 1 ?
posA = [l.index(next(x for x in l if x[0] == 'A')) for l in G]; pos1 = [l.index(next(x for x in l if x[1] == '1')) for l in G]
print("colonne de A rangée par rangée :", posA, "| colonne de 1 :", pos1)
NB = {}
for n in (4, 5, 6, 7, 8):
    S, masks, res = partitions(n); NB[n] = len(res)
    print("damier %d×%d : %d solutions des %d dames ; partages complets du damier en %d solutions disjointes : %d" % (n, n, len(S), n, n, len(res)), flush=True)
    if n in (5, 7) and res:
        # un partage = un carré « lettres » (à l'ordre des lettres près). Carrés complets = couples de partages orthogonaux.
        def grille(part):
            g = [[None]*n for _ in range(n)]
            for k, i in enumerate(part):
                for r in range(n): g[r][S[i][r]] = k
            return g
        gr = [grille(p) for p in res]
        orth = 0; couples = []
        for a in range(len(gr)):
            for b in range(len(gr)):
                if len({(gr[a][r][c], gr[b][r][c]) for r in range(n) for c in range(n)}) == n*n: orth += 1; couples.append((a, b))
        NB[(n, 'couples')] = orth
        print("   couples (partage des lettres, partage des chiffres) donnant 49 jetons tous différents :" if n == 7 else "   couples orthogonaux :", orth)
        from math import factorial
        print("   → dispositions complètes en comptant les façons de nommer lettres et chiffres :", orth, "×", factorial(n), "×", factorial(n), "=", orth * factorial(n)**2)
        if n == 7:
            # la sienne : quels partages ?
            def part_de(G, k):
                d = {}
                for r in range(n):
                    for c in range(n): d.setdefault(G[r][c][k], []).append((r, c))
                return frozenset(frozenset(v) for v in d.values())
            ens = [frozenset(frozenset((r, S[i][r]) for r in range(n)) for i in p) for p in res]
            print("   sa disposition : partage des lettres n°", ens.index(part_de(G, 0)), "| partage des chiffres n°", ens.index(part_de(G, 1)), "| couple présent :", (ens.index(part_de(G, 0)), ens.index(part_de(G, 1))) in couples)
            for p in res: print("     partage : décalages de colonne d'une rangée à la suivante →", sorted({tuple((S[i][r+1]-S[i][r]) % n for r in range(n-1)) for i in p})[:2])

# --- ce que dit l'article
assert valide(G)[0] and NB[7] == 4 and NB[(7, 'couples')] == 12
assert (NB[4], NB[5], NB[6], NB[8], NB[(5, 'couples')]) == (0, 2, 0, 0, 2)
assert [(posA[r+1] - posA[r]) % 7 for r in range(6)] == [2]*6 and [(pos1[r+1] - pos1[r]) % 7 for r in range(6)] == [4]*6
# temoin : deux jetons de la premiere colonne echanges (A1 et F4) doivent etre refuses
T2 = [l[:] for l in G]; T2[0][0], T2[1][0] = T2[1][0], T2[0][0]
assert not valide(T2)[0]
print("controles : tout est conforme (temoins refuses)")
