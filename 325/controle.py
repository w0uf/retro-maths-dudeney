"""n° 325 AN EPISCOPAL VISITATION : compile eveque.c ; aucune tournée en 16 coups, seize en 17 (huit depuis chaque
coin blanc, les unes à l'envers des autres) ; sans la règle des cases voisines, 16 coups suffisent. Quelques secondes."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(["gcc", "-O3", "-o", "eveque", "eveque.c"], check=True)
def lance(*a):
    r = subprocess.run(["./eveque"] + list(map(str, a)), capture_output=True, text=True, env=dict(os.environ, TOUS="1")).stdout.splitlines()
    return [l.split(":")[1].split() for l in r if "trajet en" in l], int(r[-1].split(":")[1])
case = lambda s: ("abcdefgh".index(s[0]), int(s[1]) - 1)
def tournee(T, regle=True):
    """contrôle indépendant : coups de fou, cases blanches couvertes, arêtes jamais reprises ; renvoie le nombre de coups"""
    vues = {T[0]}; aretes = set()
    for (a, b), (c, d) in zip(T, T[1:]):
        dx, dy = c - a, d - b; assert abs(dx) == abs(dy) > 0, "pas un coup de fou"
        sx, sy = dx // abs(dx), dy // abs(dy)
        for k in range(abs(dx)):
            p, q = (a + k * sx, b + k * sy), (a + (k + 1) * sx, b + (k + 1) * sy)
            e = frozenset((p, q)); assert not (regle and e in aretes), "deux fois entre les mêmes cases"; aretes.add(e); vues.add(q)
    assert vues == {(x, y) for x in range(8) for y in range(8) if (x + y) % 2 == 1}, "paroisses oubliées"
    return len(T) - 1
assert lance(16)[1] == 0; print("16 coups : aucune tournée")
R, n = lance(17); print("17 coups :", n, "tournées"); assert n == 16
T = [[case(s) for s in r] for r in R]
assert all(tournee(t) == 17 for t in T)
dep = {(t[0], t[-1]) for t in T}; print("départ et arrivée :", dep); assert dep == {((0, 7), (7, 0)), ((7, 0), (0, 7))}
A = [tuple(t) for t in T if t[0] == (0, 7)]; H = [tuple(t) for t in T if t[0] == (7, 0)]
assert set(H) == {t[::-1] for t in A}
ref = lambda p: (7 - p[1], 7 - p[0])
print("depuis a8, à reflet près :", len({min(t, tuple(map(ref, t))) for t in A}))
R, n = lance(16, "libre"); print("sans la règle, 16 coups :", n, "tournées"); assert n > 0
t = [case(s) for s in R[0]]; tournee(t, regle=False)
try: tournee(t); print("ERREUR : la tournée sans règle passe la règle"); sys.exit(1)
except AssertionError as e: print("témoin : cette tournée en 16 est refusée avec la règle (%s)" % e)
