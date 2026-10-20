#!/usr/bin/env python3
"""n° 352 IMMOVABLE PAWNS : les 17 coups de Dudeney (les Noirs jouent les mêmes coups, en miroir).
Demande python-chess."""
import chess
W = "Nf3 Nh4 Ng6 Nxh8 Ng6 Nxf8 Kxf1 Nc3 Na4 Nb6 Nxa8 Nb6 Nxc8 Nd6 Qe1 Nxe8 Kxe1".split()
miroir = lambda c: c.translate(str.maketrans("12345678", "87654321"))
CIBLE = "4k3/pppppppp/8/8/8/8/PPPPPPPP/4K3"
b = chess.Board()
for m in W:
    b.push_san(m); b.push_san(miroir(m))
print(b, "\n", b.board_fen(), "| position de la gravure :", b.board_fen() == CIBLE, "| coups :", b.fullmove_number - 1)
assert b.board_fen() == CIBLE
# témoin : sans le 15e coup de la dame (Qe1 / Qe8), les dames survivent et la position n'est pas atteinte
t = chess.Board()
for m in W[:14] + W[15:]:
    t.push_san(m); t.push_san(miroir(m))
print("témoin (dames immobiles) :", t.board_fen(), "| refusé :", t.board_fen() != CIBLE)
assert t.board_fen() != CIBLE
