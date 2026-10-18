# -*- coding: utf-8 -*-
"""n° 157 THE TABLE-TOP AND STOOLS.

Un plateau circulaire découpé en huit pièces qui forment deux tabourets ovales
percés d'un trou pour la main. Le maître d'école propose une découpe ; un élève
prétend faire des trous plus petits, et reçoit le fouet. Dudeney donne raison à
l'élève : « ces trous sont un rien plus longs que ceux du maître, mais beaucoup
plus étroits et d'une aire considérablement plus petite ».

Trois affirmations comparatives. On les vérifie en reconstruisant EXACTEMENT
les deux figures à partir des gravures, puis en mesurant.
"""
import math, os
from PIL import Image
import numpy as np

R = 1.0                     # rayon du plateau
ICI = os.path.dirname(os.path.abspath(__file__))

# ═══ 1. la découpe du maître d'école (gravure de l'énoncé) ════════════════
# disque de rayon R, cercle intérieur de rayon rho, deux diamètres à 90°.
# 8 pièces : 4 quarts du disque intérieur + 4 secteurs de la couronne.
# Un tabouret = 2 secteurs de couronne (à gauche et à droite) + 2 quarts de
# disque (en haut et en bas). Le trou est la lentille laissée entre les deux
# arcs intérieurs des secteurs : deux arcs de 90° et de rayon rho.
def maitre(rho):
    trou_long = rho*math.sqrt(2)                     # corde des arcs de 90°
    trou_larg = rho*(2 - math.sqrt(2))               # deux fois la flèche
    trou_aire = rho*rho*(math.pi/2 - 1)              # deux segments de 90°
    tab_haut  = rho*(2 + math.sqrt(2))
    tab_larg  = 2*R - math.sqrt(2)*rho
    bois      = math.pi/2*(R*R - rho*rho) + math.pi/2*rho*rho   # = πR²/2
    return trou_long, trou_larg, trou_aire, tab_haut, tab_larg, bois

# ═══ 2. la découpe de Dudeney (gravure de la solution) ═══════════════════
# Deux cordes verticales à x = ±a, deux horizontales à y = ±a, un carré
# curviligne central à quatre arcs de rayon R, coupé par ses diagonales.
# Les pièces 5-6-7-8 sont quatre triangles curvilignes rectangles isocèles de
# côté a√2 ; pour qu'ils composent les pointes du tabouret il faut
#     h - k = a√2   et   √(R²-k²) - a = a√2       (h = √(R²-a²))
# ce qui donne a = R·sin(π/8), c'est-à-dire 22°30'.
a = R*math.sin(math.pi/8)
h = R*math.cos(math.pi/8)
assert abs((h - a*math.sqrt(2)) - math.sqrt(R*R - (a*(1+math.sqrt(2)))**2)) < 1e-12

tab_haut_D = 2*h                      # le tabouret : lentille de deux arcs R
tab_larg_D = 2*(R - a)
trou_long_D = 2*a                     # lentille de deux arcs de rayon R
trou_larg_D = 2*(R - h)               # deux fois la flèche
trou_aire_D = 2*(R*R*math.asin(a/R) - a*h)     # deux segments de corde 2a

# contrôle indépendant : la conservation du bois
lentille = 2*(R*R*math.acos(a/R) - a*h)        # aire du contour du tabouret
bois_D = 2*(lentille - trou_aire_D)
print("═══ Dudeney : le bois est-il conservé ? ═══")
print("  contour d'un tabouret  : %.10f R²" % lentille)
print("  trou                   : %.10f R²   (= (π−2√2)/4 : %.10f)"
      % (trou_aire_D, (math.pi - 2*math.sqrt(2))/4))
print("  2 × (contour − trou)   : %.10f R²" % bois_D)
print("  aire du plateau  πR²   : %.10f R²" % (math.pi*R*R))
print("  écart                  : %.2e   →  découpe EXACTE, pas approchée"
      % abs(bois_D - math.pi*R*R))

# témoin : avec des cordes à a = R/3 au lieu de R·sin(π/8), les pointes ne se composent plus
a3 = R/3; h3 = math.sqrt(R*R - a3*a3)
ecart3 = abs((h3 - a3*math.sqrt(2)) - math.sqrt(R*R - (a3*(1+math.sqrt(2)))**2))
print("  témoin a = R/3 : les pièces ne se raccordent pas (écart %.3f R) -> refusé" % ecart3)
assert ecart3 > 1e-3

# contrôle numérique brut du trou (intégration)
n = 2_000_000
s = 0.0
for i in range(n):
    y = -a + 2*a*(i+0.5)/n
    s += 2*(math.sqrt(R*R - y*y) - h)
print("  trou par intégration   : %.10f R²" % (s*2*a/n))

# ═══ 3. quel rayon intérieur le maître d'école a-t-il choisi ? ═══════════
# On le lit sur la gravure : le rapport hauteur/largeur du tabouret le donne.
im = np.array(Image.open(os.path.join(ICI, 'q157.png')).convert('L')) < 128
col = im.sum(axis=0)
bl, deb = [], None
for x in range(im.shape[1]):
    if col[x] and deb is None: deb = x
    elif not col[x] and deb is not None:
        if x-deb > 20: bl.append((deb, x-1))
        deb = None
