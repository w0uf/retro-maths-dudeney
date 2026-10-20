#!/usr/bin/env python3
"""Rétro Math's — n° 173 MRS. PERKINS'S QUILT (Dudeney, 1917).
Découper un carré 13 × 13 en carrés entiers, le moins possible. Recherche exhaustive : on remplit toujours la case
libre la plus haute puis la plus à gauche (le carré qui l'occupe y a son coin), avec élagage par l'aire.
Deux pièges notés dans le commentaire : la borne sûre sur le côté des carrés restants est (N − hauteur minimale) ;
et pour énumérer TOUTES les découpes optimales, la cible doit rester fixe.
    python3 quilt.py   (quelques secondes)"""
def decoupes(N, cible, borne_sure=True, tout=True):
    sols = []
    def rec(h, pose, n):
        if min(h) == N:
            if n == cible: sols.append(list(pose))
            return
        if n >= cible: return
        y = min(h); x = h.index(y); w = 0
        while x + w < N and h[x + w] == y: w += 1
        w = min(w, N - y)
        if w == N: w = N - 1                               # pas le carré entier lui-même
        reste = N * N - sum(h)
        cm = (N - y) if borne_sure else w                  # la mauvaise borne : la place disponible ICI
        if n + -(-reste // (cm * cm)) > cible: return
        for c in range(w, 0, -1):
            for i in range(x, x + c): h[i] += c
            pose.append((x, y, c)); rec(h, pose, n + 1); pose.pop()
            for i in range(x, x + c): h[i] -= c
            if sols and not tout: return
    rec([0] * N, [], 0)
    return sols
def minimum(N, **k):
    n = 1
    while not decoupes(N, n, tout=False, **k): n += 1
    return n
def grille(s, N):
    g = [[0] * N for _ in range(N)]
    for x, y, c in s:
        for i in range(y, y + c):
            for j in range(x, x + c): assert g[i][j] == 0; g[i][j] = c
    return g
def canon(s, N):
    g = grille(s, N); formes = []
    for _ in range(4):
        g = [list(r) for r in zip(*g[::-1])]
        formes.append(tuple(map(tuple, g))); formes.append(tuple(map(tuple, [r[::-1] for r in g])))
    return min(formes)
petits = {n: minimum(n) for n in (2, 3, 5, 7, 11)}
print("petits côtés :", petits)
assert petits == {2: 4, 3: 6, 5: 8, 7: 9, 11: 11}            # valeurs connues : le programme est sain
assert decoupes(13, 10, tout=False) == []                    # dix ne suffisent pas
sols = decoupes(13, 11)
print("découpes à 11 carrés :", len(sols), "| à symétrie près :", len({canon(s, 13) for s in sols}))
assert len(sols) == 8 and len({canon(s, 13) for s in sols}) == 1
assert sorted(c for _, _, c in sols[0]) == [1, 1, 2, 2, 2, 3, 3, 4, 6, 6, 7]
# la découpe du commentaire, colonnes et rangées numérotées de 1 à 13 : (colonne, rangée, côté) du coin haut-gauche
SIENNE = [(1, 1, 7), (8, 1, 6), (1, 8, 6), (10, 7, 4), (7, 9, 3), (11, 11, 3), (8, 7, 2), (7, 12, 2), (9, 12, 2), (7, 8, 1), (10, 11, 1)]
g = grille([(x - 1, y - 1, c) for x, y, c in SIENNE], 13)
assert all(v for r in g for v in r) and sum(c * c for *_, c in SIENNE) == 169
assert canon([(x - 1, y - 1, c) for x, y, c in SIENNE], 13) == canon(sols[0], 13)
# la méthode gloutonne (le plus grand carré possible) : 12 × 12 puis 25 carrés unités, 26 morceaux
assert 1 + (169 - 144) == 26
# témoin : avec la mauvaise borne, la recherche manque le 11 et rend 12
assert minimum(13, borne_sure=False) == 12
print("contrôles : tout est conforme (témoins refusés)")
