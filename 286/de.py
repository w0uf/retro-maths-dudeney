# -*- coding: utf-8 -*-
"""n° 286 PAINTING THE DIE — de combien de façons marquer les six faces d'un dé,
sachant que 1 et 6, 2 et 5, 3 et 4 doivent être opposées ?"""
import itertools

FACES = ["+x", "-x", "+y", "-y", "+z", "-z"]
OPP = {"+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y", "+z": "-z", "-z": "+z"}
PAIRES = [(1, 6), (2, 5), (3, 4)]
AXES = [("+x", "-x"), ("+y", "-y"), ("+z", "-z")]

# ── 1. toutes les façons de marquer un dé TENU EN MAIN ──────────────────
marquages = []
for perm in itertools.permutations(AXES):
    for sens in itertools.product((0, 1), repeat=3):
        m = {}
        for (a, b), (p, q), s in zip(perm, PAIRES, sens):
            m[a], m[b] = (p, q) if s == 0 else (q, p)
        marquages.append(tuple(m[f] for f in FACES))
print("façons de marquer un dé tenu en main :", len(marquages),
      " (Dudeney : 48)", len(marquages) == 48)
print("son compte : 6 places pour le 1, puis 4 pour le 2, puis 2 pour le 3 →",
      6*4*2)

# ── 2. les rotations du cube ───────────────────────────────────────────
def rot(v, axe):
    x, y, z = v
    return {"x": (x, -z, y), "y": (z, y, -x), "z": (-y, x, z)}[axe]
VEC = {"+x": (1,0,0), "-x": (-1,0,0), "+y": (0,1,0),
       "-y": (0,-1,0), "+z": (0,0,1), "-z": (0,0,-1)}
NOM = {v: k for k, v in VEC.items()}
rotations = set()
depart = tuple(VEC[f] for f in FACES)
pile = [depart]; vus = {depart}
while pile:
    e = pile.pop()
    for a in "xyz":
        s = tuple(rot(v, a) for v in e)
        if s not in vus: vus.add(s); pile.append(s)
rotations = list(vus)
print()
print("rotations du cube :", len(rotations), " (attendu : 24)")

# ── 3. combien de dés VRAIMENT différents ? ─────────────────────────────
def applique(m, r):
    """le marquage m vu après la rotation r"""
    d = {f: m[i] for i, f in enumerate(FACES)}
    return tuple(d[NOM[r[FACES.index(f)]]] for f in FACES)

orbites = set()
for m in marquages:
    orbites.add(min(applique(m, r) for r in rotations))
print("dés différents une fois qu'on a le droit de les tourner :", len(orbites))
print("   %d marquages / %d rotations = %d" % (len(marquages), len(rotations),
                                               len(marquages)//len(rotations)))

# ── 4. les deux dés sont-ils images l'un de l'autre dans un miroir ? ────
def sens(m):
    """au sommet où se rencontrent 1, 2 et 3 : dans quel sens tourne-t-on ?"""
    d = {m[i]: FACES[i] for i in range(6)}
    v1, v2, v3 = VEC[d[1]], VEC[d[2]], VEC[d[3]]
    det = (v1[0]*(v2[1]*v3[2]-v2[2]*v3[1])
         - v1[1]*(v2[0]*v3[2]-v2[2]*v3[0])
         + v1[2]*(v2[0]*v3[1]-v2[1]*v3[0]))
    return "droitier" if det > 0 else "gaucher"
print()
for o in sorted(orbites):
    n = sum(1 for m in marquages if min(applique(m, r) for r in rotations) == o)
    print("   un dé %-9s : %2d marquages sur 48" % (sens(o), n))
print("→ les deux dés sont images l'un de l'autre dans un miroir :")
print("   aucune rotation ne transforme l'un en l'autre.")

# ── témoins ─────────────────────────────────────────────────────────────
def valide(m):
    d = {FACES[i]: m[i] for i in range(6)}
    return sorted(m) == [1, 2, 3, 4, 5, 6] and all(d[f] + d[OPP[f]] == 7 for f in FACES)
faux = (1, 2, 3, 4, 5, 6)              # 1 face à 2 : interdit
print()
print("témoin : un marquage avec 1 face à 2 est refusé :", not valide(faux))
print("les 48 marquages sont tous valides :", all(valide(m) for m in marquages))
# un miroir (x -> -x) doit faire passer d'un dé à l'autre
miroir = lambda m: (m[1], m[0]) + m[2:]
o1, o2 = sorted(orbites)
cl = lambda m: min(applique(m, r) for r in rotations)
print("le miroir envoie un dé sur l'autre :", cl(miroir(o1)) == o2 and cl(miroir(o2)) == o1)
print("une rotation ne change pas de dé :", all(cl(applique(o1, r)) == o1 for r in rotations))
assert not valide(faux) and all(valide(m) for m in marquages) and len(orbites) == 2
assert cl(miroir(o1)) == o2 and sens(o1) != sens(o2)
