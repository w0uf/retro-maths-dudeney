# -*- coding: utf-8 -*-
"""n° 83 DIGITAL MULTIPLICATION.

Avec les neuf chiffres employes une fois chacun, former DEUX multiplications de
meme produit. Dudeney demande celle dont la somme des chiffres du produit est
la plus petite, et celle ou elle est la plus grande. Il ajoute : « Il n'y a pas
d'autre moyen d'obtenir la solution que par essais effectifs. »
"""
from itertools import permutations, combinations

CH = "123456789"

def sol_toutes():
    vues = set()
    for p in permutations(CH):
        for i, j, k in combinations(range(1, 9), 3):
            a = int("".join(p[:i])); b = int("".join(p[i:j]))
            if a*b > 100000: continue
            c = int("".join(p[j:k])); d = int("".join(p[k:]))
            if a*b == c*d:
                cle = frozenset({(min(a,b), max(a,b)), (min(c,d), max(c,d))})
                if len(cle) == 2: vues.add((cle, a*b))
    return vues

S = sol_toutes()
print("=== Toutes les solutions ===")
print("  nombre de solutions distinctes : %d" % len(S))

def somme(n): return sum(int(c) for c in str(n))
par_somme = {}
for cle, prod in S:
    par_somme.setdefault(somme(prod), []).append((cle, prod))
print()
print("  somme des chiffres du produit -> nombre de solutions :")
for s in sorted(par_somme):
    print("     %2d : %3d solution(s)" % (s, len(par_somme[s])))
mini, maxi = min(par_somme), max(par_somme)
print()
print("=== Les deux extremes ===")
def montre(lst):
    for cle, prod in sorted(lst, key=lambda t: t[1]):
        (a, b), (c, d) = sorted(cle)
        print("     %d x %d = %d x %d = %d   (somme %d)" % (a, b, c, d, prod,
                                                            somme(prod)))
print("  somme minimale : %d" % mini); montre(par_somme[mini])
print("  somme maximale : %d" % maxi); montre(par_somme[maxi])

SIENNES = [((23, 174), (58, 69), 4002), ((9, 654), (18, 327), 5886)]
print()
print("=== Ses deux reponses ===")
for (a, b), (c, d), p in SIENNES:
    ok = a*b == p and c*d == p and \
         "".join(sorted(str(a)+str(b)+str(c)+str(d))) == CH
    print("  %d x %d = %d x %d = %d : valide %s, somme des chiffres %d"
          % (a, b, c, d, p, ok, somme(p)))
def valide(a, b, c, d):
    return a*b == c*d and "".join(sorted(str(a)+str(b)+str(c)+str(d))) == CH
print("  temoin 2 x 3 = 1 x 6 (quatre chiffres seulement) refuse :", not valide(2, 3, 1, 6))
print("  temoin 7 x 984 = 56 x 123 (neuf chiffres, produit 6 888) accepte :", valide(7, 984, 56, 123))
assert not valide(2, 3, 1, 6) and valide(7, 984, 56, 123)
print("  la plus petite somme est bien la sienne :",
      mini == somme(4002) and any(p == 4002 for _, p in par_somme[mini]))
print("  la plus grande aussi :",
      maxi == somme(5886) and any(p == 5886 for _, p in par_somme[maxi]))
print("  et elles sont uniques :", len(par_somme[mini]) == 1,
      "/", len(par_somme[maxi]) == 1)

# ═══ son exemple ═══════════════════════════════════════════════════════
print()
print("=== Son exemple d'introduction ===")
print("  7 x 658 = 14 x 329 = %d, somme des chiffres %d" % (7*658, somme(7*658)))
print("  « ni la plus haute ni la plus basse » :",
      somme(4606) not in (mini, maxi))

# ═══ la preuve par neuf ════════════════════════════════════════════════
print()
print("=== Une regularite qu'il ne signale pas ===")
r = sorted({somme(p) % 9 for _, p in S})
print("  restes modulo 9 des sommes rencontrees : %s" % r)
print("  toutes les sommes observees : %s" % sorted(par_somme))
