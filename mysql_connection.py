import pymysql


def connect_mysql_and_execute_query(_host, _port, _usr, _passwd, _db, _sql):
    try:
        # 打开数据库连接
        conn = pymysql.connect(host=_host, port=_port, user=_usr, passwd=_passwd, db=_db, charset='utf8')
        cursor = conn.cursor()
        data = cursor.execute(_sql)
        row = cursor.fetchone()
        index = cursor.description
        # all = cursor.fetchall()
        # print(all)

        while row:
            print("\nrow: ", cursor.rownumber)
            print(row)
            for i in range(len(index)):
                print(str(index[i][0]) + " : " + str(row[i]))
            row = cursor.fetchone()

        # 关闭光标
        cursor.close()

    except pymysql.Error as e:
        print(e)
    finally:
        if conn:
            # 关闭数据库连接
            conn.close()


if __name__ == "__main__":
    sql = 'select * from table_test where citycode > 9990;'
    connect_mysql_and_execute_query("", 9030, "", "", "", sql)
