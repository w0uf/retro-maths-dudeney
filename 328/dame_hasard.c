/* recherche au hasard guidée : à chaque coup, on tire parmi les coups qui couvrent le plus de cases neuves
   (ou presque le plus). ./hasard DEPART N ESSAIS [ferme] */
#include <stdio.h>
#include <stdlib.h>
int DX[8]={1,1,0,-1,-1,-1,0,1},DY[8]={0,1,1,1,0,-1,-1,-1};
int main(int argc,char**argv){int dep=atoi(argv[1]),N=atoi(argv[2]);long E=atol(argv[3]);int ferme=argc>4;srand(argc>5?atoi(argv[5]):1917);
  for(long e=0;e<E;e++){int vu[64]={0},nvu=1,s=dep,ch[40];vu[dep]=1;ch[0]=dep;
    for(int g=0;g<N;g++){int cd[64],ck[64],cn[64],nc=0,best=0;
      for(int d=0;d<8;d++){int x=s%8,y=s/8,neuf=0;for(int k=1;k<8;k++){x+=DX[d];y+=DY[d];if(x<0||x>7||y<0||y>7)break;if(!vu[y*8+x])neuf++;cd[nc]=d;ck[nc]=k;cn[nc]=neuf;nc++;if(neuf>best)best=neuf;}}
      int seuil=best-(rand()%3); int L[64],nl=0; for(int i=0;i<nc;i++)if(cn[i]>=seuil&&cn[i]>0)L[nl++]=i; if(!nl)for(int i=0;i<nc;i++)L[nl++]=i;
      int i=L[rand()%nl]; int x=s%8,y=s/8; for(int k=1;k<=ck[i];k++){x+=DX[cd[i]];y+=DY[cd[i]];if(!vu[y*8+x]){vu[y*8+x]=1;nvu++;}} s=y*8+x; ch[g+1]=s;
      if(nvu==64&&(!ferme||s==dep)&&g+1==N){printf("essai %ld : %d coups :",e,N);for(int j=0;j<=N;j++)printf(" %c%d","abcdefgh"[ch[j]%8],ch[j]/8+1);printf("\n");return 0;}
      if(nvu==64&&!ferme){printf("essai %ld : %d coups (moins que %d) :",e,g+1,N);for(int j=0;j<=g+1;j++)printf(" %c%d","abcdefgh"[ch[j]%8],ch[j]/8+1);printf("\n");return 0;}
    }}
  printf("rien en %ld essais\n",E);}
