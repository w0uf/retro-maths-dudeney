# -*- coding: utf-8 -*-
"""n° 137 A STUDY IN THRIFT — Dudeney, 1917.

Trouver les cinq plus petits nombres superieurs a 36 qui puissent a la fois
former un carre, un triangle, deux triangles et trois triangles.
Dudeney donne le tableau : 36, 1225, 41616, 1413721, 48024900, 1631432881.
"""
from math import isqrt

T = lambda n: n*(n+1)//2
def est_carre(x):
    r = isqrt(x); return r if r*r == x else None
def est_triangle(x):
    d = 8*x + 1; r = isqrt(d)
    return (r-1)//2 if r*r == d and (r-1) % 2 == 0 else None

TABLE = [(36, 6, 8, (6,5), (5,5,3)),
         (1225, 35, 49, (36,34), (33,32,16)),
         (41616, 204, 288, (204,203), (192,192,95)),
         (1413721, 1189, 1681, (1189,1188), (1121,1120,560)),
         (48024900, 6930, 9800, (6930,6929), (6533,6533,3267)),
         (1631432881, 40391, 57121, (40391,40390), (38081,38080,19040))]

print("=== Son tableau, ligne par ligne ===")
for n, cs, ts, deux, trois in TABLE:
    c = est_carre(n); t = est_triangle(n)
    s2 = sum(T(x) for x in deux); s3 = sum(T(x) for x in trois)
    print("  %12d : carre de %-6s %s | triangle de %-6s %s | deux triangles %s | trois %s"
          % (n, c, "ok" if c == cs else "COTE ANNONCE %d" % cs,
             t, "ok" if t == ts else "COTE ANNONCE %d" % ts,
             "ok" if s2 == n else "FAUX : %d + %d = %d" % (T(deux[0]), T(deux[1]), s2),
             "ok" if s3 == n else "FAUX (%d)" % s3))

print("\n=== La ligne fautive, de plus pres ===")
n, cs, ts, deux, trois = TABLE[1]
print("  pour %d, il annonce deux triangles de cotes %d et %d :" % (n, *deux))
print("     T(%d) + T(%d) = %d + %d = %d  -> %s" % (deux[0], deux[1], T(deux[0]), T(deux[1]),
      T(deux[0])+T(deux[1]), "juste" if T(deux[0])+T(deux[1]) == n else "FAUX"))
bons = [(a, b) for a in range(1, 60) for b in range(1, a+1) if T(a)+T(b) == n]
print("  toutes les decompositions en deux triangles :", bons)
print("  la regle suivie par toutes les autres lignes est cote du carre + (cote - 1) :")
for x, cs2, ts2, d, _ in TABLE:
    print("     %12d : carre %6d -> %d + %d  %s" % (x, cs2, cs2, cs2-1,
          "ok" if T(cs2)+T(cs2-1) == x else "non"))

print("\n=== Les nombres carres ET triangulaires, dans l'ordre ===")
suite = []
k = 1
while len(suite) < 8:
    t = T(k)
    if est_carre(t): suite.append(t)
    k += 1
    if k > 200000: break
print("  ", suite)
print("  les siens sont-ils consecutifs dans cette suite :",
      suite[1:7] == [x[0] for x in TABLE])
print("\n  recurrence a(n) = 34 a(n-1) - a(n-2) + 2 :",
      all(suite[i] == 34*suite[i-1] - suite[i-2] + 2 for i in range(2, len(suite))))
print("  rapport d'un terme au precedent :",
      [round(suite[i]/suite[i-1], 3) for i in range(1, len(suite))])
print("\n  le sixieme cadeau vaut %.0f fois le premier." % (TABLE[5][0]/TABLE[0][0]))

print("\n=== Sa phrase glissee en passant : le theoreme d'Eureka ===")
print('  « Tout nombre entier est soit triangulaire, soit la somme de deux')
print('    nombres triangulaires, soit la somme de trois. »')
LIM = 200000
tri = []
k = 1
while T(k) <= LIM: tri.append(T(k)); k += 1
S = set(tri)
S2 = set()
for i, a in enumerate(tri):
    for b in tri[i:]:
        if a+b <= LIM: S2.add(a+b)
        else: break
S3 = set()
for x in S2:
    for a in tri:
        if x+a > LIM: break
        S3.add(x+a)
manquants = [n for n in range(1, LIM+1) if n not in S and n not in S2 and n not in S3]
print("  contre-exemples jusqu'a %d :" % LIM, manquants if manquants else "aucun")
print("  c'est le theoreme d'Eureka de Gauss (10 juillet 1796) ; Dudeney l'enonce")
print("  comme une evidence de salon, sans citer personne.")

from math import sqrt
print("\n  limite du rapport :", round(17 + 12*sqrt(2), 4))

# temoins : la ligne fautive doit etre refusee, les autres acceptees
print("\n=== Temoins ===")
fautives = [n for n, cs, ts, deux, trois in TABLE if sum(T(x) for x in deux) != n]
print("  lignes refusees par le controle des deux triangles :", fautives, "(attendu : [1225])")
print("  1225 corrige en 35 + 34 :", T(35) + T(34) == 1225)
print("  37 (36 mal lu) refuse comme triangulaire :", est_triangle(37) is None)
assert fautives == [1225] and T(35) + T(34) == 1225 and est_triangle(37) is None
assert suite[1:7] == [x[0] for x in TABLE] and not manquants
assert all(est_carre(n) == cs and est_triangle(n) == ts and sum(T(x) for x in trois) == n
           for n, cs, ts, deux, trois in TABLE)
