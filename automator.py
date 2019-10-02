from target import TargetType
from cv import UIMatcher
import uiautomator2 as u2
import time,random


class Automator:
    def __init__(self, device: str, targets: dict):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.targets = targets

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            # 判断是否出现货物。
            for target in TargetType:
                self._match_target(target)

            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 当然，也可以使用图像探测的模式。
            self.d.click(550, 1650)
            self._upgrade(2)
            self._upgrade(4)
            # self._upgrade(random.randint(1,9))
            # self._upgrade(random.randint(1,9))
            # 滑动屏幕，收割金币。
            self._swipe()

    def _upgrade(self,id):
        self.d.click(1000, 1100)
        sx, sy=self._get_position(id)
        self.d.click(sx, sy)
        time.sleep(0.5)
        self.d.click(860, 1760)
        time.sleep(0.5)
        self.d.click(1000, 1100)
        

    def _swipe(self):
        """
        滑动屏幕，收割金币。
        """
        for i in range(3):
            # 横向滑动，共 3 次。
            sx, sy = self._get_position(i * 3 + 1)
            ex, ey = self._get_position(i * 3 + 3)
            self.d.swipe(sx-100, sy+70, ex, ey)

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
        counter = 6
        while counter != 0:
            counter = counter - 1

            # 使用 OpenCV 探测货物。
            result = UIMatcher.match(screen, target)

            # 若无探测到，终止对该货物的探测。
            # 实现冗余的原因：返回的货物屏幕位置与实际位置存在偏差，导致移动失效
            if result is None:
                break

            sx, sy = result
            # 获取货物目的地的屏幕位置。
            ex, ey = self._get_target_position(target)

            # 搬运货物。
            self.d.swipe(sx, sy, ex, ey)
