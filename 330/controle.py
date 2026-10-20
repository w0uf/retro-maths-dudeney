"""n° 330 : le tracé du corrigé, relevé sur la gravure (points de virage, colonne et rangée comptées depuis le coin
en bas à gauche, de 0 à 7), rejoué trait par trait. Instantané."""
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from etoiles import rayees
N = 8
TRACE = [tuple(map(int, t.split(","))) for t in "0,3 6,6 1,6 7,0 0,0 0,7 7,7 7,1 1,1 6,6 6,2 1,2 1,6 7,3 0,3".split()]
V = rayees(TRACE, N, dame=False, hors=False)
print("traits :", len(TRACE) - 1, "| étoiles :", len(V), "/", N * N, "| départ", TRACE[0], "arrivée", TRACE[-1])
assert len(TRACE) - 1 == 14 and len(V) == N * N
obliques = [(a, b) for a, b in zip(TRACE, TRACE[1:]) if not (a[0] == b[0] or a[1] == b[1] or abs(a[0]-b[0]) == abs(a[1]-b[1]))]
print("bords obliques :", obliques, "| fin du septième bord :", TRACE[7]); assert len(obliques) == 2
assert TRACE[0] == TRACE[-1] == (0, 3) and TRACE[7] == (7, 1)   # retour au mouillage, drapeau au 7e bord
# témoin : le même tracé sans son avant-dernier virage (deux traits fondus en un) doit échouer
T2 = TRACE[:-2] + TRACE[-1:]
try:
    ok = len(rayees(T2, N, dame=False, hors=False)) == N * N
except AssertionError: ok = False
print("témoin (un virage supprimé) refusé :", not ok); assert not ok
