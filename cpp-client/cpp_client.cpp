#include<stdio.h>

#include "HelloService.h"
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <string>

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace demo;

using boost::shared_ptr;

/*编译命令：
 * g++ HelloService.cpp hello_types.cpp hello_constants.cpp cpp_client.cpp -g -I /home/mi/Project/Thrift/installed/include/ -L /home/mi/Project/Thrift/installed/lib/ -lthrift -pthread -o cpp-client
 * */

int main(int argc, char **argv) {
    boost::shared_ptr<TSocket> socket(new TSocket("localhost", 2345));
    boost::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
    boost::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));

    HelloServiceClient client(protocol);
    try {
        transport->open();

        string ret;
        client.helloFunc(ret, "Hello World!(Send from cpp client)");
        printf("%s\n", ret.c_str());

        transport->close();
    } catch (TException &tx) {
        printf("ERROR: %s\n", tx.what());
    }

    return 0;
}