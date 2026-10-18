# -*- coding: utf-8 -*-
"""n° 79 THE LOCKERS PUZZLE.

Trois armoires de neuf casiers (trois rangees de trois). Dans chacune, les deux
rangees du haut forment deux nombres de trois chiffres dont la somme est la
rangee du bas. Chaque armoire emploie neuf chiffres DIFFERENTS (un seul des dix
est omis), et le zero ne peut pas occuper la place des centaines.
L'armoire A doit donner la plus petite somme possible, l'armoire C la plus
grande, et les neuf chiffres des trois totaux doivent etre tous differents.
"""
from itertools import combinations

def valides():
    """toutes les additions possibles, la paire etant non ordonnee"""
    out = []
    for x in range(100, 1000):
        for y in range(x, 1000):
            s = x + y
            if s > 999: break
            d = str(x) + str(y) + str(s)
            if len(set(d)) == 9:
                out.append((x, y, s))
    return out

V = valides()
print("=== Toutes les additions possibles ===")
print("  nombre d'additions (paires non ordonnees) : %d" % len(V))
sommes = sorted({s for _, _, s in V})
print("  sommes possibles : %d valeurs, de %d a %d"
      % (len(sommes), sommes[0], sommes[-1]))
print("  les cinq plus petites : %s" % sommes[:5])
print("  les cinq plus grandes : %s" % sommes[-5:])

mini, maxi = sommes[0], sommes[-1]
print()
print("=== Les deux extremes ===")
for nom, val in (("la plus petite", mini), ("la plus grande", maxi)):
    reps = [(x, y) for x, y, s in V if s == val]
    print("  %s somme : %d   (%d ecriture(s) : %s)"
          % (nom, val, len(reps), ", ".join("%d + %d" % r for r in reps)))
print("  Dudeney annonce 356 et 981 :", mini == 356 and maxi == 981)

# ═══ le casse-tete complet ═════════════════════════════════════════════
print()
print("=== Les trois armoires ensemble ===")
dA = set(str(mini)); dC = set(str(maxi))
reste = set("0123456789") - dA - dC
print("  chiffres pris par les totaux de A et de C : %s"
      % "".join(sorted(dA | dC)))
print("  il reste %s pour le total de B" % "".join(sorted(reste)))
milieux = sorted({s for _, _, s in V if set(str(s)) <= reste})
print("  totaux possibles pour B : %s" % milieux)
print("  Dudeney annonce 720, 702 et 407 :", milieux == [407, 702, 720])

print()
print("=== Le compte des 3 072 ===")
print("  ATTENTION : les ecritures trouvees ci-dessus ne sont pas")
print("  independantes. Echanger les deux chiffres d'une colonne du haut ne")
print("  change pas la somme : les 2^3 = 8 echanges donnent 8 dispositions,")
print("  soit 4 paires non ordonnees. Le nombre de dispositions VRAIMENT")
print("  differentes s'obtient donc en divisant par quatre.")
def classes(val):
    return len([1 for x, y, s in V if s == val]) // 4
cA = classes(mini); cC = classes(maxi)
cB = sum(classes(v) for v in milieux)
print()
print("  armoire A : %d ecriture(s) essentiellement differente(s)" % cA)
print("  armoire B : %d" % cB)
print("  armoire C : %d" % cC)
print("  dispositions totales : %d x %d x %d x 8^3 = %d"
      % (cA, cB, cC, cA*cB*cC*512))
print("  Dudeney annonce 3 072 :", cA*cB*cC*512 == 3072)
print()
print("  ses mots : « aucun choix pour la premiere armoire, une alternative")
print("  pour la troisieme, et l'un de trois arrangements pour celle du")
print("  milieu » -> %d, %d et %d. Exact." % (cA, cC, cB))

# ═══ la clause sur le zero ═════════════════════════════════════════════
print()
print("=== La clause sur le zero aux centaines ===")
sans = []
for x in range(0, 1000):
    for y in range(x, 1000):
        s = x + y
        if s > 999: break
        d = "%03d%03d%03d" % (x, y, s)
        if len(set(d)) == 9: sans.append((x, y, s))
print("  en autorisant un zero en tete : %d additions au lieu de %d"
      % (len(sans), len(V)))
print("  la plus petite somme tomberait a %d, la plus grande monterait a %d"
      % (min(s for _, _, s in sans), max(s for _, _, s in sans)))
print("  La clause n'est donc pas decorative : elle change la reponse.")

# ═══ sa table « chiffre omis -> somme des chiffres du total » ═══════════
print()
print("=== Sa table : chiffre omis -> somme des chiffres du total ===")
def S(n): return sum(map(int, str(n)))
def omis(x, y, s): return int((set("0123456789") - set(str(x) + str(y) + str(s))).pop())
SA_TABLE = {9: 9, 7: 10, 5: 11, 3: 12, 1: 13, 8: 14, 6: 15, 4: 16, 2: 17, 0: 18}
ecarts = [(x, y, s) for x, y, s in V if S(s) != SA_TABLE[omis(x, y, s)]]
print("  additions qui la contredisent : %d sur %d" % (len(ecarts), len(V)))
for d in sorted(SA_TABLE):
    n = sum(1 for x, y, s in V if omis(x, y, s) == d)
    print("     %d omis -> %2d   (%d additions)" % (d, SA_TABLE[d], n))

def retenues(x, y):
    c, r = 0, 0
    for i in range(3):
        r = (x // 10**i % 10 + y // 10**i % 10 + r) >= 10
        c += r
    return c
print()
print("=== Ce que la table dit de plus : le nombre de retenues ===")
print("  S(x) + S(y) = S(x+y) + 9c, et les neuf chiffres font 45 - d,")
print("  d'ou 2 S(total) = 45 - d - 9c : la parite de d fixe c.")
loi = [(x, y, s) for x, y, s in V
       if retenues(x, y) != (1 if omis(x, y, s) % 2 == 0 else 2)
       or 2 * S(s) != 45 - omis(x, y, s) - 9 * retenues(x, y)]
print("  d pair -> 1 retenue, d impair -> 2 : contredit par %d addition(s)" % len(loi))

# temoins : une addition fautive, une table alteree, doivent etre refusees
print()
faux = (123, 456, 579)                     # le 5 sert deux fois
print("  temoin 123 + 456 = 579 (le 5 deux fois) retenu :", faux in V, "-> refuse")
TABLE_FAUSSE = dict(SA_TABLE); TABLE_FAUSSE[9], TABLE_FAUSSE[7] = 10, 9
n_faux = sum(1 for x, y, s in V if S(s) != TABLE_FAUSSE[omis(x, y, s)])
print("  temoin : table avec 9 et 7 echanges -> %d contradiction(s), refusee" % n_faux)
assert faux not in V and n_faux > 0 and not ecarts and not loi
assert len(V) == 544 and len(sommes) == 115 and cA * cB * cC * 512 == 3072
assert retenues(999, 1) == 3 and retenues(123, 456) == 0
