#include <stdio.h>
#include <stdlib.h>

typedef struct Trie {
    struct Trie *left, *right;
    int id;
} Trie;

Trie* new_node(){
    Trie* n = malloc(sizeof(Trie));
    n->left = n->right = NULL;
    n->id = -1;
    return n;
}

void insert(Trie* root, unsigned int ip, int prefix, int id){
    Trie* cur = root;

    printf("\nInserindo prefixo (ID=%d, /%d):\n", id, prefix);

    for(int i=31;i>=32-prefix;i--){
        int bit = (ip >> i) & 1;
        printf("Bit %d -> %d\n", i, bit);

        if(bit==0){
            if(!cur->left){
                cur->left = new_node();
                printf("  Criou nó à esquerda\n");
            }
            cur = cur->left;
        } else {
            if(!cur->right){
                cur->right = new_node();
                printf("  Criou nó à direita\n");
            }
            cur = cur->right;
        }
    }

    cur->id = id;
    printf(">> Prefixo armazenado com ID %d\n", id);
}

int lookup(Trie* root, unsigned int ip){
    Trie* cur = root;
    int last = -1;

    printf("\nBuscando IP:\n");

    for(int i=31;i>=0;i--){
        if(cur->id != -1){
            last = cur->id;
            printf("  Encontrou prefixo válido (ID=%d)\n", last);
        }

        int bit = (ip >> i) & 1;
        printf("Bit %d -> %d\n", i, bit);

        if(bit==0){
            if(!cur->left){
                printf("  Caminho terminou\n");
                break;
            }
            cur = cur->left;
        } else {
            if(!cur->right){
                printf("  Caminho terminou\n");
                break;
            }
            cur = cur->right;
        }
    }

    return last;
}

int main(){
    Trie* root = new_node();

    // Inserções
    insert(root, 0xC0A80000,16,10); //192.168.0.0/16
    insert(root, 0xC0A80100,24,20); //192.168.1.0/24

    // Busca
    int result = lookup(root, 0xC0A80105); //192.168.1.5

    printf("\nResultado final (LPM): %d\n", result);

    return 0;
}