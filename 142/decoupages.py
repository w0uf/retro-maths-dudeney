#!/usr/bin/env python3
"""N° 142 THE SILK PATCHWORK : tous les découpages du patchwork (croix de 21 cases) en un carré gardé entier
+ quatre morceaux superposables qui forment une croix grecque. Sans dépendance.
    python3 decoupages.py"""
import itertools, sys

print("=== 142 THE SILK PATCHWORK")
Q = {(r, c) for r in range(5) for c in range(5)} - {(0, 0), (0, 4), (4, 0), (4, 4)}
def norm(cs):
    r0 = min(r for r, c in cs); c0 = min(c for r, c in cs); return tuple(sorted((r - r0, c - c0) for r, c in cs))
def orients(cs, miroir=True):
    out = set(); cur = list(cs)
    for m in range(2 if miroir else 1):
        for _ in range(4):
            cur = [(c, -r) for r, c in cur]; out.add(norm(cur))
        cur = [(r, -c) for r, c in cur]
    return out
def libre(cs): return min(orients(cs))
def unilat(cs): return min(orients(cs, False))
def connexe(cs):
    cs = set(cs); pile = [next(iter(cs))]; vu = set(pile)
    while pile:
        r, c = pile.pop()
        for v in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if v in cs and v not in vu: vu.add(v); pile.append(v)
    return len(vu) == len(cs)
def pavages(region, k=5):
    """toutes les partitions de region en polyominos connexes de k cases"""
    if not region: yield []; return
    a = min(region); 
    def croitre(piece, front):
        if len(piece) == k: yield frozenset(piece); return
        cand = sorted({v for (r, c) in piece for v in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if v in region and v not in piece and v > a})
        for v in cand:
            yield from croitre(piece | {v}, None)
    faits = set()
    for p in croitre(frozenset([a]), None):
        if p in faits: continue
        faits.add(p)
        for reste in pavages(region - p, k): yield [p] + reste
def pave_croix(forme, miroir):
    X = {(r, c) for r in range(6) for c in range(6)} - {(r, c) for r in (0, 1, 4, 5) for c in (0, 1, 4, 5)}
    ors = orients(forme, miroir); n = 0
    def rec(reg, k):
        nonlocal n
        if not reg: n += 1; return
        a = min(reg)
        for o in ors:
            for (dr, dc) in o:
                p = {(a[0] + r - dr, a[1] + c - dc) for r, c in o}
                if p <= reg: rec(reg - p, k + 1)
    rec(X, 0); return n
print("cases :", len(Q), "| carré entier de côté s : 21 − s² multiple de 4 →", [s for s in range(1, 5) if (21 - s * s) % 4 == 0 and 21 - s * s > 0], "| 21−1 = 20 = 5×4 ; 21−9 = 12, 12/5 pas un carré")
sols = []
for F in sorted(Q):
    for part in pavages(frozenset(Q - {F})):
        if len({libre(p) for p in part}) == 1 and all(connexe(p) for p in part): sols.append((F, part))
print("carré d'une case + 4 pentominos superposables (retournement admis) :", len(sols))
from collections import Counter
print("  par case retirée :", Counter(F for F, _ in sols)); print("  par forme :", Counter(libre(p[0]) for _, p in sols))
bons = []
for F, part in sols:
    f = libre(part[0]); sans = len({unilat(p) for p in part}) == 1
    t1, t2 = pave_croix(part[0], True), pave_croix(part[0], False)
    if t1: bons.append((F, f, sans, t1, t2))
print("  dont les 4 morceaux pavent la croix d'aire 20 :", len(bons))
for b in bons: print("   case", b[0], "forme", b[1], "| mêmes sans retournement :", b[2], "| pavages de la croix (avec/sans retournement) :", b[3], b[4])
def sym(part, F):
    out = set()
    for m in range(2):
        for k in range(4):
            def g(x):
                r, c = x
                if m: c = 4 - c
                for _ in range(k): r, c = c, 4 - r
                return (r, c)
            out.add((g(F), frozenset(frozenset(g(x) for x in p) for p in part)))
    return min(out, key=lambda z: (z[0], sorted(sorted(p) for p in z[1])))
orb = {}
for F, part in sols:
    if pave_croix(part[0], True): orb.setdefault(sym(part, F), (F, libre(part[0])))
print("  solutions distinctes aux symétries du patchwork près :", len(orb), Counter((f in ((2, 2),), fo) for f, fo in orb.values()))
for (F, part), (f0, fo) in orb.items(): print("    carré en", F, "| morceaux :", [sorted(p) for p in part])
def pave_carre(forme, n=4):
    X = frozenset((r, c) for r in range(n) for c in range(n)); ors = orients(forme, True); k = [0]
    def rec(reg):
        if not reg: k[0] += 1; return
        a = min(reg)
        for o in ors:
            for (dr, dc) in o:
                p = {(a[0] + r - dr, a[1] + c - dc) for r, c in o}
                if p <= reg: rec(reg - p)
    rec(X); return k[0]
print("  tétrominos et carré 4×4 : L →", pave_carre(((0, 0), (0, 1), (0, 2), (1, 0))), "pavages ; S →", pave_carre(((0, 0), (0, 1), (1, 1), (1, 2))))
livre = [{(0, 1), (0, 2), (0, 3), (1, 1), (1, 2)}, {(1, 3), (1, 4), (2, 3), (2, 4), (3, 4)}, {(4, 3), (4, 2), (4, 1), (3, 3), (3, 2)}, {(3, 0), (2, 0), (1, 0), (3, 1), (2, 1)}]
print("  figure du livre (F au centre, G H I K) : réunion =", set().union(*livre) | {(2, 2)} == Q, "| forme", {libre(p) for p in livre}, "| sans retournement :", len({unilat(p) for p in livre}) == 1)
# le problème d'origine (Fig. 39) : croix entière + 4 morceaux égaux formant un carré 4×4
X5 = {(2, 2), (1, 2), (3, 2), (2, 1), (2, 3)}; n39 = 0
for part in pavages(frozenset(Q - X5), 4):
    if len({libre(p) for p in part}) == 1: n39 += 1; print("  Fig. 39 : croix centrale + 4 tétrominos", libre(part[0]))
print("  Fig. 39, nombre de découpages :", n39)

