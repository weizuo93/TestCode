package org.example;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

public class Main
{
    public static void main( String[] args )
    {
//        shortConnectionTest();

//        try {
//            longConnectionTest();
//        } catch (Exception e) {
//            System.out.println("Failed to close Connection!");
//        }

        try {
            connectionPoolTest();
        } catch (Exception e) {
            System.out.println("Failed to return connection to pool!");
        }
    }

    public static void shortConnectionTest() {
        ShortConnection jdbcService = new ShortConnection();
        try {
            jdbcService.init("IP", 9030, "用户名", "密码");
            String sql = "select * from test_db.table_test limit 5;";
            List<Map<String, String>> data = jdbcService.selectData(sql);
            int i = 1;
            for (Map<String, String> line : data) {
                System.out.println("Line id : " + i++);
                for (String column : line.keySet()) {
                    System.out.println("column= "+ column + ", value= " + line.get(column));
                }
            }
            System.out.println("row number : " + data.size());
        } catch (SQLException e) {
            System.out.println("execute sql failed" + e);
        }
    }

    public static void longConnectionTest() throws SQLException {
        LongConnection jdbcService = new LongConnection();
        try {
            jdbcService.init("IP", 9030, "用户名", "密码");
            for (int j = 0; j < 5; j++) {
                System.out.println("Connection Valid:" + jdbcService.connectionValidate());
                String sql = "select * from test_db.table_test limit 3;";
                List<Map<String, String>> data = jdbcService.selectData(sql);
                int i = 1;
                for (Map<String, String> line : data) {
                    System.out.println("Line id : " + i++);
                    for (String column : line.keySet()) {
                        System.out.println("column= " + column + ", value= " + line.get(column));
                    }
                }
                System.out.println("row number : " + data.size());
            }
        } catch (SQLException e) {
            System.out.println("execute sql failed" + e);
        } finally {
            jdbcService.closeConnection();
        }
    }

    public static void connectionPoolTest() throws SQLException {
        ConnectionPool connectionPool = new ConnectionPool();
        Connection connection = connectionPool.getConnection();
        try {
            for (int j = 0; j < 5; j++) {
                System.out.println("Connection Valid:" + !connection.isClosed());
                String sql = "select * from test_db.table_test limit 3;";
                List<Map<String, String>> data = connectionPool.selectData(connection, sql);
                int i = 1;
                for (Map<String, String> line : data) {
                    System.out.println("Line id : " + i++);
                    for (String column : line.keySet()) {
                        System.out.println("column= " + column + ", value= " + line.get(column));
                    }
                }
                System.out.println("row number : " + data.size());
                connection.close();
            }
        } catch (SQLException e) {
            System.out.println("execute sql failed" + e);
        } finally {
            connection.close(); // 将connection归还给连接池，并不是断开连接
        }
    }
}
