#请注意我们已经成功执行图像拼接！
# 但那些全景周围的黑色区域呢？那些是什么？
# 这些区域来自执行构建全景图所需的视角warps。
# 有一种方法可以摆脱它们……但我们需要在下一节中实现一些额外的逻辑

# 导入必要的packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# 构建参数编译器和需要编译的参数
ap = argparse.ArgumentParser()
ap.add_argument("-i","--images",type=str, default='images/scottsdale',
                help="path to input directory of images to stitch")
ap.add_argument("-o","--output",type=str, default='output1.png',
                help="path to the output image")
args = vars(ap.parse_args())


# 获取输入图像的地址并初始化我们的图片列表
print("[INFO] loading images...")
testpath = args["images"]
test = paths.list_images(testpath)
test2 = list(test)
imagePaths = sorted(list(paths.list_images(args["images"])))
# images = []

# 循环遍历图片的路径，导入每张图片，并且把它们加入到我们的拼接图片列表中
# for imagePath in imagePaths:
#     image = cv2.imread(imagePath)
#     images.append(image)
img1 = cv2.imread('images/scottsdale/1.jpg')
img2 = cv2.imread('images/scottsdale/2.jpg')
# 初始化OpenCV的图片拼接对象并且然后执行图像拼接
print("[INFO] stitching images...")
# stitcher = cv2.createStitcher(False) # 如果OpenCV为3.x版本
stitcher = cv2.Stitcher_create() # 如果OpenCV为4.x 版本
(status, stitched) = stitcher.stitch((img1,img2))

# 如果status是0，那么OpenCV成功实现了图像拼接
if status == 0:
    # 将拼接后的图片写入硬盘
    cv2.imwrite(args["output"], stitched)

    # 展示拼接好的图片到屏幕上
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)

# 否则拼接失败，可能由于被检测的关键点不足、
else:
    print("[INFO] image stitching failed ({})".format(status))
