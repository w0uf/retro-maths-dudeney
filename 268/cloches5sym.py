# -*- coding: utf-8 -*-
"""Cinq cloches : sonnerie juste possedant la symetrie des vraies methodes
(la sonnerie se retrouve identique 24 rangees plus loin, apres renommage des
cloches selon un cycle d'ordre 5).  On ne cherche que 24 changements."""
import sys, time, json, os
SORTIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peal5.json")
from itertools import permutations
sys.setrecursionlimit(100000)
N = 5
def chs(n):
    out=[]
    def rec(i,pris):
        if i>=n-1:
            if pris: out.append(tuple(pris))
            return
        rec(i+1,pris); rec(i+2,pris+[i])
    rec(0,[]); return out
CH = chs(N)
def app(p,c):
    q=list(p)
    for i in c: q[i],q[i+1]=q[i+1],q[i]
    return tuple(q)
DEPART=tuple(range(1,N+1))
t0=time.time()

def cycles5():
    out=[]
    for p in permutations(range(1,N+1)):
        # p vu comme sigma : sigma(i) = p[i-1] ; d'ordre 5 ?
        q=list(range(1,N+1)); ordre=1
        r=[p[i-1] for i in q]
        while r!=q:
            r=[p[i-1] for i in r]; ordre+=1
        if ordre==5: out.append(p)
    return out

def cherche(sig):
    S={b: sig[b-1] for b in range(1,N+1)}
    def ren(p): return tuple(S[x] for x in p)
    def orbite(p):
        o=[p]
        for _ in range(4): o.append(ren(o[-1]))
        return o
    chemin=[DEPART]; vus=set(orbite(DEPART))
    noeuds=[0]
    def rec():
        noeuds[0]+=1
        if len(chemin)==24:
            cible=ren(chemin[0])
            if not any(app(chemin[-1],c)==cible for c in CH): return None
            rows=[]; bloc=list(chemin)
            for _ in range(5):
                rows+=bloc; bloc=[ren(r) for r in bloc]
            if len(set(rows))!=120: return None
            for pl in (0,N-1):
                col=[r[pl] for r in rows]
                for i in range(120):
                    if col[i]==col[(i+1)%120]==col[(i+2)%120]: return None
            return rows
        for c in CH:
            q=app(chemin[-1],c)
            if q in vus: continue
            if len(chemin)>=2 and any(chemin[-2][pl]==chemin[-1][pl]==q[pl] for pl in (0,N-1)):
                continue
            o=orbite(q)
            if len(set(o))!=5: continue
            chemin.append(q); vus.update(o)
            r=rec()
            if r: return r
            chemin.pop(); vus.difference_update(o)
        return None
    return rec(), noeuds[0]

SIG=cycles5()
print("renommages d'ordre cinq :", len(SIG), flush=True)
tot=0
for k,s in enumerate(SIG,1):
    r,n = cherche(s); tot+=n
    if r:
        print("TROUVEE avec le renommage", s, "en %.1f s" % (time.time()-t0), flush=True)
        json.dump(r, open(SORTIE,"w"))
        for i in range(0,120,10):
            print("   ", " ".join("".join(map(str,x)) for x in r[i:i+10]), flush=True)
        break
    if k%4==0: print("  %d/%d renommages, %d noeuds, %.0f s" % (k,len(SIG),tot,time.time()-t0), flush=True)
else:
    print("AUCUNE sonnerie de cette forme (%d noeuds, %.1f s)" % (tot, time.time()-t0), flush=True)
