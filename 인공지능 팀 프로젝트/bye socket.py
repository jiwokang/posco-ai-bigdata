import numpy as np
import cv2

def showVideo():
    try:
        print("카메라를 구동합니다.")
        cap=cv2.VideoCapture(-1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        cap.set(cv2.CAP_PROP_FPS, 20)
        while True:
             ret, img = cap.read()
             cv2.imshow('Image', img)

    except:
        print("카메라 구동 실패")
        return


showVideo()