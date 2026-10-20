"""n° 335 FARMER LAWRENCE'S CORNFIELDS : compile cavalier7.c et compte les chemins de cavalier avec les étapes
1 = a7, 13 = a1, 25 = d4, 37 = g7, 49 = g1 (rangée 1 en bas). Quelques minutes."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from cavalier import case, chemin
subprocess.run(["gcc", "-O3", "-o", "cavalier7", "cavalier7.c"], check=True)
r = subprocess.run(["./cavalier7", "42", "6", "13:0", "25:24", "37:48"], capture_output=True, text=True).stdout
T = [case(s) for s in r.split("premier :")[1].splitlines()[0].split()]
E = [(1, case("a7")), (13, case("a1")), (25, case("d4")), (37, case("g7")), (49, case("g1"))]
chemin(T, E); n = int(r.split("chemins :")[1]); print("premier chemin contrôlé ; chemins :", n); assert n == 54020
T2 = list(T); T2[20], T2[21] = T2[21], T2[20]
try: chemin(T2, E); print("témoin accepté : ERREUR"); sys.exit(1)
except AssertionError as e: print("témoin (deux parcelles échangées) refusé :", e.args[0][0])
