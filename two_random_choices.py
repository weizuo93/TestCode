import random
import matplotlib.pyplot as plt
import numpy as np

''''''
num_tablet = 30000 #需要创建的tablet的个数
num_bin = 10       #磁盘个数

#bins_original = [0] * num_bin                        # 0初始化tablet在各个磁盘上的分布
bins_original = random.sample(range(1000), num_bin-5) #初始化tablet在各个磁盘上的分布
bins_original.extend([0, 0, 0, 0, 0])                 #初始化tablet在各个磁盘上的分布，其中5个磁盘初始情况下没有tablet分布

'''使用柱状图呈现初始状态下tablet在各个磁盘上的分布'''
plt.subplot(3, 1, 1) #3行1列中的第1个图
plt.bar(range(1, len(bins_original)+1), bins_original, tick_label=range(num_bin)) #绘制柱状图
plt.ylabel('tablet number') #为y轴设置名称
plt.title("original bins")  #设置图表标题

bins_choice = bins_original.copy()
bins_two_choices = bins_original.copy()
diff_choice = []      #保存tablet创建过程中（随机磁盘选择算法）在各个磁盘上分布的极差
diff_two_choices = [] #保存tablet创建过程中（two random choices磁盘选择算法）在各个磁盘上分布的极差
std_choice = []       #保存tablet创建过程中（随机磁盘选择算法）在各个磁盘上分布的标准差
std_two_choices = []  #保存tablet创建过程中（two random choices磁盘选择算法）在各个磁盘上分布的标准差

#使用随机磁盘选择算法依次进行num_tablet个tablet的创建
def random_choice():
    for i in range(num_tablet):
        bin_id = random.randint(0, num_bin-1) #随机选出一个磁盘
        bins_choice[bin_id] = bins_choice[bin_id] + 1 #在选出的磁盘上创建tablet，该磁盘上的tablet数量增加1
        diff_choice.append(max(bins_choice) - min(bins_choice)) #计算tablet在各个磁盘上分布的极差
        std_choice.append(np.std(bins_choice)) #计算tablet在各个磁盘上分布的标准差

#使用two random choices磁盘选择算法依次进行num_tablet个tablet的创建
def two_random_choice():
    for i in range(num_tablet):
        two_bin_id = random.sample(range(num_bin), 2)   #随机选出一个磁盘。sample(x,y)函数的作用是从序列x中，随机选择y个不重复的元素。
        if bins_two_choices[two_bin_id[0]] > bins_two_choices[two_bin_id[1]]: #从选出的两个磁盘中选择tablet数量较小的那一个，用于当前tablet的创建
            bin_id = two_bin_id[1]
        else:
            bin_id = two_bin_id[0]

        bins_two_choices[bin_id] = bins_two_choices[bin_id] + 1  #在选出的磁盘上创建tablet，该磁盘上的tablet数量增加1
        diff_two_choices.append(max(bins_two_choices) - min(bins_two_choices)) #计算tablet在各个磁盘上分布的极差
        std_two_choices.append(np.std(bins_two_choices)) #计算tablet在各个磁盘上分布的标准差

if __name__ == '__main__':
    random_choice()
    two_random_choice()

    print('original bins:')
    print(bins_original)
    print('max load: {0}, min load: {1}, diff: {2}\n'.format(max(bins_original), min(bins_original), max(bins_original) - min(bins_original)))
    print('random choice:')
    print(bins_choice)
    print('max load: {0}, min load: {1}, diff: {2}\n'.format(max(bins_choice), min(bins_choice), max(bins_choice) - min(bins_choice)) )
    print('two random choices:')
    print(bins_two_choices)
    print('max load: {0}, min load: {1}, diff: {2}\n'.format(max(bins_two_choices), min(bins_two_choices), max(bins_two_choices) - min(bins_two_choices)))

    '''使用柱状图呈现使用随机磁盘选择算法完成num_tablet个tablet的创建之后tablet在各个磁盘上的分布'''
    plt.subplot(3, 1, 2) #3行1列中的第2个图
    plt.bar(range(1, len(bins_choice)+1), bins_choice, tick_label=range(num_bin)) #绘制柱状图
    plt.ylabel('tablet number')
    plt.title("random choice")

    '''使用柱状图呈现使用two random choices磁盘选择算法完成num_tablet个tablet的创建之后tablet在各个磁盘上的分布'''
    plt.subplot(3, 1, 3) #3行1列中的第3个图
    plt.bar(range(1, len(bins_two_choices)+1), bins_two_choices, tick_label=range(num_bin))
    plt.ylabel('tablet number')
    plt.title("two random choices")

    plt.show() #图表显示

    '''使用折线图呈现使用随机磁盘选择算法创建tablet的过程中tablet在各个磁盘上分布的极差'''
    plt.subplot(2, 1, 1)  #2行1列中的第1个图
    line_random_choice = plt.plot(range(num_tablet), diff_choice, 'r', label = 'random choice') #图表中第1条折线的label配置
    line_two_choices = plt.plot(range(num_tablet), diff_two_choices, 'b', label='two random choices') #图表中第2条折线的label配置
    plt.plot(range(num_tablet), diff_choice, 'r', range(num_tablet), diff_two_choices, 'b') #绘制的两条折线图分别用红色和蓝色呈现
    plt.xlabel('The creation process for the tablet')
    plt.ylabel('The range of the tablet distribution')
    plt.title('The Range comparison for different disk selection strategies')
    plt.legend() #设置标签

    '''使用折线图呈现使用two random choices磁盘选择算法创建tablet的过程中tablet在各个磁盘上分布的标准差'''
    plt.subplot(2, 1, 2)#2行1列中的第2个图
    line_random_choice = plt.plot(range(num_tablet), std_choice, 'r', label = 'random choice')
    line_two_choices = plt.plot(range(num_tablet), std_two_choices, 'b', label='two random choices')
    plt.plot(range(num_tablet), std_choice, 'r', range(num_tablet), std_two_choices, 'b')
    plt.xlabel('The creation process for the tablet')
    plt.ylabel('The standard deviation of the tablet distribution')
    plt.title('The standard deviation comparison for different disk selection strategies')
    plt.legend()

    plt.show() #图表显示