"""n° 328-332 : rejoue un tracé (points de virage) et compte les étoiles rayées.
Les traits suivent les lignes de la dame si DAME, sinon n'importe quelle droite ; une étoile est rayée si le trait passe dessus."""
from fractions import Fraction as F
def rayees(points, n, dame=True, hors=False):
    vus = set()
    for (a, b), (c, d) in zip(points, points[1:]):
        dx, dy = c - a, d - b
        if dame: assert dx == 0 or dy == 0 or abs(dx) == abs(dy), ("pas une ligne de dame", (a, b), (c, d))
        for x in range(n):
            for y in range(n):
                # (x,y) sur le segment ?
                if (x - a) * dy == (y - b) * dx and min(a, c) <= x <= max(a, c) and min(b, d) <= y <= max(b, d): vus.add((x, y))
    if not hors: assert all(0 <= x < n and 0 <= y < n for x, y in points), "virage hors du plateau"
    return vus
if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]); P = [tuple(map(int, t.split(","))) for t in sys.argv[2].split()]
    V = rayees(P, n, dame="oblique" not in sys.argv, hors="hors" in sys.argv)
    print("traits :", len(P) - 1, "| étoiles rayées :", len(V), "/", n * n, "| départ", P[0], "arrivée", P[-1])
