import requests
import json
import random
import copy
import matplotlib.pyplot as plt


# 获取be上所有partition的信息
def get_all_partitions_info(host, port):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/tablets_distribution')
    except:
        print('Internet Error')
    else:
        tablet_distribution_str = response.text
        tablet_distribution_dict = json.loads(tablet_distribution_str)
        tablet_distribution_backend = dict()
        partitions = tablet_distribution_dict['data']['tablets_distribution']
        for partition in range(len(partitions)):
            tablet_distribution_partition = {}
            disks = partitions[partition]['disks']
            for disk in range(len(disks)):
                tablet_distribution_partition[disks[disk]['disk_path']] = disks[disk]['tablets_num']
            tablet_distribution_backend[partitions[partition]['partition_id']] = tablet_distribution_partition
    return tablet_distribution_backend


# 获取单个partition下的tablet在各个磁盘之间的分布
def get_tablet_distribution(host, port, partition_id):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/tablets_distribution?partition_id=' + partition_id)
    except:
        print('Internet Error')
    else:
        tablet_distribution_str = response.text
        tablet_distribution_dict = json.loads(tablet_distribution_str)
        tablet_distribution_backend = dict()
        partitions = tablet_distribution_dict['data']['tablets_distribution']
        for partition in range(len(partitions)):
            tablet_distribution_partition = {}
            disks = partitions[partition]['disks']
            for disk in range(len(disks)):
                tablets = disks[disk]['tablets']
                tablets_list = []
                for tablet in range(len(tablets)):
                    tablet_dict = dict()
                    tablet_dict['tablet_id'] = tablets[tablet]['tablet_id']
                    tablet_dict['schema_hash'] = tablets[tablet]['schema_hash']
                    tablet_dict['tablet_size'] = tablets[tablet]['tablet_size']
                    tablets_list.append(tablet_dict)
                tablet_distribution_partition[disks[disk]['disk_path']] = tablets_list
            tablet_distribution_backend[partitions[partition]['partition_id']] = tablet_distribution_partition
    return tablet_distribution_backend


# 根据获取的单个partition下tablet在各个磁盘之间的分布信息进行迁移策略规划
def migration_plan(tablet_distribution):
    tablet_num = 0
    for i in tablet_distribution:
        tablet_num = tablet_num + len(tablet_distribution[i])

    average = tablet_num / len(tablet_distribution)
    print('\ntablet分布均值 : {}\n'.format(average))

    out_disk = {}
    in_disk = {}
    for i in tablet_distribution:
        if len(tablet_distribution[i]) > average:
            out_disk[i] = int(len(tablet_distribution[i]) - average)
        elif len(tablet_distribution[i]) < average:
            if int(average - len(tablet_distribution[i])) == (average - len(tablet_distribution[i])):
                in_disk[i] = int(average - len(tablet_distribution[i]))
            else:
                in_disk[i] = int(average - len(tablet_distribution[i])) + 1

    print('磁盘需要迁出的tablet数量:')
    for i in out_disk:
        print('{} : {}'.format(i, out_disk[i]))

    print('磁盘可以迁入的tablet数量:')
    for i in in_disk:
        print('{} : {}'.format(i, in_disk[i]))

    # print('迁移规划：')
    migration_items = []
    for i in out_disk:
        for j in in_disk:
            if out_disk[i] <= in_disk[j]:
                for k in range(out_disk[i]):
                    dict = copy.deepcopy(tablet_distribution[i][k])
                    tablet_distribution[i].pop(k)
                    tablet_distribution[j].append(dict)
                    dict['from_disk'] = i
                    dict['to_disk'] = j
                    migration_items.append(dict)
                in_disk[j] = in_disk[j] - out_disk[i]
                out_disk[i] = 0
                break
            else:
                for k in range(in_disk[j]):
                    dict = copy.deepcopy(tablet_distribution[i][k])
                    tablet_distribution[i].pop(k)
                    tablet_distribution[j].append(dict)
                    dict['from_disk'] = i
                    dict['to_disk'] = j
                    migration_items.append(dict)
                out_disk[i] = out_disk[i] - in_disk[j]
                in_disk[j] = 0
                continue
    return migration_items


# 执行单个tablet的磁盘间迁移
def single_tablet_migration_exec(host, port, tablet_id, schema_hash, dest_disk):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/tablet_migration?tablet_id=' + tablet_id + '&schema_hash=' + schema_hash + '&disk=' + dest_disk)
    except:
        print('Internet Error')
        return False
    else:
        print(response.text)
        result = json.loads(response.text)
        if("status" in result.keys() and result["status"] == "Success"):
            return True
        else:
            return False


'''
# 生成特定长度的随机数字字符串
def get_random_number_str(length):
    num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
    return num_str
'''

'''
# 生成tablet分布数据
def tablet_distribution_generation(num_disk = 10):
    tablet_distribution = {}
    disks_original = random.sample(range(10000), num_disk)
    for i in range(len(disks_original)):
        num_tablet = disks_original[i]
        tablets = []
        schema_hash = get_random_number_str(9)
        for j in range(num_tablet):
            tablet = {}
            tablet['tablet_id'] = get_random_number_str(5)
            tablet['schema_hash'] = schema_hash
            tablet['tablet_size'] = random.randint(0, 10000)
            tablets.append(tablet)

        disk_id = 'disk_' + str(i)
        tablet_distribution[disk_id] = tablets
    return tablet_distribution
'''

