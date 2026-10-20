"""n° 294 THE CHESSBOARD SENTENCE : les quatorze pièces de « .CUT.THY.LIFE. », relevées sur la gravure de l'énoncé
(b = case noire, w = case blanche), et tous les assemblages en échiquier, rotations permises."""
PIECES = {
 ".1": ["w"], ".2": ["w"], ".3": ["w"], ".4": ["w"],
 "C": ["wb", "b.", "wb"],
 "U": ["w.w", "b.b", "wbw"],
 "T1": ["bwb", ".b.", ".w."],
 "T2": ["wbw", ".w.", ".b."],
 "H": ["b.b", "wbw", "b.b"],
 "Y": ["b.b", "wbw", ".w."],
 "L": ["b..", "w..", "b..", "wbw"],
 "I": ["b", "w", "b"],
 "F": ["bwb", "w..", "bw.", "w.."],
 "E": ["wb.", "b..", "wb.", "b..", "wbw"],
}
def cases(m): return [(r, c, ch) for r, l in enumerate(m) for c, ch in enumerate(l) if ch != "."]
def orientations(cs, retourner=False):
    vus = set(); out = []
    for f in ((False, True) if retourner else (False,)):
        c0 = [(r, -c if f else c, ch) for r, c, ch in cs]
        for k in range(4):
            c1 = c0
            for _ in range(k): c1 = [(c, -r, ch) for r, c, ch in c1]
            mr = min(r for r, _, _ in c1); mc = min(c for _, c, _ in c1)
            t = tuple(sorted((r - mr, c - mc, ch) for r, c, ch in c1))
            if t not in vus: vus.add(t); out.append(t)
    return out
assert sum(len(cases(m)) for m in PIECES.values()) == 64
assert sum(ch == "w" for m in PIECES.values() for _, _, ch in cases(m)) == 32
def poses(retourner):
    """pour chaque pièce, ses placements sur l'échiquier (masques de 64 bits), rangés par leur plus petite case"""
    P = {}
    for n, m in PIECES.items():
        if n.startswith("."): continue
        L = {}
        for o in orientations(cases(m), retourner):
            for dr in range(8):
                for dc in range(8):
                    cs = [(r + dr, c + dc) for r, c, _ in o]
                    if all(0 <= r < 8 and 0 <= c < 8 for r, c in cs) and all((ch == "b") == ((r + dr + c + dc) % 2 == 1) for r, c, ch in o):
                        k = [r * 8 + c for r, c in cs]; L.setdefault(min(k), []).append(sum(1 << x for x in k))
        P[n] = L
    return P
def resout(retourner):
    """on remplit toujours la première case vide : par une pièce encore libre, ou par un point si elle est blanche"""
    P = poses(retourner); noms = list(P); sols = []
    PLEIN = (1 << 64) - 1
    def rec(occ, libres, points, choix):
        if occ == PLEIN: sols.append(frozenset(choix)); return
        c = (~occ & -~occ).bit_length() - 1
        if points and (c // 8 + c % 8) % 2 == 0:
            choix.append(1 << c); rec(occ | 1 << c, libres, points - 1, choix); choix.pop()
        for n in libres:
            for m in P[n].get(c, ()):
                if not m & occ:
                    choix.append(m); rec(occ | m, libres - {n}, points, choix); choix.pop()
    rec(0, frozenset(noms), 4, []); return sols
for ret in (False, True):
    S = resout(ret)
    # le demi-tour garde les couleurs de l'échiquier : on compte aussi à demi-tour près
    tourne = lambda s: frozenset(int(bin(m)[2:].zfill(64)[::-1], 2) for m in s)
    classes = {min(s, tourne(s), key=lambda x: sorted(x)) for s in S}
    print(("retournements permis" if ret else "rotations seulement"), ": découpages", len(S), "| à demi-tour près", len(set(map(frozenset, classes))))
# le corrigé de Gutenberg (texte) : son découpage, relevé comme au n° 293
import re, os
T = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "corrige294.txt")).read()
A = [l[4:] for l in re.search(r"((?:    [+I|].*\n)+)", T).group(1).splitlines()]
par = {k: k for k in range(64)}
def f(a):
    while par[a] != a: a = par[a]
    return a
for r in range(8):
    for c in range(8):
        k = r * 8 + c                # même repère que le solveur : case 0 = coin blanc en haut à gauche
        if c < 7 and A[2*r+1][4*c+4] not in "|I": par[f(k)] = f(k + 1)
        if r < 7 and not set(A[2*r+2][4*c+1:4*c+4]) & set("=-"): par[f(k)] = f(k + 8)
G = {}
for k in range(64): G.setdefault(f(k), 0); G[f(k)] |= 1 << k
G = list(G.values())
print("corrigé du texte de Gutenberg :", len(G), "pièces")
S = resout(False)
dans = [s for s in S if all(any(m & g == m for g in G) for m in s)]
print("assemblages compatibles avec ses traits :", len(dans))
for s in dans:
    fus = [g for g in G if sum(1 for m in s if m & g == m) > 1]
    print("  pièce du texte qui en contient deux :", [[k for k in range(64) if m >> k & 1 and m & g == m] for g in fus for m in s if m & g == m])
assert len(S) == 124 and len(dans) == 1 and len(G) == 13
# témoin : le découpage du texte de Gutenberg, tel quel, n'est pas un assemblage des quatorze pièces
print("témoin (découpage du texte tel quel) refusé :", frozenset(G) not in set(S)); assert frozenset(G) not in set(S)
