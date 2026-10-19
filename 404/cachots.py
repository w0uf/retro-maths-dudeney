# -*- coding: utf-8 -*-
"""n° 404 THE SIBERIAN DUNGEONS — les 14 deplacements de Mr. Wotherspoon sont un minimum.
Seize prisonniers dans les cellules 1 a 16 doivent former un carre magique (somme
34) dans le carre de 4 sur 4 que font les cellules 17 a 24, 5 a 8 et 13 a 16. Un
deplacement : un homme va, par des cellules vides, a une cellule vide (portes
entre voisines de gauche, droite, dessus, dessous). Dudeney donne la solution en
14 deplacements d'un lecteur et la croit imbattable, sans le demontrer.
    python3 cachots.py          (une dizaine de secondes)"""
import time
from collections import Counter

CASE = {}
for i, n in enumerate(range(17, 21)): CASE[n] = (0, 4 + i)
for i, n in enumerate(range(21, 25)): CASE[n] = (1, 4 + i)
for i, n in enumerate(range(1, 9)): CASE[n] = (2, i)
for i, n in enumerate(range(9, 17)): CASE[n] = (3, i)
POS = {v: k for k, v in CASE.items()}
VOIS = {n: [m for m in CASE if abs(CASE[n][0] - CASE[m][0]) + abs(CASE[n][1] - CASE[m][1]) == 1] for n in CASE}
def accessible(occ, de, vers):
    if vers in occ: return False
    vu = {de}; pile = [de]
    while pile:
        x = pile.pop()
        for y in VOIS[x]:
            if y == vers: return True
            if y not in occ and y not in vu: vu.add(y); pile.append(y)
    return False
coups = [(8, 17), (16, 21), (6, 16), (14, 8), (5, 18), (4, 14), (3, 24), (11, 20), (10, 19), (2, 23), (13, 22), (12, 6), (1, 5), (9, 13)]
cellule = {h: h for h in range(1, 17)}; ok = True
for de, vers in coups:
    occ = set(cellule.values()); h = [x for x, c in cellule.items() if c == de][0]
    if not accessible(occ, de, vers): ok = False; print("  coup impossible :", de, vers)
    cellule[h] = vers
REGION = [[17, 18, 19, 20], [21, 22, 23, 24], [5, 6, 7, 8], [13, 14, 15, 16]]
inv = {c: h for h, c in cellule.items()}
M = [[inv.get(c) for c in ligne] for ligne in REGION]
def magique4(M):
    return all(sum(r) == 34 for r in M) and all(sum(M[i][j] for i in range(4)) == 34 for j in range(4)) and sum(M[i][i] for i in range(4)) == 34 and sum(M[i][3 - i] for i in range(4)) == 34
assert ok and magique4(M)
print("temoin : au depart, 16 peut-il gagner la cellule 21 ? (8 et 15 lui barrent la route)",
      accessible(set(range(1, 17)) - {16}, 16, 21))
assert not accessible(set(range(1, 17)) - {16}, 16, 21) and accessible(set(range(1, 17)) - {8}, 8, 17)
print("14 coups du corrigé permis :", ok, "; carré final :", M, "; magique :", magique4(M), "; figure du corrigé :", M == [[8, 5, 10, 11], [16, 13, 2, 3], [1, 12, 7, 14], [9, 4, 15, 6]])
# tous les carrés magiques d'ordre 4
def gen():
    TOUS = []; M = [0] * 16; used = set()
    def put(i, x):
        if x < 1 or x > 16 or x in used: return False
        M[i] = x; used.add(x); return True
    def rm(i): used.discard(M[i]); M[i] = 0
    R = range(1, 17)
    for a in R:
        put(0, a)
        for b in R:
            if not put(1, b): continue
            for c in R:
                if not put(2, c): continue
                if put(3, 34 - a - b - c):
                    for e in R:
                        if not put(4, e): continue
                        for i in R:
                            if not put(8, i): continue
                            if put(12, 34 - a - e - i):
                                for f in R:
                                    if not put(5, f): continue
                                    for k in R:
                                        if not put(10, k): continue
                                        if put(15, 34 - a - f - k):
                                            for g in R:
                                                if not put(6, g): continue
                                                if put(7, 34 - e - f - g):
                                                    if put(9, 34 - M[3] - M[6] - M[12]):
                                                        if put(11, 34 - i - M[9] - k):
                                                            if put(13, 34 - b - f - M[9]):
                                                                if put(14, 34 - c - g - k):
                                                                    if M[12] + M[13] + M[14] + M[15] == 34 and M[3] + M[7] + M[11] + M[15] == 34:
                                                                        TOUS.append(tuple(M))
                                                                    rm(14)
                                                                rm(13)
                                                            rm(11)
                                                        rm(9)
                                                    rm(7)
                                                rm(6)
                                            rm(15)
                                        rm(10)
                                    rm(5)
                                rm(12)
                            rm(8)
                        rm(4)
                    rm(3)
                rm(2)
            rm(1)
        rm(0)
    return TOUS
