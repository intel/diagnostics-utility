# How to build the project

## Install dependencies

Use Ubuntu 20.04

Project dependencies:

  1. Follow https://dgpu-docs.intel.com/installation-guides/ubuntu/ubuntu-focal.html
  2. Install OpenCL SDK - https://software.intel.com/content/www/us/en/develop/tools/opencl-sdk.html
  3. Install sqlite - sudo apt-get install -y libsqlite3-dev

Documentation dependencies:

  1. Run the following command:

     ```
     pip install -r docs/requirements.txt
     ```


## Build options

Cmake build options:

  1. `-DDEV_PACKAGE=ON` (`OFF` by default). Install examples to package.
  2. `-DBUILD_TESTS=ON` (`OFF` by default). Install unit and integration tests to package.
  3. `-DCOVERAGE=ON` (`OFF` by default). Add --coverage flag to C/CPP compilers.
  4. `-BUILD_DOCS=ON` (`OFF` by default). Install HTML documentation to package.

## Build procudure

From root folder

1. Create `build` directory

   ```
   mkdir build
   ```

2. Go to `build` directory

   ```
   cd build
   ```

3. Create the build files

   ```
   cmake ..
   ```

4. Compile C checks and install tool

   ```
   make install
   ```

   **Note:** `install` folder should be packed in `build` directory
