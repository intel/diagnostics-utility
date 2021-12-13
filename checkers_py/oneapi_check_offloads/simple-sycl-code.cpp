/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include <CL/sycl.hpp>
#include <iostream>

int main() {
    // Creating SYCL queue
    // cl::sycl::host_selector selector;
    // cl::sycl::queue deviceQueue(selector);
    // std::vector<cl::sycl::device> devices = cl::sycl::device::get_devices();
    // cl::sycl::queue deviceQueue(devices[selected_device_id]);
      
    cl::sycl::queue Queue;
    // cl::sycl::queue Queue(devices[1]);

    // Creating buffer of 4 ints
    cl::sycl::buffer<cl::sycl::cl_int, 1> Buffer(4);

    // Size of index space for kernel
    cl::sycl::range<1> NumOfWorkItems{Buffer.get_count()};

    // Submitting command group to queue
    Queue.submit([&](cl::sycl::handler &cgh) {
        // Getting write only access to the buffer on a device
        auto Accessor = Buffer.get_access<cl::sycl::access::mode::write>(cgh);
        // Executing kernel
        cgh.parallel_for<class FillBuffer>(NumOfWorkItems, [=](cl::sycl::id<1> WIid) {
            // Fill buffer with indexes
            Accessor[WIid] = (cl::sycl::cl_int)WIid.get(0);
        });
    });

    // Getting read only access to the buffer on the host
    const auto HostAccessor = Buffer.get_access<cl::sycl::access::mode::read>();

    // Check that the results are correct
    bool MismatchFound = false;
    for (size_t I = 0; I < Buffer.get_count(); ++I) {
        if (HostAccessor[I] != I) {
            std::cout << "    !!! FAILED - The result is incorrect for element: " << I
                      << " , expected: " << I << " , got: " << HostAccessor[I]
                      << std::endl;
            MismatchFound = true;
        }
    }

    if (!MismatchFound) {
        std::cout << "        PASSED" << std::endl;
    }

    return MismatchFound;
}
