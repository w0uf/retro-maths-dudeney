# -*- coding: utf-8 -*-
"""n° 127 SIMPLE DIVISION.
Trouver le plus grand diviseur qui laisse le meme reste dans 701, 1059, 1417 et
2312. Dudeney passe par le pgcd des six differences : 179, reste 164.
Ici, on essaie aussi tous les diviseurs, comme il le deconseille.
    python3 division.py"""
from math import gcd
from functools import reduce

def bons(N):
    """tous les diviseurs >= 2 qui laissent le meme reste dans tous les nombres de N"""
    return [d for d in range(2, max(N) + 1) if len({n % d for n in N}) == 1]

assert bons([7, 12, 17]) == [5] and bons([7, 12, 18]) == []          # temoins
N = [701, 1059, 1417, 2312]
six = [b - a for i, a in enumerate(N) for b in N[i + 1:]]
trois = [N[i + 1] - N[i] for i in range(3)]
print("six differences :", sorted(six), "-> pgcd", reduce(gcd, six))
print("trois differences entre voisins :", trois, "-> pgcd", reduce(gcd, trois))
print("restes par 179 :", [n % 179 for n in N])
print("essai direct de tous les diviseurs de 2 a 2312 :", bons(N), "-> le plus grand est aussi le seul")
print("chacun des quatre est un multiple de 179 moins 15 :", [(n + 15) // 179 for n in N], [(n + 15) % 179 for n in N])
print("essais en descendant depuis 700 avant de tomber sur 179 :", 700 - 179 + 1)
assert reduce(gcd, six) == reduce(gcd, trois) == 179 and bons(N) == [179] and {n % 179 for n in N} == {164}
