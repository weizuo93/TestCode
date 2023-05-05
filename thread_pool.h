#pragma once

#include <queue>
#include <mutex>

#include <list>
#include <thread>
#include <functional>
#include <condition_variable>
#include <future>
#include <utility>
#include <atomic>

template<typename T>
class TaskQueue {
public:
    TaskQueue(int max_size) : _max_size(max_size) {};
    ~TaskQueue() {};

    bool empty() {
        std::unique_lock<std::mutex> lock(_mutex);
        return _task_queue.empty();
    }

    int size() {
        std::unique_lock<std::mutex> lock(_mutex);
        return _task_queue.size();
    }

    bool enqueue(T& t) {
        std::unique_lock<std::mutex> lock(_mutex);
        if (_task_queue.size() >= _max_size) {
            return false;
        }
        _task_queue.emplace(t);
        return true;
    }

    bool dequeue(T& t) {
        std::unique_lock<std::mutex> lock(_mutex);
        if (_task_queue.empty()) {
            return false;
        }
        t = std::move(_task_queue.front());
        _task_queue.pop();
        return true;
    }

private:
    std::queue<T> _task_queue;
    std::mutex _mutex;
    int _max_size;
};


class ThreadPool {
public:
    ThreadPool(int min_thread_num, int max_thread_num, int max_queue_size);
    ~ThreadPool() {};
    ThreadPool(const ThreadPool&) = delete;
    ThreadPool(ThreadPool&&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;
    ThreadPool& operator=(ThreadPool&&) = delete;

    void init();
    void shut_down();
    bool submit(std::function<void()> f);

    int min_thread_num() {
        return _min_thread_num;
    }

    int max_thread_num() {
        return _max_thread_num;
    }

    int task_queue_size() {
        return _task_queue.size();
    }

    int thread_num() {
        return _thread_nums.load();
    }

private:

    void _thread_worker();

    int _min_thread_num;
    int _max_thread_num;
    bool _shut_down;
    TaskQueue<std::function<void()>> _task_queue;
    std::atomic<int> _thread_nums;

    std::mutex _mutex;
    std::condition_variable _cv_task;
    std::condition_variable _cv_shut_down;
};
