# -*- coding: utf-8 -*-
"""n° 136 THE SULTAN'S ARMY.

« Un sultan voulait envoyer au combat une armee qu'on put ranger en deux carres
parfaits de douze facons differentes. Quel est le plus petit effectif ? »
Dudeney donne la reponse, et surtout tout un cours d'arithmetique : les nombres
premiers 4n+1, ceux qui sont somme de deux carres, la facon de compter les
decompositions. On verifie chacune de ses affirmations.
"""
import math
from collections import defaultdict

LIM = 400_000

# r(n) : nombre de facons d'ecrire n = a^2 + b^2 avec a >= b >= 1.
# (Convention de Dudeney, lisible dans son propre exemple : 130 compte pour
#  deux — 81+49 et 121+9 — et 25 pour une seule, 16+9, donc le carre NUL est
#  exclu ; mais 50 compte pour deux, 49+1 et 25+25, donc a = b est admis.)
r = defaultdict(int)
racine = defaultdict(list)
amax = math.isqrt(LIM)
for a in range(1, amax + 1):
    aa = a*a
    if aa + 1 > LIM: break
    for b in range(1, a + 1):
        n = aa + b*b
        if n > LIM: break
        r[n] += 1
        racine[n].append((a, b))

print("=== Sa convention, relue sur ses propres exemples ===")
for n in (130, 25, 50, 45, 15, 135, 5, 65, 1105, 32045, 125, 625, 3125):
    print("  %6d -> %d facon(s)  %s" % (n, r[n], racine[n] if r[n] <= 3 else ""))

# temoins comptes a la main dans son texte : 130 = 81+49 = 121+9, 25 = 16+9, 50 = 49+1 = 25+25, 15 jamais
assert (r[130], r[25], r[50], r[15]) == (2, 1, 2, 0)
print("  temoins a la main (130 : 2, 25 : 1, 50 : 2, 15 : 0) : conformes")

print()
print("=== Ses lois, mises a l'epreuve ===")
def premier(n):
    if n < 2: return False
    for d in range(2, math.isqrt(n)+1):
        if n % d == 0: return False
    return True
p1 = [p for p in range(2, 200) if premier(p) and p % 4 == 1]
p3 = [p for p in range(2, 200) if premier(p) and p % 4 == 3]
print("  tout premier 4n+1 est somme de deux carres, d'une seule facon :",
      all(r[p] == 1 for p in p1), "  (%d premiers testes)" % len(p1))
print("  aucun premier 4n-1 ne l'est                                  :",
      all(r[p] == 0 for p in p3), "  (%d premiers testes)" % len(p3))
print("  5, 65, 1105, 32045 : %d, %d, %d, %d facons — le double a chaque"
      " nouveau facteur : %s" % (r[5], r[65], r[1105], r[32045],
      r[65] == 2*r[5] and r[1105] == 2*r[65] and r[32045] == 2*r[1105]))
print("  25, 125, 625, 3125 : %d, %d, %d, %d — la repetition suit une autre loi :"
      " %s" % (r[25], r[125], r[625], r[3125],
      [r[5**k] for k in range(1, 8)]))
print("  15 et 135 impossibles (%d, %d), 45 possible d'une seule facon (%d) : %s"
      % (r[15], r[135], r[45], r[15] == 0 and r[135] == 0 and r[45] == 1))

# « le facteur 2 n'affecte jamais le nombre de solutions, sauf quand il double
#   un carre » : on teste la loi exacte r(2n) = r(n) + [n carre parfait]
def carre(n): return math.isqrt(n)**2 == n
def double_carre(n): return n % 2 == 0 and carre(n//2)
# loi naive, celle qu'on croit lire chez lui
naifs = [n for n in range(1, LIM//2)
         if r[2*n] != r[n] + (1 if carre(n) else 0)]
# loi exacte
exacts = [n for n in range(1, LIM//2)
          if r[2*n] != r[n] + (1 if carre(n) else 0) - (1 if double_carre(n) else 0)]
print("  loi du facteur 2. Il ecrit : doubler ne change rien, SAUF quand cela")
print("     double un carre — 25 donne une facon, 50 en donne deux. Exact.")
print("     mais il manque la moitie de la regle : quand n est le DOUBLE d'un")
print("     carre, doubler fait PERDRE une facon. 50 -> %d, 100 -> %d."
      % (r[50], r[100]))
print("     loi telle qu'on la lit chez lui : %d contre-exemples sous %d"
      % (len(naifs), LIM//2))
print("     loi complete r(2n) = r(n) + [n carre] - [n double d'un carre] : %d"
      % len(exacts))
print("     cas ou il perd une facon, sous %d : %d"
      % (LIM//2, sum(1 for n in range(1, LIM//2) if double_carre(n) and not carre(n))))

print()
print("=== La reponse au probleme du sultan ===")
douze = [n for n in range(1, LIM) if r[n] == 12]
petit = douze[0]
print("  (le nombre lui-meme n'est pas imprime ici : c'est la reponse.)")
print("  nombre d'entiers strictement plus petits ayant douze facons : %d"
      % len([n for n in range(1, petit) if r[n] == 12]))
print("  et en ayant PLUS de douze : %d"
      % len([n for n in range(1, petit) if r[n] > 12]))
print("  -> « le plus petit » est donc sans ambiguite : aucun effectif")
print("     inferieur ne se range en deux carres de douze facons, ni de plus.")
print("  ses douze paires sont-elles exactes et completes ?")
siennes = [tuple(sorted(p, reverse=True)) for p in
           [(400,15),(399,32),(393,76),(392,81),(384,113),(375,140),
            (360,175),(356,183),(337,216),(329,228),(311,252),(265,300)]]
ok = all(a*a+b*b == petit for a, b in siennes)
print("     les douze sommes valent bien son nombre :", ok)
print("     et ce sont exactement celles que trouve le programme :",
      sorted(siennes) == sorted(racine[petit]))

# et si l'on acceptait le carre nul ?
r0 = defaultdict(int)
for a in range(1, amax + 1):
    if a*a > LIM: break
    r0[a*a] += 1                      # n = a^2 + 0^2
for n, v in r.items(): r0[n] += v
douze0 = next(n for n in range(1, LIM) if r0[n] == 12)
print()
print("=== Et si le carre nul etait admis ? ===")
print("  la reponse changerait : elle serait %s que la sienne."
      % ("plus petite" if douze0 < petit else "plus grande"))
print("  l'enonce ne dit pas qu'un carre doit contenir au moins un homme ;")
print("  c'est son exemple des 130 hommes qui fixe la convention.")
