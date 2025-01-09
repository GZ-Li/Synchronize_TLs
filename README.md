

本文档描述根据给定经纬度坐标，在Carla和SUMO地图中自动化添加交通信号灯的方法。即输入为经纬度坐标（如lat=130, lon=60），输出为可在SUMO中运行的`.net.xml`路网文件与可用于渲染Carla地图的`.xodr`文件。在后续研究中，该转换可将前端展示界面（如Unity）中设置的交通信号灯根据经纬度信息同步到Carla中。该同步过程旨在解决两个问题：

* 坐标表示不一致：Carla的地图`.xml`文件只包含道路编号信息，表示道路之间的连接关系；不展示道路的具体地理位置信息，难以直接同步；

* 实现自动化同步：已有做法主要基于手动放置交通信号灯。本文档阐述的同步过程通过修改`.xml`文件，跳过了从可视化界面手动放置信号灯的环节，为大规模地图同步提供便利。

本文档所涉及的代码开源在：https://github.com/GZ-Li/Synchronize\_TLs

# 步骤一：在SUMO的路网文件中添加信号灯

输入：经纬度坐标、原始SUMO路网文件(`.net.xml`)；

输出：编辑后的SUMO路网文件(`.net.xml`)

在`synchronize_TL_net.py`中修改如下参数：

```python
net_path = ""
output_net_path = ""
target_coor = []  #e.g. ['1131.7', '678.29']
```

修改后运行程序：

```python
python synchronize_TL_net.py
```

即可得到修改后的SUMO路网文件。



# 步骤二：根据修改后的SUMO路网文件生成Opendrive文件

利用SUMO内置`netconvert`工具进行转换：

```python
netconvert -s sumo_net_path --opendrive-output opendrive_output_path
```

得到输出的opendrive文件。



# 步骤三：修改直接输出的Opendrive文件

由于目前SUMO将`.net.xml`转化为`.xodr`文件的功能尚不完善，且在本项目中存在版本不一致的问题，因此通过`synchronize_TL_xodr.py`进行修正。

输入：待修正的opendrive(`.xodr`)文件路径；

输出：修正后的opendrive文件输出路径；

修改如下参数：

```python
xodr_path = "C:\\Users\\pc\\Desktop\\20250106_temp\\example\\test_add_TLs_0108_case1.xodr"
output_xodr_path = "C:\\Users\\pc\\Desktop\\20250106_temp\\example\\test_add_TLs_0108_case1_modified.xodr"
```

修改后运行程序：

```python
python synchronize_TL_xodr.py
```

即可得到在指定位置添加交通信号灯后的opendrive文件。



后续，参考[将Unity地图同步到Carla与SUMO的方案](https://scn8jxylm0ia.feishu.cn/wiki/SDQQwZ9XUiYUcfkE5EKcVYugnHb)，通过RoadRunner生成Carla地图渲染所需要的`.fbx`文件，导入Carla中，即完成交通信号灯的同步过程。
