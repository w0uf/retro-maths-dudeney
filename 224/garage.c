/* n° 224 THE MOTOR-GARAGE PUZZLE — Dudeney, Amusements in Mathematics (1917).
 *
 *   A B C D          A-B-C-D          douze emplacements, huit voitures.
 *     E                |              Un deplacement = une voiture, une
 *     F G              B-E-F-G        distance quelconque, par des cases
 *     H                    |  F-H     libres.  Depart  A..D = 5 6 7 8,
 *   I J K L               H-J         I..L = 1 2 3 4 ; arrivee : les deux
 *                     I-J-K-L         rangees echangees.
 *
 * Dudeney donne 43 coups et affirme que c'est le plus court.
 * Parcours en largeur sur les 19 958 400 etats.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 12
static int adj[N][4], deg[N];
static void arete(int a, int b){ adj[a][deg[a]++]=b; adj[b][deg[b]++]=a; }

static int patidx[1<<N];
static int fact[9];
#define NETATS 19958400

static long rang(const signed char *v){          /* v[node] = 0 vide, 1..8 voiture */
    int masque=0, ordre[8], n=0;
    for(int i=0;i<N;i++) if(v[i]){ masque|=1<<i; ordre[n++]=v[i]; }
    long r=0;
    for(int i=0;i<8;i++){
        int c=0;
        for(int j=i+1;j<8;j++) if(ordre[j]<ordre[i]) c++;
        r += (long)c*fact[7-i];
    }
    return (long)patidx[masque]*40320L + r;
}

static unsigned char *dist;
static int *file;

int main(void){
    arete(0,1); arete(1,2); arete(2,3); arete(1,4);
    arete(4,5); arete(5,6); arete(5,7); arete(7,9);
    arete(8,9); arete(9,10); arete(10,11);

    fact[0]=1; for(int i=1;i<9;i++) fact[i]=fact[i-1]*i;
    int np=0;
    for(int m=0;m<(1<<N);m++){ patidx[m]=-1; if(__builtin_popcount(m)==8) patidx[m]=np++; }
    printf("motifs d'occupation : %d   etats : %ld\n", np, (long)np*40320);

    signed char dep[N]={5,6,7,8,0,0,0,0,1,2,3,4};
    signed char but[N]={1,2,3,4,0,0,0,0,5,6,7,8};

    dist = malloc(NETATS); memset(dist,255,NETATS);
    file = malloc(sizeof(int)*NETATS);
    long rd=rang(dep), rb=rang(but);
    printf("rang depart %ld  arrivee %ld\n", rd, rb);

    /* table rang -> etat, reconstruite a la volee : on stocke l'etat dans la file */
    signed char *etats = malloc((size_t)NETATS*N);
    memcpy(etats+(size_t)rd*N, dep, N);
    dist[rd]=0; file[0]=rd; long tete=0, queue=1;
    long vus=1;
    while(tete<queue){
        long r=file[tete++];
        signed char v[N]; memcpy(v,etats+(size_t)r*N,N);
        unsigned char d=dist[r];
        if(r==rb){ printf("\n>>> optimum trouve : %d coups\n", d); break; }
        for(int i=0;i<N;i++){
            if(!v[i]) continue;
            /* cases atteignables depuis i par des cases vides */
            int pile[N], np2=0, vu=0;
            for(int k=0;k<deg[i];k++){ int w=adj[i][k]; if(!v[w] && !(vu>>w&1)){ vu|=1<<w; pile[np2++]=w; } }
            for(int p=0;p<np2;p++){
                int x=pile[p];
                for(int k=0;k<deg[x];k++){ int w=adj[x][k]; if(!v[w] && !(vu>>w&1)){ vu|=1<<w; pile[np2++]=w; } }
            }
            for(int p=0;p<np2;p++){
                int x=pile[p];
                signed char w2[N]; memcpy(w2,v,N); w2[x]=v[i]; w2[i]=0;
                long r2=rang(w2);
                if(dist[r2]==255){ dist[r2]=d+1; memcpy(etats+(size_t)r2*N,w2,N); file[queue++]=r2; vus++; }
            }
        }
    }
    if(dist[rb]==255) printf("inaccessible\n");
    else printf("distance depart->arrivee : %d coups   (Dudeney : 43)\n", dist[rb]);
    printf("etats explores : %ld\n", vus);
    return 0;
}
