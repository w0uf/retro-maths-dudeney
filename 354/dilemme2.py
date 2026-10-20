#!/usr/bin/env python3
"""n° 354, suite : les mats sont-ils réellement ATTEIGNABLES depuis la position du livre, les Blancs jouant seuls ?
Parcours en largeur de toutes les positions (roi blanc, fou, pion ou pièce promue, tour noire prise ou non).
Le roi noir ne bouge jamais ; les Blancs peuvent le laisser en échec, mais leur propre roi doit rester en sûreté.
    python3 dilemme2.py          (les 54 cases, environ 50 s)
    python3 dilemme2.py b2 e8    (quelques cases)"""
import chess, sys, time
from collections import deque
def att(pt, s, occ):
    if pt == chess.KING: return chess.BB_KING_ATTACKS[s]
    if pt == chess.KNIGHT: return chess.BB_KNIGHT_ATTACKS[s]
    d = chess.BB_DIAG_ATTACKS[s][chess.BB_DIAG_MASKS[s] & occ]
    l = chess.BB_RANK_ATTACKS[s][chess.BB_RANK_MASKS[s] & occ] | chess.BB_FILE_ATTACKS[s][chess.BB_FILE_MASKS[s] & occ]
    return d if pt == chess.BISHOP else l if pt == chess.ROOK else d | l
def bits(b):
    while b:
        l = b & -b; yield l.bit_length() - 1; b ^= l
E5 = chess.E5
def cherche(X, limite=None):
    """rend (profondeur du premier mat, position) ou (None, nombre de positions visitées)"""
    bx = 1 << X; KX = chess.BB_KING_ATTACKS[X]
    s0 = (chess.G7, chess.F6, chess.PAWN, chess.F7, True)
    dist = {s0: 0}; q = deque([s0])
    def mat(wk, wb, pt, ps, tour):
        occ = (1 << wk) | (1 << wb) | (1 << ps) | ((1 << E5) if tour else 0)
        A = chess.BB_KING_ATTACKS[wk] | att(chess.BISHOP, wb, occ)
        A |= (chess.BB_PAWN_ATTACKS[chess.WHITE][ps] if pt == chess.PAWN else att(pt, ps, occ))
        if not A >> X & 1 or KX & ~A & ~((1 << E5) if tour else 0): return False
        b = chess.Board(None); b.set_piece_at(X, chess.Piece(chess.KING, False)); b.set_piece_at(wk, chess.Piece(chess.KING, True))
        b.set_piece_at(wb, chess.Piece(chess.BISHOP, True)); b.set_piece_at(ps, chess.Piece(pt, True))
        if tour: b.set_piece_at(E5, chess.Piece(chess.ROOK, False))
        b.turn = chess.BLACK; return b.is_checkmate()
    while q:
        s = q.popleft(); wk, wb, pt, ps, tour = s; d = dist[s]
        if mat(*s): return d, s
        if limite and d >= limite: continue
        tb = (1 << E5) if tour else 0
        occ = (1 << wk) | (1 << wb) | (1 << ps) | tb | bx
        blancs = (1 << wk) | (1 << wb) | (1 << ps)
        def sur(wk2, occ2, tour2):          # le roi blanc n'est pas en prise
            if KX >> wk2 & 1: return False
            return not (tour2 and att(chess.ROOK, E5, occ2) >> wk2 & 1)
        suiv = []
        for t in bits(chess.BB_KING_ATTACKS[wk] & ~blancs & ~bx):
            t2 = tour and t != E5; o2 = (occ ^ (1 << wk)) | (1 << t)
            if sur(t, o2, t2): suiv.append((t, wb, pt, ps, t2))
        for t in bits(att(chess.BISHOP, wb, occ) & ~blancs & ~bx):
            t2 = tour and t != E5; o2 = (occ ^ (1 << wb)) | (1 << t)
            if sur(wk, o2, t2): suiv.append((wk, t, pt, ps, t2))
        if pt == chess.PAWN:
            t = ps + 8
            if not occ >> t & 1:
                for np in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT):
                    o2 = (occ ^ (1 << ps)) | (1 << t)
                    if sur(wk, o2, tour): suiv.append((wk, wb, np, t, tour))
        else:
            for t in bits(att(pt, ps, occ) & ~blancs & ~bx):
                t2 = tour and t != E5; o2 = (occ ^ (1 << ps)) | (1 << t)
                if sur(wk, o2, t2): suiv.append((wk, wb, pt, t, t2))
        for v in suiv:
            if v not in dist: dist[v] = d + 1; q.append(v)
    return None, len(dist)
if __name__ == "__main__":
    nom = "?PNBRQK"
    cases = [chess.parse_square(a) for a in sys.argv[1:]] or [X for X in chess.SQUARES if X not in (chess.G7, chess.F6, chess.F7, E5) and not chess.BB_KING_ATTACKS[X] >> chess.G7 & 1]
    sans = []; prof = {}
    for X in cases:
        t0 = time.time(); d, s = cherche(X); prof[chess.square_name(X)] = d
        if d is None: sans.append(chess.square_name(X)); print(chess.square_name(X), ": AUCUN MAT ATTEIGNABLE (%d positions explorées, %.0f s)" % (s, time.time() - t0), flush=True)
        else: print(chess.square_name(X), ": mat en %d coups blancs — Rb %s, F %s, %s %s, tour %s (%.0f s)" % (d, chess.square_name(s[0]), chess.square_name(s[1]), nom[s[2]], chess.square_name(s[3]), "en e5" if s[4] else "prise", time.time() - t0), flush=True)
    print("cases imprenables :", sans)
    if not sys.argv[1:]:
        # --- ce que dit l'article
        assert len(cases) == 54 and sans == ["b2"]
        assert cherche(chess.B2) == (None, 585469)                         # plus d'un demi-million de positions, aucun mat
        d = [v for v in prof.values() if v is not None]
        assert (min(d), max(d)) == (2, 9) and prof["e8"] == 2 and prof["b4"] == 9
        # temoin : le meme parcours trouve le mat en 2 coups pour la case e8 ; il ne repond donc pas « aucun » par defaut
        assert cherche(chess.E8)[0] == 2
        print("controles : tout est conforme (temoins refuses)")
