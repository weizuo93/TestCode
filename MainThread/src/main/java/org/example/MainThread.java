package org.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Scanner;

public class MainThread {
    private static final Logger LOG = LogManager.getLogger(MainThread.class);
    private static Map<String, PluginLoader> plugins = new HashMap<>();

    public static void main(String[] args) throws Exception {
        ConfigLoader configLoader = ConfigLoader.getConfigLoader();
        configLoader.loadProperties("config.properties");

        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("请输入插件操作(install/uninstall/show/quit)：");
            String isInstallUninstall = scanner.nextLine();

            if (isInstallUninstall.equalsIgnoreCase("install")) {
                installPlugin();
            } else if (isInstallUninstall.equalsIgnoreCase("uninstall")) {
                uninstallPlugin();
            } else if (isInstallUninstall.equalsIgnoreCase("show")) {
                showPlugin();
            } else if (isInstallUninstall.equalsIgnoreCase("quit")) {
                uninstallAllPlugin();
                break;
            } else {
                try {
                    LOG.info("Main Thread Sleep ...");
                    Thread.sleep(5000);
                } catch (Exception e) {}
            }
        }
    }

    private static void installPlugin() {
        LOG.info("安装插件 ...");
        Scanner scanner = new Scanner(System.in);
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
            plugins.put(pluginName, pluginLoader);
            LOG.info("install plugin [{}] successfully.",pluginName);
        } catch (Exception e) {
            LOG.warn("Failed to install plugin [{}], and remove the plugin file.", pluginName, e);
            try {
                pluginLoader.uninstall();
            } catch (Exception ex) {
                LOG.warn("Failed to remove plugin [{}] file, plugin not exist.", pluginName);
            }
        }
    }

    private static void uninstallPlugin() {
        LOG.info("卸载插件 ...");
        Scanner scanner = new Scanner(System.in);
        System.out.println("请输入插件名称：");
        String pluginName = scanner.nextLine();

        if (!plugins.containsKey(pluginName)) {
            LOG.warn("Failed to uninstall plugin [{}], plugin not exist.", pluginName);
        }

        PluginLoader pluginLoader = plugins.get(pluginName);
        try {
            pluginLoader.uninstall();
            plugins.remove(pluginName);
            LOG.info("uninstall plugin [{}] successfully.",pluginName);
        } catch (Exception e) {
            LOG.warn("Failed to uninstall plugin [{}].",pluginName, e);
        }
    }

    private static void uninstallAllPlugin() {
        LOG.info("卸载所有插件 ...");
        for(Iterator<String> iterator = plugins.keySet().iterator(); iterator.hasNext(); ) {
            String pluginName = iterator.next();
            LOG.info("uninstall plugin [{}].", pluginName);
            if (!plugins.containsKey(pluginName)) {
                LOG.warn("Failed to uninstall plugin [{}], plugin not exist.", pluginName);
            }

            PluginLoader pluginLoader = plugins.get(pluginName);
            try {
                pluginLoader.uninstall();
                iterator.remove();
                LOG.info("uninstall plugin [{}] successfully.", pluginName);
            } catch (Exception e) {
                LOG.warn("Failed to uninstall plugin [{}].", pluginName, e);
            }
        }
    }

    private static void showPlugin() {
        System.out.println("Current plugin list :");
        for (Map.Entry<String, PluginLoader> entry : plugins.entrySet()) {
            System.out.println(entry.getKey());
        }
    }
}
