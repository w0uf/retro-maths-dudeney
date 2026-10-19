# -*- coding: utf-8 -*-
"""n° 140 FIND ADA'S SURNAME — Dudeney, 1917.

Cinq dames et leurs cinq filles achetent du drap ; chacune paie autant de
farthings par pied qu'elle achete de pieds — sa depense est donc le CARRE
du nombre de pieds.  Chaque mere depense 8 s 5 d 1/4 de plus que sa fille.
Un journal de Sydney a refuse ce probleme en le declarant « puerile » et
insoluble.
"""
from itertools import permutations
from math import isqrt

F = 4                                  # quatre farthings dans un penny
ECART  = (8*12 + 5)*F + 1              # 8 s 5 d 1/4, en farthings
SIX_SH = 6*12*F                        # 6 shillings
TROIS_L = (3*240 + 8)*F                # 3 livres 0 s 8 d
print("ecart mere-fille :", ECART, "farthings |  6 shillings :", SIX_SH,
      "| 3 L 0 s 8 d :", TROIS_L)

# --- les couples mere-fille possibles ---------------------------------
couples = []
for d in range(1, 3000):
    m2 = d*d + ECART
    m = isqrt(m2)
    if m*m == m2: couples.append((m, d))
print("\ncouples (pieds de la mere, pieds de la fille) :", couples)
print("  il y en a exactement cinq, et il y a cinq meres : chacun sert une fois.")

MERES = ["Robinson", "Evans", "Jones", "Smith", "Brown"]
FILLES = ["Bessie", "Annie", "Mary", "Emily", "Ada"]

def cherche(avec_le_quart):
    sols = []
    for attrib in permutations(couples):          # attrib[i] = couple de MERES[i]
        M = {n: c[0] for n, c in zip(MERES, attrib)}
        fille_de = {n: c[1] for n, c in zip(MERES, attrib)}
        if M["Robinson"]**2 - M["Evans"]**2 != SIX_SH: continue
        if M["Smith"] != max(M.values()): continue
        if avec_le_quart:
            if not (0.20 <= M["Evans"]**2 / M["Jones"]**2 <= 0.30): continue
        for noms in permutations(FILLES):         # noms[i] = prenom de la fille de MERES[i]
            pieds = {p: fille_de[m] for p, m in zip(noms, MERES)}
            if M["Brown"] - pieds["Bessie"] != 63: continue        # 21 yards
            if pieds["Annie"] - pieds["Mary"] != 48: continue      # 16 yards
            if pieds["Annie"]**2 - pieds["Emily"]**2 != TROIS_L: continue
            sols.append({p: m for p, m in zip(noms, MERES)})
    return sols

for avec in (True, False):
    s = cherche(avec)
    print("\n=== %s la clause « environ le quart » ===" % ("Avec" if avec else "SANS"))
    print("  solutions :", len(s))
    for x in s:
        print("   ", ", ".join("%s %s" % (p, x[p]) for p in FILLES))
print("\nDudeney : Ada Smith, Annie Brown, Emily Jones, Mary Robinson, Bessie Evans")

print("\n=== La clause approximative, de plus pres ===")
def depenses(sol):
    """pieds achetes par chaque mere dans une attribution prenom -> nom de famille"""
    for attrib in permutations(couples):
        M = {n: c[0] for n, c in zip(MERES, attrib)}
        fille_de = {n: c[1] for n, c in zip(MERES, attrib)}
        pieds = {p: fille_de[m] for p, m in sol.items()}
        if (M["Robinson"]**2 - M["Evans"]**2 == SIX_SH and M["Smith"] == max(M.values())
                and M["Brown"] - pieds["Bessie"] == 63 and pieds["Annie"] - pieds["Mary"] == 48
                and pieds["Annie"]**2 - pieds["Emily"]**2 == TROIS_L):
            return M
    return None
SIENNE = {"Ada": "Smith", "Annie": "Brown", "Emily": "Jones", "Mary": "Robinson", "Bessie": "Evans"}
M = depenses(SIENNE)
ev, jo = M["Evans"]**2, M["Jones"]**2
print("  dans la bonne solution, Mme Evans depense %d farthings et Mme Jones %d ;" % (ev, jo))
print("  le rapport vaut %.4f — « environ le quart », en effet, mais a 5 %% pres." % (ev/jo))

# temoins : une attribution fausse doit etre refusee, et un ecart mal converti
# ne doit plus donner cinq couples
print("\n=== Temoins ===")
FAUSSE = dict(SIENNE); FAUSSE["Ada"], FAUSSE["Emily"] = "Jones", "Smith"
print("  la sienne acceptee :", M is not None, "| Ada et Emily echangees refusee :", depenses(FAUSSE) is None)
n404 = sum(1 for d in range(1, 3000) if isqrt(d*d + 404)**2 == d*d + 404)
print("  avec un ecart de 404 farthings (le quart de penny oublie) : %d couple(s) au lieu de 5" % n404)
assert M is not None and depenses(FAUSSE) is None and n404 != 5
assert len(couples) == 5 and cherche(True) == cherche(False) == [SIENNE]
