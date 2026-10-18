#!/usr/bin/env python3
"""N° 269 THREE MEN IN A BOAT : le tableau de Dudeney est l'espace projectif PG(3,2).
On cherche une façon de numéroter les quinze hommes par les quinze vecteurs non nuls de quatre bits telle que chaque bordée
{x, y, z} vérifie x XOR y XOR z = 0 : les 35 bordées sont alors exactement les 35 droites de PG(3,2), et chaque journée
(5 bordées disjointes) en est un « spread ».
    python3 pg32.py"""
from itertools import combinations

L = "ABCDEFGHIJKLMNO"
SIEN = [["ABC","DEF","GHI","JKL","MNO"], ["ADG","BKN","COL","JEI","MHF"], ["AJM","BEH","CFI","DKO","GNL"],
        ["AEK","CGM","BOI","DHL","JNF"], ["AHN","CDJ","BFL","GEO","MKI"], ["AFO","BGJ","CKH","DNI","MEL"],
        ["AIL","BDM","CEN","GKF","JHO"]]   # 1er jour corrigé : DEF (le texte imprime « DBF »)

def numerote(bordees):
    """Une numérotation des lettres par 1..15 où chaque bordée fait XOR nul, ou None s'il n'y en a pas."""
    def rec(f):
        for t in bordees:                        # propagation : deux lettres connues fixent la troisième
            k = [c for c in t if c in f]
            if len(k) == 3 and f[t[0]] ^ f[t[1]] ^ f[t[2]]: return None
            if len(k) == 2:
                (u,) = [c for c in t if c not in f]; v = f[k[0]] ^ f[k[1]]
                if v == 0 or v in f.values(): return None
                return rec({**f, u: v})
        libres = [c for c in L if c not in f]
        if not libres: return f
        for v in range(1, 16):
            if v not in f.values():
                r = rec({**f, libres[0]: v})
                if r: return r
        return None
    return rec({})

def juge(nom, jours):
    bordees = [t for j in jours for t in j]
    paires = [p for t in bordees for p in combinations(sorted(t), 2)]
    sts = len(bordees) == 35 and len(set(paires)) == 105 == len(paires)
    f = numerote(bordees) if sts else None
    print("%-28s 105 paires une seule fois : %s ; numérotation projective : %s" % (nom, sts, "oui" if f else "aucune"))
    if f: print("   ", " ".join("%s=%s" % (c, format(f[c], "04b")) for c in L))
    return f is not None

assert juge("tableau de Dudeney", SIEN)
droites = {frozenset((x, y, x ^ y)) for x in range(1, 16) for y in range(1, 16) if x != y}
print("droites de PG(3,2) :", len(droites))
# témoin : un système de triplets de Steiner d'ordre 15 qui n'est pas projectif. On part du tableau et l'on fait une
# « transformation de Pasch » : quatre bordées sur six hommes, deux à deux sécantes, sont remplacées par les quatre autres
# bordées qui couvrent les mêmes douze paires. Le système couvre toujours chaque paire une fois, mais n'a plus de numérotation.
def pasch(bordees):
    B = [frozenset(t) for t in bordees]
    for q in combinations(B, 4):
        pts = frozenset().union(*q)
        if len(pts) != 6 or any(len(x & y) != 1 for x, y in combinations(q, 2)): continue
        paires = {frozenset(p) for t in q for p in combinations(t, 2)}
        for r in combinations([frozenset(t) for t in combinations(sorted(pts), 3)], 4):
            if set(r) != set(q) and {frozenset(p) for t in r for p in combinations(t, 2)} == paires:
                return [t for t in B if t not in q] + list(r)
t = pasch([t for j in SIEN for t in j])
assert not juge("témoin (après un échange de Pasch)", [["".join(sorted(x)) for x in t]])
