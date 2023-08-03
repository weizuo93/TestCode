package org.example;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class TaskPlugin extends Plugin
{
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
                System.out.println("task plugin is installed successfully.");
                this.thread = new Thread(new TaskPluginWorker(), "task plugin thread");
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
                System.out.println("encounter exception when closing task plugin" + e);
            }
        }
    }

    private class TaskPluginWorker implements Runnable {

        public TaskPluginWorker() {
        }

        public void run() {
            while (!isClosed) {
                System.out.println(longToTimeString(System.currentTimeMillis()) + " Task Plugin is running ...");
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
