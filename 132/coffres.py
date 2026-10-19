# -*- coding: utf-8 -*-
"""n° 132 THE NINE TREASURE BOXES — Dudeney, 1917.

Neuf coffres contenant chacun un nombre CARRE de doublons, formant trois
progressions arithmetiques (A,B,C), (D,E,F), (G,H,I) de MEME raison ;
et le coffre A ne contient pas plus de douze pieces.

Dudeney : raison 3 360, racines 2, 58, 82 / 46, 74, 94 / 97, 113, 127.
"""
from math import isqrt
from collections import defaultdict

LIM = 4000                      # racines jusqu'a 4000
CARRES = {i*i: i for i in range(1, LIM+1)}

# --- toutes les progressions de trois carres, par raison ---------------
par_raison = defaultdict(list)
for a in range(1, LIM+1):
    A = a*a
    for b in range(a+1, LIM+1):
        B = b*b
        d = B - A
        C = B + d
        if C > LIM*LIM: break
        if C in CARRES: par_raison[d].append((a, b, CARRES[C]))

print("=== Les raisons qui portent au moins trois progressions ===")
riches = sorted((d, v) for d, v in par_raison.items() if len(v) >= 3)
for d, v in riches[:8]:
    print("  raison %6d : %d progressions  %s" % (d, len(v), v[:4]))
print("  ...")
print("\n  la plus petite raison a trois progressions :", riches[0][0])

print("\n=== Sa reponse ===")
d = 3360
v = sorted(par_raison[d])
print("  raison 3 360 : %d progressions" % len(v))
for t in v: print("     racines", t, "-> coffres", [x*x for x in t])
sienne = [(2,58,82),(46,74,94),(97,113,127)]
print("  les siennes y figurent toutes :", all(t in v for t in sienne))

print("\n=== La contrainte « A ne depasse pas douze pieces » ===")
petits = [(dd, vv) for dd, vv in riches if any(t[0]*t[0] <= 12 for t in vv)]
print("  raisons a trois progressions dont l'une commence a 1, 4 ou 9 doublons :")
for dd, vv in petits[:6]:
    deb = [t for t in vv if t[0]*t[0] <= 12]
    print("     raison %7d : depart(s) %s, %d progressions en tout" % (dd, deb, len(vv)))
print("\n  la plus petite de ces raisons :", petits[0][0] if petits else "aucune")
if petits:
    dd, vv = petits[0]
    print("  ses progressions :", sorted(vv))
    print("  neuf coffres tous differents :", len({x for t in sorted(vv)[:3] for x in t}) == 9)

print("\n=== Une infinite de reponses sans la clause, et plusieurs familles ===")
print("  multiplier les racines par k multiplie les coffres et la raison par k^2")
primitives = []
for d, vv in riches[:12]:
    src = [p for p in primitives if d % p == 0 and isqrt(d // p)**2 == d // p]
    if src:
        print("  raison %7d : la raison %d, racines x %d" % (d, src[0], isqrt(d // src[0])))
    else:
        primitives.append(d)
        print("  raison %7d : NOUVELLE famille" % d)
autres = primitives[1:]
print("  familles distinctes dans ce debut de liste :", primitives)

# temoins
print("\n=== Temoins ===")
def trois_carres(t, d):
    return all(isqrt(x)**2 == x for x in t) and t[1]-t[0] == d and t[2]-t[1] == d
print("  (4, 3364, 6724) raison 3360 accepte :", trois_carres((4, 3364, 6724), 3360))
print("  (4, 3364, 6725) refuse :", not trois_carres((4, 3364, 6725), 3360))
assert trois_carres((4, 3364, 6724), 3360) and not trois_carres((4, 3364, 6725), 3360)
assert all(trois_carres([x*x for x in t], 3360) for t in sienne)
assert riches[0][0] == 3360 and len(petits) == 1 and autres[:2] == [43680, 127680]
