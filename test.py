# from target import TargetType
# import cv2,time
# from matplotlib import pyplot as

# screen = cv2.imread('./targets/Screenshot.png')
# template = cv2.imread(TargetType.Chair.value)
# x, y = template.shape[0:2]
# template = cv2.resize(template, (int(y / 2), int(x / 2)))
# # cv2.imshow(screen,1)
# height=len(screen)
# width=len(screen[0])
# screen = screen[int(0.65*height):int(0.9*height),int(0.5*width):width]
# cv2.namedWindow("Image") 
# cv2.imshow("Image", screen) 
# cv2.waitKey(0)
# # cv2.destroyAllWindows()
# # 获取货物图片的宽高。
# th, tw = template.shape[:2]
# # 调用 OpenCV 模板匹配。
# res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# # 矩形左上角的位置。
# tl = min_loc

# # 阈值判断。
# if min_val > 0.15:
#     return None





from target import TargetType
import numpy as np
import cv2
import matplotlib.pyplot as plt
import automator


        
        
# # 获取对应货物的图片。
# # 有个要点：通过截屏制作货物图片时，请在快照为实际大小的模式下截屏。
# # img0 = cv2.imread('./targets/test/Screenshot.png',0) # query image
# # img1 = cv2.imread('./targets/cross.jpg',0)  # train image
# screen = cv2.imread('./targets/test/Mu.png',0)
# template = cv2.imread('./targets/test/Cross.png',0)
# x, y = template.shape[0:2]
# # cv2.imshow(screen,1)
# height=len(screen)
# width=len(screen[0])
# screen = screen[int(0.6*height):height,int(0.5*width):width]
# # cv2.namedWindow("Image") 
# # cv2.imshow("Image", screen) 
# # # cv2.waitKey(0) ti
# # time.sleep(1)
# # cv2.destroyAllWindows()
# # 获取货物图片的宽高。
# th, tw = template.shape[:2]

# # 调用 OpenCV 模板匹配。
# res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# left_top = max_loc  # 左上角
# right_bottom = (left_top[0] + tw, left_top[1] + th)  # 右下角
# cv2.rectangle(screen, left_top, right_bottom, 255, 2)  # 画出矩形位置
# plt.imshow(screen, cmap='gray')
# plt.show()

# # 矩形左上角的位置。
# tl = min_loc

# # 阈值判断。
# if min_val > 0.15:
#     print(0)
# else:
#     print(1)


    
min_match_count = 5
img0 = cv2.imread('./targets/test/Mu2.png',0) # query image
img1 = cv2.imread('./targets/Cotton.jpg',0)  # train image
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
    # 获取关键点的坐标
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
    # 将原图像转换为灰度图
    print(1)
else:
    # print('Not enough matches are found - %d/%d' % (len(good), min_match_count))
    matchesMask = None
    print('Not enough matches are found - %d/%d' % (len(good), min_match_count))
    print(0)
draw_params = dict(matchColor=(0, 255, 0),
            singlePointColor=None,
            matchesMask=matchesMask,
            flags=2)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
plt.imshow(img3, cmap='gray')
plt.show()


