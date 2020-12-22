import pymysql

try:
    # 打开数据库连接
    conn = pymysql.connect(
             host='tj-hadoop-tst-ct01.kscn',
             port=19030,
             user='root',
             # passwd='password',
             db='test_db',
             charset='utf8'
             )

    cursor = conn.cursor()
    data = cursor.execute('select * from table_test where citycode > 9990')
    row = cursor.fetchone()
    # all = cursor.fetchall()
    # print(all)

    while row:
        print("row: ", cursor.rownumber)
        print(row)
        row = cursor.fetchone()

    # 关闭光标
    cursor.close()

except pymysql.Error as e:
    print(e)
finally:
    if conn:
        # 关闭数据库连接
        conn.close()