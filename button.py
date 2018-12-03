import RPi.GPIO as GPIO
import time
import settings
#from RPLCD.gpio import CharLCD
import lcd

MODE = 12 # board pin 12
CHECKOUT = 16 # board pin 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def check_mode():
    GPIO.setup(MODE, GPIO.IN)
    while settings.checkout == False:
        while GPIO.input(MODE) == 0:
            pass
        if settings.insertion == 1:
            settings.insertion = -1;
            lcd.lcd_write("Delete item", 0, 0, 1)
            print("Switched to Delete Mode")
        else:
            settings.insertion = 1;
            print("Switched to Insert Mode")
            lcd.lcd_write("Add item", 1, 0, 1)
        time.sleep(.05)

def check_checkout():
    GPIO.setup(CHECKOUT, GPIO.IN)
    while GPIO.input(CHECKOUT) == 0:
        pass
    # lcd.lcd_clear_screen()
    # lcd.display('ARE YOU SURE ?')
    print("Something on checkout")
    # while GPIO.input(CHECKOUT) == 0:
    #     pass
    settings.checkout = True;
