package org.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class TaskPlugin extends Plugin {
    private static final Logger LOG = LogManager.getLogger(TaskPlugin.class);
    private static SimpleDateFormat DATETIME_FORMAT = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    private volatile boolean isInit = false;
    private volatile boolean isClosed = false;
    private Thread thread;

    @Override
    public void init() throws PluginException {
        super.init();
        try {
            synchronized (this) {
                if (isInit) {
                    return;
                }
                LOG.info("task plugin [{}] is installed successfully.", this.name);
                this.thread = new Thread(new TaskPluginWorker(this.name), "task plugin thread");
                this.thread.start();

                isInit = true;
            }
        } catch (Exception e) {
            throw new PluginException(e.getMessage());
        }

    }

    @Override
    public void close() throws IOException {
        super.close();
        isClosed = true;
        if (thread != null) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                LOG.warn("encounter exception when closing task plugin", e);
            }
        }
    }

    private class TaskPluginWorker implements Runnable {
        private String pluginName;
        public TaskPluginWorker(String name) {
            this.pluginName = name;
        }

        public void run() {
            while (!isClosed) {
                LOG.info(longToTimeString(System.currentTimeMillis()) + " Task Plugin [{}] is running ...", this.pluginName);
                try {
                    Thread.sleep(5000);
                } catch (Exception e) {}
            }
        }
    }

    public static synchronized String longToTimeString(long timeStamp) {
        if (timeStamp <= 0L) {
            return "1900-01-01 00:00:00";
        }
        return DATETIME_FORMAT.format(new Date(timeStamp));
    }
}
