# -*- coding: utf-8 -*-
"""n° 90 THE CENTURY PUZZLE.

Ecrire 100 sous la forme d'un nombre fractionnaire employant les neuf chiffres
une fois chacun. « Le regrette mathematicien francais Edouard Lucas en trouva
sept facons et doutait qu'il y en eut d'autres. En realite il y en a exactement
onze, et pas une de plus. »
"""
from itertools import permutations, combinations
import math

CH = "123456789"

def solutions(cible=100):
    out = []
    # la partie entiere a au plus autant de chiffres que la cible : au-dela de
    # 100, elle peut en avoir trois (la premiere version s'arretait a deux)
    for la in range(1, len(str(cible)) + 1):
        for da in permutations(CH, la):
            a = int("".join(da))
            k = cible - a
            if k <= 0: continue
            reste = [c for c in CH if c not in da]
            for lc in range(1, len(reste)):
                for dc in permutations(reste, lc):
                    c = int("".join(dc))
                    b = k * c
                    sb = str(b)
                    if len(sb) != len(reste) - lc: continue
                    if sorted(sb) == sorted(x for x in reste if x not in dc):
                        out.append((a, b, c))
    return out

S = solutions()
print("=== Toutes les solutions, par recherche exhaustive ===")
print("  nombre de solutions : %d" % len(S))
for a, b, c in sorted(S, key=lambda t: (-t[0], t[1])):
    print("   %2d + %5d/%-4d   (tous les chiffres : %s)"
          % (a, b, c, "".join(sorted(str(a)+str(b)+str(c))) == CH))

SIENNES = [(96,2148,537),(96,1752,438),(96,1428,357),(94,1578,263),
           (91,7524,836),(91,5823,647),(91,5742,638),(82,3546,197),
           (81,7524,396),(81,5643,297),(3,69258,714)]
print()
print("=== Sa liste de onze ===")
print("  toutes valides :", all(a + b/c == 100 and
      "".join(sorted(str(a)+str(b)+str(c))) == CH for a, b, c in SIENNES))
print("  identiques a celles du programme :", sorted(SIENNES) == sorted(S))
print("  « onze et pas une de plus » :", len(S) == 11)

# ═══ sa loi des racines numeriques ═════════════════════════════════════
def racine(n): return 9 if n % 9 == 0 else n % 9
print()
print("=== Sa loi des racines numeriques ===")
print("  « pour 96 + 4, les racines du numerateur et du denominateur seront")
print("    toutes deux 6 ; pour 94 + 6 : 3 et 2 ; pour 91 + 9 et 82 + 18 :")
print("    9 et 8 ; pour 81 + 19 : 9 et 9 ; pour 3 + 97 : 3 et 3. »")
annonce = {96: (6,6), 94: (3,2), 91: (9,8), 82: (9,8), 81: (9,9), 3: (3,3)}
bon = True
for a, b, c in sorted(S, key=lambda t: -t[0]):
    r = (racine(b), racine(c))
    if a in annonce and r != annonce[a]: bon = False
    print("   %2d : racines %d et %d   %s" % (a, r[0], r[1],
          "conforme" if a in annonce and r == annonce[a] else ""))
print("  ses six annonces sont exactes :", bon)
print()
print("  la raison : les neuf chiffres font 45, donc a + b + c est divisible")
print("  par 9. Avec b = k c et a = 100 - k, cela force c modulo 9, donc b.")
for a, b, c in S:
    assert (a + b + c) % 9 == 0
print("  verifie sur les %d solutions : a + b + c est toujours multiple de 9."
      % len(S))

# ═══ ses eliminations ══════════════════════════════════════════════════
print()
print("=== Ses eliminations, mises a l'epreuve ===")
parties = sorted({a for a, b, c in S})
print("  parties entieres qui marchent : %s" % parties)
print("  « le nombre entier ne peut pas aller de 12 a 23 inclus » : %s"
      % (not any(12 <= a <= 23 for a in parties)))
for a in (98, 92, 97, 86, 83, 74, 89, 79, 88, 77, 90, 80):
    print("     %2d : %s" % (a, "aucune solution" if a not in parties
                             else "SOLUTION TROUVEE"))

# ═══ 100 est-il un nombre privilegie ? ═════════════════════════════════
print()
print("=== 100 est-il particulierement riche ? ===")
compte = {}
for t in range(1, 201):
    compte[t] = len(solutions(t))
best = sorted(compte.items(), key=lambda kv: -kv[1])[:10]
print("  les dix cibles les plus riches entre 1 et 200 :")
for t, n in best:
    print("     %3d : %3d facons %s" % (t, n, "<-- le sien" if t == 100 else ""))
rang = 1 + sum(1 for t, n in compte.items() if n > compte[100])
print("  rang de 100 : %d sur 200" % rang)

# ═══ temoins ═══════════════════════════════════════════════════════════
def ecriture(a, b, c, cible=100):
    return a * c + b == cible * c and "".join(sorted(str(a) + str(b) + str(c))) == CH
print()
print("=== Temoins ===")
print("  96 + 2148/537 accepte :", ecriture(96, 2148, 537))
print("  96 + 2148/538 refuse  :", not ecriture(96, 2148, 538))
print("  94 + 1578/236 (bons chiffres, mauvaise valeur) refuse :", not ecriture(94, 1578, 236))
print("  50 + 50/1 (chiffres repetes) refuse :", not ecriture(50, 50, 1))
assert ecriture(96, 2148, 537) and not ecriture(96, 2148, 538)
assert not ecriture(94, 1578, 236) and not ecriture(50, 50, 1)
assert all(ecriture(a, b, c) for a, b, c in S)
# au-dela de 100 la partie entiere peut avoir trois chiffres : sans eux, on en perd
s197 = solutions(197)
print("  197 : %d facons, dont %d avec une partie entiere de trois chiffres"
      % (len(s197), sum(1 for a, b, c in s197 if a >= 100)))
assert len(S) == 11 and compte[89] == 36 and rang == 36
