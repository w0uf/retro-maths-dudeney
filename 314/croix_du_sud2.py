#!/usr/bin/env python3
"""n° 314, suite : cinq planètes suffisent-elles sur des carrés plus grands ?
Rend le premier exemple trouvé, ou 0 après une recherche complète.
    python3 croix_du_sud2.py            (côtés 9 à 12, environ 35 s)
    python3 croix_du_sud2.py 13 14      (d'autres côtés)"""
import sys, time
def essai(N, compter=False):
    TOUT = (1 << N*N) - 1; n = N*N
    lig = lambda a, b: a[0]==b[0] or a[1]==b[1] or abs(a[0]-b[0])==abs(a[1]-b[1])
    C = [divmod(i, N) for i in range(n)]
    COUV = [sum(1 << j for j in range(n) if lig(C[i], C[j])) for i in range(n)]
    nb = 0; t0 = time.time()
    for a in range(n):
        ma = COUV[a]
        for b in range(a+1, n):
            mb = ma | COUV[b]
            for c in range(b+1, n):
                mc = mb | COUV[c]
                r3 = TOUT & ~mc
                u = (r3 & -r3).bit_length() - 1          # une étoile encore libre : d ou e doit la tenir
                for d in range(c+1, n):
                    md = mc | COUV[d]
                    r = TOUT & ~md
                    if r == 0: nb += n - d - 1; continue
                    tient = COUV[d] >> u & 1
                    for e in range(d+1, n):
                        if (tient or COUV[e] >> u & 1) and not r & ~COUV[e]:
                            nb += 1
                            if not compter: return [C[x] for x in (a,b,c,d,e)], time.time()-t0
    return nb, time.time()-t0
def couvre(N, S):
    return all(any(a[0]==s[0] or a[1]==s[1] or abs(a[0]-s[0])==abs(a[1]-s[1]) for s in S) for a in [divmod(i, N) for i in range(N*N)])
R = {}
for N in map(int, sys.argv[1:] or ["9", "10", "11", "12"]):
    R[N] = essai(N)[0]; print(N, R[N], flush=True)
    if R[N]: assert couvre(N, R[N])                      # chaque exemple est recontrole independamment
if not sys.argv[1:]:
    assert R[9] and R[10] and R[11] and R[12] == 0        # cinq suffisent jusqu'a 121 etoiles, plus a 144
    # temoin : l'exemple trouve pour 11 x 11 ne couvre pas le carre de 12
    assert not couvre(12, R[11])
    print("controles : tout est conforme (temoins refuses)")
