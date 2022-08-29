/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "CLDriverChecker.h"



cl_int CL_API_CALL
(*fp_clGetPlatformIDs)(
				 cl_uint          num_entries,
                 cl_platform_id * platforms,
                 cl_uint *        num_platforms) = nullptr;

cl_int CL_API_CALL
(*fp_clGetPlatformInfo)(
				  cl_platform_id   platform,
                  cl_platform_info param_name,
                  size_t           param_value_size,
                  void *           param_value,
                  size_t *         param_value_size_ret) = nullptr;

cl_int CL_API_CALL
(*fp_clGetDeviceIDs)(
			   cl_platform_id   platform,
               cl_device_type   device_type,
               cl_uint          num_entries,
               cl_device_id *   devices,
               cl_uint *        num_devices) = nullptr;

cl_int CL_API_CALL
(*fp_clGetDeviceInfo)(
				cl_device_id    device,
                cl_device_info  param_name,
                size_t          param_value_size,
                void *          param_value,
                size_t *        param_value_size_ret) = nullptr;


CL_DriverChecker::CL_DriverChecker() {
	// TODO Auto-generated constructor stub

}

CL_DriverChecker::~CL_DriverChecker() {
	// TODO Auto-generated destructor stub
}


bool CL_DriverChecker::Load(string& message) {
    void *handle;
    char *error;
    stringstream ss;

    dlerror();    /* Clear any existing error */
    handle = dlopen("libOpenCL.so", RTLD_LAZY);
    if (!handle) {
    	ss << "OpenCL™ library loading error: " << dlerror();
        message = ss.str();
        return false;
    }

    *(void **) (&fp_clGetPlatformIDs) = dlsym(handle, "clGetPlatformIDs");
    error = dlerror();
    if (error != NULL) {
    	ss << "OpenCL™ library loading error: " << error;
        message = ss.str();
        return false;
    }

    *(void **) (&fp_clGetPlatformInfo) = dlsym(handle, "clGetPlatformInfo");
    error = dlerror();
    if (error != NULL) {
    	ss << "OpenCL™ library loading error: " << error;
        message = ss.str();
        return false;
    }

    *(void **) (&fp_clGetDeviceIDs) = dlsym(handle, "clGetDeviceIDs");
    error = dlerror();
    if (error != NULL) {
    	ss << "OpenCL™ library loading error: " << error;
        message = ss.str();
        return false;
    }

    *(void **) (&fp_clGetDeviceInfo) = dlsym(handle, "clGetDeviceInfo");
    error = dlerror();
    if (error != NULL) {
    	ss << "OpenCL™ library loading error: " << error;
        message = ss.str();
        return false;
    }

    return true;
}


