package org.example;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.Set;

public class PluginLoader {
    private Path installPath;
    private Plugin plugin;
    private PluginInfo pluginInfo;

    public PluginLoader(Path installPath, PluginInfo pluginInfo) {
        this.installPath = installPath;
        this.pluginInfo = pluginInfo;
    }

    public void install() throws Exception {
        plugin = dynamicLoadPlugin();
        try {
            plugin.init();
        } catch (Error e) {
            throw new Exception(e.getMessage());
        }
    }

    private Plugin dynamicLoadPlugin() throws Exception {
        Set<URL> jarList = getJarUrl(installPath);

        // create a child to load the plugin in this bundle
        ClassLoader parentLoader = PluginClassLoader.createLoader(getClass().getClassLoader(), Collections.EMPTY_LIST);
        ClassLoader loader = URLClassLoader.newInstance(jarList.toArray(new URL[0]), parentLoader);

        Class<? extends Plugin> pluginClass;
        try {
            pluginClass = loader.loadClass(pluginInfo.getClassName()).asSubclass(Plugin.class);
        } catch (ClassNotFoundException e) {
            throw new Exception("Could not find plugin class [" + pluginInfo.getClassName() + "]", e);
        }
        return loadPluginClass(pluginClass);
    }

    private Plugin loadPluginClass(Class<? extends Plugin> pluginClass) {
        final Constructor<?>[] constructors = pluginClass.getConstructors();
        if (constructors.length == 0) {
            throw new IllegalStateException("no public constructor for [" + pluginClass.getName() + "]");
        }

        if (constructors.length > 1) {
            throw new IllegalStateException("no unique public constructor for [" + pluginClass.getName() + "]");
        }

        final Constructor<?> constructor = constructors[0];

        try {
            if (constructor.getParameterCount() == 0) {
                return (Plugin) constructor.newInstance();
            } else {
                throw new IllegalStateException("failed to find correct constructor.");
            }
        } catch (final ReflectiveOperationException e) {
            throw new IllegalStateException("failed to load plugin class [" + pluginClass.getName() + "]", e);
        }
    }

    private Set<URL> getJarUrl(Path path) throws IOException {
        Set<URL> urls = new LinkedHashSet<>();
        // gather urls for jar files
        try (DirectoryStream<Path> jarStream = Files.newDirectoryStream(path, "*.jar")) {
            for (Path jar : jarStream) {
                // normalize with toRealPath to get symlinks out of our hair
                URL url = jar.toRealPath().toUri().toURL();
                if (!urls.add(url)) {
                    throw new IllegalStateException("duplicate codebase: " + url);
                }
            }
        }

        return urls;
    }
}
