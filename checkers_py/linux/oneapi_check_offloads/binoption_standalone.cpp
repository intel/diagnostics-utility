/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include <mathimf.h>
#include <stdlib.h>
#include <float.h>
#include <iostream>
#include <string.h>

inline void* w_malloc(size_t bytes) {return malloc(bytes);}
inline void  w_free(void* memory)   {free(memory);}

#ifndef VECTOR_LENGTH
#define VECTOR_LENGTH 16
#endif

#define RISKFREE 0.02f
#define VOLATILITY 0.30f

#define MAX_NUM_STEPS 255
#define NUM_STEPS_ROUND (MAX_NUM_STEPS + 1)
#define STEPS_CACHE_SIZE (NUM_STEPS_ROUND + VECTOR_LENGTH)

using namespace std;

class BinOption {
 public:
    int m_numSamples;
    int m_numSteps;
    float* m_randArray;
    float* m_outputArray;
    float* m_refOutputArray;
    bool open();
    bool validate();
    bool close();
    void execute_CPU();
    void execute_offload();
};

int main() {
    BinOption BO;

    if (!BO.open()) {
        cout << "FAILED open\n";
        exit(1);
    }

    //  cout << "\nBEGIN REFERENCE CPU RUN...\n";
    BO.execute_CPU();
    //  cout << "END REFERENCE CPU RUN.\n";

    //  cout << "\nBEGIN OFFLOAD RUN...\n";
    BO.execute_offload();
    //  cout << "END OFFLOAD RUN\n";

    if (!BO.validate()) {
        cout << "    !!! FAILED validate\n";
        exit(2);
    }

    if (!BO.close()) {
        cout << "    !!! FAILED close\n";
        exit(3);
    }

    cout << "        PASSED\n";
}


bool BinOption::open() {
   //m_numSamples = 131072; //large  dataset
   //m_numSamples = 32768;  //medium dataset
   //m_numSamples = 1024;   //small  dataset

    m_numSamples = 1024;
    m_numSteps   = 254;

    if (m_numSteps > MAX_NUM_STEPS) {
        cout << endl << "numSteps exceeded and defaulted to " << MAX_NUM_STEPS << endl;
        m_numSteps = MAX_NUM_STEPS;
    }

    // cout << endl << "numSamples = " << m_numSamples << endl << "numSteps = " << m_numSteps << endl;

    m_randArray = (float*)w_malloc(4*m_numSamples * sizeof(float));

    if (m_randArray == NULL) {
        std::cout << "Failed to allocate host memory. (randArray)\n";
        return false;
    }
    srand(2010);
    for (int i = 0; i < m_numSamples * 4; i++) {
        m_randArray[i] = (float) rand() / (float) RAND_MAX;
    }

    m_outputArray = (float*)w_malloc(4*m_numSamples * sizeof(float));
    if (m_outputArray == NULL) {
        std::cout << "Failed to allocate host memory. (output)\n";
        return false;
    }
    memset(m_outputArray, 0, 4*m_numSamples * sizeof(float));

    m_refOutputArray = (float*)w_malloc(4*m_numSamples * sizeof(float));
    if (m_refOutputArray == NULL) {
        std::cout << "Failed to allocate host memory. (refOutput)\n";
        return false;
    }
    memset(m_refOutputArray, 0, 4*m_numSamples * sizeof(float));

    return true;
}


bool BinOption::validate() {
    bool failed;
    failed = false;
    for (int i = 0; i < 4*m_numSamples; i++) {
        if (fabs(m_outputArray[i] - m_refOutputArray[i]) > 0.01f) {
            cout << m_outputArray[i] << " " << m_refOutputArray[i] << endl;
            failed = true;
        }
    }
    return !failed;
}


bool BinOption::close() {
    w_free(m_randArray);
    w_free(m_outputArray);
    w_free(m_refOutputArray);
    return true;
}


void BinOption::execute_offload() {
    float* inArr  = m_randArray;
    float* outArr = m_outputArray;
    int N = 4*m_numSamples;
    int numSteps = m_numSteps;

    #pragma omp target map(to: inArr[0:N]) map(from: outArr[0:N]) 
    #pragma omp parallel for
    for (int bid = 0; bid < N; ++bid) {
        float s;
        float x;
        float vsdt;
        float puByr;
        float pdByr;
        float optionYears;

        float inRand;

        inRand = inArr[bid];
        s = (1.0f - inRand) * 5.0f + inRand * 30.f;
        x = (1.0f - inRand) * 1.0f + inRand * 100.f;
        optionYears = (1.0f - inRand) * 0.25f + inRand * 10.f;
        float dt = optionYears * (1.0f / (float) numSteps);
        vsdt = VOLATILITY * sqrtf(dt);
        float rdt = RISKFREE * dt;
        float r = expf(rdt);
        float rInv = 1.0f / r;
        float u = expf(vsdt);
        float d = 1.0f / u;
        float pu = (r - d) / (u - d);
        float pd = 1.0f - pu;
        puByr = pu * rInv;
        pdByr = pd * rInv;

        float stepsArray[STEPS_CACHE_SIZE];
        for (int j = 0; j < STEPS_CACHE_SIZE; j++) {
            float profit = s * expf(vsdt * (2.0f * j - numSteps)) - x;
            stepsArray[j] = profit > 0.0f ? profit : 0.0f;
        }
        for (int j = 0; j < numSteps; j++) {
            for (int k = 0; k < NUM_STEPS_ROUND; ++k) {
                stepsArray[k] = pdByr * stepsArray[k + 1] + puByr * stepsArray[k];
            }
        }
        outArr[bid] = stepsArray[0];
    }
}

void BinOption::execute_CPU() {
    float* inArr  = m_randArray;
    float* outArr = m_refOutputArray;
    int N = 4*m_numSamples;
    #pragma omp parallel for
    for (int bid = 0; bid < N; ++bid) {
        float s;
        float x;
        float vsdt;
        float puByr;
        float pdByr;
        float optionYears;

        float inRand;
        float stepsArray[STEPS_CACHE_SIZE];

        inRand = inArr[bid];
        s = (1.0f - inRand) * 5.0f + inRand * 30.f;
        x = (1.0f - inRand) * 1.0f + inRand * 100.f;
        optionYears = (1.0f - inRand) * 0.25f + inRand * 10.f;
        float dt = optionYears * (1.0f / (float) m_numSteps);
        vsdt = VOLATILITY * sqrtf(dt);
        float rdt = RISKFREE * dt;
        float r = expf(rdt);
        float rInv = 1.0f / r;
        float u = expf(vsdt);
        float d = 1.0f / u;
        float pu = (r - d) / (u - d);
        float pd = 1.0f - pu;
        puByr = pu * rInv;
        pdByr = pd * rInv;
        //#pragma simd vectorlength(32)
        for (int j = 0; j <= m_numSteps; j++) {
            float profit = s * expf(vsdt * (2.0f * j - m_numSteps)) - x;
            stepsArray[j] = profit > 0.0f ? profit : 0.0f;
        }
        for (int j = m_numSteps; j > 0; --j) {
        //#pragma simd vectorlength(32)
            for (int k = 0; k <= j - 1; ++k) {
            //for (int k = 0; k <= m_numSteps - 1; ++k) {
                stepsArray[k] = pdByr * stepsArray[k + 1] + puByr * stepsArray[k];
            }
        }
        outArr[bid] = stepsArray[0];
    }
}
