from target import TargetType
from cv import UIMatcher
import uiautomator2 as u2
import time,random



class Automator:
    def __init__(self, device: str, targets: dict, upgrade_list: list, harvest_filter:list):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.targets = targets
        self.upgrade_list = upgrade_list
        self.harvest_filter = harvest_filter
        

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        
        trainStop = False # 有可能火车还在进站就截图了，所以等停稳再收获
        findSomething = True
        trainCount = 0
        '''
        这段逻辑有点吃屎，我也懒得改了
        主要实现的是：
            判断火车是否停稳(上次检测火车不在，这次检测在，那么就是停稳)
            火车停稳后只搜索固定次数（比如5次），超过搜索次数后就不搜索了，继续收金币和升级
        '''
        while True:
            # 判断火车
            screen = self.d.screenshot(format="opencv")
           
            if UIMatcher.trainParking(screen):
                
                if trainStop is False:
                    
                    time.sleep(0.5) # 等火车停稳
                    print("[%s] Train come!"%time.asctime())
                if trainCount < 5 and findSomething:
                    self._harvest(self.harvest_filter)
                else:
                    findSomething = False
                    self._upgrade(self.upgrade_list)
                    # 滑动屏幕，收割金币。
                    self._swipe()
                    pass
                trainStop = True
                trainCount += 1
                continue
            else:
                print("[%s] No Train."%time.asctime())
                findSomething = True
                trainStop = False
                trainCount = 0


            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 当然，也可以使用图像探测的模式。
            self.d.click(550, 1650)
            self._upgrade(self.upgrade_list)
            # 滑动屏幕，收割金币。
            self._swipe()

    def _upgrade_one_with_count(self,id,count):
        sx, sy=self._get_position(id)
        self.d.click(sx, sy)
        time.sleep(0.3)
        for i in range(count):
            self.d.click(0.798, 0.884)
            # time.sleep(0.1)
    
    def _switch_upgrade_interface(self):
        self.d.click(0.9, 0.57)

    def _open_upgrade_interface(self):
        screen = self.d.screenshot(format="opencv")
        # 判断升级按钮的颜色，蓝比红多就处于正常界面，反之在升级界面
        R, G, B = UIMatcher.getPixel(screen,0.974,0.615)
        if B > R:
            self.d.click(0.9, 0.57)

    def _close_upgrade_interface(self):
        screen = self.d.screenshot(format="opencv")
        # 判断升级按钮的颜色，蓝比红多就处于正常界面，反之在升级界面
        R, G, B = UIMatcher.getPixel(screen,0.974,0.615)
        if B < R:
            self.d.click(0.9, 0.57)

    def _upgrade(self, upgrade_list):
        self._open_upgrade_interface()
        for building,count in upgrade_list:
           self._upgrade_one_with_count(building,count) 
        self._close_upgrade_interface()
    
    def _swipe(self):
        """
        滑动屏幕，收割金币。
        """
        print("[%s] Swiped."%time.asctime())
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



    def _harvest(self, building_filter):
        """
        探测货物，并搬运货物，过滤想要的建筑位置号
        @param: 需要收取的坐标列表
        @return: 货物坐标，货物类型
        """
        # 获取当前屏幕快照
        detected = None
        screen = self.d.screenshot(format="opencv")
        
        for target in TargetType:
            # print("Detecting %s"%target, end="")
            detected = UIMatcher.match2(screen, target)
            if detected is not None:
                # 如果在过滤列表里
                if self.targets.get(target) not in building_filter:
                    print("Skip ---%s---."%target)
                    continue
                print("Detected +++%s+++."%target)
                # 搬运5次
                for itr in range(5):
                    self._move_good(target, detected)
                detected = None
            # else:
            #     # print("")
                    
    def _move_good(self, good: TargetType, source):
        try:
            ex, ey = self._get_target_position(good)
            sx, sy = source
            self.d.swipe(sx, sy, ex, ey)
        except(Exception):
            pass