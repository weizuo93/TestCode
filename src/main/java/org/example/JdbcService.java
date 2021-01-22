package org.example;

import com.google.common.collect.Maps;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class JdbcService {
    private static Log LOG = LogFactory.getLog(JdbcService.class);
    private static String jdbcTemplate  = "jdbc:mysql://%s:%s/?user=%s&password=%s";
    private String jdbcUrl;

    static {
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            LOG.warn(e);
        }
    }

    public void init(String url, int port, String user, String password) {
        this.jdbcUrl = String.format(jdbcTemplate, url, port, user, password);
    }

    public List<Map<String, String>> selectData(String sql) throws SQLException {
        List<Map<String, String>> data = new ArrayList<Map<String, String>>();
        try (Connection connection = DriverManager.getConnection(jdbcUrl);
             Statement statement = connection.createStatement()) {
            try (ResultSet resultSet = statement.executeQuery(sql)) {
                ResultSetMetaData meta = resultSet.getMetaData();
                int columeCount = meta.getColumnCount();
                while (resultSet.next()) {
                    Map<String, String> line = Maps.newHashMap();
                    for (int i = 1; i <= columeCount; i++) {
                        line.put(meta.getColumnName(i), resultSet.getString(i));
                    }
                    data.add(line);
                }
            }
            return data;
        } catch (SQLException e) {
            throw e;
        }
    }
}
