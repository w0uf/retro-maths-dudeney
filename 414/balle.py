# -*- coding: utf-8 -*-
"""n° 414 WHO WAS FIRST?
A un mille du tireur, on voit la fumee, on entend la detonation, on recoit la
balle : dans quel ordre ? La lumiere est instantanee a cette echelle ; tout se
joue entre la balle et le son.
Vitesse du son : formule usuelle 331,3 x racine(1 + T/273,15) m/s (air sec).
    python3 balle.py"""
MILE = 1609.344                       # metres
C = 299_792_458                       # lumiere, m/s
def son(T): return 331.3 * (1 + T / 273.15) ** .5

assert abs(son(20) - 343) < 1 and abs(son(0) - 331.3) < 1e-9      # temoins : valeurs de reference
for T in (0, 10, 15, 20):
    print("a %2d degres : son %.0f m/s, %.2f s pour un mille ; lumiere %.1f millioniemes de seconde"
          % (T, son(T), MILE / son(T), MILE / C * 1e6))
print("pour arriver avant la detonation, la balle doit tenir en moyenne plus de %.0f m/s sur le mille (a 15 degres)" % son(15))
