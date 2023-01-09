from Controller import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication
)
from View import MainWindow
import sys
from Adafruit_IO import MQTTClient
import cv2,imutils
AIO_FEED_ID = ["temperature","moisture","relay1","relay2","threshold","ai image"]
AIO_USERNAME = "DaveFrostSnow"
AIO_KEY = "aio_VPKh87xX65zA0KsQ0C1a6zCCiv3Z"
import cv2
import torch



def detect_corn(source_frame):
    result=model(source_frame)
    result.xyxy[0]  # im1 predictions (tensor)
    result.pandas().xyxy[0]  # im1 predictions (pandas)
    crop_img=source_frame
    if not result.xyxy[0].size(dim=0) == 0:
        for box in result.xyxy[0]:
            if box[5] == 0 and box[4]>0.3:
                print("detected")
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])
                crop_img = source_frame[yA:yB, xA:xB]
                cv2.rectangle(source_frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                window.Scrn1.thread_box11.change_pixmap_signal.emit(source_frame)
                return 1
    return 0

def connected ( client ) :
    print ("Ket noi thanh cong ...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)
        print(feed)

def subscribe ( client , userdata , mid , granted_qos ) :
    print ("Subcribe thanh cong ...")

def disconnected ( client ) :
    print (" Ngat ket noi ...")
    sys . exit (1)

def message ( client , feed_id , payload ):
    print ("Nhan du lieu : " + payload +" from feed "+ feed_id)
    if feed_id=="relay1" and payload=="1":
        window.Scrn1.box5.setText("On")
    if feed_id=="relay1" and payload=="0":
        window.Scrn1.box5.setText("Off")
    if feed_id=="relay2" and payload=="1":
        window.Scrn1.box6.setText("On")
    if feed_id=="relay2" and payload=="0":
        window.Scrn1.box6.setText("Off")
    if feed_id == "temperature" :
        window.Scrn1.hourbox7.append(window.Scrn1.hourbox7[-1] + 1)
        window.Scrn1.temperature.append(int(float(payload)))  # Add a new random value.
        window.Scrn1.data_line_box7.setData(window.Scrn1.hourbox7, window.Scrn1.temperature)
        window.Scrn1.box9.setText("Temp: "+payload)
    if feed_id == "moisture" :
        window.Scrn1.hourbox8.append(window.Scrn1.hourbox7[-1] + 1)
        window.Scrn1.moisture.append(int(float(payload)))  # Add a new random value.
        window.Scrn1.data_line_box8.setData(window.Scrn1.hourbox8, window.Scrn1.moisture)
        window.Scrn1.box10.setText("Moisture: " + payload)


def connect_adafruit():
    clients = MQTTClient(AIO_USERNAME , AIO_KEY)
    return clients

def detect_camera(clients):
    vid = cv2.VideoCapture(0)
    AI_check=0
    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        window.Scrn1.thread_box12.change_pixmap_signal.emit(frame)
        var_detect=detect_corn(frame)
        if(var_detect==1):
            AI_check=1
        if (var_detect==0 and AI_check==1):
            AI_check=0
            AI(clients)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

model = torch.hub.load('ultralytics/yolov5', 'custom','E:/Study/Python_Yolo_Dataset/Đồ_Án_Đa_Ngành/yolov5-master/runs/train/exp4/weights/best.pt')
clients=connect_adafruit()


clients.on_connect = connected
clients.on_message = message
clients.connect()
clients.loop_background()



app = QApplication(sys.argv)
window = MainWindow(clients)
window.show()
detect_camera(clients)
app.exec()

