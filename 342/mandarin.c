/* n° 342 THE MANDARIN'S PUZZLE : IDA* exact. ./mandarin [fixes] : fixes=1 interdit de bouger les pions déjà en place */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int X[25]={2,2,3,4,1,2,3,4,5,6,1,2,3,4,5,0,1,2,3,4,5,2,3,4,4};
static const int Y[25]={0,1,1,1,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4,5,5,5,6};
/* départ, en ordre de lecture (cases 0..24) ; 0 = vide */
static const int D0[25]={16,11,3,13,22,6,7,8,9,21,19,12,4,14,15,5,17,18,2,20,1,10,23,24,0};
int nb[25][8],nn[25],dist[25][25],pos[25],but[26],fixe[26],FIX; int ligne[64];long noeuds;
int h(void){int s=0;for(int c=0;c<25;c++)if(pos[c])s+=dist[c][but[pos[c]]];return s;}
int dfs(int vide,int g,int lim,int hh,int prec){
  if(hh==0)return 1; if(g+hh>lim)return 0; noeuds++;
  for(int k=0;k<nn[vide];k++){int c=nb[vide][k];int p=pos[c]; if(p==prec)continue; if(FIX&&fixe[p])continue;
    int nh=hh-dist[c][but[p]]+dist[vide][but[p]];
    pos[vide]=p;pos[c]=0;ligne[g]=p;
    if(dfs(c,g+1,lim,nh,p))return 1;
    pos[c]=p;pos[vide]=0;}
  return 0;}
int main(int argc,char**argv){FIX=argc>1?atoi(argv[1]):0;
  for(int a=0;a<25;a++){nn[a]=0;for(int b=0;b<25;b++){int dx=abs(X[a]-X[b]),dy=abs(Y[a]-Y[b]);if(dx*dy==2)nb[a][nn[a]++]=b;}}
  for(int a=0;a<25;a++){for(int b=0;b<25;b++)dist[a][b]=99;dist[a][a]=0;int q[25],t=0,f=0;q[t++]=a;while(f<t){int u=q[f++];for(int k=0;k<nn[u];k++){int v=nb[u][k];if(dist[a][v]==99){dist[a][v]=dist[a][u]+1;q[t++]=v;}}}}
  for(int c=0;c<24;c++)but[c+1]=c; /* le pion n va sur la case n-1 */
  int vide=0;for(int c=0;c<25;c++){pos[c]=D0[c];if(!D0[c])vide=c;if(D0[c]&&but[D0[c]]==c)fixe[D0[c]]=1;}
  printf("pions déjà en place :");for(int p=1;p<=24;p++)if(fixe[p])printf(" %d",p);printf("\n");
  int h0=h();printf("borne de départ (somme des distances de cavalier) : %d\n",h0);
  for(int lim=h0;lim<=60;lim+=2){noeuds=0;int r=dfs(vide,0,lim,h0,-1);printf("limite %d : %s (%ld noeuds)\n",lim,r?"TROUVÉ":"rien",noeuds);fflush(stdout);
    if(r){printf("solution :");for(int i=0;i<lim;i++){printf(" %d",ligne[i]);if(!ligne[i+1]&&i+1<lim)break;}printf("\n");break;}}
}
