# -*- coding: utf-8 -*-
"""n° 128 A PROBLEM IN SQUARES — Dudeney, 1917.

Trois planches carrees : la premiere a cinq pieds carres de plus que la
deuxieme, la deuxieme cinq de plus que la troisieme.  Puis : trois carres
en progression arithmetique de raison 7, puis de raison 13.
Et son defi final : « Que le lecteur essaie maintenant le cas ou la raison
vaut 23.  C'est un os assez dur. »
"""
from fractions import Fraction as F
from math import isqrt, gcd

def carre(x):
    r = isqrt(x); return r*r == x

print("=== Les trois planches ===")
a, b, c = 31, 41, 49                     # en pouces
print("  cotes :", a, b, c, "pouces")
print("  aires :", a*a, b*b, c*c, "pouces carres")
print("  differences :", b*b-a*a, "et", c*c-b*b, "pouces carres")
print("  en pieds carres (144 pouces carres) :", F(b*b-a*a,144), "et", F(c*c-b*b,144))
print("  progression arithmetique de raison cinq :", b*b-a*a == c*c-b*b == 720)

print("\n=== Ses deux progressions de raison 7 et 13 ===")
for raison, trio in ((7, (113, 337, 463)), (13, (80929, 106921, 127729))):
    den = 120 if raison == 7 else 19380
    q = [F(x, den) for x in trio]
    d1 = q[1]**2 - q[0]**2; d2 = q[2]**2 - q[1]**2
    print("  raison %2d : %s  ->  differences %s et %s  | exact : %s"
          % (raison, trio, d1, d2, d1 == d2 == raison))

print("\n=== Sa remarque : en nombres entiers, la raison est multiple de 24 ===")
raisons = set()
for x in range(1, 400):
    for y in range(x+1, 500):
        d = y*y - x*x
        z2 = y*y + d
        if z2 > 260000: break
        if carre(z2): raisons.add(d)
print("  raisons entieres trouvees :", sorted(raisons)[:12], "...")
print("  toutes divisibles par 24 :", all(r % 24 == 0 for r in raisons))
print("  (c'est pourquoi 5, 7, 13 et 23 exigent des fractions)")

# --- son defi : la raison 23 -------------------------------------------
print("\n=== Son defi : la raison 23 ===")
print("  Trois carres rationnels en progression de raison d <=> un triangle")
print("  rectangle a cotes rationnels d'aire d.  (Si les cotes sont u, v, w,")
print("  alors ((v-u)/2)^2, (w/2)^2, ((u+v)/2)^2 sont en progression de raison uv/2.)")

def racine(fr):
    n, d = fr.numerator, fr.denominator
    a, b = isqrt(n), isqrt(d)
    return F(a, b) if a*a == n and b*b == d else None

# le triangle d'aire 23 (verifie ci-dessous de bout en bout)
u = F(80155, 20748); v = F(41496, 3485)
w = racine(u*u + v*v)
print("\n  triangle : %s , %s , %s" % (u, v, w))
print("    Pythagore :", u*u + v*v == w*w, " | aire :", u*v/2)

x = (v-u)/2; y = w/2; z = (u+v)/2
print("\n  les trois nombres dont les carres sont en progression :")
for nom, q in (("petit", x), ("moyen", y), ("grand", z)):
    print("     %-6s %s" % (nom, q))
print("    denominateur commun :", x.denominator == y.denominator == z.denominator,
      "->", x.denominator)
print("    numerateurs :", x.numerator, y.numerator, z.numerator)
print("    carres :", x*x, "|", y*y, "|", z*z)
print("    differences :", y*y - x*x, "et", z*z - y*y,
      "-> raison 23 :", y*y - x*x == z*z - y*y == 23)

print("\n  taille des reponses, raison par raison :")
for d, num, den in ((5, [31,41,49], 12), (7, [113,337,463], 120),
                    (13, [80929,106921,127729], 19380),
                    (23, [x.numerator, y.numerator, z.numerator], x.denominator)):
    print("    raison %2d : numerateurs a %2d chiffres, denominateur a %2d chiffres"
          % (d, len(str(max(num))), len(str(den))))

# le triangle primitif d'ou il vient
from math import gcd
den = 72306780
A = u.numerator * (den // u.denominator); B = v.numerator * (den // v.denominator)
g = gcd(A, B); A //= g; B //= g
print("\n  triangle primitif correspondant : cotes %d et %d" % (A, B))
# m, n tels que A = m^2 - n^2 et B = 2mn  (ou l'inverse)
for (p, q) in ((A, B), (B, A)):
    s = isqrt((p + isqrt(p*p + q*q)) // 2) if False else None
C = isqrt(A*A + B*B)
m = isqrt((C + A)//2); n = isqrt((C - A)//2)
if m*m - n*n == A and 2*m*n == B:
    print("  engendre par m = %d et n = %d" % (m, n))
    print("  -> une recherche par (m, n) aurait du aller jusqu'a %d, pas jusqu'a 6 000." % m)

# --- temoins -------------------------------------------------------------
def progression(nums, den, raison):
    q = [F(x, den) for x in nums]
    return q[1]**2 - q[0]**2 == raison and q[2]**2 - q[1]**2 == raison
print("\n=== Temoins ===")
print("  raison 7 avec 113 lu 114 :", "refuse" if not progression((114,337,463),120,7) else "ACCEPTE")
print("  raison 23 avec un numerateur altere d'une unite :",
      "refuse" if not progression((x.numerator+1, y.numerator, z.numerator), x.denominator, 23) else "ACCEPTE")
u2 = F(80155, 20749)
print("  triangle avec 20748 lu 20749 : hypotenuse rationnelle ?", racine(u2*u2 + v*v) is not None, "-> refuse")
assert not progression((114,337,463),120,7) and progression((113,337,463),120,7)
assert not progression((x.numerator+1, y.numerator, z.numerator), x.denominator, 23)
assert progression((x.numerator, y.numerator, z.numerator), x.denominator, 23)
assert racine(u2*u2 + v*v) is None and all(r % 24 == 0 for r in raisons)
