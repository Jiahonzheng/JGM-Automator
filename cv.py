from target import TargetType
import cv2,time,numpy as np,matplotlib.pyplot as plt


class UIMatcher:
    @staticmethod
    def match2(screen, target: TargetType):
        # 参考 https://blog.csdn.net/github_39611196/article/details/81164752
 
        min_match_count = 5
        img0 = screen
        img1 = cv2.imread(target.value)  # train image
        height=len(img0)
        width=len(img0[0])
        img2 = img0[int(0.65*height):int(0.9*height),int(0.5*width):width] # 截取截屏的右下角
        hh=len(img2)
        ww=len(img2[0])
        cover1 = np.array([[[0,0], [ww,0], [ww,int(0.28*hh)], [0,int(hh*0.83)]]], dtype = np.int32) #绘制遮罩1
        cover2 = np.array([[[ww,hh], [int(ww*0.9),hh], [int(ww*0.2),hh], [ww,int(0.5*hh)]]], dtype = np.int32) #绘制遮罩2
        img2 = cv2.fillPoly(img2, cover1,  (58,190,149))
        img2 = cv2.fillPoly(img2, cover2,  (58,190,149))
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        
        flann_index_kdtree = 0
        index_params = dict(algorithm=flann_index_kdtree, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        
        # store all the good matches as per Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        
        '''
        设置只有存在10个以上匹配时，采取查找目标 min_match_count=10，否则显示特征点匹配不了
        如果找到了足够的匹配，就提取两幅图像中匹配点的坐标，把它们传入到函数中做变换
        '''
        if len(good) > min_match_count:
            # 获取关键点的坐标
            try:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                # 第三个参数 Method used to computed a homography matrix.
                #  The following methods are possible: #0 - a regular method using all the points
                # CV_RANSAC - RANSAC-based robust method
                # CV_LMEDS - Least-Median robust method
                # 第四个参数取值范围在 1 到 10  绝一个点对的 值。原图像的点经 变换后点与目标图像上对应点的 差 #    差就 为是 outlier
                #  回值中 M 为变换矩 。
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                matchesMask = mask.ravel().tolist()
                # 获取原图像的高和宽
                h, w = len(img1),len(img1[0])
                # 使用得到的变换矩阵对原图想的四个变换获得在目标图像上的坐标
                pts = np.float32([[0, 0], [0, h -1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                point = np.mean(dst, axis=0)
                # print(point[0])
                tarx = int(point[0][0] +0.5*width)
                tary = int(point[0][1] +0.65*height)
                return tarx/width, tary/height
            except(Exception ):
                return 0.5,0.5
        else:
            return None

    @staticmethod
    def trainParking(screen):
        '''
        检测火车是否到达，其实是检测铁轨是否还存在
        @return: 到达:True 没到: False
        '''
        min_match_count = 5
        img0 = screen # query image
        img1 = cv2.imread('./targets/test/Rail3.jpg',0)  # train image
        height=len(img0)
        width=len(img0[0])
        img2 = img0[int(0.65*height):int(0.9*height),int(0.5*width):width]
        
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        
        flann_index_kdtree = 0
        index_params = dict(algorithm=flann_index_kdtree, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        
        if len(good) > min_match_count:
            return False
        else:
            return True

    @staticmethod
    def getPixel(img, rx, ry):
        """
        获取某一坐标的RGB值(灰度图会报错)
        """
        pixel = img[int(ry*len(img)), int(rx*len(img[0]))]
        return pixel[2],pixel[1],pixel[0]

