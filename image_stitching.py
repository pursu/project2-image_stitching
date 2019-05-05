# 我将再次重申，这种方法是一种黑客（hack）行为。
# 我们将审查基本的图像处理操作，包括阈值，轮廓提取，形态学操作等，以获得我们想要的结果。
# 据我所知，OpenCV的Python绑定并没有为我们提供手动提取全景图的最大内部矩形区域所需的信息。

# 导入必要的packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# 构建参数变异其和需要编译的参数
ap = argparse.ArgumentParser()
ap.add_argument("-i","--images",type=str, default='images/scottsdale',
            help="path to input diretory of images to stitch")
ap.add_argument("-o","--output",type=str, default='output2.png',
            help="path to the output image")
ap.add_argument("-c","--crop",type=int, default=1,
            help="whether to crop out largest rectangular region")
args = vars(ap.parse_args())

# 获取输入图片的地址并初始化我们的图片列表
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"])))
images = []

# 循环访问图片的所有路径，导入每张图片，并且把它们加入到我们的图片拼接liebiao
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

# 初始化OpenCV的图片拼接对象并且在之后执行图片拼接
print("[INFO] stitching images...")
# stitcher = cv2.createStitcher() # 如果OpenCV为3.x版本
stitcher = cv2.Stitcher_create()  # 如果OpenCV为4.x版本
(status, stitched) = stitcher.stitch(images)

# 如果status是0，那么OpenCV成功执行了图像拼接
if status == 0:
    # 检查看看，我们是否应该从拼接后的图像中裁剪出最大的矩形区域
    if args["crop"] > 0:
        # 创建一个10个像素的边界，包围住拼接后的图片
        print("[INFO] cropping...")
        stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
                    cv2.BORDER_CONSTANT, (0, 0, 0))

        # 将拼接后的图片转化成灰度图并且用阈值限制它
        # 这样所有比0大的像素被设置成了255
        # （前景）而其他的物体保持为0（背景）
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        # 找到所有阈值图像中的外部轮廓，然后
        # 找到“最大的”的轮廓，这个轮廓将是拼接图像的轮廓/外接边
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        #为掩码分配空间
        # 该掩码将包含拼接图片区域的矩形边框
        mask = np.zeros(thresh.shape, dtype = "uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # 创建两个mask的副本：一个作为我们的实际的最小矩形区域
        # 另一个作为一个计算工具，针对有多少像素需要被移除来构成
        # 最小的矩形区域
        minRect = mask.copy()
        sub = mask.copy()

        # 保持循环，直到没有非零的像素遗留在削减后的图片中
        while cv2.countNonZero(sub) > 0:
           # 侵蚀最小的矩形mask，之后从最小矩形mask中
           # 减去阈值图片，因此我们可以计算是否有非零像素遗留下来
           minRect = cv2.erode(minRect, None)
           sub = cv2.subtract(minRect, thresh)

        # 找到在最小矩形mask中的轮廓，然后提取边框（x,y）坐标点
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)

        # 使用边框的坐标来提取我们的最终拼接的图片的结果
        stitched = stitched[y:y + h, x:x + w]

        # 将拼接好的结果图片写入硬盘
        cv2.imwrite(args["output"], stitched)

        #展示输出的拼接图片的结果
        cv2.imshow("Stitched", stitched)
        cv2.waitKey(0)
#否则拼接失败，可能由于被检测到的关键点不足
else:
	print("[INFO] image stitching failed ({})".format(status))