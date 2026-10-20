"""n° 342 THE MANDARIN'S PUZZLE : compile mandarin.c (IDA*, heuristique admissible : somme des distances de cavalier)
et compte.c (toutes les solutions d'une longueur donnée) ; rejoue sa suite de 30 coups. Quelques secondes."""
import subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for f in ("mandarin", "compte"): subprocess.run(["gcc", "-O2", "-o", f, f + ".c"], check=True)
run = lambda *a: subprocess.run(list(map(str, a)), capture_output=True, text=True).stdout
r = run("./mandarin", 1); print(r.strip().splitlines()[-2]); assert "limite 32 : TROUVÉ" in r and "limite 30 : rien" in r
r = run("./mandarin", 0); print(r.strip().splitlines()[-2]); assert "limite 30 : TROUVÉ" in r and "limite 28 : rien" in r
S = [l for l in run("./compte", 0, 30).splitlines() if l.startswith("sol")]; print("solutions en 30 :", len(S)); assert len(S) == 2
assert {l.split("bougés:")[1].split("|")[0].strip() for l in S} == {"6", "15"}
S = [l for l in run("./compte", 1, 32).splitlines() if l.startswith("sol")]; print("sans bouger les pions en place, en 32 :", len(S)); assert len(S) == 11
# rejeu indépendant de la suite du corrigé, sur la table relevée sur la gravure
X = [2,2,3,4,1,2,3,4,5,6,1,2,3,4,5,0,1,2,3,4,5,2,3,4,4]; Y = [0,1,1,1,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4,5,5,5,6]
D0 = [16,11,3,13,22,6,7,8,9,21,19,12,4,14,15,5,17,18,2,20,1,10,23,24,0]
def rejoue(suite):
    pos = list(D0)
    for p in suite:
        v, c = pos.index(0), pos.index(p)
        assert sorted((abs(X[v]-X[c]), abs(Y[v]-Y[c]))) == [1, 2], ("pas un saut de cavalier", p)
        pos[v], pos[c] = p, 0
    return pos == list(range(1, 25)) + [0]
DUD = [2, 6, 13, 4, 1, 21, 4, 1, 10, 2, 21, 10, 2, 5, 22, 16, 1, 13, 6, 19, 11, 2, 5, 22, 16, 5, 13, 4, 10, 21]
print("sa suite de", len(DUD), "coups range les jetons :", rejoue(DUD)); assert rejoue(DUD)
# témoins : les deux exemples de l'énoncé (premier coup par 1, 2 ou 10 seulement ; après 1 : 23, 4, 8 ou 21)
v = D0.index(0); prem = sorted(D0[c] for c in range(25) if sorted((abs(X[v]-X[c]), abs(Y[v]-Y[c]))) == [1, 2]); assert prem == [1, 2, 10]
D1 = list(D0); c = D1.index(1); D1[v], D1[c] = 1, 0; v = c
apres = sorted(D1[c] for c in range(25) if D1[c] != 1 and sorted((abs(X[v]-X[c]), abs(Y[v]-Y[c]))) == [1, 2]); assert apres == [4, 8, 21, 23]
print("relevé de la table conforme aux deux exemples de l'énoncé")
try: rejoue(DUD[:5] + DUD[6:]); sys.exit("témoin accepté : ERREUR")
except AssertionError as e: print("témoin (un coup retiré) refusé :", e.args[0][0])
