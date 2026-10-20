#!/usr/bin/env python3
"""Rétro Math's — n° 358 THE SIX PAWNS (Dudeney, 1917).
Six pions sur l'échiquier, de façon qu'il reste un nombre pair de cases vides dans chaque rangée et chaque colonne :
c'est dire un nombre pair de pions par ligne. Sur un damier de côté impair, Dudeney demande un nombre impair de cases
vides : la même condition sur les pions. Comptage rangée par rangée (état : parité de chaque colonne), puis contrôle
par force brute sur les petits damiers, et sa formule 6·C(n, 3)².
    python3 six_pions.py   (quelques secondes)"""
from functools import lru_cache
from itertools import combinations
from math import comb

def compte(n, k):
    """dispositions de k pions sur n × n, nombre pair de pions dans chaque rangée et chaque colonne"""
    rangees = [m for m in range(1 << n) if bin(m).count('1') % 2 == 0]
    @lru_cache(None)
    def rec(r, par, reste):
        if r == n: return 1 if reste == 0 and par == 0 else 0
        return sum(rec(r + 1, par ^ m, reste - bin(m).count('1')) for m in rangees if bin(m).count('1') <= reste)
    return rec(0, 0, k)

def force_brute(n, k):
    t = 0
    for S in combinations(range(n * n), k):
        if all(sum(1 for s in S if s // n == i) % 2 == 0 and sum(1 for s in S if s % n == i) % 2 == 0 for i in range(n)): t += 1
    return t

for n in range(3, 10):
    c = compte(n, 6); f = 6 * comb(n, 3) ** 2
    print("damier %d : %d | formule 6·C(n,3)² = %d" % (n, c, f))
    assert c == f                                            # sa formule, « pour tous les carrés plus grands que deux »
assert compte(8, 6) == 18816
assert compte(8, 4) == 784 == comb(8, 2) ** 2               # quatre pions : un carré parfait
assert compte(8, 8) == 586040                               # huit pions : plus de formule simple
print("échiquier : 4 pions 784, 6 pions 18 816, 8 pions 586 040 ; une disposition sur %.0f" % (comb(64, 6) / 18816))
assert round(comb(64, 6) / 18816) == 3985
# recoupement par force brute, independant du comptage rangee par rangee
for n in (3, 4, 5):
    assert force_brute(n, 6) == compte(n, 6)
assert force_brute(4, 4) == compte(4, 4)
# temoin : la lecture litterale « nombre pair de cases vides » sur un damier impair (donc pions en nombre impair
# par ligne) ne donne pas la formule ; la condition de parite est donc bien lue
def litteral(n, k):
    rangees = [m for m in range(1 << n) if (n - bin(m).count('1')) % 2 == 0]
    @lru_cache(None)
    def rec(r, par, reste):
        if r == n: return 1 if reste == 0 and par == (0 if n % 2 == 0 else (1 << n) - 1) else 0
        return sum(rec(r + 1, par ^ m, reste - bin(m).count('1')) for m in rangees if bin(m).count('1') <= reste)
    return rec(0, 0, k)
assert litteral(5, 6) != 6 * comb(5, 3) ** 2 and litteral(8, 6) == 18816
print("controles : tout est conforme (temoins refuses)")
