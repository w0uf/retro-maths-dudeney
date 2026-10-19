#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 12
static int adj[N][4],deg[N];static void ar(int a,int b){adj[a][deg[a]++]=b;adj[b][deg[b]++]=a;}
static int pi_[1<<N];static int fact[9];
#define NE 19958400
static long rang(const signed char*v){int m=0,o[8],n=0;for(int i=0;i<N;i++)if(v[i]){m|=1<<i;o[n++]=v[i];}
 long r=0;for(int i=0;i<8;i++){int c=0;for(int j=i+1;j<8;j++)if(o[j]<o[i])c++;r+=(long)c*fact[7-i];}
 return (long)pi_[m]*40320L+r;}
int main(void){ar(0,1);ar(1,2);ar(2,3);ar(1,4);ar(4,5);ar(5,6);ar(5,7);ar(7,9);ar(8,9);ar(9,10);ar(10,11);
 fact[0]=1;for(int i=1;i<9;i++)fact[i]=fact[i-1]*i;
 int np=0;for(int m=0;m<(1<<N);m++){pi_[m]=-1;if(__builtin_popcount(m)==8)pi_[m]=np++;}
 signed char dep[N]={5,6,7,8,0,0,0,0,1,2,3,4};
 unsigned char*d=malloc(NE);memset(d,255,NE);int*f=malloc(4L*NE);signed char*et=malloc((size_t)NE*N);
 long rd=rang(dep);memcpy(et+(size_t)rd*N,dep,N);d[rd]=0;f[0]=rd;long t=0,q=1;
 while(t<q){long r=f[t++];signed char v[N];memcpy(v,et+(size_t)r*N,N);unsigned char dd=d[r];
  for(int i=0;i<N;i++){if(!v[i])continue;int pl[N],n2=0,vu=0;
   for(int k=0;k<deg[i];k++){int w=adj[i][k];if(!v[w]&&!(vu>>w&1)){vu|=1<<w;pl[n2++]=w;}}
   for(int p=0;p<n2;p++){int x=pl[p];for(int k=0;k<deg[x];k++){int w=adj[x][k];if(!v[w]&&!(vu>>w&1)){vu|=1<<w;pl[n2++]=w;}}}
   for(int p=0;p<n2;p++){int x=pl[p];signed char w2[N];memcpy(w2,v,N);w2[x]=v[i];w2[i]=0;long r2=rang(w2);
    if(d[r2]==255){d[r2]=dd+1;memcpy(et+(size_t)r2*N,w2,N);f[q++]=r2;}}}}
 int montre=0;const char*NOMS="ABCDEFGHIJKL";
 for(long i=0;i<NE&&montre<6;i++) if(d[i]==45){
   signed char*v=et+(size_t)i*N;printf("  position a 45 coups : ");
   for(int k=0;k<N;k++) if(v[k]) printf("%c=%d ",NOMS[k],v[k]);
   printf("\n");montre++;}
 return 0;}
