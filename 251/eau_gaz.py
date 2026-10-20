#!/usr/bin/env python3
"""Rétro Math's — n° 251 WATER, GAS, AND ELECTRICITY (Dudeney, 1917).
Trois usines (W, G, E), trois maisons (A, B, C), neuf conduites sans croisement : impossible sur une feuille.
Contrôle des deux preuves du commentaire : le grand circuit W–A–G–B–E–C–W et ses trois diagonales entrelacées ;
puis le comptage d'Euler. Et la bouée (tore), où l'inégalité passe.
    python3 eau_gaz.py   (instantané)"""
from itertools import combinations
USINES, MAISONS = "WGE", "ABC"
ARETES = {frozenset((u, m)) for u in USINES for m in MAISONS}
assert len(ARETES) == 9
CYCLE = "WAGBEC"
bords = {frozenset((CYCLE[i], CYCLE[(i + 1) % 6])) for i in range(6)}
assert bords <= ARETES and len(bords) == 6                       # le grand circuit n'emploie que des conduites permises
cordes = ARETES - bords
assert cordes == {frozenset("WB"), frozenset("GC"), frozenset("EA")}
def entrelacees(c1, c2, cycle=CYCLE):
    """deux cordes d'un cycle se croisent si l'on dessine les deux du même côté : leurs extrémités alternent"""
    a, b = sorted(cycle.index(x) for x in c1); c, d = sorted(cycle.index(x) for x in c2)
    return (a < c < b) != (a < d < b) and not {a, b} & {c, d}
def deux_cotes(cordes, cycle=CYCLE):
    """peut-on répartir les cordes dedans/dehors sans croisement ? (graphe des conflits biparti)"""
    cordes = list(cordes)
    for choix in range(2 ** len(cordes)):
        cote = [(choix >> i) & 1 for i in range(len(cordes))]
        if all(not (cote[i] == cote[j] and entrelacees(cordes[i], cordes[j], cycle)) for i, j in combinations(range(len(cordes)), 2)):
            return True
    return False
assert all(entrelacees(x, y) for x, y in combinations(cordes, 2))       # deux à deux entrelacées
assert not deux_cotes(cordes)                                            # neuf conduites : impossible
assert all(deux_cotes(cordes - {c}) for c in cordes)                    # huit conduites : toujours possible
# le comptage d'Euler : S − A + F = 2 ; pas de circuit de longueur 3 (biparti) : chaque région bordée par au moins 4
S, A = 6, 9
F = 2 - S + A
assert F == 5 and 2 * A == 18 < 4 * F == 20
assert not any(len({x for e in t for x in e}) == 3 and all(e in ARETES for e in t)
               for t in combinations([frozenset(p) for p in combinations(USINES + MAISONS, 2)], 3))
# sur une bouée : S − A + F = 0, F = 3, et 18 >= 12 : l'obstacle disparaît
assert 0 - S + A == 3 and 2 * A >= 4 * 3
# témoins : un hexagone avec trois cordes « courtes » non entrelacées se dessine ; et K4 (planaire) passe Euler
courtes = {frozenset((CYCLE[0], CYCLE[2])), frozenset((CYCLE[2], CYCLE[4])), frozenset((CYCLE[4], CYCLE[0]))}
assert deux_cotes(courtes)
assert 3 * (2 - 4 + 6) <= 2 * 6                               # K4 : S = 4, A = 6, F = 4, régions triangulaires : 12 <= 12
print("neuf conduites : impossible ; huit : possible ; bouée : l'inégalité passe")
print("contrôles : tout est conforme (témoins refusés)")
