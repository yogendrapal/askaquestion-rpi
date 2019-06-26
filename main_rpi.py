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
from threading import Thread

height=240
width=320
root = None
canvas = None
avr = record.AV_Recorder()
fname = ""
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# def rec_start():
# 	global height
# 	global width
# 	global root
# 	global canvas 
# 	img = Image.open("images/record3.png")  # PIL solution
# 	img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
# 	img = ImageTk.PhotoImage(img) 
# 	#img = ImageTk.PhotoImage(Image.open("record3.png"))  
# 	canvas.create_image(0, 0, anchor="nw", image=img) 
# 	root.update()

# def rec_stop():
# 	global height
# 	global width
# 	global root
# 	global canvas  
# 	img = Image.open("images/record1.png")  # PIL solution
# 	img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
# 	img = ImageTk.PhotoImage(img) 
# 	#img = ImageTk.PhotoImage(Image.open("record1.png"))  
# 	canvas.create_image(0, 0, anchor="nw", image=img)  
# 	root.update()

class check_buttons(Thread):

	def __init__(self,canvas):
		Thread.__init__(self)
		self.height=240
		self.width=320
		self.canvas = canvas
		img = Image.open("images/first.png")  # PIL solution
		img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img)
		self.img_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=img)

		self.avr = record.AV_Recorder()
		self.fname = ""
		time.sleep(1)

	def checkloop(self):
		while True:
			if GPIO.input(18) == 0:
				print("Button on pin 18 was pushed!")
				if self.avr.is_recording():
					self.avr.stop()
					img = Image.open("images/record1.png")  # PIL solution
					img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
					img = ImageTk.PhotoImage(img)
					self.canvas.itemconfig(self.img_on_canvas,image=img)
					logger.new_log_entry(self.fname,self.avr.ext)
					print('Video was saved as "'+self.fname + '.' + self.avr.ext +'"\n')
				else:
					self.fname = 'vid' + str(random.randint(100,1001))
					self.avr.record(OUTPUT_DIR+fname)
					img = Image.open("images/record3.png")  # PIL solution
					img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
					img = ImageTk.PhotoImage(img)
					self.canvas.itemconfig(self.img_on_canvas,image=img)
				time.sleep(3)

			if GPIO.input(16) == 0:
				print("Button on pin 16 was pushed!")
				self.avr.discard()
				time.sleep(3)

			if GPIO.input(18) == 0:
				print("Button on pin 18 was pushed!")
				sync.sync2server()
				time.sleep(3)

# def check_gpio():
# 	if GPIO.input(12) == 0:
# 		print("Button on pin 12 was pushed!")
# 		if avr.is_recording():
# 			avr.stop()
# 			rec_stop()
# 			logger.new_log_entry(fname,avr.ext)
# 			print('Video was saved as "'+fname + '.' + avr.ext +'"\n')
# 		else:
# 			fname = 'vid' + str(random.randint(100,1001))
# 			avr.record(OUTPUT_DIR+fname)
# 			rec_start()
# 		time.sleep(3)

# 	if GPIO.input(16) == 0:
# 		print("Button on pin 16 was pushed!")
# 		avr.discard()
# 		time.sleep(3)

# 	if GPIO.input(18) == 0:
# 		print("Button on pin 18 was pushed!")
# 		sync.sync2server()
# 		time.sleep(3)

print('Program Started...')
root = Tk()  
canvas = Canvas(root, width = width, height = height)  
canvas.pack() 
# img = Image.open("images/first.png")  # PIL solution
# img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
# img = ImageTk.PhotoImage(img) 
# #img = ImageTk.PhotoImage(Image.open("Photo.jpg"))  
# canvas.create_image(0, 0, anchor="nw", image=img) 

# root.after(500,check_gpio)

chk = check_buttons(canvas)
t1 = Thread(target=chk.checkloop)
t1.start()

root.mainloop()
	

GPIO.cleanup()