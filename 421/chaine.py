"""Rétro Math's — n° 421 A CHAIN PUZZLE (Dudeney, 1917).
Neuf tronçons (7, 8, 6, 3, 4, 5, 6, 5, 6 maillons) à réunir en une chaîne fermée ; ouvrir et refermer un maillon
coûte trois pence, une chaîne neuve en coûte 26. Combien de maillons ouvrir au minimum ? Énumération complète
par tronçon, puis programmation dynamique.
    python3 chaine421.py   (instantané)"""
from itertools import combinations
T=[7,8,6,3,4,5,6,5,6]; assert sum(T)==50
def fragments(L, ouverts):
    """nombre de bouts fermés restant quand on ouvre l'ensemble `ouverts` d'un tronçon de L maillons"""
    n=0; dans=False
    for i in range(L):
        if i in ouverts: dans=False
        elif not dans: n+=1; dans=True
    return n
# pour chaque tronçon : j maillons ouverts -> minimum de fragments restants (énumération complète)
def profil(L):
    return [min(fragments(L,set(c)) for c in combinations(range(L),j)) for j in range(L+1)]
# programmation dynamique : best[k] = min de fragments avec k maillons ouverts en tout
best={0:0}; voies={0:[[]]}
for L in T:
    p=profil(L); nb={}; nv={}
    for k,f in best.items():
        for j,g in enumerate(p):
            t=(f+g)
            if k+j not in nb or t<nb[k+j]: nb[k+j]=t; nv[k+j]=[v+[j] for v in voies[k]]
            elif t==nb[k+j]: nv[k+j]+= [v+[j] for v in voies[k]]
    best=nb; voies=nv
for k in range(4,11): print(k,"ouverts -> au mieux",best[k],"fragments", "FAISABLE" if best[k]<=k else "")
kmin=min(k for k in best if best[k]<=k); print("minimum",kmin,"maillons =",3*kmin,"d")
print("répartitions optimales (maillons ouverts par tronçon, longueurs",T,"):")
for v in voies[kmin]: print("  ",v)
print("naïf",27,"d ; tronçon de 8 :",3*8,"d, fragments restants",8)

# --- ce que dit le commentaire (et le corrigé)
assert kmin == 7 and 3 * kmin == 21 and voies[7] == [[0, 0, 0, 3, 4, 0, 0, 0, 0]]   # ouvrir les tronçons de 3 et de 4 : 1 s. 9 d.
assert 9 * 3 == 27 > 26                                                           # la méthode naïve coûte plus qu'une chaîne neuve
assert best[6] > 6                                                                 # six ne suffisent pas
# témoin : ouvrir les 8 maillons du tronçon de 8 laisse 8 bouts à relier, avec 8 maillons : faisable, mais 24 d.
assert fragments(8, set(range(8))) == 0 and sum(1 for L in T if L != 8) == 8
print("contrôles : tout est conforme (témoins refusés)")
