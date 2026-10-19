# -*- coding: utf-8 -*-
"""n° 390 THE HORSE-RACE PUZZLE — trois chevaux, cotes de 4 contre 1, 3 contre 1
et 2 contre 1. Combien miser sur chacun pour gagner 13 livres quel que soit le
vainqueur ?"""
from fractions import Fraction as F

COTES = {"Acorn": 4, "Bluebottle": 3, "Capsule": 2}
GAIN = F(13)

# ── le témoin : l'exemple de l'énoncé, 5 livres sur chaque ──────────────
print("l'exemple de l'énoncé — 5 livres sur chacun :")
mises = {c: F(5) for c in COTES}
for gagnant in COTES:
    g = COTES[gagnant]*mises[gagnant] - sum(m for c, m in mises.items() if c != gagnant)
    print("   si %-11s gagne : %+d livre(s)" % (gagnant, g))

# ── le système ─────────────────────────────────────────────────────────
# mise a sur une cote de k contre 1 : si ce cheval gagne, on empoche k·a et
# l'on perd les autres mises. On veut le même gain G pour les trois.
# k·a - (S - a) = G, donc (k+1)·a = S + G : a = (S+G)/(k+1).
# en sommant : (S+G)·Σ 1/(k+1) = S
somme_inv = sum(F(1, k+1) for k in COTES.values())
S = GAIN*somme_inv/(1 - somme_inv)
print()
print("somme des 1/(cote+1) :", somme_inv, "=", float(somme_inv))
print("mise totale S =", S, "livres")
mises = {c: (S+GAIN)/(k+1) for c, k in COTES.items()}
print()
for c, m in mises.items(): print("   %-11s : %s livres" % (c, m))
print("   total misé :", sum(mises.values()), "livres")
print()
for gagnant in COTES:
    g = COTES[gagnant]*mises[gagnant] - sum(m for c, m in mises.items() if c != gagnant)
    print("   si %-11s gagne : %+s livres" % (gagnant, g))
print("Dudeney : 12 sur Acorn, 15 sur Bluebottle, 20 sur Capsule →",
      mises == {"Acorn": F(12), "Bluebottle": F(15), "Capsule": F(20)})

# ── pourquoi ça marche, et pourquoi ça n'arrive jamais ─────────────────
print()
print("les cotes correspondent à des probabilités implicites :")
for c, k in COTES.items(): print("   %-11s : 1/%d = %.4f" % (c, k+1, 1/(k+1)))
print("   leur somme :", somme_inv, "=", "%.4f" % float(somme_inv),
      "→ inférieure à 1 : le pari sûr existe.")
print()
print("chez un vrai bookmaker, la somme atteint ou dépasse 1 — c'est sa marge :")
exemples = (("cotes de Dudeney",      (F(4), F(3), F(2))),
            ("livre exactement juste", (F(1), F(2), F(5))),
            ("livre avec 10 % de marge", (F(1,10)*F(100,55)-1+F(1), None, None)))
def montre(nom, cotes):
    s = sum(F(1)/(k+1) for k in cotes)
    if s >= 1:
        reste = "aucun pari sûr : la marge est pour le bookmaker"
        if s == 1: reste = "gain garanti exactement nul : le livre est juste"
        print("   %-26s somme = %.4f → %s" % (nom, float(s), reste))
    else:
        tot = GAIN*s/(1-s)
        print("   %-26s somme = %.4f → pari sûr, %.2f misés pour gagner 13"
              % (nom, float(s), float(tot)))
montre("cotes de Dudeney", (F(4), F(3), F(2)))
montre("livre exactement juste", (F(1), F(2), F(5)))
# marge de 10 % : on majore les probabilités implicites de 10 %
p = [F(11,20), F(11,30), F(11,60)]      # 1,1 x (1/2, 1/3, 1/6), somme 1,1
montre("livre avec 10 % de marge", [1/x - 1 for x in p])
print()
print("→ le pari sûr n'existe que si la somme des probabilités implicites est")
print("   INFÉRIEURE à 1. Les cotes de Dudeney sont donc celles d'un bookmaker")
print("   imaginaire, qui perdrait à coup sûr — aucun n'en offre de pareilles.")

# ── témoins ─────────────────────────────────────────────────────────────
def issues(m):
    return [COTES[g]*m[g] - sum(x for c, x in m.items() if c != g) for g in COTES]
fausses = {"Acorn": F(12), "Bluebottle": F(15), "Capsule": F(21)}
print()
print("témoin : 12 / 15 / 21 donne", [str(x) for x in issues(fausses)], "-> refusé (gains inégaux)")
print("témoin : 5 sur chacun donne", [str(x) for x in issues({c: F(5) for c in COTES})])
assert issues(mises) == [13, 13, 13] and len(set(issues(fausses))) > 1
assert issues({c: F(5) for c in COTES}) == [10, 5, 0] and S == 47 and somme_inv == F(47, 60)
