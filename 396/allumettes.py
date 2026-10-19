# -*- coding: utf-8 -*-
"""n° 396 A MATCH MYSTERY — Dudeney, Amusements in Mathematics (1917).

Trente allumettes en trois tas inegaux ; on prend a son tour autant
d'allumettes qu'on veut dans un seul tas ; QUI PREND LA DERNIERE PERD.
C'est le Nim, en version « misere ».

Dudeney donne treize repartitions gagnantes pour celui qui forme les tas
(et joue donc en second), puis la theorie complete : ecrire chaque tas en
puissances de deux et s'arranger pour que chaque puissance apparaisse un
nombre pair de fois.
"""
from functools import lru_cache
from itertools import combinations

SIENNES = [(15,14,1),(15,13,2),(15,12,3),(15,11,4),(15,10,5),(15,9,6),(15,8,7),
           (14,13,3),(14,11,5),(14,9,7),(13,11,6),(13,10,7),(12,11,7)]

# --- 1. le jeu, calcule sans aucune theorie ----------------------------
@lru_cache(None)
def perdante(tas):
    """position perdante pour celui qui doit jouer (regle : qui prend la derniere perd)"""
    tas = tuple(sorted(t for t in tas if t))
    if not tas: return False          # l'adversaire vient de prendre la derniere : il a perdu
    for i, t in enumerate(tas):
        for k in range(1, t+1):
            suiv = list(tas); suiv[i] = t - k
            if perdante(tuple(sorted(x for x in suiv if x))): return False
    return True

trouvees = sorted((a,b,c) for a,b,c in combinations(range(1,29), 3)
                  if a+b+c == 30 and perdante((a,b,c)))
print("repartitions de 30 en trois tas ou celui qui vient de jouer gagne :")
print("  nombre trouve :", len(trouvees), " | Dudeney en donne", len(SIENNES),
      "->", len(trouvees) == len(SIENNES))
print("  identiques a la liste du livre :",
      sorted(tuple(sorted(t, reverse=True)) for t in trouvees)
      == sorted(tuple(sorted(t, reverse=True)) for t in SIENNES))
for t in sorted(trouvees, reverse=True): print("   ", t)

# --- 2. sa theorie : le OU exclusif ------------------------------------
print("\n=== Sa regle des puissances de deux ===")
print("  « un nombre pair de chaque puissance » = ou exclusif nul.")
ecarts = [t for t in combinations(range(1,29), 3) if sum(t) == 30
          and (t[0]^t[1]^t[2] == 0) != perdante(t)]
print("  desaccords entre sa regle et le calcul direct, sur les 30 :", len(ecarts))
mauvais = [(a,b,c) for a in range(1,16) for b in range(1,16) for c in range(1,16)
           if ((a^b^c) == 0) != perdante((a,b,c))]
print("  desaccords sur TOUS les triplets de tas jusqu'a 15 :", len(mauvais))
if mauvais: print("   exemples :", mauvais[:6])

# --- 3. ce qu'il ne dit pas -------------------------------------------
print("\n=== Le mot « inegaux » est superflu ===")
print("  si deux tas sont egaux, le ou exclusif ne peut s'annuler qu'avec un")
print("  troisieme tas vide : trois tas non vides gagnants sont donc toujours")
print("  deux a deux differents.  Verifie :",
      all(len(set(t)) == 3 for t in trouvees))

print("\n=== Combien de repartitions gagnantes selon le total ? ===")
def gagnantes(n):
    return [(a,b,c) for a,b,c in combinations(range(1, n-1), 3)
            if a+b+c == n and (a^b^c) == 0]
for n in range(6, 41, 2):
    g = gagnantes(n)
    print("   %2d allumettes : %2d repartitions" % (n, len(g)), "  <-- celui du livre" if n == 30 else "")
print("\n   totaux impairs :", [(n, len(gagnantes(n))) for n in range(7, 32, 2)])

# --- l'exception de la regle, precisement ------------------------------
print("\n=== Ou exactement sa regle generale se trompe-t-elle ? ===")
from itertools import combinations_with_replacement
faux = []
for k in range(1, 6):
    for t in combinations_with_replacement(range(1, 7), k):
        if ((0 if not t else __import__("functools").reduce(lambda a,b: a^b, t)) == 0) != perdante(t):
            faux.append(t)
print("  positions (jusqu'a 5 tas de 6 allumettes) ou sa regle se trompe :", len(faux))
for t in faux: print("   ", t)
print("  -> ce sont exactement les positions ou chaque tas ne contient qu'une allumette.")
print("  il signale « 1, 1 » dans son dialogue, mais ne reporte pas l'exception")
print("  dans l'enonce de sa regle generale.")

# --- pourquoi trente ? -------------------------------------------------
print("\n=== Pourquoi trente allumettes ? ===")
rec, best = [], 0
for n in range(4, 65, 2):
    g = len(gagnantes(n))
    if g > best: best, marque = g, "  <-- record"
    else: marque = ""
    rec.append((n, g))
    if g >= 4 or n in (30, 62): print("   %2d : %3d repartitions%s" % (n, g, marque))
print("\n  la somme doit etre paire (le ou exclusif et la somme ont meme parite) :",
      all(g == 0 for n, g in [(n, len(gagnantes(n))) for n in range(5, 34, 2)]))
print("  maximum jusqu'a 62 :", max(rec, key=lambda x: x[1]))

# --- la partie d'exemple du livre --------------------------------------
print("\n=== La partie donnee en exemple dans l'enonce ===")
PARTIE = [(14,11,5),(8,11,5),(8,11,3),(8,5,3),(6,5,3),(4,5,3),(4,5,1),
          (4,3,1),(2,3,1),(2,1,1),(1,1,1)]
from functools import reduce
for i, p in enumerate(PARTIE):
    qui = "Stubbs" if i % 2 == 0 else "Wilson"
    x = reduce(lambda a,b: a^b, p)
    print("   %-7s laisse %-10s ou exclusif %d   position perdante pour l'autre : %s"
          % (qui, str(p), x, perdante(p)))
print("\n  toutes les positions laissees par Stubbs sont perdantes pour Wilson :",
      all(perdante(PARTIE[i]) for i in range(0, len(PARTIE), 2)))
print("  mais la derniere, 1-1-1, a un ou exclusif NON NUL :",
      reduce(lambda a,b: a^b, (1,1,1)))
print("  c'est le seul coup de sa partie que sa propre regle deconseille,")
print("  et c'est le coup gagnant. Il le joue.")

# --- temoins ------------------------------------------------------------
print("\n=== Temoins ===")
print("  (16, 13, 1) n'est pas gagnante :", not perdante((16, 13, 1)), "| ou exclusif :", 16 ^ 13 ^ 1)
print("  (1, 1) : perdante pour qui joue ?", perdante((1, 1)), "(il prend une, l'autre prend la derniere)")
print("  (1,) : perdante pour qui joue ?", perdante((1,)), "(il doit prendre la derniere)")
assert not perdante((16, 13, 1)) and not perdante((1, 1)) and perdante((1,))
assert len(trouvees) == 13 and not ecarts
assert faux == [(1,), (1, 1), (1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1, 1)]
assert [len(gagnantes(n)) for n in (6, 14, 30, 62)] == [1, 4, 13, 40]
