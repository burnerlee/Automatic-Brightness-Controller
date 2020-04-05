import math
import os
import time
import signal
import sys
try:
    import pyscreenshot as ImageGrab
except:
    print "\nInstall Pyscreenshot from pip using `pip install pyscreenshot`\n"
    exit(0)
print "Welcome to Automatic Brightness Adjuster for you and your eyes"
print "Congrats You are on the right path to save your eyes from damage\n"
print "Usage:"
print "python main.py [pixel_gap] [time-interval]\n"
print "pixel-gap(positive integer value)-> spacing between pixels to calculate brightness of screen"
print "high pixel gap means low accuracy but low computational cost and vice-versa. Default value: 3 pixels\n"
print "time-interval(positive value > 1)-> time interval between adjusting your screen brightness. Recommended 1.0. Default: 1.0 sec\n"
arguments=sys.argv
try:
    if len(arguments)==2:
        if int(arguments[1])>=1:
            increment=int(arguments[1])
        else:
            print "Please enter a valid value for pixel-gap. Currently set to default"
            increment=3
        time_interval=1.0
    elif len(arguments)>2:
        if arguments[2]>1:
            time_interval=float(arguments[2])
        else:
            time_interval=1.0
            print "Please enter a valid value for time-interval . Currently set to default"
        if int(arguments[1])>1:
            increment=int(arguments[1])
        else:
            print "Please enter a valid value for pixel-gap. Currently set to default"
            increment=3
except:
    print "Please enter valid arguments"
    print "Exiting..."
    exit(0)
else:
    increment=3
    time_interval=1.0
print "Enjoy! Just leave it on us to save you\n"
print "Starting ..."
time.sleep(3)
SCREEN = ImageGrab.grab()
SCREEN_SIZE=SCREEN.size
MAX_X = SCREEN_SIZE[0]
MAX_Y = SCREEN_SIZE[1]
BRIGHTNESS_DEFAULT=1.0
brightness_set=BRIGHTNESS_DEFAULT
stream = os.popen("xrandr -q | grep ' connected' | head -n 1 | cut -d ' ' -f1")
DESKTOP_NAME = stream.readline()
DESKTOP_NAME = DESKTOP_NAME.rstrip() 
def exit_function():
    command = "xrandr --output "+ DESKTOP_NAME +" --brightness 1"
    os.system(command)
    print "\n\nBYE BYE!"
    print "Brightness set to normal!"   
def keyboardInterruptHandler(signal, frame):
    exit_function()
    exit(0)
signal.signal(signal.SIGINT, keyboardInterruptHandler)
while 1:
    sum_brightness=0
    current_screen = ImageGrab.grab()
    for x in range (0,MAX_X,increment):
        for y in range (0,MAX_Y,increment):
            cordinate=x,y
            rgb = (current_screen.getpixel(cordinate))
            R=rgb[0]
            G=rgb[1]
            B=rgb[2]
            brightness=math.sqrt(0.299*R*R + 0.587*G*G + 0.114*B*B )
            sum_brightness+=brightness
    average_brightness=sum_brightness/MAX_X/MAX_Y*increment*increment
    difference=255-average_brightness
    mean=difference/255
    if((mean+0.3)>(brightness_set+0.1) or (mean+0.3)<(brightness_set-0.1)):
        brightness_set=0.3+mean
        print "Brightness set to " + str(brightness_set)
        command = "xrandr --output "+ DESKTOP_NAME +" --brightness "+str(brightness_set)
        os.system(command)
    else:
        print "Brightness same"
    time.sleep(float(time_interval))
