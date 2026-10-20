#!/usr/bin/env python3
"""n° 350 THE FORSAKEN KING — compile et lance le solveur exhaustif roi_abandonne.c, puis contrôle ses sorties :
pas de mat en 5, mat en 6 ; 1. e4 seul sur 20 ; après chaque réponse noire, 2. Dg4 seul sur 30 ; chaque branche du
tableau de Dudeney parmi les coups gagnants. Le rejeu d'une variante complète avec python-chess sert de témoin indépendant.
Demande un compilateur C (gcc) et python-chess (pip install chess).
    python3 controle.py          (environ 10 s)
    python3 controle.py carte    (ajoute la carte des 40 cases du roi noir, utile au n° 351 ; plusieurs minutes)"""
import os, re, subprocess, sys
ici = os.path.dirname(os.path.abspath(__file__)); exe = os.path.join(ici, "roi_abandonne")
subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(ici, "roi_abandonne.c")], check=True)
out = subprocess.run([exe], capture_output=True, text=True, check=True).stdout
print(out)
assert "mat en 5 ? 0 | mat en 6 ? 1" in out
premiers = re.findall(r"1\. (\S+)\s+: (MAT EN 6|pas de mat en 6)", out)
assert len(premiers) == 20 and [c for c, r in premiers if r == "MAT EN 6"] == ["Pe2-e4"]
seconds = re.findall(r"1\.\.\. R(\w\d) : (.*?)\s+\((\d+) sur (\d+)\)", out)
assert len(seconds) == 5 and all(c.split() == ["Qd1-g4"] and n == "1" and t == "30" for _, c, n, t in seconds)
# son tableau : 3. Dg7, ou 3. Dd7 si le roi est sur la colonne f ; 4. Fb5 (apres Dg7) ou b3 (apres Dd7) si le roi
# est revenu sur la 8e rangee, sinon 4. d4
branches = 0
for r1, r2, reste in re.findall(r"1\.\.\.R(\w\d) 2\.\.\.R(\w\d) : 3e coup ->(.*)", out):
    troisiemes = dict(re.findall(r"(\S+) \[(.*?)\]", reste))
    le3 = "Qg4-d7" if r2[0] == "f" else "Qg4-g7"
    assert le3 in troisiemes, (r1, r2)
    for r3, coups in re.findall(r"R(\w\d):(\S*)", troisiemes[le3]):
        le4 = ("Pb2-b3" if le3 == "Qg4-d7" else "Bf1-b5") if r3[1] == "8" else "Pd2-d4"
        assert le4 in coups.split(","), (r1, r2, r3); branches += 1
print("tableau de Dudeney : %d branches, le coup prescrit est toujours gagnant" % branches)
# temoin independant, avec python-chess : une branche du tableau jouee jusqu'au bout. Apres 1. e4 Rd8 2. Dg4 Re8
# 3. Dg7 Rd8 4. Fb5, chaque reponse noire est matee en deux coups (recherche exhaustive). Temoin : apres 2... Rf7,
# le coup que son tableau ecarte (3. Dg7+, roi sur la colonne f) laisse 3... Re6, et la, pas de mat en deux
import chess
def mat1(b):
    return any((b.push(m), b.is_checkmate(), b.pop())[1] for m in list(b.legal_moves))
def mat2(b):
    for m in list(b.legal_moves):
        b.push(m)
        ok = not b.is_stalemate() and (b.is_checkmate() or all((b.push(n), mat1(b), b.pop())[1] for n in list(b.legal_moves)))
        b.pop()
        if ok: return True
    return False
b = chess.Board("4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1")
for c in "e4 Kd8 Qg4 Ke8 Qg7 Kd8 Bb5".split(): b.push_san(c)
reps = list(b.legal_moves)
assert reps and all((b.push(n), mat2(b), b.pop())[1] for n in reps)
print("branche 1. e4 Rd8 2. Dg4 Re8 3. Dg7 Rd8 4. Fb5 : %d reponse(s) noire(s), matee(s) en deux" % len(reps))
t = chess.Board("4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1"); [t.push_san(c) for c in ("e4", "Kf8", "Qg4", "Kf7", "Qg7+", "Ke6")]
assert not mat2(t)
if sys.argv[1:] == ["carte"]:
    carte = subprocess.run([exe, "carte"], capture_output=True, text=True, check=True).stdout
    print(carte)
    m = dict((c, (int(n), cles.split())) for c, n, cles in re.findall(r"(\w\d) : mat en (\d) ; premiers coups gagnants : \d+ sur \d+ →(.*)", carte))
    assert len(m) == 40 and sum(1 for n, _ in m.values() if n == 6) == 37
    assert m["h4"] == (3, ["Pd2-d4"]) and m["a4"] == (5, ["Pc2-c4"]) and m["e4"][0] == 7
    print("carte : 37 cases en 6, h4 en 3 (1. d4 seul), a4 en 5 (1. c4 seul), e4 en 7")
print("controles : tout est conforme (temoins refuses)")
