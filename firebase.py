import firebase_admin, time
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/Documents/cart/smartcart-365b7-firebase-adminsdk-z3den-79f18008bd.json')
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://smartcart-365b7.firebaseio.com/Items'})
result=db.reference('/Items')

def item_get_wt(barcode):
    item_list = result.get()
    if barcode in item_list:
        return item_list[barcode]['Weight']
    else:
        time.sleep(1)
        lcd.lcd_write("Item not found", 0 ,0, 1)
        return -1
    
def item_get_name(barcode):
    item_list = result.get()
    if barcode in item_list:
        return item_list[barcode]['ItemName']
    else:
        time.sleep(1)
        lcd.lcd_write("Item not found", 0 ,0, 1)
        return "-1"

