# -*- coding: utf-8 -*-
"""n° 88 DIGITAL DIVISION — Dudeney, Amusements in Mathematics (1917).

Ranger les neuf chiffres 1 a 9 en deux groupes tels que l'un divise l'autre
exactement.  Dudeney donne les huit quotients de 2 a 9, et annonce pour
chacun « la plus petite paire de nombres possible ».
"""
from collections import Counter, defaultdict

CHIFFRES = "123456789"
def racine(n):                    # racine numerique
    return 1 + (n-1) % 9 if n else 0

sols = defaultdict(list)
for num in range(1234, 9877):
    s = str(num)
    if len(set(s)) != 4 or "0" in s: continue
    for k in range(2, 10):
        den = num*k
        if len(str(den)) != 5: continue
        if sorted(s + str(den)) == list(CHIFFRES):
            sols[k].append((num, den))

SIENNES = {2:(6729,13458), 3:(5823,17469), 4:(3942,15768), 5:(2697,13485),
           6:(2943,17658), 7:(2394,16758), 8:(3187,25496), 9:(6381,57429)}

print("=== Toutes les solutions, quotient par quotient ===")
for k in range(2, 10):
    L = sorted(sols[k])
    mini = L[0]
    print("\n  1/%d : %d solution(s)" % (k, len(L)))
    print("        les siennes : %d/%d" % SIENNES[k],
          "-> valide :", SIENNES[k] in L)
    print("        la plus petite : %d/%d" % mini,
          "-> c'est la sienne :", mini == SIENNES[k])
    if len(L) <= 12: print("       ", ["%d/%d" % x for x in L])

print("\n=== Ses racines numeriques ===")
for k in range(2, 10):
    formes = sorted({(racine(n), racine(d)) for n, d in sols[k]})
    print("  1/%d : formes %s" % (k, formes))
print("\n  il annonce 9-9 pour 3,4,6,7,9 :",
      all({(racine(n),racine(d)) for n,d in sols[k]} == {(9,9)} for k in (3,4,6,7,9)))
print("  il annonce 6-3 (ou 3-6) pour 2 et 5 :",
      all({(racine(n),racine(d)) for n,d in sols[k]} <= {(6,3),(3,6)} for k in (2,5)))
print("  il annonce les cinq formes pour 8 :",
      len({tuple(sorted(x)) for x in {(racine(n),racine(d)) for n,d in sols[8]}}))

print("\n=== Ses petites remarques d'elimination ===")
print("  le 5 n'est jamais le dernier chiffre du numerateur :",
      all(str(n)[-1] != "5" for k in sols for n, d in sols[k]))
print("  le 1 non plus :",
      all(str(n)[-1] != "1" for k in sols for n, d in sols[k]))
print("  pour 1/6, le 6 n'est jamais le dernier chiffre du numerateur :",
      all(str(n)[-1] != "6" for n, d in sols[6]))
print("  pour 1/5, le dernier chiffre du numerateur n'est jamais pair :",
      all(int(str(n)[-1]) % 2 for n, d in sols[5]))

print("\n=== Le tableau complet ===")
print("  nombre total de solutions :", sum(len(v) for v in sols.values()))
for k in range(2, 10):
    print("   1/%d : %2d" % (k, len(sols[k])))

print("\n=== Sa regle sur le 1 : contre-exemples ===")
mauvais = [(k, n, d) for k in sols for n, d in sols[k] if str(n)[-1] == "1"]
for k, n, d in sorted(mauvais):
    print("   1/%d : %d/%d  <- numerateur termine par 1%s"
          % (k, n, d, "   *** C'EST SA PROPRE REPONSE ***" if (n, d) == SIENNES[k] else ""))
print("   au total :", len(mauvais), "solutions sur", sum(len(v) for v in sols.values()))
print("   sa regle sur le 5 est exacte car 5k se termine par 0 ou 5 ;")
print("   mais 1 multiplie par k se termine par k, ce qui ne gene rien.")

# ═══ temoins et controles ════════════════════════════════════════════════
def partage(num, den, k):
    """num x k = den, et les neuf chiffres 1-9 employes une fois chacun"""
    return num * k == den and sorted(str(num) + str(den)) == list(CHIFFRES)
print("\n=== Temoins ===")
print("  6729 x 2 = 13458 accepte :", partage(6729, 13458, 2))
print("  1234 x 2 = 2468 (chiffres manquants) refuse :", not partage(1234, 2468, 2))
print("  6729 x 3 = 20187 (zero, chiffres repetes) refuse :", not partage(6729, 20187, 3))
assert partage(6729, 13458, 2) and not partage(1234, 2468, 2) and not partage(6729, 20187, 3)
# le partage 4/5 est le seul : force brute sur toutes les longueurs de numerateur
from itertools import permutations
tous = set()
for p in permutations(CHIFFRES):
    s = "".join(p)
    for i in range(1, 9):
        n, d = int(s[:i]), int(s[i:])
        if d % n == 0 and 2 <= d // n <= 9: tous.add((n, d))
print("  force brute, toutes coupures confondues : %d solutions,"
      " toutes de la forme 4/5 chiffres : %s"
      % (len(tous), all(len(str(n)) == 4 for n, d in tous)))
assert tous == {x for k in sols for x in sols[k]} and len(tous) == 89
assert all(sorted(sols[k])[0] == SIENNES[k] for k in SIENNES) and len(mauvais) == 16
