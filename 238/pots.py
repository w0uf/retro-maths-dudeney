# -*- coding: utf-8 -*-
"""n° 238 ARRANGING THE JAM POTS.

Vingt-quatre pots de confiture dans vingt-quatre casiers, a remettre dans
l'ordre en echangeant deux pots a la fois. Dudeney : « vingt-deux echanges les
remettront tous en place. Mais ce n'est pas le minimum : la bonne reponse est
dix-sept. »

L'arrangement est LU SUR LA GRAVURE (q238.png), quatre rangees de six :
"""
from fractions import Fraction

GRAVURE = [3, 1, 2, 15, 8, 21,
           17, 6, 18, 24, 12, 10,
           13, 9, 16, 4, 20, 5,
           19, 7, 23, 14, 22, 11]
N = 24

print("=== La lecture de la gravure ===")
for r in range(4):
    print("   " + "  ".join("%2d" % x for x in GRAVURE[6*r:6*r+6]))
print("  les 24 pots sont-ils tous presents une fois :",
      sorted(GRAVURE) == list(range(1, N+1)))
fixes = [i+1 for i in range(N) if GRAVURE[i] == i+1]
print("  pots deja a leur place : %s" % fixes)
print("  Dudeney ecrit : « deux des pots, 13 et 19, etaient a leur place ».")
print("  -> la lecture de la gravure est confirmee par son propre texte.")

# ═══ les cycles ════════════════════════════════════════════════════════
vus = [False]*(N+1); cycles = []
for d in range(1, N+1):
    if vus[d]: continue
    c, x = [], d
    while not vus[x]:
        vus[x] = True; c.append(x); x = GRAVURE[x-1]
    cycles.append(c)
print()
print("=== Les cycles de l'arrangement ===")
for c in cycles:
    print("   longueur %2d : %s" % (len(c), " -> ".join(map(str, c))))
print("  nombre de cycles : %d" % len(cycles))
print("  minimum d'echanges = %d - %d = %d" % (N, len(cycles), N - len(cycles)))
print("  Dudeney annonce dix-sept.")
print("  cycles de longueur 1 (pots deja places) : %d"
      % sum(1 for c in cycles if len(c) == 1))
print("  d'ou son calcul : %d - %d (les cinq parentheses) = %d"
      % (N - sum(1 for c in cycles if len(c) == 1),
         sum(1 for c in cycles if len(c) > 1),
         N - len(cycles)))

# ═══ sa liste de dix-sept echanges, jouee coup par coup ════════════════
SIENNE = [(3,1),(2,3), (15,4),(16,15), (17,7),(20,17),
          (24,10),(11,24),(12,11),
          (8,5),(6,8),(21,6),(23,21),(22,23),(14,22),(9,14),(18,9)]
print()
print("=== Ses dix-sept echanges, joues un par un ===")
pos = {p: i for i, p in enumerate(GRAVURE)}       # pot -> casier
etat = list(GRAVURE)
for k, (a, b) in enumerate(SIENNE, 1):
    ia, ib = pos[a], pos[b]
    etat[ia], etat[ib] = etat[ib], etat[ia]
    pos[a], pos[b] = ib, ia
justes = sum(1 for i in range(N) if etat[i] == i+1)
print("  nombre d'echanges : %d" % len(SIENNE))
print("  pots a leur place a la fin : %d sur %d" % (justes, N))
print("  l'arrangement est trie :", etat == list(range(1, N+1)))

# ═══ le theoreme, valide sur des temoins ═══════════════════════════════
print()
print("=== « minimum = n - nombre de cycles » : verification sur temoins ===")
import itertools, random
def cycles_de(p):
    n = len(p); v = [False]*n; k = 0
    for d in range(n):
        if v[d]: continue
        k += 1; x = d
        while not v[x]: v[x] = True; x = p[x]-1
    return k
def minimum_force_brute(p):
    """recherche exhaustive du nombre minimal d'echanges (petites tailles)"""
    from collections import deque
    n = len(p); but = tuple(range(1, n+1))
    d = {tuple(p): 0}; f = deque([tuple(p)])
    while f:
        e = f.popleft()
        if e == but: return d[e]
        for i in range(n):
            for j in range(i+1, n):
                s = list(e); s[i], s[j] = s[j], s[i]; s = tuple(s)
                if s not in d: d[s] = d[e]+1; f.append(s)
    return None
ok = True
for n in range(2, 7):
    for p in itertools.permutations(range(1, n+1)):
        if minimum_force_brute(list(p)) != n - cycles_de(list(p)): ok = False
print("  toutes les permutations de 2 a 6 elements (%d cas) : formule exacte %s"
      % (sum(len(list(itertools.permutations(range(n)))) for n in range(2,7)), ok))

# ═══ Dorothy a-t-elle eu de la chance ? ════════════════════════════════
print()
print("=== L'arrangement de Dorothy est-il facile ou difficile ? ===")
# nombres de Stirling de premiere espece non signes : repartition du nombre
# de cycles d'une permutation de 24 elements prise au hasard
S = [[0]*(N+1) for _ in range(N+1)]
S[0][0] = 1
for n in range(1, N+1):
    for k in range(1, n+1):
        S[n][k] = S[n-1][k-1] + (n-1)*S[n-1][k]
total = sum(S[N])
H = sum(Fraction(1, i) for i in range(1, N+1))
print("  nombre moyen de cycles d'un rangement au hasard : %.4f" % float(H))
print("  donc nombre moyen d'echanges necessaires : %.2f" % (N - float(H)))
print("  l'arrangement de la gravure en a %d, soit %d echanges." % (len(cycles), N-len(cycles)))
p = sum(S[N][k] for k in range(len(cycles), N+1)) / total
print("  proportion des rangements aussi faciles ou plus faciles : %.4f %%"
      % (100*p))
print("  maximum possible (un seul grand cycle) : %d echanges" % (N-1))
print("  -> son rangement est nettement plus commode que la moyenne.")

# ═══ temoins : une lecture ou une liste fautive doit etre refusee ══════════
print()
print("=== Temoins ===")
def joue(depart, echanges):
    etat = list(depart); pos = {p: i for i, p in enumerate(etat)}
    for a, b in echanges:
        ia, ib = pos[a], pos[b]
        etat[ia], etat[ib] = etat[ib], etat[ia]; pos[a], pos[b] = ib, ia
    return etat == list(range(1, N+1))
print("  ses 17 echanges trient la gravure :", joue(GRAVURE, SIENNE))
print("  sans le dernier echange           :", joue(GRAVURE, SIENNE[:-1]), "-> refuse")
LUE_MAL = list(GRAVURE); i, j = LUE_MAL.index(13), LUE_MAL.index(14)
LUE_MAL[i], LUE_MAL[j] = LUE_MAL[j], LUE_MAL[i]
fx = [k+1 for k in range(N) if LUE_MAL[k] == k+1]
print("  gravure lue avec 13 et 14 echanges : pots en place %s, et non [13, 19] -> refusee" % fx)
print("  la force brute refuse une formule fausse (n - points fixes) :",
      minimum_force_brute([2, 3, 1]) != 3 - 0)
assert joue(GRAVURE, SIENNE) and not joue(GRAVURE, SIENNE[:-1]) and fx != [13, 19]
assert fixes == [13, 19] and N - len(cycles) == 17 and ok
