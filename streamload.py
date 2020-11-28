import time
import random
import string
import os

'''
# 建表语句
CREATE TABLE table_test
(
    event_day DATE,
    siteid INT DEFAULT '10',
    citycode SMALLINT,
    username VARCHAR(32) DEFAULT '',
    pv BIGINT SUM DEFAULT '0'
)
AGGREGATE KEY(event_day, siteid, citycode, username)
PARTITION BY RANGE(event_day)
(
    PARTITION p2010 VALUES LESS THAN ('2011-01-01'),
    PARTITION p2011 VALUES LESS THAN ('2012-01-01'),
    PARTITION p2012 VALUES LESS THAN ('2013-01-01'),
    PARTITION p2013 VALUES LESS THAN ('2014-01-01'),
    PARTITION p2014 VALUES LESS THAN ('2015-01-01'),
    PARTITION p2015 VALUES LESS THAN ('2016-01-01'),
    PARTITION p2016 VALUES LESS THAN ('2017-01-01'),
    PARTITION p2017 VALUES LESS THAN ('2018-01-01'),
    PARTITION p2018 VALUES LESS THAN ('2019-01-01'),
    PARTITION p2019 VALUES LESS THAN ('2020-01-01')
)
DISTRIBUTED BY HASH(siteid) BUCKETS 10
PROPERTIES("replication_num" = "3");
'''


def generate_date():
    a1=(2010, 1, 1, 0, 0, 0, 0, 0, 0)              # 设置开始日期时间元组（1976-01-01 00：00：00）
    a2=(2019, 12, 31, 23, 59, 59, 0, 0, 0)    # 设置结束日期时间元组（1990-12-31 23：59：59）

    start = time.mktime(a1)    # 生成开始时间戳
    end = time.mktime(a2)      # 生成结束时间戳

    # 随机生成日期字符串
    t = random.randint(start,end)    # 在开始和结束时间戳中随机取出一个
    date_tuple = time.localtime(t)          # 将时间戳生成时间元组
    date = time.strftime("%Y-%m-%d", date_tuple)  # 将时间元组转成格式化字符串（1976-05-21）
    return date


def generate_siteid():
    return random.randint(0,100000000)


def generate_citycode():
    return random.randint(0,10000)


def generate_username():
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return ran_str


def generate_pv():
    return random.randint(0,100000000)


def write_data_file():
    f = open('./data.txt', 'w')
    for i in range(2000):
        date = generate_date()
        siteid = generate_siteid()
        citycode = generate_citycode()
        username = generate_username()
        pv = generate_pv()
        row = str(date) + '|' + str(siteid) + '|' + str(citycode) + '|' + str(username) + '|' + str(pv) + '\n'
        f.write(row)

    f.close()


if __name__ == "__main__":
    while True:
        write_data_file()
        time.sleep(8)
        cmd = 'curl --location-trusted -u root: -H "label:' + str(int(time.time())) +'" -H "column_separator:|" -T ./data.txt http://tj-hadoop-tst-ct01.kscn:18030/api/test_db/table_test/_stream_load;'
        os.system(cmd)
