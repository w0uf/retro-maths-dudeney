#!/usr/bin/env python3
"""Rétro Math's — n° 354 AN AMAZING DILEMMA (Dudeney, 1917). Blancs : Rg7, Ff6, pion f7 ; Noirs : Te5 et un roi
posé on ne sait où, qui ne joue JAMAIS (ni lui ni la tour). Sur quelle case le roi noir est-il imprenable ?
On cherche, pour chaque case X, une position de mat que les Blancs peuvent construire : roi, fou de cases noires,
pion promu (D, T, F ou C), tour noire prise ou laissée en e5.
Demande python-chess (pip install chess).
    python3 dilemme.py    (mats « statiques » : existent-ils ? environ 30 s)
    python3 dilemme2.py   (sont-ils atteignables depuis la position du livre ? environ 50 s)"""
import chess, sys, time
from collections import deque
OCC0 = {chess.G7, chess.F6, chess.F7, chess.E5}
SOMBRES = [s for s in chess.SQUARES if (chess.square_file(s) + chess.square_rank(s)) % 2 == 0]
def att(pt, s, occ):
    if pt == chess.KING: return chess.BB_KING_ATTACKS[s]
    if pt == chess.KNIGHT: return chess.BB_KNIGHT_ATTACKS[s]
    d = chess.BB_DIAG_ATTACKS[s][chess.BB_DIAG_MASKS[s] & occ]
    l = chess.BB_RANK_ATTACKS[s][chess.BB_RANK_MASKS[s] & occ] | chess.BB_FILE_ATTACKS[s][chess.BB_FILE_MASKS[s] & occ]
    return d if pt == chess.BISHOP else l if pt == chess.ROOK else d | l
def mats_statiques(X, avec_tour):
    """positions de mat (roi noir en X, immobile) ; rend la liste des (type promu, case, roi blanc, fou)"""
    out = []; bx = 1 << X; voisins = chess.BB_KING_ATTACKS[X]
    tour = (1 << chess.E5) if avec_tour else 0
    for wk in chess.SQUARES:
        if wk == X or voisins >> wk & 1 or (avec_tour and wk == chess.E5): continue
        if avec_tour and att(chess.ROOK, chess.E5, (1 << wk) | bx) >> wk & 1 and False: pass
        for wb in SOMBRES:
            if wb in (X, wk) or (avec_tour and wb == chess.E5): continue
            for pt in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT):
                for ps in (SOMBRES if pt == chess.BISHOP else chess.SQUARES):
                    if ps in (X, wk, wb) or (avec_tour and ps == chess.E5): continue
                    occ = (1 << wk) | (1 << wb) | (1 << ps) | tour          # sans le roi noir : il est transparent pour ses fuites
                    A = chess.BB_KING_ATTACKS[wk] | att(chess.BISHOP, wb, occ) | att(pt, ps, occ)
                    if not A >> X & 1: continue                              # pas d'échec
                    if voisins & ~A & ~tour: continue                        # une fuite (ou une prise) reste
                    b = chess.Board(None); b.set_piece_at(X, chess.Piece(chess.KING, False)); b.set_piece_at(wk, chess.Piece(chess.KING, True))
                    b.set_piece_at(wb, chess.Piece(chess.BISHOP, True)); b.set_piece_at(ps, chess.Piece(pt, True))
                    if avec_tour: b.set_piece_at(chess.E5, chess.Piece(chess.ROOK, False))
                    b.turn = chess.BLACK
                    if b.is_checkmate() and not b.is_attacked_by(chess.BLACK, wk): out.append((pt, ps, wk, wb))
    return out
t0 = time.time(); res = {}
for X in chess.SQUARES:
    if X in OCC0 or chess.BB_KING_ATTACKS[X] >> chess.G7 & 1: continue
    sans = mats_statiques(X, False); avec = mats_statiques(X, True)
    res[X] = (len(sans), len(avec))
    print(chess.square_name(X), "mats tour prise :", len(sans), "| mats tour encore en e5 :", len(avec), flush=True)
print("%.0f s" % (time.time() - t0))
print("cases où aucun mat n'existe :", [chess.square_name(X) for X, (a, b) in res.items() if a + b == 0])

# --- ce que dit l'article
assert len(res) == 54 and [chess.square_name(X) for X, (a, b) in res.items() if a + b == 0] == ["b2"]
# la case jumelle de b2 est g7, occupee par le roi blanc : le roi noir y serait imprenable lui aussi
assert len(mats_statiques(chess.G7, False)) == 0 == len(mats_statiques(chess.G7, True))
# temoin : un mat connu (roi noir e8 ; Rg7, Ff6, Df7, tour noire en e5) est bien reconnu
assert (chess.QUEEN, chess.F7, chess.G7, chess.F6) in mats_statiques(chess.E8, True)
print("controles : tout est conforme (temoins refuses)")
