cmake_minimum_required(VERSION 3.19)
project(mem_pool)

set(CMAKE_CXX_STANDARD 14)

add_executable(mem_pool main.cpp mem_pool.cpp chunk_allocator.cpp)