if __name__ == '__main__':
    be_host = 'c3-hadoop-doris-tst-st03.bj'
    webserver_port = '8040'
    # partitions_info = get_all_partitions_info(be_host, webserver_port)
    # for partition_id in partitions_info:
    #     print(str(partition_id))
    #     partition = partitions_info[partition_id]
    #     for disk in partition:
    #         print(str(disk) + " : " + str(partition[disk]))

    # 执行单个partition下的tablet在各个磁盘之间的re-balance
    partition_id = '6929403'
    tablet_distribution_backend = get_tablet_distribution(be_host, webserver_port, partition_id)  # 获取当前partition下的tablet在各个磁盘之间的分布
    for par_id in tablet_distribution_backend:
        tablet_distribution = tablet_distribution_backend[par_id]
        print('re-balance 前，tablet分布情况：')
        total_tablet = 0
        for i in tablet_distribution:
            total_tablet = total_tablet + len(tablet_distribution[i])
        print('total number of tablet : {}'.format(total_tablet))
        for i in tablet_distribution:
            print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
            print('{} : {}'.format(i, tablet_distribution[i]))

        migration_items = migration_plan(tablet_distribution)  # 迁移策略规划
        print('migration_item:')
        for i in range(len(migration_items)):
            print('---------------------------------------------------------------------------------------------------')
            print(migration_items[i])
            status = single_tablet_migration_exec(be_host, webserver_port, str(migration_items[i]["tablet_id"]), str(migration_items[i]["schema_hash"]), str(migration_items[i]["to_disk"])) # 执行单个tablet的磁盘间迁移
            if not status:
                print('There is something wrong when migrate tablet')
                break
            print('---------------------------------------------------------------------------------------------------')
        # 根据随机生成的数据进行模拟迁移之后的分布情况
        # print('迁移后，tablet分布情况：')
        # total_tablet = 0
        # for i in tablet_distribution:
        #     total_tablet = total_tablet + len(tablet_distribution[i])
        # print('total number of tablet : {}'.format(total_tablet))
        # for i in tablet_distribution:
        #     print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
        #     print('{} : {}'.format(i, tablet_distribution[i]))

    tablet_distribution_backend = get_tablet_distribution(be_host, webserver_port, partition_id)
    for par_id in tablet_distribution_backend:
        tablet_distribution = tablet_distribution_backend[par_id]
        print('re-balance后，tablet分布情况：')
        total_tablet = 0
        for i in tablet_distribution:
            total_tablet = total_tablet + len(tablet_distribution[i])
        print('total number of tablet : {}'.format(total_tablet))
        for i in tablet_distribution:
            print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
            print('{} : {}'.format(i, tablet_distribution[i]))

    """
    tablet_distribution = tablet_distribution_generation(10)

    print('迁移前，tablet分布情况：')
    total_tablet = 0
    for i in tablet_distribution:
        total_tablet = total_tablet + len(tablet_distribution[i])
    print('total number of tablet : {}'.format(total_tablet))
    disk_origin = []
    for i in tablet_distribution:
        print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
        print('{} : {}'.format(i, tablet_distribution[i]))
        disk_origin.append(len(tablet_distribution[i]))

    '''使用柱状图呈现初始状态下tablet在各个磁盘上的分布'''
    plt.subplot(1, 2, 1)  # 2行1列中的第1个图
    plt.bar(range(1, len(disk_origin) + 1), disk_origin, tick_label=range(len(disk_origin)))  # 绘制柱状图
    plt.xlabel('disks')  # 为y轴设置名称
    plt.ylabel('tablet number')  # 为y轴设置名称
    plt.title("Original Tablet Distribution Between Different Disks")  # 设置图表标题

    migration_items = migration_execute(tablet_distribution)
    ''''''
    print('migration_item:')
    for i in range(len(migration_items)):
        print(migration_items[i])

    print('迁移后，tablet分布情况：')
    total_tablet = 0
    for i in tablet_distribution:
        total_tablet = total_tablet + len(tablet_distribution[i])
    print('total number of tablet : {}'.format(total_tablet))
    disk_finish = []
    for i in tablet_distribution:
        print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
        print('{} : {}'.format(i, tablet_distribution[i]))
        disk_finish.append(len(tablet_distribution[i]))

    '''使用柱状图呈现最终状态下tablet在各个磁盘上的分布'''
    plt.subplot(1, 2, 2)  # 2行1列中的第1个图
    plt.bar(range(1, len(disk_finish) + 1), disk_finish, tick_label=range(len(disk_finish)))  # 绘制柱状图
    plt.xlabel('disks')
    plt.ylabel('tablet number')  # 为y轴设置名称
    plt.title("Tablet Distribution Between Different Disks After Rebalance")  # 设置图表标题
    plt.show()  # 图表显示

    # migration_items = migration_execute(tablet_distribution)
    # migration_items = migration_execute(tablet_distribution)

    """

