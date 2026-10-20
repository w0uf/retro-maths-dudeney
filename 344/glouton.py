"""recherche pondérée (A* avec f = g + w·h) : donne des solutions valides, pas forcément minimales"""
import heapq, json, sys
B = json.load(open("chaines.json"))
man = [[abs(a//5-b//5)+abs(a%5-b%5) for b in range(25)] for a in range(25)]
nb = [[b for b in range(25) if man[a][b]==1] for a in range(25)]
def cherche(ch, w, cap=1_500_000):
    but = [None] + [k-1 for k in ch]
    s0 = bytes([c+1 if c < 20 else 0 for c in range(25)])
    h0 = sum(man[d-1][but[d]] for d in range(1, 21))
    g = {s0: 0}; par = {s0: None}; tas = [(w*h0, 0, h0, s0)]
    while tas and len(g) < cap:
        f, gg, h, s = heapq.heappop(tas)
        if gg > g[s]: continue
        if h == 0:
            L = []; 
            while par[s]: s, m = par[s]; L.append(m)
            return gg, L[::-1]
        for v in range(25):
            if s[v]: continue
            for c in nb[v]:
                d = s[c]
                if not d: continue
                t = bytearray(s); t[v] = d; t[c] = 0; t = bytes(t)
                if gg+1 < g.get(t, 999):
                    nh = h - man[c][but[d]] + man[v][but[d]]
                    g[t] = gg+1; par[t] = (s, "%d-%d" % (d, v+1)); heapq.heappush(tas, (gg+1+w*nh, gg+1, nh, t))
    return None, None
w = float(sys.argv[1]); best = {}
for b, ch in B:
    if b >= 46: break
    n, L = cherche(ch, w)
    print(b, n, ch, flush=True)
    if n: best[tuple(ch)] = (n, L)
json.dump({" ".join(map(str,k)): v for k, v in best.items()}, open("glouton_%s.json" % sys.argv[1], "w"))
