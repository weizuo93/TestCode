cmake_minimum_required(VERSION 3.19)
project(thread_pool)

set(CMAKE_CXX_COMPILER "g++")
set(CMAKE_BUILD_TYPE "Debug")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}-pthread")

add_executable(thread_pool main.cpp thread_pool.cpp)