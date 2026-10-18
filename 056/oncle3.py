# -*- coding: utf-8 -*-
"""Les trois dispositions minimales, et la robustesse du resultat."""
from oncle import familles, couples, freres, oncles, canonique, degres_prohibes
from oncle2 import proches, conjoints, parents, enfants

def alliance(par, n, belle_soeur_licite=True, veuve_du_frere_licite=True):
    conj = conjoints(par, n)
    for a, b in couples(par):
        for x, y in ((a, b), (b, a)):
            for z in proches(par, n, x):
                if y in conj.get(z, ()):
                    if freres(par, z, x):
                        if not veuve_du_frere_licite: return True
                    else:
                        return True
            for z in conj.get(x, ()) - {y}:
                if y in (parents(par, z) | enfants(par, n, z)): return True
                if freres(par, z, y) and not belle_soeur_licite: return True
    return False

def cherche(n, **kw):
    out = {}
    for sexe, par in familles(n):
        if degres_prohibes(par) or alliance(par, n, **kw): continue
        o = oncles(sexe, par, n, False)
        p = [(a, b) for a, b in o if (b, a) in o and a < b]
        if p: out[canonique(sexe, par, n)] = (sexe, par, p[0])
    return out

if __name__ == "__main__":
    print("=== Les trois dispositions a huit personnes (loi de 1917) ===")
    t = cherche(8)
    for i, (k, (sexe, par, (a, b))) in enumerate(sorted(t.items()), 1):
        print("  -- disposition %d --" % i)
        for j in range(8):
            print("     %d (%s) %s" % (j, sexe[j],
                  "enfant de %d et %d" % par[j] if par[j] else "-"))
        print("     %d et %d : oncle et neveu l'un de l'autre" % (a, b))

    # celle que Dudeney decrit (deux hommes epousant chacun la mere de l'autre, voir oncle2.py)
    dudeney = canonique(("H","F","H","F","H","H","H","H"), (None,None,None,None,(0,1),(2,3),(4,3),(5,1)), 8)
    print("  celle de Dudeney est la disposition", 1 + sorted(t).index(dudeney))

    print()
    print("=== Le resultat depend-il des details de la loi ? ===")
    for bs in (True, False):
        for vf in (True, False):
            n7 = len(cherche(7, belle_soeur_licite=bs, veuve_du_frere_licite=vf))
            n8 = len(cherche(8, belle_soeur_licite=bs, veuve_du_frere_licite=vf))
            print("  sœur de l'epouse %-7s | veuve du frere %-7s -> 7 pers. : %d,"
                  "  8 pers. : %d" % ("licite" if bs else "interdite",
                  "licite" if vf else "interdite", n7, n8))
