#!/usr/bin/env python3
"""N° 244 : contrôle de verif_244.c sur les petits cas, par une recherche Python sans aucun élagage.
Pour 0 à 8 tournants, compare le maximum et le nombre de trajets qui l'atteignent.
    gcc -O2 -o verif_244 verif_244.c && python3 controle_petits.py"""
import collections, os, subprocess

def tous(t):
    """Longueurs de tous les trajets de t tournants au plus (un trajet = une suite de segments)."""
    out = collections.Counter()
    def dfs(c, r, horiz, reste, total, routes):
        out[total] += 1
        if not reste: return
        for s in (-1, 1):
            q, l, pris = (c if horiz else r), 0, []
            while True:
                q += s; l += 1
                if not 0 <= q <= 7: break
                a, b = ((q - s, r), (q, r)) if horiz else ((c, q - s), (c, q))
                e = frozenset((a, b))
                if e in routes: break
                pris.append(e)
                dfs(b[0], b[1], not horiz, reste - 1, total + l, routes | set(pris))
    dfs(0, 4, True, t + 1, 0, frozenset()); dfs(0, 4, False, t + 1, 0, frozenset())
    del out[0]
    return out

ici = os.path.dirname(os.path.abspath(__file__))
for t in range(9):
    py = tous(t); m = max(py)
    c = subprocess.run([os.path.join(ici, "verif_244"), str(t), str(m)], capture_output=True, text=True).stdout
    cmax = int(c.split("maximum")[1].split(";")[0]); cnb = int(c.split("longueur %d :" % m)[1].split()[0])
    print("%2d tournants : Python max %d (%d trajets) ; C max %d (%d trajets) %s" % (t, m, py[m], cmax, cnb, "OK" if (m, py[m]) == (cmax, cnb) else "DIFFÉRENT"))
