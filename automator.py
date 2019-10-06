from target import TargetType
from cv import UIMatcher
import uiautomator2 as u2
import time,random,cv2
import matplotlib.pyplot as plt



class Automator:
    def __init__(self, device: str, upgrade_list: list, harvest_filter:list):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.upgrade_list = upgrade_list
        self.harvest_filter = harvest_filter
        self.dWidth, self.dHeight = self.d.window_size()
        self.appRunning = False
        
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
            if self.d.app_wait("com.tencent.jgm", front=True):
                print('App is front.')
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    print("JGM agent start in 5 seconds")
                    time.sleep(5) 
                self.appRunning = True
            else:
                print('Not Running.')
                self.appRunning = False
                continue

            # 判断火车,但是准确率不好，还要再改
            screen = self.d.screenshot(format="opencv")
            if UIMatcher.trainParking(screen):
                print("[%s] Train come!"%time.asctime())
                self._harvest2(self.harvest_filter)
                self._upgrade([random.choice(self.upgrade_list)])
                # 滑动屏幕，收割金币。
                self._swipe()
            else:
                print("[%s] No Train."%time.asctime())
                findSomething = True
                trainStop = False
                trainCount = 0
            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 不管它出不出现，每次都点一下 确定 所在的位置
            self.d.click(550/1080, 1650/1920)
            self._upgrade([random.choice(self.upgrade_list)])
            # 滑动屏幕，收割金币。
            self._swipe()

    def start_without_train(self):
        """
        只收金币和升级，不收火车
        """
        trainCount = 0
        while True:
            trainCount = (trainCount+1) % 2
            if self.d.app_wait("com.tencent.jgm", front=True, timeout=1):
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    print("JGM agent start in 5 seconds")
                    time.sleep(5)
                if trainCount:
                    self._upgrade([random.choice(self.upgrade_list)])
                else:
                    self._swipe()
                
                self.appRunning = True
            else:
                print('App not running.')
                self.appRunning = False
                continue

    def _upgrade_one_with_count(self,id,count):
        sx, sy=self._get_position(id)
        self.d.click(sx, sy)
        time.sleep(0.3)
        for i in range(count):
            self.d.click(0.798, 0.884)
            # time.sleep(0.1)

    def guess_good(self, good_id):
        '''
        按住货物，探测绿光出现的位置
        这一段应该用numpy来实现，奈何我对numpy不熟。。。
        '''
        diff_screen = self.get_screenshot_while_touching(GOODS_POSITIONS[good_id])
        pos_ID = 0   
        for pos_ID in range(1,10):
            # print('hhhh')
            x,y = GOODS_SAMPLE_POSITIONS[pos_ID]
            lineCount = 0
            for line in range(-2,7): #划8条线, 任意2条判定成功都算
                R,G,B = 0,0,0
                for i in range(-10,10):# 取一条线上10个点,取平均值
                    r,g,b = UIMatcher.getPixel(diff_screen, (x+1.73*i)/540,(y+line+i)/960)
                    R+=r
                    G+=g
                    B+=b
                # 如果符合绿光的条件
                if R/10 >220   and G/10 < 70:
                    lineCount += 1
            # print (R/10,G/10,B/10,pos_ID)            
            if lineCount > 1:
                print(pos_ID)
                return pos_ID
        return 0

    def get_screenshot_while_touching(self, location, pressed_time=0.2):
        '''
        Get screenshot with screen touched.
        '''
        screen2 = self.d.screenshot(format="opencv")
        h,w = len(screen2),len(screen2[0])
        x,y = (location[0] * w,location[1] *h)
        # 按下
        self.d.touch.down(x,y)
        # print('[%s]Tapped'%time.asctime())
        time.sleep(pressed_time)
        # 截图
        screen = self.d.screenshot(format="opencv")
        # print('[%s]Screenning'%time.asctime())
        # 松开
        self.d.touch.up(x,y)
        # 返回按下前后两幅图的差值
        return screen- screen2

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


    def _harvest2(self,building_filter):
        '''
        新的傻瓜搬货物方法,先按住截图判断绿光探测货物目的地,再搬
        '''
        for good in range(1,4):
            time.sleep(0.2)
            screen = self.d.screenshot(format="opencv")
            if not UIMatcher.trainParking(screen):
                return
            pos_id = self.guess_good(good)
            if pos_id != 0 and pos_id in building_filter:
                # 搬5次
                print("got")
                self._move_good_by_id(good, self._get_position(pos_id), times=4)
                time.sleep(0.2)
             


    def _move_good_by_id(self, good: int, source, times=1):
        try:
            sx, sy = GOODS_POSITIONS[good]
            ex, ey = source
            for i in range(times):
                self.d.drag(sx, sy, ex, ey, duration = 0.1)
                time.sleep(0.2)
        except(Exception):
            pass    

      

def showimg(screen):
    plt.imshow(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    plt.show()

GOODS_POSITIONS = { 1: (0.609,0.854),
                    2: (0.758,0.815),
                    3: (0.896,0.766)}

GOODS_SAMPLE_POSITIONS = {  1: (98, 634),
                            2: (226, 569),
                            3: (346, 508),
                            4: (96, 503),
                            5: (221, 439),
                            6: (346, 377),
                            7: (100, 379),
                            8: (223, 316),
                            9: (349, 249)}