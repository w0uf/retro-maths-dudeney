# -*- coding: utf-8 -*-
"""n° 188 THE BALL PROBLEM — deux questions : combien de boules identiques
peuvent toucher une boule centrale, toutes posées au sol ? et quel diamètre
donne à une sphère une aire numériquement égale à son volume ?"""
import math

# ── 1. la question du tailleur de pierre : des cercles autour d'un cercle ─
print("des disques de même rayon autour d'un disque central, tous au sol :")
print("   deux voisins consécutifs et le centre forment un triangle équilatéral,")
print("   donc chacun occupe un angle de 60° autour du centre.")
print("   360 / 60 =", 360//60, "→ six voisins, et pas un de plus.")
print("   (sept demanderaient 7 × 60 = %d° > 360°)" % (7*60))

# ── 2. la question du gamin : aire = volume ─────────────────────────────
print()
print("sphère de diamètre d : aire = π d², volume = π d³ / 6")
print("   l'égalité donne d² = d³/6, c'est-à-dire d = 6 — et π disparaît.")
d = 6
print("   contrôle : aire = %.4f, volume = %.4f" % (math.pi*d*d, math.pi*d**3/6))

# ── 3. la coïncidence qui n'en est pas une ─────────────────────────────
print()
print("le cube dont l'aire égale le volume : 6a² = a³ → a = 6, le même nombre !")
print("ce n'est pas un hasard : pour tout solide convexe circonscrit à une")
print("sphère, volume = aire × rayon inscrit / 3. L'égalité équivaut donc à")
print("un rayon inscrit égal à 3 — la sphère de diamètre 6 et le cube de côté 6")
print("ont bien tous deux un rayon inscrit de 3.")
print()
print("%-24s | %-12s | %-12s | rayon inscrit" % ("solide (aire = volume)", "aire", "volume"))
def ligne(nom, S, V, r): print("%-24s | %12.4f | %12.4f | %.4f" % (nom, S, V, r))
ligne("sphère, diamètre 6", math.pi*36, math.pi*216/6, 3)
ligne("cube, côté 6", 6*36, 216, 3)
a = 6*math.sqrt(6)                       # tétraèdre régulier de rayon inscrit 3
ligne("tétraèdre rég., a=6√6", math.sqrt(3)*a*a, a**3/(6*math.sqrt(2)), a/(2*math.sqrt(6)))
a = 3*math.sqrt(6)                       # octaèdre régulier de rayon inscrit 3
ligne("octaèdre rég., a=3√6", 2*math.sqrt(3)*a*a, math.sqrt(2)*a**3/3, a/math.sqrt(6))
r = 3                                     # cylindre de rayon 3, hauteur 6
ligne("cylindre r=3, h=6", 2*math.pi*r*r + 2*math.pi*r*6, math.pi*r*r*6, 3)

# temoin : la loi V = S r / 3 ne vaut que pour un solide circonscrit a une sphere
print()
a, b, c = 4, 6, 12
S, V = 2*(a*b + b*c + a*c), a*b*c
print("temoin : pave %d x %d x %d -> aire %d, volume %d, egales : %s" % (a, b, c, S, V, S == V))
print("   mais il n'a pas de sphere inscrite (la plus grande boule qu'il contient")
print("   a pour rayon %g, pas 3) : la loi ne s'applique pas, et le seuil 3 non plus." % (min(a, b, c)/2))
assert S == V and min(a, b, c)/2 != 3
for S_, V_ in ((math.pi*36, math.pi*36), (216, 216)):
    assert abs(S_ - V_) < 1e-9
