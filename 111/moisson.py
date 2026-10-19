# -*- coding: utf-8 -*-
"""n° 111 REAPING THE CORN.
Un champ carre ; le fermier fauche une bande d'une perche (rod) tout autour, et
il reste un carre de la moitie de l'aire. Dudeney : 46.626 perches carrees, cote
interieur 4.8284, aire interieure 23.313, soit .2914 acre.
Valeur exacte : cote 4 + 2 racine(2), aire 24 + 16 racine(2).
    python3 moisson.py"""
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 30
r2 = D(2).sqrt()
cote = 4 + 2 * r2; aire = cote * cote; dedans = cote - 2
arr = lambda x, n: x.quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)
assert abs(dedans * dedans - aire / 2) < D("1e-25")
print("cote exact      %s" % cote)
print("aire exacte     %s   arrondie a 3 decimales : %s   livre : 46.626" % (aire, arr(aire, 3)))
print("cote interieur  %s   arrondi a 4 decimales  : %s   livre : 4.8284" % (dedans, arr(dedans, 4)))
print("aire interieure %s   arrondie a 3 decimales : %s   livre : 23.313" % (dedans * dedans, arr(dedans * dedans, 3)))
print("en acres (160 perches carrees) : %s   livre : .2914" % arr(aire / 160, 4))
assert arr(dedans, 4) == D("4.8284") and arr(aire / 160, 4) == D("0.2914")
assert arr(aire, 3) == D("46.627") and arr(dedans * dedans, 3) == D("23.314")     # ses deux aires : un millieme de trop peu

print("\nd'ou viennent ses deux aires :")
c = D("4.8284")
print("  4.8284 au carre = %s -> %s (son 23.313)" % (c * c, arr(c * c, 3)))
print("  le double de 23.313 = %s (son 46.626)" % (2 * D("23.313")))
print("  temoin : le grand cote arrondi, 6.8284, au carre = %s -> %s, ce n'est pas son nombre"
      % (D("6.8284") ** 2, arr(D("6.8284") ** 2, 3)))
assert arr(c * c, 3) == D("23.313") and 2 * D("23.313") == D("46.626") and arr(D("6.8284") ** 2, 3) != D("46.626")
print("\nl'autre racine de s^2 - 8 s + 8 = 0 : %s, moins de deux perches : pas de carre interieur" % (4 - 2 * r2))
