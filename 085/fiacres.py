#!/usr/bin/env python3
"""Rétro Math's — n° 85 THE CAB NUMBERS (Dudeney, 1917).
Deux nombres qui emploient à eux deux les neuf chiffres 1 à 9 une fois chacun, et dont le produit les emploie aussi
une fois chacun : le plus grand produit possible. Essai de toutes les permutations et de toutes les coupes.
    python3 fiacres.py   (environ 10 s)"""
import itertools, math
from collections import Counter
print("=== 85. Fiacres ===")
NEUF = set("123456789"); couples = []
for perm in itertools.permutations("123456789"):
    for k in range(1, 5):
        a = int("".join(perm[:k])); b = int("".join(perm[k:]))
        p = str(a * b)
        if len(p) == 9 and set(p) == NEUF: couples.append((a * b, a, b))
couples.sort()
print("   couples :", len(couples), "| par taille du petit facteur :", dict(sorted(Counter(len(str(a)) for _, a, b in couples).items())))
print("   plus grand :", couples[-1], "| suivants :", couples[-4:-1])
print("   plus petit :", couples[0])
print("   facteurs tous multiples de 3 :", all(a % 3 == 0 and b % 3 == 0 for _, a, b in couples),
      "| l'un des deux multiple de 9 :", all(a % 9 == 0 or b % 9 == 0 for _, a, b in couples),
      "| les deux multiples de 9 :", sum(a % 9 == 0 and b % 9 == 0 for _, a, b in couples))
print("   produits distincts :", len({p for p, a, b in couples}), "| doublons :", [c for c in couples if [x[0] for x in couples].count(c[0]) > 1])
print("   a un chiffre :", [(a, b, p) for p, a, b in couples if a < 10])
print("   a deux chiffres, les 6 plus grands :", [(a, b, p) for p, a, b in couples if 10 <= a < 100][-6:])
print("   plus gros produit sans contrainte : 9642 x 87531 =", 9642 * 87531, "| 96 x 8745231 =", 96 * 8745231)
best = max((int("".join(p[:k])) * int("".join(p[k:])), int("".join(p[:k])), int("".join(p[k:]))) for p in itertools.permutations("123456789") for k in range(1, 5))
print("   maximum sans la 3e contrainte :", best)
for k in (1, 2, 3, 4): print("   coupe %d+%d : candidats %d, dont multiples de 3 des deux cotes %d" % (k, 9-k,
      math.perm(9, 9), sum(1 for p in itertools.permutations("123456789") if int("".join(p[:k])) % 3 == 0 and int("".join(p[k:])) % 3 == 0)))


# --- contrôles
assert couples[-1] == (839542176, 96, 8745231)                       # son « je crois » : c'est bien le plus grand
assert 96 * 8745231 == 839542176 and sorted(str(839542176)) == list("123456789")
assert len(couples) == 1625 and couples[0] == (123547968, 48, 2573916)
assert all(a % 3 == 0 and b % 3 == 0 for _, a, b in couples)       # les deux facteurs toujours multiples de 3
assert best == (843973902, 9642, 87531)                              # sans exiger les neuf chiffres au produit, on irait plus haut
# témoin : ce produit plus grand n'emploie pas les neuf chiffres une fois chacun, il est bien refusé
assert sorted(str(843973902)) != list("123456789")
print("contrôles : tout est conforme (témoins refusés)")
