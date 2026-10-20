/* Rétro Math's — n° 350 THE FORSAKEN KING (Dudeney, 1917).
   Solveur exhaustif « mat en n » : armée blanche complète contre roi noir seul.
   Cases 0..63, a1 = 0, h8 = 63. Promotion (D, T, F, C), roque, prise par le roi noir : tout est géré.
   gcc -O2 -o roi_abandonne roi_abandonne.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
enum {VIDE, P, N, B, R, Q, K};
typedef struct { signed char c[64]; int bk; int roqK, roqQ; } Pos;
static int F(int s){return s&7;} static int Rg(int s){return s>>3;}
static const int KN[8][2]={{1,2},{2,1},{-1,2},{-2,1},{1,-2},{2,-1},{-1,-2},{-2,-1}};
static const int KG[8][2]={{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
/* la case s est-elle attaquée par les Blancs ? (le roi noir est transparent : on l'ignore comme écran) */
static int attaquee(const Pos*p,int s){
  int f=F(s), r=Rg(s), i,k;
  if(r>0){ if(f>0 && p->c[s-9]==P) return 1; if(f<7 && p->c[s-7]==P) return 1; }
  for(i=0;i<8;i++){ int x=f+KN[i][0], y=r+KN[i][1]; if(x>=0&&x<8&&y>=0&&y<8&&p->c[y*8+x]==N) return 1; }
  for(i=0;i<8;i++){ int x=f+KG[i][0], y=r+KG[i][1]; if(x>=0&&x<8&&y>=0&&y<8&&p->c[y*8+x]==K) return 1; }
  for(i=0;i<8;i++){ int dx=KG[i][0], dy=KG[i][1], x=f+dx, y=r+dy;
    while(x>=0&&x<8&&y>=0&&y<8){ int t=y*8+x, c=p->c[t];
      if(c){ if(c==Q || (i<4&&c==R) || (i>=4&&c==B)) return 1; break; }
      if(t==p->bk){ x+=dx; y+=dy; continue; }      /* transparent */
      x+=dx; y+=dy; } }
  (void)k; return 0;
}
static int wk(const Pos*p){int i;for(i=0;i<64;i++) if(p->c[i]==K) return i; return -1;}
static int adj(int a,int b){int dx=abs(F(a)-F(b)),dy=abs(Rg(a)-Rg(b));return dx<=1&&dy<=1;}
typedef struct { unsigned char de, a, promo, roque; } Coup;
static int gen_blancs(const Pos*p, Coup*L){
  int n=0,s,i;
  for(s=0;s<64;s++){ int c=p->c[s]; if(!c) continue; int f=F(s), r=Rg(s);
    if(c==P){ int t=s+8; if(t<64 && !p->c[t] && t!=p->bk){
        if(Rg(t)==7){ int q; for(q=Q;q>=N;q--){ L[n].de=s;L[n].a=t;L[n].promo=q;L[n].roque=0;n++; } }
        else { L[n].de=s;L[n].a=t;L[n].promo=0;L[n].roque=0;n++;
          if(r==1 && !p->c[s+16] && s+16!=p->bk){ L[n].de=s;L[n].a=s+16;L[n].promo=0;L[n].roque=0;n++; } } }
    } else if(c==N){ for(i=0;i<8;i++){ int x=f+KN[i][0], y=r+KN[i][1]; if(x<0||x>7||y<0||y>7) continue; int t=y*8+x;
        if(!p->c[t] && t!=p->bk){ L[n].de=s;L[n].a=t;L[n].promo=0;L[n].roque=0;n++; } }
    } else if(c==K){ for(i=0;i<8;i++){ int x=f+KG[i][0], y=r+KG[i][1]; if(x<0||x>7||y<0||y>7) continue; int t=y*8+x;
        if(!p->c[t] && t!=p->bk && !adj(t,p->bk)){ L[n].de=s;L[n].a=t;L[n].promo=0;L[n].roque=0;n++; } }
      if(s==4){ /* roques : cases libres, roi ni à côté du roi noir au départ, au passage, à l'arrivée */
        if(p->roqK && p->c[7]==R && !p->c[5] && !p->c[6] && p->bk!=5 && p->bk!=6 && !adj(4,p->bk) && !adj(5,p->bk) && !adj(6,p->bk)){ L[n].de=4;L[n].a=6;L[n].promo=0;L[n].roque=1;n++; }
        if(p->roqQ && p->c[0]==R && !p->c[1] && !p->c[2] && !p->c[3] && p->bk!=1 && p->bk!=2 && p->bk!=3 && !adj(4,p->bk) && !adj(3,p->bk) && !adj(2,p->bk)){ L[n].de=4;L[n].a=2;L[n].promo=0;L[n].roque=2;n++; } }
    } else { int d0=(c==B)?4:0, d1=(c==R)?4:8;
      for(i=d0;i<d1;i++){ int dx=KG[i][0], dy=KG[i][1], x=f+dx, y=r+dy;
        while(x>=0&&x<8&&y>=0&&y<8){ int t=y*8+x; if(p->c[t]||t==p->bk) break; L[n].de=s;L[n].a=t;L[n].promo=0;L[n].roque=0;n++; x+=dx; y+=dy; } } }
  }
  return n;
}
static void joue(Pos*p, Coup m){
  int c=p->c[m.de]; p->c[m.de]=VIDE; p->c[m.a]=m.promo?m.promo:c;
  if(m.roque==1){ p->c[7]=VIDE; p->c[5]=R; } if(m.roque==2){ p->c[0]=VIDE; p->c[3]=R; }
  if(c==K){ p->roqK=p->roqQ=0; } if(m.de==7) p->roqK=0; if(m.de==0) p->roqQ=0;
}
static int gen_noirs(const Pos*p, int*L){ /* cases d'arrivée du roi noir */
  int n=0,i,f=F(p->bk),r=Rg(p->bk);
  for(i=0;i<8;i++){ int x=f+KG[i][0], y=r+KG[i][1]; if(x<0||x>7||y<0||y>7) continue; int t=y*8+x;
    if(p->c[t]==K) continue;
    Pos q=*p; q.c[t]=VIDE; q.bk=t;                 /* prise éventuelle */
    if(t==7||p->c[t]==R){ if(t==7) q.roqK=0; if(t==0) q.roqQ=0; }
    if(!attaquee(&q,t)) L[n++]=t; }
  return n;
}
/* table de transposition */
#define TT (1<<24)
static uint64_t cles[TT]; static signed char ok_n[TT], non_n[TT];
static uint64_t hache(const Pos*p){ uint64_t h=1469598103934665603ULL; int i;
  for(i=0;i<64;i++){ h^=(uint64_t)(p->c[i]+1); h*=1099511628211ULL; }
  h^=p->bk+100; h*=1099511628211ULL; h^=p->roqK*2+p->roqQ+7; h*=1099511628211ULL; return h?h:1; }
