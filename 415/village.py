# -*- coding: utf-8 -*-
"""n° 415 A WONDERFUL VILLAGE — un village où le soleil est, à midi, plus proche
des habitants de 3 000 milles et plus qu'à son lever ou à son coucher.
Dudeney répond que c'est vrai partout, le rayon terrestre valant près de
4 000 milles. Voyons de plus près."""
import math

R_KM = 6371.0                       # rayon terrestre moyen
MILLE = 1.609344                    # un mille terrestre en kilomètres
R = R_KM / MILLE
print("rayon de la Terre : %.0f km = %.0f milles" % (R_KM, R))
print("Dudeney : « le demi-diamètre terrestre vaut près de 4 000 milles » →",
      "juste" if 3900 < R < 4000 else "à revoir")

# ── l'écart exact : R × cos(distance zénithale à midi) ──────────────────
print()
print("à l'horizon, l'observateur est à la même distance du soleil que le centre")
print("de la Terre ; à midi, il en est plus proche de R × cos z, où z est la")
print("distance zénithale du soleil à midi.")
seuil = math.degrees(math.acos(3000/R))
print("l'écart dépasse 3 000 milles tant que cos z > %.4f, c'est-à-dire z < %.1f °"
      % (3000/R, seuil))

# ── et au Japon ? ──────────────────────────────────────────────────────
print()
LAT = 35.0                          # latitude moyenne du Japon habité
print("pour un village japonais à %.0f ° de latitude nord :" % LAT)
print("  date            | déclinaison | z à midi | écart (milles) | > 3 000 ?")
for nom, decl in (("solstice d'été", 23.44), ("équinoxes", 0.0),
                  ("1er novembre", -14.2), ("solstice d'hiver", -23.44)):
    z = abs(LAT - decl)
    e = R * math.cos(math.radians(z))
    print("  %-15s | %+8.2f °  | %6.1f ° | %13.0f | %s"
          % (nom, decl, z, e, "oui" if e > 3000 else "NON"))

# ── combien de temps dans l'année la phrase est-elle vraie ? ────────────
print()
decl_min = LAT - seuil
print("il faut z = |lat - déclinaison| < %.1f °, donc déclinaison > %.1f °"
      % (seuil, decl_min))
jours = 0
for j in range(365):
    d = 23.44 * math.sin(math.radians(360/365.24 * (j - 80)))   # approximation
    if abs(LAT - d) < seuil: jours += 1
print("nombre de jours de l'année où l'affirmation tient, à %.0f ° de latitude : %d"
      % (LAT, jours))
print("→ elle est FAUSSE pendant %d jours, soit près de %d mois." % (365-jours, round((365-jours)/30.4)))

# ── où la phrase est-elle vraie toute l'année ? ─────────────────────────
print()
for lat in range(0, 61, 5):
    ok = all(abs(lat - 23.44*math.sin(math.radians(360/365.24*(j-80)))) < seuil
             for j in range(365))
    if not ok:
        print("vraie toute l'année jusqu'à %d ° de latitude environ" % (lat-5))
        break
print("(au-delà, il y a une partie de l'année où le soleil reste trop bas à midi)")

# ── la borne exacte, et le cas du Japon ────────────────────────────────
print()
lat_max = seuil - 23.44
print("l'affirmation tient TOUTE l'année si latitude + 23,44° < %.1f °," % seuil)
print("c'est-à-dire au-dessous de %.1f ° de latitude — les tropiques." % lat_max)
print()
print("or le Japon habité s'étend de 24 ° (Okinawa) à 45 ° (Hokkaido) :")
for nom, lat in (("Okinawa", 24.0), ("Tokyo", 35.7), ("Sapporo", 43.1)):
    d_lim = lat - seuil
    jours = sum(1 for j in range(365)
                if abs(lat - 23.44*math.sin(math.radians(360/365.24*(j-80)))) < seuil)
    print("   %-8s (%.1f °) : vraie %d jours sur 365, fausse %d jours"
          % (nom, lat, jours, 365-jours))
print("→ nulle part au Japon l'affirmation n'est vraie toute l'année.")

# ── l'ordre de grandeur, pour relativiser ──────────────────────────────
print()
peri, aphe = 91.40e6, 94.51e6      # milles
print("distance Terre-Soleil : de %.1f à %.1f millions de milles dans l'année,"
      % (peri/1e6, aphe/1e6))
print("soit une variation de %.0f milles — environ %d fois l'effet du rayon terrestre."
      % (aphe-peri, (aphe-peri)/R))

# ── témoins ─────────────────────────────────────────────────────────────
def jours_vrais(lat):
    return sum(1 for j in range(365)
               if abs(lat - 23.44*math.sin(math.radians(360/365.24*(j-80)))) < seuil)
print()
print("témoins : à l'équateur, vraie %d jours sur 365 ; au pôle Nord, %d"
      % (jours_vrais(0.0), jours_vrais(90.0)))
print("          soleil au zénith (z = 0) : écart = R = %.0f milles" % (R * math.cos(0)))
assert jours_vrais(0.0) == 365 and jours_vrais(90.0) == 0
assert 3950 < R < 3965 and 40.6 < seuil < 40.8
assert jours_vrais(35.7) == 208 and jours_vrais(43.1) == 171 and jours_vrais(24.0) == 275
