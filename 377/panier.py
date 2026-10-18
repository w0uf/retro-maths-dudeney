# -*- coding: utf-8 -*-
"""n° 377 STEALING THE CASTLE TREASURE.

Une poulie, deux paniers : quand l'un est au sol, l'autre est a la fenetre. Le
seul moteur est la difference de poids. L'homme pese 195 livres, le jeune homme
105, le garcon 90, le coffre 75. « Le poids du panier qui descend ne pouvait
exceder celui de l'autre de plus de 15 livres sans provoquer une descente si
rapide qu'elle fut tres dangereuse POUR UN ETRE HUMAIN, quoiqu'elle n'abimat pas
le bien vole. » Un panier ne peut recevoir que deux personnes, ou une personne
et le coffre. Tous doivent descendre, avec le coffre.

Dudeney : « Voici la meilleure reponse, en onze manipulations. » Verifions.
"""
from itertools import combinations
from collections import deque

P = {"homme": 195, "jeune": 105, "garcon": 90, "coffre": 75}
GENS = {"homme", "jeune", "garcon"}
TOUT = frozenset(P)

def charges(dispo):
    """les chargements licites d'un panier, pris dans « dispo »"""
    out = [frozenset()]
    for x in dispo:
        out.append(frozenset({x}))
    for a, b in combinations(sorted(dispo), 2):
        if a in GENS and b in GENS: out.append(frozenset({a, b}))
        elif "coffre" in (a, b): out.append(frozenset({a, b}))
    return out

def poids(c): return sum(P[x] for x in c)

def coups(haut, regle):
    """un coup : on charge le panier de la FENETRE (seul a pouvoir descendre)
    et celui du sol ; le premier doit etre le plus lourd."""
    bas = TOUT - haut
    for T in charges(haut):
        for G in charges(bas):
            d = poids(T) - poids(G)
            if d <= 0: continue
            if regle == "descente" and (T & GENS) and d > 15: continue
            if regle == "humains" and ((T | G) & GENS) and d > 15: continue
            if regle == "toujours" and d > 15: continue
            yield frozenset((haut - T) | G)

def resous(regle):
    dist = {TOUT: 0}; pere = {TOUT: None}; f = deque([TOUT])
    while f:
        e = f.popleft()
        if not e: break
        for s in coups(e, regle):
            if s not in dist:
                dist[s] = dist[e] + 1; pere[s] = e; f.append(s)
    return dist, pere

print("=== Le minimum, selon la lecture de la clause des 15 livres ===")
for regle, texte in (("descente", "seul un HUMAIN QUI DESCEND est en danger"),
                     ("humains", "tout humain, qui monte ou qui descend"),
                     ("toujours", "la regle s'applique aussi au coffre seul")):
    dist, _ = resous(regle)
    n = dist.get(frozenset())
    print("  %-52s : %s" % (texte,
          "%d manipulations" % n if n is not None else "IMPOSSIBLE"))
print("  Dudeney en annonce onze.")

# ═══ sa suite, verifiee coup par coup ══════════════════════════════════
sien = [("coffre", ""), ("garcon", "coffre"), ("jeune", "garcon"),
        ("coffre", ""), ("homme", "jeune coffre"), ("coffre", ""),
        ("garcon", "coffre"), ("coffre", ""), ("jeune", "garcon"),
        ("garcon", "coffre"), ("coffre", "")]
print()
print("=== Son tableau, coup par coup ===")
haut, bon = TOUT, True
for k, (desc, mont) in enumerate(sien, 1):
    T = frozenset(desc.split()); G = frozenset(mont.split()) if mont else frozenset()
    d = poids(T) - poids(G)
    ok = T <= haut and G <= (TOUT - haut) and d > 0 and \
         (not (T & GENS) or d <= 15) and T in charges(haut) and G in charges(TOUT-haut)
    if not ok: bon = False
    print("  %2d. descend %-14s monte %-14s ecart %4d  %s"
          % (k, " + ".join(sorted(T)) or "-", " + ".join(sorted(G)) or "-", d,
             "licite" if ok else "ILLICITE"))
    haut = frozenset((haut - T) | G)
print("  tout le monde en bas a la fin :", not haut, "| tous les coups licites :", bon)
# temoin : l'homme descend seul au 5e coup (ecart 195 - 0, mortel)
def licite(T, G, haut):
    d = poids(T) - poids(G)
    return T <= haut and G <= (TOUT - haut) and d > 0 and (not (T & GENS) or d <= 15) \
        and T in charges(haut) and G in charges(TOUT - haut)
h = TOUT
for desc, mont in sien[:4]:
    h = frozenset((h - frozenset(desc.split())) | (frozenset(mont.split()) if mont else frozenset()))
print("  temoin (5e coup : l'homme descend seul) refuse :", not licite(frozenset({"homme"}), frozenset(), h))
assert bon and not haut and not licite(frozenset({"homme"}), frozenset(), h)

# ═══ combien de solutions en onze coups ? ══════════════════════════════
def compte(n, regle):
    niveau = {TOUT: 1}
    for _ in range(n):
        s = {}
        for e, k in niveau.items():
            if not e: continue                 # on s'arrete des qu'on a fini
            for f in coups(e, regle):
                s[f] = s.get(f, 0) + k
        niveau = s
    return niveau.get(frozenset(), 0)
dist, _ = resous("descente")
m = dist[frozenset()]
print()
print("=== Combien de suites optimales ? ===")
print("  suites de %d coups qui aboutissent : %d" % (m, compte(m, "descente")))
print("  situations atteignables : %d sur %d concevables" % (len(dist), 2**4))

# ═══ la regle « deux personnes, ou une personne et le coffre » sert-elle ?
print()
print("=== Et si un panier pouvait tout emporter ? ===")
def charges_libres(dispo):
    out = []
    d = sorted(dispo)
    for k in range(len(d) + 1):
        for c in combinations(d, k): out.append(frozenset(c))
    return out
def coups_libres(haut):
    bas = TOUT - haut
    for T in charges_libres(haut):
        for G in charges_libres(bas):
            d = poids(T) - poids(G)
            if d <= 0: continue
            if (T & GENS) and d > 15: continue
            yield frozenset((haut - T) | G)
dist = {TOUT: 0}; f = deque([TOUT])
while f:
    e = f.popleft()
    for s in coups_libres(e):
        if s not in dist: dist[s] = dist[e] + 1; f.append(s)
print("  sans la regle de chargement : %d manipulations" % dist[frozenset()])
print("  avec : 11. La regle change donc bien quelque chose."
      if dist[frozenset()] != 11 else
      "  avec : 11 aussi. La regle de chargement ne change rien au compte.")

# ═══ qui voyage le plus ? ══════════════════════════════════════════════
print()
print("=== Qui fait le plus de trajets dans sa solution ? ===")
comptes = {x: 0 for x in P}
for desc, mont in sien:
    for x in desc.split() + (mont.split() if mont else []): comptes[x] += 1
for x, k in sorted(comptes.items(), key=lambda t: -t[1]):
    print("  %-8s : %2d trajets sur les 11 manipulations" % (x, k))