void CL_DriverChecker::GetDriverInfo(string& message) {

    cl_uint num_platforms;
    json_object* node = json_object_new_object();
    cl_int result = fp_clGetPlatformIDs(0, nullptr, &num_platforms);
    if (result != CL_SUCCESS) {
    	message = GetErrorMessage(result);
        JsonNode::AddJsonNode(node, "Platform number", ERROR, message, "", 0, "Unknown");
    	return;
    }

    JsonNode::AddJsonNode(node, "Platform number", INFO, num_platforms);

    vector<cl_platform_id> platforms(num_platforms);
    result = fp_clGetPlatformIDs(num_platforms, platforms.data(), nullptr);
    if (result != CL_SUCCESS) {
    	message = GetErrorMessage(result);
        JsonNode::AddJsonNode(node, "Platform #", ERROR, message, "clGetPlatformIDs(num_platforms, platforms, NULL)", 0, "Unknown");
    	return;
    }
    for (cl_uint iter = 0; iter < num_platforms; iter ++)	{
    	json_object* platform = json_object_new_object();
    	stringstream ss1;
        ss1 << string("Platform # ") << iter;
    	JsonNode::AddJsonNode(node, ss1.str().c_str(), INFO, "", "clGetPlatformInfo(platform, CL_PLATFORM_NAME, 0, NULL, &parameterSize)", 0, platform);

    	size_t parameterSize;
    	result = fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_NAME, 0, nullptr, &parameterSize );
    	if (result == CL_SUCCESS) {
    		char name[parameterSize];
			fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_NAME, parameterSize, name, nullptr );
			JsonNode::AddJsonNode(platform, "Name", INFO, name);
    	}
    	result = fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_VENDOR, 0, nullptr, &parameterSize );
    	if (result == CL_SUCCESS) {
    		char vendor[parameterSize];
			fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_VENDOR, parameterSize, vendor, nullptr );
			JsonNode::AddJsonNode(platform, "Vendor", INFO, 2, vendor);
    	}
    	result = fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_VERSION, 0, nullptr, &parameterSize );
    	if (result == CL_SUCCESS) {
    		char version[parameterSize];
			fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_VERSION, parameterSize, version, nullptr );
			JsonNode::AddJsonNode(platform, "Version", INFO, version);
    	}
    	result = fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_PROFILE, 0, nullptr, &parameterSize );
    	if (result == CL_SUCCESS) {
    		char profile[parameterSize];
			fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_PROFILE, parameterSize, profile, nullptr );
			JsonNode::AddJsonNode(platform, "Profile", INFO, 2, profile);
    	}
    	result = fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_EXTENSIONS, 0, nullptr, &parameterSize );
    	if (result == CL_SUCCESS) {
    		char extensions[parameterSize];
			fp_clGetPlatformInfo(platforms[iter], CL_PLATFORM_EXTENSIONS, parameterSize, extensions, nullptr );
			JsonNode::AddJsonNode(platform, "Extensions", INFO, 1, extensions);
    	}

    	// Get information about the platform devices
     	json_object* js_devices = json_object_new_object();
     	JsonNode::AddJsonNode(platform, "Devices", INFO, js_devices);

    	cl_uint num_devices;
    	result = fp_clGetDeviceIDs(platforms[iter], CL_DEVICE_TYPE_ALL, 0, nullptr, &num_devices);
        if (result != CL_SUCCESS) {
        	message = GetErrorMessage(result);
        	JsonNode::AddJsonNode(js_devices, "Device number", ERROR, message, "clGetDeviceIDs(platform, CL_DEVICE_TYPE_ALL, 0, NULL, &num_devices)", 0, "Unknown");
        }
        else {
        	JsonNode::AddJsonNode(js_devices, "Device number", INFO, "", "clGetDeviceIDs(platform, CL_DEVICE_TYPE_ALL, 0, NULL, &num_devices)", 0, num_devices);

        	vector<cl_device_id> devices(num_platforms);
			result = fp_clGetDeviceIDs(platforms[iter], CL_DEVICE_TYPE_ALL, num_devices, devices.data(), nullptr);
        	if (result != CL_SUCCESS) {
            	message = GetErrorMessage(result);
                stringstream ss;
            	ss << "Devices: Unknown" << endl;
            	JsonNode::AddJsonNode(js_devices, "Device number", ERROR, message, "", 0, "Unknown");
        	}
        	else {
        		for (cl_uint jter = 0; jter < num_devices; jter ++) {
        	    	stringstream ss;
        	    	ss << string("Device # ") << jter;
					GetDeviceInfo(devices[jter], message);
					JsonNode::AddJsonNode(js_devices, ss.str(), INFO, "", "clGetDeviceInfo(deviceId, CL_DEVICE_TYPE, 0, NULL, &parameterSize)", 0, json_tokener_parse(message.c_str()));
        		}
        	}
        }
    }

	const char *json_string = json_object_to_json_string(node);
	if (json_string == NULL) {
		message = "Cannot convert json object to string.";
	} else {
		message = string(json_string);
	}
	return;
}


