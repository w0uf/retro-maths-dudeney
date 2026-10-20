#!/usr/bin/env python3
"""Rétro Math's — n° 355 CHECKMATE! (Dudeney, 1917). La position est mat : quel fut le dernier coup ?
Énumération de toutes les positions précédentes légales (analyse rétrograde, sans les promotions).
Demande python-chess (pip install chess).
    python3 echec_et_mat.py   (instantané)"""
import chess
FINALE = "6K1/8/5Pk1/6Pp/7P/8/P7/1B6 b - - 0 1"
def legale(P):
    """position jouable : le camp qui n'a pas le trait n'est pas en échec, rois présents, pions hors des rangées 1 et 8"""
    if len(P.pieces(chess.KING, True)) != 1 or len(P.pieces(chess.KING, False)) != 1: return False
    if any(chess.square_rank(s) in (0, 7) for s in P.pieces(chess.PAWN, True) | P.pieces(chess.PAWN, False)): return False
    return not P.was_into_check() and not P.is_attacked_by(P.turn, P.king(not P.turn))
def predecesseurs(F):
    """toutes les positions P (trait au camp qui vient de jouer dans F) d'où un coup légal donne F"""
    camp = not F.turn; cible = F.board_fen(); out = []
    pieces = [(s, F.piece_at(s)) for s in chess.SQUARES if F.piece_at(s) and F.piece_at(s).color == camp]
    for t, pc in pieces:
        for s in chess.SQUARES:
            if s == t or F.piece_at(s): continue
            for pris in (None, chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
                P = F.copy(stack=False); P.turn = camp; P.ep_square = None; P.castling_rights = 0
                P.remove_piece_at(t); P.set_piece_at(s, pc)
                if pris: P.set_piece_at(t, chess.Piece(pris, not camp))
                if not legale(P): continue
                for m in P.legal_moves:
                    if m.from_square == s and m.to_square == t and not m.promotion:
                        Q = P.copy(stack=False); Q.push(m)
                        if Q.board_fen() == cible: out.append((P, P.san(m)))
        # prise en passant : le pion arrive en t, le pion adverse pris était derrière lui
        if pc.piece_type == chess.PAWN:
            r = chess.square_rank(t); f = chess.square_file(t)
            if (camp and r == 5) or (not camp and r == 2):
                derriere = t - 8 if camp else t + 8
                for df in (-1, 1):
                    if 0 <= f + df < 8:
                        s = chess.square(f + df, chess.square_rank(derriere))
                        if F.piece_at(s) or F.piece_at(derriere): continue
                        P = F.copy(stack=False); P.turn = camp; P.castling_rights = 0
                        P.remove_piece_at(t); P.set_piece_at(s, pc); P.set_piece_at(derriere, chess.Piece(chess.PAWN, not camp)); P.ep_square = t
                        if not legale(P): continue
                        for m in P.legal_moves:
                            if m.from_square == s and m.to_square == t and P.is_en_passant(m):
                                Q = P.copy(stack=False); Q.push(m)
                                if Q.board_fen() == cible: out.append((P, P.san(m)))
    return out
F = chess.Board(FINALE)
print(F); print("mat :", F.is_checkmate())
n1 = predecesseurs(F)
print("\n=== dernier coup blanc : positions précédentes légales :", len(n1))
for P, san in n1: print("   ", san, "depuis", P.fen())
P = n1[0][0]
# le coup noir d'avant : la prise en passant impose le double pas ; on le reconstruit et on le contrôle
Q = P.copy(stack=False); Q.turn = chess.BLACK; Q.ep_square = None
Q.remove_piece_at(chess.F5); Q.set_piece_at(chess.F7, chess.Piece(chess.PAWN, False))
print("\n=== un coup plus tôt (trait aux Noirs) :", Q.fen(), "| échec :", Q.is_check(), "| coups noirs légaux :", [Q.san(m) for m in Q.legal_moves])
n3 = predecesseurs(Q)
print("=== coup blanc d'avant : positions précédentes légales :", len(n3))
for R, san in n3[:30]: print("   ", san, "depuis", R.fen())
from collections import Counter
print("   par coup :", Counter(san for _, san in n3))

# --- ce que dit l'article
assert F.is_checkmate() and len(n1) == 1 and n1[0][1] == "exf6#"           # le dernier coup : la prise en passant
assert Q.is_check() and [Q.san(m) for m in Q.legal_moves] == ["f5"]          # le coup noir d'avant, seul legal
assert len(n3) == 1 and n3[0][1] == "e5+"                                    # et le coup blanc d'avant encore
# temoins : la position de depart reconstituee, 1. e5+ f5 2. exf6 e.p., redonne bien la gravure ;
# une position sans le pion e (rien n'a pu donner l'echec) n'a aucun predecesseur
R = n3[0][0].copy(); [R.push_san(x) for x in ("e5+", "f5", "exf6")]
assert R.board_fen() == F.board_fen() and R.is_checkmate()
G = F.copy(stack=False); G.remove_piece_at(chess.F6)
assert predecesseurs(G) == []
print("controles : tout est conforme (temoins refuses)")
