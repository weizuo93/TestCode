package org.example;


import java.sql.Connection;
import java.sql.SQLException;
import java.util.concurrent.TimeUnit;
import java.util.List;
import java.util.Map;
import org.apache.commons.dbcp.BasicDataSource;

public class App 
{
    private static BasicDataSource bds;

    public static void main( String[] args )
    {
        JdbcService jdbcService = new JdbcService();
//        try {
//            jdbcService.init("", 19030, "", "");
//            Connection connection = jdbcService.getConnection();

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
                TimeUnit.SECONDS.sleep(5);
            } catch (InterruptedException e1) {
                // do nothing
            }
        }

//            String sql = "select * from test_db.table_test_0";
//            List<Map<String, String>> data = jdbcService.selectData(connection, sql);
//            int i = 1;
//            for (Map<String, String> line : data) {
//                System.out.println("Line id : " + i++);
//                for (String column : line.keySet()) {
//                    System.out.println("column= "+ column + ", value= " + line.get(column));
//                }
//            }
//        } catch (SQLException e) {
//            System.out.println("execute sql failed" + e);
//        }
    }

    /*
    private static boolean validate(Connection conn)
    {
        boolean isValidated = true;
        try {
            com.mysql.jdbc.Connection c = (com.mysql.jdbc.Connection)conn;
            c.ping();
        } catch (SQLException e) {
            // TODO Auto-generated catch block
            // e.printStackTrace();
            isValidated = false;
        }

        return isValidated;
    }
    */

    public static Connection getConnection() {
        if (bds == null) {
            //创建核心类
            bds = new BasicDataSource();
            //配置4个基本参数
            bds.setDriverClassName("com.mysql.jdbc.Driver");
            bds.setUrl("jdbc:mysql://:/");
            bds.setUsername("");
            bds.setPassword("");

            //管理连接配置
            bds.setMaxActive(10); //最大活动数
            bds.setMaxIdle(5);  //最大空闲数
            bds.setMinIdle(3);  //最小空闲数
            bds.setInitialSize(10);  //初始化个数
//            bds.setValidationQuery("SELECT 1");
        }
        //获取连接
        try {
            return bds.getConnection();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
