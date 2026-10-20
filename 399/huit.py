"""Rétro Math's — n° 399 THE TROUBLESOME EIGHT (Dudeney, 1917).
Un carré magique de somme 15, le 8 au milieu de la rangée du haut, neuf nombres différents. Tout le carré s'écrit
avec un paramètre a (le coin en haut à gauche) ; on contrôle la famille par force brute, puis chaque lecture de
« nombre » : entiers positifs, avec zéro, relatifs, fractions.
    python3 huit.py   (instantané)"""
from fractions import Fraction as F
from itertools import permutations

def carre(a):
    return [a, 8, 7 - a, 12 - 2 * a, 5, 2 * a - 2, 3 + a, 2, 10 - a]

def magique(c, s=15):
    L = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return all(sum(c[i] for i in l) == s for l in L)

# 1. la famille à un paramètre est bien magique, et c'est la seule :
#    force brute sur les entiers de -20 à 40 avec 8 en haut au milieu
assert all(magique(carre(F(n, 7))) for n in range(-50, 100))
brut = set()
for a in range(-20, 41):
    for e in range(-20, 41):
        c = 15 - 8 - a
        h = 15 - 8 - e
        for d in range(-20, 41):
            g = 15 - a - d; f = 15 - d - e; i = 15 - g - h
            k = [a, 8, c, d, e, f, g, h, i]
            if magique(k): brut.add(tuple(k))
assert all(k[4] == 5 and k == tuple(carre(k[0])) for k in brut), "famille incomplète"
print("carrés magiques (répétitions admises) trouvés par force brute :", len(brut), "- tous de la famille")

# 2. chiffres 1 à 9
lo = [p for p in permutations(range(1, 10)) if magique(p)]
print("carrés 1-9 :", len(lo), "| 8 en coin dans tous :", all(p.index(8) in (0,2,6,8) for p in lo))

# 3. valeurs de a qui donnent un doublon
interdits = set()
for n in range(-400, 800):
    a = F(n, 12)
    if len(set(carre(a))) < 9: interdits.add(a)
print("a interdits :", sorted(interdits))

ok = lambda a: len(set(carre(a))) == 9
print("entiers > 0 :", [a for a in range(-50, 60) if ok(a) and min(carre(a)) > 0])
print("entiers >= 0 :", [(a, carre(a)) for a in range(-50, 60) if ok(a) and min(carre(a)) >= 0])
print("entiers relatifs, quelques a :", [a for a in range(-5, 12) if ok(a)])
print("a=0 :", carre(0))
dem = [F(n, 2) for n in range(-20, 40) if n % 2]
print("demis > 0 :", [(str(a), [str(x) for x in carre(a)]) for a in dem if ok(a) and min(carre(a)) > 0])
print("Dudeney a=9/2 :", [str(x) for x in carre(F(9, 2))], ok(F(9,2)))
print("positifs ssi 1<a<6 :", all((min(carre(F(n,12)))>0) == (1 < F(n,12) < 6) for n in range(-100,200)))

# --- ce que dit le commentaire
assert carre(F(9, 2)) == [F(9, 2), 8, F(5, 2), 3, 5, 7, F(15, 2), 2, F(11, 2)] and ok(F(9, 2)) and magique(carre(F(9, 2)))
assert len(lo) == 8 and all(p.index(8) in (0, 2, 6, 8) for p in lo)
assert [a for a in range(-50, 60) if ok(a) and min(carre(a)) > 0] == []                  # entiers positifs : impossible
assert [a for a in range(-50, 60) if ok(a) and min(carre(a)) >= 0] == [1, 6]              # avec zéro : a = 1 et son miroir
assert carre(1) == [1, 8, 6, 10, 5, 0, 4, 2, 9] and carre(0) == [0, 8, 7, 12, 5, -2, 3, 2, 10]
assert sorted(interdits) == [-1, 2, 3, F(7, 2), 4, 5, 8]
assert [a for a in dem if ok(a) and min(carre(a)) > 0] == [F(3, 2), F(5, 2), F(9, 2), F(11, 2)]   # deux carrés, à un miroir près
# témoin : a = 4 donne un doublon (le 4 deux fois) et doit être refusé
assert not ok(4)
print("contrôles : tout est conforme (témoins refusés)")
