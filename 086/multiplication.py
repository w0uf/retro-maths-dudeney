# -*- coding: utf-8 -*-
"""n° 86 QUEER MULTIPLICATION.
51 249 876 x 3 = 153 749 628 : multiplicateur et multiplicande prennent les neuf
chiffres une fois, le produit aussi. Avec 6 pour multiplicateur, Dudeney donne
32 547 891 x 6 = 195 287 346, sans dire combien il y en a.
On essaie, pour chaque multiplicateur de 2 a 9, les 40 320 arrangements des
huit autres chiffres.
    python3 multiplication.py          (quelques secondes)"""
from itertools import permutations

NEUF = set("123456789")

def convient(n, m):
    """n (huit chiffres) et m (un chiffre) prennent les neuf chiffres, et n x m aussi"""
    return set(str(n) + str(m)) == NEUF and len(str(n)) == 8 and \
           len(str(n * m)) == 9 and set(str(n * m)) == NEUF

sols = {}
for m in range(2, 10):
    sols[m] = [int("".join(p)) for p in permutations(sorted(NEUF - {str(m)}))
               if convient(int("".join(p)), m)]
    print("multiplicateur %d : %3d solutions%s" % (m, len(sols[m]),
          "  (ex. %d x %d = %d)" % (sols[m][0], m, sols[m][0] * m) if sols[m] else ""))

print("\nexemples de l'enonce et du corrige :")
for n, m in ((51249876, 3), (16583742, 9), (32547891, 6)):
    print("   %d x %d = %d : %s ; dans la liste : %s" % (n, m, n * m, convient(n, m), n in sols[m]))
    assert convient(n, m) and n in sols[m]
# temoins : deux chiffres permutes dans la reponse du corrige -> refuses
for n in (32547819, 23547891):
    print("   temoin %d x 6 = %d : %s" % (n, n * 6, "refuse" if not convient(n, 6) else "ERREUR : accepte"))
    assert not convient(n, 6)

print("\nLa preuve par neuf dit pourquoi seuls 3, 6 et 9 marchent : le produit contient")
print("les neuf chiffres, donc est multiple de 9 ; le multiplicande vaut 45 - m modulo 9,")
print("donc m x (45 - m) = -m^2 doit etre multiple de 9, ce qui demande 3 | m.")
print("   m tels que m^2 soit multiple de 9 :", [m for m in range(2, 10) if m * m % 9 == 0])
assert [m for m in sols if sols[m]] == [3, 6, 9]
assert (len(sols[3]), len(sols[6]), len(sols[9])) == (336, 87, 144)
