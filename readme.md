1.在主目录下执行：
`sh build-install.sh`
编译并安装thrift-0.9.3，安装目录为主目录下的`installed/`。

2.在主目录下执行：
`./installed/bin/thrift -r --gen java hello.thrift`
和
`./installed/bin/thrift -r --gen cpp hello.thrift`
在当前目录下生成`gen-java/`和`gen-cpp/`目录。

3.编写C++ Server代码。
在主目录下创建`cpp-server/`目录，将`gen-cpp/`目录下的`hello_types.h`、`hello_types.cpp`、`HelloService.h`、`HelloService.cpp`和`HelloService_server.skeleton.cpp`拷贝到新创建的`cpp-server/`目录下，并修改`HelloService_server.skeleton.cpp`文件名称为`cpp_server.cpp`。在文件`cpp_server.cpp`中修改服务端代码逻辑（需要配置RPC端口）。
在目录`cpp-server/`下执行命令编译C++服务端代码：
`g++ HelloService.cpp hello_types.cpp cpp_server.cpp -g -I /home/mi/Project/Thrift/installed/include/ -L /home/mi/Project/Thrift/installed/lib/ -lthrift -pthread -o cpp-server`
编译成功，在目录`cpp-server/`下生成可执行文件`cpp-server`。

4.编写C++ Client代码。
在主目录下创建`cpp-client/`目录，将`gen-cpp/`目录下的`hello_types.h`、`hello_types.cpp`、`hello_constants.h`、`hello_constants.h`、`HelloService.h`和`HelloService.cpp`拷贝到新创建的`cpp-client/`目录下，并在`cpp-client/`目录下创建文件`cpp_client.cpp`，在其中编写客户端代码逻辑（需要配置RPC端口，需要与服务端保持一致）。
在目录`cpp-client/`下执行命令编译C++客户端代码：
`g++ HelloService.cpp hello_types.cpp hello_constants.cpp cpp_client.cpp -g -I /home/mi/Project/Thrift/installed/include/ -L /home/mi/Project/Thrift/installed/lib/ -lthrift -pthread -o cpp-client`
编译成功，在目录`cpp-client/`下生成可执行文件`cpp-client`。

5.编写Java Server代码。
在主目录下创建`java-server/`目录，并在其中创建Mevean工程。在pom文件中添加依赖项。
```
    <dependency>
      <groupId>org.apache.thrift</groupId>
      <artifactId>libthrift</artifactId>
      <version>0.12.0</version>
    </dependency>
```
将`gen-java/`目录下的`HelloService.java`文件拷贝到工程中，并创建`HelloServiceImpl.java`类，实现HelloService的Iface接口，并在其中实现服务端代码逻辑。编写服务端启动代码`Server.java`（需要配置RPC端口）。

6.编写Java Client代码。
在主目录下创建`java-client/`目录，并在其中创建Mevean工程。在pom文件中添加依赖项。
```
    <dependency>
      <groupId>org.apache.thrift</groupId>
      <artifactId>libthrift</artifactId>
      <version>0.12.0</version>
    </dependency>
```
将`gen-java/`目录下的`HelloService.java`文件拷贝到工程中，并创建`Clent.java`编写客户端代码逻辑（需要配置RPC端口，需要与服务端保持一致）。



如此，便可进行跨语言的RPC通信（cpp-client ---> cpp-server、cpp-client ---> java-server、java-client ---> java-server、cpp-client ---> cpp-server）。

