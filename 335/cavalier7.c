/* Chemins de cavalier sur 7×7 visitant les 49 cases. ./cavalier7 DEPART FIN [n:case ...]
   cases 0..48, case = 7*rangée + colonne (rangée 0 = la plus basse). n:case impose la case du n-ième passage (1 = départ). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int dist[49][49],prochain[50];int nb[49][8],nn[49],vu[49],impose[50],ou[49];long nsol;int seq[50],fin;
void dfs(int s,int k){ /* s = case du k-ième passage */
  if(k==49){ if(s==fin){nsol++; if(nsol==1){printf("  premier :");for(int i=1;i<=49;i++)printf(" %c%d","abcdefg"[seq[i]%7],seq[i]/7+1);printf("\n");fflush(stdout);}} return;}
  if(s==fin)return;
  /* coupure : une case libre (autre que la fin) sans plus aucune issue = impasse */
  for(int i=0;i<nn[s];i++){int t=nb[s][i]; if(vu[t])continue;
    if(impose[k+1]>=0&&impose[k+1]!=t)continue; if(ou[t]>=0&&ou[t]!=k+1)continue;
    { int w=prochain[k+1]; if(w<=49){int c=impose[w]; if(dist[t][c]>w-(k+1))continue;} }
    vu[t]=1;seq[k+1]=t;
    /* coupure : toute case libre doit garder deux issues (vers une case libre ou vers t), sauf la case finale,
       et une seule peut n'en avoir qu'une (elle sera alors forcément la dernière) */
    int ok=1,impasse=0; for(int u=0;u<49&&ok;u++){ if(vu[u])continue; int d=0; for(int q=0;q<nn[u];q++){int v=nb[u][q]; if(!vu[v]||v==t)d++;}
      if(u==fin){ if(d==0)ok=0; continue; } if(d==0)ok=0; else if(d==1){ int seul_t=0; for(int q=0;q<nn[u];q++)if(nb[u][q]==t)seul_t=1; if(!seul_t)ok=0; else impasse++; } }
    if(impasse>1)ok=0;
    if(ok)dfs(t,k+1); vu[t]=0;}
}
int main(int argc,char**argv){int dep=atoi(argv[1]);fin=atoi(argv[2]);memset(impose,-1,sizeof impose);memset(ou,-1,sizeof ou);
  for(int i=3;i<argc;i++){int n,c;sscanf(argv[i],"%d:%d",&n,&c);impose[n]=c;ou[c]=n;}
  for(int a=0;a<49;a++){nn[a]=0;for(int b=0;b<49;b++){int dx=abs(a%7-b%7),dy=abs(a/7-b/7);if(dx*dy==2)nb[a][nn[a]++]=b;}}
  for(int a=0;a<49;a++){for(int b=0;b<49;b++)dist[a][b]=99;dist[a][a]=0;int q[49],h=0,t=0;q[t++]=a;while(h<t){int u=q[h++];for(int i=0;i<nn[u];i++){int v=nb[u][i];if(dist[a][v]==99){dist[a][v]=dist[a][u]+1;q[t++]=v;}}}}
  impose[49]=fin; { int w=99; for(int n=49;n>=1;n--){ prochain[n]=w; if(impose[n]>=0) w=n; } }
  vu[dep]=1;seq[1]=dep;dfs(dep,1);printf("chemins : %ld\n",nsol);}
