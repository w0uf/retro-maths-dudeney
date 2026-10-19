# -*- coding: utf-8 -*-
"""n° 385 — rejeu de la partie de 62 coups de Dudeney, dans le modele de patience.py.
Il ecrit en « macro-coups » : « 4 C up on 5 D (9) » porte le 4 de trefle avec
tout ce qui repose dessus, en 9 coups. Pour chaque macro-coup, on cherche le
plus petit nombre de coups qui produit le meme resultat, et on le compare au sien.
S'ils concordent tous, notre modele joue bien selon ses regles.
    python3 dudeney62.py"""
from collections import deque
def v(c): return int(c[0])
def key(P): return tuple(sorted(tuple(p) for p in P if p))
def voisins(P):
    for i,p in enumerate(P):
        if not p: continue
        c=p[-1]
        for k,q in enumerate(P):
            if k==i: continue
            if (q and v(q[-1])==v(c)+1) or (not q and len(p)>1):
                n=[list(x) for x in P]; n[i].pop(); n[k].append(c); yield n
def plus_court(P,but):
    b=key(but); d={key(P):0}; f=deque([P])
    while f:
        e=f.popleft()
        if key(e)==b: return d[key(e)], e
        for n in voisins(e):
            k=key(n)
            if k not in d: d[k]=d[key(e)]+1; f.append(n)
def bloc(P,c,dst):
    n=[list(x) for x in P]; i=[k for k,p in enumerate(n) if c in p][0]; h=n[i].index(c)
    s=n[i][h:]; del n[i][h:]
    if dst=="place vide": j=[k for k,p in enumerate(n) if not p][0]
    else: j=[k for k,p in enumerate(n) if p and p[-1]==dst][0]; assert v(dst)==v(c)+1
    n[j]+=s; return n
P=[["9D","8S","7D","6S","5D","4S","3D","2S","1D"],["9H","8C","7H","6C","5H","4C","3H","2C","1H"],[],[],[],[]]
# (carte, destination, nombre de coups qu'il annonce), dans l'ordre de son corrigé
DUD=[("1D","place vide",1),("2S","place vide",1),("3D","place vide",1),("2S","3D",1),("1H","2S",1),("2C","place vide",1),("1D","2C",1),("4S","place vide",1),("3H","4S",1),
("2S","3H",3),("echange",None,6),("3D","4C",1),("6S","place vide",3),("4C","5H",3),("2C","3D",3),("7D","place vide",1),("6C","7D",3),("8S","place vide",1),
("7H","8S",1),("8C","9D",1),("7H","8C",1),("8S","9H",1),("7H","8S",1),("7D","8C",5),("4C","5D",9),("6S","7H",3),("4S","5H",7)]
tot=0
for c,dst,n in DUD:
    if c=="echange":   # 5 H et 5 D échangés, puis 4 C sur 5 D
        but=[list(x) for x in P]
        i=[k for k,p in enumerate(but) if p and p[-1]=="5D"][0]; j=[k for k,p in enumerate(but) if "5H" in p][0]
        but[i][-1]="5H"; but[j][but[j].index("5H")]="5D"
    else: but=bloc(P,c,dst)
    m,P=plus_court(P,but); tot+=m
    lib = "5H et 5D echanges, puis 4C sur 5D" if c == "echange" else "%s sur %s" % (c, dst)
    print("%-36s il compte %d, le programme %d%s" % (lib, n, m, "" if m == n else "  <-- ECART"))
    assert m == n
print("total", tot, "(il annonce 62)")
assert tot == 62 and P[:2] == [["9D","8C","7D","6C","5D","4C","3D","2C","1D"], ["9H","8S","7H","6S","5H","4S","3H","2S","1H"]]
print("position finale : l'echange est fait")
