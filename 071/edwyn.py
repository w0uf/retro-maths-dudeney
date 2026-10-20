#!/usr/bin/env python3
"""Rétro Math's — n° 71 SIR EDWYN DE TUDOR (Dudeney, 1917).
À 15 milles à l'heure, une heure d'avance ; à 10, une heure de retard. La distance, et l'allure juste.
    python3 edwyn.py   (instantané)"""
from fractions import Fraction as F
def resoudre(v1, v2, avance, retard):
    """d/v1 = t - avance, d/v2 = t + retard ; rend (d, t, d/t)"""
    d = (avance + retard) / (F(1, v2) - F(1, v1)); t = d / v1 + avance
    return d, t, d / t
d, t, v = resoudre(15, 10, 1, 1)
print("distance", d, "milles ; temps juste", t, "h ; allure", v, "milles à l'heure")
assert (d, t, v) == (60, 5, 12)
assert v == F(2 * 10 * 15, 10 + 15)                         # la moyenne harmonique
assert all(resoudre(15, 10, k, k)[2] == 12 and resoudre(15, 10, k, k)[0] == 60 * k for k in (1, 2, 3))
a, b = 1, 3                                                 # une heure trop tôt, trois trop tard
assert resoudre(15, 10, a, b)[2] == F((a + b) * 15 * 10, a * 15 + b * 10)
assert F(2 * 10 * 25, 10 + 25) == 14 + F(2, 7)              # dix et vingt-cinq : pas entier
# témoin : la moyenne arithmétique, 12,5, ne fait pas arriver à l'heure
assert F(60) / F(25, 2) != t
print("contrôles : tout est conforme (témoins refusés)")
