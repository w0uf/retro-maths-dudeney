# -*- coding: utf-8 -*-
"""n° 118 CIRCLING THE SQUARES — dix cases en cercle (A..K). Pour deux cases
voisines, la somme de leurs carrés doit égaler la somme des carrés des deux
cases diamétralement opposées. Quatre nombres sont donnés : A=16, B=2, G=14,
F=8, les opposés étant A-F, B-G, C-H, D-I, E-K."""
from itertools import permutations, combinations
import math

M = 10                                  # cases 0..9 ; opposée de i : i+5
DONNE = {0: 16, 1: 2, 5: 8, 6: 14}      # A, B, F, G

def valide(n):
    for i in range(M):
        j, o, p = (i+1) % M, (i+5) % M, (i+6) % M
        if n[i]**2 + n[j]**2 != n[o]**2 + n[p]**2: return False
    return True

# ── la structure : les paires opposées ont un écart de carrés constant ──
print("A² - F² =", 16**2 - 8**2, "   B² - G² =", 2**2 - 14**2)
print("→ l'écart des carrés de deux cases opposées vaut 192, au signe près")
N = 192
print()
print("192 = (a-b)(a+b), les deux facteurs pairs :")
paires = []
for u in range(1, int((N//4)**.5)+1):
    if (N//4) % u == 0:
        v = (N//4)//u
        paires.append((v+u, v-u))
        print("   2×%-2d et 2×%-2d  →  a = %2d, b = %2d, écart %2d"
              % (u, v, v+u, v-u, (v+u)-(v-u)))
print("les cinq paires :", paires, " (Dudeney : 47-49, 22-26, 13-19, 8-16, 2-14)")
print("écarts :", sorted((a-b) for a, b in paires), " (Dudeney : 2, 4, 6, 8, 12)")

# ── combien de façons de compléter ? balayage complet ───────────────────
reste = [x for p in paires for x in p if x not in DONNE.values()]
libres = [i for i in range(M) if i not in DONNE]
sols = set()
for perm in permutations(reste):
    n = [None]*M
    for i, v in DONNE.items(): n[i] = v
    for i, v in zip(libres, perm): n[i] = v
    if valide(n): sols.add(tuple(n))
print()
print("façons de compléter le cercle :", len(sols), " (Dudeney : six)")
for s in sorted(sols)[:6]: print("   ", s)

# ── sa règle sur la taille du cercle : 4n + 6 ───────────────────────────
print()
print("pour quelles tailles de cercle une telle disposition est-elle possible ?")
for m in range(4, 19, 2):
    k = m//2
    print("   %2d cases : %s" % (m, "possible" if k % 2 == 1 else "IMPOSSIBLE"),
          "(la moitié, %d, est %s)" % (k, "impaire" if k % 2 else "paire"))
print("→ les tailles possibles sont 6, 10, 14, 18…  c'est-à-dire 4n + 6 ✔")

# ── 260, somme de deux carrés de deux façons ────────────────────────────
print()
n = 260
rep = [(a, b) for a in range(1, int(n**.5)+1) for b in range(a, int(n**.5)+1)
       if a*a + b*b == n]
print("260 = somme de deux carrés :", rep)
print("260 = 2² × 5 × 13 ; 5 et 13 sont tous deux de la forme 4k+1,")
print("d'où exactement deux écritures — théorème de Fermat sur les deux carrés.")
for m in (65, 325, 1105):
    r = [(a, b) for a in range(1, int(m**.5)+1) for b in range(a, int(m**.5)+1)
         if a*a + b*b == m]
    print("   %5d → %d écritures : %s" % (m, len(r), r))

# ── la regle 4n + 6, mise a l'epreuve par une recherche directe ──────────
# On ne se sert ici que de la condition elle-meme : une fois choisies deux
# cases opposees et les cases d'un demi-cercle, la condition sur chaque paire
# de voisines impose la case opposee suivante. On garde les dispositions de
# nombres tous differents, de 1 a N, et on les controle en entier par une
# fonction qui ne suppose rien.
from math import isqrt
def valide_m(n):
    m = len(n); k = m // 2
    return all(n[i]**2 + n[(i+1) % m]**2 == n[(i+k) % m]**2 + n[(i+k+1) % m]**2
               for i in range(m))
def recherche(m, N, limite=1):
    k = m // 2; trouve = []
    def suite(n, i):
        if len(trouve) >= limite: return
        if i == k:
            if valide_m(n) and len(set(n)) == m: trouve.append(tuple(n))
            return
        for v in range(1, N + 1):
            if v in n: continue
            c2 = n[i-1]**2 + v*v - n[i-1+k]**2
            if c2 <= 0: continue
            c = isqrt(c2)
            if c*c != c2 or c > N or c in n or c == v: continue
            n[i] = v; n[i+k] = c
            suite(n, i + 1)
            n[i] = n[i+k] = None
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            if a != b:
                n = [None]*m; n[0] = a; n[k] = b
                suite(n, 1)
    return trouve
print()
print("recherche directe, nombres tous differents de 1 a 60 :")
res = {}
for m in (4, 6, 8, 10, 12):
    r = recherche(m, 60)
    res[m] = bool(r)
    print("   %2d cases : %s" % (m, r[0] if r else "aucune disposition"))
# temoin : la fonction de controle doit refuser une disposition faussee
faussee = list(sorted(sols)[0]); faussee[2], faussee[3] = faussee[3], faussee[2]
print("temoin : deux cases voisines echangees ->", "refuse" if not valide_m(faussee) else "ACCEPTE")
assert not valide_m(faussee) and all(valide_m(list(s)) for s in sols)
assert res == {4: False, 6: True, 8: False, 10: True, 12: False} and len(sols) == 6
