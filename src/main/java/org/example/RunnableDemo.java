package org.example;


import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

public class RunnableDemo implements Runnable{
    private String threadName;
    private Connection connection;

    RunnableDemo(String tname, Connection conn) {
        this.connection = conn;
        this.threadName = tname;
    }

    @Override
    public void run() {
        JdbcService jdbcService = new JdbcService();
        try {
            System.out.println("thread : " + this.threadName + ", valid connection : " + jdbcService.connectionValidate(connection));
            String sql = "select * from test_db.table_test_0";
            List<Map<String, String>> data = jdbcService.selectData(connection, sql);
            int i = 1;
            for (Map<String, String> line : data) {
//                System.out.println("thread : " + this.threadName +"Line id : " + i++);
                for (String column : line.keySet()) {
//                    System.out.println("thread : " + this.threadName +"column= "+ column + ", value= " + line.get(column));
                }
            }
            
        } catch (SQLException e) {
            System.out.println("execute sql failed. " + e);
        }
    }
}
