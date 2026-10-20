/* IDA* exact pour le chenil : 20 chiens, 5 chenils vides, pas orthogonaux.
   ./chenil LIMMAX c1 ... c20   (ci = chenil final du chien i) */
#include <stdio.h>
#include <stdlib.h>
int but[21],occ[25],nb[25][4],nn[25],man[25][25];long noeuds;int ligne[200][2];
int dfs(int g,int lim,int h,int dern){
  if(h==0)return 1; if(g+h>lim)return 0; noeuds++;
  for(int v=0;v<25;v++)if(!occ[v])for(int k=0;k<nn[v];k++){int c=nb[v][k];int d=occ[c];if(!d||d==dern)continue;
    int nh=h-man[c][but[d]]+man[v][but[d]]; if(g+1+nh>lim)continue;
    occ[v]=d;occ[c]=0;ligne[g][0]=d;ligne[g][1]=v;
    if(dfs(g+1,lim,nh,d))return 1; occ[c]=d;occ[v]=0;}
  return 0;}
int main(int argc,char**argv){int lmax=atoi(argv[1]);
  for(int a=0;a<25;a++){nn[a]=0;for(int b=0;b<25;b++){int dr=abs(a/5-b/5),dc=abs(a%5-b%5);man[a][b]=dr+dc;if(dr+dc==1)nb[a][nn[a]++]=b;}}
  for(int i=1;i<=20;i++)but[i]=atoi(argv[1+i])-1;
  for(int c=0;c<25;c++)occ[c]=c<20?c+1:0;
  int h=0;for(int i=1;i<=20;i++)h+=man[i-1][but[i]];
  for(int lim=h;lim<=lmax;lim+=2){noeuds=0;int r=dfs(0,lim,h,0);fprintf(stderr,"  limite %d : %s (%ld)\n",lim,r?"OK":"rien",noeuds);
    if(r){printf("%d",lim);for(int i=0;i<lim;i++)printf(" %d-%d",ligne[i][0],ligne[i][1]+1);printf("\n");return 0;}}
  printf("aucune <= %d\n",lmax);return 0;}
