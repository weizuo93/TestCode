package org.example;

public class PluginInfo {
    private String name;
    private String className;

    public PluginInfo(String name, String className) {
        this.name = name;
        this.className = className;
    }

    public String getName() {
        return name;
    }

    public String getClassName() {
        return className;
    }
}
