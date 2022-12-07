from Controller import *
from PyQt5.QtWidgets import (
    QApplication
)
from View import MainWindow
import sys
from Adafruit_IO import MQTTClient
AIO_FEED_ID = ["temperature","moisture","relay1","relay2"]
AIO_USERNAME = "DaveFrostSnow"
AIO_KEY = "aio_BWXP93SfRb9MK7l1TWNKM8Thj8Fs"

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
        window.box5.setText("On")
    if feed_id=="relay1" and payload=="0":
        window.box5.setText("Off")
    if feed_id=="relay2" and payload=="1":
        window.box6.setText("On")
    if feed_id=="relay2" and payload=="0":
        window.box6.setText("Off")
    if feed_id == "temperature" :
        window.hourbox7.append(window.hourbox7[-1] + 1)
        window.temperature.append(int(float(payload)))  # Add a new random value.
        window.data_line_box7.setData(window.hourbox7, window.temperature)
    if feed_id == "moisture" :
        window.hourbox8.append(window.hourbox7[-1] + 1)
        window.moisture.append(int(float(payload)))  # Add a new random value.
        window.data_line_box8.setData(window.hourbox8, window.moisture)


def connect_adafruit():
    clients = MQTTClient(AIO_USERNAME , AIO_KEY)
    return clients

clients=connect_adafruit()


clients.on_connect = connected
clients.on_message = message
clients.connect()
clients.loop_background()

app = QApplication(sys.argv)
window = MainWindow(clients)
window.show()
app.exec()