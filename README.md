# JGM Automator

* 基于 https://github.com/Jiahonzheng/JGM-Automator 改进
* ~~基于opencv的特征值匹配 [CSDN博客](https://blog.csdn.net/github_39611196/article/details/81164752)~~
* ~~更改搜索逻辑，大幅提高了搜索速度 ~~
* ~~货物不再要求原分辨率图片，理论上对手机或模拟器分辨率只要求16:9~~
* 收货方式改为先按下货物寻找绿光位置再把货物挪过去，简单方便，准确更高

## 安装与运行
运行前的准备：

[uiautomator2](https://github.com/openatx/uiautomator2)是python封装的安卓自动化测试库，比原生adb shell命令强大得多，方便得多。 

如果cv库安装太慢可以用清华大学的tuna源
```bash
# 安装依赖
python -m pip install uiautomator2 opencv-python opencv-contrib-python==3.4.2.16

# adb 连接
# 如果使用 MuMu 模拟器，请先在shell中adb连接mumu
adb connect 127.0.0.1:7555

# 获取 device 名称,并填写至 main.py
adb devices

# 在已完成 adb 连接后，在手机安装 ATX 应用
python -m uiautomator2 init

# 打开 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的。
```

如何运行：
``` bash
python main.py
```
因为火车识别还不是很准确，这里用了个折中的方法：

在main.py中，注释两者其一可以选择是只收金币还是收火车一起
```py
    instance.start()
    # instance.start_without_train()
```

## 说明

+ 建筑编号

<img src="./assets/Screenshot.png" style="zoom:40%" />


+ 升级列表和收货列表
  在 `main.py`里，定义这两个列表，即可指定要升级的建筑和要收货的建筑
  ```py
   # 升级建筑列表
    up_list = [(2,1),(3,5)] # 2号升级1次， 3号升级5次
    # 收货过滤列表
    harvest_filter = [5,6,7,8] # 只收取5,6,7,8号建筑的货物
  ```

## 实现细节
* 收火车时，先点按货物，然后检测绿光获取货物目的地：
<img src="./targets/test/Diff2.png" style="zoom:40%" />
* 实现这一功能时，若使用原生adb shell实现的话需要多线程或者多进程才行（分别执行按住和截图命令）
在这里由于uiautomator的强大轮子使得我可以很方便的实现这一功能。

### 以下功能已废弃：
+ ~~截图后，分割右下角，并打上遮罩，提高特征值匹配速度，减少错误：~~
+ <img src="./targets/test/Figure_1.png" style="zoom:40%" />
+ <img src="./targets/test/Figure_2.png" style="zoom:40%" />