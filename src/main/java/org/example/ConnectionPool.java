package org.example;

import com.google.common.collect.Maps;
import org.apache.commons.dbcp.BasicDataSource;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ConnectionPool {
    private static BasicDataSource bds;

    public ConnectionPool() {
        //创建核心类
        bds = new BasicDataSource();
        //配置4个基本参数
        bds.setDriverClassName("com.mysql.jdbc.Driver");
        bds.setUrl("jdbc:mysql://IP:9030");
        bds.setUsername("用户名");
        bds.setPassword("密码");

        //管理连接配置
        bds.setMaxActive(5); //最大活动数
        bds.setMaxIdle(5);  //最大空闲数
        bds.setMinIdle(1);  //最小空闲数
        bds.setInitialSize(5);  //初始化个数
        bds.setValidationQuery("SELECT 1");
    }

    public Connection getConnection() {
        //获取连接
        try {
            return bds.getConnection();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public List<Map<String, String>> selectData(Connection connection, String sql) throws SQLException {
        List<Map<String, String>> data = new ArrayList<Map<String, String>>();
        try (Statement statement = connection.createStatement()) {
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
