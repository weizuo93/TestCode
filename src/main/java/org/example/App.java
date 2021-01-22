package org.example;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.SQLException;
import java.util.List;
import java.util.Map;

public class App 
{
//    private static Log LOG = LogFactory.getLog(App.class);
    private static final Logger LOG = LogManager.getLogger(App.class);

    public static void main( String[] args )
    {
        JdbcService jdbcService = new JdbcService();
        jdbcService.init("tj-hadoop-tst-ct01.kscn", 19030, "root", "root");
        String sql = "select * from test_db.table_test_0";
        try {
            List<Map<String, String>> data = jdbcService.selectData(sql);
            int i = 1;
            for (Map<String, String> line : data) {
//                System.out.println("Line id : " + i++);
                LOG.info("Line id : " + i);
                for (String column : line.keySet()) {
//                    System.out.println("column= "+ column + ", value= " + line.get(column));
                    LOG.info("column= "+ column + ", value= " + line.get(column));
                }
            }
        } catch (SQLException e) {
            LOG.error("execute sql failed", e);
        }
    }
}
