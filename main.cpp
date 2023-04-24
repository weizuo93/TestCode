#include <iostream>
#include <memory>

#include "mem_pool.h"

int main() {
    std::unique_ptr<MemPool> mem_pool(new MemPool());

    uint8_t* p0 = mem_pool->allocate(2);
    std::cout << "p0 : " << (uint64_t)p0 << ", size : " << 2 << std::endl;
    uint8_t* p1 = mem_pool->allocate(4);
    std::cout << "p1 : " << (uint64_t)p1 << ", size : " << 4 << std::endl;
    uint8_t* p2 = mem_pool->allocate(8);
    std::cout << "p2 : " << (uint64_t)p2 << ", size : " << 8 << std::endl;
    uint8_t* p3 = mem_pool->allocate(16);
    std::cout << "p3 : " << (uint64_t)p3 << ", size : " << 16 << std::endl;
    uint8_t* p4 = mem_pool->allocate(32);
    std::cout << "p4 : " << (uint64_t)p4 << ", size : " << 32 << std::endl;
    uint8_t* p5 = mem_pool->allocate(64);
    std::cout << "p5 : " << (uint64_t)p5 << ", size : " << 64 << std::endl;
    uint8_t* p6 = mem_pool->allocate(128);
    std::cout << "p6 : " << (uint64_t)p6 << ", size : " << 128 << std::endl;
    uint8_t* p7 = mem_pool->allocate(256);
    std::cout << "p7 : " << (uint64_t)p7 << ", size : " << 256 << std::endl;
    uint8_t* p8 = mem_pool->allocate(512);
    std::cout << "p8 : " << (uint64_t)p8 << ", size : " << 512 << std::endl;
    uint8_t* p9 = mem_pool->allocate(1024);
    std::cout << "p9 : " << (uint64_t)p9 << ", size : " << 1024 << std::endl;
    uint8_t* p10 = mem_pool->allocate(2048);
    std::cout << "p10 : " << (uint64_t)p10 << ", size : " << 2048 << std::endl;
    uint8_t* p11 = mem_pool->allocate(4096);
    std::cout << "p11 : " << (uint64_t)p11 << ", size : " << 4096 << std::endl;
    uint8_t* p12 = mem_pool->allocate(8192);
    std::cout << "p12 : " << (uint64_t)p12 << ", size : " << 8192 << std::endl;
    uint8_t* p13 = mem_pool->allocate(10 * 8192);
    std::cout << "p13 : " << (uint64_t)p13 << ", size : " << 81920 << std::endl;

    std::cout << "======== free all ========" << std::endl;
    mem_pool->free_all();

    p0 = mem_pool->allocate(2);
    std::cout << "p0 : " << (uint64_t)p0 << ", size : " << 2 << std::endl;
    p1 = mem_pool->allocate(4);
    std::cout << "p1 : " << (uint64_t)p1 << ", size : " << 4 << std::endl;
    p2 = mem_pool->allocate(8);
    std::cout << "p2 : " << (uint64_t)p2 << ", size : " << 8 << std::endl;
    p3 = mem_pool->allocate(16);
    std::cout << "p3 : " << (uint64_t)p3 << ", size : " << 16 << std::endl;
    p4 = mem_pool->allocate(32);
    std::cout << "p4 : " << (uint64_t)p4 << ", size : " << 32 << std::endl;
    p5 = mem_pool->allocate(64);
    std::cout << "p5 : " << (uint64_t)p5 << ", size : " << 64 << std::endl;
    p6 = mem_pool->allocate(128);
    std::cout << "p6 : " << (uint64_t)p6 << ", size : " << 128 << std::endl;
    p7 = mem_pool->allocate(256);
    std::cout << "p7 : " << (uint64_t)p7 << ", size : " << 256 << std::endl;
    p8 = mem_pool->allocate(512);
    std::cout << "p8 : " << (uint64_t)p8 << ", size : " << 512 << std::endl;
    p9 = mem_pool->allocate(1024);
    std::cout << "p9 : " << (uint64_t)p9 << ", size : " << 1024 << std::endl;
    p10 = mem_pool->allocate(2048);
    std::cout << "p10 : " << (uint64_t)p10 << ", size : " << 2048 << std::endl;
    p11 = mem_pool->allocate(4096);
    std::cout << "p11 : " << (uint64_t)p11 << ", size : " << 4096 << std::endl;
    p12 = mem_pool->allocate(8192);
    std::cout << "p12 : " << (uint64_t)p12 << ", size : " << 8192 << std::endl;
    p13 = mem_pool->allocate(10 * 8192);
    std::cout << "p13 : " << (uint64_t)p13 << ", size : " << 81920 << std::endl;

    return 0;
}
