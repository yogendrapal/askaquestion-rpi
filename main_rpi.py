import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from config import *
import logger
import record
import random
import sync
import os
import time
from tkinter import *  
from PIL import ImageTk,Image  
import threading


root = None
canvas = None

class MyTkApp(threading.Thread):
    def __init__(self):
		self.root=Tk()
		self.height=240
		self.width=320
		self.canvas = Canvas(root, width = width, height = height)  
		self.canvas.pack() 
		img = Image.open("images/first.png")  # PIL solution
		img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img) 
		#img = ImageTk.PhotoImage(Image.open("Photo.jpg"))  
		self.canvas.create_image(0, 0, anchor="nw", image=img)
		threading.Thread.__init__(self)

	def Rec_start():
		img = Image.open("images/record3.png")  # PIL solution
		img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img) 
		#img = ImageTk.PhotoImage(Image.open("record3.png"))  
		self.canvas.create_image(0, 0, anchor="nw", image=img)
		self.root.update()

	def Rec_stop():
		img = Image.open("images/record1.png")  # PIL solution
		img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img) 
		#img = ImageTk.PhotoImage(Image.open("record1.png"))  
		self.canvas.create_image(0, 0, anchor="nw", image=img)
		self.root.update()

	def run(self):
		self.root.mainloop()

   

avr = record.AV_Recorder()
fname = ""


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(1)
app = MyTkApp()
app.start()
print('Program Started...')
while True: # Run forever
	if GPIO.input(12) == 0:
		print("Button on pin 12 was pushed!")
		if avr.is_recording():
			avr.stop()
			app.Rec_stop()
			logger.new_log_entry(fname,avr.ext)
			print('Video was saved as "'+fname + '.' + avr.ext +'"\n')
		else:
			fname = 'vid' + str(random.randint(100,1001))
			avr.record(OUTPUT_DIR+fname)
			app.Rec_start()
		time.sleep(3)

	if GPIO.input(16) == 0:
		print("Button on pin 16 was pushed!")
		avr.discard()
		time.sleep(3)

	if GPIO.input(18) == 0:
		print("Button on pin 18 was pushed!")
		sync.sync2server()
		time.sleep(3)

GPIO.cleanup()