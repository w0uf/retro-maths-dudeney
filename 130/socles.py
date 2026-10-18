# -*- coding: utf-8 -*-
"""n° 130 THE SCULPTOR'S PROBLEM.

Deux socles cubiques INEGAUX dont le nombre de pieds lineaires (la somme des
deux aretes) egale le nombre de pieds cubes (la somme des deux volumes).
Trouver les dimensions « dans les plus petits chiffres possibles ».

    x^3 + y^3 = x + y,  x != y, x et y > 0
    (x+y)(x^2 - xy + y^2) = x + y   =>   x^2 - xy + y^2 = 1
"""
import math, os
from fractions import Fraction
from math import gcd

def ok(x, y): return x**3 + y**3 == x + y

# ═══ 1. « la reponse doit etre fractionnaire » ═══════════════════════════
print("=== Sa premiere affirmation : la reponse ne peut pas etre entiere ===")
ent = [(x, y) for x in range(1, 60) for y in range(1, x) if ok(x, y)]
print("  couples d'entiers distincts jusqu'a 60 qui conviennent :", ent)
print("  raison : x^3 >= x des que x >= 1, avec egalite pour x = 1 seulement ;")
print("  la somme ne peut donc coller que si x = y = 1 — et les socles sont")
print("  INEGAUX. Son affirmation est exacte, et se demontre en une ligne.")

# ═══ 2. « un numerateur plus grand, l'autre plus petit que le denominateur »
print()
print("=== Sa deuxieme affirmation : un socle depasse le pied, l'autre non ===")
print("  x^2 - xy + y^2 = (x-y)^2 + xy. Si x et y sont tous deux <= 1 et")
print("  distincts, cette quantite est < 1 ; s'ils sont tous deux >= 1, elle")
print("  est > 1. Il en faut donc un de chaque cote. Verification numerique :")
mauvais = 0
for i in range(1, 200):
    for j in range(1, 200):
        x, y = Fraction(i, 100), Fraction(j, 100)
        if x == y: continue
        v = x*x - x*y + y*y
        if (x <= 1 and y <= 1 and v >= 1) or (x >= 1 and y >= 1 and v <= 1):
            mauvais += 1
print("  contre-exemples sur %d couples testes : %d" % (199*199, mauvais))
x, y = Fraction(1, 2), Fraction(3, 4)            # temoin : deux socles sous le pied
print("  temoin 1/2 et 3/4 : x^2 - xy + y^2 = %s < 1, donc refuse par l'equation :" % (x*x - x*y + y*y), not ok(x, y))
assert x*x - x*y + y*y < 1 and not ok(x, y)

# ═══ 3. la plus petite solution ════════════════════════════════════════
print()
print("=== Sa reponse est-elle la plus petite ? ===")
sols = []
for d in range(1, 301):
    hmax = int(d * 2 / math.sqrt(3)) + 1
    for p in range(1, hmax + 1):
        for q in range(1, p):
            if p*p - p*q + q*q == d*d and gcd(gcd(p, q), d) == 1:
                sols.append((d, p, q))
sols.sort()
print("  solutions reduites, denominateur <= 300 : %d" % len(sols))
print("  les cinq plus petits denominateurs :", sorted({s[0] for s in sols})[:5])
print("  (les fractions elles-memes ne sont pas imprimees : c'est la reponse.)")
d0 = sols[0][0]
print("  aucun denominateur inferieur a %d ne donne de solution : %s"
      % (d0, not any(s[0] < d0 for s in sols)))
print("  nombre de solutions a ce plus petit denominateur : %d"
      % sum(1 for s in sols if s[0] == d0))
print("  -> il y en a deux ; il retient celle aux plus petits numerateurs,")
print("     et c'est bien « dans les plus petits chiffres possibles ».")

# ═══ 4. sa recette de fabrication ══════════════════════════════════════
print()
print("=== Sa recette a generateurs ===")
print("  « trois generateurs a > b > c ; denominateur ab + c^2 ; numerateurs")
print("    a^2 - c^2, b^2 - c^2 et a^2 - b^2. »")
def recette(a, b, c):
    d = a*b + c*c
    return d, (a*a - c*c, b*b - c*c, a*a - b*b)
def teste(a, b, c):
    d, (u, v, w) = recette(a, b, c)
    paires = [(u, v), (u, w), (v, w)]
    return [(p, q) for p, q in paires
            if Fraction(p, d)**3 + Fraction(q, d)**3 == Fraction(p, d) + Fraction(q, d)
            and p != q]
for trio in ((3, 2, 1), (4, 3, 2), (5, 4, 3), (4, 3, 1), (5, 3, 2), (5, 4, 1)):
    a, b, c = trio
    bonnes = teste(a, b, c)
    print("  generateurs %d, %d, %d  (a = b + c : %-5s) -> %d paire(s) valable(s)"
          % (a, b, c, a == b + c, len(bonnes)))
