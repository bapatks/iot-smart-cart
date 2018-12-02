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
#    lcd = CharLCD(cols=16, rows=2, pin_rs=13, pin_e=15, pins_data=[29,23,21,19,11,37,5,3], numbering_mode=GPIO.BOARD)
    GPIO.setup(MODE, GPIO.IN)
    while settings.checkout == False:
        while GPIO.input(MODE) == 0:
            pass
        if settings.insertion == 1:
            settings.insertion = -1;
            #lcd.clear()
            #lcd.cursor_pos = (0,0)
            #lcd.display("Delete item")
            lcd.lcd_write("Delete item", 0, 0, 1)
            print("Switched to Delete Mode")
        else:
            settings.insertion = 1;
            print("Switched to Insert Mode")
            #lcd.clear()
            #lcd.cursor_pos = (0,0)
            lcd.lcd_write("Addd item", 1, 0, 0)
            #lcd.display("Add item")
        time.sleep(.05)

def check_checkout():
    #lcd = CharLCD(cols=16, rows=2, pin_rs=13, pin_e=15, pins_data=[29,23,21,19,11,37,5,3], numbering_mode=GPIO.BOARD)
    GPIO.setup(CHECKOUT, GPIO.IN)
    while GPIO.input(CHECKOUT) == 0:
        pass
    # lcd.lcd_clear_screen()
    # lcd.display('ARE YOU SURE ?')
    print("Something on checkout")
    # while GPIO.input(CHECKOUT) == 0:
    #     pass
    settings.checkout = True;
