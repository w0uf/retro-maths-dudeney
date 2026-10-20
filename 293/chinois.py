"""n° 293 THE CHINESE CHESSBOARD : combien de pièces toutes différentes (couleurs comprises, rotations permises,
pas de retournement) ? 1) borne par les aires  2) contrôle des deux découpages du corrigé."""
from collections import Counter
def norm(cells):
    """forme canonique d'une pièce colorée à rotation près ; couleur = (x+y)%2 de la case d'origine"""
    best = None
    for r in range(4):
        c = cells
        for _ in range(r): c = [(y, -x, col) for x, y, col in c]
        mx = min(x for x, y, _ in c); my = min(y for x, y, _ in c)
        t = tuple(sorted((x-mx, y-my, col) for x, y, col in c))
        if best is None or t < best: best = t
    return best
def pieces(nmax):
    """polyominos colorés à rotation près, par aire"""
    par = {1: {norm([(0, 0, 0)]), norm([(0, 0, 1)])}}
    for n in range(2, nmax+1):
        s = set()
        for p in par[n-1]:
            occ = {(x, y) for x, y, _ in p}
            for x, y, col in p:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    q = (x+dx, y+dy)
                    if q not in occ: s.add(norm(list(p) + [(q[0], q[1], 1-col)]))
        par[n] = s
    return par
P = pieces(8)
nb = {n: len(P[n]) for n in P}
print("pièces différentes par aire :", nb)
# plus petite aire totale pour k pièces différentes : on prend les plus petites
aires = [n for n in sorted(nb) for _ in range(nb[n])]
cum = 0
for k, a in enumerate(aires, 1):
    cum += a
    if k in (17, 18, 19): print("k = %d pièces : aire minimale %d" % (k, cum))
    if k == 19: break
assert sum(aires[:19]) > 64 and sum(aires[:18]) <= 64
# les deux découpages du corrigé, relevés sur la gravure (une lettre par pièce, rangée du haut d'abord)
import re, os
def releve(L):
    """L : les 17 lignes ASCII du corrigé (Gutenberg). Une coupe = « | », « I » ou « = » ; pas de coupe = espace, « : » ou « . »"""
    par = {(r, c): (r, c) for r in range(8) for c in range(8)}
    def f(a):
        while par[a] != a: a = par[a]
        return a
    for r in range(8):
        for c in range(8):
            if c < 7 and L[2*r+1][4*c+4] not in "|I": par[f((r, c))] = f((r, c+1))
            if r < 7 and "=" not in L[2*r+2][4*c+1:4*c+4] and "-" not in L[2*r+2][4*c+1:4*c+4]: par[f((r, c))] = f((r+1, c))
    # contrôle de la couleur dessinée : « : » = case noire, et l'échiquier commence par une blanche
    for r in range(8):
        for c in range(8):
            noir = ":" in L[2*r+1][4*c+1:4*c+4]
            assert noir == ((r + c) % 2 == 1), ("couleur", r, c)
    D = {}
    for r in range(8):
        for c in range(8): D.setdefault(f((r, c)), []).append((c, r))
    return list(D.values())
T = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "corrige293.txt")).read()
BLOCS = [[l[4:] for l in b.splitlines()] for b in re.findall(r"((?:    [+I|].*\n)+)", T)]
def controle(D, nom):
    cases = {k: [(x, y, (x+y) % 2) for x, y in p] for k, p in enumerate(D)}
    formes = [norm(c) for c in cases.values()]
    # connexité
    for ch, c in cases.items():
        s = {(x, y) for x, y, _ in c}; vu = {next(iter(s))}; f = list(vu)
        while f:
            x, y = f.pop()
            for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if q in s and q not in vu: vu.add(q); f.append(q)
        assert vu == s, ("pièce non connexe", ch)
    dbl = [f for f, k in Counter(formes).items() if k > 1]
    print(nom, ":", len(cases), "pièces, aires", sorted(len(c) for c in cases.values()), "| toutes différentes :", not dbl)
    return len(cases), not dbl

r1 = controle(releve(BLOCS[0]), "découpage numéroté")
r2 = controle(releve(BLOCS[1]), "découpage à cinq cases au plus")
assert r1 == (18, True) and r2 == (18, True)
# témoin : le premier découpage avec une coupe effacée entre deux pièces (on recolle 5 et 6) ne doit plus passer
L = [list(l) for l in BLOCS[0]]; L[1][4*6+4] = " "
print("témoin :", controle(releve(["".join(l) for l in L]), "témoin, 5 et 6 recollées"))
# quelles tailles de pièces un découpage en 18 peut-il avoir ? (aire 64, au plus nb[n] pièces d'aire n)
from itertools import product
comp = []
def rec(n, reste_k, reste_a, acc):
    if reste_k == 0:
        if reste_a == 0: comp.append(dict(acc))
        return
    if n > 64: return
    for m in range(min(nb.get(n, 10**9), reste_k, reste_a // n) + 1):
        acc[n] = m; rec(n+1, reste_k-m, reste_a-m*n, acc)
    acc.pop(n, None)
rec(1, 18, 64, {})
for c in comp: print("répartition possible :", {k: v for k, v in c.items() if v})
assert len(comp) == 8 and all(c.get(1) == 2 for c in comp) and min(c.get(4, 0) for c in comp) == 7
