# -*- coding: utf-8 -*-
"""n° 283 THE FIFTEEN DOMINOES — Dudeney, 1917.

Les quinze dominos du jeu « double-quatre » alignes selon la regle du jeu ;
gauche-a-droite et droite-a-gauche comptent pour deux facons differentes.
Dudeney : 126 720, par le chemin 264 x 2^5 x 15.
Et il ajoute, pour le jeu complet de vingt-huit dominos : 7 959 229 931 520.
"""
import sys, time
sys.setrecursionlimit(10000)

def dominos(n):
    """les dominos de 0-0 a n-n"""
    return [(a, b) for a in range(n+1) for b in range(a, n+1)]

def aligne(n):
    """nombre d'alignements complets, en ligne droite"""
    D = dominos(n)
    total = [0]
    pris = [False]*len(D)
    def rec(k, fin):
        if k == len(D): total[0] += 1; return
        for i, (a, b) in enumerate(D):
            if pris[i]: continue
            if a == fin:
                pris[i] = True; rec(k+1, b); pris[i] = False
            if b == fin and a != b:
                pris[i] = True; rec(k+1, a); pris[i] = False
    for i, (a, b) in enumerate(D):
        pris[i] = True
        rec(1, b)
        if a != b: rec(1, a)
        pris[i] = False
    return total[0]

t0 = time.time()
for n in (2, 3, 4):
    v = aligne(n)
    print("  dominos jusqu'au double-%d (%2d pieces) : %8d alignements  (%.0f s)"
          % (n, len(dominos(n)), v, time.time()-t0), flush=True)
print("\n  Dudeney annonce 126 720 pour le double-quatre ->", aligne(4) == 126720)

# --- sa decomposition -------------------------------------------------
print("\n=== Sa decomposition : 264 x 2^5 x 15 ===")
print("  264 x 32 x 15 =", 264*32*15)
def circuits(n):
    """« routes circulaires » sur le polygone a n+1 sommets : parcours fermes
    empruntant chaque arete une fois, comptes depuis le sommet 0, avec le sens"""
    S = n+1
    aretes = [(a, b) for a in range(S) for b in range(a+1, S)]
    idx = {e: i for i, e in enumerate(aretes)}
    total = [0]
    used = [False]*len(aretes)
    def rec(k, v, depart):
        if k == len(aretes):
            if v == depart: total[0] += 1
            return
        for w in range(S):
            if w == v: continue
            e = (min(v, w), max(v, w))
            i = idx[e]
            if used[i]: continue
            used[i] = True; rec(k+1, w, depart); used[i] = False
    rec(0, 0, 0)          # depart impose au sommet 0
    return total[0]
c5 = circuits(4)
print("  circuits euleriens du pentagone au depart d'un sommet fixe :", c5)
print("  chaque circuit passe DEUX fois par ce sommet (degre 4) : il est compte deux fois")
print("  circuits distincts : %d / 2 = %d  | Dudeney annonce 264 -> %s" % (c5, c5 // 2, c5 // 2 == 264))

# temoins
print("\n=== Temoins ===")
print("  double-deux : 2 circuits du triangle x 6 coupures = 12 alignements attendus ->", aligne(2) == 12)
print("  double-trois : degres impairs, aucun alignement attendu ->", aligne(3) == 0)
print("  le faux facteur 2^7 pour le jeu complet donnerait %d, et non 7 959 229 931 520"
      % (129976320 * 2**7 * 28))
assert aligne(2) == 12 and aligne(3) == 0 and aligne(4) == 126720 and c5 == 528
assert 129976320 * 2**7 * 28 != 7959229931520
