"""n° 328 THE QUEEN'S TOUR : les dix familles de cases ; un parcours de 14 coups depuis J (d5) ; des tours fermés de
14 coups depuis A, B, C, D, E, F et H, trouvés par une recherche au hasard guidée (dame_hasard.c, graine fixe).
Aucun tour n'a été trouvé depuis G, I ou J : ce n'est pas une preuve. python3 controle.py [long]  (long : H, quelques
minutes ; G, I, J : 100 millions d'essais chacun, une dizaine de minutes)"""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from etoiles import rayees
subprocess.run(["gcc", "-O3", "-o", "dame_hasard", "dame_hasard.c"], check=True)
# les dix familles : orbites des cases sous les huit symétries du carré
sym = lambda x, y: {(x, y), (7-x, y), (x, 7-y), (7-x, 7-y), (y, x), (7-y, x), (y, 7-x), (7-y, 7-x)}
familles = {frozenset(sym(x, y)) for x in range(8) for y in range(8)}
print("familles de cases :", len(familles)); assert len(familles) == 10
case = lambda s: ("abcdefgh".index(s[0]), int(s[1]) - 1)
def cherche(dep, essais, ferme=False, graine=1917):
    a = ["./dame_hasard", str(dep), "14", str(essais)] + (["ferme", str(graine)] if ferme else [])
    r = subprocess.run(a, capture_output=True, text=True).stdout
    if "coups :" not in r: return None
    return [case(s) for s in r.split("coups :")[1].split()]
def controle(T, ferme):
    V = rayees(T, 8, dame=True); assert len(T) - 1 == 14 and len(V) == 64 and (not ferme or T[0] == T[-1]); return True
T = cherche(35, 50_000_000); print("parcours depuis J (d5) :", T); controle(T, False)
LETTRES = {"A": 0, "B": 1, "C": 2, "D": 9, "E": 10, "F": 18, "G": 3, "H": 11, "I": 19, "J": 27}
for L in "ABCDEF":
    T = cherche(LETTRES[L], 3_000_000, ferme=True); controle(T, True); print("tour fermé depuis", L, ": trouvé")
if "long" in sys.argv:
    T = cherche(LETTRES["H"], 400_000_000, ferme=True, graine=1); controle(T, True); print("tour fermé depuis H : trouvé")
    for L in "GIJ": print("tour fermé depuis", L, ":", "trouvé" if cherche(LETTRES[L], 100_000_000, ferme=True) else "aucun en 100 millions d'essais")
# témoin : le parcours depuis J privé de son dernier coup ne couvre plus tout
T = cherche(35, 50_000_000)
print("témoin (dernier coup retiré) refusé :", len(rayees(T[:-1], 8)) < 64); assert len(rayees(T[:-1], 8)) < 64
