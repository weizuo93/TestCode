#pragma once

#include <cstddef>
#include <cstdint>
#include <mutex>
#include <vector>
#include <atomic>

struct Chunk {
    uint8_t* data = nullptr;
    size_t size = 0;
};

// <= MIN_CHUNK_SIZE, A large number of small chunks will waste extra storage and increase lock time.
static constexpr size_t MIN_CHUNK_SIZE = 4096; // 4K
// >= MAX_CHUNK_SIZE, Large chunks may not be used for a long time, wasting memory.
static constexpr size_t MAX_CHUNK_SIZE = 64 * (1ULL << 20); // 64M

// 单例类
class ChunkAllocator {
public:
    static ChunkAllocator* instance() {
        if (_s_instance == nullptr) {
            _s_instance = new ChunkAllocator();
        }
        return _s_instance;
    }

    bool allocate(size_t size, Chunk* chunk);
    void free(const Chunk& chunk);

private:
    ChunkAllocator();
    ~ChunkAllocator();
    ChunkAllocator(const ChunkAllocator& chunkAllocator) = delete;
    const ChunkAllocator& operator=(const ChunkAllocator& chunkAllocator) = delete;
    void _push_free_chunk(uint8_t* ptr, size_t size);
    bool _pop_free_chunk(size_t size, uint8_t** ptr);
    uint8_t* _allocate_via_mmap(size_t length);
    void _free_via_munmap(uint8_t* ptr, size_t length);

    static ChunkAllocator* _s_instance;

    std::mutex _mutex;
    std::vector<std::vector<uint8_t*>> _chunk_lists; //维护了64个chunk list，每个chunk list中维护了固定大小的chunk
    std::atomic<int64_t> _reserved_bytes;
    size_t _reserve_bytes_limit;
};

static inline int Log2Floor64(uint64_t n) {
    return n == 0 ? -1 : 63 ^ __builtin_clzll(n);
}

static inline int Log2Ceiling64(uint64_t n) {
    int floor = Log2Floor64(n);
    // Check if zero or a power of two. This pattern is recognised by gcc and optimised
    // into branch-free code.
    if (0 == (n & (n - 1))) {
        return floor;
    } else {
        return floor + 1;
    }
}
