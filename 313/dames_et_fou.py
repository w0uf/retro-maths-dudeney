#!/usr/bin/env python3
"""Rétro Math's — n° 313 QUEENS AND BISHOP PUZZLE (Dudeney, 1917).
Toute case occupée ou attaquée (les pièces font écran). Vérifie ses figures et
ses affirmations d'unicité par balayage complet. Cases : (rangée depuis le haut, colonne).
    python3 dames_et_fou.py        (C, F et T : 4 dames + cavalier, fou, tour ; environ 20 min)
    python3 dames_et_fou.py C      (le cavalier seul : environ 4 min)
    python3 dames_et_fou.py X      (les figures seules, instantané)
Les balayages à 3 dames + 2 pièces sont dans dames_et_fou2.py."""
import sys, time
from itertools import combinations
from collections import Counter
N = 8; TOUT = (1 << 64) - 1
def b(l, c): return 1 << (l*8 + c)
DQ = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]; DR = [(-1,0),(1,0),(0,-1),(0,1)]; DB = [(-1,-1),(-1,1),(1,-1),(1,1)]
RAY = {}
for l in range(8):
    for c in range(8):
        for d in DQ:
            r = []; x, y = l+d[0], c+d[1]
            while 0 <= x < 8 and 0 <= y < 8: r.append(x*8+y); x += d[0]; y += d[1]
            RAY[(l*8+c, d)] = r
def glisse(s, dirs, occ):
    m = 0
    for d in dirs:
        for t in RAY[(s, d)]:
            m |= 1 << t
            if occ >> t & 1: break
    return m
def saut(s, pas):
    l, c = divmod(s, 8); m = 0
    for dl, dc in pas:
        if 0 <= l+dl < 8 and 0 <= c+dc < 8: m |= b(l+dl, c+dc)
    return m
CAV = [saut(s, [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]) for s in range(64)]
ROI = [saut(s, DQ) for s in range(64)]
PION = [saut(s, [(-1,-1),(-1,1)]) for s in range(64)]       # pion blanc : il prend vers le haut
def attaque(t, s, occ):
    return {'Q': lambda: glisse(s, DQ, occ), 'R': lambda: glisse(s, DR, occ), 'B': lambda: glisse(s, DB, occ),
            'N': lambda: CAV[s], 'K': lambda: ROI[s], 'P': lambda: PION[s]}[t]()
def couverture(P):                      # P = [(type, case)]
    occ = 0
    for _, s in P: occ |= 1 << s
    m = occ
    for t, s in P: m |= attaque(t, s, occ)
    return m
def domine(P): return couverture(P) == TOUT
def gardees(P):
    occ = 0
    for _, s in P: occ |= 1 << s
    return all(any(attaque(t2, s2, occ) >> s & 1 for t2, s2 in P if s2 != s) for _, s in P)
