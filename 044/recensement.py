#!/usr/bin/env python3
"""Rétro Math's — n° 44 A CENSUS PUZZLE (Dudeney, 1917).
Quinze enfants nés à un an et demi d'intervalle ; l'aînée, Ada, est « sept fois plus âgée » que Johnnie, le cadet.
Les deux lectures de « sept fois plus », et quand Ada aura-t-elle le double de l'âge de Johnnie ?
    python3 recensement.py   (instantané)"""
from fractions import Fraction as F
ecart = 14 * F(3, 2)
assert ecart == 21                                        # quatorze intervalles d'un an et demi
def ages(k):
    """Ada = k fois Johnnie et Ada = Johnnie + 21"""
    j = ecart / (k - 1); return k * j, j
dudeney, aujourdhui = ages(8), ages(7)                    # « plus âgée de sept fois son âge » / « sept fois son âge »
print("lecture de Dudeney :", dudeney, "| lecture d'aujourd'hui :", aujourdhui)
assert dudeney == (24, 3) and dudeney[0] == dudeney[1] + 7 * dudeney[1]
assert aujourdhui == (F(49, 2), F(7, 2)) and aujourdhui[0] == 7 * aujourdhui[1]
# le double : quand Johnnie aura l'écart, 21 ans ; Ada en aura 42, quelle que soit la lecture
for a, j in (dudeney, aujourdhui):
    attente = ecart - j
    assert a + attente == 2 * (j + attente) and a + attente == 42
assert ecart - dudeney[1] == 18 and ecart - aujourdhui[1] == F(35, 2)
# témoin : la lecture « sept fois » mal appliquée à la lecture de Dudeney donne une contradiction
assert ages(8) != ages(7)
print("contrôles : tout est conforme (témoins refusés)")
