/* n° 325 AN EPISCOPAL VISITATION : le fou doit passer sur les 32 cases blanches ; il peut repasser sur une case,
   jamais deux fois entre les deux mêmes cases voisines. Recherche exhaustive du plus petit nombre de coups.
   Coupure (admissible) : une case blanche du bord ne peut pas être traversée, elle est forcément le bout d'un coup ;
   il faut donc au moins un coup par case de bord encore jamais atteinte.
   ./eveque LIM [libre] : cherche depuis chaque case blanche un trajet en LIM coups au plus, et les compte. */
#include <stdio.h>
#include <stdlib.h>
int bord(int s){int x=s%8,y=s/8;return x==0||x==7||y==0||y==7;}
int blanc(int s){return (s%8+s/8)%2==1;}
unsigned char ar[64][4]; int DX[4]={1,1,-1,-1},DY[4]={1,-1,1,-1},OPP[4]={3,2,1,0};
int cnt[64],nvu,nbr,lim,libre; long nsol; int chemin[64],dep;
void dfs(int s,int g){
  if(nvu==32){ nsol++; if(getenv("TOUS")||nsol<=3){printf("  trajet en %d coups :",g);for(int i=0;i<=g;i++)printf(" %c%d","abcdefgh"[chemin[i]%8],chemin[i]/8+1);printf("\n");} return; }
  if(g+nbr>lim||g>=lim)return;
  for(int d=0;d<4;d++){
    int cur=s,k=0,pas[8];
    while(1){int x=cur%8+DX[d],y=cur/8+DY[d]; if(x<0||x>7||y<0||y>7||(!libre&&ar[cur][d]))break;
      int t=y*8+x; ar[cur][d]=1; ar[t][OPP[d]]=1; if(cnt[t]++==0){nvu++; if(bord(t))nbr--;}
      pas[k++]=t; chemin[g+1]=t; dfs(t,g+1); cur=t;}
    for(int i=k-1;i>=0;i--){int t=pas[i],p=i?pas[i-1]:s; if(--cnt[t]==0){nvu--; if(bord(t))nbr++;} ar[p][d]=0; ar[t][OPP[d]]=0;}
  }}
int main(int argc,char**argv){lim=atoi(argv[1]);libre=argc>2; /* libre : sans la règle des cases voisines */long tot=0;
  for(int s=0;s<64;s++)if(blanc(s)){
    for(int i=0;i<64;i++)cnt[i]=0; nvu=1;cnt[s]=1;nbr=0;for(int i=0;i<64;i++)if(blanc(i)&&bord(i)&&i!=s)nbr++;
    nsol=0;chemin[0]=s;dfs(s,0);
    if(nsol)printf("départ %c%d : %ld trajet(s) en %d coups au plus\n","abcdefgh"[s%8],s/8+1,nsol,lim);tot+=nsol;}
  printf("total : %ld\n",tot);}
