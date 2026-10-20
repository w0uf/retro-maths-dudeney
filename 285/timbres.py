"""Rétro Math's — n° 285 THE FOUR POSTAGE STAMPS (Dudeney, 1917).
Planche de 3 × 4 timbres : de combien de façons détacher quatre timbres qui tiennent ensemble par les côtés ?
Énumération complète, classement par formes, puis la planche 4 × 4.
    python3 timbres.py   (instantané)"""
from itertools import combinations
from collections import Counter
C=[(r,c) for r in range(3) for c in range(4)]
def connexe(s):
    s=set(s); v={next(iter(s))}; p=list(v)
    while p:
        r,c=p.pop()
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(r+d[0],c+d[1])
            if q in s and q not in v: v.add(q); p.append(q)
    return len(v)==len(s)
def norm(s):
    r0=min(r for r,c in s); c0=min(c for r,c in s); return tuple(sorted((r-r0,c-c0) for r,c in s))
def images(s, retourne=True):
    out=[]; t=list(s)
    for k in range(4):
        t=[(c,-r) for r,c in t]; out.append(norm(t))
        if retourne: out.append(norm([(r,-c) for r,c in t]))
    return out
L=[s for s in combinations(C,4) if connexe(s)]
print("total",len(L), "sur", len(list(combinations(C,4))))
libre=Counter(min(images(s)) for s in L); fixe=Counter(norm(s) for s in L); uni=Counter(min(images(s,False)) for s in L)
print("formes libres",len(libre),sorted(libre.values())); print("unilatérales",len(uni),sorted(uni.values())); print("orientées",len(fixe))
for f,n in libre.items(): print(n,f)
# non connexes par les côtés mais se touchant par un coin ?

def compte(H,W):
    C=[(r,c) for r in range(H) for c in range(W)]
    L=[s for s in combinations(C,4) if connexe(s)]
    lib=Counter(min(images(s)) for s in L)
    return len(L), dict(lib), L
R={}
for H,W in ((3,4),(4,4)):
    n,lib,L=compte(H,W); R[(H,W)]=(n,sorted(lib.values())); print(H,W,n,sorted(lib.values()))
    # détail par orientation : boîte englobante couchée/debout
    d=Counter()
    for s in L:
        f=norm(s); h=max(r for r,c in f)+1; w=max(c for r,c in f)+1
        d[(min(images(s)),h,w)]+=1
    for k,v in sorted(d.items()): print("  ",k[0],f"boîte {k[1]}x{k[2]}",v)
# le groupe 1,2,7,8 : tient-il seulement par un coin ?
print(connexe([(0,0),(0,1),(1,2),(1,3)]))

# --- ce que dit le commentaire
assert R[(3, 4)][0] == 65 and len(list(combinations(C, 4))) == 495
assert len(libre) == 5 and sorted(libre.values()) == [3, 6, 14, 14, 28]              # barre, carré, T, S, L
assert len(uni) == 7                                                                   # les sept pièces de Tetris
assert R[(3, 4)] == (65, [3, 6, 14, 14, 28]) and R[(4, 4)] == (113, [8, 9, 24, 24, 48])
# témoin : le groupe 1, 2, 7, 8 ne tient que par un coin, il est refusé ; le groupe 1, 2, 6, 7 (le S) est accepté
assert not connexe([(0, 0), (0, 1), (1, 2), (1, 3)]) and connexe([(0, 0), (0, 1), (1, 1), (1, 2)])
print("contrôles : tout est conforme (témoins refusés)")
