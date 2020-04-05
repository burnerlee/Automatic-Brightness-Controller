import pyscreenshot as ImageGrab
import math
import os
import time
increment=3
screen = ImageGrab.grab()
SCREEN_SIZE=screen.size
MAX_X = SCREEN_SIZE[0]
MAX_Y = SCREEN_SIZE[1]
time_interval=1.0
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
    print sum_brightness
    average_brightness=sum_brightness/MAX_X/MAX_Y*increment*increment
    difference=255-average_brightness
    mean=difference/255
    brightness_set=0.3+mean
    print brightness_set
    stream = os.popen("xrandr -q | grep ' connected' | head -n 1 | cut -d ' ' -f1")
    DESKTOP_NAME = stream.readline()
    DESKTOP_NAME = DESKTOP_NAME.rstrip()
    brightness_set=0.3+mean
    command = "xrandr --output "+ DESKTOP_NAME +" --brightness "+str(brightness_set)
    os.system(command)
    time.sleep(time_interval)