#!/usr/bin/env python3
"""Rétro Math's — n° 314 THE SOUTHERN CROSS (Dudeney, 1917). 81 étoiles en carré 9×9,
cinq planètes ; toute étoile doit être en ligne (rangée, colonne, diagonale) avec une planète.
Cases : (rangée depuis le haut, colonne).
    python3 croix_du_sud.py   (environ 2 s ; les carrés plus grands sont dans croix_du_sud2.py)"""
from itertools import combinations, permutations
from collections import Counter
import time
N = 9; TOUT = (1 << N*N) - 1
def idx(l, c): return l*N + c
def ligne(a, b): return a[0]==b[0] or a[1]==b[1] or abs(a[0]-b[0])==abs(a[1]-b[1])
C = [(l, c) for l in range(N) for c in range(N)]
COUV = [sum(1 << idx(*y) for y in C if ligne(x, y)) for x in C]        # simple alignement (la case elle-même comprise)
def couv(S): 
    m = 0
    for s in S: m |= COUV[idx(*s)]
    return m
def couv_ecran(S):
    occ = set(S); m = 0
    for s in S:
        m |= 1 << idx(*s)
        for dl in (-1,0,1):
            for dc in (-1,0,1):
                if dl == dc == 0: continue
                x, y = s[0]+dl, s[1]+dc
                while 0 <= x < N and 0 <= y < N:
                    m |= 1 << idx(x, y)
                    if (x, y) in occ: break
                    x += dl; y += dc
    return m
depart = [(2,4),(3,3),(3,5),(4,4),(5,4)]
sol = [(0,4),(4,3),(5,7),(8,0),(1,8)]          # dans l'ordre des planètes de départ
m = couv(depart); manque = [x for x in C if not m >> idx(*x) & 1]
MANQUE = manque
print("départ : étoiles hors de toute ligne :", len(manque), manque, "| avec écran :", bin(TOUT & ~couv_ecran(depart)).count('1'))
print("solution de Dudeney : tout couvert ?", couv(sol) == TOUT, "| avec écran :", couv_ecran(sol) == TOUT,
      "| chaque planète bouge en ligne droite :", all(ligne(a, b) and a != b for a, b in zip(depart, sol)), "| cinq autres étoiles :", not set(sol) & set(depart))
t0 = time.time(); doms = []
n = N*N
for a in range(n):
    ma = COUV[a]
    for b in range(a+1, n):
        mb = ma | COUV[b]
        for c in range(b+1, n):
            mc = mb | COUV[c]
            for d in range(c+1, n):
                md = mc | COUV[d]
                if md == TOUT: 
                    for e in range(d+1, n): doms.append((a,b,c,d,e))
                    continue
                r = TOUT & ~md
                for e in range(d+1, n):
                    if not r & ~COUV[e]: doms.append((a,b,c,d,e))
print("dispositions de 5 planètes couvrant les 81 étoiles :", len(doms), "(%.0f s)" % (time.time()-t0))
T = [lambda l,c:(l,c), lambda l,c:(c,N-1-l), lambda l,c:(N-1-l,N-1-c), lambda l,c:(N-1-c,l), lambda l,c:(l,N-1-c), lambda l,c:(N-1-l,c), lambda l,c:(c,l), lambda l,c:(N-1-c,N-1-l)]
def canon(S): return min(tuple(sorted(t(*x) for x in S)) for t in T)
D = [tuple(divmod(i, N) for i in S) for S in doms]
fam = Counter(canon(S) for S in D)
print("familles à symétrie près :", len(fam), "| tailles :", dict(Counter(fam.values())))
print("   celles qui restent couvrantes avec écran :", sum(1 for S in D if couv_ecran(S) == TOUT))
QUATRE = any(True for S in combinations(range(n), 4) if (COUV[S[0]]|COUV[S[1]]|COUV[S[2]]|COUV[S[3]]) == TOUT)
print("quatre planètes peuvent-elles suffire ?", any(True for S in combinations(range(n), 4) if (COUV[S[0]]|COUV[S[1]]|COUV[S[2]]|COUV[S[3]]) == TOUT))
# le casse-tête : chaque planète bouge une fois en ligne droite
def atteignable(S, obliger_cinq_nouvelles):
    for p in permutations(S):
        if all(ligne(a, b) and a != b for a, b in zip(depart, p)): return True
    return False
cinq = [S for S in D if not set(S) & set(depart) and atteignable(S, True)]
print("solutions du casse-tête (5 planètes déplacées, 5 étoiles nouvelles) :", len(cinq), "| à symétrie près :", len({canon(S) for S in cinq}))
for S in cinq[:40]: print("   ", sorted(S), "← Dudeney" if sorted(S) == sorted(sol) else "")
def quatre_bougent(S):
    reste = set(S) & set(depart)
    if len(reste) != 1: return False
    fixe = next(iter(reste)); autres_d = [x for x in depart if x != fixe]; autres_s = [x for x in S if x != fixe]
    return any(all(ligne(a, b) and a != b for a, b in zip(autres_d, p)) for p in permutations(autres_s))
q = [S for S in D if quatre_bougent(S)]
print("solutions « plus faciles » (4 planètes déplacées, une reste) :", len(q), "| à symétrie près :", len({canon(S) for S in q}))
for S in q[:12]: print("   ", sorted(S))
MOINS = []
for k in (3, 2, 1):
    nb = 0
    for S in D:
        reste = set(S) & set(depart)
        if len(reste) == 5 - k:
            ad = [x for x in depart if x not in reste]; as_ = [x for x in S if x not in reste]
            if any(all(ligne(a, b) and a != b for a, b in zip(ad, p)) for p in permutations(as_)): nb += 1
    print("avec seulement", k, "planète(s) déplacée(s) :", nb); MOINS.append(nb)

# --- ce que dit l'article
assert len(MANQUE) == 10                                    # les dix etoiles pointees de la gravure
assert couv(sol) == TOUT and couv_ecran(sol) == TOUT and not set(sol) & set(depart)
assert len(doms) == 114 and len(fam) == 21 and not QUATRE
assert len(cinq) == 42 and sorted(sol) in [sorted(S) for S in cinq]
assert len(q) == 8 and all(len(set(S) & set(depart)) == 1 for S in q) and MOINS == [0, 0, 0]
# temoins : la croix de depart est refusee ; la solution du livre privee d'une planete aussi
assert couv(depart) != TOUT and couv(sol[:4]) != TOUT
print("controles : tout est conforme (temoins refuses)")
