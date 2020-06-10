#from picamera import PiCamera
#from time import sleep
#import sys

#file_name=sys.argv[1]
#camera=PiCamera()
#camera.start_preview()
#sleep(2)
#camera.capture('/home/pi/shared/'+file_name)
#camera.stop_preview()


from picamera import PiCamera
from time import sleep
import sys
import serial 
import RPi.GPIO as GPIO
import time

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

file_name=sys.argv[1]
camera=PiCamera()

loop = True
counter = 0
previous_val = 0

while loop:
    
    read_ser = ser.readline()
    str_read = str(read_ser)
    print(str_read)
    if str_read:
        val = float(str_read.lstrip("b'").rstrip("'n\\r\\"))
        if abs(val-previous_val) < 5:
            counter += 1
        else:
            counter = 0

        previous_val = val
        if counter == 5:
            camera.start_preview()
            sleep(2)
            camera.capture('/home/pi/shared/'+file_name)
            camera.stop_preview()
            break

