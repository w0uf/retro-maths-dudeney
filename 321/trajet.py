"""Contrôle indépendant d'un trajet de tour case par case : 64 cases, chacune une fois, pas orthogonaux,
nombre de lignes droites (coups), case de fin de certains coups. Utilisé par 321, 322 et 324."""
def case(s): return ("abcdefgh".index(s[0]), int(s[1:]) - 1)
def lignes(T):
    """découpe un trajet (liste de cases) en lignes droites ; renvoie la liste des cases de fin de chaque ligne"""
    fins = []; d0 = None
    for i in range(1, len(T)):
        d = (T[i][0] - T[i-1][0], T[i][1] - T[i-1][1])
        assert abs(d[0]) + abs(d[1]) == 1, ("pas qui n'est pas un pas de tour", T[i-1], T[i])
        if d0 is not None and d != d0: fins.append(T[i-1])
        d0 = d
    fins.append(T[-1]); return fins
def controle(T, toutes=True):
    if toutes: assert sorted(set(T)) == sorted((x, y) for x in range(8) for y in range(8)) and len(T) == 64, "pas les 64 cases une fois chacune"
    return lignes(T)
