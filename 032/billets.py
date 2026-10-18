# -*- coding: utf-8 -*-
"""n° 32 THE EXCURSION TICKET PUZZLE — Dudeney, 1917.

« Ce billet d'excursion coute dix-neuf shillings et neuf pence, et j'aimerais
savoir de combien de facons differentes on peut payer une telle somme avec
la monnaie courante du royaume. »
Dudeney : 458 908 622 — et il refuse de donner sa methode.

Monnaie britannique de 1917, en farthings (le farthing = un quart de penny) :
  farthing 1, demi-penny 2, penny 4, trois pence 12, six pence 24,
  shilling 48, florin 96, demi-couronne 120, double florin 192,
  couronne 240, demi-souverain 480, souverain 960.
"""
SOMME = (19*12 + 9) * 4          # dix-neuf shillings et neuf pence, en farthings
print("somme a payer :", SOMME//4, "pence, soit", SOMME, "farthings")

def facons(total, pieces):
    f = [0]*(total+1); f[0] = 1
    for p in pieces:
        for s in range(p, total+1): f[s] += f[s-p]
    return f[total]

JEUX = {
 "sans le double florin" : [1,2,4,12,24,48,96,120,240,480],
 "avec le double florin" : [1,2,4,12,24,48,96,120,192,240,480],
 "sans la demi-couronne" : [1,2,4,12,24,48,96,240,480],
 "sans le demi-souverain": [1,2,4,12,24,48,96,120,240],
 "bronze + argent usuel" : [1,2,4,12,24,48,96,120,240,480,960],
}
for nom, p in JEUX.items():
    n = facons(SOMME, [x for x in p if x <= SOMME])
    print("  %-24s : %12d   %s" % (nom, n, "<<< c'est son nombre" if n == 458908622 else ""))

print("\n=== Sa formule pour les seules pieces de bronze ===")
print("  « toute somme peut etre payee de (n+1)^2 facons, n etant le nombre de pence »")
BRONZE = [1,2,4]
for n in range(1, 13):
    v = facons(4*n, BRONZE)
    print("   %2d pence : %4d facons   (n+1)^2 = %4d   %s" % (n, v, (n+1)**2,
          "ok" if v == (n+1)**2 else "ECART"))

print("\n=== Son tableau de la monnaie rendue ===")
PIECES = [("farthing",1),("demi-penny",2),("penny",4),("trois pence",12),
          ("six pence",24),("shilling",48),("florin",96),("demi-couronne",120),
          ("double florin",192),("couronne",240),("demi-souverain",480),
          ("souverain",960)]
SIENS = [0,1,3,16,66,402,3818,8709,60239,166651,6261622,500291833]
print("   piece              valeur   calcul        Dudeney      ")
ok = True
for (nom, v), s in zip(PIECES, SIENS):
    plus_petites = [p for _, p in PIECES if p < v]
    n = facons(v, plus_petites) if plus_petites else 0
    marque = "ok" if n == s else "ECART"
    if n != s: ok = False
    print("   %-16s %6d  %12d  %12d  %s" % (nom, v, n, s, marque))
print("\n  les douze lignes de son tableau :", "toutes exactes" if ok else "une ou plusieurs fausses")

# ═══ temoins : le calcul par programmation dynamique, recoupe par force brute ═══
print("\n=== Controle du calcul sur de petites sommes ===")
def brute(total, pieces):
    """enumeration directe des combinaisons, sans programmation dynamique"""
    if not pieces: return 1 if total == 0 else 0
    p, reste = pieces[-1], pieces[:-1]
    return sum(brute(total - k * p, reste) for k in range(total // p + 1))
def faux(total, pieces):
    """erreur classique : boucles inversees, on compte alors les suites ordonnees"""
    f = [0]*(total+1); f[0] = 1
    for s in range(1, total+1):
        for p in pieces:
            if p <= s: f[s] += f[s-p]
    return f[total]
P = [1,2,4,12,24,48,96,120,192,240,480]
for total in (4, 48, 120, 240):
    pp = [x for x in P if x <= total]
    print("  %3d farthings : dynamique %8d | force brute %8d | version fautive %.3g"
          % (total, facons(total, pp), brute(total, pp), float(faux(total, pp))))
    assert facons(total, pp) == brute(total, pp) != faux(total, pp)
print("  la version fautive est bien refusee ; la bonne concorde partout")
print("  un penny en bronze : %d facons (4 farthings, 2 farthings + 1 demi-penny,"
      " 2 demi-pence, 1 penny)" % facons(4, [1, 2, 4]))
assert facons(4, [1, 2, 4]) == 4 and ok
assert facons(SOMME, [x for x in P if x <= SOMME]) == 458908622
assert facons(SOMME, [x for x in P if x <= SOMME and x != 192]) == 357549696
