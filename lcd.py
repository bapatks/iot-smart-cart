import RPi.GPIO as GPIO
import time

DB4 = 11 # board pin 3
DB5 = 37 # board pin 5
DB6 = 5 # board pin 7
DB7 = 3 # board pin 11
RS = 13 # board pin 13
E = 15 # board pin 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def lcd_command(cmd):
    GPIO.output(RS,0) # set register select to 0

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,1) # set enable to 1

    GPIO.output(DB7, (cmd>>7) & 1 ) # These four lines
    GPIO.output(DB6, (cmd>>6) & 1 ) # put the upper nibble of
    GPIO.output(DB5, (cmd>>5) & 1 ) # cmd on the data bus
    GPIO.output(DB4, (cmd>>4) & 1 ) #

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,0) # set enable to 0, latch the data

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,1) # set enable to 1

    GPIO.output(DB7, (cmd>>3) & 1 ) # These four lines
    GPIO.output(DB6, (cmd>>2) & 1 ) # put the lower nibble of
    GPIO.output(DB5, (cmd>>1) & 1 ) # cmd on the data bus
    GPIO.output(DB4, (cmd>>0) & 1 ) #

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,0) # set enable to 0, latch the data

    time.sleep(.007) # sleep for 7 ms

def lcd_clear_screen():  # clears the lcd_screen
    lcd_command(1)

def lcd_place_cursor(address):   #input address as an integer
    lcd_command(128 | address)  # places cursor at desired address

# Locations on the 16x2 LCD and their addresses in hex
#_____________________________________________
#|      |      |      |                |      |
#| 0x00 | 0x01 | 0x02 |................| 0x0F |
#|______|______|______|________________|______|
#|      |      |      |                |      |
#| 0x40 | 0x41 | 0x42 |................| 0x4F |
#|______|______|______|________________|______|
#
# 0x40 = 64 decimal
# 0x4F = 79 decimal

def lcd_init():
    GPIO.setup(DB4, GPIO.OUT)   #set up GPIO pins
    GPIO.setup(DB5, GPIO.OUT)
    GPIO.setup(DB6, GPIO.OUT)
    GPIO.setup(DB7, GPIO.OUT)
    GPIO.setup(RS, GPIO.OUT)
    GPIO.setup(E, GPIO.OUT)

    lcd_command(51) # initialize LCD driver
    lcd_command(50) # four bit mode
    lcd_command(44) # 2 line mode
    lcd_command(15) # display on, cursor on, blink on. lcd_command(12) for no cursor
    lcd_command(1) # clear screen, cursor home
    lcd_command(6) # increment cursor to the right and don't shift screen

def lcd_char(singleChar):   # an example call would be lcd_char('h')
    singleChar = ord(singleChar)

    GPIO.output(RS,1) # set register select to 1
    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,1) # set enable to 1

    GPIO.output(DB7, (singleChar>>7) & 1 ) # These four lines
    GPIO.output(DB6, (singleChar>>6) & 1 ) # put the upper nibble of
    GPIO.output(DB5, (singleChar>>5) & 1 ) # singleChar on the data bus
    GPIO.output(DB4, (singleChar>>4) & 1 ) #

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,0) # set enable to 0, latch the data

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,1) # set enable to 1

    GPIO.output(DB7, (singleChar>>3) & 1 ) # These four lines
    GPIO.output(DB6, (singleChar>>2) & 1 ) # put the lower nibble of
    GPIO.output(DB5, (singleChar>>1) & 1 ) # singleChar on the data bus
    GPIO.output(DB4, (singleChar>>0) & 1 ) #

    time.sleep(.005) # sleep for 5ms

    GPIO.output(E,0) # set enable to 0, latch the data

    time.sleep(.007) # sleep for 7 ms

def lcd_string(string): # an example call would be lcd_string('hello')
                        # be mindfull of the amount of space left on the
                        # lcd screen's line and where the cursor is.
    for i in range(0, len(string)):
        lcd_char(string[i])
        #time.sleep(0.1)

def display(string):
    lcd_clear_screen()
    if(len(string)>16):
        str1 = string[:16]
        str2 = string[16:]
        lcd_string(str1)
        lcd_place_cursor(64) # place cursor at second line
        lcd_string(str2)
    else:
        lcd_string(string)
#example call: write("hi", 0, 0, 1) # write "hi" to first cell of first line
#               yes to clear screen
def lcd_write(string, row, col, clear):
    if clear == 1:
        lcd_clear_screen()
    if row == 0:
        lcd_place_cursor(col)
    elif row == 1:
        lcd_place_cursor(col + 64)
    lcd_string(string)


# example code
# lcd_init()
# lcd_string('Smart Cart is')
# lcd_place_cursor(64) # place cursor at second line
# lcd_string('the greatest!')
#lcd_init()
#write("hello", 0, 0, 0)
#time.sleep(2)
#write("hi", 1, 0, 1)
