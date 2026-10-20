"""n° 331 : le tracé du corrigé, relevé sur la gravure (points de virage, colonne et rangée comptées depuis le coin
en bas à gauche, de 0 à 7), rejoué trait par trait. Instantané."""
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from etoiles import rayees
N = 8
TRACE = [tuple(map(int, t.split(","))) for t in "8,7 0,7 0,0 8,0 1,7 1,1 7,1 7,6 2,6 2,2 6,2 6,5 3,5 3,2 8,7".split()]
V = rayees(TRACE, N, dame=True, hors=True)
print("traits :", len(TRACE) - 1, "| étoiles :", len(V), "/", N * N, "| départ", TRACE[0], "arrivée", TRACE[-1])
assert len(TRACE) - 1 == 14 and len(V) == N * N
hors = sorted(set(p for p in TRACE if not (0 <= p[0] < 8 and 0 <= p[1] < 8)))
print("virages hors du carré :", hors); assert hors == [(8, 0), (8, 7)] and TRACE[0] == TRACE[-1]
# témoin : le même tracé sans son avant-dernier virage (deux traits fondus en un) doit échouer
T2 = TRACE[:-2] + TRACE[-1:]
try:
    ok = len(rayees(T2, N, dame=True, hors=True)) == N * N
except AssertionError: ok = False
print("témoin (un virage supprimé) refusé :", not ok); assert not ok
