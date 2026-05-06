#include <stdio.h>
#include <stdlib.h>

#define CAP 4

typedef struct {
    float x, y;
} Point;

typedef struct Node {
    float xmin, xmax, ymin, ymax;
    Point points[CAP];
    int count;

    struct Node *nw, *ne, *sw, *se;
} Node;

Node* create(float xmin, float xmax, float ymin, float ymax){
    Node* n = malloc(sizeof(Node));
    n->xmin=xmin; n->xmax=xmax;
    n->ymin=ymin; n->ymax=ymax;
    n->count=0;
    n->nw=n->ne=n->sw=n->se=NULL;

    printf("Criado no: [%.0f,%.0f] x [%.0f,%.0f]\n", xmin, xmax, ymin, ymax);

    return n;
}

void subdivide(Node* n){
    float mx = (n->xmin+n->xmax)/2;
    float my = (n->ymin+n->ymax)/2;

    printf("Dividindo no: [%.0f,%.0f] x [%.0f,%.0f]\n",
           n->xmin, n->xmax, n->ymin, n->ymax);

    n->nw = create(n->xmin,mx,my,n->ymax);
    n->ne = create(mx,n->xmax,my,n->ymax);
    n->sw = create(n->xmin,mx,n->ymin,my);
    n->se = create(mx,n->xmax,n->ymin,my);
}

int contains(Node* n, Point p){
    return (p.x >= n->xmin && p.x <= n->xmax &&
            p.y >= n->ymin && p.y <= n->ymax);
}

void insert(Node* n, Point p){
    if(!contains(n,p)) return;

    if(n->count < CAP){
        n->points[n->count++] = p;
        printf("Ponto (%.0f,%.0f) inserido em [%0.f,%0.f]\n",
               p.x,p.y,n->xmin,n->xmax);
        return;
    }

    if(!n->nw){
        subdivide(n);
    }

    insert(n->nw,p);
    insert(n->ne,p);
    insert(n->sw,p);
    insert(n->se,p);
}

void print_tree(Node* n, int level){
    if(!n) return;

    printf("Nivel %d | Região [%.0f,%.0f] x [%.0f,%.0f] | Pontos: %d\n",
           level, n->xmin, n->xmax, n->ymin, n->ymax, n->count);

    for(int i=0;i<n->count;i++){
        printf("   (%.0f,%.0f)\n", n->points[i].x, n->points[i].y);
    }

    print_tree(n->nw, level+1);
    print_tree(n->ne, level+1);
    print_tree(n->sw, level+1);
    print_tree(n->se, level+1);
}

int main(){
    Node* root = create(0,1000,0,1000);

    Point pts[] = {
        {100,200}, {300,400}, {700,800},
        {150,250}, {600,700}, {900,950},
        {50,50}, {800,100}
    };

    for(int i=0;i<8;i++){
        insert(root, pts[i]);
    }

    printf("\n--- Estrutura da Quadtree ---\n");
    print_tree(root, 0);

    return 0;
}