#!/usr/bin/env python3
"""Rétro Math's — n° 349 STALEMATE (Dudeney, 1917).
Sa partie de douze coups, rejouée coup par coup : pat des Blancs, les trente-deux pièces sur l'échiquier.
Puis la partie de dix coups attribuée à Sam Loyd (de mémoire, sans source vérifiée), où les prises sont permises.
Que sa partie soit « la meilleure possible » n'est PAS vérifié ici : il faudrait parcourir toutes les parties d'une
vingtaine de demi-coups.
Demande python-chess (pip install chess).
    python3 pat.py   (instantané)"""
import chess
SIENNE = "d4 e5 Qd3 Qh4 Qg3 Bb4+ Nd2 a5 a4 d6 h3 Be6 Ra3 f5 Qh2 c5 Rg3 Bb3 c4 f4 f3 e4 d5 e3".split()
LOYD = "e3 a5 Qh5 Ra6 Qxa5 h5 h4 Rah6 Qxc7 f6 Qxd7+ Kf7 Qxb7 Qd3 Qxb8 Qh7 Qxc8 Kg6 Qe6".split()
def rejoue(coups):
    b = chess.Board()
    for c in coups: b.push_san(c)             # leve une exception si le coup est illegal
    return b
b = rejoue(SIENNE)
print("sa partie :", len(SIENNE) // 2, "coups ; pat :", b.is_stalemate(), "; pièces :", len(b.piece_map()), "|", b.fen())
assert len(SIENNE) == 24 and b.turn == chess.WHITE and b.is_stalemate() and not b.is_check() and len(b.piece_map()) == 32
assert b.board_fen() == "rn2k1nr/1p4pp/3p4/p1pP4/PbP2p1q/1b2pPRP/1P1NP1PQ/2B1KBNR"
l = rejoue(LOYD)
print("partie de Loyd :", (len(LOYD) + 1) // 2, "coups blancs ; pat des Noirs :", l.is_stalemate(), "; pièces :", len(l.piece_map()))
assert l.turn == chess.BLACK and l.is_stalemate() and len(l.piece_map()) == 26
# temoins : sa partie privee du dernier coup noir n'est pas un pat ; un coup illegal est refuse
assert not rejoue(SIENNE[:-1]).is_stalemate()
try: rejoue(SIENNE[:2] + ["Qd4"]); raise SystemExit("ERREUR : coup illegal accepte")
except ValueError: pass
print("controles : tout est conforme (temoins refuses)")
