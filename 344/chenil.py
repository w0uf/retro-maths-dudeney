"""n° 344 THE KENNEL PUZZLE : rejeu des 46 coups de Dudeney, puis bornes pour toutes les chaînes de cavalier."""
import sys
L = lambda k: divmod(k - 1, 5)          # chenil 1..25 -> (rangée, colonne)
CIBLE = {1:1,2:18,3:9,4:14,5:5,6:8,7:13,8:4,9:19,10:10,11:17,12:2,13:11,14:6,15:15,16:12,17:7,18:16,19:3,20:20}  # chenil -> chien
COUPS = "16-21 16-22 16-23 17-16 12-17 12-22 12-21 7-12 7-17 7-22 11-12 11-17 2-7 2-12 6-11 8-7 8-6 13-8 18-13 11-18 2-17 18-12 18-7 18-2 13-7 3-8 3-13 4-3 4-8 9-4 9-3 14-9 14-4 19-14 19-9 3-14 3-19 6-12 6-13 6-14 17-11 12-16 2-12 7-17 11-13 16-18".split()
def rejoue(coups):
    ou = {d: d for d in range(1, 21)}; occ = {d: d for d in range(1, 21)}
    for c in coups:
        d, k = map(int, c.split("-")); a = ou[d]
        (r1, c1), (r2, c2) = L(a), L(k)
        assert abs(r1 - r2) + abs(c1 - c2) == 1, ("pas voisin", c)
        assert k not in occ, ("chenil occupé", c)
        del occ[a]; occ[k] = d; ou[d] = k
    return occ
fin = rejoue(COUPS)
print("46 coups rejoués :", len(COUPS), "| position finale = la sienne :", fin == CIBLE)
cav = lambda a, b: sorted(map(abs, (L(a)[0]-L(b)[0], L(a)[1]-L(b)[1]))) == [1, 2]
inv = {d: k for k, d in CIBLE.items()}
print("chaîne de cavalier :", all(cav(inv[d], inv[d+1]) for d in range(1, 20)), "| chiens immobiles :", [d for d in range(1, 21) if inv[d] == d])
man = lambda a, b: abs(L(a)[0]-L(b)[0]) + abs(L(a)[1]-L(b)[1])
print("borne de Manhattan pour sa chaîne :", sum(man(d, inv[d]) for d in range(1, 21)))
# toutes les chaînes de cavalier sur les 20 chenils du haut
V = {a: [b for b in range(1, 21) if cav(a, b)] for a in range(1, 21)}
chaines = []
def dfs(ch, vu):
    if len(ch) == 20: chaines.append(list(ch)); return
    for b in V[ch[-1]]:
        if b not in vu: vu.add(b); ch.append(b); dfs(ch, vu); ch.pop(); vu.discard(b)
for s in range(1, 21): dfs([s], {s})
print("chaînes de cavalier (orientées) :", len(chaines))
B = sorted((sum(man(d, ch[d-1]) for d in range(1, 21)), ch) for ch in chaines)
from collections import Counter
print("bornes de Manhattan, les plus petites :", Counter(b for b, _ in B).most_common()[:0] or sorted(Counter(b for b, _ in B).items())[:8])
print("meilleure :", B[0])
import json, os; json.dump(B, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chaines.json"), "w"))
assert fin == CIBLE and len(COUPS) == 46 and len(chaines) == 164 and B[0][0] == 32
assert sum(man(d, inv[d]) for d in range(1, 21)) == 36
# témoin : sa suite privée d'un coup ne doit pas passer le contrôle
try:
    print("témoin accepté :", rejoue(COUPS[:10] + COUPS[11:]) == CIBLE); raise SystemExit("ERREUR")
except AssertionError as e: print("témoin (un coup retiré) refusé :", e.args[0][0])