t = time.time(); TOUS = gen()
print("carrés magiques d'ordre 4 :", len(TOUS), "(%.0f s)" % (time.time() - t))
# combien de prisonniers peuvent rester en place ? (cellules 5-8 et 13-16 de la région)
def fixes(sq):
    return [sq[4 * r + c] for r in (2, 3) for c in range(4) if sq[4 * r + c] == REGION[r][c]]
dist = Counter(len(fixes(s)) for s in TOUS)
print("  prisonniers restant en place, selon le carré :", sorted(dist.items()))
def faisable_un_coup_chacun(sq):
    """chaque prisonnier qui doit bouger le fait en un seul coup, directement à sa place finale ; existe-t-il un ordre ?"""
    cible = {sq[4 * r + c]: REGION[r][c] for r in range(4) for c in range(4)}
    bouge = [h for h in range(1, 17) if cible[h] != h]
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def f(masque):
        if masque == (1 << len(bouge)) - 1: return True
        occ = set();
        for i, h in enumerate(bouge): occ.add(cible[h] if masque >> i & 1 else h)
        for h in range(1, 17):
            if h not in bouge: occ.add(h)
        for i, h in enumerate(bouge):
            if not masque >> i & 1 and accessible(occ - {h}, h, cible[h]) and f(masque | 1 << i): return True
        return False
    return f(0)
for k in sorted(dist, reverse=True):
    if k < 2: break
    cands = [s for s in TOUS if len(fixes(s)) == k]
    oks = sum(1 for s in cands if faisable_un_coup_chacun(s))
    print("  carrés laissant %d prisonniers en place : %d ; faisables en %d coups (un par prisonnier) : %d" % (k, len(cands), 16 - k, oks))
sq = [s for s in TOUS if sorted(fixes(s)) == [6, 7, 13, 16]]
print("  carrés gardant 6, 7, 13 et 16 :", len(sq), "; faisables d'une façon quelconque ? (14 et 15 coincés)", [faisable_un_coup_chacun(s) for s in sq][:4])
un = [s for s in TOUS if len(fixes(s)) == 2 and faisable_un_coup_chacun(s)]
print("  le carré faisable en 14 :", un, "; c'est celui du corrigé :", [list(un[0][4 * r:4 * r + 4]) for r in range(4)] == M)
def faisable_en(sq, limite):
    """recherche en profondeur : coups libres (un homme vers n'importe quelle cellule vide accessible), au plus `limite`."""
    cible = {sq[4 * r + c]: REGION[r][c] for r in range(4) for c in range(4)}
    cases = sorted(CASE)
    def h(pos): return sum(1 for x in range(1, 17) if pos[x - 1] != cible[x])
    vus = {}
    def dfs(pos, reste):
        mal = h(pos)
        if mal == 0: return True
        if mal > reste: return False
        if vus.get(pos, -1) >= reste: return False
        vus[pos] = reste
        occ = set(pos)
        for x in range(1, 17):
            de = pos[x - 1]
            for vers in cases:
                if vers not in occ and accessible(occ - {de}, de, vers):
                    p2 = list(pos); p2[x - 1] = vers
                    if dfs(tuple(p2), reste - 1): return True
        return False
    return dfs(tuple(range(1, 17)), limite)
# Le compte : chaque prisonnier qui n'est pas a sa place finale bouge au moins une fois.
# Un carre qui laisse k hommes en place demande donc au moins 16 - k deplacements.
#   k <= 1 : au moins 15.        k = 2 : 14 exactement si chacun bouge une seule fois.
#   k = 3 et k = 4 : il faut chercher, avec des hommes qui bougent plusieurs fois.
D = (8, 5, 10, 11, 16, 13, 2, 3, 1, 12, 7, 14, 9, 4, 15, 6)
print("\ntemoin, le carre du corrige : en 14 ?", faisable_en(D, 14), "; en 13 ?", faisable_en(D, 13))
assert faisable_en(D, 14) and not faisable_en(D, 13)
res = []
for k in (4, 3):
    for s in [s for s in TOUS if len(fixes(s)) == k]:
        r13, r14 = faisable_en(s, 13), faisable_en(s, 14)
        res.append((r13, r14))
        print("  carre a %d immobiles %s : en 13 ? %s ; en 14 ? %s" % (k, fixes(s), r13, r14))
assert not any(r13 or r14 for r13, r14 in res) and len(un) == 1
print("\nAucun carre ne se forme en moins de 14 deplacements ; un seul en 14 : celui du corrige.")