static long noeuds=0;
static int mat_en(Pos*p,int n);          /* trait aux Blancs : peuvent-ils mater en n coups au plus ? */
static int noirs_perdent(Pos*p,int n){   /* trait aux Noirs après un coup blanc ; n = coups blancs restants */
  int L[8], k=gen_noirs(p,L), i; int echec=attaquee(p,p->bk);
  if(k==0) return echec;                 /* mat, ou pat (= échec de la tentative) */
  if(n==0) return 0;
  for(i=0;i<k;i++){ Pos q=*p; int t=L[i]; if(q.c[t]){ if(t==7) q.roqK=0; if(t==0) q.roqQ=0; } q.c[t]=VIDE; q.bk=t;
    if(!mat_en(&q,n)) return 0; }
  return 1;
}
static int mat_en(Pos*p,int n){
  if(n==0) return 0; noeuds++;
  uint64_t h=hache(p); unsigned idx=(unsigned)(h&(TT-1));
  if(cles[idx]==h){ if(ok_n[idx] && ok_n[idx]<=n) return 1; if(non_n[idx]>=n) return 0; } else { cles[idx]=h; ok_n[idx]=0; non_n[idx]=0; }
  Coup L[256]; int k=gen_blancs(p,L), i;
  for(i=0;i<k;i++){ Pos q=*p; joue(&q,L[i]);
    if(noirs_perdent(&q,n-1)){ if(cles[idx]==h){ if(!ok_n[idx]||ok_n[idx]>n) ok_n[idx]=n; } return 1; } }
  if(cles[idx]==h && non_n[idx]<n) non_n[idx]=n; return 0;
}
static const char*NOM="?PNBRQK";
static void nom_coup(const Pos*p,Coup m,char*o){ if(m.roque){ strcpy(o,m.roque==1?"O-O":"O-O-O"); return; }
  sprintf(o,"%c%c%d-%c%d%s",NOM[(int)p->c[m.de]],'a'+F(m.de),1+Rg(m.de),'a'+F(m.a),1+Rg(m.a),m.promo?"=?":""); }
static void depart(Pos*p){ int i; memset(p,0,sizeof *p); const char init[8]={R,N,B,Q,K,B,N,R};
  for(i=0;i<8;i++){ p->c[i]=init[i]; p->c[8+i]=P; } p->bk=60; p->roqK=p->roqQ=1; }