x0, x1 = bl[1]
lig = im[:, x0:x1+1].sum(axis=1); ys = [y for y in range(im.shape[0]) if lig[y]]
H, L = ys[-1]-ys[0]+1, x1-x0+1
r = H/L
u = 2*r/((2+math.sqrt(2)) + math.sqrt(2)*r)     # résolution de (2+√2)u/(2−√2u)=r
print()
print("═══ Le maître d'école : son cercle intérieur ═══")
print("  tabouret gravé : %d × %d px, rapport %.4f" % (H, L, r))
print("  d'où  ρ/R = %.4f  →  il a pris ρ = R/2" % u)
rho = R/2
tl, tw, ta, th, twd, bois = maitre(rho)
print("  bois par tabouret : %.10f R²  (moitié du plateau : %.10f)"
      % (bois, math.pi/2))

# ═══ 4. les trois affirmations de Dudeney ═══════════════════════════════
print()
print("═══ Les trois affirmations, mises à l'épreuve ═══")
print("                        maître d'école     Dudeney      rapport")
print("  longueur du trou      %8.5f R      %8.5f R    %+.1f %%"
      % (tl, trou_long_D, 100*(trou_long_D/tl - 1)))
print("  largeur  du trou      %8.5f R      %8.5f R    %+.1f %%"
      % (tw, trou_larg_D, 100*(trou_larg_D/tw - 1)))
print("  aire     du trou      %8.5f R²     %8.5f R²   %+.1f %%"
      % (ta, trou_aire_D, 100*(trou_aire_D/ta - 1)))
print()
print("  « un rien plus longs »            :", "VRAI" if trou_long_D > tl else "FAUX",
      "(+%.1f %%)" % (100*(trou_long_D/tl-1)))
print("  « beaucoup plus étroits »         :", "VRAI" if trou_larg_D < tw else "FAUX",
      "(%.0f %% de la largeur)" % (100*trou_larg_D/tw))
print("  « aire considérablement moindre » :", "VRAI" if trou_aire_D < ta else "FAUX",
      "(%.0f %% de l'aire)" % (100*trou_aire_D/ta))

# ═══ 5. est-ce vraiment la « vesica piscis » ? ══════════════════════════
def pointe(rayon, ecart):
    """angle INTÉRIEUR de la lentille à sa pointe : deux fois l'angle
    tangente-corde, soit 2·arcsin(y/rayon) avec y la demi-longueur."""
    y = math.sqrt(rayon*rayon - (ecart/2)**2)
    return 2*math.degrees(math.asin(y/rayon))
print()
print("═══ Le mot « vesica piscis » ═══")
print("  la vraie vesica des architectes (centres distants du rayon) :")
print("     pointes %.1f°,  longueur/largeur = %.4f  (= √3)"
      % (pointe(1.0, 1.0), math.sqrt(3)))
print("  le tabouret de Dudeney (centres distants de 2a = %.4f R) :" % (2*a))
print("     pointes %.1f°,  longueur/largeur = %.4f"
      % (pointe(R, 2*a), tab_haut_D/tab_larg_D))
# et sur la gravure ?
im2 = np.array(Image.open(os.path.join(ICI, 'a157b.png')).convert('L')) < 128
col2 = im2.sum(axis=0); bl2, deb = [], None
for x in range(im2.shape[1]):
    if col2[x] and deb is None: deb = x
    elif not col2[x] and deb is not None:
        if x-deb > 20: bl2.append((deb, x-1))
        deb = None
for i,(p,q) in enumerate(bl2):
    l2 = im2[:, p:q+1].sum(axis=1); yy = [y for y in range(im2.shape[0]) if l2[y]]
    print("  gravure, tabouret %d : rapport mesuré %.4f"
          % (i+1, (yy[-1]-yy[0]+1)/(q-p+1)))
print("  → la gravure donne ~1,46 : c'est bien %.2f et non √3 = %.2f."
      % (tab_haut_D/tab_larg_D, math.sqrt(3)))


# ═══ 6. et si le maître d'école avait simplement pris un cercle plus petit ?
print()
print("═══ Le maître pouvait-il gagner sans changer de méthode ? ═══")
print("   sa construction marche pour N'IMPORTE QUEL cercle intérieur ρ :")
print("   le bois vaut toujours πR²/2 par tabouret, et le trou vaut ρ²(π/2−1).")
print()
print("     ρ/R      aire du trou     tabouret (haut × larg)")
for u in (0.50, 0.45, 0.40, 0.37033, 0.35, 0.30):
    tl, tw, ta, th, twd, _ = maitre(u*R)
    print("     %.3f     %.5f R²      %.3f × %.3f R   %s"
          % (u, ta, th, twd, "← égale celui de Dudeney" if abs(ta-trou_aire_D)<1e-4 else
             ("plus petit que celui de Dudeney" if ta < trou_aire_D else "")))
seuil = math.sqrt(trou_aire_D/(math.pi/2 - 1))
print()
print("   seuil : dès que ρ < %.5f R, le trou du maître d'école devient" % seuil)
print("   PLUS PETIT que celui de l'élève — sans rien changer à sa découpe.")