tous = [(a, b, c) for a in range(2, 40) for b in range(1, a) for c in range(1, b)]
sans = [t for t in tous if not teste(*t)]
avec = [t for t in tous if t[0] == t[1] + t[2]]
print("  triplets a > b > c avec a < 40 : %d" % len(tous))
print("     qui ne donnent AUCUNE paire valable : %d" % len(sans))
print("     qui verifient a = b + c            : %d" % len(avec))
print("     parmi ces derniers, ceux qui echouent : %d"
      % len([t for t in avec if not teste(*t)]))
print("  -> sa recette est juste, mais il manque une condition qu'il ne dit")
print("     pas : le plus grand generateur doit etre la somme des deux autres.")

# ═══ 5. son exemple « plein de neuf » ══════════════════════════════════
print()
print("=== Son exemple a rallonge ===")
P, Q, D = 99999999, 19999, 99990001
x, y = Fraction(P, D), Fraction(Q, D)
print("  %d/%d  et  %d/%d" % (P, D, Q, D))
print("  p^2 - pq + q^2 = %d" % (P*P - P*Q + Q*Q))
print("  d^2            = %d" % (D*D))
print("  egaux :", P*P - P*Q + Q*Q == D*D)
print("  x^3 + y^3 = x + y :", x**3 + y**3 == x + y)
print("  fraction irreductible :", gcd(gcd(P, Q), D) == 1)
# d'ou vient-il ?
for b in range(1, 20001):
    c = None
    disc = 4*D - 3*b*b
    if disc < 0: break
    r = math.isqrt(disc)
    if r*r == disc and (r - b) % 2 == 0 and (r - b)//2 > 0:
        c = (r - b)//2
        if b > c:
            print("  il sort des generateurs a = %d, b = %d, c = %d (a = b + c)"
                  % (b + c, b, c))
            break

# ═══ 6. la loi des denominateurs ═══════════════════════════════════════
print()
print("=== « Le denominateur est un premier 6n+1, ou un produit de tels » ===")
def facteurs(n):
    f, d = [], 2
    while d*d <= n:
        while n % d == 0: f.append(d); n //= d
        d += 1
    if n > 1: f.append(n)
    return f
dd = sorted({s[0] for s in sols})
faux = [d for d in dd if any(p % 6 != 1 for p in facteurs(d))]
print("  denominateurs reduits trouves (<= 300) : %s ..." % dd[:12])
print("  ceux dont un facteur premier n'est pas de la forme 6n+1 : %d" % len(faux))
print("  ses exemples permis : 13 ->", facteurs(13), "| 19 ->", facteurs(19),
      "| interdits : 25 ->", facteurs(25), "| 55 ->", facteurs(55), "| 187 ->", facteurs(187))
print("  13 et 19 sont atteints :", 13 in dd and 19 in dd, "| 25, 55, 187 jamais :", not {25, 55, 187} & set(dd))
print("  -> exact. Mais attention : la recette peut sortir un denominateur")
print("     comme 21 (= 3 x 7) — c'est qu'il n'est pas reduit.")
assert 21 in [d for d in range(1, 30) if any(p % 6 != 1 for p in facteurs(d))]   # temoin : 21 est bien signale
d21, (u21, v21, w21) = recette(5, 4, 1)
print("     generateurs 5, 4, 1 : denominateur %d, numerateurs %s"
      % (d21, (u21, v21, w21)), "-> se simplifient par %d" % gcd(gcd(u21, v21), d21))

# les quatre triplets qui marchent sans respecter la condition
ex = [t for t in tous if teste(*t) and t[0] != t[1] + t[2]]
print()
print("  les triplets qui marchent SANS a = b + c :", ex)
print("  (tous multiples d'un meme triplet ; une seule paire au lieu de deux,")
print("   et elle redonne une solution deja obtenue.)")

# ═══ 7. la gravure est-elle d'accord avec la reponse ? ═══════════════════
try:
    from PIL import Image
    import numpy as np
    g = np.array(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q130.png')).convert('L')) < 110
    def runs(v):
        o=[]; deb=None
        for i,b in enumerate(v):
            if b and deb is None: deb=i
            elif not b and deb is not None: o.append((deb,i-1)); deb=None
        return [r for r in o if r[1]-r[0] >= 1]
    gauche = runs(g[300]); droite = runs(g[280])
    lg = gauche[2][0] - gauche[1][1]          # x = 24..148
    ld = droite[5][0] - droite[4][1]          # x = 258..355
    print()
    print("=== La gravure montre-t-elle ce que la reponse exige ? ===")
    print("  face avant du socle de gauche : environ %d px de large" % lg)
    print("  face avant du socle de droite : environ %d px de large" % ld)
    print("  rapport dessine : %.2f" % (lg/ld))
    d0, p0, q0 = sols[0]
    print("  rapport exige par la reponse : %.2f" % (p0/q0))
    print("  -> « de tailles inegales, comme on le voit sur l'illustration » :")
    print("     l'ecart dessine est bien plus doux que celui qu'il faut.")
except Exception as e:
    print("  (gravure non mesuree : %s)" % e)