void CL_DriverChecker::GetDeviceInfo(cl_device_id deviceId, string& message){
    cl_int result;
    size_t parameterSize;
    cl_device_type type;
	json_object* node = json_object_new_object();

    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_TYPE, sizeof(cl_device_type), &type, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Type", INFO, GetDeviceTypeString(type).c_str());
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NAME, 0, nullptr, &parameterSize );
    if (result == CL_SUCCESS) {
    	char name[parameterSize];
    	fp_clGetDeviceInfo(deviceId, CL_DEVICE_NAME, parameterSize, name, nullptr );
    	JsonNode::AddJsonNode(node, "Name", INFO, name);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_VENDOR, 0, nullptr, &parameterSize );
    if (result == CL_SUCCESS) {
    	char vendor[parameterSize];
    	fp_clGetDeviceInfo(deviceId, CL_DEVICE_VENDOR, parameterSize, vendor, nullptr );
    	JsonNode::AddJsonNode(node, "Vendor", INFO, 2, vendor);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_VERSION, 0, nullptr, &parameterSize );
    if (result == CL_SUCCESS) {
    	char version[parameterSize];
    	fp_clGetDeviceInfo(deviceId, CL_DEVICE_VERSION, parameterSize, version, nullptr );
    	JsonNode::AddJsonNode(node, "Version", INFO, version);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PROFILE, 0, nullptr, &parameterSize );
    if (result == CL_SUCCESS) {
    	char profile[parameterSize];
    	fp_clGetDeviceInfo(deviceId, CL_DEVICE_PROFILE, parameterSize, profile, nullptr );
    	JsonNode::AddJsonNode(node, "Profile", INFO, 2, profile);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DRIVER_VERSION, 0, nullptr, &parameterSize );
    if (result == CL_SUCCESS) {
    	char version[parameterSize];
    	fp_clGetDeviceInfo(deviceId, CL_DRIVER_VERSION, parameterSize, version, nullptr );
    	JsonNode::AddJsonNode(node, "Driver version", INFO, 2, version);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_EXTENSIONS, 0, nullptr, &parameterSize );
    if (result == CL_SUCCESS) {
    	char extensions[parameterSize];
    	fp_clGetDeviceInfo(deviceId, CL_DEVICE_EXTENSIONS, parameterSize, extensions, nullptr );
    	JsonNode::AddJsonNode(node, "Extensions", INFO, 1, extensions);
	}
    cl_uint max_compute_units;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_COMPUTE_UNITS, sizeof(cl_uint), &max_compute_units, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max compute units", INFO, 1, max_compute_units);
	}
    cl_uint max_wi_dimensions;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS, sizeof(cl_uint), &max_wi_dimensions, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max work item dimensions", INFO, 1, max_wi_dimensions);
	}
    size_t max_wi_sizes[max_wi_dimensions];
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_WORK_ITEM_SIZES, sizeof(size_t) * max_wi_dimensions,
    							max_wi_sizes, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max work item sizes", INFO, 1, GetArrayString(max_wi_sizes, max_wi_dimensions));
	}
    size_t max_wg_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(size_t), &max_wg_size, nullptr );
    if (result == CL_SUCCESS) {
    	stringstream ss;
    	ss << "Max work group size: " << max_wg_size << endl;
	}
    // Preferred vector widths
    cl_uint vector_width_char;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_CHAR, sizeof(cl_uint), &vector_width_char, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for char", INFO, 2, vector_width_char);
	}
    cl_uint vector_width_short;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_SHORT, sizeof(cl_uint), &vector_width_short, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for short", INFO, 2, vector_width_short);
	}
    cl_uint vector_width_half;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_HALF, sizeof(cl_uint), &vector_width_half, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for half", INFO, 2, vector_width_half);
	}
    cl_uint vector_width_int;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_INT, sizeof(cl_uint), &vector_width_int, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for int", INFO, 2, vector_width_int);
	}
    cl_uint vector_width_long;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_LONG, sizeof(cl_uint), &vector_width_long, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for long", INFO, 2, vector_width_long);
	}
    cl_uint vector_width_float;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_FLOAT, sizeof(cl_uint), &vector_width_float, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for float", INFO, 2, vector_width_float);
	}
    cl_uint vector_width_double;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PREFERRED_VECTOR_WIDTH_DOUBLE, sizeof(cl_uint), &vector_width_double, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Preferred vector width for double", INFO, 2, vector_width_double);
	}
    // Native vector widths
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_CHAR, sizeof(cl_uint), &vector_width_char, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for char", INFO, 2, vector_width_char);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_SHORT, sizeof(cl_uint), &vector_width_short, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for short", INFO, 2, vector_width_short);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_HALF, sizeof(cl_uint), &vector_width_half, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for half", INFO, 2, vector_width_half);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_INT, sizeof(cl_uint), &vector_width_int, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for int", INFO, 2, vector_width_int);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_LONG, sizeof(cl_uint), &vector_width_long, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for long", INFO, 2, vector_width_long);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_FLOAT, sizeof(cl_uint), &vector_width_float, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for float", INFO, 2, vector_width_float);
	}
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_NATIVE_VECTOR_WIDTH_DOUBLE, sizeof(cl_uint), &vector_width_double, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Native vector width for double", INFO, 2, vector_width_double);
	}

    cl_uint max_clock_freq;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_CLOCK_FREQUENCY, sizeof(cl_uint), &max_clock_freq, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max clock frequency (MHz)", INFO, 2, max_clock_freq);
	}
    cl_uint address_bits;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_ADDRESS_BITS, sizeof(cl_uint), &address_bits, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Address bits", INFO, 2, address_bits);
	}
    cl_ulong max_mem_alloc_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_MEM_ALLOC_SIZE, sizeof(cl_ulong), &max_mem_alloc_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max memory allocation size (bytes)", INFO, 2, max_mem_alloc_size);
	}

    cl_bool image_support;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_IMAGE_SUPPORT, sizeof(cl_bool), &image_support, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Image support", INFO, 2, (image_support == CL_TRUE) ? "Yes" : "No");
	}
    cl_uint max_read_image_args;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_READ_IMAGE_ARGS, sizeof(cl_uint), &max_read_image_args, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max number of read image args", INFO, 2, max_read_image_args);
	}
    cl_uint max_write_image_args;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_WRITE_IMAGE_ARGS, sizeof(cl_uint), &max_write_image_args, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max number of write image args", INFO, 2, max_write_image_args);
	}
    cl_uint max_rw_image_args;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_READ_WRITE_IMAGE_ARGS, sizeof(cl_uint), &max_rw_image_args, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max number of read/write image args", INFO, 2, max_rw_image_args);
	}

    size_t image2d_max_width;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_IMAGE2D_MAX_WIDTH, sizeof(size_t), &image2d_max_width, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max width of 2D image (pixels)", INFO, 2, image2d_max_width);
	}
    size_t image2d_max_height;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_IMAGE2D_MAX_HEIGHT, sizeof(size_t), &image2d_max_height, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max height of 2D image (pixels)", INFO, 2, image2d_max_height);
	}
    size_t image3d_max_width;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_IMAGE3D_MAX_WIDTH, sizeof(size_t), &image3d_max_width, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max width of 3D image (pixels)", INFO, 2, image3d_max_width);
	}
    size_t image3d_max_height;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_IMAGE3D_MAX_HEIGHT, sizeof(size_t), &image3d_max_height, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max height of 3D image (pixels)", INFO, 2, image3d_max_height);
	}
    size_t image3d_max_depth;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_IMAGE3D_MAX_DEPTH, sizeof(size_t), &image3d_max_depth, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max depth of 3D image (pixels)", INFO, 2, image3d_max_depth);
	}

    cl_uint max_samplers;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_SAMPLERS, sizeof(cl_uint), &max_samplers, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max number of samplers", INFO, 2, max_samplers);
	}
    size_t max_parameter_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_PARAMETER_SIZE, sizeof(size_t), &max_parameter_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max parameter size (bytes)", INFO, 2, max_parameter_size);
	}
    cl_uint mem_base_addr_align;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MEM_BASE_ADDR_ALIGN, sizeof(cl_uint), &mem_base_addr_align, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Base address alignment (bits)", INFO, 2, mem_base_addr_align);
	}
    cl_uint min_data_type_align_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MIN_DATA_TYPE_ALIGN_SIZE, sizeof(cl_uint), &min_data_type_align_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "The smallest alignment (bytes)", INFO, 2, min_data_type_align_size);
	}

    cl_device_fp_config singe_fp_config;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_SINGLE_FP_CONFIG, sizeof(cl_device_fp_config), &singe_fp_config, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Denorms are supported", INFO, 2, (singe_fp_config & CL_FP_DENORM) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "INF and quiet NaNs are supported", INFO, 2, (singe_fp_config & CL_FP_INF_NAN) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "Round to nearest even supported", INFO, 2, (singe_fp_config & CL_FP_ROUND_TO_NEAREST) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "Round to zero supported", INFO, 2, (singe_fp_config & CL_FP_ROUND_TO_ZERO) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "Round to infinity supported", INFO, 2, (singe_fp_config & CL_FP_ROUND_TO_INF) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "IEEE754-2008 fused multiply-add supported", INFO, 2, (singe_fp_config & CL_FP_FMA) ? "Yes" : "No");
	}
    cl_device_mem_cache_type global_mem_cache_type;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_GLOBAL_MEM_CACHE_TYPE, sizeof(cl_device_mem_cache_type), &global_mem_cache_type, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Global memory cache type", INFO, 2, GetCacheTypeString(global_mem_cache_type));
	}
    cl_uint golbal_mem_cacheline_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_GLOBAL_MEM_CACHELINE_SIZE, sizeof(cl_uint), &golbal_mem_cacheline_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Size of global memory cache line (bytes)", INFO, 2, golbal_mem_cacheline_size);
	}

    cl_ulong global_mem_cache_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_GLOBAL_MEM_CACHE_SIZE, sizeof(cl_ulong), &global_mem_cache_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Size of global memory cache (bytes)", INFO, 2, global_mem_cache_size);
	}
    cl_ulong golbal_mem_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(cl_ulong), &golbal_mem_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Size of global device memory (bytes)", INFO, 2, golbal_mem_size);
	}
    cl_ulong max_const_buffer_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_CONSTANT_BUFFER_SIZE, sizeof(cl_ulong), &max_const_buffer_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max size of constant buffer (bytes)", INFO, 2, max_const_buffer_size);
	}
    cl_uint max_const_arg;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_MAX_CONSTANT_ARGS, sizeof(cl_uint), &max_const_arg, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Max number of constant arguments", INFO, 2, max_const_arg);
	}

    cl_device_local_mem_type local_mem_type;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_GLOBAL_MEM_CACHE_TYPE, sizeof(cl_device_local_mem_type), &local_mem_type, nullptr );
    if (result == CL_SUCCESS) {
    	stringstream ss;
    	ss << "Local memory type: " << GetLocalMemTypeString(local_mem_type) << endl;
    	JsonNode::AddJsonNode(node, "Local memory type", INFO, 2, GetLocalMemTypeString(local_mem_type));
	}
    cl_ulong local_mem_size;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_LOCAL_MEM_SIZE, sizeof(cl_ulong), &local_mem_size, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Local memory size (bytes)", INFO, 2, local_mem_size);
	}
    cl_bool error_correction_support;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_ERROR_CORRECTION_SUPPORT, sizeof(cl_bool), &error_correction_support, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Error correction support", INFO, 2, (error_correction_support == CL_TRUE) ? "Yes" : "No");
	}

    size_t prof_timer_resolution;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_PROFILING_TIMER_RESOLUTION, sizeof(size_t), &prof_timer_resolution, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Profiling timer resolution (ns)", INFO, 2, prof_timer_resolution);
	}
    cl_bool available;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_AVAILABLE, sizeof(cl_bool), &available, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Device available", INFO, 2, (available == CL_TRUE) ? "Yes" : "No");
	}
    cl_bool comp_available;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_COMPILER_AVAILABLE, sizeof(cl_bool), &comp_available, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Compiler available", INFO, 2, (comp_available == CL_TRUE) ? "Yes" : "No");
	}
    cl_bool endian_little;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_ENDIAN_LITTLE, sizeof(cl_bool), &endian_little, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Little endian", INFO, 2, (endian_little == CL_TRUE) ? "Yes" : "No");
	}

    cl_device_exec_capabilities exec_cap;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_SINGLE_FP_CONFIG, sizeof(cl_device_exec_capabilities), &exec_cap, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Execute OpenCL™ kernels", INFO, 2, (exec_cap & CL_EXEC_KERNEL) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "Execute OpenCL™ native kernels", INFO, 2, (exec_cap & CL_EXEC_NATIVE_KERNEL) ? "Yes" : "No");
	}
    cl_command_queue_properties com_queue_prop;
    result = fp_clGetDeviceInfo(deviceId, CL_DEVICE_SINGLE_FP_CONFIG, sizeof(cl_command_queue_properties), &com_queue_prop, nullptr );
    if (result == CL_SUCCESS) {
    	JsonNode::AddJsonNode(node, "Out-of-order supported", INFO, 2, (com_queue_prop & CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE) ? "Yes" : "No");
    	JsonNode::AddJsonNode(node, "Profiling of command-queue enabled", INFO, 2, (com_queue_prop & CL_QUEUE_PROFILING_ENABLE) ? "Yes" : "No");
	}

	const char *json_string = json_object_to_json_string(node);
	if (json_string == NULL) {
		message = "Cannot convert json object to string.";
	} else {
		message = string(json_string);
	}
    return ;
}


