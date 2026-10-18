# -*- coding: utf-8 -*-
"""n° 1 A POST-OFFICE PERPLEXITY — Dudeney, 1917.

« Donnez-moi pour une couronne de timbres, des timbres a deux pence, six fois
plus de timbres a un penny, et le reste en timbres a deux pence et demi. »
Une couronne = 60 pence = 120 demi-pence.
(Le script de l'atelier a ete perdu ; celui-ci le refait.)
"""

def cout(x, y, z):
    """valeur en demi-pence de x timbres a 2 d, y a 1 d, z a 2 d 1/2"""
    return 4 * x + 2 * y + 5 * z

def convient(x, y, z):
    return y == 6 * x and cout(x, y, z) == 120

# temoin : une commande fausse doit etre refusee
assert convient(5, 30, 8)
assert not convient(5, 30, 9) and not convient(4, 24, 9) and not convient(6, 30, 8)
print("temoins : (5, 30, 9), (4, 24, 9) et (6, 30, 8) refuses ; (5, 30, 8) accepte")

# balayage complet : x timbres a 2 d, 6x a 1 d, z a 2 d 1/2, soit 16x + 5z = 120
sols = [(x, 6 * x, z) for x in range(0, 121) for z in range(0, 121) if convient(x, 6 * x, z)]
print("\nsolutions entieres de 16x + 5z = 120 :", sols)
assert sols == [(0, 0, 24), (5, 30, 8)]
print("la solution nulle (aucun timbre a 2 d) est exclue par l'enonce :")
print("« donnez-moi DES timbres a deux pence ». Reste celle de Dudeney :")
x, y, z = sols[1]
print("  %d a 2 d, %d a 1 d, %d a 2 d 1/2 = %d pence" % (x, y, z, cout(x, y, z) // 2))
print("\nle verrou : 5z = 120 - 16x impose x multiple de 5, et x = 10 depasse la couronne")
