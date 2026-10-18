#!/usr/bin/env python3
"""n° 269 THREE MEN IN A BOAT.

Quinze hommes, sept jours, cinq canots de trois chaque jour. Deux hommes ne
sortent jamais deux fois ensemble ; un homme ne monte jamais deux fois dans le
meme canot ; et il faut employer LE MOINS DE CANOTS POSSIBLE.
Dudeney : « il ne nous en faut que dix ». Verifions.
"""
import random
from itertools import combinations

L = "ABCDEFGHIJKLMNO"
IDX = {c: i for i, c in enumerate(L)}

# Son tableau. ATTENTION : le texte imprime « (DBF) » au premier jour, ou B
# apparait deux fois et E nulle part : c'est (DEF), comme le dit son enonce.
SIEN = [
    (["ABC","DEF","GHI","JKL","MNO"], [1,2,3,4,5]),
    (["ADG","BKN","COL","JEI","MHF"], [8,6,7,9,10]),
    (["AJM","BEH","CFI","DKO","GNL"], [3,5,4,1,2]),
    (["AEK","CGM","BOI","DHL","JNF"], [7,6,8,9,1]),
    (["AHN","CDJ","BFL","GEO","MKI"], [4,5,3,10,2]),
    (["AFO","BGJ","CKH","DNI","MEL"], [6,7,8,10,1]),
    (["AIL","BDM","CEN","GKF","JHO"], [5,4,3,9,2]),
]

print("=== Son tableau est-il un arrangement valable ? ===")
triplets, canots = [], []
for jour, (ts, bs) in enumerate(SIEN):
    for t, b in zip(ts, bs):
        triplets.append((jour, tuple(sorted(IDX[c] for c in t))))
        canots.append(b)
# chaque homme sort une fois par jour
ok_jour = all(sorted(sum((list(t) for j, t in triplets if j == d), [])) ==
              list(range(15)) for d in range(7))
print("  chaque homme sort une fois et une seule chaque jour :", ok_jour)
# chaque paire exactement une fois
vues = {}
for j, t in triplets:
    for p in combinations(t, 2): vues[p] = vues.get(p, 0) + 1
print("  paires couvertes : %d sur %d ; toutes une seule fois : %s"
      % (len(vues), 105, all(v == 1 for v in vues.values())))
# les canots
parjour = {}
parhomme = {}
for (j, t), b in zip(triplets, canots):
    parjour.setdefault(j, []).append(b)
    for h in t: parhomme.setdefault(h, []).append(b)
print("  deux canots differents le meme jour :",
      all(len(set(v)) == 5 for v in parjour.values()))
print("  aucun homme deux fois dans le meme canot :",
      all(len(set(v)) == 7 for v in parhomme.values()))
print("  nombre de canots employes : %d" % len(set(canots)))

# ═══ dix est-il le minimum ? ═══════════════════════════════════════════
def conflits(trips):
    n = len(trips)
    adj = [set() for _ in range(n)]
    for a in range(n):
        for b in range(a+1, n):
            ja, ta = trips[a]; jb, tb = trips[b]
            if ja == jb or set(ta) & set(tb):
                adj[a].add(b); adj[b].add(a)
    return adj

def chromatique(adj, kmax=12):
    n = len(adj)
    ordre = sorted(range(n), key=lambda v: -len(adj[v]))
    for k in range(1, kmax+1):
        coul = [-1]*n
        def rec(i):
            if i == n: return True
            v = ordre[i]
            interdits = {coul[w] for w in adj[v] if coul[w] >= 0}
            plafond = min(k, max([coul[ordre[j]] for j in range(i)] + [-1]) + 2)
            for c in range(plafond):
                if c in interdits: continue
                coul[v] = c
                if rec(i+1): return True
                coul[v] = -1
            return False
        if rec(0): return k
    return None

adj = conflits(triplets)
print()
print("=== Le nombre minimal de canots pour SON arrangement ===")
print("  un homme sort sept fois, dans sept canots differents : au moins 7.")
print("  nombre chromatique du graphe des conflits : %d" % chromatique(adj))

# ═══ et pour d'autres arrangements ? ═══════════════════════════════════
def toutes_journees(used, rng, cap=None):
    """toutes les partitions en 5 triplets n'employant que des paires libres"""
    res = []
    def rec(rest, cour):
        if cap and len(res) >= cap: return
        if not rest:
            res.append(tuple(cour)); return
        a = rest[0]; autres = rest[1:]
        for i in range(len(autres)):
            b = autres[i]
            if (a, b) in used: continue
            for k in range(i+1, len(autres)):
                c = autres[k]
                if (a, c) in used or (b, c) in used: continue
                rec([x for x in autres if x not in (b, c)], cour + [(a, b, c)])
    rec(list(range(15)), [])
    rng.shuffle(res)
    return res

def systeme(rng):
    """un systeme de Kirkman tire au hasard, par retour arriere randomise"""
    def rec(jour, used, jours):
        if jour == 7: return jours
        for c in toutes_journees(used, rng):
            nv = set(used)
            for t in c: nv |= set(combinations(t, 2))
            r = rec(jour+1, nv, jours + [c])
            if r: return r
        return None
    return rec(0, set(), [])

print()
print("=== Et d'autres arrangements feraient-ils mieux ? ===")
rng = random.Random(1917)
vus, mini, essais = set(), 99, 0
for _ in range(120):
    s = systeme(rng)
    if s is None: continue
    essais += 1
    trips = [(d, t) for d, j in enumerate(s) for t in j]
    k = chromatique(conflits(trips))
    vus.add(k); mini = min(mini, k)
print("  %d arrangements tires au hasard" % essais)
print("  nombres de canots necessaires rencontres : %s" % sorted(vus))
print("  minimum rencontre : %d" % mini)

# ═══ son chiffre d'echauffement ════════════════════════════════════════
import math
print()
print("=== « le nombre est 455 puissance 7 » ===")
print("  C(15,3) = %d  : le nombre de BORDEES possibles" % math.comb(15, 3))
jour = math.factorial(15) // (math.factorial(3)**5 * math.factorial(5))
print("  15!/(3!^5 5!) = %d : le nombre de facons de repartir les quinze"
      % jour)
print("     hommes en cinq canots de trois un jour donne")
print("  sur sept jours sans aucune condition : %d^7 = %.3e" % (jour, jour**7.0))
print("  son chiffre : 455^7 = %.3e" % (455.0**7))
print("  -> 455 est le nombre de bordees, pas celui des repartitions :")
print("     son compte vaudrait si UN SEUL canot sortait chaque jour.")
