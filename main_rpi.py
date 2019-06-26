
from config import *
if RPI:
	import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
else:
	import keyboard
import logger
import record
import random
import sync
import os
import time
from tkinter import *  
from PIL import ImageTk,Image  
from threading import Thread


stop_thread = False
height=240
width=320
root = None
canvas = None
if RPI:
	GPIO.setwarnings(False) # Ignore warning for now
	GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
	GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
	GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
else:
	class emugpio():
		def __init__(self):
			pass
		def input(self,pin):
			if pin==18 and keyboard.is_pressed('1'):
				return False
			elif pin == 16 and keyboard.is_pressed('2'):
				return False
			elif pin == 12 and keyboard.is_pressed('3'):
				return False
			else:
				return True
	GPIO = emugpio()

class check_buttons(Thread):

	def __init__(self,canvas):
		global height
		global width
		Thread.__init__(self)
		self.height=height
		self.width=width
		self.canvas = canvas
		img = Image.open("images/first.png")  # PIL solution
		img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img)
		self.img_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=img)

		self.avr = record.AV_Recorder()
		self.fname = ""
		time.sleep(1)

	def get_img(self,img_path):
		img = Image.open(img_path)  # PIL solution
		img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img)
		return img

	def checkloop(self):
		global root
		while not stop_thread:
			if GPIO.input(18) == 0:
				print("Button on pin 18 was pushed!")
				if self.avr.is_recording():
					self.avr.stop()
					img = self.get_img("images/record1.png")
					self.canvas.itemconfig(self.img_on_canvas,image=img)
					# self.set_image("images/record1.png")
					logger.new_log_entry(self.fname,self.avr.ext)
					print('Video was saved as "'+self.fname + '.' + self.avr.ext +'"\n')
					time.sleep(3)
					img = self.get_img("images/first.png")
					self.canvas.itemconfig(self.img_on_canvas,image=img)
				else:
					self.fname = 'vid' + str(random.randint(100,1001))
					self.avr.record(OUTPUT_DIR+self.fname)
					img = self.get_img("images/record3.png")
					self.canvas.itemconfig(self.img_on_canvas,image=img)
					time.sleep(3)

			if GPIO.input(16) == 0:
				print("Button on pin 16 was pushed!")
				self.avr.discard()
				time.sleep(3)

			if GPIO.input(12) == 0:
				print("Button on pin 12 was pushed!")
				sync.sync2server()
				time.sleep(3)

def updater():
	global root
	root.update()
	root.after(10,updater)

print('Program Started...')
root = Tk()

#set first image 
canvas = Canvas(root, width = width, height = height)  
canvas.pack() 
img = Image.open("images/first.png")  # PIL solution
img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
img = ImageTk.PhotoImage(img) 
canvas.create_image(0, 0, anchor="nw", image=img) 

chk = check_buttons(canvas)
t1 = Thread(target=chk.checkloop)
t1.start()


updater()
root.mainloop()
stop_thread = True
if RPI:
	GPIO.cleanup()
