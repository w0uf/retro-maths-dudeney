"""n° 344 THE KENNEL PUZZLE : rejeu de ses 46 coups, les 164 chaînes, puis la recherche exacte (IDA*, somme des
distances comme heuristique) pour sa chaîne jusqu'à 40 coups : aucune solution. Quelques secondes.
La recherche approchée glouton.py (A* pondéré) est à part : python3 glouton.py 3 (plusieurs minutes)."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "chenil.py"], check=True)
subprocess.run(["gcc", "-O3", "-o", "chenil", "chenil.c"], check=True)
SA_CHAINE = "1 12 19 8 5 14 17 6 3 10 13 16 7 4 15 18 11 2 9 20".split()   # chenil final des chiens 1 à 20
r = subprocess.run(["./chenil", "40"] + SA_CHAINE, capture_output=True, text=True)
print(r.stderr.strip()); print(r.stdout.strip()); assert "aucune <= 40" in r.stdout
# témoin : la même recherche trouve bien une solution quand elle existe (le chien 20 descend d'une niche : un coup)
r = subprocess.run(["./chenil", "6"] + [str(k) for k in range(1, 20)] + ["25"], capture_output=True, text=True)
print("témoin (chien 20 envoyé en niche 25) :", r.stdout.strip()); assert r.stdout.startswith("1 20-25")
