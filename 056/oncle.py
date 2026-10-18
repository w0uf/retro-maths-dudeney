# -*- coding: utf-8 -*-
"""n° 56 WILSON'S POSER.

« David George Linklater est mon oncle, et il est aussi mon neveu. »
Dudeney repond : deux hommes epousent chacun la mere de l'autre ; les fils issus
de ces deux mariages sont, chacun, l'oncle ET le neveu de l'autre. Puis il
ajoute : « Il y a d'autres facons d'amener cette parente, mais celle-ci est la
plus simple. » Il ne dit pas lesquelles. On les cherche.

Modele : n personnes numerotees dans un ordre topologique (les parents avant les
enfants — c'est sans perte de generalite), un sexe par personne, et pour chacune
soit aucun parent, soit un couple (pere, mere) deja present.
"""
from itertools import product, permutations

def familles(n):
    """toutes les structures familiales a n personnes, a renumerotation pres"""
    for sexe in product("HF", repeat=n):
        choix = []
        for i in range(n):
            h = [j for j in range(i) if sexe[j] == "H"]
            f = [j for j in range(i) if sexe[j] == "F"]
            choix.append([None] + [(a, b) for a in h for b in f])
        for par in product(*choix):
            yield sexe, par

def ancetres(par, i):
    vus, pile = set(), [i]
    while pile:
        v = pile.pop()
        if par[v]:
            for p in par[v]:
                if p not in vus: vus.add(p); pile.append(p)
    return vus

def consanguins(par, a, b):
    """a et b ont-ils un ancetre commun, ou l'un est-il ancetre de l'autre ?"""
    A, B = ancetres(par, a) | {a}, ancetres(par, b) | {b}
    return bool(A & B)

def couples(par):
    return {p for p in par if p}

def degres_prohibes(par):
    return any(consanguins(par, f, m) for f, m in couples(par))

def freres(par, a, b):
    return a != b and par[a] and par[b] and bool(set(par[a]) & set(par[b]))

def oncles(sexe, par, n, alliance):
    """couples (u, v) tels que u soit oncle de v"""
    conj = {}
    for f, m in couples(par):
        conj.setdefault(f, set()).add(m); conj.setdefault(m, set()).add(f)
    out = set()
    for u in range(n):
        if sexe[u] != "H": continue
        for v in range(n):
            if not par[v]: continue
            if any(freres(par, u, p) for p in par[v]):
                out.add((u, v)); continue
            if alliance and any(freres(par, w, p)
                                for w in conj.get(u, ()) for p in par[v]):
                out.add((u, v))
    return out

def canonique(sexe, par, n):
    best = None
    for s in permutations(range(n)):
        sx = [None]*n; pr = [None]*n
        for i in range(n):
            sx[s[i]] = sexe[i]
            pr[s[i]] = tuple(sorted((s[par[i][0]], s[par[i][1]]))) if par[i] else (-1, -1)
        c = (tuple(sx), tuple(pr))
        if best is None or c < best: best = c
    return best

def cherche(n, alliance=False, interdits=True):
    trouves = {}
    for sexe, par in familles(n):
        if interdits and degres_prohibes(par): continue
        o = oncles(sexe, par, n, alliance)
        paires = [(a, b) for a, b in o if (b, a) in o and a < b]
        if paires:
            trouves[canonique(sexe, par, n)] = (sexe, par, paires[0])
    return trouves

def oncles_entiers(sexe, par, n):
    """comme oncles(), mais avec des freres de pere ET de mere seulement"""
    def freres_entiers(a, b):
        return a != b and par[a] and par[b] and set(par[a]) == set(par[b])
    out = set()
    for u in range(n):
        if sexe[u] != "H": continue
        for v in range(n):
            if par[v] and any(freres_entiers(u, p) for p in par[v]):
                out.add((u, v))
    return out

if __name__ == "__main__":
    print("=== Les detecteurs, eprouves sur des temoins ===")
    # un frere qui epouse sa sœur : 0 pere, 1 mere, 2 fils, 3 fille, 4 enfant de 2 et 3
    par = (None, None, (0, 1), (0, 1), (2, 3))
    print("  frere epousant sa sœur, refuse :", degres_prohibes(par))
    assert degres_prohibes(par)
    # un oncle ordinaire : 0 pere, 1 mere, 2 et 3 leurs fils, 4 epouse de 2, 5 fils de 2 et 4
    sexe = ("H", "F", "H", "H", "F", "H")
    par = (None, None, (0, 1), (0, 1), None, (2, 4))
    o = oncles(sexe, par, 6, False)
    print("  oncle ordinaire : 3 oncle de 5 :", (3, 5) in o, "| 5 oncle de 3 :", (5, 3) in o,
          "-> pas d'oncle-neveu reciproque, refuse :", not any((b, a) in o for a, b in o))
    assert (3, 5) in o and not any((b, a) in o for a, b in o)
    print("  le meme oncle, vu par le detecteur a freres pleins :", (3, 5) in oncles_entiers(sexe, par, 6))
    assert (3, 5) in oncles_entiers(sexe, par, 6)
    print()

    print("=== Combien de personnes faut-il au minimum ? ===")
    mini = None
    for n in range(2, 9):
        t = cherche(n)
        print("  %d personnes : %d configuration(s) essentiellement differente(s)"
              % (n, len(t)))
        if t:
            mini = n
            break

    print()
    print("=== Les configurations minimales ===")
    t = cherche(mini)
    for k, (sexe, par, (a, b)) in sorted(t.items()):
        print("  sexes %s" % "".join(sexe))
        for i in range(mini):
            p = par[i]
            print("     %d (%s) %s" % (i, sexe[i],
                  "enfant de %d et %d" % p if p else "— sans parents connus"))
        print("     %d et %d sont oncle et neveu l'un de l'autre" % (a, b))

    print()
    print("=== La construction de Dudeney y est-elle ? ===")
    # 0 = mere de A, 1 = mere de B, 2 = A, 3 = B, 4 = fils de A et de la mere de B,
    # 5 = fils de B et de la mere de A
    # telle qu'il la decrit, il faut aussi les PERES de A et de B : le plus
    # economique est de leur donner le meme pere.
    # 0 = le pere commun, 1 = mere de A, 2 = mere de B, 3 = A, 4 = B,
    # 5 = fils de A et de la mere de B, 6 = fils de B et de la mere de A
    sexe = ("H", "F", "F", "H", "H", "H", "H")
    par  = (None, None, None, (0, 1), (0, 2), (3, 2), (4, 1))
    print("  sexes", "".join(sexe), "| parentes", par)
    print("  aucun mariage entre consanguins :", not degres_prohibes(par))
    o = oncles(sexe, par, 7, False)
    print("  5 oncle de 6 :", (5, 6) in o, " | 6 oncle de 5 :", (6, 5) in o)
    print("  cette configuration est-elle dans la liste minimale :",
          canonique(sexe, par, 7) in t)

    print()
    print("=== Faut-il des DEMI-freres ? ===")
    for n in range(2, 9):
        k = 0
        for sexe, par in familles(n):
            if degres_prohibes(par): continue
            o = oncles_entiers(sexe, par, n)
            if any((b, a) in o for a, b in o if a < b): k += 1
        print("  %d personnes, freres au sens PLEIN seulement : %d cas" % (n, k))
