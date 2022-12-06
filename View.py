
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
from PyQt5.QtWidgets import (
    QGridLayout,
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QFormLayout
)
import time
import sys
from Adafruit_IO import MQTTClient
AIO_FEED_ID = ["temperature","moisture","relay1","relay2"]
AIO_USERNAME = "DaveFrostSnow"
AIO_KEY = "aio_BWXP93SfRb9MK7l1TWNKM8Thj8Fs"

def connected ( client ) :
    print ("Ket noi thanh cong ...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

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
        # print(payload)
        window.box7_update_plot_data(int(float(payload)))
    if feed_id == "moisture":
        # print(payload)
        window.box8_update_plot_data(int(float(payload)))





clients = MQTTClient(AIO_USERNAME , AIO_KEY)
clients.on_connect = connected
clients.on_message = message
clients.connect()
clients.loop_background()

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QGridLayout()

        # Check Box
        self.box1 = QCheckBox("Check Box")
        self.box1.setCheckState(Qt.Checked)
        self.box1.stateChanged.connect(self.box1_show_state)
        layout.addWidget(self.box1,0,1)
        # ===============================================

        # Dial
        self.box2 = QDial()
        self.box2.setRange(0, 50)
        self.box2.setSingleStep(1)
        self.box2_display_data=QLabel("Threshold:")
        self.box2_value=0
        self.box2.valueChanged.connect(self.box2_value_changed)
        self.box2.sliderMoved.connect(self.box2_slider_position)
        self.box2.sliderPressed.connect(self.box2_slider_pressed)
        self.box2.sliderReleased.connect(self.box2_slider_released)
        self.dialbox2value=0
        self.box2_display_data.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.box2,1,0)
        layout.addWidget(self.box2_display_data,1,1)
        # ===============================================

        # Date
        self.box3 = QDateEdit()
        self.box3.editingFinished.connect(self.box3_update_calendar)

        self.box4 = QDateEdit()
        self.box4.editingFinished.connect(self.box4_update_calendar)
        self.titlebox3=QLabel("Start Date: ")
        self.titlebox4=QLabel("End Date: ")
        self.titlebox3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.titlebox4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.titlebox3,3,0)
        layout.addWidget(self.box3,3,1)
        layout.addWidget(self.titlebox4, 4, 0)
        layout.addWidget(self.box4,4,1)
        # ================================================

        # Button
        self.box5 = QPushButton("On")
        clients.publish("relay1", "1")
        self.box5.setCheckable(True)
        self.box5.clicked.connect(self.box5_button_clicked)

        self.box6=QPushButton("On")
        clients.publish("relay2", "1")
        self.box6.setCheckable(True)
        self.box6.clicked.connect(self.box6_button_clicked)

        self.titlebox5 = QLabel("Relay1: ")
        self.titlebox6 = QLabel("Relay2: ")
        self.titlebox5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.titlebox6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.titlebox5, 5, 0)
        layout.addWidget(self.box5, 5, 1)
        layout.addWidget(self.titlebox6, 6, 0)
        layout.addWidget(self.box6, 6, 1)

        # ================================================

        # Line
        self.box7=pg.PlotWidget()
        self.box7.setXRange(0,20,padding=0)
        self.box7.setYRange(0, 60, padding=0)
        self.box7.setBackground('w')
        pen = pg.mkPen(color=(0, 0, 255))
        self.hourbox7 = [0,0]
        self.temperature = [0,0]
        styles = {'color': 'r', 'font-size': '20px'}
        self.box7.setTitle("Temperature", color="b", size="30pt")
        self.box7.setLabel('left', 'Temperature (°C)', **styles)
        self.box7.setLabel('bottom', 'Hour (H)', **styles)
        self.box7.showGrid(x=True, y=True)
        self.data_line_box7=self.box7.plot(self.hourbox7,self.temperature,pen=pen)


        self.box8 = pg.PlotWidget()
        self.box8.setXRange(0, 20, padding=0)
        self.box8.setYRange(0, 60, padding=0)
        self.box8.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.hourbox8 = [0, 0]
        self.moisture = [0, 0]
        styles = {'color': 'r', 'font-size': '20px'}
        self.box8.setTitle("Moisture", color="r", size="30pt")
        self.box8.setLabel('left', 'Moisture (%)', **styles)
        self.box8.setLabel('bottom', 'Hour (H)', **styles)
        self.box8.showGrid(x=True, y=True)
        self.data_line_box8 = self.box8.plot(self.hourbox8, self.moisture, pen=pen)

        layout.addWidget(self.box7, 7, 1)
        layout.addWidget(self.box8, 8,1)
        # ===================================

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def box7_update_plot_data(self, new_data):
        # self.hourbox7 = self.hourbox7[1:]  # Remove the first y element.
        # self.temperature = self.temperature[1:]  # Remove the first

        self.hourbox7.append(self.hourbox7[-1] + 1)  # Add a new value 1 higher than the last.
        self.temperature.append(new_data)  # Add a new random value.
        # print(self.box2_value-new_data)
        self.data_line_box7.setData(self.hourbox7, self.temperature)

    def box8_update_plot_data(self, new_data):
        # self.hour = self.hour[1:]  # Remove the first y element.
        self.hourbox8.append(self.hourbox8[-1] + 1)  # Add a new value 1 higher than the last.

        # self.temperature = self.temperature[1:]  # Remove the first
        self.moisture.append(new_data)  # Add a new random value.

        self.data_line_box8.setData(self.hourbox8, self.moisture)

    def box5_button_clicked(self):
        print("Clicked")
        if self.box5.text() == "On":
            self.box5.setText("Off")
            clients.publish("relay1", "0")
        else:
            self.box5.setText("On")
            clients.publish("relay1", "1")

    def box6_button_clicked(self):
        print("Clicked")
        if self.box6.text() == "On":
            self.box6.setText("Off")
            clients.publish("relay2", "0")
        else:
            self.box6.setText("On")
            clients.publish("relay2", "1")

    def box3_update_calendar(self):
        value = self.box3.date()
        print(value.toPyDate())

    def box4_update_calendar(self):
        value = self.box3.date()
        print(value.toPyDate())

    def display(self, date):
        print(date.date().toPyDate())

    def box1_show_state(self, s):
        print(s == Qt.Checked)
        print(s)

    def box2_value_changed(self, i):
        self.box2_value = i
        self.box2_display_data.setText("Threshold:" + str(i))
        print(self.box2_value)

    def box2_slider_position(self, p):
        print("position", p)

    def box2_slider_pressed(self):
        print("Pressed!")

    def box2_slider_released(self):
        print("Released")



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



