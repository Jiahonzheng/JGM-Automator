# Simple-JiaGuoMeng-Agent

* 🔥🔥🔥自动升级政策
* 可选自动完成任务
* 自动收货
* 自动收金币
* 自动升级建筑
* 基于 https://github.com/Jiahonzheng/JGM-Automator 基本上改的面目全非了。。。

* 想只收金色货物的，只要选择收哪些建筑的货就行了，因为金建筑一定是金色货物。
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

### 政策升级界面为检测绿色箭头实现
* <img src="./assets/Policies2.png" style="zoom:30%" />
* 先分离三个通道二值化，再检测轮廓
* <img src="./assets/ArrowFind.png" style="zoom:40%" />
### 收火车时，先点按货物，然后检测绿光获取货物目的地：
* <img src="./assets/Diff2.png" style="zoom:40%" />
* 实现这一功能时，若使用原生adb shell实现的话需要多线程或者多进程才行（分别执行按住和截图命令）
在这里由于uiautomator的强大轮子使得我可以很方便的实现这一功能。

