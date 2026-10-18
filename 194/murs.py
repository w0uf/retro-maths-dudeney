# -*- coding: utf-8 -*-
"""n° 194 THE GARDEN WALLS.

Un champ circulaire, quatre chaumieres, et trois murs a batir : chaque locataire
doit avoir la MEME SURFACE et exactement la MEME LONGUEUR DE MUR. Dudeney
consacre sa reponse a discuter ce qu'est « un mur », puis donne une figure qu'il
juge « la seule solution correcte et parfaitement satisfaisante ».

Sa construction : sur un diametre du champ, on marque les points qui le
partagent en quatre ; chaque mur est fait de DEUX demi-cercles, l'un au-dessus
du diametre et l'autre au-dessous.
"""
import math

R = 4.0                     # rayon du champ
def mur(k):
    """le mur n° k : demi-cercle superieur de rayon k, inferieur de rayon 4-k
    (en unites ou le rayon du champ vaut 4)"""
    return (k*R/4, (R - k*R/4))

print("=== Les trois murs ===")
for k in (1, 2, 3):
    a, b = mur(k)
    print("  mur %d : demi-cercle de rayon %.1f au-dessus, %.1f au-dessous"
          % (k, a, b))
    print("          longueur : pi x %.1f + pi x %.1f = %.4f" % (a, b, math.pi*(a+b)))
print("  -> les trois murs ont la MEME longueur : pi x R = %.4f," % (math.pi*R))
print("     c'est-a-dire exactement la moitie du mur circulaire du champ.")

# ═══ les quatre jardins ════════════════════════════════════════════════
def aires_de(mur, n=3000):
    """aire de chaque jardin, mesuree sur un quadrillage n x n"""
    def gauche(k, x, y):
        a, b = mur(k)
        if y >= 0: return (x - (a - R))**2 + y*y < a*a
        return (x - (R - b))**2 + y*y > b*b
    def jardin(x, y):
        for k in (1, 2, 3):
            if gauche(k, x, y): return k
        return 4
    aires = {1: 0, 2: 0, 3: 0, 4: 0}
    pas = 2*R/n
    for i in range(n):
        x = -R + (i + .5)*pas
        for j in range(n):
            y = -R + (j + .5)*pas
            if x*x + y*y < R*R:
                aires[jardin(x, y)] += pas*pas
    return aires
def egales(aires, tol=0.01):
    q = math.pi*R*R/4
    return all(abs(v - q)/q < tol for v in aires.values())

print()
print("=== Les quatre surfaces, mesurees ===")
aires = aires_de(mur)
tot = sum(aires.values())
print("  aire du champ : %.4f   (pi R^2 = %.4f)" % (tot, math.pi*R*R))
for k in (1, 2, 3, 4):
    print("  jardin %d : %.4f   (le quart : %.4f)   ecart %.2f %%"
          % (k, aires[k], math.pi*R*R/4, 100*abs(aires[k] - math.pi*R*R/4)/(math.pi*R*R/4)))
print("  -> les quatre parts sont egales (a 1 % pres) :", egales(aires))
# temoin : les deux demi-cercles d'un mur de meme rayon k (au lieu de k et 4-k)
mauvais = aires_de(lambda k: (k*R/4, k*R/4), 1000)
print("  temoin (demi-cercles de meme rayon) :", ", ".join("%.2f" % mauvais[k] for k in (1, 2, 3, 4)),
      "-> refuse :", not egales(mauvais))
assert egales(aires) and not egales(mauvais)

# ═══ les longueurs de mur ══════════════════════════════════════════════
print()
print("=== La longueur de mur de chaque locataire ===")
print("  jardin 1 : la moitie du mur circulaire (%.4f) + le mur 1 (%.4f)"
      % (math.pi*R, math.pi*R))
print("  jardin 4 : de meme, par symetrie")
print("  jardins 2 et 3 : deux murs entiers (%.4f + %.4f)" % (math.pi*R, math.pi*R))
print("  -> chacun dispose de %.4f de mur : exactement la meme longueur."
      % (2*math.pi*R))
print()
print("  Et ce nombre vaut le PERIMETRE du champ : %.4f = 2 pi R." % (2*math.pi*R))
print("  Chaque locataire a donc autant de mur que s'il possedait le champ")
print("  entier — ce que Dudeney ne signale pas.")