/* carte : pour chaque case du roi noir, distance de mat exacte et nombre de premiers coups qui la conservent */
static void carte(void){
  int s, n, i; Pos p; Coup L[256]; char o[16];
  for(s=63;s>=0;s--){ depart(&p); if(p.c[s]) continue; p.bk=s;
    if(attaquee(&p,s)){ printf("%c%d : roi en échec au trait des Blancs (position illégale)\n",'a'+F(s),1+Rg(s)); continue; }
    for(n=1;n<=8;n++) if(mat_en(&p,n)) break;
    if(n>8){ printf("%c%d : pas de mat en 8\n",'a'+F(s),1+Rg(s)); continue; }
    int k=gen_blancs(&p,L), nb=0; char cles[400]=""; 
    for(i=0;i<k;i++){ Pos q=p; joue(&q,L[i]); if(noirs_perdent(&q,n-1)){ nb++; nom_coup(&p,L[i],o); if(strlen(cles)<300){ strcat(cles," "); strcat(cles,o); } } }
    printf("%c%d : mat en %d ; premiers coups gagnants : %d sur %d →%s\n",'a'+F(s),1+Rg(s),n,nb,k,cles); fflush(stdout); }
}
int main(int argc,char**argv){
  if(argc>1 && !strcmp(argv[1],"carte")){ carte(); return 0; }
  Pos p; depart(&p); Coup L[256]; int k=gen_blancs(&p,L), i, j; char o[16];
  printf("coups blancs au départ : %d\n",k);
  printf("mat en 5 ? %d | mat en 6 ? %d (noeuds %ld)\n", mat_en(&p,5), mat_en(&p,6), noeuds); fflush(stdout);
  printf("=== premier coup : lesquels gardent le mat en 6 ?\n");
  for(i=0;i<k;i++){ Pos q=p; joue(&q,L[i]); nom_coup(&p,L[i],o); long n0=noeuds; int r=noirs_perdent(&q,5);
    printf("   1. %-8s : %s (%ld noeuds)\n",o,r?"MAT EN 6":"pas de mat en 6",noeuds-n0); fflush(stdout); }
  /* deuxième coup après 1. e4 */
  Coup e4; e4.de=12; e4.a=28; e4.promo=0; e4.roque=0; Pos a=p; joue(&a,e4);
  int R1[8], kr=gen_noirs(&a,R1);
  printf("=== après 1. e4, pour chaque réponse noire : quels deuxièmes coups gardent le mat en 6 ?\n");
  for(j=0;j<kr;j++){ Pos b=a; b.c[R1[j]]=VIDE; b.bk=R1[j]; Coup M[256]; int km=gen_blancs(&b,M), nb=0;
    printf("   1... R%c%d :",'a'+F(R1[j]),1+Rg(R1[j]));
    for(i=0;i<km;i++){ Pos q=b; joue(&q,M[i]); if(noirs_perdent(&q,4)){ nom_coup(&b,M[i],o); printf(" %s",o); nb++; } }
    printf("  (%d sur %d)\n",nb,km); fflush(stdout); }
  /* l'arbre de Dudeney : 1. e4, 2. Dg4, puis les 3e et 4e coups qui gardent le mat en 6, réponse noire par réponse noire */
  printf("=== troisième et quatrième coups\n");
  for(j=0;j<kr;j++){ Pos b1=a; b1.c[R1[j]]=VIDE; b1.bk=R1[j]; Coup g4; g4.de=3; g4.a=30; g4.promo=0; g4.roque=0; joue(&b1,g4);
    int R2[8], k2=gen_noirs(&b1,R2), u;
    for(u=0;u<k2;u++){ Pos b2=b1; b2.c[R2[u]]=VIDE; b2.bk=R2[u]; Coup M[256]; int km=gen_blancs(&b2,M);
      printf("   1...R%c%d 2...R%c%d : 3e coup ->",'a'+F(R1[j]),1+Rg(R1[j]),'a'+F(R2[u]),1+Rg(R2[u]));
      for(i=0;i<km;i++){ Pos q=b2; joue(&q,M[i]); if(noirs_perdent(&q,3)){ nom_coup(&b2,M[i],o); printf(" %s",o);
          /* 4e coups après chaque réponse */
          int R3[8], k3=gen_noirs(&q,R3), v; printf(" [");
          for(v=0;v<k3;v++){ Pos b3=q; b3.c[R3[v]]=VIDE; b3.bk=R3[v]; Coup M4[256]; int k4=gen_blancs(&b3,M4), w; char o4[16];
            printf(" R%c%d:",'a'+F(R3[v]),1+Rg(R3[v]));
            for(w=0;w<k4;w++){ Pos q4=b3; joue(&q4,M4[w]); if(noirs_perdent(&q4,2)){ nom_coup(&b3,M4[w],o4); printf("%s,",o4); } } }
          printf(" ]"); } }
      printf("\n"); } }
  printf("noeuds au total : %ld\n",noeuds);
  return 0;
}
