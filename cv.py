from target import TargetType
import cv2,time,numpy as np


class UIMatcher:
    @staticmethod
    def match(screen, target: TargetType):
        """
        在指定快照中确定货物的屏幕位置。
        """
        # 获取对应货物的图片。
        # 有个要点：通过截屏制作货物图片时，请在快照为实际大小的模式下截屏。
        template = cv2.imread(target.value)
        x, y = template.shape[0:2]
        template = cv2.resize(template, (int(y / 2), int(x / 2)))
        # cv2.imshow(screen,1)
        height=len(screen)
        width=len(screen[0])
        screen = screen[int(0.6*height):height,int(0.5*width):width]
        # cv2.namedWindow("Image") 
        # cv2.imshow("Image", screen) 
        # # cv2.waitKey(0) ti
        # time.sleep(1)
        # cv2.destroyAllWindows()
        # 获取货物图片的宽高。
        th, tw = template.shape[:2]

        # 调用 OpenCV 模板匹配。
        res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # 矩形左上角的位置。
        tl = min_loc

        # 阈值判断。
        if min_val > 0.15:
            return None

        # 这里，我随机加入了数字（15），用于补偿匹配值和真实位置的差异。
        # return (tl[0] + tw / 2 + 15 + 1080*0.5)/1080, (tl[1] + th / 2 + 15 + 1920*0.6)/1920
        return (tl[0] + tw  + 15 + 1080*0.5)/1080+0.05, (tl[1] + th + 15 + 1920*0.6)/1920+0.1 # 960*540

    @staticmethod
    def match2(screen, target: TargetType):
        # 参考 https://blog.csdn.net/github_39611196/article/details/81164752
        min_match_count = 5
        img0 = screen # query image
        img1 = cv2.imread(target.value,0)  # train image
        height=len(img0)
        width=len(img0[0])
        img2 = img0[int(0.65*height):int(0.9*height),int(0.5*width):width]
        
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
                h, w = img1.shape
                # 使用得到的变换矩阵对原图想的四个变换获得在目标图像上的坐标
                pts = np.float32([[0, 0], [0, h -1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                point = np.mean(dst, axis=0)
                # print(point[0])
                tarx = int(point[0][0] +0.5*width)
                tary = int(point[0][1] +0.65*height)
                return tarx/width, tary/height
            except(Exception ):
                return None
            # print(tarx,tary)
            # # 将原图像转换为灰度图
            # # img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            # img4 = cv2.circle(img0,(tarx,tary),10,255,thickness=3)
        else:
            # print('Not enough matches are found - %d/%d' % (len(good), min_match_count))
            # matchesMask = None
            return None

    @staticmethod
    def trainParking(screen):
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
        
        # store all the good matches as per Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        
        if len(good) > min_match_count:
            return False
        else:
            # print('Not enough matches are found - %d/%d' % (len(good), min_match_count))
            # matchesMask = None
            return True

    @staticmethod
    def read(filepath: str):
        """
        工具函数，用于读取图片。
        """
        return cv2.imread(filepath)
