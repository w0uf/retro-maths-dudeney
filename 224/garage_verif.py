# -*- coding: utf-8 -*-
"""Verification de la sequence de 43 coups publiee par Dudeney en 1917."""
NOM = "ABCDEFGHIJKL"
ADJ = {}
for a, b in [("AB"),("BC"),("CD"),("BE"),("EF"),("FG"),("FH"),("HJ"),("IJ"),("JK"),("KL")]:
    ADJ.setdefault(a, set()).add(b); ADJ.setdefault(b, set()).add(a)

etat = dict(zip("ABCDIJKL", [5,6,7,8,1,2,3,4]))
BUT  = dict(zip("ABCDIJKL", [1,2,3,4,5,6,7,8]))

COUPS = """6-G 2-B 1-E 3-H 4-I 3-L 6-K 4-G 1-I 2-J 5-H 4-A 7-F 8-E 4-D 8-C 7-A 8-G 5-C
2-B 1-E 8-I 1-G 2-J 7-H 1-A 7-G 2-B 6-E 3-H 8-L 3-I 7-K 3-G 6-I 2-J 5-H 3-C 5-G
2-B 6-E 5-I 6-J""".split()

def accessibles(depart, occupe):
    vu, pile = set(), [depart]
    while pile:
        x = pile.pop()
        for w in ADJ[x]:
            if w not in occupe and w not in vu: vu.add(w); pile.append(w)
    return vu

def rejoue(coups):
    """None si un coup est illegal, sinon la position finale"""
    e = dict(zip("ABCDIJKL", [5,6,7,8,1,2,3,4]))
    for c in coups:
        voiture, cible = c.split("-"); voiture = int(voiture)
        depart = [k for k, v in e.items() if v == voiture]
        if not depart: return None
        depart = depart[0]
        if cible not in accessibles(depart, set(e) - {depart}): return None
        del e[depart]; e[cible] = voiture
    return e

print("coups annonces :", len(COUPS))
fin = rejoue(COUPS)
print("les 43 coups sont tous legaux :", fin is not None)
print("conforme au but :", fin == BUT)

# temoins : une sequence fautive doit etre refusee
t1 = COUPS[:-1]                                  # le dernier coup oublie
t2 = COUPS[:2] + [COUPS[3], COUPS[2]] + COUPS[4:]   # deux coups intervertis
t3 = ["6-H"] + COUPS[1:]                         # legal, mais H bouche alors le passage du coup 2-B
for nom, t in (("dernier coup oublie", t1), ("coups 3 et 4 intervertis", t2), ("6-H au lieu de 6-G (bouche 2-B)", t3)):
    r = rejoue(t)
    print("  temoin %-32s : %s" % (nom, "coup illegal" if r is None else
          ("ACCEPTE" if r == BUT else "n'arrive pas au but")))
    assert r != BUT
assert fin == BUT

# recoupement independant du programme C : les premiers niveaux du parcours
# en largeur, recalcules ici sans rien lui emprunter
# (garage2.c donne 1, 8, 55, 250, 712 positions a distance 0 a 4)
niveau, vus = [frozenset(zip("ABCDIJKL", [5,6,7,8,1,2,3,4]))], set()
vus.add(niveau[0]); compte = [1]
for d in range(4):
    suivant = []
    for pos in niveau:
        e = dict(pos)
        for case, v in e.items():
            for cible in accessibles(case, set(e) - {case}):
                f = dict(e); del f[case]; f[cible] = v
                k = frozenset(f.items())
                if k not in vus: vus.add(k); suivant.append(k)
    niveau = suivant; compte.append(len(suivant))
print("positions a distance 0, 1, 2, 3, 4 :", compte, "(garage2.c : [1, 8, 55, 250, 712])")
assert compte == [1, 8, 55, 250, 712]
