# -*- coding: utf-8 -*-
"""n° 419 THE FIVE PENNIES.
Placer cinq pennies de sorte que chacun touche les quatre autres. Dudeney dit
« a egale distance » ; pris au sens propre, entre les centres, c'est impossible.
Le determinant de Cayley-Menger de n points s'annule si et seulement si ces
points tiennent dans un espace de dimension n - 2.
    python3 pennies.py"""
from fractions import Fraction

def det(A):
    A = [[Fraction(x) for x in r] for r in A]; n = len(A); d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return Fraction(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            for k in range(c, n): A[r][k] -= f * A[c][k]
    return d

def cayley_menger(D2):
    """D2 : carres des distances"""
    n = len(D2)
    return det([[0] + [1] * n] + [[1] + list(D2[i]) for i in range(n)])

def carres(points):
    return [[sum((a - b) ** 2 for a, b in zip(p, q)) for q in points] for p in points]

# temoins : des points qui tiennent dans la bonne dimension donnent 0
carre = [(0, 0), (1, 0), (1, 1), (0, 1)]                       # 4 points d'un plan
cube = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]  # 5 points de l'espace
print("temoins : 4 sommets d'un carre ->", cayley_menger(carres(carre)),
      "; 5 sommets d'un cube ->", cayley_menger(carres(cube)))
assert cayley_menger(carres(carre)) == 0 and cayley_menger(carres(cube)) == 0

for n in (3, 4, 5):
    D2 = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    v = cayley_menger(D2)
    print("%d points deux a deux a la distance 1 : determinant %s -> ils ne tiennent pas en dimension %d"
          % (n, v, n - 2))
    assert v != 0
print("\nQuatre points equidistants ne tiennent pas dans un plan, cinq pas dans l'espace :")
print("cinq pennies ne se touchent tous que grace a leur forme plate, pas par leurs centres.")
print("vue d'en haut, la quatrieme piece posee sur trois : son centre est a %.3f rayon de chacun" % (2 / 3 ** .5))
