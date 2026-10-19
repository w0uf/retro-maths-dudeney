# -*- coding: utf-8 -*-
"""n° 218 THE VICTORIA CROSS PUZZLE — Dudeney, Amusements in Mathematics (1917).

Neuf divisions en croix (une grille de trois sur trois), huit jetons portant
les lettres de VICTORIA, la division centrale vide.  On glisse une lettre a
la fois dans la case vide ; il faut que le mot se lise de nouveau en tournant
dans le meme sens, mais avec le V sur l'un des bras noirs (les quatre cases
du milieu des cotes), le centre restant vide.

     0   1   2        coins  : 0 2 6 8   (bras clairs)
     3   4   5        bras   : 1 3 5 7   (bras noirs)
     6   7   8        centre : 4

Depart (sens horaire depuis le coin 2) : V I C T O R I A
     0=I2  1=A   2=V
     3=R   4=.   5=I1
     6=O   7=T   8=C

Affirmations de Dudeney a verifier :
  (a) impossible si les huit lettres etaient toutes differentes ;
  (b) le minimum est 18 coups ;
  (c) il y a exactement six solutions en 18 coups ;
  (d) dans chacune, C T O R ne bougent qu'une fois, le second I bouge
      quatre fois, et le V finit toujours sur le bras de droite ;
  (e) il existe une solution en 22 coups qui epelle
      « A VICTOR! A VICTOR! A VICTOR I! » ;
  (f) il existe une solution en 28 coups ou seuls les I passent par le centre.
"""
from collections import deque
from itertools import permutations

VOISINS = {0:(1,3), 1:(0,2,4), 2:(1,5), 3:(0,4,6), 4:(1,3,5,7),
           5:(2,4,8), 6:(3,7), 7:(4,6,8), 8:(5,7)}
HORAIRE = (2,5,8,7,6,3,0,1)          # le tour de la croix, sens des aiguilles
BRAS    = (1,3,5,7)
MOT     = "VICTORIA"

DEPART = ("I2","A","V","R",".","I1","O","T","C")

def cibles():
    """toutes les positions d'arrivee admises"""
    res = set()
    for depart_v in range(8):
        if HORAIRE[depart_v] not in BRAS: continue
        for i1, i2 in ((1,6),(6,1)):          # les deux I sont interchangeables
            g = ["."]*9
            for k, lettre in enumerate(MOT):
                case = HORAIRE[(depart_v+k) % 8]
                g[case] = "I1" if k == i1 else "I2" if k == i2 else lettre
            if sorted(x for x in g if x != ".") == sorted(x for x in DEPART if x != "."):
                res.add(tuple(g))
    return res

CIBLES = cibles()
print("positions d'arrivee possibles (V sur un bras, centre vide) :", len(CIBLES))

# --- (a) la parite ------------------------------------------------------
def parite(etat):
    ordre = [etat[c] for c in HORAIRE]
    ref   = [DEPART[c] for c in HORAIRE]
    perm  = [ref.index(x) if ref.count(x) == 1 else None for x in ordre]
    p = list(range(8))
    for i, x in enumerate(ordre): p[i] = ref.index(x)
    signe, vu = 1, [False]*8
    for i in range(8):
        if vu[i]: continue
        j, n = i, 0
        while not vu[j]: vu[j] = True; j = p[j]; n += 1
        if n % 2 == 0: signe = -signe
    return signe

print("\n(a) parite du depart :", parite(DEPART))
for c in sorted(CIBLES):
    print("    arrivee", "".join(x[0] for x in c), "parite", parite(c),
          "->", "atteignable" if parite(c) == 1 else "impossible")

# --- parcours en largeur ------------------------------------------------
def coups(etat):
    v = etat.index(".")
    for w in VOISINS[v]:
        e = list(etat); e[v], e[w] = e[w], e[v]
        yield etat[w], tuple(e)

dist = {DEPART: 0}; pere = {DEPART: []}
f = deque([DEPART])
while f:
    e = f.popleft()
    for lettre, e2 in coups(e):
        if e2 not in dist:
            dist[e2] = dist[e]+1; pere[e2] = [(e, lettre)]; f.append(e2)
        elif dist[e2] == dist[e]+1: pere[e2].append((e, lettre))
print("\npositions atteignables :", len(dist), "sur", 9*8*7*6*5*4*3*2)

atteintes = [c for c in CIBLES if c in dist]
print("\n(b) distances aux arrivees :", sorted(dist[c] for c in atteintes))
mini = min(dist[c] for c in atteintes)
print("    minimum :", mini, " (Dudeney : 18 ->", mini == 18, ")")

# --- (c) toutes les solutions optimales ---------------------------------
def chemins(e):
    if not pere[e]: return [[]]
    out = []
    for p, lettre in pere[e]:
        for ch in chemins(p): out.append(ch + [lettre])
    return out

sols = []
for c in atteintes:
    if dist[c] == mini: sols += [(c, ch) for ch in chemins(c)]
