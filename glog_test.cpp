#include <iostream>
#include "glog/logging.h"

/*
 * 编译命令：g++ glog_test.cpp -I installed/include/  -L installed/lib/ -lglog -lgflags -lpthread -o glog_test.out
 */
int main(int argc, char** argv) {
    google::InitGoogleLogging("test");
    // INFO
    std::string str_info;
    str_info.append("./log");
    str_info.append("/INFO_");
    google::SetLogDestination(google::INFO, str_info.c_str());
    // WARNING
    std::string str_warn;
    str_warn.append("./log");
    str_warn.append("/WARNING_");
    google::SetLogDestination(google::WARNING, str_warn.c_str());
    // ERROR
    std::string str_err;
    str_err.append("./log");
    str_err.append("/ERROR_");
    google::SetLogDestination(google::ERROR, str_err.c_str());
    // FATAL
    std::string str_fatal;
    str_fatal.append("./log");
    str_fatal.append("/FATAL_");
    google::SetLogDestination(google::FATAL, str_fatal.c_str());

    LOG(INFO) << "INFO : Hello GLOG!";
    LOG(WARNING) << "WARNING : Hello GLOG!";
//    LOG(ERROR) << "ERROR : Hello GLOG!";
//    LOG(FATAL) << "FATAL : Hello GLOG!";
    return 0;
}
