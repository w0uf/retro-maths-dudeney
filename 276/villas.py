# -*- coding: utf-8 -*-
"""n° 276 THE EIGHT VILLAS.

Huit villas autour d'un terrain de jeu carre : trois par cote. Le nombre
d'occupants de chaque cote vaut neuf. De combien de facons les villas
peuvent-elles etre occupees ? Dudeney repond 2 035, donne le detail de son
calcul, et une formule generale : (n^2 + 3n + 2)(n^2 + 3n + 3)/6.
"""
from itertools import product

def formule(n): return (n*n + 3*n + 2) * (n*n + 3*n + 3) // 6

def force_brute(n):
    """on compte les huit nombres ; les quatre du milieu sont determines"""
    k = 0
    for a, b, c, d in product(range(n+1), repeat=4):
        if a+b <= n and b+c <= n and c+d <= n and d+a <= n:
            k += 1
    return k

print("=== Sa formule tient-elle ? ===")
print("   n    force brute   sa formule   sa table")
TABLE = [1, 7, 26, 70, 155, 301, 532, 876, 1365, 2035]
ok = True
for n in range(0, 16):
    fb, fo = force_brute(n), formule(n)
    t = TABLE[n] if n < len(TABLE) else ""
    if fb != fo: ok = False
    if n < len(TABLE) and fb != TABLE[n]: ok = False
    print("  %2d  %11d  %11d   %s" % (n, fb, fo, t))
print("  accord parfait :", ok)
faux = lambda n: (n*n + 3*n + 2) * (n*n + 3*n + 4) // 6          # temoin : un facteur altere
print("  temoin (formule alteree) rejete par la force brute :", any(force_brute(n) != faux(n) for n in range(16)))
assert ok and any(force_brute(n) != faux(n) for n in range(16))
print("  pour neuf occupants par cote : %d" % force_brute(9))

# ═══ son detail, coin par coin ═════════════════════════════════════════
print()
print("=== Son detail : le nombre de solutions selon le coin en haut a gauche ===")
sien = {9:10, 8:37, 7:77, 6:126, 5:180, 4:235, 3:287, 2:332, 1:366, 0:385}
tot = 0
for a in range(9, -1, -1):
    k = sum(1 for b, c, d in product(range(10), repeat=3)
            if a+b <= 9 and b+c <= 9 and c+d <= 9 and d+a <= 9)
    tot += k
    print("   coin = %d : %3d solutions   (il annonce %3d)  %s"
          % (a, k, sien[a], "d'accord" if k == sien[a] else "DESACCORD"))
print("   total : %d" % tot)

# ═══ pourquoi cette formule ? ══════════════════════════════════════════
print()
print("=== D'ou sort la formule ===")
print("  Les quatre coins a, b, c, d suffisent : chaque villa du milieu est")
print("  imposee des que ses deux voisines de coin sont connues.")
print("  Pour a et c fixes, le nombre de b possibles est n+1-max(a,c), et")
print("  autant pour d. En groupant selon k = max(a,c), qui se realise de")
print("  2k+1 facons, le total vaut somme de (2k+1)(n+1-k)^2.")
for n in (9, 12):
    s = sum((2*k+1)*(n+1-k)**2 for k in range(n+1))
    print("   n = %2d : somme = %d   formule = %d   egaux : %s"
          % (n, s, formule(n), s == formule(n)))
print("  en posant m = (n+1)(n+2), la formule s'ecrit m(m+1)/6 : c'est")
print("  toujours un entier, car m ou m+1 est divisible par 3 selon le")
print("  reste de n modulo 3, et m est toujours pair.")
for n in range(0, 40):
    m = (n+1)*(n+2)
    assert m*(m+1) % 6 == 0
print("  verifie pour n de 0 a 39.")

# ═══ ce qu'il ne compte pas : a rotation et symetrie pres ══════════════
print()
print("=== Et si l'on ne comptait PAS les rotations et les reflexions ? ===")
print("  Il insiste : toutes doivent etre comptees. Mais combien y a-t-il")
print("  d'arrangements essentiellement differents ?")
def orbites(n):
    """Burnside sur le groupe du carre (8 elements) applique aux coins"""
    sols = [(a,b,c,d) for a,b,c,d in product(range(n+1), repeat=4)
            if a+b <= n and b+c <= n and c+d <= n and d+a <= n]
    S = set(sols)
    def rot(t, k):
        return tuple(t[(i-k) % 4] for i in range(4))
    def refl(t, k):
        r = tuple(reversed(t))
        return rot(r, k)
    fixes = 0
    for k in range(4):
        fixes += sum(1 for t in sols if rot(t, k) in S and rot(t, k) == t)
    for k in range(4):
        fixes += sum(1 for t in sols if refl(t, k) == t)
    return fixes // 8, len(sols)
for n in (9,):
    o, tot = orbites(n)
    print("  arrangements etiquetes        : %d" % tot)
    print("  arrangements a symetrie pres  : %d" % o)
    print("  soit %.1f fois moins." % (tot/o))

# contrôle : les orbites comptées directement, sans Burnside
def orbites_directes(n):
    from itertools import product
    sols = {(a,b,c,d) for a,b,c,d in product(range(n+1), repeat=4)
            if a+b <= n and b+c <= n and c+d <= n and d+a <= n}
    vus, reps = set(), 0
    for t in sols:
        if t in vus: continue
        reps += 1
        for k in range(4):
            vus.add(tuple(t[(i-k) % 4] for i in range(4)))
            r = tuple(reversed(t))
            vus.add(tuple(r[(i-k) % 4] for i in range(4)))
    return reps
# temoin compte a la main : n = 1, coins a 0 ou 1 sans deux 1 voisins -> 7 arrangements,
# 3 a symetrie pres (aucun, un coin, deux coins opposes)
print("  temoin n = 1 : %s arrangements, %s a symetrie pres (attendu 7 et 3) ; directe : %d"
      % (orbites(1)[1], orbites(1)[0], orbites_directes(1)))
assert orbites(1) == (3, 7) and orbites_directes(1) == 3
print()
print("  controle par enumeration directe des orbites : %d" % orbites_directes(9))
print("  (et 365, c'est le nombre de jours de l'annee.)")
