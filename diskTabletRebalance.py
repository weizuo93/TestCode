import requests
import json
import random
import copy
import matplotlib.pyplot as plt


def httpRequest(host, port):
    try:
        response = requests.get(url='http://' + host + ':' + port + '/tablets_distribution')
    except:
        print('Internet Error')

    tabletDistribution_str = response.text
    tabletDistribution_dict = json.loads(tabletDistribution_str)

    tablet_distribution_backend = {}
    partitions = tabletDistribution_dict['data']['tablets_distribution'];
    for partition in range(len(partitions)) :
        tablet_distribution_partition = {}
        #print('partition_id : {}'.format(partitions[partition]['partition_id']))
        disks = partitions[partition]['disks']
        for disk in range(len(disks)):
            #print('partition_id : {},---------------------disk_id : {},---------------------tablets_num : {},------------------tablets_total_size : {}'.format(partitions[partition]['partition_id'], disks[disk]['disk_id'], disks[disk]['tablets_num'], disks[disk]['tablets_total_size']))
            tablets = disks[disk]['tablets']
            tablets_list = []
            for tablet in range(len(tablets)):
                #print('tablet_id : {},  schema_hash : {}, tablet_footprint : {}'.format(tablets[tablet]['tablet_id'], tablets[tablet]['schema_hash'], tablets[tablet]['tablet_footprint']))
                tablet_dict = {}
                tablet_dict['tablet_id'] = tablets[tablet]['tablet_id']
                tablet_dict['schema_hash'] = tablets[tablet]['schema_hash']
                tablet_dict['tablet_footprint'] = tablets[tablet]['tablet_footprint']
                tablets_list.append(tablet_dict)
            tablet_distribution_partition[disks[disk]['disk_path_hash']] = tablets_list
        tablet_distribution_backend[partitions[partition]['partition_id']] = tablet_distribution_partition
    return tablet_distribution_backend


'''生成特定长度的随机数字字符串'''
def get_random_number_str(length):
    num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
    return num_str


'''生成tablet分布数据'''
def tablet_distribution_generation(num_disk = 10):
    tablet_distribution = {}
    disks_original = random.sample(range(1000), num_disk)
    for i in range(len(disks_original)):
        num_tablet = disks_original[i]
        tablets = []
        schema_hash = get_random_number_str(9)
        for j in range(num_tablet):
            tablet = {}
            tablet['tablet_id'] = get_random_number_str(5)
            tablet['schema_hash'] = schema_hash
            tablet['tablet_footprint'] = random.randint(0, 10000)
            tablets.append(tablet)

        disk_id = 'disk_' + str(i)
        tablet_distribution[disk_id] = tablets
    return tablet_distribution


def migration_execute(tablet_distribution):
    tablet_num = 0
    for i in tablet_distribution:
        tablet_num = tablet_num + len(tablet_distribution[i])

    average = (int)(tablet_num / len(tablet_distribution))
    print('\ntablet分布均值 : {}\n'.format(average))

    out_disk = {}
    in_disk = {}
    for i in tablet_distribution:
        if len(tablet_distribution[i]) > average:
            out_disk[i] = len(tablet_distribution[i]) - average - 1
        elif len(tablet_distribution[i]) < average:
            in_disk[i] = average - len(tablet_distribution[i])

    print('磁盘需要迁出的tablet数量:')
    for i in out_disk:
        print('{} : {}'.format(i, out_disk[i]))

    print('磁盘可以迁入的tablet数量:')
    for i in in_disk:
        print('{} : {}'.format(i, in_disk[i]))

    print('迁移规划：')
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


if __name__ == '__main__':
    tablet_distribution = tablet_distribution_generation(10)

    print('迁移前，tablet分布情况：')
    total_tablet = 0
    for i in tablet_distribution:
        total_tablet = total_tablet + len(tablet_distribution[i])
    print('total number of tablet : {}'.format(total_tablet))
    for i in tablet_distribution:
        print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
        print('{} : {}'.format(i, tablet_distribution[i]))

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
    for i in tablet_distribution:
        print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
        print('{} : {}'.format(i, tablet_distribution[i]))

    # migration_items = migration_execute(tablet_distribution)
    # migration_items = migration_execute(tablet_distribution)

    """
    tablet_distribution_backend = httpRequest('', '18040')
    for partition_id in tablet_distribution_backend:
        print('==============================================================================================================================================================================================')
        tablet_distribution = tablet_distribution_backend[partition_id]
        '''
        print('\npartition_id ： {}'.format(partition_id))
        total_tablet = 0
        for i in tablet_distribution:
            total_tablet = total_tablet + len(tablet_distribution[i])
        print('total number of tablet : {}'.format(total_tablet))
        for i in tablet_distribution:
            print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
            print('{} : {}'.format(i, tablet_distribution[i]))
        '''
        print('迁移前，tablet分布情况：')
        total_tablet = 0
        for i in tablet_distribution:
            total_tablet = total_tablet + len(tablet_distribution[i])
        print('total number of tablet : {}'.format(total_tablet))
        for i in tablet_distribution:
            print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
            print('{} : {}'.format(i, tablet_distribution[i]))

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
        for i in tablet_distribution:
            print('{}中tablet数量: {}'.format(i, len(tablet_distribution[i])))
            print('{} : {}'.format(i, tablet_distribution[i]))

        # migration_items = migration_execute(tablet_distribution)
        # migration_items = migration_execute(tablet_distribution)
    """