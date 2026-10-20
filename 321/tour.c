/* Trajets de tour case par case sur un échiquier (chemin hamiltonien du quadrillage), comptés en « coups »
   = segments droits ; un coup se termine forcément par un virage.
   ./tour MAXSEG DEPART [CASE10 FIN]   cases notées 0..63, x = colonne a..h, y = rangée 1..8 (case = 8*y + x).
   Avec CASE10 et FIN : le 10e coup finit sur CASE10, le dernier coup sur FIN (problème 321). */
#include <stdio.h>
#include <stdlib.h>
int vu[64],maxseg,c10=-1,fin=-1;long nsol,noeuds;int seq[64];
int DX[4]={1,-1,0,0},DY[4]={0,0,1,-1};
int libre(int x,int y){return x>=0&&x<8&&y>=0&&y<8&&!vu[y*8+x];}
int connexe(int s,int n){ /* les cases libres restent-elles d'un seul tenant, avec au plus une impasse ? */
  int st[64],sp=0,m[64]={0},k=0,imp=0; int st0=-1;
  for(int i=0;i<64;i++)if(!vu[i]){st0=i;break;} if(st0<0)return 1;
  st[sp++]=st0;m[st0]=1;
  while(sp){int c=st[--sp];k++;int x=c%8,y=c/8,deg=0;
    for(int d=0;d<4;d++){int nx=x+DX[d],ny=y+DY[d];if(nx<0||nx>7||ny<0||ny>7)continue;int t=ny*8+nx;
      if(t==s)deg++; if(vu[t])continue; deg++; if(!m[t]){m[t]=1;st[sp++]=t;}}
    if(deg<=1)imp++;}
  return k==64-n && imp<=1;}
void dfs(int s,int dir,int seg,int n){
  noeuds++;
  if(n==64){ if(fin>=0&&s!=fin)return; if(seg>maxseg)return; nsol++;
    if(getenv("TOUS")||nsol<=2){printf("  %d coups :",seg);for(int i=0;i<64;i++)printf(" %c%d","abcdefgh"[seq[i]%8],seq[i]/8+1);printf("\n");} return;}
  if(!connexe(s,n))return;
  int x=s%8,y=s/8;
  for(int d=0;d<4;d++){int nx=x+DX[d],ny=y+DY[d];if(!libre(nx,ny))continue;
    int ns=seg+(d!=dir); if(ns>maxseg)continue;
    /* contrainte du 10e coup : on ne peut quitter CASE10 qu'en tournant, et CASE10 termine le coup n° 10 */
    if(c10>=0){ if(s==c10&&(d==dir||seg!=10))continue; if(s!=c10&&d!=dir&&seg==10)continue; }
    int t=ny*8+nx; vu[t]=1;seq[n]=t; dfs(t,d,ns,n+1); vu[t]=0;}
}
int main(int argc,char**argv){maxseg=atoi(argv[1]);int s=atoi(argv[2]);if(argc>4){c10=atoi(argv[3]);fin=atoi(argv[4]);}
  if(argc>5){ /* 322 : aller-retour depuis la case de départ vers la case X = argv[5], puis on repart */
    int X=atoi(argv[5]); vu[s]=1;vu[X]=1;seq[0]=X;seq[1]=s; int d=(X%8==s%8)?(X/8<s/8?2:3):(X%8<s%8?0:1); /* direction X -> s */
    dfs(s,d,2,2);
  } else { vu[s]=1;seq[0]=s; dfs(s,-1,0,1); } printf("trajets en %d coups au plus : %ld (%ld noeuds)\n",maxseg,nsol,noeuds);}
