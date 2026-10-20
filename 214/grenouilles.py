#!/usr/bin/env python3
"""Rétro Math's — n° 214 THE SIX FROGS (Dudeney, 1917).
Renverser l'ordre de n grenouilles, une case vide ; un coup = une glissade ou un saut par-dessus une voisine.
Parcours en largeur exhaustif pour n = 2 à 9, rejeu de la suite de Dudeney, et sa règle générale.
    python3 grenouilles.py   (environ 10 s)"""
from itertools import permutations, product
from collections import deque, defaultdict
from fractions import Fraction as F
import random
print("=== 214 SIX FROGS")
def bfs(n, vide_gauche=True):
    s = (0,)+tuple(range(1,n+1)) if vide_gauche else tuple(range(1,n+1))+(0,)
    t = (0,)+tuple(range(n,0,-1)) if vide_gauche else tuple(range(n,0,-1))+(0,)
    d={s:(0,0)}; q=deque([s])   # (coups, sauts) — sauts d'un chemin optimal
    while q:
        u=q.popleft()
        if u==t: return d[u]
        z=u.index(0)
        for dz in (-2,-1,1,2):
            w=z+dz
            if 0<=w<=n:
                v=list(u); v[z],v[w]=v[w],v[z]; v=tuple(v)
                if v not in d: d[v]=(d[u][0]+1,d[u][1]+(abs(dz)==2)); q.append(v)
R={}
for n in range(2,10):
    c,s=bfs(n); c2,_=bfs(n,False); R[n]=(c,s,c2)
    f=(n*n+n)//2 if n%2==0 else (n*n+3*n)//2-4
    print(n,"coups",c,"(vide à droite:",c2,") sauts",s,"glissades",c-s,"formule",f,"paires",n*(n-1)//2)
# la suite de Dudeney pour six
seq=[2,4,6,5,3,1]*3+[2,4,6]
u=[0,1,2,3,4,5,6]; sauts=0
for g in seq:
    i=u.index(g); z=u.index(0); assert abs(i-z) in (1,2),(g,u)
    sauts+=abs(i-z)==2; u[i],u[z]=u[z],u[i]
print("Dudeney:",len(seq),"coups ->",u,"sauts",sauts)
print("distance totale:",sum(abs(7-2*i) for i in range(1,7)))


# --- ce que dit le commentaire
assert len(seq) == 21 and u == [0, 6, 5, 4, 3, 2, 1] and sauts == 15
for n, (c, s, c2) in R.items():
    regle = (n * n + n) // 2 if n % 2 == 0 else (n * n + 3 * n) // 2 - 4
    assert c == c2 == regle and s == n * (n - 1) // 2             # sauts = nombre de couples
    assert c - s == (n if n % 2 == 0 else 2 * n - 4)               # glissades
assert [R[n][0] for n in range(2, 10)] == [3, 5, 10, 16, 21, 31, 36, 50]
seq14 = ([2, 4, 6, 8, 10, 12, 14, 13, 11, 9, 7, 5, 3, 1] * 7) + [2, 4, 6, 8, 10, 12, 14]
u = [0] + list(range(1, 15))
for g in seq14:
    i = u.index(g); z = u.index(0); assert abs(i - z) in (1, 2); u[i], u[z] = u[z], u[i]
assert len(seq14) == 105 == (14 * 14 + 14) // 2 and u == [0] + list(range(14, 0, -1))
# témoin : la suite de Dudeney privée de son dernier coup ne renverse pas l'ordre
u = [0, 1, 2, 3, 4, 5, 6]
for g in seq[:-1]:
    i = u.index(g); z = u.index(0); u[i], u[z] = u[z], u[i]
assert u != [0, 6, 5, 4, 3, 2, 1]
print("contrôles : tout est conforme (témoins refusés)")
