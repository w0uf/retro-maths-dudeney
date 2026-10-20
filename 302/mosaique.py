"""n° 302 A PROBLEM IN MOSAICS : 62 carreaux de 8 couleurs, aucune couleur deux fois sur une même ligne,
colonne ou diagonale ; deux cases occupées par des bouches d'aération. Combien de pavages pour chaque emplacement ?"""
from itertools import combinations
def reines(n=8):
    S = []
    def rec(r, cols):
        if r == n: S.append(tuple(cols)); return
        for c in range(n):
            if all(c != cc and abs(c - cc) != r - rr for rr, cc in enumerate(cols)): rec(r + 1, cols + [c])
    rec(0, []); return [frozenset((r, c) for r, c in enumerate(s)) for s in S]
Q = reines(); print("solutions des huit dames :", len(Q))
ok = lambda a, b: a[0] != b[0] and a[1] != b[1] and abs(a[0] - b[0]) != abs(a[1] - b[1])
def pavages(trous):
    """partitions des 62 cases en 6 solutions complètes + 2 ensembles de 7 cases sans alignement"""
    T = set(trous); cand = [q for q in Q if not q & T]
    res = []
    def rec(i, pris, choix):
        if len(choix) == 6:
            reste = sorted(set((r, c) for r in range(8) for c in range(8)) - pris - T)
            # partager les 14 cases restantes en deux groupes de 7 sans alignement
            a = reste[0]
            for g in combinations(reste[1:], 6):
                G = (a,) + g; H = [x for x in reste if x not in G]
                if all(ok(x, y) for x, y in combinations(G, 2)) and all(ok(x, y) for x, y in combinations(H, 2)):
                    res.append((tuple(sorted(map(tuple, map(sorted, choix)))), tuple(G), tuple(H)))
            return
        for j in range(i, len(cand)):
            if not cand[j] & pris: rec(j + 1, pris | cand[j], choix + [cand[j]])
    rec(0, frozenset(), []); return res
for nom, trous in (("bouches dans les coins du bas (énoncé)", [(7, 0), (7, 7)]), ("bouches sur les cases cerclées (question)", [(2, 2), (2, 5)])):
    P = pavages(trous)
    print(nom, ":", len(P), "pavage(s) (à la couleur près)")
    for p in P: print("   ", p[1], p[2])
# le dallage de l'énoncé, relevé dans le texte de Gutenberg (V R Y G O P W B), bouches en bas aux coins
G0 = ["VRYGOPWB", "WBOPYGVR", "GPWVBRYO", "RYBOGVPW", "BGRYPWOV", "OVPWRYBG", "PWGBVORY", ".OVRWBG."]
cl = {}
for r, l in enumerate(G0):
    for c, ch in enumerate(l):
        if ch != ".": cl.setdefault(ch, set()).add((r, c))
print("énoncé : tailles des couleurs", {k: len(v) for k, v in cl.items()}, "| sans alignement :", all(ok(x, y) for v in cl.values() for x, y in combinations(sorted(v), 2)))
# combien de carreaux peuvent rester en place, au mieux, quand on passe aux nouvelles bouches ?
from itertools import permutations
P = pavages([(2, 2), (2, 5)]); meilleur = []
for six, g, h in P:
    classes = [set(s) for s in six]; sept = [set(g), set(h)]
    for perm in permutations("VRGOWB"):
        f6 = sum(len(classes[i] & cl[perm[i]]) for i in range(6))
        for yp in (("Y", "P"), ("P", "Y")):
            tot = f6 + len(sept[0] & cl[yp[0]]) + len(sept[1] & cl[yp[1]])
            meilleur.append(tot)
print("carreaux qui peuvent rester en place, au mieux :", max(meilleur), "sur 62 → au moins", 62 - max(meilleur), "à déplacer")
# le corrigé, relevé sur la gravure a302
G1 = ["VYRGOWPB", "ROBYPVGW", "BW.OG.RV", "PGVWRBOY", "WBOPYGVR", "GRYVBPWO", "YVGRWOBP", "OPWBVRYG"]
c1 = {}
for r, l in enumerate(G1):
    for c, ch in enumerate(l):
        if ch != ".": c1.setdefault(ch, set()).add((r, c))
print("corrigé : tailles", {k: len(v) for k, v in sorted(c1.items())}, "| sans alignement :", all(ok(x, y) for v in c1.values() for x, y in combinations(sorted(v), 2)))
cles = {frozenset(frozenset(v) for v in c1.values())}
print("le corrigé est l'un des 9 :", any(frozenset([frozenset(s) for s in six] + [frozenset(g), frozenset(h)]) in cles for six, g, h in P))
print("carreaux restés en place dans le corrigé :", sum(1 for r in range(8) for c in range(8) if G0[r][c] == G1[r][c] != "."))
# témoin : deux carreaux échangés dans le corrigé doivent être refusés
G2 = [list(l) for l in G1]; G2[0][0], G2[0][1] = G2[0][1], G2[0][0]
c2 = {}
for r, l in enumerate(G2):
    for c, ch in enumerate(l):
        if ch != ".": c2.setdefault(ch, set()).add((r, c))
print("témoin (V et Y échangés en haut à gauche) refusé :", not all(ok(x, y) for v in c2.values() for x, y in combinations(sorted(v), 2)))
assert len(pavages([(7, 0), (7, 7)])) == 2 and len(P) == 9 and max(meilleur) == 42
