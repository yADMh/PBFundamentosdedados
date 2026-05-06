#include <stdio.h>
#include <omp.h>

void print_array(int a[], int l, int r) {
    for(int i = l; i <= r; i++)
        printf("%d ", a[i]);
    printf("\n");
}

void merge(int a[], int l, int m, int r) {
    int i=l, j=m+1, k=0;
    int temp[1000];

    printf("Thread %d fazendo merge de [%d-%d] e [%d-%d]\n",
           omp_get_thread_num(), l, m, m+1, r);

    while(i<=m && j<=r)
        temp[k++] = (a[i] < a[j]) ? a[i++] : a[j++];

    while(i<=m) temp[k++] = a[i++];
    while(j<=r) temp[k++] = a[j++];

    for(i=l, k=0; i<=r; i++, k++)
        a[i] = temp[k];

    printf("Resultado do merge [%d-%d]: ", l, r);
    print_array(a, l, r);
}

void merge_sort(int a[], int l, int r) {
    if(l >= r) return;

    int m = (l+r)/2;

    printf("Thread %d dividindo [%d-%d]\n",
           omp_get_thread_num(), l, r);

    #pragma omp task
    merge_sort(a, l, m);

    #pragma omp task
    merge_sort(a, m+1, r);

    #pragma omp taskwait
    merge(a, l, m, r);
}

int main() {
    int arr[8] = {8,3,7,1,9,2,6,5};

    printf("Array original: ");
    print_array(arr, 0, 7);

    double start = omp_get_wtime();

    #pragma omp parallel
    {
        #pragma omp single
        merge_sort(arr, 0, 7);
    }

    double end = omp_get_wtime();

    printf("\nArray ordenado: ");
    print_array(arr, 0, 7);

    printf("Tempo de execucao: %f segundos\n", end - start);

    return 0;
}