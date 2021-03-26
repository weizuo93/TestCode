import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def analysis(path, prefix):
    time = []
    mem_malloc = []
    # path = "path"           # 数据文件目录
    files = os.listdir(path)  # 得到目录下的所有文件名称
    files.sort()              # 按文件名进行排序
    for file in files:        # 遍历文件
        if not os.path.isdir(file):  # 判断是否是目录，不是目录才打开
            f = open(path+"/"+file)  # 打开文件
            line = f.readline()      # 读取文件第一行，第一行数据为“Total: 3008.5 MB”
            '''
            while line:
                print(line)
                print(type(line))
                line = f.readline()
            '''
            if line:
                li = line.split()  # 根据空格对第一行数据进行分割
                if len(li) == 3:
                    print("mem: " + li[1] + " " + li[2] + ", file: " + file)
                    mem_malloc.append(float(li[1]))
                    time.append(file.split(prefix)[1])
                else:
                    print("Error." + line)
            f.close()

    '''使用折线图呈现'''
    fig, ax = plt.subplots(1, 1)
    plt.plot(time, mem_malloc, 'b', label='memory')  # 图表中第2条折线的配置
    plt.xlabel('Time')       # x轴标签
    tick_spacing = len(files) / 15  # x轴文字的显示间隔（图标中一共显示15个x轴文字）
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=15)  # x轴文字逆时针旋转15°
    plt.ylabel('Mem/MB')     # y轴标签
    plt.title('Memory Allocation')  # 图表标题
    plt.legend()  # 设置标签
    plt.show()    # 图表显示


if __name__ == '__main__':
    analysis("data_sgp2_be20", "sgp2_be20.mem.")
