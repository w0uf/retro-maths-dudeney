# -*- coding: utf-8 -*-
"""n° 365 NEW MEASURING PUZZLE.

Deux recipients de dix pintes PLEINS de vin, une mesure de cinq pintes et une de
quatre, vides. Mettre exactement trois pintes dans chacune des deux mesures.
« Comment faire ? Et combien de manipulations (transvasements d'un recipient a
un autre) vous faut-il ? » Dudeney donne un tableau de onze transvasements.
Est-ce le minimum ?
"""
from collections import deque

CAP = (10, 10, 5, 4)
DEPART = (10, 10, 0, 0)
def but(e): return e[2] == 3 and e[3] == 3

def suivants(e):
    for i in range(4):
        if e[i] == 0: continue
        for j in range(4):
            if i == j or e[j] == CAP[j]: continue
            q = min(e[i], CAP[j] - e[j])
            f = list(e); f[i] -= q; f[j] += q
            yield tuple(f)

# ═══ 1. le graphe des etats ═════════════════════════════════════════════
vus = {DEPART: None}
file = deque([DEPART])
while file:
    e = file.popleft()
    for f in suivants(e):
        if f not in vus:
            vus[f] = e; file.append(f)
print("=== Le graphe des situations ===")
print("  situations atteignables depuis le depart : %d" % len(vus))
print("  (le vin total ne change pas : 20 pintes, reparties en quatre nombres)")

# ═══ 2. le plus court chemin ═══════════════════════════════════════════
dist = {DEPART: 0}
file = deque([DEPART]); fin = None
while file:
    e = file.popleft()
    if but(e): fin = e; break
    for f in suivants(e):
        if f not in dist:
            dist[f] = dist[e] + 1; file.append(f)
print()
print("=== Combien de transvasements au minimum ? ===")
buts = [e for e in vus if but(e)]
print("  situations qui repondent a la question : %d  ->  %s" % (len(buts), buts))
mini = min(dist[e] for e in buts if e in dist)
print("  nombre minimal de transvasements : %d" % mini)
print("  Dudeney en annonce onze.")

# ═══ 3. combien de solutions minimales ? ═══════════════════════════════
def compte(n):
    """nombre de chemins de longueur exactement n du depart vers un but"""
    niveau = {DEPART: 1}
    for _ in range(n):
        suiv = {}
        for e, k in niveau.items():
            for f in suivants(e):
                suiv[f] = suiv.get(f, 0) + k
        niveau = suiv
    return sum(k for e, k in niveau.items() if but(e))
print("  chemins de longueur %d qui aboutissent : %d" % (mini, compte(mini)))
for n in range(mini, mini + 2):
    print("     de longueur %2d : %d" % (n, compte(n)))

# ═══ 4. sa suite est-elle correcte ? ═══════════════════════════════════
sien = [(10,10,0,0),(5,10,5,0),(5,10,1,4),(9,10,1,0),(9,6,1,4),(9,7,0,4),
        (9,7,4,0),(9,3,4,4),(9,3,5,3),(9,8,0,3),(4,8,5,3),(4,10,3,3)]
print()
print("=== Son tableau, ligne a ligne ===")
bon = True
for k in range(len(sien) - 1):
    if sien[k+1] not in set(suivants(sien[k])):
        print("  ligne %d -> %d : transvasement IMPOSSIBLE %s -> %s"
              % (k+1, k+2, sien[k], sien[k+1])); bon = False
    if sum(sien[k]) != 20: print("  ligne %d : le total n'est pas 20 !" % (k+1))
print("  les onze transvasements sont tous licites :", bon)
print("  total constant a 20 pintes :", all(sum(e) == 20 for e in sien))
print("  arrivee conforme a la question :", but(sien[-1]))
print("  nombre de transvasements de son tableau : %d" % (len(sien) - 1))
faux = list(sien); faux[2] = (5, 10, 2, 3)            # temoin : 5 -> 4 qui ne remplit pas la 4
print("  temoin (ligne 3 remplacee par un versement qui ne vide ni ne remplit) refuse :",
      faux[2] not in set(suivants(faux[1])))
assert bon and faux[2] not in set(suivants(faux[1]))

# ═══ 5. et si l'on n'avait qu'un seul recipient de dix pintes ? ════════
print()
print("=== Les deux grands recipients sont-ils necessaires ? ===")
for cap, dep in (((10, 5, 4), (10, 0, 0)), ((20, 5, 4), (20, 0, 0))):
    C, D = cap, dep
    def suiv2(e):
        for i in range(len(C)):
            if e[i] == 0: continue
            for j in range(len(C)):
                if i == j or e[j] == C[j]: continue
                q = min(e[i], C[j] - e[j])
                f = list(e); f[i] -= q; f[j] += q
                yield tuple(f)
    d = {D: 0}; fl = deque([D]); res = None
    while fl:
        e = fl.popleft()
        if e[-2] == 3 and e[-1] == 3: res = d[e]; break
        for f in suiv2(e):
            if f not in d: d[f] = d[e] + 1; fl.append(f)
    print("  recipients %s : %s" % (str(C),
          "%d transvasements" % res if res is not None else "IMPOSSIBLE"))

# ═══ 6. combien de solutions vraiment differentes ? ════════════════════
def compte_vers(n, cible):
    niveau = {DEPART: 1}
    for _ in range(n):
        suiv = {}
        for e, k in niveau.items():
            for f in suivants(e):
                suiv[f] = suiv.get(f, 0) + k
        niveau = suiv
    return niveau.get(cible, 0)
print()
print("=== Combien de solutions vraiment differentes ? ===")
a = compte_vers(mini, (4, 10, 3, 3)); b = compte_vers(mini, (10, 4, 3, 3))
print("  chemins de %d coups vers (4,10,3,3) : %d" % (mini, a))
print("  chemins de %d coups vers (10,4,3,3) : %d" % (mini, b))
print("  les deux grands recipients etant interchangeables, cela fait")
print("  %d solutions essentiellement differentes — en onze coups." % a)

# ═══ 7. combien de situations le vin peut-il prendre ? ═════════════════
toutes = [(x, y, z, t) for x in range(11) for y in range(11)
          for z in range(6) for t in range(5) if x+y+z+t == 20]
print()
print("=== L'espace des situations ===")
print("  repartitions possibles du vin, en respectant les contenances : %d"
      % len(toutes))
print("  celles qu'on peut reellement atteindre par transvasements : %d"
      % len(vus))
print("  soit %.0f %% : les transvasements ne menent pas partout."
      % (100*len(vus)/len(toutes)))
