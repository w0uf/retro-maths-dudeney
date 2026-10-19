# -*- coding: utf-8 -*-
"""n° 250 THE GRAND TOUR.

Un homme part de sa ville natale A, veut « entrer dans chaque ville une fois et
une seule » et finir chez son ami a Z. Dudeney montre par un argument de
coloriage que c'est impossible, puis trouve la faille : n'ayant jamais quitte A
de sa vie, il n'y est jamais « entre » — il peut donc y entrer une fois.

Sa figure 1 ramene la carte a une grille de quatre colonnes sur six rangees,
les chemins de fer reliant les villes voisines. A est un coin, Z le coin
diagonalement oppose.
"""
import sys
sys.setrecursionlimit(100000)

LIG, COL = 6, 4
V = [(r, c) for r in range(LIG) for c in range(COL)]
IDX = {p: i for i, p in enumerate(V)}
def voisins(p):
    r, c = p
    return [q for q in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)) if q in IDX]
ADJ = {p: voisins(p) for p in V}
A = (0, COL-1)          # coin superieur droit
Z = (LIG-1, 0)          # coin inferieur gauche

print("=== La carte, simplifiee ===")
print("  %d villes, %d liaisons" % (len(V), sum(len(a) for a in ADJ.values())//2))
def couleur(p): return (p[0] + p[1]) % 2
print("  A est %s, Z est %s" % ("noire" if couleur(A) else "blanche",
                                "noire" if couleur(Z) else "blanche"))
print("  villes noires : %d, blanches : %d"
      % (sum(1 for p in V if couleur(p)), sum(1 for p in V if not couleur(p))))
print()
print("  Un trajet qui passe une fois par chacune des %d villes alterne les" % len(V))
print("  couleurs : la premiere et la derniere sont donc de couleurs")
print("  DIFFERENTES. Or A et Z sont de la meme. L'itineraire demande est")
print("  impossible — c'est exactement son argument.")

# ═══ verification exhaustive de l'impossibilite ════════════════════════
def hamiltoniens(depart, arrivee):
    n = 0
    vus = {depart}
    def rec(p):
        nonlocal n
        if len(vus) == len(V):
            if p == arrivee: n += 1
            return
        for q in ADJ[p]:
            if q not in vus:
                vus.add(q); rec(q); vus.remove(q)
    rec(depart)
    return n
print()
print("=== Verification exhaustive ===")
print("  itineraires passant une fois par chaque ville, de A a Z : %d"
      % hamiltoniens(A, Z))

# ═══ la faille : une seule entree dans A ═══════════════════════════════
print()
print("=== Avec sa faille : il peut ENTRER une fois dans A ===")
solutions = []
def cherche():
    vus = {A}
    chemin = [A]
    retour = [None]      # a quel rang il revient en A
    def rec(p, rentre):
        if len(vus) == len(V) and rentre and p == Z:
            solutions.append((retour[0], list(chemin))); return
        for q in ADJ[p]:
            if q == A:
                if rentre or len(chemin) < 2: continue
                retour[0] = len(chemin) - 1     # villes visitees avant le retour
                chemin.append(A); rec(A, True); chemin.pop(); retour[0] = None
            elif q not in vus:
                vus.add(q); chemin.append(q); rec(q, rentre)
                chemin.pop(); vus.remove(q)
    rec(A, False)
cherche()
print("  itineraires valables : %d" % len(solutions))
from collections import Counter
c = Counter(k for k, _ in solutions)
print("  nombre de villes visitees AVANT le retour en A :")
for k in sorted(c):
    print("     %2d ville(s) : %5d itineraire(s)" % (k, c[k]))
print()
print("  Dudeney : « nous avons ainsi prouve que le casse-tete ne peut etre")
print("  resolu que par un retour en A immediatement apres l'avoir quitte ».")
print("  Est-ce vrai ? %s" % ("OUI" if list(c) == [1] else
      "NON — il existe des itineraires ou il revient plus tard"))

# ═══ la parite suffit-elle a le prouver ? ══════════════════════════════
print()
print("=== Son argument prouve-t-il vraiment cette necessite ? ===")
print("  Le coloriage autorise un retour apres 1, 3, 5... villes : un circuit")
print("  A -> t1 -> t2 -> t3 -> A a quatre liaisons, longueur paire, donc")
print("  parfaitement licite dans un graphe biparti ; et les 20 villes")
print("  restantes laissent la parite d'arrivee correcte.")
# existe-t-il seulement de tels circuits ?
def circuits(k):
    n = 0; vus = {A}
    def rec(p, reste):
        nonlocal n
        if reste == 0:
            if A in ADJ[p]: n += 1
            return
        for q in ADJ[p]:
            if q not in vus and q != A:
                vus.add(q); rec(q, reste-1); vus.remove(q)
    rec(A, k)
    return n
for k in (1, 3, 5):
    print("  circuits A -> %d ville(s) -> A : %d" % (k, circuits(k)))
print("  Le coloriage ne les interdit donc pas. Et pourtant aucun itineraire")
print("  complet n'en emploie : sa CONCLUSION est juste, mais son ARGUMENT ne")
print("  la demontre pas — il faut examiner tous les cas pour s'en assurer.")

# ═══ temoins : le compteur doit trouver des itineraires quand ils existent ═
print()
print("=== Temoins ===")
Z2 = (LIG-1, COL-1)               # coin de l'autre couleur que A
n2 = hamiltoniens(A, Z2)
print("  de A au coin %s (couleur opposee) : %d itineraire(s) -> le compteur n'est pas aveugle" % (Z2, n2))
assert n2 > 0 and hamiltoniens(A, Z) == 0 and len(solutions) == 43
