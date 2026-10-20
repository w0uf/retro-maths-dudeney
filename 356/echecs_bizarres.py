#!/usr/bin/env python3
"""Rétro Math's — n° 356 QUEER CHESS (Dudeney, 1917). Deux tours et un cavalier blancs, roi noir seul sur une case
centrale, en échec et sans aucun coup. Essai de toutes les dispositions, puis les autres cases du roi.
Demande python-chess (pip install chess).
    python3 echecs_bizarres.py   (environ 1 min)"""
import chess
from itertools import combinations
from math import comb
print("=== 356 : deux tours et un cavalier blancs ; roi noir sur l'une des 4 cases centrales, en échec, sans aucun coup")
CENTRE = [chess.D4, chess.E4, chess.D5, chess.E5]
sols = []
for k in CENTRE:
    libres = [s for s in chess.SQUARES if s != k]
    for r1, r2 in combinations(libres, 2):
        occ = chess.BB_SQUARES[r1] | chess.BB_SQUARES[r2] | chess.BB_SQUARES[k]
        for n in libres:
            if n in (r1, r2): continue
            b = chess.Board(None); b.set_piece_at(k, chess.Piece(chess.KING, False))
            b.set_piece_at(r1, chess.Piece(chess.ROOK, True)); b.set_piece_at(r2, chess.Piece(chess.ROOK, True)); b.set_piece_at(n, chess.Piece(chess.KNIGHT, True))
            b.turn = chess.BLACK
            if b.is_check() and not any(True for _ in b.legal_moves): sols.append((k, r1, r2, n, len(b.checkers())))
nm = chess.square_name
print("positions :", len(sols))
for k, r1, r2, n, c in sols: print("   roi", nm(k), "| tours", nm(r1), nm(r2), "| cavalier", nm(n), "| pièces donnant échec :", c)
def canon(t):
    k, r1, r2, n, c = t; best = None
    for f in range(8):
        def tr(s):
            x, y = chess.square_file(s), chess.square_rank(s)
            for _ in range(f % 4): x, y = y, 7 - x
            if f >= 4: x = 7 - x
            return chess.square(x, y)
        v = (tr(k), tuple(sorted((tr(r1), tr(r2)))), tr(n))
        best = v if best is None or v < best else best
    return best
print("à symétrie près :", len({canon(t) for t in sols}))
# et ailleurs que sur les cases centrales ?
tout = 0; par_case = {}
for k in chess.SQUARES:
    if k in CENTRE: continue
    cnt = 0; libres = [s for s in chess.SQUARES if s != k]
    for r1, r2 in combinations(libres, 2):
        for n in libres:
            if n in (r1, r2): continue
            b = chess.Board(None); b.set_piece_at(k, chess.Piece(chess.KING, False))
            b.set_piece_at(r1, chess.Piece(chess.ROOK, True)); b.set_piece_at(r2, chess.Piece(chess.ROOK, True)); b.set_piece_at(n, chess.Piece(chess.KNIGHT, True))
            b.turn = chess.BLACK
            if b.is_check() and not any(True for _ in b.legal_moves): cnt += 1
    par_case[k] = cnt


# --- ce que dit l'article
assert len(sols) == 16 and all(sum(1 for t in sols if t[0] == k) == 4 for k in CENTRE)
assert len({canon(t) for t in sols}) == 2
assert all(c == 2 for *_, c in sols)                                    # toujours echec double…
for k, r1, r2, n, c in sols:                                            # …et donne par les deux tours
    b = chess.Board(None); b.set_piece_at(k, chess.Piece(chess.KING, False))
    for r in (r1, r2): b.set_piece_at(r, chess.Piece(chess.ROOK, True))
    b.set_piece_at(n, chess.Piece(chess.KNIGHT, True)); b.turn = chess.BLACK
    assert set(b.checkers()) == {r1, r2}
bord = lambda s: chess.square_file(s) in (0, 7) or chess.square_rank(s) in (0, 7)
coins = [par_case[s] for s in (chess.A1, chess.H1, chess.A8, chess.H8)]
bords = [v for s, v in par_case.items() if bord(s) and v not in coins]
interieur = [v for s, v in par_case.items() if not bord(s)]
print("coins :", set(coins), "| bords :", min(bords), "à", max(bords), "| intérieur hors centre :", sorted(set(interieur)))
assert set(coins) == {4399} and (min(bords), max(bords)) == (1576, 1691) and set(interieur) <= {2, 3, 4}
# temoin : une de ses dispositions, cavalier retire, n'immobilise plus le roi
k, r1, r2, n, c = sols[0]
b = chess.Board(None); b.set_piece_at(k, chess.Piece(chess.KING, False))
for r in (r1, r2): b.set_piece_at(r, chess.Piece(chess.ROOK, True))
b.turn = chess.BLACK; assert any(True for _ in b.legal_moves)
print("controles : tout est conforme (temoins refuses)")