string CL_DriverChecker::GetErrorMessage(cl_int error) {
	switch (error)
	{
	default:
		stringstream ss;
		ss << "Unknown internal error: 0x." << hex << error;
		return ss.str();
	}
}


string CL_DriverChecker::GetDeviceTypeString(cl_device_type type) {
	switch (type & 0xFFFFFFFE) {
		case CL_DEVICE_TYPE_CPU:
			return "CPU";
		case CL_DEVICE_TYPE_GPU:
			return "GPU";
		case CL_DEVICE_TYPE_ACCELERATOR:
			return "ACCELERATOR";
		// case CL_DEVICE_TYPE_CUSTOM:_
		//  	return "CL_DEVICE_TYPE_CUSTOM";
		default:
			return "unknown";
	}
}


string CL_DriverChecker::GetArrayString(size_t* array, size_t array_size) {
	stringstream ss;
	for (size_t iter = 0; iter < array_size; iter ++) {
		ss << array[iter];
		if (iter < array_size -1)
			ss << ",";
	}

	return ss.str();
}


string CL_DriverChecker::GetCacheTypeString(cl_device_mem_cache_type type) {
	switch (type) {
		case CL_NONE:
			return "none";
		case CL_READ_ONLY_CACHE:
			return "read only";
		case CL_READ_WRITE_CACHE:
			return "read/write";
		default:
			return "unknown";
	}
}


string CL_DriverChecker::GetLocalMemTypeString(cl_device_local_mem_type type) {
	switch (type) {
		case CL_LOCAL:
			return "dedicated local";
		case CL_GLOBAL:
			return "global";
		default:
			return "unknown";
	}
}
