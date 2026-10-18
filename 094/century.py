#!/usr/bin/env python3
"""n° 94 THE DIGITAL CENTURY — Dudeney 1917.
Placer des signes entre 1 2 3 4 5 6 7 8 9 (dans cet ordre) pour faire 100.
Minimiser (1) le nombre de signes, (2) le nombre de traits de plume :
+ et x valent 2 traits, - vaut 1, ÷ vaut 3. Le « collage » de deux chiffres
ne coute rien. Recensement complet des 5^8 = 390 625 combinaisons."""
from fractions import Fraction as F
from itertools import product

OPS = {"": (0, 0), "+": (1, 2), "-": (1, 1), "*": (1, 2), "/": (1, 3)}
TRAIT = {"+": "+", "-": "−", "*": "×", "/": "÷", "": ""}

def evalue(expr):
    try:
        return eval(expr, {"__builtins__": {}}, {"F": F})
    except ZeroDivisionError:
        return None

def joli(choix):
    s = "1"
    for i, o in enumerate(choix, 2):
        s += TRAIT[o] + str(i)
    return s

sols = []
for choix in product(OPS, repeat=8):
    # on construit l'expression avec des Fractions pour les divisions
    morceaux = ["F(1)"]
    for i, o in enumerate(choix, 2):
        if o == "": morceaux[-1] = morceaux[-1][:-1] + str(i) + ")" if morceaux[-1].startswith("F(") and morceaux[-1].endswith(")") else morceaux[-1] + str(i)
        else: morceaux.append(o); morceaux.append("F(%d)" % i)
    expr = "".join(morceaux)
    v = evalue(expr)
    if v == 100:
        signes = sum(OPS[o][0] for o in choix)
        traits = sum(OPS[o][1] for o in choix)
        sols.append((signes, traits, joli(choix)))
print("expressions valant 100 :", len(sols))
sols.sort()
print("\nminimum de signes :", sols[0][0])
mini = [s for s in sols if s[0] == sols[0][0]]
print("   solutions à ce nombre de signes :", len(mini))
for s in sorted(mini, key=lambda x: x[1]):
    print("      %s   (%d signes, %d traits)" % (s[2], s[0], s[1]))
print("\npar nombre de signes :")
from collections import Counter
c = Counter(s[0] for s in sols)
for k in sorted(c): print("   %d signes : %d solutions" % (k, c[k]))

# témoins : la solution de Dudeney doit être trouvée ; la ligne fautive de la transcription Gutenberg ne vaut pas 100
assert any(s[2] == "123−45−67+89" for s in sols)
print("\nla ligne « 123 + 4 − 5 + 67 − 8 − 9 » de la transcription vaut", 123 + 4 - 5 + 67 - 8 - 9, "; la vraie ligne « 123 + 4 − 5 + 67 − 89 » vaut", 123 + 4 - 5 + 67 - 89)
