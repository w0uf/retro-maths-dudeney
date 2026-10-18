# -*- coding: utf-8 -*-
"""n° 65 THE RAILWAY STATION CLOCK.

Une horloge sur le mur d'une gare, mur long de 71 pieds 9 pouces et haut de
10 pieds 4 pouces. Les aiguilles pointent en sens opposes et sont paralleles a
l'une des diagonales du mur. Quelle heure exactement ?
"""
import math
from fractions import Fraction as F

LONG = 71*12 + 9        # 861 pouces
HAUT = 10*12 + 4        # 124 pouces
print("=== Le mur ===")
print("  %d pouces de long, %d de haut  (rapport %s)" % (LONG, HAUT, F(HAUT, LONG)))
diag = math.degrees(math.atan2(HAUT, LONG))
print("  ses diagonales font %.6f degres avec l'horizontale" % diag)

# ═══ les onze instants ou les aiguilles sont opposees ══════════════════
# minute t apres midi : aiguille des minutes a 6t degres, des heures a t/2.
# opposees : 5,5 t = 180 + 360 k
print()
print("=== Les onze instants ou les aiguilles sont opposees (en 12 heures) ===")
print("  heure exacte          angle de la ligne des aiguilles avec l'horizontale")
proches = []
for k in range(11):
    t = F(360 + 720*k, 11)                      # minutes apres midi
    h, m = divmod(t, 60)
    angle_vert = float(6*t) % 180               # angle avec la verticale
    angle_hor = abs(90 - angle_vert)
    ecart = abs(angle_hor - diag)
    marque = ""
    if ecart < 1:
        proches.append((t, angle_hor, ecart)); marque = "   <-- parallele a une diagonale"
    print("  %2d h %s min   %10.4f deg   (ecart %8.4f)%s"
          % (int(h), str(m) if m.denominator == 1 else "%d+%d/%d"
             % (m.numerator//m.denominator, m.numerator % m.denominator, m.denominator),
             angle_hor, ecart, marque))

# temoin : un mur carre (diagonales a 45 degres) ne doit designer aucun instant
carre = [k for k in range(11) if abs(abs(90 - float(6*F(360 + 720*k, 11)) % 180) - 45) < 1]
print("  temoin : un mur carre (45 deg) designe %d instant(s) -> %s"
      % (len(carre), "refuse" if not carre else "ERREUR"))
assert not carre and len(proches) == 2

print()
print("=== Combien de reponses ? ===")
print("  instants compatibles avec une diagonale : %d" % len(proches))
for t, a, e in proches:
    h, m = divmod(t, 60)
    print("     %d h %d + %d/%d min  (soit %s min apres l'heure)"
          % (int(h), m.numerator//m.denominator, m.numerator % m.denominator,
             m.denominator, m))
print("  Dudeney n'en donne qu'un : 43 + 7/11 min apres deux heures.")
print("  l'autre est son image dans un miroir vertical — et le mur a bien")
print("  DEUX diagonales.")

# ═══ « exactement » ? ══════════════════════════════════════════════════
print()
print("=== Le parallelisme est-il exact ? ===")
t = proches[0][0]
angle = proches[0][1]
print("  angle de la ligne des aiguilles : %.8f deg" % angle)
print("  angle de la diagonale du mur    : %.8f deg" % diag)
print("  ecart : %.6f deg, soit %.1f secondes d'arc"
      % (abs(angle-diag), abs(angle-diag)*3600))
haut_exact = LONG * math.tan(math.radians(angle))
long_exact = HAUT / math.tan(math.radians(angle))
print()
print("  pour que le parallelisme soit EXACT, il faudrait :")
print("     un mur de %d pouces de long et %.4f pouces de haut" % (LONG, haut_exact))
print("       soit %d pieds %.2f pouces  (il ecrit 10 pieds 4 pouces)"
      % (int(haut_exact//12), haut_exact % 12))
print("     ou un mur de %d pouces de haut et %.3f de long" % (HAUT, long_exact))
print("       soit %d pieds %.2f pouces  (il ecrit 71 pieds 9 pouces)"
      % (int(long_exact//12), long_exact % 12))
print("  il a donc arrondi : %.2f pouce de trop en hauteur." % (HAUT - haut_exact))

# ═══ la tolerance ══════════════════════════════════════════════════════
print()
print("=== Le mur pouvait-il etre tres different ? ===")
autres = sorted(abs(90 - (float(6*F(360+720*k, 11)) % 180)) for k in range(11))
rival = min(a for a in autres if a > angle + 1e-9)
print("  l'instant rival le plus proche fait %.4f deg avec l'horizontale" % rival)
limite = (angle + rival)/2
print("  tant que la diagonale du mur reste sous %.4f deg, c'est le meme" % limite)
print("  instant qui est designe : un rapport hauteur/longueur jusqu'a %.4f."
      % math.tan(math.radians(limite)))
print("  celui du mur vaut %.4f. Les dimensions sont donc beaucoup plus"
      % (HAUT/LONG))
print("  precises que necessaire — signe qu'il a cherche l'exactitude.")

# ═══ le parallelisme exact est-il seulement possible ? ═════════════════
print()
print("=== Un mur pourrait-il convenir EXACTEMENT ? ===")
print("  l'angle de la ligne des aiguilles vaut %s degres, soit pi/22 radians."
      % F(90, 11))
print("  le rapport hauteur/longueur devrait donc valoir tan(pi/22) = %.10f."
      % math.tan(math.pi/22))
print("  Or le theoreme de Niven (1956) dit que les seules valeurs")
print("  RATIONNELLES de la tangente d'un multiple rationnel de pi sont")
print("  0 et +/- 1. tan(pi/22) est donc irrationnel :")
print("  AUCUN mur mesure en pouces entiers — ni meme en nombres rationnels")
print("  de pouces — ne peut rendre le parallelisme exact.")
print("  Le sien s'en approche a %.1f secondes d'arc pres." % (abs(angle-diag)*3600))
