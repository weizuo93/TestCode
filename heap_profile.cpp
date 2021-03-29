#include <stdlib.h>
#include <iostream>

using namespace std;

/*
 * 编译：g++ heap_profile.cpp -ltcmalloc -g -o heap_profile
 *
 * 运行：HEAPPROFILE=./tmp/hprof HEAP_PROFILE_ALLOCATION_INTERVAL=107374182400 HEAP_PROFILE_INUSE_INTERVAL=1073741824 ./heap_profile
 * 其中，
 * HEAPPROFILE：用来配置内存镜像文件的dump路径已经文件名前缀，内存镜像文件的dump路径为“./tmp/”，内存镜像文件名称为“hprof.****.heap”；
 * HEAP_PROFILE_ALLOCATION_INTERVAL：用来配置触发内存dump的条件，上次dump之后分配的内存大小达到该阈值时（其中包括已经释放的内存），触发新的内存dump，单位为字节(107374182400=100GB)；
 * HEAP_PROFILE_INUSE_INTERVAL：用来配置触发内存dump的条件，上次dump之后正在使用的内存大小达到该阈值时，触发新的内存dump，单位为字节(1073741824=1GB)；
 * (本例中，配置正在使用的内存增量超过1GB，或分配的内存增量超过100GB，触发内存dump)
 * */

void* create(unsigned int size) {
    return malloc(size);
}

int main(void) {
    const int loop = 10;
    char* a[loop];
    unsigned int mega = 1024 * 1024;

    for (int i = 0; i < loop; i++) {
        const unsigned int create_size = 1024 * mega + 1;
        a[i] = (char*)create(create_size); // 循环每次执行完该语句，使用内存增加1GB+，会dump一次内存（共10次）。
    }

    for (int i = 0; i < 5; i++) {
        free(a[i]);
    }

    for (int i = 0; i < 5; i++) {
        malloc(1024 * mega + 1);
    }
    malloc(1024 * mega + 1); // 执行完该语句，使用内存距离上次dump内存增加了1GB+，此时，会dump一次内存（1次）。

    return 0;
    // 函数退出，会dump一次内存（1次）。
}





/*
mi@mi:~/Project/HeapProfile$ g++ heap_profile.cpp -ltcmalloc -g -o heap_profile
mi@mi:~/Project/HeapProfile$ ll
总用量 52
drwxr-xr-x  4 mi mi  4096 3月  29 18:52 ./
drwxr-xr-x 14 mi mi  4096 3月  29 17:31 ../
-rwxr-xr-x  1 mi mi 29384 3月  29 18:52 heap_profile*
-rw-rw-r--  1 mi mi  1663 3月  29 18:51 heap_profile.cpp
drwxrwxr-x  2 mi mi  4096 3月  29 18:51 .idea/
drwxr-xr-x  2 mi mi  4096 3月  29 18:52 tmp/
mi@mi:~/Project/HeapProfile$ HEAPPROFILE=./tmp/hprof HEAP_PROFILE_ALLOCATION_INTERVAL=107374182400 HEAP_PROFILE_INUSE_INTERVAL=1073741824 ./heap_profile
Starting tracking the heap
tcmalloc: large alloc 1073750016 bytes == 0x55e946b04000 @  0x7f50916291e7 0x55e944fca920 0x55e944fca96a 0x7f5090e9dbf7 0x55e944fca82a
Dumping heap profile to ./tmp/hprof.0001.heap (1024 MB currently in use)
Dumping heap profile to ./tmp/hprof.0002.heap (2048 MB currently in use)
Dumping heap profile to ./tmp/hprof.0003.heap (3072 MB currently in use)
Dumping heap profile to ./tmp/hprof.0004.heap (4096 MB currently in use)
Dumping heap profile to ./tmp/hprof.0005.heap (5120 MB currently in use)
Dumping heap profile to ./tmp/hprof.0006.heap (6144 MB currently in use)
Dumping heap profile to ./tmp/hprof.0007.heap (7168 MB currently in use)
Dumping heap profile to ./tmp/hprof.0008.heap (8192 MB currently in use)
Dumping heap profile to ./tmp/hprof.0009.heap (9216 MB currently in use)
Dumping heap profile to ./tmp/hprof.0010.heap (10240 MB currently in use)
Dumping heap profile to ./tmp/hprof.0011.heap (11264 MB currently in use)
Dumping heap profile to ./tmp/hprof.0012.heap (Exiting, 11264 MB in use)
mi@mi:~/Project/HeapProfile$
*/