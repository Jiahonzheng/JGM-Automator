# JGM Automator

> 基于 https://github.com/Jiahonzheng/JGM-Automator 改进而来
> 改的地方比较多，我怕合并回去和作者原思路冲突太大，就先放着吧
> 取消了训练模式的设定，并且将模板匹配改为特征值匹配
> 提高了搜索速度
> 不再要求原分辨率图片，理论上对手机或模拟器分辨率只要求16:9

## 安装与运行

```bash
# 安装依赖
python -m pip install uiautomator2 opencv

# adb 连接
# 使用 MuMu 模拟器，确保屏幕大小为 1920（长） * 1080（宽）
adb connect 127.0.0.1:7555

# 获取 device 名称,并填写至 main.py
adb devices

# 在已完成 adb 连接后，在手机安装 ATX 应用
python -m uiautomator2 init

# 打开 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的。

# 进入游戏页面，启动自动脚本。
python main.py
```

## 说明

+ 建筑编号

<img src="./assets/Screenshot.png" style="zoom:40%" />

+ Weditor

我们可以使用 Weditor 工具，获取屏幕坐标，以及在线编写自动化脚本。

```bash
# 安装依赖
python -m pip install --pre weditor

# 启动 Weditor
python -m weditor
```

+ 货物素材

我们可以自行制作货物的素材：先生成屏幕快照，~~随后在**实际大小**下~~，截取货物图片，保存至 `targets/` 目录下，并在 `target.py` 声明对应的货物种类及其图片路径。