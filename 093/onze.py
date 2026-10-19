# -*- coding: utf-8 -*-
"""n° 93 THE MYSTIC ELEVEN — parmi tous les nombres de neuf chiffres formés de
neuf des dix chiffres (0 compris), lesquels sont divisibles par 11 ?
Dudeney annonce 102 347 586 comme le plus petit et 987 652 413 comme le plus grand."""
from itertools import permutations
from collections import Counter

petit, grand, total = None, None, 0
par_omis = Counter()
for omis in range(10):
    chiffres = [c for c in "0123456789" if c != str(omis)]
    for p in permutations(chiffres):
        if p[0] == "0": continue
        n = int("".join(p))
        if n % 11 == 0:
            total += 1; par_omis[omis] += 1
            if petit is None or n < petit: petit = n
            if grand is None or n > grand: grand = n
print("nombres de 9 chiffres distincts divisibles par 11 :", total)
print("le plus petit :", format(petit, ",").replace(",", " "),
      "  (Dudeney : 102 347 586)", petit == 102347586)
print("le plus grand :", format(grand, ",").replace(",", " "),
      "  (Dudeney : 987 652 413)", grand == 987652413)
print()
print("chiffre omis → combien de nombres :", dict(sorted(par_omis.items())))
print("le chiffre omis dans le plus petit :", [c for c in "0123456789" if c not in str(petit)])
print("le chiffre omis dans le plus grand :", [c for c in "0123456789" if c not in str(grand)])

# ── le témoin de l'énoncé et la règle de Dudeney ─────────────────────────
print()
t = 896743012
print("le témoin de l'énoncé", t, ": divisible par 11 ?", t % 11 == 0)
s = str(t)
impairs = sum(int(c) for c in s[0::2]); pairs = sum(int(c) for c in s[1::2])
print("   somme des rangs impairs :", impairs, " des rangs pairs :", pairs,
      " différence :", impairs - pairs)
for n in (petit, grand):
    s = str(n)
    a = sum(int(c) for c in s[0::2]); b = sum(int(c) for c in s[1::2])
    print("   %d : %d et %d, différence %d (multiple de 11 : %s)"
          % (n, a, b, a-b, (a-b) % 11 == 0))

# ── la règle « étendue » était-elle nécessaire ? ─────────────────────────
from itertools import permutations
mx0 = None
for omis in range(10):
    ch = [c for c in "0123456789" if c != str(omis)]
    for p in permutations(ch):
        if p[0] == "0": continue
        a = sum(int(c) for c in p[0::2]); b = sum(int(c) for c in p[1::2])
        if a == b:
            n = int("".join(p))
            if mx0 is None or n > mx0: mx0 = n
print()
print("le plus grand avec une différence NULLE :", format(mx0, ",").replace(",", " "))
print("le plus grand tout court                :", format(grand, ",").replace(",", " "))
print("la règle étendue (différence multiple de 11) était donc indispensable :",
      grand > mx0)

# ── temoins : la regle des rangs doit refuser un nombre non divisible ─────
def regle(n):
    s = str(n)
    return (sum(int(c) for c in s[0::2]) - sum(int(c) for c in s[1::2])) % 11 == 0
print()
for n in (896743012, 896743021, 102347568, 987652413):
    print("  %d : regle des rangs %-5s | reste de la division par 11 : %d"
          % (n, regle(n), n % 11))
assert regle(896743012) and not regle(896743021) and not regle(102347568)
assert all(regle(n) == (n % 11 == 0) for n in range(10**8, 10**8 + 200000))
print("  la regle et la division concordent sur 200 000 nombres consecutifs")
assert total == 296640 and petit == 102347586 and grand == 987652413 and mx0 == 987645230
