/* n° 343 — solveur optimal du taquin de quinze, par IDA* avec distance de
   Manhattan et conflits lineaires (corrigés le 18/10/2026 : la première version comptait 2 coups par paire inversée,
   ce qui surestime quand trois tuiles d'une ligne sont inversées et rendait la recherche non optimale). La cible est quelconque (lue au clavier). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int gr[16], gc[16];      /* ligne et colonne de chaque tuile dans la cible */
static int etat[16];            /* etat courant : etat[case] = tuile */
static int pos_vide;
static int seuil, suivant, sol[100];
static long long noeuds;

static int manhattan(void) {
    int d = 0, i;
    for (i = 0; i < 16; i++) {
        int t = etat[i];
        if (!t) continue;
        int r = i / 4, c = i % 4;
        d += abs(r - gr[t]) + abs(c - gc[t]);
    }
    return d;
}

/* Conflits linéaires, version admissible : dans une ligne (ou une colonne), parmi les tuiles qui y ont leur place,
   il faut en sortir au moins (nombre - plus longue sous-suite croissante), et chaque sortie coûte 2 coups de plus. */
static int a_sortir(const int *v, int n) {
    int lis[4], k, i, j, best = 0;
    for (i = 0; i < n; i++) { lis[i] = 1; for (j = 0; j < i; j++) if (v[j] < v[i] && lis[j] + 1 > lis[i]) lis[i] = lis[j] + 1; if (lis[i] > best) best = lis[i]; }
    k = n - best; return k;
}
static int conflits(void) {
    int n = 0, l, i, v[4], k;
    for (l = 0; l < 4; l++) {                    /* lignes */
        for (k = 0, i = 0; i < 4; i++) { int a = etat[l*4+i]; if (a && gr[a] == l) v[k++] = gc[a]; }
        n += 2 * a_sortir(v, k);
        for (k = 0, i = 0; i < 4; i++) { int a = etat[i*4+l]; if (a && gc[a] == l) v[k++] = gr[a]; }   /* colonnes */
        n += 2 * a_sortir(v, k);
    }
    return n;
}

static const int DR[4] = {-1, 1, 0, 0}, DC[4] = {0, 0, -1, 1};

static int fouille(int g, int md, int dernier) {
    int h = md + conflits();
    if (g + h > seuil) {
        if (g + h < suivant) suivant = g + h;
        return 0;
    }
    if (md == 0) return 1;
    noeuds++;
    int vieux = pos_vide, r = vieux / 4, c = vieux % 4, d;
    for (d = 0; d < 4; d++) {
        if ((d ^ 1) == dernier) continue;        /* ne pas defaire le coup */
        int nr = r + DR[d], nc = c + DC[d];
        if (nr < 0 || nr > 3 || nc < 0 || nc > 3) continue;
        int np = nr*4 + nc, t = etat[np];
        int avant = abs(nr - gr[t]) + abs(nc - gc[t]);
        int apres = abs(r  - gr[t]) + abs(c  - gc[t]);
        etat[vieux] = t; etat[np] = 0; pos_vide = np;
        sol[g] = t;
        if (fouille(g + 1, md - avant + apres, d)) return 1;
        etat[np] = t; etat[vieux] = 0; pos_vide = vieux;
    }
    return 0;
}

int main(void) {
    int cible[16], i;
    while (1) {
        for (i = 0; i < 16; i++)
            if (scanf("%d", &cible[i]) != 1) return 0;
        for (i = 0; i < 16; i++) { gr[cible[i]] = i / 4; gc[cible[i]] = i % 4; }
        for (i = 0; i < 15; i++) etat[i] = i + 1;
        etat[15] = 0; pos_vide = 15;
        noeuds = 0;
        seuil = manhattan() + conflits();
        while (1) {
            suivant = 1 << 30;
            if (fouille(0, manhattan(), -1)) break;
            if (suivant == 1 << 30) { seuil = -1; break; }
            seuil = suivant;
        }
        printf("%d %lld", seuil, noeuds);
        for (i = 0; i < seuil; i++) printf(" %d", sol[i]);
        printf("\n");
        fflush(stdout);
    }
}
