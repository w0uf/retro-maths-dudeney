#!/usr/bin/env python3
"""n° 313, suite : trois dames + deux pièces (tours, ou tour + fou), balayage complet
avec préfiltre (les cases que les dames laissent doivent tomber sur les lignes des deux pièces).
    python3 dames_et_fou2.py   (environ 10 s)"""
import os
import sys, io, contextlib, time
sys.argv = ['x', 'X']
with contextlib.redirect_stdout(io.StringIO()): exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dames_et_fou.py')).read())
RC = [glisse(s, DR, 0) | 1 << s for s in range(64)]; DG = [glisse(s, DB, 0) | 1 << s for s in range(64)]
def passe(t2, etiquette):
    t0 = time.time(); fam = {}; gard = {}; total = 0
    SUP1 = RC; SUP2 = RC if t2 == 'R' else DG
    for Q in combinations(range(64), 3):
        occ = 0
        for s in Q: occ |= 1 << s
        m = occ
        for s in Q: m |= glisse(s, DQ, occ)
        M = TOUT & ~m
        u = (M & -M).bit_length() - 1
        base = [('Q', s) for s in Q]; vus = set()
        libres = [s for s in range(64) if not occ >> s & 1]
        cand = []
        for s1 in libres:                       # la tour couvre u…
            if SUP1[s1] >> u & 1:
                r = M & ~SUP1[s1]
                cand += [(s1, s2) for s2 in libres if s2 != s1 and not r & ~SUP2[s2]]
        for s2 in libres:                       # …ou c'est l'autre pièce
            if SUP2[s2] >> u & 1:
                r = M & ~SUP2[s2]
                cand += [(s1, s2) for s1 in libres if s1 != s2 and not r & ~SUP1[s1]]
        for s1, s2 in cand:
            cle = (min(s1, s2), max(s1, s2)) if t2 == 'R' else (s1, s2)
            if cle in vus: continue
            vus.add(cle)
            P = base + [('R', s1), (t2, s2)]
            if domine(P):
                total += 1; fam.setdefault(canon(P), []).append(P)
                if gardees(P): gard.setdefault(canon(P), []).append(P)
    print("%s : %d dispositions, %d familles ; toutes pièces gardées : %d familles (%.0f s)" % (etiquette, total, len(fam), len(gard), time.time()-t0), flush=True)
    return fam, gard
occn = lambda P: sum(1 << s for _, s in P)
def aucune_gardee(P):
    o = occn(P); return not any(attaque(t2, s2, o) >> s & 1 for _, s in P for t2, s2 in P if s2 != s)
fam, gard = passe('R', "3 dames + 2 tours")
assert len(fam) == 92 and len(gard) == 1 and canon(fig4) in gard        # Planck : la seule, toutes pieces gardees
for k in gard: print("   gardées :", nomme(k), "| Planck ?", k == canon(fig4))
print("   aucune pièce gardée :", sum(1 for k in fam if aucune_gardee(list(k))), "familles")
fam, gard = passe('B', "3 dames + tour + fou")
sans = [k for k in fam if aucune_gardee(list(k))]
assert len(fam) == 4 and sans == [canon(fig5)]                          # quatre en tout, une seule sans piece gardee : la sienne
print("   sa fig. 5 y est :", canon(fig5) in fam, "| familles sans aucune pièce gardée :", sum(1 for k in fam if aucune_gardee(list(k))), "| toutes gardées :", len(gard))
for k in list(gard)[:6]: print("   gardées :", nomme(k))
# temoins : la disposition de Planck privee d'une tour ne tient plus l'echiquier ; sa fig. 5 a des pieces non gardees
assert not domine(fig4[:-1]) and not gardees(fig5)
print("controles : tout est conforme (temoins refuses)")
