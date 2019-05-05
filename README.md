# project2-image_stitching
The code of images stitching by OpenCV.


I just debug the source code of https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/ and test it in my environment successfully by myself.


# Environment
  Python 3.6
  
  
  Anaconda3
  
  
  OpenCV 4.0(This is important !!!)
  
  imutils
  
# Note


There is the fatal bug in this code that when this code runs  OpenCV 3.2 or below（maybe or not, because I just test it on OpenCV 3.2.0 and OpenCV 4.0). And there has not been a good way to solve it except update the OpenCV to later version such as 4.0. So I suggested that this code is better to run in OpenCV 4.0. You can get the detail of the bug in https://stackoverflow.com/questions/43002279/error-with-simple-stitching-and-opencv-3-2-0-cv2-cpp152-error-215-the-da

# Result
![image_stitching_simple](output1.png)


![image_stitching](output2.png)
