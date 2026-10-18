# -*- coding: utf-8 -*-
"""n° 60 THE WAPSHAW'S WHARF MYSTERY — la montre s'est arrêtée alors que
l'aiguille des heures et celle des minutes étaient exactement superposées,
et que la trotteuse venait de passer la quarante-neuvième seconde.
Quelle heure était-il ?"""
from fractions import Fraction as F

# ── les instants de superposition en douze heures ───────────────────────
# les aiguilles coïncident tous les 12/11 d'heure
pas = F(12, 11)                                   # en heures
print("les aiguilles se superposent tous les %s d'heure," % pas)
print("soit %s heures, %s minutes et %s secondes."
      % (int(pas), int(pas % 1 * 60), (pas % 1 * 60) % 1 * 60))
print("en douze heures, cela fait", 12 // pas if (12 % pas) == 0 else int(12/pas),
      "superpositions (midi non recompté).")
print()
print("n° |  heure exacte                    | secondes de la minute")
for k in range(11):
    t = k * pas                                   # en heures
    h = int(t)
    m = (t - h) * 60
    mi = int(m)
    s = (m - mi) * 60
    marque = ""
    if 49 <= s < 50: marque = "   ← « vient de passer la 49e seconde »"
    print("%2d | %2d h %2d min %-10s | %-10s%s"
          % (k+1, h, mi, "%s s" % s, str(float(s))[:7], marque))

# ── la réponse, et son contrôle ────────────────────────────────────────
print()
for k in range(11):
    t = k * pas
    h = int(t); m = (t - h)*60; mi = int(m); s = (m - mi)*60
    if 49 <= s < 50:
        print("la montre s'est arrêtée à %d h %d min %s s" % (h, mi, s))
        print("   soit, en décimales : %d h %d min %.4f s" % (h, mi, float(s)))
        # contrôle : les deux aiguilles sont-elles bien superposées ?
        angle_h = (t % 12) * 30                   # 30° par heure
        angle_m = (t % 1) * 360                   # un tour par heure
        print("   angle de l'aiguille des heures  : %s °" % angle_h)
        print("   angle de l'aiguille des minutes : %s °" % angle_m)
        print("   superposées :", angle_h % 360 == angle_m % 360)

# ── et si l'on cherchait les autres secondes ? ─────────────────────────
print()
print("les onze superpositions tombent sur ces secondes :")
print("  ", sorted(set(float(((k*pas - int(k*pas))*60 % 1)*60) for k in range(11))))
print("→ une seule tombe entre 49 et 50 : la réponse est unique.")

# ── temoin : le controle des angles doit refuser un instant faux ─────────
def superposees(t):
    return (t % 12) * 30 % 360 == (t % 1) * 360 % 360
juste = 4 + F(21, 60) + F(49, 3600) + F(1, 11 * 3600)        # 4 h 21 min 49 1/11 s
arrondi = 4 + F(21, 60) + F(49, 3600)                         # 4 h 21 min 49 s pile
print()
print("temoin : 4 h 21 min 49 s pile, superposees ?", superposees(arrondi), "-> refuse")
print("         4 h 21 min 49 1/11 s, superposees ?", superposees(juste))
assert superposees(juste) and not superposees(arrondi)
assert sum(1 for k in range(11) if 49 <= ((k*pas - int(k*pas))*60 % 1)*60 < 50) == 1
entieres = [k for k in range(11) if ((k*pas*60) % 1) == 0]
print("superpositions tombant sur une seconde entiere :", len(entieres),
      "(midi) -> les trois aiguilles ne sont ensemble qu'a midi et minuit")
assert entieres == [0]
