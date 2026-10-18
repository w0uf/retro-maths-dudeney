# -*- coding: utf-8 -*-
"""n° 343 EXERCISE FOR PRISONERS.

Un taquin de quinze dans seize cellules. Les prisonniers veulent se ranger en
un PARCOURS DE CAVALIER parfait (1, 2, 3... 15 se suivant par sauts de
cavalier), la cellule du coin inferieur droit restant vide, en laissant au repos
le plus d'hommes possible, et en le moins de coups possible.
"""
from itertools import permutations

N = 4
CELLS = [(r, c) for r in range(N) for c in range(N)]
VIDE = (3, 3)
OCC = [p for p in CELLS if p != VIDE]
def cav(a, b):
    return sorted((abs(a[0]-b[0]), abs(a[1]-b[1]))) == [1, 2]
ADJ = {p: [q for q in OCC if cav(p, q)] for p in OCC}

# ═══ 1. les parcours de cavalier ═══════════════════════════════════════
chemins = []
def rec(ch, vus):
    if len(ch) == 15: chemins.append(list(ch)); return
    for q in ADJ[ch[-1]]:
        if q not in vus:
            vus.add(q); ch.append(q); rec(ch, vus); ch.pop(); vus.remove(q)
for d in OCC:
    rec([d], {d})
print("=== Les parcours de cavalier ===")
print("  arrangements formant un parcours parfait : %d" % len(chemins))
print("  (chaque chemin compte deux fois : numerote dans un sens ou dans")
print("   l'autre ; cela fait donc %d chemins geometriques.)" % (len(chemins)//2))
print("  Dudeney annonce quatre-vingts :", len(chemins) == 80)

# ═══ 2. lesquels sont atteignables ? ═══════════════════════════════════
DEPART = {}
for k, p in enumerate(OCC): DEPART[p] = k + 1     # 1..15 en lecture naturelle
def grille(ch):
    g = {}
    for k, p in enumerate(ch): g[p] = k + 1
    return g
def parite(g):
    """parite de la permutation des quinze hommes, le vide restant au coin"""
    ordre = [g[p] for p in OCC]
    vu = [False]*16; t = 0
    for i in range(15):
        if vu[i]: continue
        j, l = i, 0
        while not vu[j]:
            vu[j] = True; j = ordre[j] - 1; l += 1
        t += l - 1
    return t % 2
att = [ch for ch in chemins if parite(grille(ch)) == 0]
print()
print("=== Lesquels peuvent etre atteints sans que deux hommes se croisent ? ===")
print("  arrangements de parite paire (donc atteignables) : %d" % len(att))
print("  Dudeney annonce quarante :", len(att) == 40)

# ═══ 3. combien d'hommes au repos ? ════════════════════════════════════
def repos(ch):
    g = grille(ch)
    return frozenset(g[p] for p in OCC if g[p] == DEPART[p])
print()
print("=== Combien d'hommes peuvent rester au repos ? ===")
tous = sorted({len(repos(ch)) for ch in chemins})
print("  sur les 80 arrangements, nombres d'hommes immobiles possibles : %s" % tous)
paires = sorted({tuple(sorted(repos(ch))) for ch in chemins if len(repos(ch)) == 2})
print("  paires d'hommes pouvant rester en place : %s"
      % ", ".join("%d et %d" % p for p in paires))
print("  Dudeney annonce 7-13, 8-13, 5-7 et 5-13 :",
      paires == [(5,7),(5,13),(7,13),(8,13)])
attr = [ch for ch in att if len(repos(ch)) == 2]
print("  parmi les ATTEIGNABLES, paires possibles : %s"
      % ", ".join("%d et %d" % p for p in sorted({tuple(sorted(repos(ch)))
                                                  for ch in attr})))
print("  et nombre d'arrangements correspondants : %d" % len(attr))
print("  Dudeney annonce quatre arrangements, tous avec 7 et 13 :",
      len(attr) == 4 and all(repos(ch) == frozenset({7, 13}) for ch in attr))
print()
for k, ch in enumerate(attr, 1):
    g = grille(ch)
    print("   arrangement %d :" % k)
    for r in range(4):
        print("      " + " ".join("%2s" % (g.get((r, c), "**")) for c in range(4)))

# ═══ 4. la distance de Manhattan, pour jauger la difficulte ════════════
print()
print("=== Distance de Manhattan de chaque cible (borne inferieure) ===")
def manhattan(ch):
    g = grille(ch); d = 0
    for p, t in g.items():
        q = OCC[t-1]
        d += abs(p[0]-q[0]) + abs(p[1]-q[1])
    return d
for k, ch in enumerate(attr, 1):
    g = grille(ch)
    print("  cible %d : repos {%s}, Manhattan %d"
          % (k, ", ".join(map(str, sorted(repos(ch)))), manhattan(ch)))

# ═══ 5. on ecrit les cibles pour le solveur ════════════════════════════
import io as _io
with _io.open("cibles.txt", "w") as f:
    for ch in attr:
        g = grille(ch)
        f.write(" ".join(str(g.get((r, c), 0)) for r in range(4) for c in range(4)) + "\n")
print()
print("cibles.txt ecrit : %d cibles" % len(attr))
