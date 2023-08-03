### 简单的Java插件框架实现

环境依赖：jdk 11

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

主线程运行起来之后，按照代码提示输入`插件操作`的信息（install/uninstall/show/quit）：
* 如果选择安装插件（install），则需要依次输入`插件名称`（随便叫什么名称都可以）、`插件主类名称`和`插件jar包所在的路径`，系统会将插件jar包移动到配置文件设置的plugin_dir目录下，并加载插件类，完成插件安装。
* 如果选择卸载插件（uninstall），则需要输入`插件名称`，完成对应插件的卸载，关闭插件任务线程。
* 如果选择查看插件（show），则会输出进程中安装的所有插件列表。
* 如果选择终止程序（quit），则会依次卸载所有的插件，关闭插件任务线程，并结束主线程。

```
mi@mi:~/Project/Java/JavaPlugin/MainThread/output$ java -jar simple-plugin-main-thread.jar
请输入插件操作(install/uninstall/show/quit)：
install
请输入插件名称：
taskplugin
请输入插件主类名称：
org.example.TaskPlugin
请输入插件jar包所在路径：
/home/mi/Project/Java/JavaPlugin/TaskPlugin/output
2023-08-08 17:27:41.998 [INFO] (main) [TaskPlugin.init():25] task plugin [taskplugin1] is installed successfully.
2023-08-08 17:27:41.998 [INFO] (main) [MainThread.installPlugin():60] install plugin [taskplugin1] successfully.
2023-08-08 17:27:41.999 [INFO] (task plugin thread) [TaskPlugin$TaskPluginWorker.run():58] 2023-08-08 17:27:41 Task Plugin [taskplugin] is running ...
2023-08-08 17:27:47.000 [INFO] (task plugin thread) [TaskPlugin$TaskPluginWorker.run():58] 2023-08-08 17:27:47 Task Plugin [taskplugin] is running ...
2023-08-08 17:27:52.001 [INFO] (task plugin thread) [TaskPlugin$TaskPluginWorker.run():58] 2023-08-08 17:27:52 Task Plugin [taskplugin] is running ...
请输入插件操作(install/uninstall/show/quit)：
show
Current plugin list :
taskplugin
请输入插件操作(install/uninstall/show/quit)：
uninstall
请输入插件名称：
taskplugin
2023-08-08 17:42:41.018 [INFO] (main) [MainThread.uninstallPlugin():85] uninstall plugin [taskplugin] successfully.
请输入插件操作(install/uninstall/show/quit)：
show
Current plugin list :
请输入插件操作(install/uninstall/show/quit)：
```
