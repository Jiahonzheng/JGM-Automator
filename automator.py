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
        trainStop = False # 有可能火车还在进站就截图了，所以等一个周期再收获
        while True:
            # 判断火车
            screen = self.d.screenshot(format="opencv")
            if UIMatcher.trainParking(screen):
                print("Train come!")
                if trainStop is True:
                    self._harvest()
                trainStop = True
            else:
                print("Train leave.")
                trainStop = False


            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 当然，也可以使用图像探测的模式。
            self.d.click(550, 1650)
            # self._upgrade(2)
            # self._upgrade(4)
            self._upgrade(random.randint(1,9))
            self._upgrade(random.randint(1,9))
            self._upgrade(random.randint(1,9))
            self._upgrade(random.randint(1,9))
            
            # 滑动屏幕，收割金币。
            self._swipe()

    def _upgrade(self,id):
        self.d.click(0.9, 0.57)
        sx, sy=self._get_position(id)
        self.d.click(sx, sy)
        time.sleep(0.5)
        self.d.click(860/1080, 1760/1920)
        time.sleep(0.5)
        self.d.click(1000/1080, 1100/1920)
        

    def _swipe(self):
        """
        滑动屏幕，收割金币。
        """
        for i in range(3):
            # 横向滑动，共 3 次。
            sx, sy = self._get_position(i * 3 + 1)
            ex, ey = self._get_position(i * 3 + 3)
            self.d.swipe(sx-0.1, sy+0.05, ex, ey)

    @staticmethod
    def _get_position(key):
        """
        获取指定建筑的屏幕位置。
        """
        positions = {
            1: (294/1080, 1184/1920),
            2: (551/1080, 1061/1920),
            3: (807/1080, 961/1920),
            4: (275/1080, 935/1920),
            5: (535/1080, 810/1920),
            6: (799/1080, 687/1920),
            7: (304/1080, 681/1920),
            8: (541/1080, 568/1920),
            9: (787/1080, 447/1920)
        }
        return positions.get(key)

    def _get_target_position(self, target: TargetType):
        """
        获取货物要移动到的屏幕位置。
        """
        # print("Target Number =%d"%self.targets.get(target))
        return self._get_position(self.targets.get(target))



    def _harvest(self):
        """
        探测货物，并搬运货物
        return: 货物坐标，货物类型
        """
        # 获取当前屏幕快照
        detected = None
        screen = self.d.screenshot(format="opencv")
        
        for target in TargetType:
            print("Detecting %s"%target, end="")
            detected = UIMatcher.match2(screen, target)
            if detected is not None:
                print("%s is detected."%target)
                # 搬运5次
                for itr in range(5):
                    self._move_good(self,target, detected)
                detected = None
            else:
                print("")
              
    @staticmethod       
    def _move_good(self, good: TargetType, source):
        ex, ey = self._get_target_position(good)
        sx, sy = source
        self.d.swipe(sx, sy, ex, ey)