def sq(l, c): return l*8+c
SYM = [lambda l,c:(l,c), lambda l,c:(c,7-l), lambda l,c:(7-l,7-c), lambda l,c:(7-c,l), lambda l,c:(l,7-c), lambda l,c:(7-l,c), lambda l,c:(c,l), lambda l,c:(7-c,7-l)]
def canon(P): return min(tuple(sorted((t, sq(*f(*divmod(s, 8)))) for t, s in P)) for f in SYM)
def nomme(P): return ' '.join(t + "abcdefgh"[s % 8] + str(8 - s // 8) for t, s in sorted(P))

print("=== ses figures")
enonce = [('Q',sq(0,2)),('Q',sq(1,6)),('Q',sq(4,1)),('Q',sq(5,5)),('R',sq(6,0))]
fig1 = [('Q',sq(0,7)),('Q',sq(3,2)),('Q',sq(4,4)),('Q',sq(5,3)),('B',sq(6,0))]
fig2 = [('Q',sq(2,3)),('Q',sq(3,7)),('Q',sq(6,2)),('Q',sq(7,6))]
fig3 = [('Q',sq(1,6)),('Q',sq(2,3)),('Q',sq(3,5)),('Q',sq(4,4)),('N',sq(7,2))]
fig4 = [('Q',sq(1,1)),('Q',sq(1,5)),('Q',sq(7,3)),('R',sq(3,7)),('R',sq(5,3))]
fig5 = [('R',sq(0,3)),('Q',sq(2,7)),('Q',sq(4,1)),('Q',sq(6,5)),('B',sq(3,4))]
for n, P in (("énoncé (4D + T)", enonce), ("fig. 1 (4D + F)", fig1), ("fig. 3 Wallis (4D + C)", fig3), ("fig. 4 Planck (3D + 2T)", fig4), ("fig. 5 (3D + T + F)", fig5)):
    print(n, ":", nomme(P), "| domine :", domine(P), "| toutes gardées :", gardees(P), "| aucune gardée :", not any(gardees([p] + [q for q in P if q != p][:0] or P) for p in P[:0]))
occ2 = sum(1 << s for _, s in fig2)
lettres = {'a': [(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)], 'b': [(1,1)], 'c': [(0,1),(1,0)], 'd': [(0,2),(2,0)], 'e': [(0,0)]}
quelle = {sq(*x): k for k, v in lettres.items() for x in v}
FIG2 = {}
for t, attendu in (('Q', 'abcde'), ('R', 'c'), ('B', 'abe'), ('P', 'b'), ('K', 'bce'), ('N', '')):
    ok = FIG2[t] = [s for s in range(64) if not occ2 >> s & 1 and domine(fig2 + [(t, s)])]
    print("fig. 2 +", t, ":", len(ok), "cases", sorted(quelle.get(s, '?' + "abcdefgh"[s % 8] + str(8 - s // 8)) for s in ok), "| attendu :", sum(len(lettres[k]) for k in attendu), attendu)

# --- ses figures : ce que dit l'article
assert all(domine(P) for P in (enonce, fig1, fig3, fig4, fig5)) and gardees(fig4)
assert [len(FIG2[t]) for t in "QRBPKN"] == [12, 2, 5, 1, 4, 0]     # le fou : 5 cases, et non ses 8
annoncees = [sq(*x) for k in 'abe' for x in lettres[k]]          # ses 8 cases pour le fou (lettres a, b, e)
fautives = [s for s in annoncees if s not in FIG2['B']]
assert sorted(nomme([('B', s)])[1:] for s in fautives) == ["c6", "d5", "g2"]
# temoin de la raison : sur ces trois cases, une dame convient, un fou non (il fait ecran a une dame)
assert all(domine(fig2 + [('Q', s)]) and not domine(fig2 + [('B', s)]) for s in fautives)
print("figures : conformes ; fou de la fig. 2 : 5 cases, fautives", sorted(nomme([('B', s)])[1:] for s in fautives))

def balayage(nq, autres, filtre=None, etiquette=""):
    """nq dames + les pièces de `autres` (types) ; rend les familles dominantes."""
    t0 = time.time(); fam = {}; total = 0
    portee = {'R': 15, 'B': 14, 'N': 9, 'K': 9, 'P': 3, 'Q': 28}
    maxi = sum(portee[t] for t in autres)
    for Q in combinations(range(64), nq):
        occ = 0
        for s in Q: occ |= 1 << s
        m = occ
        for s in Q: m |= glisse(s, DQ, occ)
        manque = TOUT & ~m
        if bin(manque).count('1') > maxi: continue
        libres = [s for s in range(64) if not occ >> s & 1]
        base = [('Q', s) for s in Q]
        if len(autres) == 1:
            for s in libres:
                P = base + [(autres[0], s)]
                if domine(P) and (not filtre or filtre(P)): total += 1; fam.setdefault(canon(P), []).append(P)
        else:
            t1, t2 = autres
            for i, s1 in enumerate(libres):
                for s2 in (libres[i+1:] if t1 == t2 else libres):
                    if s2 == s1: continue
                    P = base + [(t1, s1), (t2, s2)]
                    if domine(P) and (not filtre or filtre(P)): total += 1; fam.setdefault(canon(P), []).append(P)
    print("%s : %d dispositions, %d familles (%.0f s)" % (etiquette, total, len(fam), time.time()-t0), flush=True)
    return fam

quoi = sys.argv[1:] or ['C', 'F', 'T']
if 'C' in quoi:
    f = balayage(4, ['N'], etiquette="4 dames + cavalier")
    for k in f: print("   ", nomme(k), "| Wallis ?", k == canon(fig3))
    assert len(f) == 1 and canon(fig3) in f              # « la seule disposition connue » est la seule
if 'F' in quoi:
    f = balayage(4, ['B'], etiquette="4 dames + fou")
    ici = [P for v in f.values() for P in v if ('B', sq(6,0)) in P]
    print("   avec le fou sur la case de la tour (a2) :", len(ici), [nomme(P) for P in ici[:12]], "| sa fig. 1 y est :", any(sorted(P) == sorted(fig1) for P in ici))
    assert len(f) == 49 and sum(len(v) for v in f.values()) == 388 and len(ici) == 6 and any(sorted(P) == sorted(fig1) for P in ici)
if 'T' in quoi:
    f = balayage(4, ['R'], etiquette="4 dames + tour")
    assert len(f) == 384 and sum(len(v) for v in f.values()) == 3032
if 'D' in quoi:
    f = balayage(3, ['R', 'R'], filtre=gardees, etiquette="3 dames + 2 tours, toutes gardées")
    for k in f: print("   ", nomme(k), "| Planck ?", k == canon(fig4))
    f = balayage(3, ['R', 'R'], etiquette="3 dames + 2 tours, sans condition")
if 'E' in quoi:
    f = balayage(3, ['R', 'B'], etiquette="3 dames + tour + fou")
    print("   sa fig. 5 y est :", canon(fig5) in f)
print("controles : tout est conforme (temoins refuses)")
