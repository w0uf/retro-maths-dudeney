# -*- coding: utf-8 -*-
"""n° 46 MARY AND MARMADUKE.
Marmaduke : « dans sept ans, nos ages feront 63 ». Mary : « j'ai aujourd'hui l'age
que tu avais quand j'avais la moitie de l'age que tu as. » Dudeney : 29 ans 2/5
et 19 ans 3/5. On cherche tous les couples d'ages, a differents pas de temps.
    python3 ages.py"""
from fractions import Fraction as F

def couples(somme, pas):
    """ages (lui, elle) multiples de 1/pas, de somme `somme`, verifiant la phrase de Mary"""
    out = []
    for m in range(1, somme * pas):
        M = somme * pas - m
        # quand elle avait m - (M - m) = 2m - M, il avait m ; elle a m = 2 (2m - M)
        if M > m and m == 2 * (2 * m - M): out.append((F(M, pas), F(m, pas)))
    return out

for pas, nom in ((1, "annees"), (12, "mois"), (5, "cinquiemes d'annee"), (60, "soixantiemes")):
    print("pas : %-20s -> %s" % (nom, [(str(a), str(b)) for a, b in couples(63 - 14, pas)]))
assert couples(49, 12) == [] and couples(49, 60) == [(F(147, 5), F(98, 5))]
M, m = F(147, 5), F(98, 5)
print("Dudeney : 29 2/5 et 19 3/5 :", (M, m) == (29 + F(2, 5), 19 + F(3, 5)), "; dans sept ans :", M + m + 14)

print("\nsommes annoncees de 55 a 75 qui donnent des ages en annees entieres :")
ok = [S for S in range(55, 76) if couples(S - 14, 1)]
print("  ", [(S, [(int(a), int(b)) for a, b in couples(S - 14, 1)]) for S in ok])
assert ok == [59, 64, 69, 74]          # temoin positif : 64 tombe juste en annees, 63 non
