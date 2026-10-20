"""n° 340 THE CUBIC KNIGHT'S TOUR : six échiquiers sur les faces d'un cube, 384 cases. Le cavalier passe d'une face
à l'autre en « marchant » sur la surface : deux cases droit devant puis une de côté (ou l'inverse), et une case qui
déborde d'une arête se retrouve sur la face voisine, comme si on la dépliait. On cherche un tour fermé."""
import random, sys
N = 8
def cellules():
    C = []
    for ax in range(3):
        for sg in (0, N):
            for i in range(N):
                for j in range(N):
                    p = [0, 0, 0]; p[ax] = sg; o = [a for a in range(3) if a != ax]
                    p[o[0]] = i + .5; p[o[1]] = j + .5
                    n = [0, 0, 0]; n[ax] = 1 if sg else -1
                    C.append((tuple(p), tuple(n)))
    return C
C = cellules(); idx = {c: k for k, c in enumerate(C)}
add = lambda a, b, k=1: tuple(x + k * y for x, y in zip(a, b))
def pas(p, n, d):
    """une case dans la direction d (tangente) ; renvoie la nouvelle case et les nouvelles (normale, direction)"""
    q = add(p, d)
    if all(0 < x < N for x, nx in zip(q, n) if nx == 0):
        return q, n, d
    # on franchit l'arête : nouvelle face de normale d, on avance vers -n
    q = add(add(p, d, .5), n, -.5)
    return q, d, tuple(-x for x in n)
def tourne(n, d, e):
    return e
def sauts(k, prudent=False):
    p, n = C[k]
    tang = [t for t in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)) if sum(a*b for a, b in zip(t, n)) == 0]
    S = set()
    for d in tang:
        for e in tang:
            if sum(a*b for a, b in zip(d, e)) != 0 or d == tuple(-x for x in e): continue
            # saut « deux selon d, un selon e », par les deux chemins : d d e, et e d d
            fins = []
            for ordre in ((d, d, e), (e, d, d)):
                q, nn = p, n; dirs = list(ordre)
                for i in range(3):
                    q2, n2, nd = pas(q, nn, dirs[i])
                    if n2 != nn:     # arête franchie : les directions restantes qui pointaient selon l'ancienne… 
                        dirs = [nd if x == dirs[i] else x for x in dirs]
                    q, nn = q2, n2
                fins.append(idx[(tuple(round(x * 2) / 2 for x in q), nn)])
            if prudent:
                if fins[0] == fins[1]: S.add(fins[0])
            else: S.update(fins)
    S.discard(k); return sorted(S)
PRUDENT = "prudent" in sys.argv
V = [sauts(k, PRUDENT) for k in range(len(C))]
from collections import Counter
print("cases :", len(C), "| nombre de sauts par case :", sorted(Counter(len(v) for v in V).items()))
assert all(k in V[j] for k in range(len(C)) for j in V[k]), "relation non symétrique"
def warnsdorff(dep, rng):
    vu = {dep}; ch = [dep]
    while len(ch) < len(C):
        s = ch[-1]; L = [t for t in V[s] if t not in vu]
        if not L: return None
        m = min(sum(1 for u in V[t] if u not in vu) for t in L)
        t = rng.choice([t for t in L if sum(1 for u in V[t] if u not in vu) == m])
        vu.add(t); ch.append(t)
    return ch
rng = random.Random(1917)
for essai in range(1, 20001):
    ch = warnsdorff(0, rng)
    if ch and ch[0] in V[ch[-1]]:
        print("tour fermé trouvé à l'essai", essai); break
else: sys.exit("pas de tour fermé")
assert len(set(ch)) == 384 and all(ch[i+1] in V[ch[i]] for i in range(383)) and ch[0] in V[ch[-1]]
faces = [C[k][1] for k in ch]; print("changements de face le long du tour :", sum(faces[i] != faces[i-1] for i in range(384)))

# contrôle du tour et témoin : deux cases échangées au milieu du tour doivent casser la chaîne de sauts
def est_tour(T): return len(set(T)) == len(C) == len(T) and all(T[(i+1) % len(T)] in V[T[i]] for i in range(len(T)))
assert est_tour(ch)
T2 = list(ch); T2[100], T2[200] = T2[200], T2[100]
print("tour contrôlé ; témoin (deux cases échangées) refusé :", not est_tour(T2)); assert not est_tour(T2)
# sans ambiguïté aux coins (« prudent »), chaque saut est symétrique et ne dépend pas de l'ordre des branches du L
print("convention :", "sauts sans ambiguïté seulement" if PRUDENT else "les deux ordres du L")
