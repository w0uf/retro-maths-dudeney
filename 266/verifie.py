# -*- coding: utf-8 -*-
"""n° 266 — verification independante d'une grille de double mixte.
Hommes en majuscules, dames en minuscules ; a et A sont mari et femme.
    python3 verifie.py [tennis8.json]
Ne reprend aucun code des programmes de recherche."""
import sys, os, json, copy

def defauts(jours, n):
    """liste des manquements aux regles de Dudeney (vide si la grille est bonne)"""
    out, avec, contre = [], {}, {}
    for d, matchs in enumerate(jours, 1):
        if len(matchs) != n // 2: out.append("jour %d : %d matchs au lieu de %d" % (d, len(matchs), n // 2))
        presents = [x for m in matchs for eq in m for x in eq]
        if len(set(presents)) != 2 * n or len(presents) != 2 * n:
            out.append("jour %d : tout le monde ne joue pas une fois et une seule" % d)
        for (h1, f1), (h2, f2) in matchs:
            if not (h1.isupper() and h2.isupper() and f1.islower() and f2.islower()):
                out.append("jour %d : equipe qui n'est pas un homme et une dame" % d)
            for p in ((h1, f1), (h2, f2)):
                avec[frozenset(p)] = avec.get(frozenset(p), 0) + 1
            for p in ((h1, h2), (h1, f2), (f1, h2), (f1, f2)):
                contre[frozenset(p)] = contre.get(frozenset(p), 0) + 1
    for nom, t in (("avec", avec), ("contre", contre)):
        for p, k in t.items():
            x, y = sorted(p)
            if k > 1: out.append("%s et %s jouent %s l'un de l'autre %d fois" % (x, y, nom, k))
            if x.lower() == y.lower(): out.append("%s et %s, mari et femme, jouent %s l'un de l'autre" % (x, y, nom))
    return out, avec, contre

def bilan(nom, jours, n):
    d, avec, contre = defauts(jours, n)
    print("%s : %d couples, %d jours" % (nom, n, len(jours)))
    print("   partenariats distincts : %d sur %d hors conjoints" % (len(avec), n * (n - 1)))
    print("   oppositions distinctes : %d sur %d hors conjoints" % (len(contre), n * (2 * n - 1) - n))
    print("   defauts :", d or "aucun")
    return not d

# la grille de Dudeney, recopiee de sa solution
SIENNE = [[(("A", "d"), ("B", "e")), (("D", "a"), ("E", "b"))],
          [(("A", "e"), ("D", "b")), (("E", "a"), ("B", "d"))],
          [(("A", "b"), ("E", "d")), (("B", "a"), ("D", "e"))]]
ok4 = bilan("Grille de Dudeney", SIENNE, 4)

ici = os.path.dirname(os.path.abspath(__file__))
fichier = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ici, "tennis8.json")
G8 = [[tuple(tuple(e) for e in m) for m in j] for j in json.load(open(fichier))]
print()
ok8 = bilan("Grille a huit couples (%s)" % os.path.basename(fichier), G8, 8)

# temoins : deux grilles fautives, qui doivent etre refusees
print()
t1 = copy.deepcopy(G8)                                 # deux dames echangees entre deux courts du jour 1
(h1, f1), e1 = t1[0][0]; (h2, f2), e2 = t1[0][1]
t1[0][0] = ((h1, f2), e1); t1[0][1] = ((h2, f1), e2)
r1 = defauts(t1, 8)[0]
print("temoin 1 (deux dames echangees le jour 1) : %d defaut(s), par ex. %s -> %s"
      % (len(r1), r1[0] if r1 else "-", "refuse" if r1 else "ERREUR : accepte"))
t2 = copy.deepcopy(G8)                                 # le jour 7 remplace par le jour 1
t2[6] = t2[0]
r2 = defauts(t2, 8)[0]
print("temoin 2 (jour 1 rejoue le jour 7)         : %d defaut(s) -> %s"
      % (len(r2), "refuse" if r2 else "ERREUR : accepte"))
assert ok4 and ok8 and r1 and r2
