# -*- coding: utf-8 -*-
"""n° 152 ANOTHER JOINER'S PROBLEM.
Un carre ACLF (cote s) et un demi-carre coupe en diagonale, le triangle CED
(grand cote CD = h), doivent donner un plateau carre. La regle de Dudeney :
reporter la moitie de CD de A en B, scier de B a F et de B a E ; les morceaux
G, H et M changent de place et l'on obtient le carre BEKF, en cinq morceaux. On l'essaie sur des
triangles de toutes tailles : les deux traits sont-ils egaux et perpendiculaires,
combien de morceaux, et un programme sait-il ranger les morceaux mobiles dans le
carre final sans en retourner aucun ?
Demande shapely (pip install shapely).
    python3 menuisier.py          (environ une seconde)"""
import math
from shapely.geometry import Polygon, LineString
from shapely import affinity
from shapely.ops import unary_union, split


def assembler(pieces, T, miroir=False, limite=200000, tous=True):
    """range les pièces dans la cible T ; rotations : une arête de la pièce parallèle à une arête de la cible ou d'une pièce posée"""
    Tb = T.buffer(1e-6); trouve = {}; n = [0]
    def dirs(polys):
        s = set()
        for p in polys:
            co = list(p.exterior.coords)
            for (x1, y1), (x2, y2) in zip(co, co[1:]): s.add(math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180)
        return s
    def poses(p, places):
        D = dirs([T] + [w for _, w in places]); anc = list(T.exterior.coords[:-1]) + [c for _, w in places for c in w.exterior.coords[:-1]]
        vus = set()
        for b in [p] + ([affinity.scale(p, -1, 1, origin=(0, 0))] if miroir else []):
            co = list(b.exterior.coords)
            rots = {round((dd + k - math.degrees(math.atan2(y2 - y1, x2 - x1))) % 360, 5): (dd + k - math.degrees(math.atan2(y2 - y1, x2 - x1))) % 360 for (x1, y1), (x2, y2) in zip(co, co[1:]) for dd in D for k in (0, 180)}
            for r in rots.values():
                q = affinity.rotate(b, r, origin=(0, 0))
                for vx, vy in q.exterior.coords[:-1]:
                    for ax, ay in anc:
                        w = affinity.translate(q, ax - vx, ay - vy)
                        cle = tuple(sorted((round(x, 4), round(y, 4)) for x, y in w.exterior.coords[:-1]))
                        if cle in vus: continue
                        vus.add(cle)
                        if Tb.contains(w): yield w
    def libre_bas_gauche(places):
        U = unary_union([w for _, w in places]) if places else None
        R = T if U is None else T.difference(U.buffer(1e-7))
        if R.is_empty or R.area < 1e-6: return None
        return min(((round(y, 5), round(x, 5), y, x) for g in (R.geoms if hasattr(R, "geoms") else [R]) if g.area > 1e-6 for x, y in g.exterior.coords))
    def dfs(places, restants):
        if n[0] > limite: return
        if not restants:
            cle = frozenset(tuple(sorted((round(x, 3), round(y, 3)) for x, y in w.exterior.coords[:-1])) for _, w in places); trouve[cle] = list(places); return
        coin = libre_bas_gauche(places); faits = set()
        for i, k in enumerate(restants):
            for w in poses(pieces[k], places):
                n[0] += 1
                # la pièce doit couvrir le coin libre le plus bas à gauche
                if coin and not any(abs(x - coin[3]) < 1e-5 and abs(y - coin[2]) < 1e-5 for x, y in w.exterior.coords): continue
                if all(w.intersection(z).area < 1e-7 for _, z in places):
                    cle = tuple(sorted((round(x, 4), round(y, 4)) for x, y in w.exterior.coords[:-1]))
                    if cle in faits: continue
                    faits.add(cle)
                    places.append((k, w)); dfs(places, restants[:i] + restants[i + 1:]); places.pop()
                    if trouve and not tous: return
    dfs([], list(range(len(pieces)))); return trouve, n[0]
def essai(s, h, bavard=False):
    A, C, L, F = (0, s), (s, s), (s, 0), (0, 0); D = (s, s - h); E = (s + h / 2, s - h / 2); B = (h / 2, s)
    car, tri = Polygon([A, C, L, F]), Polygon([C, E, D])
    K = (F[0] + E[0] - B[0], F[1] + E[1] - B[1]); cible = Polygon([B, E, K, F])
    coupes = [LineString([B, F]), LineString([B, E])]; mor = [car, tri]
    for c in coupes:
        c2 = affinity.scale(c, 1 + 1e-9, 1 + 1e-9)
        nv = []
        for m in mor:
            try: nv += [g for g in split(m, c2).geoms if g.area > 1e-12]
            except Exception: nv.append(m)
        mor = nv
    mor = [m.simplify(1e-9) for m in mor]
    fixes = [m for m in mor if cible.buffer(1e-7).contains(m)]; mobiles = [m for m in mor if not cible.buffer(1e-7).contains(m)]
    trou = cible.difference(unary_union(fixes).buffer(1e-9)) if fixes else cible
    res = None
    if trou.geom_type == "Polygon" and abs(trou.area - sum(m.area for m in mobiles)) < 1e-6:
        t, n = assembler(mobiles, trou.simplify(1e-6), miroir=False, tous=False); res = len(t)
    if bavard:
        print("  BF =", math.dist(B, F), "BE =", math.dist(B, E), "| perpendiculaires :", abs((F[0] - B[0]) * (E[0] - B[0]) + (F[1] - B[1]) * (E[1] - B[1])) < 1e-12, "| aire visée :", s * s + h * h / 4, "= BF² :", math.dist(B, F) ** 2)
        print("  morceaux :", len(mor), "aires", [round(m.area, 4) for m in mor], "| restent en place :", len(fixes), "| à déplacer :", len(mobiles))
    return len(mor), len(fixes), len(mobiles), res
r = essai(1, .48, True)
print("cas du dessin, s = 1, h = 0,48 : (morceaux, fixes, mobiles, assemblages trouves) =", r)
assert r == (5, 2, 3, 1)
res = {}
for h in (.1, .3, .48, .8, 1.0, 1.2, 1.5, 1.9, 2.0):
    res[h] = essai(1, h)
    print("  h/s =", h, "| aire triangle / aire carré =", round(h * h / 4, 4), "→ (morceaux, fixes, mobiles, assemblage sans retournement) :", res[h])
assert all(res[h] == (5, 2, 3, 1) for h in res if h < 2)
print("\nhuit triangles de taille croissante : cinq morceaux, deux fixes, trois ranges sans retournement ;")
print("a h = 2 (triangle de meme aire que le carre), la construction degenere en trois morceaux.")

# temoin : l'assembleur doit refuser des pieces qui ne remplissent pas la cible
T = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
bon = [Polygon([(0, 0), (1, 0), (1, .5), (0, .5)]), Polygon([(0, 0), (1, 0), (1, .5), (0, .5)])]
faux = [Polygon([(0, 0), (1, 0), (1, .6), (0, .6)]), Polygon([(0, 0), (1, 0), (1, .5), (0, .5)])]
print("temoin : deux demi-carres dans le carre ->", len(assembler(bon, T, tous=False)[0]),
      "assemblage ; un 0,6 et un 0,5 ->", len(assembler(faux, T, tous=False)[0]))
assert assembler(bon, T, tous=False)[0] and not assembler(faux, T, tous=False)[0]
