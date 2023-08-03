package org.example;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Properties;

public class ConfigLoader {

    private static final ConfigLoader INSTANCE = new ConfigLoader();
    private Properties properties = new Properties();

    private ConfigLoader() {};

    public static ConfigLoader getConfigLoader() {
        return INSTANCE;
    }

    public Properties loadProperties(String propertiesPath) throws Exception {
        InputStream inputStream = new FileInputStream(propertiesPath);
        InputStreamReader inputStreamReader = new InputStreamReader(inputStream, "utf-8");
        BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
        properties.load(bufferedReader);
        return properties;
    }

    public String getConfig(String key) {
        return properties.getProperty(key);
    }
}
