"""Contrôle indépendant d'un chemin de cavalier sur 7 × 7 (utilisé par 334 et 335)."""
case = lambda s: ("abcdefg".index(s[0]), int(s[1]) - 1)
def chemin(T, etapes=()):
    assert len(T) == 49 and len(set(T)) == 49 and all(0 <= x < 7 and 0 <= y < 7 for x, y in T), "pas les 49 cases une fois chacune"
    for a, b in zip(T, T[1:]): assert sorted((abs(a[0]-b[0]), abs(a[1]-b[1]))) == [1, 2], ("saut qui n'est pas de cavalier", a, b)
    for k, c in etapes: assert T[k-1] == c, ("étape manquée", k)
    return True
