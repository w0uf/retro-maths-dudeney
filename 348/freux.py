#!/usr/bin/env python3
"""Rétro Math's — n° 348 THE ROOKERY (Dudeney, 1917). Huit tours numérotées dans un carré 3×3 (c3-e5),
centre vide ; roi noir d7, fou noir d6. Mater avec la tour 8, les autres en ordre numérique autour du carré,
la coupure entre 1 et 7.
Demande python-chess (pip install chess).
    python3 freux.py   (instantané)"""
import chess
from collections import deque
CASES = [(r, c) for r in range(3) for c in range(3)]             # (0,0) = c5 … (2,2) = e3
nom = lambda rc: "cde"[rc[1]] + str(5 - rc[0])
print("=== par où la tour 8 peut-elle mater en quittant le carré ?")
sorties = []
for vide in CASES:
    for p in CASES:
        if p == vide: continue
        b = chess.Board(None)
        b.set_piece_at(chess.D7, chess.Piece.from_symbol('k')); b.set_piece_at(chess.D6, chess.Piece.from_symbol('b'))
        b.set_piece_at(chess.A1, chess.Piece.from_symbol('K'))
        for x in CASES:
            if x != vide: b.set_piece_at(chess.parse_square(nom(x)), chess.Piece.from_symbol('R'))
        b.turn = chess.WHITE
        dedans = {chess.parse_square(nom(x)) for x in CASES}
        for m in b.legal_moves:
            if m.from_square == chess.parse_square(nom(p)) and m.to_square not in dedans:
                b.push(m)
                if b.is_checkmate(): sorties.append((nom(p), nom(vide), chess.square_name(m.to_square)))
                b.pop()
print("(case de la tour 8, case vide, case d'arrivée) :", sorties)

print("=== le taquin")
ANNEAU = [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0),(1,0)]       # sens des aiguilles d'une montre depuis c5
depart = {(0,0):2,(0,1):3,(0,2):4,(1,2):5,(2,2):6,(2,1):7,(2,0):8,(1,0):1,(1,1):0}
cle = lambda d: tuple(d[x] for x in CASES)
def voisins(t):
    i = t.index(0); r, c = divmod(i, 3)
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        x, y = r+dr, c+dc
        if 0 <= x < 3 and 0 <= y < 3:
            j = x*3+y; l = list(t); l[i], l[j] = l[j], l[i]; yield tuple(l), t[j]
s0 = cle(depart); dist = {s0: 0}; nb = {s0: 1}; q = deque([s0])
while q:
    u = q.popleft()
    for v, _ in voisins(u):
        if v not in dist: dist[v] = dist[u] + 1; nb[v] = 0; q.append(v)
        if dist[v] == dist[u] + 1: nb[v] += nb[u]
print("positions atteignables :", len(dist), "| la plus lointaine :", max(dist.values()))
def cible(sens):                      # tour 8 en d5 (0,1), centre vide, 1..7 autour
    d = {(1,1): 0, (0,1): 8}; k = ANNEAU.index((0,1))
    autres = [ANNEAU[(k + i) % 8] for i in range(1, 8)]            # dans le sens des aiguilles après d5
    for i, x in enumerate(autres): d[x] = (i + 1) if sens == 'horaire' else (7 - i)
    return cle(d)
for sens in ('horaire', 'antihoraire'):
    t = cible(sens); print("ordre", sens, ":", t, "→", ("%d glissements, %d solutions minimales" % (dist[t], nb[t])) if t in dist else "INACCESSIBLE")
# sa suite
seq = [5,6,7,5,6,4,3,6,4,7,5,4,7,3,6,7,3,5,4,3,1,8,3,4,5,6,7,1,8,2,1]
t = s0; ok = True
for n in seq:
    nxt = [v for v, m in voisins(t) if m == n]
    if not nxt: ok = False; print("coup impossible :", n); break
    t = nxt[0]
print("sa suite :", len(seq), "glissements + la prise = ", len(seq)+1, "coups ; valide :", ok, "| position atteinte :", t, "| = cible antihoraire :", t == cible('antihoraire'), "horaire :", t == cible('horaire'))

print("=== la cible de Dudeney (tour 8 au centre, d5 vide) et la cible « tour 8 en d5 »")
cD = (1, 0, 7, 2, 8, 6, 3, 4, 5); cA = cible('antihoraire')
print("cible de Dudeney :", dist[cD], "glissements au minimum,", nb[cD], "solutions minimales")
print("tour 8 en d5     :", dist[cA], "glissements au minimum,", nb[cA], "solutions minimales")
def chemin(t):
    out = []
    while dist[t]:
        for v, m in voisins(t):
            if dist.get(v) == dist[t] - 1: out.append(m); t = v; break
    return out[::-1]
def toutes(t):
    if dist[t] == 0: return [[]]
    res = []
    for v, m in voisins(t):
        if dist.get(v) == dist[t] - 1: res += [p + [m] for p in toutes(v)]
    return res
