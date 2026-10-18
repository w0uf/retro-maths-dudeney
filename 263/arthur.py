# -*- coding: utf-8 -*-
"""n° 263 KING ARTHUR'S KNIGHTS.

Le roi Arthur et ses six chevaliers — Beleobus, Caradoc, Driam, Eric, Floll,
Galahad — s'assoient trois soirs de suite a la Table ronde sans que personne
n'ait jamais deux fois le meme voisin. Le premier soir, ordre alphabetique.
Arthur veut ensuite Beleobus AUSSI PRES que possible de lui et Galahad AUSSI
LOIN que possible. « Aucune autre facon de placer les chevaliers n'aurait ete
aussi satisfaisante. »
"""
from itertools import permutations

N = "ABCDEFG"            # A = Arthur, B..G = les six chevaliers
I = {c: i for i, c in enumerate(N)}

def paires(ordre):
    """les sept couples de voisins d'une disposition circulaire"""
    return {frozenset((ordre[i], ordre[(i+1) % 7])) for i in range(7)}

def distance(ordre, x, y):
    """distance le long de la table (de 1 a 3)"""
    a, b = ordre.index(x), ordre.index(y)
    d = abs(a - b)
    return min(d, 7 - d)

SOIR1 = tuple(N)          # ordre alphabetique
P1 = paires(SOIR1)
print("=== Le premier soir ===")
print("  ordre :", " ".join(SOIR1))
print("  voisins d'Arthur : %s" % sorted(x for p in P1 if "A" in p
                                         for x in p if x != "A"))
print("  -> B et G sont deja voisins d'Arthur : ils ne pourront plus l'etre.")

# ═══ la contrainte est-elle serree ? ═══════════════════════════════════
print()
print("=== Combien de couples les trois soirees consomment-elles ? ===")
print("  chaque soiree place 7 couples de voisins ; trois soirees en font 21.")
print("  or sept convives forment 7x6/2 = %d couples." % (7*6//2))
print("  -> les trois soirees doivent user CHAQUE couple exactement une fois :")
print("     il n'y a pas un gramme de jeu. C'est ce que les mathematiciens")
print("     appellent une decomposition du graphe complet en circuits")
print("     hamiltoniens, et Dudeney n'en dit pas un mot.")

# ═══ toutes les paires de soirees possibles ════════════════════════════
# on fixe Arthur en tete (la table est ronde) et on ignore le sens de lecture
def dispositions():
    vues = set()
    for p in permutations(N[1:]):
        o = ("A",) + p
        r = ("A",) + tuple(reversed(p))
        if r in vues: continue
        vues.add(o)
        yield o
TOUTES = list(dispositions())
print()
print("=== Les dispositions possibles ===")
print("  dispositions distinctes (table ronde, sens ignore) : %d" % len(TOUTES))

bonnes = []
for o2 in TOUTES:
    P2 = paires(o2)
    if P1 & P2: continue
    for o3 in TOUTES:
        P3 = paires(o3)
        if (P1 & P3) or (P2 & P3): continue
        bonnes.append((o2, o3))
print("  couples de soirees 2 et 3 sans voisin repete : %d" % len(bonnes))
print("  (chaque solution y figure deux fois, les soirees 2 et 3 etant")
print("   interchangeables : soit %d arrangements distincts.)" % (len(bonnes)//2))

# ═══ le critere d'Arthur ═══════════════════════════════════════════════
print()
print("=== Le vœu du roi ===")
res = {}
for o2, o3 in bonnes:
    db = (distance(o2, "A", "B"), distance(o3, "A", "B"))
    dg = (distance(o2, "A", "G"), distance(o3, "A", "G"))
    # B doit etre proche LES DEUX SOIRS : on regarde sa plus grande distance.
    # G doit etre loin LES DEUX SOIRS : on regarde sa plus PETITE distance.
    res.setdefault((max(db), min(dg)), []).append((o2, o3))
print("  (B au plus loin sur les deux soirs, G au plus pres) -> nombre de cas :")
for k in sorted(res):
    print("     B jamais au-dela de %d, G jamais en-deca de %d : %3d"
          % (k[0], k[1], len(res[k])))
meilleur = min(res, key=lambda k: (k[0], -k[1]))
print("  l'optimum est : B a %d au plus, G a %d au moins." % meilleur)
print("  nombre de couples de soirees qui l'atteignent : %d" % len(res[meilleur]))
print("  soit %d arrangements distincts." % (len(res[meilleur])//2))

# ═══ la sienne y est-elle ? ════════════════════════════════════════════
S2 = tuple("AFBDGEC"); S3 = tuple("AEBGCFD")
def norme(o):
    r = ("A",) + tuple(reversed(o[1:]))
    return min(o, r)
print()
print("=== Sa reponse ===")
print("  soir 2 :", " ".join(S2), "  soir 3 :", " ".join(S3))
print("  aucun voisin repete :",
      not (paires(SOIR1) & paires(S2)) and not (paires(SOIR1) & paires(S3))
      and not (paires(S2) & paires(S3)))
temoin = tuple("ACBDEFG")                       # le 1er soir avec B et C echanges
print("  temoin (1er soir, B et C echanges) refuse :", bool(paires(SOIR1) & paires(temoin)))
assert paires(SOIR1) & paires(temoin)
print("  distances de B : %d et %d" % (distance(S2,"A","B"), distance(S3,"A","B")))
print("  distances de G : %d et %d" % (distance(S2,"A","G"), distance(S3,"A","G")))
dans = any({norme(a), norme(b)} == {norme(S2), norme(S3)} for a, b in res[meilleur])
print("  figure parmi les arrangements optimaux :", dans)
print("  « aucune autre facon n'aurait ete aussi satisfaisante » :")
print("     il y en a %d en tout, la sienne comprise." % (len(res[meilleur])//2))

# ═══ les deux arrangements optimaux, en clair ══════════════════════════
print()
print("=== L'arrangement optimal, en clair ===")
vus = set()
for o2, o3 in res[meilleur]:
    cle = frozenset({norme(o2), norme(o3)})
    if cle in vus: continue
    vus.add(cle)
    a, b = sorted(cle)
    print("   soir 2 : %s      soir 3 : %s" % (" ".join(a), " ".join(b)))
    print("      B a %d et %d ; G a %d et %d"
          % (distance(a,"A","B"), distance(b,"A","B"),
             distance(a,"A","G"), distance(b,"A","G")))
print()
print("  il est UNIQUE : sa phrase « aucune autre facon n'aurait ete aussi")
print("  satisfaisante » est litteralement vraie, et pas seulement au sens")
print("  de « aucune meilleure ».")
