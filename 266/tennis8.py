# -*- coding: utf-8 -*-
"""Le defi de Dudeney : huit couples, quatre courts, sept jours.
Recherche generale (les partenariats ne sont plus imposes cycliques)."""
import sys, os, time, json
sys.setrecursionlimit(10000)
N = 8; JOURS = N-1

def couplages(el):
    if not el: yield (); return
    a = el[0]
    for i in range(1, len(el)):
        b = el[i]
        for r in couplages(el[1:i] + el[i+1:]): yield ((a,b),) + r
APP = list(couplages(tuple(range(N))))

hh=set(); ff=set(); hf=set(); part=set(); sol=[]
t0=time.time(); noeuds=[0]

def jour(d, P, k, sigma, nh, nf, nhf, npart):
    """affecte une dame a chaque homme, paire de match par paire de match"""
    noeuds[0]+=1
    if k == len(P):
        sol.append((tuple(P), tuple(sigma)))
        if cherche(d+1): return True
        sol.pop(); return False
    i, j = P[k]
    for wi in range(N):
        if wi == i or wi in sigma or (i, wi) in part or (i, wi) in npart: continue
        for wj in range(N):
            if wj == j or wj == wi or wj in sigma: continue
            if (j, wj) in part or (j, wj) in npart: continue
            a = (i, j)
            b = (wi, wj) if wi < wj else (wj, wi)
            c1 = (i, wj); c2 = (j, wi)
            if c1[0] == c1[1] or c2[0] == c2[1]: continue          # contre son conjoint
            if a in hh or a in nh or b in ff or b in nf: continue
            if c1 in hf or c1 in nhf or c2 in hf or c2 in nhf: continue
            s2 = dict(sigma); s2[wi]=i; s2[wj]=j
            if jour(d, P, k+1, {**sigma, wi:i, wj:j},
                    nh|{a}, nf|{b}, nhf|{c1,c2}, npart|{(i,wi),(j,wj)}):
                return True
    return False

def cherche(d):
    if d > JOURS:
        return True
    for P in APP:
        if any((i,j) in hh for (i,j) in P): continue
        if jour(d, P, 0, {}, set(), set(), set(), set()):
            # fixer definitivement
            return True
    return False

# version iterative propre : on accumule les contraintes globalement
hh=set(); ff=set(); hf=set(); part=set(); sol=[]
def cherche(d):
    if d > JOURS: return True
    debut = APP if d > 1 else [APP[0]]        # jour 1 : un appariement fixe (symetrie)
    for P in debut:
        if any(p in hh for p in P): continue
        r = remplir(d, P, 0, {}, [], [], [], [])
        if r: return True
    return False

def remplir(d, P, k, prises, ah, af, ahf, apart):
    noeuds[0]+=1
    if k == len(P):
        hh.update(ah); ff.update(af); hf.update(ahf); part.update(apart)
        sol.append((P, dict(prises)))
        if cherche(d+1): return True
        sol.pop()
        for x in ah: hh.discard(x)
        for x in af: ff.discard(x)
        for x in ahf: hf.discard(x)
        for x in apart: part.discard(x)
        return False
    i, j = P[k]
    for wi in range(N):
        if wi == i or wi in prises or (i, wi) in part or (i, wi) in apart: continue
        for wj in range(N):
            if wj == j or wj == wi or wj in prises or (j, wj) in part or (j, wj) in apart: continue
            a = (i, j); b = (wi, wj) if wi < wj else (wj, wi)
            c1 = (i, wj); c2 = (j, wi)
            if c1[0]==c1[1] or c2[0]==c2[1]: continue
            if a in hh or a in ah or b in ff or b in af: continue
            if c1 in hf or c1 in ahf or c2 in hf or c2 in ahf or c1==c2: continue
            pr = dict(prises); pr[wi]=i; pr[wj]=j
            if remplir(d, P, k+1, pr, ah+[a], af+[b], ahf+[c1,c2], apart+[(i,wi),(j,wj)]):
                return True
    return False

ok = cherche(1)
print("grille trouvee :", ok, " (%.1f s, %d noeuds)" % (time.time()-t0, noeuds[0]))
if ok:
    H="ABCDEFGH"; Fm="abcdefgh"
    jours=[]
    for d,(P,pr) in enumerate(sol,1):
        inv = {v:k for k,v in pr.items()}
        m=[((H[i],Fm[inv[i]]),(H[j],Fm[inv[j]])) for (i,j) in P]
        jours.append(m)
        print("  Jour %d :" % d, "   ".join("%s%s c. %s%s"%(a,b,c,e) for (a,b),(c,e) in m))
    json.dump([[[list(t) for t in mm] for mm in j] for j in jours], open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tennis8.json"), "w"))
