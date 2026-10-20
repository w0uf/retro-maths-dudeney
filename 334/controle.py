"""n° 334 ST. GEORGE AND THE DRAGON : chemins de cavalier de d4 (centre) à b2 (le dragon) sur 7 × 7.
python3 controle.py : trouve et contrôle un chemin (instantané). python3 controle.py compte : les compte tous
(163 578 772 ; une quarantaine de minutes)."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from cavalier import case, chemin
subprocess.run(["gcc", "-O3", "-o", "cavalier7", "cavalier7.c"], check=True)
p = subprocess.Popen(["./cavalier7", "24", "8"], stdout=subprocess.PIPE, text=True)
ligne = p.stdout.readline()
if "compte" not in sys.argv: p.kill()
T = [case(s) for s in ligne.split("premier :")[1].split()]
chemin(T, [(1, case("d4")), (49, case("b2"))]); print("un chemin du centre au dragon, contrôlé")
# témoin de parité : un dragon sur une case de l'autre couleur (b3) ne laisse aucun chemin ; on le vérifie vite par la couleur
coul = lambda c: (c[0] + c[1]) % 2
print("centre et dragon de même couleur :", coul(case("d4")) == coul(case("b2")), "| b3 :", coul(case("d4")) == coul(case("b3")))
assert coul(case("d4")) == coul(case("b2")) and coul(case("d4")) != coul(case("b3"))
T2 = T[:-1] + [case("b3")]
try: chemin(T2, [(49, case("b2"))]); sys.exit("témoin accepté : ERREUR")
except AssertionError as e: print("témoin (fin déplacée) refusé :", e.args[0])
if "compte" in sys.argv:
    reste = p.stdout.read(); n = int(reste.split("chemins :")[1]); print("chemins :", n); assert n == 163578772
