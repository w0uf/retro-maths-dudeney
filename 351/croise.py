#!/usr/bin/env python3
"""Rétro Math's — n° 351 THE CRUSADER (Dudeney, 1917).
Rejeu de sa partie de seize coups (un seul cavalier blanc joue ; quinze prises), puis recherche exhaustive du mat
dans la position obtenue : roi noir seul en h4 contre l'armée blanche au complet.
Demande python-chess (pip install chess).
    python3 croise.py   (instantané)
La carte des 40 cases du roi noir (h4 : mat en 3, ailleurs 5 à 7) est dans ../350 (python3 controle.py carte)."""
import chess
PARTIE = ("Nc3 d5 Nxd5 Nc6 Nxe7 g5 Nxc8 Nf6 Nxa7 Ne4 Nxc6 Nc3 Nxd8 Rg8 Nxf7 Rg6 Nxg5 Re6 Nxh7 Nb1 "
          "Nxf8 Ra3 Nxe6 b5 Nxc7+ Kf7 Nxb5 Kg6 Nxa3 Kh5 Nxb1 Kh4").split()
def rejoue(coups):
    b = chess.Board(); prises = 0
    for c in coups:
        m = b.parse_san(c)                     # leve une exception si le coup est illegal
        prises += b.is_capture(m); b.push(m)
    return b, prises
b, prises = rejoue(PARTIE)
print("sa partie :", len(PARTIE) // 2, "coups, prises blanches :", prises, "| position :", b.fen())
assert len(PARTIE) == 32 and prises == 15 and b.board_fen() == "8/8/8/8/7k/8/PPPPPPPP/RNBQKBNR"
assert all(chess.Board().piece_at(s) == b.piece_at(s) for s in chess.SquareSet(chess.BB_RANK_1 | chess.BB_RANK_2))

def mat_en(b, n):
    """les Blancs (au trait) matent-ils en n coups au plus, quoi que fassent les Noirs ? recherche exhaustive"""
    for m in list(b.legal_moves):
        b.push(m)
        if b.is_checkmate(): b.pop(); return True
        ok = n > 1 and not b.is_stalemate() and all((b.push(r), mat_en(b, n - 1), b.pop())[1] for r in list(b.legal_moves))
        b.pop()
        if ok: return True
    return False
assert not mat_en(b, 2)                                                  # pas de mat en deux
gagnants = []
for m in list(b.legal_moves):
    b.push(m)
    if not b.is_stalemate() and all((b.push(r), mat_en(b, 2), b.pop())[1] for r in list(b.legal_moves)): gagnants.append(b.peek())
    b.pop()
print("premiers coups qui forcent le mat en trois :", [b.san(m) for m in gagnants], "sur", b.legal_moves.count())
assert [b.san(m) for m in gagnants] == ["d4"] and b.legal_moves.count() == 19
# ses deux variantes
for v in ("d4 Kh5 Qd3 Kh4 Qh3#", "d4 Kh5 Qd3 Kg4 Qh3#", "d4 Kg4 e4+ Kh4 g3#"):
    t = b.copy(); [t.push_san(c) for c in v.split()]; assert t.is_checkmate(), v
# temoins : la partie avec un coup illegal (3. Cd4, qui n'est pas un saut de cavalier) est refusee ; 17. e4, au lieu de d4, ne force pas le mat en 3
try: rejoue(["Nc3", "d5", "Nd4"] + PARTIE[3:]); raise SystemExit("ERREUR : partie fausse acceptee")
except ValueError: pass
t = b.copy(); t.push_san("e4"); assert not all((t.push(r), mat_en(t, 2), t.pop())[1] for r in list(t.legal_moves))
print("controles : tout est conforme (temoins refuses)")
