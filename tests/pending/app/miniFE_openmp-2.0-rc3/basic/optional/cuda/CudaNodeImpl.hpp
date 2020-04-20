#ifndef CUDANODE_IMPL_HPP_
#define CUDANODE_IMPL_HPP_

#include <cuda.h>
#include <cuda_runtime.h>
#include <stdlib.h>
#include <stdexcept>

#include "../../../../../app/miniFE_openmp-2.0-rc3/basic/optional/cuda/cutil_inline_runtime.h"
#include "../../../../../app/miniFE_openmp-2.0-rc3/basic/optional/cuda/CudaNode.hpp"

// TODO: consider using cudaMallocHost to allocate page-locked host memory
//       this speeds up transfer between device and host, and could be very 
//       useful in the case of Import/Export multivector operations

#endif
