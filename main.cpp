#include <iostream>
#include <cstdlib>

#include "thread_pool.h"


void task(int i) {
    std::cout << "running task-" << i << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds((rand() % 5) + 1));
}

int main() {

    ThreadPool thread_pool(5, 20, 10000);
    thread_pool.init();

    bool monitor_flag = true;
    std::thread monitor_thread([&thread_pool, &monitor_flag]() {
       while (monitor_flag) {
           std::cout << "thread_num : " << thread_pool.thread_num() << ", task_queue_size : " << thread_pool.task_queue_size() << std::endl;
           std::this_thread::sleep_for(std::chrono::milliseconds(1000));
       }
    });

    bool producer_flag = true;
    std::thread producer_thread([&thread_pool, &producer_flag](){
       long i = 0;
       while (producer_flag) {
           thread_pool.submit([i]() {task(i);});
           i++;
           std::this_thread::sleep_for(std::chrono::milliseconds(200));
       }
    });


    std::this_thread::sleep_for(std::chrono::seconds(60));
    thread_pool.shut_down();
    std::cout << "Done. thread_num : " << thread_pool.thread_num() << ", task_queue_size : " << thread_pool.task_queue_size() << std::endl;

    producer_flag = false;
    if (producer_thread.joinable()) {
        producer_thread.join();
    }

    monitor_flag = false;
    if (monitor_thread.joinable()) {
        monitor_thread.join();
    }
    return 0;
}
