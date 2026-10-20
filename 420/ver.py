#!/usr/bin/env python3
"""Rétro Math's — n° 420 THE INDUSTRIOUS BOOKWORM (Dudeney, 1917).
Volumes de 3 pouces de feuillets et deux couvertures de 1/8 de pouce, debout, dos vers le lecteur. Le ver va de la
première page du tome I à la dernière page du dernier tome. On modélise l'étagère : où tombent réellement ces deux
pages ? Livre occidental : vu par le dos, le plat avant est à droite ; livre japonais (reliure à droite) : à gauche.
    python3 ver.py   (instantané)"""
from fractions import Fraction as F
C, P = F(1, 8), F(3)
def trajet(n, livre="occidental", rangement="occidental"):
    """longueur du tunnel, du début du tome I à la fin du tome n"""
    ordre = list(range(1, n + 1)) if rangement == "occidental" else list(range(n, 0, -1))   # de gauche à droite
    x = {v: i * (P + 2 * C) for i, v in enumerate(ordre)}                                   # bord gauche de chaque tome
    def page(v, premiere):
        # la première page est contre le plat avant ; vu par le dos, le plat avant est à droite (occidental) ou à gauche
        avant_a_droite = (livre == "occidental")
        cote_droit = avant_a_droite if premiere else not avant_a_droite
        return x[v] + C + (P if cote_droit else 0)
    return abs(page(n, False) - page(1, True))
assert trajet(3) == 3 + F(1, 2)                                   # trois pouces et demi
assert trajet(10) == 26 + F(1, 4)                                 # dix volumes
for n in range(3, 15):
    assert trajet(n) == (n - 2) * P + (2 * n - 2) * C             # n − 2 volumes de feuillets, 2n − 2 couvertures
assert trajet(3, "japonais", "japonais") == 3 + F(1, 2)           # même réponse : tout est inversé
assert trajet(3, "japonais", "occidental") == 9 + F(1, 2)         # la réponse « pressée » vaut pour cette étagère-là
print("3 tomes : %s ; 10 tomes : %s ; japonais rangés à l'occidentale : %s" % (trajet(3), trajet(10), trajet(3, "japonais")))
# témoin : la réponse pressée, 9 pouces et demi, est refusée pour une étagère ordinaire
assert trajet(3) != 3 * P + 4 * C
print("contrôles : tout est conforme (témoins refusés)")
