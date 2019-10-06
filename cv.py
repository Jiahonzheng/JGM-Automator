
import cv2,numpy as np,matplotlib.pyplot as plt


class UIMatcher:

    @staticmethod
    def findArrow(screen):
        '''
        检测政策界面中 绿箭头的中心位置
        @return: 绿箭头坐标list
        '''
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
        img2 = cv2.GaussianBlur(img2, (5, 5), 0)
        # 找轮廓
        cnts = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
    
    @staticmethod
    def getPixel(img, rx, ry):
        """
        获取某一坐标的RGB值(灰度图会报错)
        """
        pixel = img[int(ry*len(img)), int(rx*len(img[0]))]
        return pixel[2],pixel[1],pixel[0]

    @staticmethod
    def showimg(screen):
        plt.imshow(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        plt.show()
