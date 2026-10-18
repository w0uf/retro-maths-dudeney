# -*- coding: utf-8 -*-
"""n° 266 A TENNIS TOURNAMENT — Dudeney, Amusements in Mathematics (1917).

Quatre couples, double mixte (un homme et une dame contre un homme et une
dame), deux courts, trois jours ; personne ne doit jamais jouer avec ni
contre la meme personne plus d'une fois.  Dudeney donne la grille, et note
que personne n'y joue avec ni contre son conjoint.

Puis il lance un defi : « Si le lecteur veut un casse-tete difficile, qu'il
essaie d'arranger huit couples (sur quatre courts en sept jours) dans des
conditions exactement semblables.  Cela peut se faire, mais je lui laisse
dans ce cas le plaisir de chercher la reponse et la solution generale. »
"""
from itertools import combinations

# --- sa grille a quatre couples ---------------------------------------
H = "ABDE"; F = "abde"
SIENNE = [ (("A","d"),("B","e")), (("D","a"),("E","b")),
           (("A","e"),("D","b")), (("E","a"),("B","d")),
           (("A","b"),("E","d")), (("B","a"),("D","e")) ]
JOURS  = [SIENNE[0:2], SIENNE[2:4], SIENNE[4:6]]

def audit(jours, n):
    part, adv, ok = {}, {}, True
    for j, matchs in enumerate(jours, 1):
        vus = set()
        for (m1,f1),(m2,f2) in matchs:
            for x in (m1,f1,m2,f2):
                if x in vus: print("   %s joue deux fois le jour %d" % (x,j)); ok=False
                vus.add(x)
            for p in ((m1,f1),(m2,f2)):
                k = tuple(sorted(p)); part[k] = part.get(k,0)+1
            for p in ((m1,m2),(m1,f2),(f1,m2),(f1,f2)):
                k = tuple(sorted(p)); adv[k] = adv.get(k,0)+1
        if len(vus) != 2*n: print("   tout le monde ne joue pas le jour", j); ok=False
    rep_p = {k:v for k,v in part.items() if v>1}
    rep_a = {k:v for k,v in adv.items() if v>1}
    print("   paires de partenaires repetees :", rep_p or "aucune")
    print("   paires d'adversaires repetees  :", rep_a or "aucune")
    conj = [k for k in list(part)+list(adv) if k[0].lower()==k[1].lower()]
    print("   quelqu'un avec ou contre son conjoint :", conj or "jamais")
    print("   partenariats distincts :", len(part), "sur", n*(n-1), "possibles hors conjoints")
    print("   oppositions distinctes :", len(adv), "sur", n*(2*n-1)-n, "possibles hors conjoints")
    return ok

print("=== Sa grille a quatre couples ===")
audit(JOURS, 4)

# --- le defi : huit couples, quatre courts, sept jours -----------------
print("\n=== Son defi : huit couples, quatre courts, sept jours ===")
N = 8
def couplages(elems):
    if not elems: yield []; return
    a = elems[0]
    for i in range(1, len(elems)):
        b = elems[i]
        reste = elems[1:i] + elems[i+1:]
        for r in couplages(reste): yield [(a,b)] + r
APPARIEMENTS = [tuple(sorted(tuple(sorted(p)) for p in c)) for c in couplages(list(range(N)))]
print("appariements possibles des huit hommes :", len(APPARIEMENTS))

# partenariats : le jour d, l'homme m joue avec la dame m+d (mod 8)
# -> chaque couple (homme, dame) non conjoint sert exactement une fois
sol = []
def cherche(d, hh, ff, hf):
    if d == 8: return True
    for P in APPARIEMENTS:
        nh, nf, nhf = set(), set(), set()
        bon = True
        for (i, j) in P:
            if (j - i) % N == d % N or (i - j) % N == d % N: bon = False; break   # contre son conjoint
            a = (i, j)
            b = tuple(sorted(((i+d) % N, (j+d) % N)))
            c1 = (i, (j+d) % N); c2 = (j, (i+d) % N)
            if a in hh or a in nh: bon=False; break
            if b in ff or b in nf: bon=False; break
            if c1 in hf or c1 in nhf or c2 in hf or c2 in nhf: bon=False; break
            nh.add(a); nf.add(b); nhf.add(c1); nhf.add(c2)
        if not bon: continue
        sol.append((d, P))
        if cherche(d+1, hh|nh, ff|nf, hf|nhf): return True
        sol.pop()
    return False

if cherche(1, set(), set(), set()):
    print("GRILLE TROUVEE\n")
    noms_h = "ABCDEFGH"; noms_f = "abcdefgh"
    jours = []
    for d, P in sol:
        matchs = []
        for (i, j) in P:
            matchs.append(((noms_h[i], noms_f[(i+d) % N]), (noms_h[j], noms_f[(j+d) % N])))
        jours.append(matchs)
        print("  Jour %d :" % d, "   ".join("%s%s contre %s%s" % (a,b,c,e)
              for (a,b),(c,e) in matchs))
    print("\n  Verification independante :")
    audit(jours, 8)
else:
    print("aucune grille de cette forme")
