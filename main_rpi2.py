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
import os
import sys

stop_thread = False
height=240
width=320
root = None
canvas = None
widget=None
counter=5
cu=0
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

	def __init__(self,canvas,label):
		global height
		global width
		global widget
		Thread.__init__(self)
		self.height=height
		self.width=width
		self.canvas = canvas
		self.widget=label
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


	def video_succ(self):
		global cu
		if cu<1:
			cu+=1
			self.widget.config(text="Recording stopped...\nVideo saved successfully!!",fg = "black",font = ("Sans-serif",16))
			#self.canvas.itemconfig(self.canvas.create_text(5,5, anchor="nw"),text="Recording stopped...\nVideo saved successfully!!",font = ("Times",22))
		if cu==1:
			cu+=1
			time.sleep(1)
			self.video_succ()
			#self.widget.after(1000,video_succ(label))
	

	def counter_label(self):
  
		def count():
				global counter
				counter -= 1
				self.widget.config(text="Please wait for "+str(counter)+"  secs",fg = "black",font = ("Sans-serif",18))
				if counter>0:
					#time.sleep(1)
					#count()
					self.widget.after(1000, count)
				else:
					self.widget.config(text="Video ready to be uploaded..",fg = "black",font = ("Sans-serif",16))
                
		if counter>0:
				count()
					

	def checkloop(self):
		global root
		global counter
		global cu
		while not stop_thread:
			try:
				counter=5
				cu=0
				if GPIO.input(18) == 0:
					print("Button on pin 18 was pushed!")
					if self.avr.is_recording():
						self.avr.stop()
						logger.new_log_entry(self.fname,self.avr.ext)
						print('Video was saved as "'+self.fname + '.' + self.avr.ext +'"\n')
						time.sleep(3)

						img = self.get_img("images/record.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)	
						self.counter_label()
						#canvas.create_window(165, 25, window=widget)	

						self.video_succ()	
						time.sleep(5) 
						self.widget.config(text="")
						img = self.get_img("images/first.png")
						self.canvas.itemconfig(self.img_on_canvas,image=img)

					else:
						img = self.get_img("images/please_wait.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
						self.fname = 'vid' + str(random.randint(100,1001))
						self.avr.record(OUTPUT_DIR+self.fname)
						img = self.get_img("images/record3.png")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
						time.sleep(3)

				if GPIO.input(16) == 0:
					print("Button on pin 16 was pushed!")
					if self.avr.discard():
						img = self.get_img("images/rec_discard.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
						time.sleep(3)
					else:
						time.sleep(1)
						if GPIO.input(16) == 0:
							os.execv(sys.executable, ['python3'] + sys.argv)	
					# w2 = Tk()
					# w2.mainloop()
					img = self.get_img("images/first.png")
					self.canvas.itemconfig(self.img_on_canvas,image=img)


				if GPIO.input(12) == 0:
					print("Button on pin 12 was pushed!")
					sync.sync2server()
					time.sleep(3)
			except:
				self.avr.discard()
				os.system('pkill -9 ffmpeg')
				os.execv(sys.executable, ['python3'] + sys.argv)

def updater():
	global root
	root.update()
	root.after(10,updater)

print('Program Started...')
root = Tk()

#set first image 
canvas = Canvas(root, width = width, height = height)  
canvas.pack() 
widget = Label(canvas,font=("Sans-serif",20),bg="white")
widget.pack()
canvas.create_window(165,25,window=widget)
img = Image.open("images/first.png")  # PIL solution
img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
img = ImageTk.PhotoImage(img) 
canvas.create_image(0, 0, anchor="nw", image=img) 

chk = check_buttons(canvas,widget)
t1 = Thread(target=chk.checkloop)
t1.start()


updater()
if RPI:
	root.attributes('-fullscreen', 'true')
	root.focus_force()
root.geometry('320x240')

root.mainloop()
stop_thread = True
time.sleep(2)
if RPI:
	GPIO.cleanup()
