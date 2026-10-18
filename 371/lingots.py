# -*- coding: utf-8 -*-
"""n° 371 GOLD PACKING IN RUSSIA.

800 lingots de 12 pouces 1/2 sur 11 sur 1. Quelles sont les dimensions
interieures d'une caisse de LONGUEUR ET LARGEUR EGALES, et de profondeur
necessaire, qui les contienne exactement, sans le moindre espace perdu ?
« Pas plus de douze lingots ne peuvent etre poses sur chant, selon le reglement
du gouvernement. »

Tout est double pour travailler en entiers : le lingot mesure 25 x 22 x 2.
"""
L, W, E = 25, 22, 2          # lingot double : 12,5 / 11 / 1 pouce
N = 800
VOL = N * L * W * E
print("=== Volume ===")
print("  800 lingots : %d (unites doubles) = %d pouces cubes"
      % (VOL, VOL // 8))

# ═══ 1. sa caisse, verifiee case par case ══════════════════════════════
def grille(dims, pieces):
    """pieces = liste de (x, y, z, dx, dy, dz) ; verifie le pavage exact"""
    A, B, C = dims
    occ = bytearray(A*B*C)
    for (x, y, z, dx, dy, dz) in pieces:
        if x < 0 or y < 0 or z < 0 or x+dx > A or y+dy > B or z+dz > C:
            return "deborde"
        for i in range(x, x+dx):
            for j in range(y, y+dy):
                base = (i*B + j)*C
                for k in range(z, z+dz):
                    if occ[base+k]: return "chevauchement en (%d,%d,%d)" % (i,j,k)
                    occ[base+k] = 1
    return "exact" if all(occ) else "%d cases vides" % (len(occ)-sum(occ))

pieces, sur_chant = [], 0
# 11 couches de 72 lingots a plat : 8 en longueur (8 x 25 = 200), 9 en
# largeur (9 x 22 = 198), epaisseur 2
for k in range(11):
    for i in range(8):
        for j in range(9):
            pieces.append((i*L, j*W, k*E, L, W, E))
# les 8 derniers sur chant dans la bande 200 x 2 x 22 qui reste
for i in range(8):
    pieces.append((i*L, 198, 0, L, E, W))
    sur_chant += 1
print()
print("=== Sa caisse : 100 x 100 x 11 pouces ===")
print("  lingots poses : %d, dont %d sur chant" % (len(pieces), sur_chant))
print("  remplissage de la caisse 200 x 200 x 22 :", grille((200, 200, 22), pieces))
print("  le reglement autorise douze lingots sur chant : %d <= 12" % sur_chant)
print("  temoin 1 (un lingot retire)  :", grille((200, 200, 22), pieces[:-1]))
x, y, z, dx, dy, dz = pieces[0]
print("  temoin 2 (un lingot decale)  :", grille((200, 200, 22), [(x + 1, y, z, dx, dy, dz)] + pieces[1:]))
assert grille((200, 200, 22), pieces) == "exact" and grille((200, 200, 22), pieces[:-1]) != "exact" \
    and grille((200, 200, 22), [(x + 1, y, z, dx, dy, dz)] + pieces[1:]) != "exact"

# ═══ 2. quelles autres caisses carrees ont le bon volume ? ═════════════
print()
print("=== Les caisses carrees de volume exact ===")
cands = []
for s in range(2, 801, 1):                  # cote, en unites doubles
    if VOL % (s*s): continue
    d = VOL // (s*s)
    if s >= L and d >= E: cands.append((s, d))
print("  cotes possibles (en pouces) et profondeurs correspondantes :")
for s, d in cands:
    print("     %7.1f x %7.1f x %7.1f" % (s/2, s/2, d/2))

# ═══ 3. lesquelles peut-on reellement remplir ? ════════════════════════
def essai(s, d):
    """remplissage « bloc a plat + bande sur chant », le plus naturel"""
    best = None
    for (pl, pw) in ((L, W), (W, L)):           # orientation a plat
        if s % pl or d % E: continue
        nl, nz = s // pl, d // E
        for nw in range(1, s // pw + 1):
            reste = s - nw*pw
            if reste < 0: break
            plats = nl * nw * nz
            if reste == 0:
                if plats == N: best = min(best or 0, 0) if best is not None else 0
                continue
            # la bande restante : s x reste x d, en lingots sur chant
            for (cl, cw, ch) in ((L, E, W), (E, L, W), (W, E, L), (E, W, L)):
                if s % cl or reste % cw or d % ch: continue
                chants = (s//cl) * (reste//cw) * (d//ch)
                if plats + chants == N:
                    if best is None or chants < best: best = chants
    return best
print()
print("=== Remplissages trouves (bloc a plat + bande sur chant) ===")
for s, d in cands:
    c = essai(s, d)
    if c is None:
        print("     %6.1f x %6.1f x %6.1f : aucun remplissage de cette forme"
              % (s/2, s/2, d/2))
    else:
        print("     %6.1f x %6.1f x %6.1f : possible, avec %d lingots sur chant %s"
              % (s/2, s/2, d/2, c, "  <-- conforme au reglement" if c <= 12 else
                 "  (le reglement l'interdit)"))

# ═══ 4. les deux caisses sans remplissage sont-elles VRAIMENT impossibles ?
print()
print("=== Preuve pour les deux caisses restantes ===")
from functools import lru_cache
@lru_cache(None)
def representable(n):
    """n est-il une somme de 25, 22 et 2 ?"""
    if n == 0: return True
    if n < 0: return False
    return any(representable(n - p) for p in (25, 22, 2))
def parts(s):
    return {p for p in (L, W, E) if representable(s - p)}
for s, d in cands:
    P = parts(s)
    diag = []
    if P == {L}:
        diag.append("le seul decoupage possible d'un cote est %d : chaque lingot"
                    " devrait avoir sa grande dimension le long des DEUX cotes"
                    " a la fois -> IMPOSSIBLE" % L)
    elif L not in P:
        diag.append("aucun lingot ne peut poser sa longueur le long d'un cote "
                    "(il resterait %d, indecomposable) : tous sont debout" % (s-L))
        if (s*s) % (W*E):
            diag.append("leur empreinte est alors %dx%d, d'aire %d, qui ne divise"
                        " pas %d -> IMPOSSIBLE" % (W, E, W*E, s*s))
    if diag:
        print("  cote %5.1f pouces : %s" % (s/2, " ; ".join(diag)))
    else:
        print("  cote %5.1f pouces : aucune impossibilite elementaire ; "
              "decoupages d'un cote possibles avec %s"
              % (s/2, sorted(x/2 for x in P)))

# ═══ 5. les deux caisses rivales, verifiees case par case ══════════════
print()
print("=== Les deux caisses rivales, verifiees sur la grille ===")
def rivale(s, d, npl_x, npl_y, nz, bande):
    p, chant = [], 0
    for i in range(npl_x):
        for j in range(npl_y):
            for k in range(nz):
                p.append((i*L, j*W, k*E, L, W, E))
    y0 = npl_y*W
    for i in range(s//L):
        for j in range(bande//E):
            for k in range(d//W):
                p.append((i*L, y0 + j*E, k*W, L, E, W)); chant += 1
    return p, chant
for s, d in ((50, 352), (100, 88)):      # 25 et 50 pouces, en unites doubles
    npl_y = (s // W); bande = s - npl_y*W
    p, chant = rivale(s, d, s//L, npl_y, d//E, bande)
    print("  caisse %5.1f x %5.1f x %5.1f : %d lingots, dont %d sur chant -> %s"
          % (s/2, s/2, d/2, len(p), chant, grille((s, s, d), p)))
print("  le reglement en autorise douze : ces caisses en demandent huit fois plus.")
