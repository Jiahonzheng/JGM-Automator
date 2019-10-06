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
        print(self.dWidth, self.dHeight)
        self.appRunning = False
        
    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            # 判断jgm进程是否在前台
            if self.d.app_wait("com.tencent.jgm", front=True):
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    print("App is front. JGM agent start in 5 seconds")
                    time.sleep(5) 
                self.appRunning = True
            else:
                print('Not Running.')
                self.appRunning = False
                continue
            
            # 判断是否可升级政策
            self.check_policy()
            # 判断货物那个叉叉是否出现
            good_id = self._has_good()
            if good_id > 0:
                print("[%s] Train come."%time.asctime())
                self._harvest2(self.harvest_filter, good_id)
                self._upgrade([random.choice(self.upgrade_list)])
                # 滑动屏幕，收割金币。
                self._swipe()
            else:
                print("[%s] No Train."%time.asctime())
                findSomething = True
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
            self.check_policy()
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
                for i in range(-10,11):# 取一条线上20个点,取平均值
                    r,g,b = UIMatcher.getPixel(diff_screen, (x+1.73*i)/540,(y+line+i)/960)
                    R+=r
                    G+=g
                    B+=b
                # 如果符合绿光的条件
                if R/20 >220   and G/20 < 70:
                    lineCount += 1           
            if lineCount > 1:
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

    def _harvest2(self,building_filter,good:int):
        '''
        新的傻瓜搬货物方法,先按住截图判断绿光探测货物目的地,再搬
        '''
        short_wait()
        screen = self.d.screenshot(format="opencv")
        pos_id = self.guess_good(good)
        if pos_id != 0 and pos_id in building_filter:
            # 搬5次
            self._move_good_by_id(good, self._get_position(pos_id), times=4)
            short_wait()
             
    def _move_good_by_id(self, good: int, source, times=1):
        try:
            sx, sy = GOODS_POSITIONS[good]
            ex, ey = source
            for i in range(times):
                self.d.drag(sx, sy, ex, ey, duration = 0.1)
                short_wait()
        except(Exception):
            pass    

    def _has_good(self):
        screen = self.d.screenshot(format="opencv")  
        for good_id in CROSS_POSITIONS.keys():
            if self._detect_cross(screen, CROSS_POSITIONS[good_id]):
                return good_id
        return 0
       
    def _detect_cross(self, screen, positon):
        x,y = positon
        # print(x,y)
        R,G,B = 0,0,0
        for i in range(-4,5):# 取一条45度线线上8个点,取平均值
            r,g,b = UIMatcher.getPixel(screen, x+i/self.dWidth,y+i/self.dHeight)
            R+=r
            G+=g
            B+=b
            # 如果符合叉叉（白色）的条件
        if R/8 >250 and G/8 > 250 and B/8 > 250:
            return True
        return False

    def check_policy(self):
        # 看看政策中心那里有没有冒绿色箭头气泡
        if len(UIMatcher.findArrow(self.d.screenshot(format="opencv"))):
            # 打开政策中心
            self.d.click(0.206, 0.097)
            mid_wait()
            # 确认升级
            self.d.click(0.077, 0.122)
            # 拉到顶
            self._slide_to_top()
            # 开始找绿色箭头
            for i in range(5):
                screen = self.d.screenshot(format="opencv")
                arrows = UIMatcher.findArrow(screen)
                if len(arrows):
                    x,y = arrows[0]
                    self.d.click(x,y) # 点击这个政策
                    short_wait()
                    self.d.click(0.511, 0.614) # 确认升级
                    print("[%s] Policy upgraded"%time.asctime())
                    self._back_to_main()

                    return
            self._back_to_main()

    def _slide_to_top(self):
        for i in range(3):
            self.d.swipe(0.488, 0.302,0.482, 0.822)
            short_wait()

    def _back_to_main(self):
        for i in range(3):
            self.d.click(0.057, 0.919)
            short_wait()
              


def short_wait():
    time.sleep(0.2)

def mid_wait():
    time.sleep(0.5)

GOODS_POSITIONS = { 1: (0.609,0.854),
                    2: (0.758,0.815),
                    3: (0.896,0.766)}

# 绿色光环检测的中心位置  540*960下的绝对位置
GOODS_SAMPLE_POSITIONS = {  1: (98, 634),
                            2: (226, 569),
                            3: (346, 508),
                            4: (96, 503),
                            5: (221, 439),
                            6: (346, 377),
                            7: (100, 379),
                            8: (223, 316),
                            9: (349, 249)}

# 货物的那个叉叉的位置 相对位置
CROSS_POSITIONS = { 1: (0.632, 0.878),
                    2: (0.776, 0.836),
                    3: (0.912, 0.794)}