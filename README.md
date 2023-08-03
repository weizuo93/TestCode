#### 编译主线程代码

```
cd MainThread/
bash build.sh
```
在 `MainThread/output/`路径下生成主线程的包`simple-plugin-main-thread.zip`，将其解压。

```
unzip simple-plugin-main-thread.zip
```
在`MainThread/output/`路径下解压出主线程的jar包`simple-plugin-main-thread.jar`。

#### 编译插件代码

##### 安装主线程jar包
因为插件代码依赖了主线程代码中的`org.example.Plugin`类，所以在插件代码中需要增加如下依赖：
```
<dependency>
  <groupId>org.example</groupId>
  <artifactId>simple-plugin-main-thread</artifactId>
  <version>1.0-SNAPSHOT</version>
</dependency>
```

编译插件代码之前需要将主线程代码的jar包安装至本地maven仓库中，否则，编译时会找不到相关依赖。安装命令如下：
```
mvn install:install-file -Dfile=/...path.../simple-plugin-main-thread.jar -DgroupId=org.example -DartifactId=simple-plugin-main-thread -Dversion=1.0-SNAPSHOT -Dpackaging=jar
```

##### 编译插件代码

```
cd TaskPlugin/
bash build.sh
```
在 `TaskPlugin/output/`路径下生成插件的包`task-plugin.zip`，将其解压。

```
unzip task-plugin.zip
```
在`TaskPlugin/output/`路径下解压出插件的jar包`task-plugin.jar`。


#### 运行主线程并安装插件

##### 运行主线程

在 `MainThread/output/`路径下执行如下命令：

```
java -jar simple-plugin-main-thread.jar
```

##### 安装插件

主线程运行起来之后，按照代码提示依次输入`是否安装插件`的信息（yes或YES）、`插件名称`（随便叫什么名称都可以）、`插件主类名称`和`插件jar包所在的路径`，完成插件安装。

```
mi@mi:~/Project/Java/JavaPlugin/MainThread/output$ java -jar simple-plugin-main-thread.jar
是否安装插件：
yes
请输入插件名称：
taskplugin
请输入插件主类名称：
org.example.TaskPlugin
请输入插件jar包所在路径：
/home/mi/Project/Java/JavaPlugin/TaskPlugin/output
task plugin is installed successfully.
是否安装插件：
2023-08-03 22:20:22 Task Plugin is running ...
2023-08-03 22:20:27 Task Plugin is running ...
2023-08-03 22:20:32 Task Plugin is running ...
2023-08-03 22:20:37 Task Plugin is running ...
2023-08-03 22:20:42 Task Plugin is running ...
2023-08-03 22:20:47 Task Plugin is running ...
```
