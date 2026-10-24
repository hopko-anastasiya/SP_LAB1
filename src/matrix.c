#include <stdio.h>
#include <stdlib.h>

#define N 1200

float A[N][N];
float B[N][N];
float C[N][N];

void init_matrices() {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = (float)(i + j) * 0.001f;
            B[i][j] = (float)(i - j) * 0.001f;
            C[i][j] = 0.0f;
        }
    }
}

void multiply_matrices() {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main() {
    printf("Ініціалізація матриць %dx%d...\n", N, N);
    init_matrices();

    printf("Початок множення...\n");
    multiply_matrices();

    printf("Завершено! Контрольне значення C[0][0] = %f\n", C[0][0]);
    return 0;
}
