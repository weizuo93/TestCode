# Doris创建tablet时的磁盘选择策略


#### 1.随机磁盘选择算法
每次创建tablet时，从所有磁盘中随机选出一个磁盘用于当前tablet的创建。

#### 2.Two random choices磁盘选择算法
每次创建tablet时，从所有磁盘中随机选出两个磁盘，然后从随机选出的这两个磁盘中选择tablet数量较少的磁盘用于当前tablet的创建。

#### 3.两种磁盘选择算法的性能对比

###### 两种磁盘选择算法在初始状态以及所有tablet创建结束之后的负载情况
（1）初始状态下tablet在各个磁盘（50个）上的分布
（2）使用随机磁盘选择算法完成100000个tablet的创建之后tablet在各个磁盘（50个）上的分布
（3）使用two random choices磁盘选择算法完成100000个tablet的创建之后tablet在各个磁盘（50个）上的分布

![image](https://github.com/weizuo93/MyCode/blob/two_random_choices_disk_selection_for_tablet_creation/image/bar.png)

###### 两种磁盘选择算法在tablet创建过程中的负载分布情况
（1）两种磁盘选择算法在tablet创建过程中的负载分布的极差变化
（2）两种磁盘选择算法在tablet创建过程中的负载分布的标准差变化

![image](https://github.com/weizuo93/MyCode/blob/two_random_choices_disk_selection_for_tablet_creation/image/plot.png)

#### 结论
随机磁盘选择算法并没有考虑各个磁盘之间的负载均衡问题；Two random choices磁盘选择算法有助于负载均衡，即使初始情况下各个磁盘之间的负载并不均衡，随着tablet的创建数量增多，各个磁盘上tablet的数量分布会逐渐趋于均衡。
