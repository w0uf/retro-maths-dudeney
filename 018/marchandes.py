# -*- coding: utf-8 -*-
"""n° 18 THE MARKET WOMEN.
Des marchandes recoivent chacune la meme somme, a des prix a la livre tous
differents (en farthings entiers), pour des poids en livres entieres. Combien
pouvaient-elles etre ? Le nombre de marchandes est le nombre de diviseurs de la
recette exprimee en farthings (prix x poids = recette).
L'edition imprimee de 1917 donne une recette de 2 s. 2 1/4 d. ; la transcription
de Project Gutenberg donne 2 s. 2 1/2 d., et avec elle le corrige ne tient plus.
    python3 marchandes.py"""

def diviseurs(n): return [d for d in range(1, n + 1) if n % d == 0]
def farthings(s, d, quarts): return 4 * (12 * s + d) + quarts       # 1 s. = 12 d., 1 d. = 4 farthings

assert diviseurs(12) == [1, 2, 3, 4, 6, 12] and diviseurs(13) == [1, 13]      # temoins

imprime, gutenberg = farthings(2, 2, 1), farthings(2, 2, 2)
for nom, f in (("2 s. 2 1/4 d. (edition de 1917)", imprime), ("2 s. 2 1/2 d. (Gutenberg)", gutenberg)):
    print("%-34s = %d farthings ; diviseurs %s -> %d marchandes" % (nom, f, diviseurs(f), len(diviseurs(f))))
assert imprime == 105 and len(diviseurs(imprime)) == 8
assert gutenberg == 106 and len(diviseurs(gutenberg)) == 4

# poids en demi-livres ou en quarts de livre : poids = k/2 (ou k/4), prix = 2R/k (ou 4R/k) farthings entiers
print("\nsi l'on vend aussi des demi-livres : %d marchandes ; des quarts de livre : %d"
      % (len(diviseurs(2 * imprime)), len(diviseurs(4 * imprime))))
assert len(diviseurs(2 * imprime)) == 16 and len(diviseurs(4 * imprime)) == 24

tranche = {f: len(diviseurs(f)) for f in range(farthings(2, 0, 0), farthings(2, 6, 0) + 1)}
print("recettes de 2 s. a 2 s. 6 d. : de %d a %d marchandes ; le maximum, %d, pour %d farthings (2 s. 6 d.)"
      % (min(tranche.values()), max(tranche.values()), max(tranche.values()), max(tranche, key=tranche.get)))
assert min(tranche.values()) == 2 and max(tranche.values()) == 16 and max(tranche, key=tranche.get) == 120
impair = [f for f in tranche if tranche[f] % 2]
print("recettes a nombre impair de marchandes (une vend autant de livres que son prix) :", impair)
