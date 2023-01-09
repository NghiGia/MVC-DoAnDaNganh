import argparse
import os
import platform
import sys
from pathlib import Path
import time
import torch
import cv2
import pandas

model = torch.hub.load('ultralytics/yolov5', 'custom','E:/Study/Python_Yolo_Dataset/Đồ_Án_Đa_Ngành/yolov5-master/runs/train/exp4/weights/best.pt')  # or yolov5m, yolov5l, yolov5x, etc.
    # model = torch.hub.load('ultralytics/yolov5', 'custom', 'path/to/best.pt')  # custom trained model
#
def detect_lp(source_frame):
    result=model(source_frame)
    result.xyxy[0]  # im1 predictions (tensor)
    result.pandas().xyxy[0]  # im1 predictions (pandas)
    # print(result.pandas().xyxy[0] )
    crop_img=source_frame

    if not result.xyxy[0].size(dim=0) == 0:
        for box in result.xyxy[0]:
            if box[5] == 0 and box[4]>0.8:
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])
                crop_img = source_frame[yA:yB, xA:xB]
                cv2.rectangle(source_frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    return crop_img,source_frame

def detect_camera():
    vid = cv2.VideoCapture(0)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        crop_img, source_frame = detect_lp(frame)
        cv2.imshow('crop_img', crop_img)
        cv2.imshow('source_frame', source_frame)
        # cv2.imshow('frame', frame)
        cv2.waitKey(1)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
def detect_image():
    path = r'E:/Study/Python_Yolo_Dataset/Đồ_Án_Đa_Ngành/yolov5-master/datasets/new\images/Corn_Blight (463).JPG'
    frame=cv2.imread(path)
    crop_img, source_frame = detect_lp(frame)
    cv2.imshow('crop_img', crop_img)
    cv2.imshow('source_frame', source_frame)
    # cv2.imshow('frame', frame)
    cv2.waitKey()

def detect_video():
    cap = cv2.VideoCapture(r'E:/Study/Python_Yolo_Dataset/NumberPlate_Recognition_DataSet/yolov5-master/data/images/video.mp4')
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame', frame)
            crop_img, source_frame = detect_lp(frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
if __name__ == '__main__':
    detect_camera()