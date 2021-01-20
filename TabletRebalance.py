import requests
import json
import copy
import time


# 获取be上所有partition的信息
def get_all_partitions_info(host, port):
    tablet_distribution_backend = dict()
    try:
        response = requests.get(url='http://' + host + ':' + port + '/api/tablets_distribution?group_by=partition')
    except:
        print('Internet Error')
    else:
        tablet_distribution_str = response.text
        tablet_distribution_dict = json.loads(tablet_distribution_str)
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
    tablet_distribution_backend = dict()
    try:
        response = requests.get(url='http://' + host + ':' + port + '/api/tablets_distribution?group_by=partition&partition_id=' + str(partition_id))
    except:
        print('Internet Error')
    else:
        tablet_distribution_str = response.text
        tablet_distribution_dict = json.loads(tablet_distribution_str)
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


# 提交单个tablet的磁盘间迁移任务
def submit_tablet_migration_task(host, port, tablet_id, schema_hash, dest_disk):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/api/tablet_migration?goal=run&tablet_id=' + tablet_id + '&schema_hash=' + schema_hash + '&disk=' + dest_disk)
    except:
        print('Internet Error')
        # return False;
    else:
        print(response.text)
        # result = json.loads(response.text)
        # if("status" in result.keys() and result["status"] == "Success"):
        #     return True
        # else:
        #     return False


# 提交单个tablet的磁盘间迁移任务
def query_tablet_migration_status(host, port, tablet_id, schema_hash):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/api/tablet_migration?goal=status&tablet_id=' + tablet_id + '&schema_hash=' + schema_hash)
    except:
        print('Internet Error')
        return False
    else:
        print(response.text)
        result = json.loads(response.text)
        if(("status" in result.keys() and result["status"] == "Success") and ("msg" in result.keys() and result["msg"] == "migration task has finished successfully")) or ("status" in result.keys() and result["status"] == "Fail"):
            return True
        else:
            return False


if __name__ == '__main__':
    be_host = ''
    webserver_port = ''
    partitions_info = get_all_partitions_info(be_host, webserver_port)
    # for partition_id in partitions_info:
    #     print(str(partition_id))
    #     partition = partitions_info[partition_id]
    #     for disk in partition:
    #         print(str(disk) + " : " + str(partition[disk]))

    partitions_info = get_all_partitions_info(be_host, webserver_port)
    for partition_id in partitions_info:
        # 执行单个partition下的tablet在各个磁盘之间的re-balance
        print('\n**********************************************************************************')
        print('              Tablet Re-balance For Partition: ' + str(partition_id))
        print('**********************************************************************************\n')
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
                # print('{} : {}'.format(i, tablet_distribution[i]))

            migration_items = migration_plan(tablet_distribution)  # 迁移策略规划
            print('submit migration tasks:')
            for i in range(len(migration_items)):
                print('---------------------------------------------------------------------------------------------------')
                print(migration_items[i])
                submit_tablet_migration_task(be_host, webserver_port, str(migration_items[i]["tablet_id"]), str(migration_items[i]["schema_hash"]), str(migration_items[i]["to_disk"]))  # 提交单个tablet的磁盘间迁移任务
                # if not status:
                #     print('There is something wrong when submit tablet migration task')
                #     break
                print('---------------------------------------------------------------------------------------------------')

            print('query migration status:')
            for i in range(len(migration_items)):
                print('---------------------------------------------------------------------------------------------------')
                print(migration_items[i])
                while True:
                    status = query_tablet_migration_status(be_host, webserver_port, str(migration_items[i]["tablet_id"]), str(migration_items[i]["schema_hash"]))  # 查询单个tablet的磁盘间迁移状态
                    if status:
                        break
                    else:
                        time.sleep(1)  # sleep 1秒
                print('---------------------------------------------------------------------------------------------------')

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
                # print('{} : {}'.format(i, tablet_distribution[i]))
