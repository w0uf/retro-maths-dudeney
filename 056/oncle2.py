# -*- coding: utf-8 -*-
"""n° 56 WILSON'S POSER — suite : et la loi ?

Dudeney insiste : la parente doit s'obtenir « sans aucun mariage dans les degres
prohibes ». Or en Angleterre les degres prohibes ne couvraient pas seulement la
consanguinite : la table de parente de l'Eglise interdisait aussi l'ALLIANCE —
epouser la femme de son pere, la fille de sa femme, la femme de son fils...
(la sœur de l'epouse defunte, elle, etait devenue licite par la loi de 1907.)
"""
from oncle import familles, ancetres, consanguins, couples, freres, oncles, \
                  canonique, degres_prohibes

def parents(par, i): return set(par[i]) if par[i] else set()
def enfants(par, n, i): return {j for j in range(n) if par[j] and i in par[j]}
def fratrie(par, n, i): return {j for j in range(n) if freres(par, i, j)}
def proches(par, n, i):
    """parents, enfants, freres et sœurs : les consanguins du premier cercle"""
    return parents(par, i) | enfants(par, n, i) | fratrie(par, n, i)

def conjoints(par, n):
    c = {}
    for f, m in couples(par):
        c.setdefault(f, set()).add(m); c.setdefault(m, set()).add(f)
    return c

def alliance_prohibee(par, n):
    """un mariage avec la femme d'un proche, ou avec une proche de sa femme —
    la sœur de l'epouse exceptee (loi de 1907)."""
    conj = conjoints(par, n)
    for a, b in couples(par):
        for x, y in ((a, b), (b, a)):
            # y est l'epouse d'un proche de x  (belle-mere, bru, belle-sœur...)
            for z in proches(par, n, x):
                if y in conj.get(z, ()) and not freres(par, z, x):
                    return True
                if y in conj.get(z, ()) and freres(par, z, x):
                    pass                      # sœur/frere du conjoint : licite
            # y est une proche d'une AUTRE epouse de x (belle-fille, belle-mere)
            for z in conj.get(x, ()) - {y}:
                if y in (parents(par, z) | enfants(par, n, z)):
                    return True
    return False

def interdit(par, n):
    return degres_prohibes(par) or alliance_prohibee(par, n)

def cherche2(n):
    out = {}
    for sexe, par in familles(n):
        if interdit(par, n): continue
        o = oncles(sexe, par, n, False)
        p = [(a, b) for a, b in o if (b, a) in o and a < b]
        if p: out[canonique(sexe, par, n)] = (sexe, par, p[0])
    return out

if __name__ == "__main__":
    print("=== Les deux solutions a sept personnes tiennent-elles devant la loi ? ===")
    sept = [
      (("F","H","F","H","F","H","H"), (None,None,(1,0),None,(3,0),(3,2),(1,4))),
      (("F","F","H","H","H","H","H"), (None,None,None,(2,1),(3,0),(2,0),(5,1))),
    ]
    for k, (sexe, par) in enumerate(sept, 1):
        print("  configuration %d : consanguinite %s | alliance %s"
              % (k, "interdite" if degres_prohibes(par) else "licite",
                 "INTERDITE" if alliance_prohibee(par, 7) else "licite"))

    print()
    print("=== La disposition que Dudeney decrit vraiment ===")
    # deux hommes SANS lien entre eux, chacun epousant la mere de l'autre :
    # 0 pere de A, 1 mere de A, 2 pere de B, 3 mere de B,
    # 4 = A, 5 = B, 6 = fils de A et de la mere de B, 7 = fils de B et de la mere de A
    sexe = ("H","F","H","F","H","H","H","H")
    par  = (None,None,None,None,(0,1),(2,3),(4,3),(5,1))
    print("  huit personnes | consanguinite :", degres_prohibes(par),
          "| alliance :", alliance_prohibee(par, 8))
    o = oncles(sexe, par, 8, False)
    print("  6 oncle de 7 :", (6,7) in o, " | 7 oncle de 6 :", (7,6) in o)

    print()
    print("=== Minimum devant la loi complete ===")
    for n in (7, 8):
        t = cherche2(n)
        print("  %d personnes : %d configuration(s) essentiellement differente(s)"
              % (n, len(t)))
