"""n° 332 : le tracé du corrigé, relevé sur la gravure (points de virage, colonne et rangée comptées depuis le coin
en bas à gauche, de 0 à 6), rejoué trait par trait. Instantané."""
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from etoiles import rayees
N = 7
TRACE = [tuple(map(int, t.split(","))) for t in "0,6 5,1 0,1 5,6 5,2 1,6 4,6 0,2 0,5 5,0 0,0 6,6 6,0".split()]
V = rayees(TRACE, N, dame=True, hors=False)
print("traits :", len(TRACE) - 1, "| étoiles :", len(V), "/", N * N, "| départ", TRACE[0], "arrivée", TRACE[-1])
assert len(TRACE) - 1 == 12 and len(V) == N * N
assert TRACE[0] == (0, 6) and TRACE[-1] == (6, 0)   # les deux étoiles noires
# témoin : le même tracé sans son avant-dernier virage (deux traits fondus en un) doit échouer
T2 = TRACE[:-2] + TRACE[-1:]
try:
    ok = len(rayees(T2, N, dame=True, hors=False)) == N * N
except AssertionError: ok = False
print("témoin (un virage supprimé) refusé :", not ok); assert not ok
