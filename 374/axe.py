#!/usr/bin/env python3
"""Rétro Math's — n° 374 CROSSING THE RIVER AXE (Dudeney, 1917).
Trois voleurs et trois sacs (800, 500, 300 £), une barque à deux places (un homme et un sac, ou deux hommes) ;
personne ne doit rester seul avec plus que sa part. Parcours en largeur de toutes les situations, avec la
condition de l'énoncé, puis avec la condition plus forte (deux hommes ensemble : pas plus que leurs deux parts).
    python3 axe.py   (instantané)"""
from itertools import permutations, product
from collections import deque, defaultdict
from fractions import Fraction as F
import random
print("=== 374 RIVER AXE")
PART={'G':800,'J':500,'T':300}; SACS=(800,500,300)
def ok_groupe(h,s,fort):
    h=[x for x in h]; tot=sum(s)
    if len(h)==0: return True          # butin sans personne : permis
    if len(h)==1: return tot<=PART[h[0]]
    if fort and len(h)==2: return tot<=PART[h[0]]+PART[h[1]]
    return True
def resoudre(fort):
    tout=frozenset('GJT')|frozenset(SACS)
    s0=(tout,0)  # ce qui est rive gauche, barque à gauche(0)
    def etat_ok(g):
        d=tout-g
        for r in (g,d):
            if not ok_groupe([x for x in r if x in PART],[x for x in r if x not in PART],fort): return False
        return True
    def charges(rive):
        H=[x for x in rive if x in PART]; S=[x for x in rive if x not in PART]
        for h in H:
            yield (h,)
            for s in S:
                if s<=PART[h]: yield (h,s)
        for i in range(len(H)):
            for j in range(i+1,len(H)): yield (H[i],H[j])
    dist={s0:0}; nb={s0:1}; q=deque([s0])
    while q:
        g,b=q.popleft()
        rive=g if b==0 else tout-g
        for c in charges(rive):
            g2=g-frozenset(c) if b==0 else g|frozenset(c)
            if not etat_ok(g2): continue
            v=(g2,1-b)
            if v not in dist: dist[v]=dist[(g,b)]+1; nb[v]=0; q.append(v)
            if dist[v]==dist[(g,b)]+1: nb[v]+=nb[(g,b)]
    f=(frozenset(),1)
    return dist.get(f),nb.get(f),len(dist)
R = {}
for fort in (False,True): R[fort]=resoudre(fort); print("condition forte" if fort else "énoncé",R[fort])

# --- ce que dit le commentaire
assert R[False] == (13, 50, 48) and R[True][:2] == (13, 8)
# sa suite de 13 traversées, rejouée sous la condition forte
SA = [("J", 500), ("J",), ("G", 300), ("G",), ("J", "T"), ("T", 300), ("G", 800), ("J", 500), ("J", "T"), ("G",), ("G", 300), ("J",), ("J", 500)]
def rejoue(seq, fort=True):
    tout = frozenset("GJT") | frozenset(SACS); g = tout; b = 0
    for c in seq:
        rive = g if b == 0 else tout - g
        assert all(x in rive for x in c), c
        g = g - frozenset(c) if b == 0 else g | frozenset(c); b = 1 - b
        for r in (g, tout - g):
            assert ok_groupe([x for x in r if x in PART], [x for x in r if x not in PART], fort), c
    return g == frozenset() and b == 1
assert rejoue(SA)
# témoin : sa suite privée de la 6e traversée (Timothy ramène les 300 £) est refusée
try: rejoue(SA[:5] + SA[6:]); raise SystemExit("ERREUR : suite fausse acceptée")
except AssertionError: pass
print("contrôles : tout est conforme (témoins refusés)")
