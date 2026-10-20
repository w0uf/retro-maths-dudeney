"""n° 322 THE LANGUISHING MAIDEN : entrée a8, demoiselle g2 ; aller-retour vers a7 ou b8, puis chemin simple.
Minimum de lignes droites : aucun trajet en 21, 28 + 28 en 22. Environ une minute ; « parite » ajoute le témoin de parité (six minutes)."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "../321"); from trajet import case, controle
subprocess.run(["gcc", "-O3", "-o", "tour", "tour.c"], check=True)
def lance(*a):
    r = subprocess.run(["./tour"] + list(map(str, a)), capture_output=True, text=True, env=dict(os.environ, TOUS="1")).stdout
    return [l.split(":")[1].split() for l in r.splitlines() if "coups :" in l], r.splitlines()[-1]
A8, G2 = 56, 14
for X, nom in ((48, "a7"), (57, "b8")):
    for m, attendu in ((21, 0), (22, 28)):
        R, fin = lance(m, A8, -1, G2, X); print("aller-retour vers", nom, ":", fin); assert len(R) == attendu
        for r in R:   # contrôle indépendant : a8, X, a8, puis les 62 autres cases
            T = [case("a8")] + [case(s) for s in r]
            assert T[1] == case(nom) and T[2] == case("a8") and T[-1] == case("g2")
            reste = T[2:]; assert len(set(reste)) == 63 and case(nom) not in reste
            assert len(controle(T, toutes=False)) == m
# témoin de parité (python3 controle.py parite, six minutes) : sans aller-retour, aucun chemin simple de a8 à g2 ne passe partout
if "parite" in sys.argv:
  R, fin = lance(40, A8, -1, G2)
  print("sans aller-retour (40 lignes permises) :", fin)
  assert len(R) == 0
# témoin rapide : un trajet trouvé, amputé de sa dernière case, ne passe plus le contrôle

R, fin = lance(22, A8, -1, G2, 48)
T = [case("a8")] + [case(s) for s in R[0]][:-1]
print("témoin (trajet amputé de la demoiselle) refusé :", len(set(T[2:])) != 63)
assert len(set(T[2:])) != 63
