# -*- coding: utf-8 -*-
"""n° 101 THE TRUSSES OF HAY.

Cinq bottes de foin. Hodge, « le benêt », les pèse DEUX PAR DEUX de toutes les
façons possibles et rapporte les dix poids :
    110, 112, 113, 114, 115, 116, 117, 118, 120, 121 livres.
Dudeney affirme qu'il n'est « nullement nécessaire » de savoir quelle pesée
correspond à quelle paire. Vérifions — et demandons-nous si cela resterait vrai
avec un autre nombre de bottes.
"""
from itertools import combinations
from fractions import Fraction

PESEES = [110, 112, 113, 114, 115, 116, 117, 118, 120, 121]
def sommes(t): return tuple(sorted(a+b for a, b in combinations(t, 2)))
cible = tuple(sorted(PESEES))

# ═══ 1. les cinq poids, par recherche exhaustive ════════════════════════
# Deux faits immédiats : la plus petite pesée est celle des deux bottes les
# plus légères (a+b = 110), la plus grande celle des deux plus lourdes
# (d+e = 121) ; et la somme des dix pesées compte chaque botte quatre fois,
# donc a+b+c+d+e = 1156/4 = 289. La botte du milieu est alors forcée, et il
# ne reste qu'à balayer a et e.
total = sum(PESEES) // 4
sol = []
for a in range(1, 110):
    b = 110 - a
    for e in range(1, 121):
        d = 121 - e
        c = total - a - b - d - e
        t = (a, b, c, d, e)
        if min(t) > 0 and list(t) == sorted(t) and sommes(t) == cible:
            sol.append(t)
print("=== Les cinq bottes ===")
print("  somme des dix pesees = %d, soit %d livres pour les cinq bottes"
      % (sum(PESEES), total))
print("  solutions trouvees : %d  ->  %s" % (len(sol), sol))
print("  une seule : l'appariement des pesees est bien INUTILE a connaitre.")

# contrôle indépendant, en fractions, sans supposer les poids entiers
P = sorted(Fraction(x) for x in PESEES)
C = sum(P)/4 - (P[0] + P[-1]); A = P[1] - C; B = P[0] - A
E = P[-2] - C; D = P[-1] - E
assert sommes([A, B, C, D, E]) == tuple(P)
print("  sans supposer les poids entiers :", [int(x) for x in (A, B, C, D, E)])

# ═══ 2. cela vaut-il pour tout nombre de bottes ? ═══════════════════════
def ambigus(n, borne):
    vu = {}
    for t in combinations(range(borne + 1), n):
        vu.setdefault(sommes(t), []).append(t)
    return [v for v in vu.values() if len(v) > 1]

print()
print("=== Le detecteur, eprouve sur un temoin ===")
ta, tb = (1, 4, 6, 7), (2, 3, 5, 8)
print("  temoin connu, n = 4 :", ta, "et", tb)
print("     sommes deux a deux :", sommes(ta))
print("                        ", sommes(tb), " -> identiques :",
      sommes(ta) == sommes(tb))
print()
print("  balayage de tous les ensembles de poids distincts pris dans 0..15 :")
for n in range(2, 9):
    b = 20 if n < 4 else 15
    amb = ambigus(n, b)
    ex = ("   ex. %s / %s" % (amb[0][0], amb[0][1])) if amb else ""
    print("    n = %d (0..%d) : %5d couple(s) ambigu(s)%s" % (n, b, len(amb), ex))
print("  -> l'ambiguite frappe n = 2, 4 et 8, et elles seules : les puissances")
print("     de deux. Theoreme de Selfridge et Straus (1958).")
print("  -> avec QUATRE bottes, Hodge aurait pu rendre son maitre perplexe.")

# ═══ 3. Hodge en a-t-il trop fait ? ════════════════════════════════════
paires = list(combinations(range(5), 2))
def determine(s):
    M = [[Fraction(1 if k in (i, j) else 0) for k in range(5)] for i, j in s]
    lig = col = rang = 0
    while lig < len(M) and col < 5:
        k = next((r for r in range(lig, len(M)) if M[r][col]), None)
        if k is None: col += 1; continue
        M[lig], M[k] = M[k], M[lig]
        M[lig] = [x / M[lig][col] for x in M[lig]]
        for r in range(len(M)):
            if r != lig and M[r][col]:
                f = M[r][col]; M[r] = [x - f*y for x, y in zip(M[r], M[lig])]
        rang += 1; lig += 1; col += 1
    return rang == 5
