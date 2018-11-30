import RPi.GPIO as GPIO
import time

DT = 10 # board pin 10
SCK = 8 # board pin 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def scale_init():
    GPIO.setup(SCK, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(DT, GPIO.IN)

def get_weight():
    for j in range(100):
        count = 0

    while GPIO.input(DT) == 1:  #while data is not ready
        i = 0

    for i in range(24):     # clock in the data
        GPIO.output(SCK,1)
        count = count << 1
        GPIO.output(SCK,0)
        time.sleep(0.001)
        if GPIO.input(DT):      #if the data is a 1
            count = count + 1   # add one to count

    GPIO.output(SCK,1)  #these two lines 
    GPIO.output(SCK,0)  #set DT back low

    weight = (103/50)*(round(count/10000, 3)-1641)
    #print(round(count/100))    # display final digital value
    print(round(weight,3))
    #print(count)

def get():
    old_weight = get_weight()
    while(abs(old_weight-get_weight()) < 0.75):
    new_weight = get_weight()
    return abs(new_weight-old_weight)


