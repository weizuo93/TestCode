#include "thread_pool.h"


ThreadPool::ThreadPool(int min_thread_num, int max_thread_num, int max_queue_size) :
                                _min_thread_num(min_thread_num),
                                _max_thread_num(max_thread_num),
                                _shut_down(false),
                                _task_queue(max_queue_size) {
    _thread_nums.store(0);
}

void ThreadPool::init() {
    for (int i = 0; i < _min_thread_num; i++) {
        std::thread([&](){
            _thread_worker();
        }).detach();
    }
}

void ThreadPool::shut_down() {
    std::unique_lock<std::mutex> lock(_mutex);
    _shut_down = true;
    _cv_task.notify_all();
    // 线程创建之后随即被detach了，因此ThreadPool对象析构之前必须执行shut_down确保所有的线程均已退出，
    // 否则，ThreadPool对象析构之后，子线程还有可能访问ThreadPool对象，这会造成整个进程崩溃。
    while(_thread_nums.load() != 0) {
        _cv_shut_down.wait_for(lock, std::chrono::milliseconds(50));
    }
}

bool ThreadPool::submit(std::function<void()> f) {
    std::unique_lock<std::mutex> lock(_mutex);
    if (_shut_down) {
        return false;
    }

    bool enqueued = _task_queue.enqueue(f);
    if (enqueued) {
        _cv_task.notify_one();
    }

    if (_task_queue.size() > _max_thread_num && _thread_nums.load() < _max_thread_num) {
        std::thread([&](){
            _thread_worker();
        }).detach();
    }

    return enqueued;
}

void ThreadPool::_thread_worker() {
    _thread_nums.fetch_add(1);
    std::function<void()> func;
    bool dequeued;
    while (!_shut_down) {
        {
            std::unique_lock<std::mutex> lock(_mutex);
            if (_task_queue.empty()) {
                _cv_task.wait_for(lock, std::chrono::milliseconds(500));
                if (_task_queue.empty() && (_thread_nums.load() > _min_thread_num)) {
                    break;
                }
            }
            dequeued = _task_queue.dequeue(func);
        }
        if (dequeued) {
            func();
        }
    }
    _thread_nums.fetch_sub(1);
    _cv_shut_down.notify_one();
}
