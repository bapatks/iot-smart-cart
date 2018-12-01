import RPi.GPIO as GPIO
import time

MODE = 12 # board pin 12
CHECKOUT = 16 # board pin 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def check_mode():
    while True:
        while GPIO.input(MODE) == 0:
            pass
        if settings.insertion == 1:
            settings.insertion = -1;
        else:
            settings.insertion = 1;
        
def check_checkout():
    while GPIO.input(CHECKOUT) == 0:
        pass
    settings.checkout = True;