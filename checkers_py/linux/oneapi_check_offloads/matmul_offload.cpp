/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define MAX 128
int A[MAX][MAX], B[MAX][MAX], C[MAX][MAX], C_SERIAL[MAX][MAX];

typedef int BOOL;
typedef int TYPE;

BOOL check_result(TYPE *actual, TYPE *expected, unsigned n) {
    for (unsigned i = 0; i < n; i++) {
        if(actual[i] != expected[i]) {
            printf("Value mismatch at index = %d. Expected: %d"
                   ", Actual: %d.\n", i, expected[i], actual[i]);
            return 0;
        }
    }
    return 1;
}

void __attribute__ ((noinline)) Compute() {
    #pragma omp target teams distribute parallel for map(to: A, B) map(tofrom: C) thread_limit(128)
    {
        for (int i = 0; i < MAX; i++) {
            for (int j = 0; j < MAX; j++) {
                for (int k = 0; k < MAX; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
}

int main() {
    for (int i = 0; i < MAX; i++) {
        for (int j = 0; j < MAX; j++) {
            A[i][j] = i + j - 1;
            B[i][j] = i - j + 1;
        }
    }

    for (int i = 0; i < MAX; i++) {
        for (int j = 0; j < MAX; j++) {
            for (int k = 0; k < MAX; k++) {
                C_SERIAL[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    Compute();

    if (!check_result((int*) &C[0][0], (int*) &C_SERIAL[0][0], MAX * MAX)) {
        printf("    !!! FAILED\n");
        return 1;
    }

    printf("        PASSED\n");
    return 0;
}
