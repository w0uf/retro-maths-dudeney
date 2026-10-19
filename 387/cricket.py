# -*- coding: utf-8 -*-
"""n° 387 THE VILLAGE CRICKET MATCH.
Quatre courses apparemment completes, mais les arbitres crient « trois courtes »
a chaque bout. Combien marque Mr. Dumkins ? Puis Luffey et Struggles : trois
courses, « deux courtes » a chaque bout. Dudeney repond par deux schemas.
On essaie toutes les facons de repartir les arrivees bonnes et courtes.
    python3 cricket.py"""
import itertools

def course(trajets, courts_par_bout, finir_en_place=True):
    """Deux batteurs, A part du bout 0, B du bout 1 ; chacun fait `trajets` allers simples.
    Chaque arrivée à un bout est « bonne » (le batteur pose sa batte dans le pli) ou « courte ».
    Les arbitres annoncent `courts_par_bout` arrivées courtes à chaque bout.
    Renvoie l'ensemble des issues : (A a-t-il jamais touché le pli d'en face, B idem, A et B ont-ils échangé leurs places)."""
    arrivees = []                                         # (batteur, numéro du trajet, bout d'arrivée)
    for t in range(1, trajets + 1):
        arrivees.append(("A", t, t % 2)); arrivees.append(("B", t, 1 - t % 2))
    issues = set(); cas = 0
    for bonnes in itertools.product((True, False), repeat=len(arrivees)):
        courts = [sum(1 for (b, t, bout), ok in zip(arrivees, bonnes) if bout == x and not ok) for x in (0, 1)]
        if courts != [courts_par_bout, courts_par_bout]: continue
        if finir_en_place and not all(ok for (b, t, bout), ok in zip(arrivees, bonnes) if t == trajets): continue
        cas += 1
        pli = {"A": 0, "B": 1}; face = {"A": False, "B": False}
        for (b, t, bout), ok in zip(arrivees, bonnes):
            if ok:
                pli[b] = bout
                if bout != {"A": 0, "B": 1}[b]: face[b] = True
        issues.add((face["A"], face["B"], pli["A"] == 1 and pli["B"] == 0))
    return cas, issues
def montre(nom, r):
    cas, issues = r
    print("%s : %d facon(s) de courir" % (nom, cas))
    for a, b, ech in sorted(issues):
        print("      %s a touche le pli d'en face : %-5s | l'autre : %-5s | ils ont change de bout : %s"
              % ("le premier", a, b, ech))
    return r

print("Issues : (le premier batteur a-t-il touche le pli d'en face, le second, ont-ils change de bout ?)\n")
r1 = montre("Dumkins et Podder, 4 courses, 3 courtes a chaque bout, chacun finit dans un pli", course(4, 3))
r2 = montre("Luffey et Struggles, 3 courses, 2 courtes a chaque bout, chacun finit dans un pli", course(3, 2))
print()
s1 = montre("Dumkins et Podder, sans exiger qu'ils finissent dans un pli", course(4, 3, False))
s2 = montre("Luffey et Struggles, sans exiger qu'ils finissent dans un pli", course(3, 2, False))
assert r1 == (1, {(False, False, False)}) and r2 == (1, {(True, True, True)})
assert s1[0] == 16 and s2[0] == 9 and len(s1[1]) > 1 and len(s2[1]) > 1
print("\nDudeney : Dumkins ne marque rien, Struggles marque un point. Avec l'hypothese")
print("muette (chacun finit dans un pli), ce sont les seules issues ; sans elle, rien n'est force.")

# temoins : sans aucune course courte, 4 allers simples ramenent chacun chez soi,
# 3 allers simples les font changer de bout
t4, t3 = course(4, 0), course(3, 0)
print("temoin, 4 courses sans courte :", t4, "; 3 courses sans courte :", t3)
assert t4 == (1, {(True, True, False)}) and t3 == (1, {(True, True, True)})

