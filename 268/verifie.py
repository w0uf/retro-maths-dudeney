# -*- coding: utf-8 -*-
"""n° 268 — verification independante d'une sonnerie de cloches.
    python3 verifie.py [peal5.json]
Ne reprend aucun code des programmes de recherche. Une sonnerie est juste si :
  (a) chaque ordre des cloches est sonne une fois et une seule ;
  (b) d'une rangee a la suivante, aucune cloche ne bouge de plus d'une place,
      et au moins une bouge ;
  (c) aucune cloche ne sonne plus de deux fois de suite a la premiere place,
      ni a la derniere ;
  (d) la derniere rangee se raccorde a la premiere (la sonnerie boucle),
      et (b) et (c) valent aussi a travers ce raccord."""
import sys, os, json, math

def defauts(rangees):
    out = []
    n = len(rangees[0]); m = len(rangees)
    if m != math.factorial(n): out.append("%d rangees au lieu de %d" % (m, math.factorial(n)))
    if len(set(map(tuple, rangees))) != m: out.append("une rangee est sonnee deux fois")
    if any(sorted(r) != list(range(1, n + 1)) for r in rangees): out.append("rangee mal formee")
    for i in range(m):
        a, b = rangees[i], rangees[(i + 1) % m]
        if a == b: out.append("rangees %d et %d identiques" % (i, (i + 1) % m))
        for cloche in a:
            if abs(a.index(cloche) - b.index(cloche)) > 1:
                out.append("rangee %d -> %d : la cloche %d saute" % (i, (i + 1) % m, cloche)); break
    for place, nom in ((0, "premiere"), (n - 1, "derniere")):
        for i in range(m):
            if rangees[i][place] == rangees[(i + 1) % m][place] == rangees[(i + 2) % m][place]:
                out.append("cloche %d trois fois de suite a la %s place (rangee %d)"
                           % (rangees[i][place], nom, i)); break
    return out

ici = os.path.dirname(os.path.abspath(__file__))
fichier = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ici, "peal5.json")
P = [list(r) for r in json.load(open(fichier))]
d = defauts(P)
print("%s : %d cloches, %d rangees, defauts : %s"
      % (os.path.basename(fichier), len(P[0]), len(P), d or "aucun"))

# la sonnerie de quatre cloches imprimee par Dudeney
SIENNE = [[int(c) for c in r] for r in
          "1234 2143 2413 4231 4321 3412 3142 1324 3124 1342 1432 4123 "
          "4213 2431 2341 3214 2314 3241 3421 4312 4132 1423 1243 2134".split()]
print("sa sonnerie de quatre cloches : defauts :", defauts(SIENNE) or "aucun")

# temoins : des sonneries fautives doivent etre refusees
print()
t0 = [list(r) for r in P]; t0[10], t0[11] = t0[11], t0[10]          # 34251 et 34215 interverties :
#   ce n'est PAS une faute, cela donne une autre sonnerie juste (temoin positif)
t1 = [list(r) for r in P]; t1[1], t1[50] = t1[50], t1[1]            # deux rangees eloignees interverties
t2 = [list(r) for r in P]; t2[5] = list(t2[7])                      # une rangee repetee
t3 = [list(r) for r in P[1:]] + [list(P[0])]                        # meme cycle, decale : doit passer
t4 = [list(r) for r in SIENNE]; t4 = t4[:12] + t4[12:][::-1]        # moitie lue a l'envers
for nom, t, attendu in (("rangees 10 et 11 interverties", t0, True), ("rangees 1 et 50 interverties", t1, False), ("une rangee repetee", t2, False),
                        ("la meme, commencee ailleurs", t3, True), ("sa sonnerie, moitie a l'envers", t4, False)):
    dd = defauts(t)
    print("  temoin %-32s : %s" % (nom, "acceptee" if not dd else "refusee (%s)" % dd[0]))
    assert (not dd) == attendu
assert not d and not defauts(SIENNE)
# temoin de la regle (c) seule : la cloche 1 garde la premiere place trois fois
t5 = [[1, 2, 3, 4], [1, 2, 4, 3], [1, 4, 2, 3], [4, 1, 2, 3]]
r5 = [x for x in defauts(t5) if "trois fois" in x]
print("  temoin regle des deux coups (1 en tete trois fois) : %s" % (r5[0] if r5 else "NON DETECTE"))
assert r5
