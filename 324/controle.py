"""n° 324 THE LION AND THE MAN : 28 trajets de l'homme (a1 → h8, aller-retour, 22 lignes), puis tous les couples."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(["gcc", "-O3", "-o", "tour", "tour.c"], check=True)
L = []
for X in (8, 1):
    for m, att in ((21, 0), (22, 14)):
        r = subprocess.run(["./tour", str(m), "0", "-1", "63", str(X)], capture_output=True, text=True, env=dict(os.environ, TOUS="1")).stdout
        R = [l for l in r.splitlines() if "coups :" in l]; print("a1 → h8, aller-retour vers", "a2" if X == 8 else "b1", ",", m, "lignes :", len(R)); assert len(R) == att
        if m == 22: L += R
open("homme.txt", "w").write("\n".join(L) + "\n")
subprocess.run([sys.executable, "lion.py"], check=True)
