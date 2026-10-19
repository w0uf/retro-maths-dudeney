# -*- coding: utf-8 -*-
"""n° 247 INSPECTING A MINE — Dudeney, 1917.

Vingt puits A..T en quadrillage de cinq colonnes sur quatre rangees, trente
et une galeries d'un stade chacune.  L'inspecteur descend en A et doit
parcourir toutes les galeries.  Quelle distance minimale ?

Dudeney : 36 stades, avec cinq galeries parcourues deux fois ; et il ajoute
que « le petit piege est que l'on part d'un noeud pair — sinon il suffirait
de 35 ».

C'est, quarante-cinq ans avant Guan Meigu, le probleme dit « du facteur
chinois » (ou probleme de l'inspection des routes).
"""
from itertools import combinations
NOMS = "ABCDEFGHIJKLMNOPQRST"
POS = {NOMS[r*5+c]: (r, c) for r in range(4) for c in range(5)}
ARETES = []
for r in range(4):
    for c in range(5):
        u = NOMS[r*5+c]
        if c < 4: ARETES.append((u, NOMS[r*5+c+1]))
        if r < 3: ARETES.append((u, NOMS[(r+1)*5+c]))
print("noeuds :", len(POS), "| galeries :", len(ARETES),
      " (Dudeney : trente et une ->", len(ARETES) == 31, ")")

ADJ = {n: [] for n in NOMS}
for u, v in ARETES: ADJ[u].append(v); ADJ[v].append(u)
DEGRE = {n: len(ADJ[n]) for n in NOMS}
IMPAIRS = [n for n in NOMS if DEGRE[n] % 2]
print("noeuds impairs :", "".join(IMPAIRS), "(%d)" % len(IMPAIRS))
print("le point de depart A est de degre", DEGRE["A"], "-> pair")

# --- distances ---------------------------------------------------------
from collections import deque
def dist_depuis(s):
    d = {s: 0}; f = deque([s])
    while f:
        x = f.popleft()
        for y in ADJ[x]:
            if y not in d: d[y] = d[x]+1; f.append(y)
    return d
D = {n: dist_depuis(n) for n in NOMS}

def couplage_min(T):
    """poids minimal d'un couplage parfait des sommets de T"""
    T = list(T)
    if not T: return 0
    from functools import lru_cache
    n = len(T)
    @lru_cache(None)
    def rec(masque):
        if masque == 0: return 0
        i = 0
        while not (masque >> i & 1): i += 1
        best = 10**9
        for j in range(i+1, n):
            if masque >> j & 1:
                best = min(best, D[T[i]][T[j]] + rec(masque & ~(1 << i) & ~(1 << j)))
        return best
    return rec((1 << n) - 1)

print("\n=== Le minimum, selon le point d'arrivee ===")
best = None
for X in NOMS:
    T = set(IMPAIRS) ^ {"A"} ^ ({X} if X != "A" else set())
    if X == "A": T = set(IMPAIRS)
    if len(T) % 2: continue
    w = couplage_min(T)
    if best is None or w < best[0]: best = (w, X)
    if w <= 5: print("   fin en %s : %d galerie(s) refaite(s) -> %d stades" % (X, w, 31+w))
print("  minimum absolu : %d galeries refaites, soit %d stades (Dudeney : 36 -> %s)"
      % (best[0], 31+best[0], 31+best[0] == 36))

print("\n=== Et si l'on partait d'un noeud impair ? ===")
best2 = None
for S in IMPAIRS:
    for X in NOMS:
        T = set(IMPAIRS) ^ {S} ^ ({X} if X != S else set())
        if X == S: T = set(IMPAIRS)
        if len(T) % 2: continue
        w = couplage_min(T)
        if best2 is None or w < best2[0]: best2 = (w, S, X)
print("  minimum : %d galeries refaites, soit %d stades  (depart %s, arrivee %s)"
      % (best2[0], 31+best2[0], best2[1], best2[2]))
print("  Dudeney : « sinon il suffirait de 35 » ->", 31+best2[0] == 35)

# --- sa tournee --------------------------------------------------------
print("\n=== Sa tournee, rejouee ===")
R = "A B G H C D I H M N I J O N S R M L G F K L Q R S T O J E D C B A F K P Q".split()
from collections import Counter
ok = True; passages = Counter()
for u, v in zip(R, R[1:]):
    if v not in ADJ[u]: print("   pas de galerie entre", u, "et", v); ok = False
    passages[frozenset((u, v))] += 1
print("  tous les pas sont des galeries :", ok)
print("  longueur :", len(R)-1, "stades")
print("  galeries visitees :", len(passages), "sur 31 ->", len(passages) == 31)
deux = [tuple(sorted(k)) for k, v in passages.items() if v == 2]
print("  galeries parcourues deux fois :", len(deux), sorted(deux))
print("  Dudeney annonce cinq repetitions ->", len(deux) == 5)
print("  il part de A et finit en", R[-1])

# temoins : une tournee fautive doit etre refusee
print("\n=== Temoins ===")
def tournee_valide(R):
    if R[0] != "A" or any(v not in ADJ[u] for u, v in zip(R, R[1:])): return False
    return len({frozenset(e) for e in zip(R, R[1:])}) == 31
R1 = R[:10] + R[11:]                                   # un puits saute
R2 = R[:-3]                                            # trois stades en moins
print("  sa tournee acceptee :", tournee_valide(R))
print("  un puits saute (%s) : %s" % (R[10], "refusee" if not tournee_valide(R1) else "ACCEPTEE"))
print("  trois derniers stades retires : %s" % ("refusee" if not tournee_valide(R2) else "ACCEPTEE"))
print("  le couplage minimal sur deux coins opposes (A, T) vaut 7 :", couplage_min({"A", "T"}) == 7)
assert tournee_valide(R) and not tournee_valide(R1) and not tournee_valide(R2)
assert couplage_min({"A", "T"}) == 7 and best[0] == 5 and best2[0] == 4 and len(deux) == 5
