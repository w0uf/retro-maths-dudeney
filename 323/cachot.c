/* n° 323 A DUNGEON PUZZLE : chemin case par case sur les 64 cellules, départ imposé, arrivée libre,
   le plus de lignes droites possible. Une « ligne droite » = un segment maximal ; un chemin de 63 pas a
   63 - k lignes, où k = nombre de fois où l'on continue tout droit. On cherche les chemins avec k <= K.
   ./cachot DEPART K */
#include <stdio.h>
#include <stdlib.h>
int vu[64],K;long nsol,noeuds;int seq[64];int DX[4]={1,-1,0,0},DY[4]={0,0,1,-1};int best=99;
int connexe(int s,int n){int st[64],sp=0,m[64]={0},k=0,imp=0,st0=-1;
  for(int i=0;i<64;i++)if(!vu[i]){st0=i;break;} if(st0<0)return 1; st[sp++]=st0;m[st0]=1;
  while(sp){int c=st[--sp];k++;int x=c%8,y=c/8,deg=0;
    for(int d=0;d<4;d++){int nx=x+DX[d],ny=y+DY[d];if(nx<0||nx>7||ny<0||ny>7)continue;int t=ny*8+nx;
      if(t==s)deg++; if(vu[t])continue; deg++; if(!m[t]){m[t]=1;st[sp++]=t;}}
    if(deg<=1)imp++;}
  return k==64-n&&imp<=1;}
void dfs(int s,int dir,int k,int n){noeuds++;
  if(n==64){nsol++; if(k<best)best=k; if(nsol<=2){printf("  %d lignes :",63-k);for(int i=0;i<64;i++)printf(" %c%d","abcdefgh"[seq[i]%8],seq[i]/8+1);printf("\n");}return;}
  if(!connexe(s,n))return;
  int x=s%8,y=s/8;
  for(int d=0;d<4;d++){int nx=x+DX[d],ny=y+DY[d];if(nx<0||nx>7||ny<0||ny>7||vu[ny*8+nx])continue;
    int nk=k+(d==dir); if(nk>K)continue; int t=ny*8+nx;vu[t]=1;seq[n]=t;dfs(t,d,nk,n+1);vu[t]=0;}}
int main(int argc,char**argv){int s=atoi(argv[1]);K=atoi(argv[2]);vu[s]=1;seq[0]=s;dfs(s,-1,0,1);
  printf("départ %d, au plus %d tout-droit : %ld chemins (%ld noeuds)\n",s,K,nsol,noeuds);}
