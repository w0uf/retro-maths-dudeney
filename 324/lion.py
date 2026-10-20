"""n° 324 THE LION AND THE MAN : l'homme part de a1, le lion de h8 ; chacun visite toutes les cellules en 22 lignes
droites (le minimum) et finit dans la cellule de l'autre ; même vitesse, une cellule par instant.
Ils ne doivent jamais se rencontrer (ni dans une cellule, ni en se croisant dans une porte), mais s'apercevoir
au moins une fois : même rangée ou même colonne au même instant."""
H = [l.split(":")[1].split() for l in open("homme.txt")]
case = lambda s: ("abcdefgh".index(s[0]), int(s[1]) - 1)
H = [[(0, 0)] + [case(s) for s in r] for r in H]   # instant 0 : l'homme est dans sa cellule de départ
rot = lambda r: [(7 - x, 7 - y) for x, y in r]
L = [rot(r) for r in H]                      # les routes du lion : celles de l'homme, plateau retourné
print("routes de l'homme en 22 lignes :", len(H), "| longueur :", {len(r) for r in H})
def bilan(h, l):
    rencontre = any(h[t] == l[t] for t in range(len(h))) or any(h[t] == l[t+1] and h[t+1] == l[t] for t in range(len(h) - 1))
    vues = [t for t in range(len(h)) if h[t][0] == l[t][0] or h[t][1] == l[t][1]]
    return rencontre, vues
ok = []; jamais = 0; tot = 0
for i, h in enumerate(H):
    for j, l in enumerate(L):
        tot += 1; r, v = bilan(h, l)
        if not r:
            if v: ok.append((i, j, v))
            else: jamais += 1
print("couples (homme, lion) :", tot, "| sans rencontre :", len(ok) + jamais, "| dont avec au moins un coup d'œil :", len(ok))
print("route retournée (j = i) : rencontres ou coups d'œil :", {bilan(H[i], L[i])[0] or bool(bilan(H[i], L[i])[1]) for i in range(len(H))})
import collections; print("nombre d'instants de coup d'œil :", collections.Counter(len(v) for _, _, v in ok))
assert len(H) == 28 and tot == 784 and len(ok) == 136 and jamais == 28
# témoin : un couple qui se rencontre doit être signalé (l'homme contre lui-même, décalé : même cellule à l'instant 0 du lion)
assert bilan(H[0], H[0])[0], "témoin non détecté"
print("témoin (deux fois le même trajet) : rencontre détectée")
