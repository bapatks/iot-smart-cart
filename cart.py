#!/usr/bin/env python
import gcloud
import argparse
import os
import time
import settings
import weight, button, firebase, reader
from threading import Thread

import lcd

def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
            'Example Google Cloud IoT Core MQTT device connection code.'))
    parser.add_argument(
            '--project_id',
            default=os.environ.get('GOOGLE_CLOUD_PROJECT'),
            help='GCP cloud project name')
    parser.add_argument(
            '--registry_id', required=True, help='Cloud IoT Core registry id')
    parser.add_argument(
            '--device_id', required=True, help='Cloud IoT Core device id')
    parser.add_argument(
            '--private_key_file',
            required=True, help='Path to private key file.')
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            required=True,
            help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--num_messages',
            type=int,
            default=100,
            help='Number of messages to publish.')
    parser.add_argument(
            '--message_type',
            choices=('event', 'state'),
            default='event',
            help=('Indicates whether the message to be published is a '
                  'telemetry event or a device state message.'))
    parser.add_argument(
            '--mqtt_bridge_hostname',
            default='mqtt.googleapis.com',
            help='MQTT bridge hostname.')
    parser.add_argument(
            '--mqtt_bridge_port',
            choices=(8883, 443),
            default=8883,
            type=int,
            help='MQTT bridge port.')
    parser.add_argument(
            '--jwt_expires_minutes',
            default=20,
            type=int,
            help=('Expiration time, in minutes, for JWT tokens.'))

    return parser.parse_args()
    
if __name__ == '__main__':
    args = parse_command_line_args()
    settings.init()
    lcd.lcd_init()
    #lcd = CharLCD(cols=16, rows=2, pin_rs=13, pin_e=15, pins_data=[29,23,21,19,11,37,5,3], numbering_mode=GPIO.BOARD)
    weight.scale_init()
    client = gcloud.setup_client(args)
    #count = 0
    #print(str(weight.get()))
    while True:
        client.loop(1)

        if settings.recvID == settings.cartID:
            print("Cart ID matched to that from cloud")
            lcd.lcd_write("Hello "+str(settings.username), 0, 0, 0)
            #lcd.display("Hello "+str(settings.username))
            time.sleep(5)
            ModeThread = Thread(target=button.check_mode)
            ModeThread.start()
            checkoutThread = Thread(target=button.check_checkout)
            checkoutThread.start()
            break;
        time.sleep(.1)

    while True:
        lcd.lcd_write("Scan an item", 0, 2, 1)
        
        #barcode.barcode_reader must wait until barcode a barcode is read
        barcode = reader.barcode_get()

        ItemName = firebase.item_get_name(barcode)
        if(ItemName == "-1"):
            continue
        
        lcd.lcd_write(ItemName,0,0,1)
        time.sleep(3)
        
        lcd.lcd_write("Place an item", 0, 0, 1)
        lcd.lcd_write("in cart", 1, 0, 0)
        
        #weight.get must wait until weight has changed
        check_weight = weight.get()
        
        lcd.lcd_write("added weight = ", 0, 0, 1)
        
        lcd.lcd_write(str(check_weight), 1, 0, 0)
        time.sleep(1)

        actual_weight = firebase.item_get_wt(barcode)
        if(actual_weight == -1):
            continue
        
        if(abs(actual_weight - check_weight) < 0.5):
            print("Preparing to publish")
            # display details of barcode
            client.loop(1)
            payload = '{}:{}'.format(barcode, settings.insertion)
            gcloud.publish(args, client, payload)
        else:
            lcd.lcd_write("call the manager",0,0,1)
            print("Must not publish")
            while True:
                time.sleep(1)
                lcd.lcd_write("call the manager",0,0,1)

    while(settings.checkout == False):
    	pass
    checkoutThread.join()
    ModeThread.join()
##    client.disconnect()
    print("Finished app")
    
