#include <fstream>
#include <vector>

#define cin fin
#define cout fout
std::ifstream cin("disjoint.in");
std::ofstream cout("disjoint.out");

std::vector<int> parent(100001,0),size(100001,0);
int a, x, y, mult, op;

int getRoot(int u)
{ if(parent[u]==u)
    return u;
  else return parent[u]=getRoot(parent[u]);
}
void join(int u, int v)
{ u=getRoot(u);
  v=getRoot(v);
  if(size[u]>size[v])
    std::swap(u,v);
  parent[v]=u;
  size[u]+=size[v];
}

int main(){
 freopen("disjoint.in", "r", stdin);
 freopen("disjoint.out", "w", stdout);

 cin>>mult>>op;

 for(int i=1;i<=mult;i++)parent[i]=i,size[i]=1;

 while(op)
 { cin>>a>>x>>y;
   if(a==1)join(x,y);
   else if(getRoot(x)==getRoot(y))cout<<"DA\n";
        else cout<<"NU\n";
   op--;
 }
 return 0;
}