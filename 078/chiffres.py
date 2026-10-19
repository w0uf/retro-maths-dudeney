# -*- coding: utf-8 -*-
"""n° 78 ODD AND EVEN DIGITS.
Ecrire avec 1, 3, 5, 7, 9 (chacun une fois) et avec 2, 4, 6, 8 (chacun une fois)
deux sommes egales. Fractions complexes ou impropres et decimales periodiques
interdites. Dudeney : 79 + 5 1/3 = 84 + 2/6, « la plus simple ».
On ecrit TOUTES les sommes possibles de chaque groupe (entiers et fractions
propres p/q), puis on compare.
    python3 chiffres.py          (quelques secondes)"""
from fractions import Fraction as F
from itertools import permutations

def partitions(seq):
    if not seq: yield []; return
    for i in range(1, len(seq) + 1):
        for r in partitions(seq[i:]): yield [seq[:i]] + r

def valeurs(chiffres):
    """{valeur: ensemble d'ecritures} ; une ecriture = (entiers tries, fractions triees)"""
    out = {}
    for perm in permutations(chiffres):
        for blocs in partitions(perm):
            nums = [int("".join(map(str, b))) for b in blocs]
            def rec(i, ent, fr):
                if i == len(nums):
                    if ent == sorted(ent) and fr == sorted(fr):
                        v = sum(ent) + sum(F(p, q) for p, q in fr)
                        out.setdefault(v, set()).add((tuple(ent), tuple(fr)))
                    return
                rec(i + 1, ent + [nums[i]], fr)
                if i + 1 < len(nums) and nums[i] < nums[i + 1]:          # fraction propre
                    rec(i + 2, ent, fr + [(nums[i], nums[i + 1])])
            rec(0, [], [])
    return out

def decimaux(chiffres):
    """variante : entiers et decimaux finis (1,5 ; ,15 ...), sans fraction"""
    out = set()
    for perm in permutations(chiffres):
        for blocs in partitions(perm):
            choix = []
            for b in blocs:
                s = "".join(map(str, b))
                choix.append({F(int(s), 10 ** (len(s) - k)) for k in range(len(s) + 1)})
            def rec(i, acc):
                if i == len(choix): out.add(acc); return
                for x in choix[i]: rec(i + 1, acc + x)
            rec(0, F(0))
    return out

I, P = valeurs([1, 3, 5, 7, 9]), valeurs([2, 4, 6, 8])
com = sorted(set(I) & set(P))
print("sommes ecrites : %d avec les impairs, %d avec les pairs" % (len(I), len(P)))
print("valeurs communes :", [str(v) for v in com])
for v in com:
    print("   %s = %.4f" % (v, v))
    for e, f in sorted(I[v]): print("      impairs :", " + ".join(list(map(str, e)) + ["%d/%d" % x for x in f]))
    for e, f in sorted(P[v]): print("      pairs   :", " + ".join(list(map(str, e)) + ["%d/%d" % x for x in f]))
livre_i, livre_p = ((5, 79), ((1, 3),)), ((84,), ((2, 6),))
print("l'ecriture du livre est dans les deux listes :", livre_i in I[F(253, 3)], livre_p in P[F(253, 3)])
assert com == [F(253, 3)] and livre_i in I[com[0]] and livre_p in P[com[0]]
assert len(I[com[0]]) == 2 and len(P[com[0]]) == 1

# sans fraction : impossible (preuve par neuf : 25 et 20 n'ont pas le meme reste)
ent = lambda V: {v for v, ecr in V.items() if any(not f for e, f in ecr)}
print("\nsans fraction, valeurs communes :", ent(I) & ent(P) or "aucune")
# temoin : deux groupes de meme reste modulo 9 doivent, eux, se rencontrer
t = ent(valeurs([1, 8])) & ent(valeurs([2, 7]))
print("temoin {1, 8} contre {2, 7} (meme reste) : valeurs communes sans fraction", sorted(t))
assert not (ent(I) & ent(P)) and 9 in t

# variante que Dudeney n'exclut pas : les decimaux finis
d = decimaux([1, 3, 5, 7, 9]) & decimaux([2, 4, 6, 8])
print("avec des decimaux finis au lieu des fractions : valeurs communes", sorted(d) or "aucune")
assert F(3, 2) in decimaux([1, 5]) and not d
