# -*- coding: utf-8 -*-
"""n° 385 — rejeu independant d'une partie, coup par coup, avec la seule regle de
l'enonce. Ne reprend aucun code de patience.py.
    python3 rejoue.py [partie_56.txt]"""
import os, sys

DEPART = [["9D", "8S", "7D", "6S", "5D", "4S", "3D", "2S", "1D"],
          ["9H", "8C", "7H", "6C", "5H", "4C", "3H", "2C", "1H"], [], [], [], []]
FIN = [["9D", "8C", "7D", "6C", "5D", "4C", "3D", "2C", "1D"],
       ["9H", "8S", "7H", "6S", "5H", "4S", "3H", "2S", "1H"]]

def rejoue(coups):
    """None si la partie est reguliere et finit bien, sinon la premiere faute"""
    places = [list(p) for p in DEPART]
    for n, m in enumerate(coups, 1):
        carte, cible = m.split(" sur ")
        src = [p for p in places if p and p[-1] == carte]
        if not src: return "coup %d (%s) : la carte n'est pas sur le dessus d'une pile" % (n, m)
        if cible == "place vide":
            dst = [p for p in places if not p]
            if not dst: return "coup %d (%s) : aucune place vide" % (n, m)
        else:
            dst = [p for p in places if p and p[-1] == cible]
            if not dst: return "coup %d (%s) : la cible n'est pas sur le dessus" % (n, m)
            if int(cible[0]) != int(carte[0]) + 1: return "coup %d (%s) : valeur pas immediatement superieure" % (n, m)
        dst[0].append(src[0].pop())
    if places[:2] != FIN or any(places[2:]): return "position finale fausse"
    return None

ici = os.path.dirname(os.path.abspath(__file__))
partie = open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ici, "partie_56.txt")).read().strip().split(" ; ")
r = rejoue(partie)
print("partie : %d coups ; %s" % (len(partie), r or "reguliere, et l'echange est fait"))
neufs = [m for m in partie if m[0] == "9"]
print("   un 9 a-t-il bouge ?", "oui" if neufs else "non")
assert r is None

print("\ntemoins (parties fautives, qui doivent etre refusees) :")
T = [("dernier coup retire", partie[:-1]),
     ("coups 1 et 5 intervertis", [partie[4]] + partie[1:4] + [partie[0]] + partie[5:]),
     ("coup 5 : 1H sur 1D au lieu de 1H sur 2S", partie[:4] + ["1H sur 1D"] + partie[5:]),
     ("un coup en trop vers une place vide, a la fin", partie + ["1H sur place vide"])]
for nom, p in T:
    f = rejoue(p)
    print("   %-45s -> %s" % (nom, f or "ERREUR : acceptee"))
    assert f
# controle positif : deux coups voisins qui ne touchent pas les memes cartes
# peuvent s'intervertir, et la partie reste juste
i = next(i for i in range(len(partie) - 1)
         if rejoue(partie[:i] + [partie[i + 1], partie[i]] + partie[i + 2:]) is None
         and partie[i] != partie[i + 1])
p = partie[:i] + [partie[i + 1], partie[i]] + partie[i + 2:]
print("   coups %d et %d intervertis (%s / %s) -> %s"
      % (i + 1, i + 2, partie[i], partie[i + 1], rejoue(p) or "acceptee, a juste titre"))
assert rejoue(p) is None
