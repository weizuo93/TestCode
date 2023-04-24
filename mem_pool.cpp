#include "mem_pool.h"

#include <iostream>


MemPool::MemPool() : _current_chunk_idx(-1),
                     _next_chunk_size(MIN_CHUNK_SIZE),
                     _total_allocated_bytes(0),
                     _total_reserved_bytes(0) {

}

MemPool::~MemPool() {
    // // MemPool对象析构时将当前对象维护的每一个chunk释放给ChunkAllocator
    for (auto& chunk : _chunks) {
        ChunkAllocator::instance()->free(chunk.chunk);
    }
}

/*通过MemPool分配一个大小为size的内存块，通过函数返回值返回首地址*/
uint8_t* MemPool::allocate(int64_t size) {
    if (size <= 0) {
        return nullptr;
    }

    if (_current_chunk_idx != -1) {
        uint8_t* result = _allocate_from_current_chunk(size, DEFAULT_ALIGNMENT); // 从当前chunk分配大小为size的内存
        if (result != nullptr) {
            return result;
        }
    }

    if (!_find_chunk(size)) { // 获取下一个适合的chunk
        return nullptr;
    }

    uint8_t* result = _allocate_from_current_chunk(size, DEFAULT_ALIGNMENT); // 从获取的新chunk中分配大小为size的内存
    return result;
}

/*从当前chunk分配大小为size的内存*/
uint8_t* MemPool::_allocate_from_current_chunk(int64_t size, int alignment) {
    ChunkInfo& chunk_info = _chunks[_current_chunk_idx];
    int64_t aligned_allocated_bytes = RoundUpToPowerOfFactor(chunk_info.allocated_bytes, alignment);
    if (aligned_allocated_bytes + size <= chunk_info.chunk.size) {
        uint8_t* result = chunk_info.chunk.data + aligned_allocated_bytes;
        std::cout << "chunk_idx : " << _current_chunk_idx << ", chunk size : " << chunk_info.chunk.size << std::endl;

        chunk_info.allocated_bytes = aligned_allocated_bytes + size;
        int64_t padding = aligned_allocated_bytes - chunk_info.allocated_bytes;
        _total_allocated_bytes += (padding + size);
        return result;
    }
    return nullptr;
}

/*获取一个适合的chunk*/
bool MemPool::_find_chunk(size_t min_size) {
    int first_free_idx;
    if (_current_chunk_idx == -1) {
        first_free_idx = 0;
    } else {
        first_free_idx = _current_chunk_idx + (_chunks[_current_chunk_idx].allocated_bytes > 0);
    }

    for (int idx = _current_chunk_idx + 1; idx < _chunks.size(); ++idx) {
        if (_chunks[idx].chunk.size >= min_size) {
            if (idx != first_free_idx) {
                std::swap(_chunks[idx], _chunks[first_free_idx]);
            }
            _current_chunk_idx = first_free_idx;
            return true;
        }
    }

    size_t  chunk_size = std::max<size_t>(min_size, _next_chunk_size);
    chunk_size = RoundUpToPowerOfTwo(chunk_size);

    Chunk chunk;
    if (!ChunkAllocator::instance()->allocate(chunk_size, &chunk)) { // 当前对象维护的chunk中没有合适的chunk用与本次内存分配，通过ChunkAllocator分配一个新的合适的chunk
        return false;
    }

    // 将ChunkAllocator分配的新的chunk添加到当前MemPool对象的chunk list中
    if (first_free_idx == static_cast<int>(_chunks.size())) {
        _chunks.emplace_back(chunk);
    } else {
        _chunks.insert(_chunks.begin() + first_free_idx, ChunkInfo(chunk));
    }

    _current_chunk_idx = first_free_idx;
    _total_reserved_bytes += chunk_size;
    _next_chunk_size = static_cast<int>(std::min<int64_t>(chunk_size * 2, MAX_CHUNK_SIZE)); // 计算ChunkAllocator为当前MemPool对象下一次分配的chunk大小
    return true;
}

/*初始化当前MemPool对象维护的所有chunk以供当前MemPool对象重复利用*/
void MemPool::clear() {
    _current_chunk_idx = -1;
    for (auto& chunk : _chunks) {
        chunk.allocated_bytes = 0;
    }
    _total_allocated_bytes = 0;
}

/*清空当前MemPool对象维护的所有chunk释放给ChunkAllocator*/
void MemPool::free_all() {
    for (auto& chunk : _chunks) {
        ChunkAllocator::instance()->free(chunk.chunk);
    }
    _chunks.clear();
    _next_chunk_size = MIN_CHUNK_SIZE;
    _current_chunk_idx = -1;
    _total_allocated_bytes = 0;
    _total_reserved_bytes = 0;
}