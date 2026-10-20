"""n° 321 THE ROOK'S JOURNEY : compile tour.c, cherche tous les trajets (départ h8, 10e coup en d1, 21e en b1),
puis contrôle le trajet trouvé indépendamment. python3 controle.py   (le décompte sans la case 10 prend une minute environ)"""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from trajet import case, controle
subprocess.run(["gcc", "-O3", "-o", "tour", "tour.c"], check=True)
def lance(*a):
    r = subprocess.run(["./tour"] + list(map(str, a)), capture_output=True, text=True, env=dict(os.environ, TOUS="1")).stdout
    routes = [l.split(":")[1].split() for l in r.splitlines() if "coups :" in l]
    return routes, r.splitlines()[-1]
R, fin = lance(21, 63, 3, 1); print("avec la case 10 :", fin)
assert len(R) == 1
T = [case(s) for s in R[0]]; F = controle(T)
print("trajet :", " ".join(R[0][::1][:1]), "→", " ".join("%s%d" % ("abcdefgh"[x], y + 1) for x, y in F))
assert len(F) == 21 and F[9] == case("d1") and F[20] == case("b1") and T[0] == case("h8")
# témoin : le même trajet avec deux cases échangées doit être refusé
T2 = list(T); T2[30], T2[31] = T2[31], T2[30]
try: controle(T2); print("témoin accepté : ERREUR"); sys.exit(1)
except AssertionError as e: print("témoin refusé :", e.args[0][0])
if "rapide" not in sys.argv:
    R2, fin2 = lance(21, 63, -1, 1); print("sans la case 10 :", fin2); assert len(R2) == 14
