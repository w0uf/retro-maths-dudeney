#!/usr/bin/env python3
"""Rétro Math's — n° 364 THE BARREL PUZZLE (Dudeney, 1917).
Le plan qui joint la lèvre du haut au bord opposé du fond passe par le centre : il coupe un tonneau symétrique
en deux moitiés égales. Contrôle par tirage au hasard dans un tonneau renflé ; puis les poids de Bachet.
    python3 tonneau.py   (environ 3 s)"""
from itertools import permutations, product
from collections import deque, defaultdict
from fractions import Fraction as F
import random
print("=== 364 BARREL (Monte-Carlo, tonneau renflé r(z)=1-0.35 z², z∈[-1,1])")
import math
random.seed(1)
def part(theta,N=400000):
    # plan passant par la lèvre haute (x=+r1, z=1)... et le bord du fond opposé (x=-r1, z=-1): passe par O
    r1=1-0.35; nx,nz=-1.0, r1   # normale au plan contenant (r1,1) et (-r1,-1) et l'axe y
    ded=0;sous=0
    for _ in range(N):
        x=random.uniform(-1,1);y=random.uniform(-1,1);z=random.uniform(-1,1)
        if x*x+y*y<=(1-0.35*z*z)**2:
            ded+=1; sous+= (nx*x+nz*z)<0
    return sous/ded
P=part(0); print("part sous le plan lèvre–bord du fond:",round(P,4))
# Bachet
S=set()
for c in product((-1,0,1),repeat=4):
    S.add(sum(k*m for k,m in zip(c,(1,3,9,27))))
print("1,3,9,27 ->",sorted(x for x in S if x>0)==list(range(1,41)), "nb combinaisons",3**4,"=2*40+1")


# --- ce que dit le commentaire
assert abs(P - 0.5) < 0.003                                       # 50,1 % : l'écart est celui du tirage
assert sorted(x for x in S if x > 0) == list(range(1, 41)) and len(S) == 81
assert 3 - 1 == 2 and 27 + 3 - 9 - 1 == 20
# témoins : sur un verre évasé (pas de centre de symétrie), le plan qui joint la lèvre (x = 1, z = 1) au bord
# opposé du fond (x = -0,2, z = -1) ne coupe pas le volume en deux ; et des masses 1, 2, 4, 8 sur deux plateaux
# laissent des doublons
random.seed(2)
N = 200000; dedans = sous = 0
for _ in range(N):
    x, y, z = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
    if x * x + y * y <= (0.6 + 0.4 * z) ** 2:                     # verre évasé, plus large en haut
        dedans += 1; sous += (-2 * x + 1.2 * z + 0.8) > 0
assert abs(sous / dedans - 0.5) > 0.02
assert len({sum(k * m for k, m in zip(c, (1, 2, 4, 8))) for c in product((-1, 0, 1), repeat=4)}) < 81
print("contrôles : tout est conforme (témoins refusés)")
