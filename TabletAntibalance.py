import requests
import json
import copy
import time
import random


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
    disks = []
    for disk in tablet_distribution:
        disks.append(disk)

    migration_items = []
    for disk in tablet_distribution:
        tablet_list = tablet_distribution[disk]
        for i in range(len(tablet_list)):
            migration_task = dict()
            migration_task['tablet_id'] = tablet_list[i]["tablet_id"]
            migration_task['schema_hash'] = tablet_list[i]["schema_hash"]
            migration_task['tablet_size'] = tablet_list[i]["tablet_size"]
            migration_task['from_disk'] = disk
            id = random.randint(0, len(disks) - 1)
            migration_task['to_disk'] = disks[id]
            migration_items.append(migration_task)

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
        print('              Tablet Anti-balance For Partition: ' + str(partition_id))
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
            print('migration tasks:')
            for i in range(len(migration_items)):
                print('---------------------------------------------------------------------------------------------------')
                print(migration_items[i])
                submit_tablet_migration_task(be_host, webserver_port, str(migration_items[i]["tablet_id"]), str(migration_items[i]["schema_hash"]), str(migration_items[i]["to_disk"]))  # 提交单个tablet的磁盘间迁移任务
                while True:
                    status = query_tablet_migration_status(be_host, webserver_port, str(migration_items[i]["tablet_id"]), str(migration_items[i]["schema_hash"]))  # 查询单个tablet的磁盘间迁移状态
                    if status:
                        break
                    else:
                        time.sleep(1)  # sleep 1秒
                # if not status:
                #     print('There is something wrong when submit tablet migration task')
                #     break
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
