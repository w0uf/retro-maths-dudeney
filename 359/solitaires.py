#!/usr/bin/env python3
"""Rétro Math's — n° 359 COUNTER SOLITAIRE et n° 360 CHESSBOARD SOLITAIRE (Dudeney, 1917).
Prises par saut orthogonal par-dessus un jeton voisin vers la case libre suivante.
    python3 solitaires.py   (environ 1 s)"""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)
def sauts(H, L):
    out = []
    for r in range(H):
        for c in range(L):
            for dr, dc in ((0,1),(0,-1),(1,0),(-1,0)):
                r2, c2 = r+2*dr, c+2*dc
                if 0 <= r2 < H and 0 <= c2 < L: out.append((r*L+c, (r+dr)*L+c+dc, r2*L+c2))
    return out
def rejoue(H, L, pos, seq):
    """pos : {numéro: case} ; seq : liste de (qui, par-dessus qui) → positions finales, ou erreur"""
    pos = dict(pos); occ = {v: k for k, v in pos.items()}
    for a, b in seq:
        pa, pb = pos[a], pos[b]; ra, ca = divmod(pa, L); rb, cb = divmod(pb, L)
        assert abs(ra-rb) + abs(ca-cb) == 1, (a, b, "pas voisins")
        r2, c2 = 2*rb-ra, 2*cb-ca; assert 0 <= r2 < H and 0 <= c2 < L, (a, b, "hors du plateau")
        t = r2*L+c2; assert t not in occ, (a, b, "case d'arrivée occupée")
        del occ[pa]; del occ[pb]; del pos[b]; pos[a] = t; occ[t] = a
    return pos

print("=== 359 : plateau 3×8, jetons 9-16 sur la rangée du milieu, 1-8 sur celle du bas")
H, L = 3, 8; S = sauts(H, L)
pos0 = {**{9+i: 8+i for i in range(8)}, **{1+i: 16+i for i in range(8)}}
seq = [(3,11),(9,10),(1,2),(7,15),(8,16),(8,7),(5,13),(1,4),(8,5),(6,14),(3,8),(6,3),(6,12),(1,6),(1,9)]
fin359 = fin = rejoue(H, L, pos0, seq); seq359, pos359 = seq, pos0; print("sa suite :", len(seq), "prises → reste", fin, "| dernière prise par le n° 1 :", seq[-1][0] == 1)
plein = sum(1 << v for v in pos0.values())
def survivants(H, L, S, plein, pos0):
    """pour chaque jeton k : peut-il rester seul ? et en faisant lui-même la dernière prise ? sur quelles cases ?"""
    res = {}
    for k, pk in pos0.items():
        vus = {}
        def rec(m, p):
            cle = (m, p)
            if cle in vus: return vus[cle]
            out = set()
            if m & (m - 1) == 0: vus[cle] = {(p, None)}; return vus[cle]
            for a, b, c in S:
                if m >> a & 1 and m >> b & 1 and not m >> c & 1 and b != p:
                    m2 = m ^ (1 << a) ^ (1 << b) ^ (1 << c); p2 = c if a == p else p
                    for (pf, _) in rec(m2, p2):
                        out.add((pf, a == p if (m2 & (m2 - 1)) == 0 else _))
            vus[cle] = out; return out
        r = rec(plein, pk)
        res[k] = (sorted({pf for pf, d in r}), sorted({pf for pf, d in r if d}), len(vus))
    return res
res = survivants(H, L, S, plein, pos0)
nomc = lambda p: "rangée %d, colonne %d" % (p // L + 1, p % L + 1)
print("jetons qui peuvent rester seuls :", [k for k in sorted(res) if res[k][0]])
print("jetons qui peuvent rester seuls EN FAISANT la dernière prise :", [k for k in sorted(res) if res[k][1]])
for k in sorted(res):
    if res[k][0]: print("   n° %2d : cases finales possibles %s ; en prenant lui-même au dernier coup %s" % (k, res[k][0], res[k][1]))
print("positions explorées (pour le n° 1) :", res[1][2])

print("\n=== 360 : échiquier, jetons 1-16 sur les deux rangées du haut, 17-32 sur les deux du bas")
H, L = 8, 8
pos0 = {**{1+i: i for i in range(16)}, **{17+i: 48+i for i in range(16)}}
seq = [(7,15),(8,16),(8,7),(2,10),(1,9),(1,2),(5,13),(3,4),(6,3),(11,1),(14,8),(6,12),(5,6),(5,11),(31,23),(32,24),(32,31),(26,18),(25,17),(25,26),(22,32),(14,22),(29,21),(14,29),(27,28),(30,27),(25,14),(30,20),(25,30),(25,5)]
fin = rejoue(H, L, pos0, seq); print("sa suite :", len(seq), "prises → restent", fin, "| le 19 n'a jamais bougé :", fin.get(19) == pos0[19], "| même groupe :", all(k >= 17 for k in fin) or all(k <= 16 for k in fin))
# l'invariant classique : classes (rangée + colonne) mod 3 et (rangée − colonne) mod 3 ; chaque prise change la parité des trois classes
def parites(cases):
    a = [0, 0, 0]; b = [0, 0, 0]
    for p in cases: r, c = divmod(p, L); a[(r+c) % 3] ^= 1; b[(r-c) % 3] ^= 1
    return tuple(a), tuple(b)
pa, pb = parites(pos0.values()); print("parités au départ (32 jetons) :", pa, pb)
print("après 31 prises (un seul jeton) il faudrait :", tuple(x ^ 1 for x in pa), tuple(x ^ 1 for x in pb), "— un jeton seul donne toujours une classe impaire et deux paires")
possibles = [p for p in range(64) if parites([p]) == (tuple(x ^ 1 for x in pa), tuple(x ^ 1 for x in pb))]
print("cases où un jeton unique respecterait l'invariant :", possibles)
deux = [(p, q) for p in range(64) for q in range(p+1, 64) if parites([p, q]) == (pa, pb)]
print("paires de cases compatibles avec l'invariant pour DEUX jetons restants :", len(deux), "sur", 64*63//2, "| celle de Dudeney :", tuple(sorted(fin.values())), tuple(sorted(fin.values())) in deux)

# --- ce que disent les articles
assert fin359 == {1: 2} and seq359[-1][0] == 1
assert [k for k in sorted(res) if res[k][0]] == list(range(1, 9))                       # aucun des 9-16
assert {p for k in res for p in res[k][0]} == {2, 5}                                    # deux cases d'arrivee seulement
assert set(fin) == {19, 25} and fin[19] == pos0[19] and fin[25] - fin[19] == -24         # meme colonne, 3 rangees d'ecart
assert possibles == [] and len(deux) == 210
# temoins : une prise par-dessus un jeton non voisin, ou vers une case occupee, est refusee par le rejeu
for faux in ([(3, 12)], [(9, 10)]):
    try: rejoue(3, 8, pos359, faux); raise SystemExit("ERREUR : coup faux accepte " + str(faux))
    except AssertionError: pass
# et la suite du 360 privee de sa derniere prise laisse trois jetons, pas deux
assert len(rejoue(8, 8, pos0, seq[:-1])) == 3
print("controles : tout est conforme (temoins refuses)")
