
import cv2,numpy as np
from util import GOODS_SAMPLE_POSITIONS

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
    def findGreenLight(diff_screens):
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
        for pos_ID in range(1,10):
            x,y = GOODS_SAMPLE_POSITIONS[pos_ID]
            lineCount = 0
            for line in range(-6,2): #划8条线, 任意2条足够亮都算
                sumG = 0
                for i in range(-10,10):# 取一条线上20个点,取平均值
                    # 相对坐标
                    rx = (x+1.73*i)/540
                    ry = (y+line+i)/960
                    sumG += img0[int(ry*h),int(rx*w)]
                # 如果符合条件               
                if sumG/20 > 250:
                    lineCount += 1 
            # 任意2条足够亮   
            # print(lineCount)       
            if lineCount > 1:
                print(pos_ID,"lineCount=",lineCount)
                return pos_ID
        return 0

    @staticmethod
    def getPixel(img, rx, ry):
        """
        获取某一坐标的RGB值(灰度图会报错)
        """
        pixel = img[int(ry*len(img)), int(rx*len(img[0]))]
        return pixel[2],pixel[1],pixel[0]

