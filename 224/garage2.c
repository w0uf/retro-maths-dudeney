/* Suite : eloignement maximal depuis le depart, et nombre de solutions en 43 coups. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 12
static int adj[N][4], deg[N];
static void arete(int a,int b){adj[a][deg[a]++]=b;adj[b][deg[b]++]=a;}
static int patidx[1<<N]; static int fact[9];
#define NETATS 19958400
static long rang(const signed char*v){int m=0,o[8],n=0;for(int i=0;i<N;i++)if(v[i]){m|=1<<i;o[n++]=v[i];}
 long r=0;for(int i=0;i<8;i++){int c=0;for(int j=i+1;j<8;j++)if(o[j]<o[i])c++;r+=(long)c*fact[7-i];}
 return (long)patidx[m]*40320L+r;}
int main(void){
 arete(0,1);arete(1,2);arete(2,3);arete(1,4);arete(4,5);arete(5,6);arete(5,7);arete(7,9);
 arete(8,9);arete(9,10);arete(10,11);
 fact[0]=1;for(int i=1;i<9;i++)fact[i]=fact[i-1]*i;
 int np=0;for(int m=0;m<(1<<N);m++){patidx[m]=-1;if(__builtin_popcount(m)==8)patidx[m]=np++;}
 signed char dep[N]={5,6,7,8,0,0,0,0,1,2,3,4}, but[N]={1,2,3,4,0,0,0,0,5,6,7,8};
 unsigned char*dist=malloc(NETATS);memset(dist,255,NETATS);
 unsigned long long*nb=calloc(NETATS,8);
 int*file=malloc(sizeof(int)*NETATS);
 signed char*et=malloc((size_t)NETATS*N);
 long rd=rang(dep),rb=rang(but);
 memcpy(et+(size_t)rd*N,dep,N);dist[rd]=0;nb[rd]=1;file[0]=rd;
 long tete=0,queue=1;
 while(tete<queue){
  long r=file[tete++];signed char v[N];memcpy(v,et+(size_t)r*N,N);unsigned char d=dist[r];
  for(int i=0;i<N;i++){ if(!v[i])continue;
   int pile[N],np2=0,vu=0;
   for(int k=0;k<deg[i];k++){int w=adj[i][k];if(!v[w]&&!(vu>>w&1)){vu|=1<<w;pile[np2++]=w;}}
   for(int p=0;p<np2;p++){int x=pile[p];for(int k=0;k<deg[x];k++){int w=adj[x][k];if(!v[w]&&!(vu>>w&1)){vu|=1<<w;pile[np2++]=w;}}}
   for(int p=0;p<np2;p++){int x=pile[p];signed char w2[N];memcpy(w2,v,N);w2[x]=v[i];w2[i]=0;
    long r2=rang(w2);
    if(dist[r2]==255){dist[r2]=d+1;nb[r2]=nb[r];memcpy(et+(size_t)r2*N,w2,N);file[queue++]=r2;}
    else if(dist[r2]==d+1) nb[r2]+=nb[r];
   }}}
 long cnt[64]={0};long atteints=0,maxd=0;
 for(long i=0;i<NETATS;i++) if(dist[i]!=255){cnt[dist[i]]++;atteints++;if(dist[i]>maxd)maxd=dist[i];}
 printf("etats atteignables depuis le depart : %ld sur %d\n",atteints,NETATS);
 printf("eloignement maximal : %ld coups\n",maxd);
 printf("distance du but : %d coups | solutions optimales : %llu\n",dist[rb],nb[rb]);
 puts("\nrepartition des etats par distance :");
 for(int d=0;d<=maxd;d++) printf("  %2d : %8ld\n",d,cnt[d]);
 return 0;}
