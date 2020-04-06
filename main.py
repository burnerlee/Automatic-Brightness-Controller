import math
import os
import time
import signal
import sys
import threading

try:
    from PyQt4 import QtGui
except ImportError:
    print "\nInstall PyQt4 using sudo apt install python-qt4\n"
    exit(0)

try:
    import pyscreenshot as ImageGrab
except ImportError:
    print "\nInstall Pyscreenshot from pip using `pip install pyscreenshot`\n"
    exit(0)

from PyQt4.QtGui import QSlider, QMessageBox
from PyQt4.QtCore import Qt
# Print instruction messages to guide the user in the beginning

print "Welcome to Automatic Brightness Adjuster for you and your eyes"
print "Congrats You are on the right path to save your eyes from damage\n"
print "Usage:"
print "Pixel-gap-> Spacing between pixels to calculate brightness of screen"
print "High pixel gap means low accuracy but low computational",
print "cost and vice-versa.\n"
print "Time-interval-> Time interval between adjusting your",
print "screen brightness.\n"
print "Sensitivity-> Set sensitivity of change in pixels for which",
print "brightness changes"
print "Low sensitivity would change brightness on larger change in ",
print "screen colour and vice versa \n"

arguments = sys.argv
stopped = False
increment = 3
time_interval = 1.0
sensitivity = 1

print "Enjoy! Just leave it on us to save you\n"
print "Starting ..."


# Defining the GUI part of the Application
class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.setGeometry(50, 50, 600, 300)
        self.setWindowTitle("Automatic Brightness Controller")
        self.setWindowIcon(QtGui.QIcon("logo.jpeg"))

        # Configure the Apply Changes button
        btn = QtGui.QPushButton("Apply Changes", self)
        btn.move(220, 240)
        btn.resize(160, 30)
        btn.clicked.connect(self.apply)

        # Defining the window labels
        l1 = QtGui.QLabel(self)
        l1.setText("You can Change the Settings and click on Apply Changes")
        l1.setGeometry(100, 10, 400, 50)
        l1.setAlignment(Qt.AlignCenter)

        l2 = QtGui.QLabel(self)
        l2.setText("Pixel Gap:")
        l2.setGeometry(20, 75, 150, 30)
        l2.setAlignment(Qt.AlignLeft)

        l3 = QtGui.QLabel(self)
        l3.setText("Time Interval:")
        l3.setGeometry(20, 120, 150, 30)
        l3.setAlignment(Qt.AlignLeft)

        l4 = QtGui.QLabel(self)
        l4.setText("Change Sensitivity:")
        l4.setGeometry(20, 165, 150, 30)
        l4.setAlignment(Qt.AlignLeft)

        l5 = QtGui.QLabel(self)
        text = "Note: Closing this will close the application,"
        text = text + "Rather minimize"
        l5.setText(text)
        l5.setGeometry(10, 210, 580, 20)
        l5.setAlignment(Qt.AlignCenter)

        global s1, s2, s3

        # Defining the three sliders which take input from the user
        s1 = QSlider(Qt.Horizontal, self)
        s1.setMinimum(3)
        s1.setMaximum(20)
        s1.setValue(3)
        s1.setSingleStep(1)
        s1.setTickPosition(QSlider.TicksBelow)
        s1.setTickInterval(1)
        s1.move(200, 80)
        s1.resize(300, 30)

        s2 = QSlider(Qt.Horizontal, self)
        s2.setMinimum(1)
        s2.setMaximum(20)
        s2.setValue(1)
        s2.move(200, 125)
        s2.resize(300, 30)
        s2.setSingleStep(1)
        s2.setTickPosition(QSlider.TicksBelow)
        s2.setTickInterval(1)

        s3 = QSlider(Qt.Horizontal, self)
        s3.setMinimum(1)
        s3.setMaximum(100)
        s3.setValue(1)
        s3.move(200, 170)
        s3.resize(300, 30)
        s3.setSingleStep(1)
        s3.setTickPosition(QSlider.TicksBelow)
        s3.setTickInterval(5)

        self.show()

    # apply is execute when user clicks the Apply Changes button
    def apply(self):
        print "Changes Applied"

        # Change the values for adjusting brightness as entered by the user
        global increment, time_interval, sensitivity
        increment = s1.value()
        time_interval = s2.value()
        sensitivity = s3.value()

        # Add the alert to confirm that changes are made
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Changes Applied")
        msg.setWindowTitle("Alert")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # closeEvent is defined to stop the application when window is closed
    def closeEvent(self, *args, **kwargs):
        super(QtGui.QMainWindow, self).closeEvent(*args, **kwargs)
        global stopped
        stopped = True


# Define the GUI
app = QtGui.QApplication(sys.argv)
GUI = Window()

# Define initial screen variables and other constants
SCREEN = ImageGrab.grab()
SCREEN_SIZE = SCREEN.size
MAX_X = SCREEN_SIZE[0]
MAX_Y = SCREEN_SIZE[1]
BRIGHTNESS_DEFAULT = 1.0
stream = os.popen("xrandr -q | grep ' connected' | head -n 1 | cut -d ' ' -f1")
DESKTOP_NAME = stream.readline()
DESKTOP_NAME = DESKTOP_NAME.rstrip()


# exit_function is called when program exits
def exit_function():
    command = "xrandr --output " + DESKTOP_NAME + " --brightness 1"
    os.system(command)
    print "\n\nBYE BYE!"
    print "Brightness set to normal!"


# define a function if program is interrupted
def keyboardInterruptHandler(signal, frame):
    exit_function()


signal.signal(signal.SIGINT, keyboardInterruptHandler)


# adjust_brightness calculate the current state of the screen
# and adjusts brightness accordingly
def adjust_brightness(brightness_set):
    time.sleep(5)
    while 1:
        global stopped, increment, sensitivity, time_interval

        if stopped:
            break

        sum_brightness = 0
        current_screen = ImageGrab.grab()

        for x in range(0, MAX_X, increment):
            for y in range(0, MAX_Y, increment):
                cordinate = x, y
                rgb = (current_screen.getpixel(cordinate))
                R = rgb[0]
                G = rgb[1]
                B = rgb[2]
                brightness = math.sqrt(0.299*R*R + 0.587*G*G + 0.114*B*B)
                # formula to derive brightness of a pixel from RGB
                sum_brightness += brightness

        average_brightness = sum_brightness/MAX_X/MAX_Y*increment*increment
        # average value of brightness
        difference = 255-average_brightness
        mean = difference/255
        sensitivity_diff = 100 - sensitivity
        sensitivity_mean = float(sensitivity_diff)/1000
        cond1 = float(mean + 0.3) > float(brightness_set + sensitivity_mean)
        cond2 = float(mean + 0.3) < float(brightness_set - sensitivity_mean)
        if(cond1 or cond2):
            brightness_set = 0.3 + mean
            print "Brightness set to " + str(brightness_set)
            command = "xrandr --output " + DESKTOP_NAME
            command += " --brightness " + str(brightness_set)
            os.system(command)
        else:
            print "Brightness is same"
        time.sleep(float(time_interval))

    exit_function()
# The adjust_brightness function is called on the thread t1


t1 = threading.Thread(target=adjust_brightness, args=(BRIGHTNESS_DEFAULT,))
t1.start()

# GUI is executed and the adjust_brightness function runs on the thread t1
app.exec_()
