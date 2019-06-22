import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from config import *
import logger
import record
import random
import sync
import os

avr = record.AV_Recorder()
fname = ""

def button1(channel):
	global avr
	global fname
	print("Button on pin 12 was pushed!")
	if avr.is_recording():
		avr.stop()
		logger.new_log_entry(fname,avr.ext)
		print('Video was saved as "'+fname + '.' + avr.ext +'"\n')
	else:
		fname = 'vid' + str(random.randint(100,1001))
		avr.record(OUTPUT_DIR+fname)

def button2(channel):
	global avr
	print("Button on pin 16 was pushed!")
	avr.discard()

def button3(channel):
	global avr
	print("Button on pin 18 was pushed!")
	sync.sync2server()



GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(12,GPIO.FALLING,callback=button1) # Setup event on pin 10 rising edge
GPIO.add_event_detect(16,GPIO.FALLING,callback=button2)
GPIO.add_event_detect(18,GPIO.FALLING,callback=button3)

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up

# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# while True: # Run forever
#     if GPIO.input(12) == GPIO.HIGH:
#         print("Button was pushed!")