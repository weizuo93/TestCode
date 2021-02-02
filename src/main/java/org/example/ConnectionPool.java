package org.example;

import org.apache.commons.dbcp.BasicDataSource;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.concurrent.TimeUnit;

public class ConnectionPool {
    private static BasicDataSource bds;

    public static Connection getConnection() {
        if (bds == null) {
            //创建核心类
            bds = new BasicDataSource();
            //配置4个基本参数
            bds.setDriverClassName("com.mysql.jdbc.Driver");
            bds.setUrl("jdbc:mysql://ip:port");
            bds.setUsername("root");
            bds.setPassword("root");

            //管理连接配置
            bds.setMaxActive(5); //最大活动数
            bds.setMaxIdle(2);  //最大空闲数
            bds.setMinIdle(1);  //最小空闲数
            bds.setInitialSize(3);  //初始化个数
            bds.setValidationQuery("SELECT 1");
        }
        //获取连接
        try {
            return bds.getConnection();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public static void connectionPoolTest() {
        int i = 1;
        while (true) {
            System.out.println("round : " + i++);
            Thread t1 = new Thread(new RunnableDemo("thread-1", getConnection()));
            Thread t2 = new Thread(new RunnableDemo("thread-2", getConnection()));
            Thread t3 = new Thread(new RunnableDemo("thread-3", getConnection()));
            Thread t4 = new Thread(new RunnableDemo("thread-4", getConnection()));
            Thread t5 = new Thread(new RunnableDemo("thread-5", getConnection()));
            t1.start(); // 启动新线程
            t2.start(); // 启动新线程
            t3.start(); // 启动新线程
            t4.start(); // 启动新线程
            t5.start(); // 启动新线程
            try {
                TimeUnit.SECONDS.sleep(30);
            } catch (InterruptedException e1) {
                // do nothing
            }
        }
    }
}
