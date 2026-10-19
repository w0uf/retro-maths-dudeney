# -*- coding: utf-8 -*-
"""n° 134 THE BANKER'S PUZZLE — Dudeney, 1917.

Le banquier depose d'abord un certain nombre de pieces de six pence ; le
client en ajoute autant qu'il veut, sans depasser une livre (soit quarante
pieces) ; puis le banquier lui demande d'en transferer un nombre de son
choix.  Le banquier gagne si le total final n'est pas divisible, c'est-a-dire
s'il est PREMIER.

Sa recette : deposer 40, puis demander le carre du nombre immediatement
inferieur a ce que le client a ajoute.
"""
def premier(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0: return False
        d += 2
    return True

print("=== Sa recette, essayee sur tous les coups possibles du client ===")
DEPOT = 40
rate = []
for ajout in range(1, 41):                 # une livre = quarante pieces de six pence
    transfert = (ajout - 1)**2
    total = DEPOT + ajout + transfert
    if not premier(total): rate.append((ajout, total))
print("  depot %d ; le client ajoute de 1 a 40 pieces." % DEPOT)
print("  coups ou le total n'est PAS premier :", rate if rate else "aucun")
print("  le banquier gagne a coup sur :", not rate)
print("\n  quelques exemples :")
for ajout in (1, 6, 12, 40):
    t = DEPOT + ajout + (ajout-1)**2
    print("     le client ajoute %2d, transfere %4d -> total %4d, premier : %s"
          % (ajout, (ajout-1)**2, t, premier(t)))

print("\n=== Le polynome cache ===")
print("  en posant m = ajout - 1, le total vaut 40 + (m+1) + m^2 = m^2 + m + 41.")
print("  c'est le fameux polynome d'Euler.")
print("  premier pour m = 0 a 39 :", all(premier(m*m+m+41) for m in range(40)))
print("  et pour m = 40 :", 40*40+40+41, "=", 41*41, "-> premier :", premier(1681))
print("  la limite « pas plus d'une livre » est donc EXACTEMENT la borne du polynome.")

print("\n=== Le depot 40 est-il le seul qui marche ? ===")
print("  cherchons les q tels que n^2 + n + q soit premier pour n = 0 a q-2 :")
bons = []
for q in range(2, 200):
    if all(premier(n*n + n + q) for n in range(q-1)): bons.append(q)
print("   ", bons)
print("  ce sont les « nombres chanceux d'Euler » ; le plus grand est 41,")
print("  et l'on sait depuis Stark et Heegner (1952-1967) qu'il n'y en a pas d'autres.")
print("\n  avec un depot de q-1, le banquier couvre les ajouts de 1 a q-1 :")
for q in bons:
    print("     depot %2d : couvre jusqu'a %2d pieces ajoutees (soit %s)"
          % (q-1, q-1, "une livre" if q == 41 else "%d pence" % (6*(q-1))))
print("  seul le depot de 40 couvre la livre entiere. Aucun autre choix ne tient.")

print("\n=== Temoins ===")
def recette_tient(depot, max_ajout=40):
    return all(premier(depot + a + (a - 1)**2) for a in range(1, max_ajout + 1))
for depot in (40, 39, 41, 16):
    perdus = [a for a in range(1, 41) if not premier(depot + a + (a - 1)**2)]
    print("  depot %2d : %s" % (depot, "tient sur les 40 coups" if not perdus
          else "perd des le coup %d (%d coups perdus)" % (perdus[0], len(perdus))))
print("  et avec 41 pieces ajoutees, depot 40 :", 40 + 41 + 40**2, "->",
      "premier" if premier(40 + 41 + 40**2) else "compose")
print("  test de primalite : 1681, 1763, 91 refuses ; 41, 1601 acceptes :",
      not premier(1681) and not premier(1763) and not premier(91) and premier(41) and premier(1601))
assert recette_tient(40) and not recette_tient(39) and not recette_tient(41) and not recette_tient(40, 41)
assert not premier(1681) and not premier(91) and premier(1601) and bons == [2, 3, 5, 11, 17, 41]
