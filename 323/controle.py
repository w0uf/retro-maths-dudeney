"""n° 323 A DUNGEON PUZZLE : compile cachot.c ; depuis la cellule du prisonnier (e1), aucun chemin à 58 lignes,
dix à 57 ; depuis les dix cases représentatives de l'échiquier, jamais plus de 57. Environ une minute."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "../321"); from trajet import case, controle
subprocess.run(["gcc", "-O3", "-o", "cachot", "cachot.c"], check=True)
def lance(dep, k):
    r = subprocess.run(["./cachot", str(dep), str(k)], capture_output=True, text=True).stdout.splitlines()
    return [l.split(":")[1].split() for l in r if "lignes :" in l], int(r[-1].split(":")[1].split()[0])
R, n = lance(4, 5); print("e1, 58 lignes ou plus :", n); assert n == 0
R, n = lance(4, 6); print("e1, 57 lignes :", n); assert n == 10
for r in R:      # contrôle indépendant des deux premiers chemins affichés
    F = controle([case(s) for s in r]); assert len(F) == 57 and case(r[0]) == case("e1")
nom = lambda s: "abcdefgh"[s % 8] + str(s // 8 + 1)
record = {}
for s in (0, 1, 2, 3, 9, 10, 11, 18, 19, 27):
    assert lance(s, 5)[1] == 0
    record[nom(s)] = lance(s, 6)[1] > 0
print("57 lignes atteintes depuis :", record)
assert [k for k, v in record.items() if not v] == ["b2", "c2", "d2", "d4"]
# témoin : un chemin à 57 lignes dont on fusionne deux pas en ligne droite n'en a plus que 56
T = [case(s) for s in R[0]]; print("témoin : lignes comptées sur un chemin à 57 :", len(controle(T)))
T2 = T[:1] + T[2:]
try: controle(T2); print("témoin accepté : ERREUR"); sys.exit(1)
except AssertionError: print("témoin (une cellule sautée) refusé")
