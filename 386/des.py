#!/usr/bin/env python3
"""Rétro Math's — n° 386 A TRICK WITH DICE (Dudeney, 1917).
Doubler le premier dé, ajouter 5, multiplier par 5, ajouter le deuxième, multiplier par 10, ajouter le troisième :
le total moins 250 s'écrit avec les trois dés. Variantes à quatre dés et à dés de dix faces.
    python3 des.py   (instantané)"""
from itertools import permutations, product
from collections import deque, defaultdict
from fractions import Fraction as F
import random
print("=== 386 DICE")
T={}
for a,b,c in product(range(1,7),repeat=3):
    t=((2*a+5)*5+b)*10+c; assert t-250==100*a+10*b+c; T[t]=(a,b,c)
print("totaux distincts",len(T),min(T),max(T))
T4=set()
for a,b,c,d in product(range(1,7),repeat=4):
    t=(((2*a+5)*5+b)*10+c)*10+d; assert t-2500==1000*a+100*b+10*c+d; T4.add(t)
print("4 dés:",len(T4),min(T4),max(T4))
T10=set()
for a,b,c in product(range(10),repeat=3):
    t=((2*a+5)*5+b)*10+c; T10.add(t)
print("d10 0-9:",len(T10),min(T10),max(T10),"ex 0-0-7 ->",((2*0+5)*5+0)*10+7, "0-4-2 ->",((5)*5+4)*10+2)
# d10 numérotés 1 à 10 : collisions ?
T11=defaultdict(list)
for a,b,c in product(range(1,11),repeat=3): T11[((2*a+5)*5+b)*10+c].append((a,b,c))
print("d10 1-10: totaux distincts",len(T11),"sur 1000")


# --- ce que dit le commentaire
assert ((2 * 1 + 5) * 5 + 3) * 10 + 6 == 386 and 386 - 250 == 136
assert (len(T), min(T), max(T)) == (216, 361, 916) and (len(T4), min(T4), max(T4)) == (1296, 3611, 9166)
assert (len(T10), min(T10), max(T10)) == (1000, 250, 1249)
assert ((5) * 5 + 0) * 10 + 7 - 250 == 7 and ((5) * 5 + 4) * 10 + 2 - 250 == 42        # lire 007 et 042
assert all(((2 * a + 7) * 5 + b) * 10 + c - 350 == 100 * a + 10 * b + c for a, b, c in product(range(1, 7), repeat=3))
# témoin : sans le × 10 final, deux lancers différents donnent le même total
assert len({((2 * a + 5) * 5 + b) + c for a, b, c in product(range(1, 7), repeat=3)}) < 216
print("contrôles : tout est conforme (témoins refusés)")