print("\n(c) solutions en %d coups : %d  (Dudeney : six -> %s)"
      % (mini, len(sols), len(sols) == 6))

from collections import Counter
print("\n(d) contenu de chaque solution optimale :")
for c, ch in sols:
    n = Counter(ch)
    print("    ", " ".join(ch))
    print("      C,T,O,R une seule fois :",
          all(n[x] == 1 for x in "CTOR"),
          "| second I quatre fois :", n["I2"] == 4,
          "| V sur le bras droit :", c[5] == "V")

# --- (e) « A VICTOR! A VICTOR! A VICTOR I! » ----------------------------
print("\n(e) la sequence « A VICTOR! A VICTOR! A VICTOR I! » :")
mots = list("AVICTOR")*3 + ["I"]
print("    ", len(mots), "coups annonces")
def jouer(etat, lettres):
    for k, L in enumerate(lettres):
        v = etat.index(".")
        possibles = [w for w in VOISINS[v] if etat[w][0] == L]
        if not possibles: return None, k
        if len(possibles) > 1:                  # un I ambigu : on essaie les deux
            for w in possibles:
                e = list(etat); e[v], e[w] = e[w], e[v]
                r, k2 = jouer(tuple(e), lettres[k+1:])
                if r is not None: return r, 0
            return None, k
        w = possibles[0]
        e = list(etat); e[v], e[w] = e[w], e[v]; etat = tuple(e)
    return etat, 0
fin, rate = jouer(DEPART, mots)
print("    sequence jouable :", fin is not None,
      "| arrive a bon port :", fin in CIBLES if fin else False)

# --- (f) une solution de 28 coups sans autre passage central que les I --
print("\n(f) solution ou seuls les I passent par le centre :")
d2 = {DEPART: 0}; f = deque([DEPART])
while f:
    e = f.popleft()
    for lettre, e2 in coups(e):
        # la lettre jouee arrive dans la case que le vide occupait
        if e.index(".") == 4 and not lettre.startswith("I"): continue
        if e2 not in d2: d2[e2] = d2[e]+1; f.append(e2)
bons = [d2[c] for c in CIBLES if c in d2]
print("    longueurs possibles :", sorted(bons) if bons else "aucune",
      "| Dudeney annonce 28 ->", bool(bons) and min(bons) <= 28)

# --- qui passe par le centre dans chaque solution optimale ? ------------
print("\n(f bis) lettres qui entrent dans la case centrale, solution par solution :")
for c, ch in sols:
    e = DEPART; centre = []
    for L in ch:
        v = e.index(".")
        w = [x for x in VOISINS[v] if e[x] == L][0]
        if v == 4: centre.append(L)
        g = list(e); g[v], g[w] = g[w], g[v]; e = tuple(g)
    assert e == c
    print("    ", " ".join(ch), "->", " ".join(centre) or "personne",
          "| seuls des I :", all(x.startswith("I") for x in centre))

# --- sa solution imprimee est-elle l'une des six ? ----------------------
SIENNE = "I1 V A I2 R O T I1 I2 A V I2 I1 C I2 V A I1".split()
print("\nsa solution imprimee figure-t-elle parmi les six :",
      any(ch == SIENNE for _, ch in sols))
def centre_de(ch):
    e = DEPART; out = []
    for L in ch:
        v = e.index(".")
        w = [x for x in VOISINS[v] if e[x] == L][0]
        if v == 4: out.append(L)
        g = list(e); g[v], g[w] = g[w], g[v]; e = tuple(g)
    return out, e
print("et passe-t-elle par le centre avec les seuls I :",
      all(x.startswith("I") for x in centre_de(SIENNE)[0]))
print("\nexcentricite depuis le depart :", max(dist.values()), "coups")

# temoins : une sequence fautive doit etre refusee
print("\n=== Temoins ===")
def rejoue(ch):
    e = DEPART
    for L in ch:
        v = e.index(".")
        w = [x for x in VOISINS[v] if e[x] == L]
        if not w: return None
        g = list(e); g[v], g[w[0]] = g[w[0]], g[v]; e = tuple(g)
    return e
t1 = SIENNE[:5] + [SIENNE[6], SIENNE[5]] + SIENNE[7:]     # deux coups intervertis
t2 = SIENNE[:-1]                                          # le dernier coup oublie
for nom, t in (("deux coups intervertis", t1), ("dernier coup oublie", t2)):
    r = rejoue(t)
    print("  %-24s -> %s" % (nom, "coup illegal" if r is None else
          ("ACCEPTE" if r in CIBLES else "n'arrive pas")))
assert rejoue(SIENNE) in CIBLES and rejoue(t1) not in CIBLES and rejoue(t2) not in CIBLES
assert mini == 18 and len(sols) == 6 and fin in CIBLES and len(dist) == 181440
assert sum(1 for c, ch in sols if all(x.startswith("I") for x in centre_de(ch)[0])) == 2
