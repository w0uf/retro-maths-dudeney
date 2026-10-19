# -*- coding: utf-8 -*-
"""n° 363 THE DOCTOR'S QUERY — Dudeney, 1917.

Deux flacons : dix onces d'alcool dans l'un, dix onces d'eau dans l'autre. On
verse un quart d'once d'alcool dans l'eau, on agite, puis on reverse un quart
d'once du melange dans l'alcool. Quelle est la proportion d'alcool et d'eau
dans chaque flacon ?
(Le script de l'atelier a ete perdu ; celui-ci le refait, en fractions exactes.)
"""
from fractions import Fraction as F

def transvase(alcool=F(10), eau=F(10), aller=F(1, 4), retour=F(1, 4), part_alcool_retour=None):
    """retourne (alcool, eau) du flacon 1 et (alcool, eau) du flacon 2.
    part_alcool_retour : proportion d'alcool dans ce qu'on reverse ; None = le
    melange bien agite du flacon 2."""
    f1 = [alcool - aller, F(0)]                     # flacon d'alcool
    f2 = [aller, eau]                               # flacon d'eau
    if part_alcool_retour is None:
        part_alcool_retour = f2[0] / (f2[0] + f2[1])
    a, e = retour * part_alcool_retour, retour * (1 - part_alcool_retour)
    f1 = [f1[0] + a, f1[1] + e]
    f2 = [f2[0] - a, f2[1] - e]
    return f1, f2

(a1, e1), (a2, e2) = transvase()
print("=== Le probleme du medecin ===")
print("  flacon d'alcool : %s d'alcool, %s d'eau -> %s contre 1" % (a1, e1, a1 / e1))
print("  flacon d'eau    : %s d'alcool, %s d'eau -> 1 contre %s" % (a2, e2, e2 / a2))
print("  autant d'eau dans l'alcool que d'alcool dans l'eau :", e1 == a2)
assert (a1, e1) == (F(400, 41), F(10, 41)) and a1 / e1 == 40 and e2 / a2 == 40 and e1 == a2

print("\n=== Le theoreme cache : toujours autant de l'un que de l'autre ===")
print("  (chaque flacon retrouve son volume ; ce qui manque d'alcool a ete")
print("   remplace par autant d'eau, et cet alcool est dans l'autre flacon)")
for alcool, eau, q in ((F(10), F(10), F(1, 4)), (F(10), F(3), F(2)), (F(7, 2), F(20), F(1, 3))):
    (a1, e1), (a2, e2) = transvase(alcool, eau, q, q)
    print("  %s oz d'alcool, %s oz d'eau, %s oz aller-retour : eau dans l'alcool %s,"
          " alcool dans l'eau %s -> egales : %s" % (alcool, eau, q, e1, a2, e1 == a2))
    assert e1 == a2

print("\n=== Et l'agitation ne sert a rien ===")
for p, nom in ((F(0), "eau pure"), (F(1, 5), "1/5 d'alcool"), (F(1, 2), "moitie-moitie"), (F(1), "alcool pur")):
    (a1, e1), (a2, e2) = transvase(part_alcool_retour=p)
    print("  on reverse %-14s : eau dans l'alcool %-6s alcool dans l'eau %-6s egales : %s"
          % (nom, e1, a2, e1 == a2))
    assert e1 == a2

# temoin : si les volumes ne sont pas retablis, l'egalite doit tomber
print("\n=== Temoin ===")
(a1, e1), (a2, e2) = transvase(retour=F(1, 8))
print("  aller 1/4, retour 1/8 seulement : eau dans l'alcool %s, alcool dans l'eau %s"
      " -> egalite : %s (refusee)" % (e1, a2, e1 == a2))
assert e1 != a2
