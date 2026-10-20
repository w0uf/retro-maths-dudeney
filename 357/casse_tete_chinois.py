#!/usr/bin/env python3
"""Rétro Math's — n° 357 ANCIENT CHINESE PUZZLE (Dudeney, 1917). Blancs : Rb6, Ta6, Tc6 ; Noirs : Rb8.
Les Blancs jouent et font mat en déplaçant chacune de leurs trois pièces une fois et une seule.
Demande python-chess (pip install chess).
    python3 casse_tete_chinois.py   (environ 1 s)"""
import chess
from itertools import permutations
FEN = "1k6/8/RKR5/8/8/8/8/8 w - - 0 1"
b0 = chess.Board(FEN)
print(b0, "\n")
# toutes les parties : 3 coups blancs, une pièce différente à chaque fois (la pièce est suivie à la trace)
def explore(b, restantes, ligne, res):
    """restantes : cases actuelles des pièces blanches qui n'ont pas encore joué"""
    if not restantes:
        return
    for m in list(b.legal_moves):
        if m.from_square not in restantes: continue
        san = b.san(m); b.push(m); r2 = restantes - {m.from_square}
        if not r2:
            res.append((ligne + [san], b.is_checkmate(), b.is_stalemate()))
        elif b.is_checkmate() or b.is_stalemate() or b.is_insufficient_material():
            res.append((ligne + [san], False, b.is_stalemate()))      # fini trop tôt
        else:
            for n in list(b.legal_moves):
                if b.is_capture(n): tag = "x"
                sn = b.san(n); b.push(n)
                # si une pièce blanche restante a été prise, la suite est perdue
                if all(b.piece_at(s) and b.piece_at(s).color for s in r2): explore(b, r2, ligne + [san, sn], res)
                else: res.append((ligne + [san, sn], False, False))
                b.pop()
        b.pop()
res = []; explore(b0.copy(), {chess.A6, chess.B6, chess.C6}, [], res)
print("lignes de jeu examinées :", len(res), "| lignes finissant par un mat au 3e coup :", sum(1 for l, m, s in res if m))
for l, m, s in res:
    if m: print("   ", ' '.join(l))
# une vraie solution : un premier coup tel que, quoi que jouent les Noirs, les Blancs puissent conclure
def gagne(b, restantes):
    for m in list(b.legal_moves):
        if m.from_square not in restantes: continue
        b.push(m); r2 = restantes - {m.from_square}; bon = False
        if not r2: bon = b.is_checkmate()
        elif not (b.is_checkmate() or b.is_stalemate()):
            reps = list(b.legal_moves); bon = True
            for n in reps:
                b.push(n)
                ok = all(b.piece_at(s) and b.piece_at(s).color for s in r2) and gagne(b, r2) is not None
                b.pop()
                if not ok: bon = False; break
        b.pop()
        if bon: yield_ = m; return m
    return None
cles = []
for m in list(b0.legal_moves):
    b = b0.copy(); san = b.san(m); b.push(m); r2 = {chess.A6, chess.B6, chess.C6} - {m.from_square}
    if b.is_stalemate(): print("   1.", san, ": PAT"); continue
    reps = list(b.legal_moves); bon = True
    for n in reps:
        b.push(n); ok = all(b.piece_at(s) and b.piece_at(s).color for s in r2) and gagne(b, r2) is not None; b.pop()
        if not ok: bon = False
    if bon: cles.append((san, [b.san(n) for n in reps]))
print("premiers coups qui forcent le mat (chaque pièce une fois) :", cles)
print("coups blancs possibles au départ :", b0.legal_moves.count(), "| dont pat immédiat :", sum(1 for m in b0.legal_moves if (lambda x: (x.push(m), x.is_stalemate())[1])(b0.copy())))
# mat le plus rapide sans la condition : recherche exhaustive en un, puis en deux coups
def mat_en_1(b):
    return [m for m in list(b.legal_moves) if (b.push(m), b.is_checkmate(), b.pop())[1]]
def mat_en_2(b):
    out = []
    for m in list(b.legal_moves):
        b.push(m)
        if not b.is_checkmate() and not b.is_stalemate():
            reps = list(b.legal_moves); lignes = []
            for n in reps:
                b.push(n); fin = mat_en_1(b)
                if fin: lignes.append(b.san(fin[0]))
                b.pop()
            if len(lignes) == len(reps): out.append(m)
        b.pop()
    return out
M1, M2 = mat_en_1(b0.copy()), mat_en_2(b0.copy())
print("sans la condition : mat en 1 :", [b0.san(m) for m in M1], "| premiers coups qui forcent le mat en 2 :", [b0.san(m) for m in M2])

# --- ce que dit l'article
assert len(res) == 2809 and cles == [("Rd6", ["Kc8"])]
mats3 = [l for l, m, s in res if m]
assert len(mats3) == 2 and ["Rd6", "Kc8", "Ka7", "Kc7", "Rac6#"] in mats3        # la sienne : 1. Td6 Rc8 2. Ra7 Rc7 3. Tac6#
assert b0.legal_moves.count() == 22 and sum(1 for m in b0.legal_moves if (lambda x: (x.push(m), x.is_stalemate())[1])(b0.copy())) == 12
assert M1 == [] and sorted(b0.san(m) for m in M2) == ["Ra8+", "Rd6"]               # mat en deux, de deux facons
# la fausse solution : 1. Te6 Rc8 2. Rc6 — mat si 2... Rd8 (3. Ta8#), mais 2... Rb8 sauve
f = chess.Board(FEN); [f.push_san(x) for x in ("Re6", "Kc8", "Kc6")]
g = f.copy(); g.push_san("Kd8"); assert "Ra8#" in [g.san(m) for m in mat_en_1(g)]
h = f.copy(); h.push_san("Kb8"); assert all(not (h.push(m), h.is_checkmate(), h.pop())[1] for m in h.legal_moves if m.from_square == chess.A6)
# temoin : le roi noir de la gravure n'a aucun coup s'il a le trait (pat en puissance)
p = chess.Board(FEN); p.turn = chess.BLACK; assert p.is_stalemate()
print("controles : tout est conforme (temoins refuses)")
