package org.example;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;
//import java.util.concurrent.TimeUnit;

public class ShortConnection {

    public static void shortConnectionTest() {
        JdbcService jdbcService = new JdbcService();
        try {
            jdbcService.init("ip", 19030, "", "");
            Connection connection = jdbcService.getConnection();
            System.out.println("valid connection : " + validate(connection));
//            try {
//                TimeUnit.SECONDS.sleep(15);
//            } catch (InterruptedException e1) {
//                // do nothing
//            }
//            System.out.println("After sleep, valid connection : " + validate(connection));
            String sql = "select * from test_db.table_test_0";
            List<Map<String, String>> data = jdbcService.selectData(connection, sql);
            int i = 1;
            for (Map<String, String> line : data) {
//                System.out.println("Line id : " + i++);
                for (String column : line.keySet()) {
//                    System.out.println("column= "+ column + ", value= " + line.get(column));
                }
            }
            System.out.println("row number : " + data.size());
        } catch (SQLException e) {
            System.out.println("execute sql failed" + e);
        }
    }


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
}
