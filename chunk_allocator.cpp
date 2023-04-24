#include "chunk_allocator.h"

#include <sys/mman.h>
#include <string.h>
#include <iostream>

// 静态成员变量初始化，静态成员变量只能在类外部初始化
ChunkAllocator* ChunkAllocator::_s_instance = nullptr;

ChunkAllocator::ChunkAllocator() : _chunk_lists(64), _reserved_bytes(0), _reserve_bytes_limit(1 * 1024 * 1024 * 1024) {

};

ChunkAllocator::~ChunkAllocator() {
    if (_s_instance != nullptr) {
        delete _s_instance;
    }

    // ChunkAllocator析构时将所有chunk list下的每一个chunk释放给系统
    for (int i = 0; i < 64; ++i) {
        if (_chunk_lists[i].empty()) continue;
        size_t size = (uint64_t)1 << i;
        for (auto ptr : _chunk_lists[i]) {
            _free_via_munmap(ptr, size);
        }
    }
}

/*通过ChunkAllocator分配一个大小为size的chunk，通过参数chunk传回，bool类型的函数返回值表示是否分配成功*/
bool ChunkAllocator::allocate(size_t size, Chunk* chunk) {
    if (size <= 0) {
        return false;
    }
    chunk->size = size;

    if (_pop_free_chunk(size, &chunk->data)) { // 从ChunkAllocator对象维护的chunk list中分配一个chunk
        _reserved_bytes.fetch_sub(size);
        return true;
    }
    // 通过chunk list分配内存失败，进一步通过mmap向系统申请一个大小为size的chunk
    chunk->data = _allocate_via_mmap(size);
    if (chunk->data == nullptr) {
        return false;
    }
    return true;
}

/*通过ChunkAllocator释放一个chunk*/
void ChunkAllocator::free(const Chunk& chunk) {
    if (chunk.size <= 0) {
        return;
    }

    int64_t old_reserved_bytes = _reserved_bytes;
    int64_t new_reserved_bytes = 0;

    do {
        new_reserved_bytes = old_reserved_bytes + chunk.size;
        if (chunk.size <= MIN_CHUNK_SIZE || chunk.size >= MAX_CHUNK_SIZE ||
            new_reserved_bytes > _reserve_bytes_limit) { // 待释放的chunk超过当前ChunkAllocator对象的所有chunk list的chunk大小，或当前ChunkAllocator对象维护的内存已经达到设定的阈值，需要将待释放的chunk释放给系统
            _free_via_munmap(chunk.data, chunk.size); // 通过munmap向系统释放一个chunk的内存
            return;
        }
    // 此处使用compare_exchange_weak表达式是考虑到多线程并发的因素，因为其他线程可能已经更改了_reserved_bytes的值：
    // 如果 _reserved_bytes == old_reserved_bytes（其他线程没有更改_reserved_bytes的值），则更新_reserved_bytes值为new_reserved_bytes，表达式返回true，while循环退出；
    // 如果 _reserved_bytes != old_reserved_bytes（_reserved_bytes的值被其他线程更改了），则更新old_reserved_bytes值为_reserved_bytes,表达式返回false，开始下一次循环，重新计算new_reserved_bytes；
    } while (!_reserved_bytes.compare_exchange_weak(old_reserved_bytes, new_reserved_bytes));

    _push_free_chunk(chunk.data, chunk.size); // 将待释放的chunk添加到ChunkAllocator对象维护的chunk list中以供重新使用
}

/*将待释放的chunk添加到ChunkAllocator对象维护的chunk list中以供重新使用*/
void ChunkAllocator::_push_free_chunk(uint8_t* ptr, size_t size) {
    int idx = Log2Ceiling64(size); // 将size映射到一个特定的chunk list上
    std::unique_lock<std::mutex> lock(_mutex);
    _chunk_lists[idx].push_back(ptr);
}

/*从ChunkAllocator对象维护的chunk list中分配一个chunk*/
bool ChunkAllocator::_pop_free_chunk(size_t size, uint8_t** ptr) {
    int idx = Log2Ceiling64(size); // 将size映射到一个特定的chunk list上
    auto& free_list = _chunk_lists[idx];

    std::unique_lock<std::mutex> lock(_mutex);
    if (free_list.empty()) {
        return false;
    }
    *ptr = free_list.back();
    free_list.pop_back();
    return true;
}

/*通过mmap向系统申请内存，从进程虚拟内存空间（堆栈之间的文件映射区）分配一个大小为length的内存块*/
uint8_t* ChunkAllocator::_allocate_via_mmap(size_t length) {
    auto ptr = (uint8_t*)mmap(nullptr, length, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE,
                              -1, 0);
    if (ptr == MAP_FAILED) {
        char buf[64];
        std::cout << "fail to allocate memory via mmap, errno=" << errno
                   << ", errmsg=" << strerror_r(errno, buf, 64);
        return nullptr;
    }
    return ptr;
}

/*通过munmap向系统释放内存，释放进程虚拟内存空间（堆栈之间的文件映射区）的大小为length的内存块*/
void ChunkAllocator::_free_via_munmap(uint8_t* ptr, size_t length) {
    auto res = munmap(ptr, length);
    if (res != 0) {
        char buf[64];
        std::cout << "fail to free memory via munmap, errno=" << errno
                   << ", errmsg=" << strerror_r(errno, buf, 64);
    }
}