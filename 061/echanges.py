#!/usr/bin/env python3
"""Rétro Math's — n° 61 CHANGING PLACES (Dudeney, 1917).
Combien de fois, entre 15 h et minuit, les aiguilles échangent-elles leurs places, et quand l'aiguille des minutes
est-elle au plus près du IX ? Positions en « minutes du cadran » (0 à 60), calcul exact en fractions.
    python3 echanges.py   (instantané)"""
from fractions import Fraction as F
def echange(a, b):
    """a h p min et b h q min : chaque aiguille prend la place de l'autre (5a + p/12 = q, 5b + q/12 = p)"""
    p = F(720 * b + 60 * a, 143); q = F(720 * a + 60 * b, 143)
    assert 5 * a + p / 12 == q and 5 * b + q / 12 == p and 0 <= p <= 60 and 0 <= q <= 60
    return p, q
HEURES = range(3, 12)                                     # de 15 h à 23 h 59
paires = [(a, b) for a in HEURES for b in HEURES if a < b]
print("échanges entre 15 h et minuit :", len(paires))
assert len(paires) == 36
assert echange(3, 4)[0] == 21 + F(57, 143)                # l'indice de l'article : 3 h 21 et des poussières
# les 72 instants ; lequel met l'aiguille des minutes au plus près du IX (minute 45) ?
instants = []
for a, b in paires:
    p, q = echange(a, b); assert p < 60 and q < 60; instants += [(abs(p - 45), a, p, (b, q)), (abs(q - 45), b, q, (a, p))]
assert len(instants) == 72
d, h, m, autre = min(instants)
print("au plus près du IX : %d h %s min, associé à %d h %s min, écart %s min" % (h, m, autre[0], autre[1], d))
assert (h, m) == (11, 44 + F(128, 143)) and autre == (8, 58 + F(106, 143)) and d == F(15, 143)
assert sorted(x[0] for x in instants)[1] > d               # seul à cette distance
assert d * 6 == F(90, 143)                                 # en degrés
# témoin : avec a = b, la « paire » est une superposition (p = q), que l'on n'a pas le droit de compter
assert all(echange(a, a)[0] == echange(a, a)[1] for a in HEURES)
assert len([(a, b) for a in HEURES for b in HEURES if a <= b]) == 45 != 36
print("contrôles : tout est conforme (témoins refusés)")
