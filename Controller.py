
def box5_button_clicked(box5,clients):
        print("Clicked")
        if box5.text() == "On":
            box5.setText("Off")
            clients.publish("relay1", "0")
        else:
            box5.setText("On")
            clients.publish("relay1", "1")

def box6_button_clicked(box6,clients):
        print("Clicked")
        if box6.text() == "On":
            box6.setText("Off")
            clients.publish("relay2", "0")
        else:
            box6.setText("On")
            clients.publish("relay2", "1")

def box3_update_calendar(box3):
        value = box3.date()
        print(value.toPyDate())

def box4_update_calendar(box4):
        value = box4.date()
        print(value.toPyDate())

def display(self, date):
        print(date.date().toPyDate())

def box1_show_state(box1):
        if box1.isChecked()==True:
            print("Check Box:Selected")
        if box1.isChecked() == False:
            print("Check Box:Deselected")

def box2_value_changed(box2,box2_display_data):
        box2_display_data.setText("Threshold:" + str(box2.value()))
        print(box2.value())

def box2_slider_position(self, p):
        print("position", p)

def box2_slider_pressed(self):
        print("Pressed!")

def box2_slider_released(self):
        print("Released")