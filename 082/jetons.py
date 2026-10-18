# -*- coding: utf-8 -*-
"""n° 82 THE TEN COUNTERS.

Les dix jetons 0 a 9, chacun une fois, repartis entre DEUX multiplications de
meme produit. Trouver la paire qui donne le plus petit produit, et celle qui
donne le plus grand. Le zero ne peut pas etre en tete d'un nombre.
"""
from itertools import combinations, permutations

CH = "0123456789"

def cotes(digits):
    """toutes les facons de former deux nombres avec ces chiffres"""
    out = set()
    for p in permutations(digits):
        for i in range(1, len(p)):
            if p[0] == "0" or p[i] == "0": continue
            a, b = int("".join(p[:i])), int("".join(p[i:]))
            out.add((min(a, b), max(a, b)))
    return out

# ═══ 1. la repartition des chiffres est-elle forcee ? ══════════════════
print("=== Combien de chiffres de chaque cote ? ===")
for k in range(2, 6):
    petits = []
    for d in combinations(CH, k):
        petits += [a*b for a, b in cotes(d)]
    grands = []
    for d in combinations(CH, 10-k):
        grands += [a*b for a, b in cotes(d)]
    print("  %d chiffres d'un cote, %d de l'autre : produits de %d a %d"
          " contre %d a %d  ->  %s"
          % (k, 10-k, min(petits), max(petits), min(grands), max(grands),
             "impossible" if max(petits) < min(grands) or max(grands) < min(petits)
             else "possible"))
print("  -> les dix jetons doivent se partager CINQ et CINQ. Dudeney ne le")
print("     dit nulle part, et c'est pourtant la premiere chose a etablir.")

# ═══ 2. toutes les solutions ═══════════════════════════════════════════
sols = []
for d in combinations(CH, 5):
    autre = tuple(c for c in CH if c not in d)
    if d > autre: continue          # on ne compte chaque partage qu'une fois
    A = {}
    for a, b in cotes(d): A.setdefault(a*b, []).append((a, b))
    for c, e in cotes(autre):
        p = c*e
        if p in A:
            for a, b in A[p]:
                sols.append((p, (a, b), (c, e)))
print()
print("=== Toutes les solutions ===")
print("  nombre de solutions : %d" % len(sols))
produits = sorted({p for p, _, _ in sols})
print("  produits possibles : %d valeurs, de %d a %d"
      % (len(produits), produits[0], produits[-1]))

def montre(p):
    for q, (a, b), (c, e) in sols:
        if q == p:
            print("     %d x %d = %d x %d = %d" % (a, b, c, e, p))
print()
print("=== Les deux extremes ===")
print("  plus petit produit : %d" % produits[0]); montre(produits[0])
print("  plus grand produit : %d" % produits[-1]); montre(produits[-1])

SIENNES = [((3485, 2), (6970, 1), 6970), ((915, 64), (732, 80), 58560)]
print()
print("=== Ses deux reponses ===")
for (a, b), (c, e), p in SIENNES:
    ok = a*b == p and c*e == p and \
         "".join(sorted(str(a)+str(b)+str(c)+str(e))) == CH
    print("  %d x %d = %d x %d = %d : valide %s" % (a, b, c, e, p, ok))
t = "".join(sorted("3045" + "2" + "6090" + "1"))
print("  temoin 3045 x 2 = 6090 x 1 (deux zeros, pas de 7 ni de 8) refuse :", t != CH)
assert t != CH
print("  le plus petit est bien le sien :", produits[0] == 6970)
print("  le plus grand est bien le sien :", produits[-1] == 58560)

# ═══ 3. son raisonnement sur le plus petit ═════════════════════════════
print()
print("=== Son raisonnement sur le plus petit produit ===")
print("  « il faut prendre pour multiplicateurs les deux plus petits nombres")
print("    possibles, 1 et 2, puis ranger les huit jetons restants en deux")
print("    nombres dont l'un soit le double de l'autre. »")
paires = [(n, 2*n) for n in range(1000, 5000)
          if "".join(sorted(str(n)+str(2*n))) ==
             "".join(sorted(c for c in CH if c not in "12"))]
print("  couples (n, 2n) employant les huit autres chiffres : %s"
      % ", ".join("%d et %d" % x for x in paires))
print("  le plus petit est %d — il annonce 3 485 : %s"
      % (paires[0][0], paires[0][0] == 3485))
print("  et il precise que 3 045, 3 405, 3 450 ne conviennent pas :")
for n in (3045, 3405, 3450):
    print("     %d x 2 = %d -> chiffres %s : %s" % (n, 2*n,
          "".join(sorted(str(n)+str(2*n))),
          "convient" if "".join(sorted(str(n)+str(2*n))) ==
          "".join(sorted(c for c in CH if c not in "12")) else "non"))
