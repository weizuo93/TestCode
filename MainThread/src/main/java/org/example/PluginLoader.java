package org.example;

import org.apache.commons.io.FileUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.DirectoryStream;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.Set;

public class PluginLoader {
    private static final Logger LOG = LogManager.getLogger(PluginLoader.class);
    private Path installPath;
    private Plugin plugin;
    private PluginInfo pluginInfo;
    private Path pluginDir;

    public PluginLoader(Path installPath, PluginInfo pluginInfo) {
        this.installPath = installPath;
        this.pluginInfo = pluginInfo;
        this.pluginDir = Path.of(ConfigLoader.getConfigLoader().getConfig("plugin_dir"));
    }

    public void install() throws Exception {
        if (hasInstalled()) {
            throw new Exception("Plugin " + pluginInfo.getName() + " has already been installed.");
        }

        movePlugin();
        plugin = dynamicLoadPlugin();
        plugin.setName(pluginInfo.getName());
        plugin.init();
    }

    public void movePlugin() throws Exception {
        if (installPath == null || !Files.exists(installPath)) {
            throw new PluginException("Install plugin " + pluginInfo.getName() + " failed, because install path doesn't "
                    + "exist.");
        }

        Path targetPath = FileSystems.getDefault().getPath(pluginDir.toString(), pluginInfo.getName());
        if (Files.exists(targetPath)) {
            if (!Files.isSameFile(installPath, targetPath)) {
                throw new PluginException(
                        "Install plugin " + pluginInfo.getName() + " failed. because " + installPath.toString()
                                + " exists");
            }
        } else {
            Files.move(installPath, targetPath, StandardCopyOption.ATOMIC_MOVE);
//            Files.copy(installPath, targetPath);
        }

        // move success
        installPath = targetPath;
    }

    private Plugin dynamicLoadPlugin() throws Exception {
        if (plugin != null) {
            try {
                plugin.close();
            } catch (Exception e) {
                LOG.warn("failed to close previous plugin, ignore it. ", e);
            } finally {
                plugin = null;
            }
        }

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

    private boolean hasInstalled() {
        // check already install
        if (pluginInfo != null) {
            Path targetPath = FileSystems.getDefault().getPath(pluginDir.toString(), pluginInfo.getName());
            if (Files.exists(targetPath)) {
                return true;
            }
        }
        return false;
    }

    public void uninstall() throws IOException {
        if (plugin != null) {
            plugin.close();
        }

        if (null != installPath && Files.exists(installPath)
                && Files.isSameFile(installPath.getParent(), pluginDir)) {
            FileUtils.deleteQuietly(installPath.toFile());
        }
    }
}