def connexe_et_impair(s):
    adj = {i: [] for i in range(5)}
    for i, j in s: adj[i].append(j); adj[j].append(i)
    coul = {0: 0}; pile = [0]; biparti = True
    while pile:
        v = pile.pop()
        for w in adj[v]:
            if w not in coul: coul[w] = 1 - coul[v]; pile.append(w)
            elif coul[w] == coul[v]: biparti = False
    return len(coul) == 5 and not biparti

tous = list(combinations(paires, 5))
bons = [s for s in tous if determine(s)]
print()
print("=== Cinq pesees auraient-elles suffi ? ===")
print("  facons de choisir 5 pesees parmi les 10 : %d" % len(tous))
print("  celles qui determinent les cinq poids   : %d" % len(bons))
print("  celles dont le graphe est connexe et non biparti : %d"
      % sum(1 for s in tous if connexe_et_impair(s)))
print("  les deux criteres coincident sur les %d cas :" % len(tous),
      all(determine(s) == connexe_et_impair(s) for s in tous))
print("  -> cinq pesees suffisent si les paires relient toutes les bottes et")
print("     referment un cycle de longueur IMPAIRE.")
print("  exemple qui marche :", bons[0])
print("  exemple qui echoue :", next(s for s in tous if not determine(s)))

# un échec plus instructif : toutes les bottes reliées, mais cycle PAIR
def connexe(s):
    adj = {i: [] for i in range(5)}
    for i, j in s: adj[i].append(j); adj[j].append(i)
    vus = {0}; pile = [0]
    while pile:
        v = pile.pop()
        for w in adj[v]:
            if w not in vus: vus.add(w); pile.append(w)
    return len(vus) == 5
ex = next(s for s in tous if connexe(s) and not determine(s))
print("  echec malgre la connexite (cycle pair) :", ex)
print("     -> dans ce cas on peut ajouter t a deux bottes et le retirer aux")
print("        trois autres sans changer aucune des cinq pesees.")

# ═══ 4. les dix pesees forment-elles un code correcteur ? ═══════════════
# Cinq inconnues, dix equations : cinq redondances. Si Hodge se trompe d'un
# chiffre, s'en apercoit-on ?
def reconstructible(liste):
    s = sorted(liste)
    if sum(s) % 4: return False
    T = sum(s)//4
    C = T - (s[0] + s[-1]); A = s[1] - C; B = s[0] - A
    E = s[-2] - C; D = s[-1] - E
    t = sorted((A, B, C, D, E))
    return min(t) > 0 and sommes(t) == tuple(s)

assert reconstructible(PESEES)                 # les vraies pesees doivent passer
detecte_somme = detecte_total = essais = 0
passees = []
for i in range(10):
    for delta in (-4, -3, -2, -1, 1, 2, 3, 4):
        faux = list(PESEES); faux[i] += delta
        essais += 1
        if sum(faux) % 4: detecte_somme += 1
        if not reconstructible(faux): detecte_total += 1
        else: passees.append((PESEES[i], faux[i], faux))
print()
print("=== Une erreur de Hodge passerait-elle inapercue ? ===")
print("  erreurs simulees (une pesee faussee de 1 a 4 livres) : %d" % essais)
print("  reperees par le seul test de divisibilite par 4      : %d" % detecte_somme)
print("  reperees par la reconstruction complete              : %d" % detecte_total)
print("  -> les dix pesees se controlent les unes les autres : cinq equations")
print("     de trop, donc cinq garde-fous.")
for vrai, lu, faux in passees:
    s = sorted(faux); T = sum(s)//4
    C = T - (s[0] + s[-1]); A = s[1] - C; B = s[0] - A; E = s[-2] - C; D = s[-1] - E
    print("  la seule qui passe : %d lu %d -> faux poids %s, parfaitement coherents"
          % (vrai, lu, sorted((A, B, C, D, E))))
