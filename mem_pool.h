#pragma once

#include <cstdint>

#include "chunk_allocator.h"

static constexpr int DEFAULT_ALIGNMENT = 8;

class MemPool {
public:
    MemPool();
    ~MemPool();

    uint8_t* allocate(int64_t size);

    // Makes all allocated chunks available for re-use, but doesn't delete any chunks.
    void clear();

    // Deletes all allocated chunks.
    void free_all();

private:
    uint8_t* _allocate_from_current_chunk(int64_t size, int alignment);
    bool _find_chunk(size_t min_size);

    struct ChunkInfo {
        Chunk chunk;
        int64_t allocated_bytes;
        explicit ChunkInfo(const Chunk& chunk) : chunk(chunk), allocated_bytes(0) {}
        ChunkInfo() : allocated_bytes(0) {}
    };

    std::vector<ChunkInfo> _chunks; // 按顺序维护了当前MemPool对象下的所有chunk

    int _current_chunk_idx; // 指示当前进行内存分配的chunk，_chunks中_current_chunk_idx之前的chunk都已经被分配，_current_chunk_idx之后的chunk都空闲
    int _next_chunk_size;   // 通过ChunkAllocator为当前MemPool对象下一次分配的chunk大小
    int64_t _total_reserved_bytes; // 当前MemPool对象维护的chunk总大小，包括已经分配的内存和空闲内存
    int64_t _total_allocated_bytes;// 当前MemPool对象已经分配出去的内存大小
};

// Returns the smallest power of two that contains v. If v is a power of two, v is returned
static inline int64_t RoundUpToPowerOfTwo(int64_t v) {
    --v;
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    v |= v >> 32;
    ++v;
    return v;
}

// Returns 'value' rounded up to the nearest multiple of 'factor' when factor is a power of two
static inline int64_t RoundUpToPowerOfFactor(int64_t value, int64_t factor) {
    return (value + (factor - 1)) & ~(factor - 1);
}