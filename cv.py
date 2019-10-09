
import cv2,numpy as np
from util import *

class UIMatcher:

    @staticmethod
    def findGreenArrow(screen):
        '''
        检测政策界面中 绿箭头的中心位置
        @return: 绿箭头坐标list
        '''
        # 增加判断screen，也就是截图是否成功的判断
        if screen.size:
            dstPoints = []
            img2 = cv2.split(screen)
            # 分离R 二值化
            ret, dst1 = cv2.threshold(img2[0], 20, 255, cv2.THRESH_BINARY_INV)
            # 分离G 二值化
            ret, dst2 = cv2.threshold(img2[1], 220, 255, cv2.THRESH_BINARY)
            # 分离B 二值化
            ret, dst3 = cv2.threshold(img2[2], 20, 255, cv2.THRESH_BINARY_INV)
            img2 = dst1&dst2&dst3 # 相与
            # 模糊边界
            # img2 = cv2.GaussianBlur(img2, (5, 5), 0)
            # import matplotlib.pyplot as plt
            # plt.imshow(img2,cmap='gray')
            # plt.show()
            # 找轮廓
            cnts = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            if cnts[1]:
                for c in cnts[1]:
                    # 获取中心点
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #
                    dstPoints.append((cX,cY))

                    # 画出轮廓和中点
                    # cv2.drawContours(img2, [c], -1, (0, 255, 0), 2)
                    # cv2.circle(img2, (cX, cY), 20, (255, 255, 255), 1)
                    # cv2.putText(img2, "center", (cX - 20, cY - 20),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    # plt.imshow(img2,cmap='gray')
                    # plt.show()
            return dstPoints
        else:
            raise Exception('Screen process is unsuccessful')
    
    @staticmethod
    def findTaskBubble(screen):
        '''
        检测城市任务那块区域黄色气泡是否出现
        @return: 是否出现
        '''
        dstPoints = []
        h=len(screen)
        w=len(screen[0])
        # 截取气泡周围区域
        img2 = cv2.split(screen[int(0.777*h):int(0.831*h),int(0.164*w):int(0.284*w)])
        ret, B = cv2.threshold(img2[0], 120, 255, cv2.THRESH_BINARY_INV)
        ret, G = cv2.threshold(img2[1], 210, 255, cv2.THRESH_BINARY_INV)
        ret, R = cv2.threshold(img2[2], 230, 255, cv2.THRESH_BINARY)
        img2 = R&B&G # 相与
        # 模糊边界
        img2 = cv2.GaussianBlur(img2, (5, 5), 0)
        # 找轮廓
        cnts = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts[1]):
            return True
        else:
            return False

    @staticmethod
    def findGreenLight(diff_screens, th=100):
        screen_before, screen_after = diff_screens
        # 转换成有符号数以处理相减后的负值
        screen_before = screen_before.astype(np.int16)
        screen_after = screen_after.astype(np.int16)

        diff = screen_after - screen_before
        h=len(diff)
        w=len(diff[0])
        B,G,R = cv2.split(diff)
        # 负值取0
        G[G < 0] = 0
        G = G.astype(np.uint8)
        # 二值化后相与, 相当于取中间范围内的值
        ret, G1 = cv2.threshold(G, 140, 255, cv2.THRESH_BINARY_INV)
        ret, G2 = cv2.threshold(G, 22, 255, cv2.THRESH_BINARY)
        img0 = G1&G2
        # 均值模糊(降噪 好像也没啥卵用) 
        img0 = cv2.medianBlur(img0,9)
        # import matplotlib.pyplot as plt
        # plt.imshow(img0,cmap='gray')
        # plt.show()
        buildings = []
        for building_ID in range(1,10):
            square = UIMatcher.getLittleSquare(img0,BUILDING_POSITIONS[building_ID],edge=0.1)
            buildings.append(np.mean(square))
        # 返回平均亮度最强的建筑物
        return buildings.index(max(buildings))+1

    @staticmethod
    def detectCross(screen, th = 5):
        '''
        探测叉叉是否出现, 先截取叉叉所在的小方块,然后对灰度图二值化,再求平均值判断
        '''
        screen = cv2.cvtColor(screen,cv2.COLOR_RGB2GRAY)
        good_id_list = []
        for good_id in CROSS_POSITIONS.keys():
            square = UIMatcher.getLittleSquare(screen,CROSS_POSITIONS[good_id])
            ret, W = cv2.threshold(square, 250, 255, cv2.THRESH_BINARY)
            # import matplotlib.pyplot as plt
            # plt.imshow(W,cmap='gray')
            # plt.show()
            # 二值化后求平均值
            if np.mean(W) > th:
                good_id_list.append(good_id)
        # print(good_id_list)
        return good_id_list

    @staticmethod
    def getPixel(img, rx, ry):
        """
        获取某一坐标的RGB值(灰度图会报错)
        """
        pixel = img[int(ry*len(img)), int(rx*len(img[0]))]
        return pixel[2],pixel[1],pixel[0]

    @staticmethod
    def getLittleSquare(img, rel_pos, edge=0.01):
        '''
        截取rel_pos附近一个小方块
        '''
        rx,ry = rel_pos
        h=len(img)
        w=len(img[0])
        scale = h/w
        x0 = int((rx-edge*scale)*w)
        x1 = int((rx+edge*scale)*w)
        y0 = int((ry-edge)*h)
        y1 = int((ry+edge)*h)
        return img[y0:y1,x0:x1]