for p in toutes(cA): print("   ", ' '.join(map(str, p)))
# contrôle indépendant : rejouer sur un vrai échiquier, coup légal par coup légal, puis la prise
def rejoue(seq, finale):
    b = chess.Board(None)
    b.set_piece_at(chess.D7, chess.Piece.from_symbol('k')); b.set_piece_at(chess.D6, chess.Piece.from_symbol('b'))
    pos = {n: chess.parse_square(nom(x)) for x, n in depart.items() if n}
    for sqr in pos.values(): b.set_piece_at(sqr, chess.Piece.from_symbol('R'))
    dedans = {chess.parse_square(nom(x)) for x in CASES}
    for n in seq:
        b.turn = chess.WHITE
        coups = [m for m in b.legal_moves if m.from_square == pos[n] and m.to_square in dedans]
        assert len(coups) == 1, (n, coups)
        b.push(coups[0]); pos[n] = coups[0].to_square
    b.turn = chess.WHITE
    m = chess.Move(pos[8], chess.D6); assert m in b.legal_moves
    b.push(m)
    return b.is_checkmate(), {n: chess.square_name(s) for n, s in sorted(pos.items())}
for nomseq, s in (("Dudeney", seq), ("29 coups", toutes(cA)[0])):
    mat, pos = rejoue(s, None); print(nomseq, ":", len(s) + 1, "coups, mat :", mat, "| tours :", pos)

print("=== parties complètes, coups noirs compris (les Noirs n'ont-ils vraiment jamais le choix ?)")
def partie(seq):
    b = chess.Board(None)
    b.set_piece_at(chess.D7, chess.Piece.from_symbol('k')); b.set_piece_at(chess.D6, chess.Piece.from_symbol('b'))
    pos = {n: chess.parse_square(nom(x)) for x, n in depart.items() if n}
    for sqr in pos.values(): b.set_piece_at(sqr, chess.Piece.from_symbol('R'))
    b.turn = chess.WHITE; dedans = {chess.parse_square(nom(x)) for x in CASES}; choix_noirs = []
    for n in seq:
        coups = [m for m in b.legal_moves if m.from_square == pos[n] and m.to_square in dedans]
        assert len(coups) == 1, (n, coups)
        b.push(coups[0]); pos[n] = coups[0].to_square
        assert not b.is_check()
        rep = list(b.legal_moves); choix_noirs.append(len(rep)); b.push(rep[0])
    m = chess.Move(pos[8], chess.D6); assert m in b.legal_moves
    b.push(m)
    return len(seq) + 1, b.is_checkmate(), chess.square_name(b.king(chess.BLACK)), set(choix_noirs), b.fen()
for nomseq, s in (("Dudeney, 32 coups", seq), ("tour 8 par d5, 29 coups", toutes(cA)[0]), ("tour 8 par le centre, 28 coups", toutes(cD)[0])):
    n, mat, roi, choix, fen = partie(s)
    print(nomseq, "→", n, "coups blancs, mat :", mat, "| roi noir en", roi, "| nombre de coups noirs possibles à chaque tour :", choix)
    print("     ", ' '.join(map(str, s)), "| position finale :", fen)

print("=== son affirmation sur le sens de rotation, et la statistique des coups")
cDh = (7, 0, 1, 6, 8, 2, 5, 4, 3)        # tour 8 au centre, d5 vide, ordre NON inversé (sens d'origine)
print("même cible avec les tours dans le sens d'origine :", "atteignable en %d" % dist[cDh] if cDh in dist else "INACCESSIBLE")
from collections import Counter
print("coups par tour, Dudeney :", sorted(Counter(seq).items()))
print("coups par tour, 28 coups :", sorted(Counter(toutes(cD)[0]).items()))

# --- ce que dit l'article
assert len(dist) == 181440 and max(dist.values()) == 30
n, mat, roi, choix, fen = partie(seq)
assert (n, mat, choix) == (32, True, {1})                          # sa partie : valide, Noirs sans choix
assert dist[cD] == 27 and nb[cD] == 1                              # 🏆 sa position finale en 27 glissements : mat en 28
SOL28 = [7, 8, 1, 7, 5, 6, 8, 5, 3, 4, 6, 8, 5, 3, 4, 2, 7, 1, 3, 4, 2, 7, 1, 2, 8, 6, 7]
assert toutes(cD) == [SOL28]
n28, mat28, _, choix28, fen28 = partie(SOL28)
assert (n28, mat28, choix28) == (28, True, {1}) and fen28.split()[0] == fen.split()[0]   # meme position finale que la sienne
assert dist[cA] == 28 and nb[cA] == 2 and cDh not in dist             # variante en 29 ; sens d'origine inaccessible
# temoins : un glissement impossible (la tour 4, en coin, ne touche pas la case vide au depart) et sa suite privee d'un coup sont refuses
for faux in ([4] + seq[1:], seq[:-1]):
    try: partie(faux); raise SystemExit("ERREUR : suite fausse acceptee")
    except AssertionError: pass
print("controles : tout est conforme (temoins refuses)")
