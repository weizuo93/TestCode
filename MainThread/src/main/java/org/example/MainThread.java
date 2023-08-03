package org.example;

import java.nio.file.Path;
import java.util.Scanner;

public class MainThread
{
    public static void main( String[] args ) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("是否安装插件：");
            String isInstall = scanner.nextLine();
            if (isInstall.equalsIgnoreCase("quit")) {
                break;
            }

            if (isInstall.equalsIgnoreCase("yes")) {
                System.out.println("请输入插件名称：");
                String pluginName = scanner.nextLine();
                System.out.println("请输入插件主类名称：");
                String pluginClass = scanner.nextLine();
                System.out.println("请输入插件jar包所在路径：");
                String pluginPath = scanner.nextLine();

                PluginInfo pluginInfo = new PluginInfo(pluginName, pluginClass);
                Path installPath = Path.of(pluginPath);
                PluginLoader pluginLoader = new PluginLoader(installPath, pluginInfo);

                try {
                    pluginLoader.install();
                } catch (Exception e) {
                    System.out.println("Failed to install plugin pluginName. " + e);
                }
            } else {
                try {
                    System.out.println("Sleep ...");
                    Thread.sleep(5000);
                } catch (Exception e) {}
            }
        }
    }


}
