/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and
your use of them is governed by the express license under which they were
provided to you (License). Unless the License provides otherwise, you may not
use, modify, copy, publish, distribute, disclose or transmit this software or
the related documents without Intel's prior written permission. This software
and the related documents are provided as is, with no express or implied
warranties, other than those that are expressly stated in the License.

*******************************************************************************/

#include <CL/sycl.hpp>
#include <iostream>

static const unsigned int DIM0 = 8;

int main(void) {
  using namespace cl::sycl;

  int in[DIM0];
  int out[DIM0];

  /* Initialize the input */
  for (unsigned int i = 0; i < DIM0; i++) {
    in[i] = i + 123;
  }

  // Open an extra scope to enforce waiting on the kernel
  {
    queue deviceQueue;
    range<1> dataRange{DIM0};
    buffer<int, 1> bufferIn{&in[0], dataRange};
    buffer<int, 1> bufferOut{&out[0], dataRange};

    deviceQueue.submit([&](handler& cgh) {
      auto accessorIn = bufferIn.get_access<access::mode::read>(cgh);
      auto accessorOut = bufferOut.get_access<access::mode::write>(cgh);

      cgh.parallel_for<class kernel>(dataRange, [=](id<1> wiID) {
        int dim0 = wiID[0]; /* kernel-first-line */
        int in_elem = accessorIn[wiID];
        accessorOut[wiID] = in_elem + 100; /* kernel-last-line */
      });
    });
  }

  /* Verify the output */
  for (unsigned int i = 0; i < DIM0; i++) {
    if (out[i] != in[i] + 100) {
      std::cout << "    !!! FAILED - Element " << i << " is " << out[i]
                << std::endl;
      return 1;
    }
  }

  std::cout << "        PASSED" << std::endl;
  return 0;
}
