from target import TargetType
from cv import UIMatcher
import uiautomator2 as u2
import time


def TIME():
    """
    时间输出工具函数。
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class Automator:
    def __init__(self, device: str, targets: dict):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.targets = targets
        self.count = 0
        
        # 开启 trainMode 即可实现每次搬运货物前自动启动应用，搬运后关闭应用，如此反复。
        # 由于启动需等待 40s ，所以默认是不开启 trainMode 的。
        self.trainMode = False
        self.harvestCount = 0

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            try:
                # 由于此处鲁棒性在我本地测试不怎么好，所以个人推荐关闭 trainMode （一家之言）。 
                if self.trainMode:
                    self.d.app_start("com.tencent.jgm")
                    self.isHarvest = False
                    time.sleep(40)
                    self.d.click(1, 1919)

                # 判断是否出现货物。
                for target in self.targets.keys():
                    self._match_target(target)

                # 滑屏拾币
                self._swipe()

                # 取消注释下一行，即可实现对特定建筑的升级
                # self._upgrade(1)

                # 开启 trainMode 后，会输出当前货物的搬运成果，随后关闭应用。
                if self.trainMode:
                    self.count = self.count + 1
                    if self.isHarvest:
                        self.harvestCount = self.harvestCount + 1
                        print(f"{TIME()} 收获！{self.harvestCount}/{self.count}")
                    else:
                        print(f"{TIME()} 未收获……{self.harvestCount}/{self.count}")
                    self.d.app_stop("com.tencent.jgm")
                    time.sleep(2)
            except Exception as e:
                print(e)

    def _swipe(self):
        """
        滑动屏幕，收割金币。
        """
        for i in range(3):
            # 横向滑动，共 3 次。
            sx, sy = self._get_position(i * 3 + 1)
            ex, ey = self._get_position(i * 3 + 3)
            self.d.swipe(sx, sy, ex, ey)

    def _upgrade(self, id):
        """
        升级指定建筑。
        """
        self.d.click(1000, 1100)
        sx, sy = self._get_position(id)
        self.d.click(sx, sy)
        time.sleep(1)
        self.d.click(875, 1750)
        time.sleep(2)
        self.d.click(1000, 1100)

    @staticmethod
    def _get_position(key):
        """
        获取指定建筑的屏幕位置。
        """
        positions = {
            1: (294, 1184),
            2: (551, 1061),
            3: (807, 961),
            4: (275, 935),
            5: (535, 810),
            6: (799, 687),
            7: (304, 681),
            8: (541, 568),
            9: (787, 447)
        }
        return positions.get(key)

    def _get_target_position(self, target: TargetType):
        """
        获取货物要移动到的屏幕位置。
        """
        return self._get_position(self.targets.get(target))

    def _match_target(self, target: TargetType):
        """
        探测货物，并搬运货物。
        """
        # 获取当前屏幕快照
        screen = self.d.screenshot(format="opencv")

        # 由于 OpenCV 的模板匹配有时会智障，故我们探测次数实现冗余。
        counter = 5
        while counter != 0:
            counter = counter - 1

            # 使用 OpenCV 探测货物。
            result = UIMatcher.match(screen, target)

            # 若无探测到，终止对该货物的探测。
            # 实现冗余的原因：返回的货物屏幕位置与实际位置存在偏差，导致移动失效
            if result is None:
                break

            # 在 trainMode 下设置搬运成果。
            if self.trainMode:
                self.isHarvest = True

            sx, sy = result
            # 获取货物目的地的屏幕位置。
            ex, ey = self._get_target_position(target)
            # 搬运货物。
            self.d.swipe(sx, sy, ex, ey)
