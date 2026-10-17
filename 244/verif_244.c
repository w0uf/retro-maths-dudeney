/* n° 244 THE FIFTEEN TURNINGS : plus long trajet sans reprendre une route, en 15 tournants au plus,
   sur le quadrillage 8 x 8 (villes à 1 mile), départ colonne 0, rangée 4.
   usage : verif_244 <tournants> <seuil> : compte les trajets de longueur >= seuil, donne le maximum */
#include <stdio.h>
#include <stdlib.h>
static int H[8], V[8];           /* H[r] : bits des routes horizontales de la rangée r ; V[c] : verticales de la colonne c */
static int seuil, best = 0; static int pc[20], pr[20], np = 0, montre = 0; static long long nb[200], noeuds = 0;
static int runs[128][4], nruns[128];
static void prep(void){ for (int m = 0; m < 128; m++){ int k = 0, l = 0; for (int i = 0; i < 7; i++){ if (!(m >> i & 1)) l++; else { if (l) runs[m][k++] = l; l = 0; } } if (l) runs[m][k++] = l; nruns[m] = k; } }
static int borne(int *L, int k){ int t[32], n = 0, s = 0; for (int i = 0; i < 8; i++) for (int j = 0; j < nruns[L[i]]; j++) t[n++] = runs[L[i]][j];
  for (int a = 0; a < k && a < n; a++){ int m = a; for (int b = a + 1; b < n; b++) if (t[b] > t[m]) m = b; int x = t[a]; t[a] = t[m]; t[m] = x; s += t[a]; } return s; }
static void dfs(int c, int r, int horiz, int reste, int total){   /* reste : segments encore permis ; horiz : le prochain segment est horizontal */
  noeuds++; pc[np] = c; pr[np] = r; np++;
  if (total >= montre && montre) { for (int i = 0; i < np; i++) printf("%d,%d ", pc[i], pr[i]); printf("= %d\n", total); }
  if (total > best) best = total;
  if (total >= seuil) nb[total]++;   /* compté à chaque fin de segment : trajets distincts par leur suite de segments */
  if (!reste) { np--; return; }
  int nh = horiz ? (reste + 1) / 2 : reste / 2, nv = reste - nh;
  if (total + borne(H, nh) + borne(V, nv) < seuil) { np--; return; }
  for (int s = -1; s <= 1; s += 2){ int *L = horiz ? &H[r] : &V[c]; int p = horiz ? c : r, sauve = *L;
    for (int l = 1; ; l++){ int q = p + s * l; if (q < 0 || q > 7) break; int bit = 1 << (s > 0 ? q - 1 : q); if (*L & bit) break; *L |= bit;
      if (horiz) dfs(q, r, 0, reste - 1, total + l); else dfs(c, q, 1, reste - 1, total + l); }
    *L = sauve; } np--; }
int main(int n, char **a){ int t = atoi(a[1]); seuil = atoi(a[2]); if (n > 3) montre = atoi(a[3]); prep();
  dfs(0, 4, 1, t + 1, 0); dfs(0, 4, 0, t + 1, 0);
  nb[0] = 0; printf("tournants %d : maximum %d ; noeuds %lld\n", t, best, noeuds);
  for (int i = seuil; i < 200; i++) if (nb[i]) printf("  longueur %d : %lld trajets\n", i, nb[i]); return 0; }
