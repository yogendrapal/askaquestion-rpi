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
import tkinter as Tk
from tkinter import ttk  
from PIL import ImageTk,Image  
from threading import Thread
import os
import sys
import facerec
import shortuuid
import vlc

stop_thread = False
height=240
width=320
root = None
canvas = None
vroot= None
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

class tPlayer(Tk.Frame):
	def __init__(self,parent):
		Tk.Frame.__init__(self,parent)
		self.parent = parent
		self.player = None
		self.videopanel = ttk.Frame(self.parent)
		self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH)
		self.videopanel.pack(fill=Tk.BOTH)
		self.Instance = vlc.Instance()
		self.player = self.Instance.media_player_new()		
		

	def play(self,vpath):
		self.Media = self.Instance.media_new(vpath)
		self.player.set_media(self.Media)
		
		self.player.set_xwindow(self.videopanel.winfo_id())
		self.player.play()

def check_return_btn():
	global vroot
	if GPIO.input(12) == 0:
		# vroot.quit()
		vroot.destroy()
		#code to exit this window and return to normal flow
	vroot.after(10,check_return_btn)

class check_buttons(Thread):

	def __init__(self,canvas):
		global height
		global width
		Thread.__init__(self)
		self.height=height
		self.width=width
		self.canvas = canvas
		img = Image.open("images/first.jpeg")  # PIL solution
		img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img)
		self.img_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=img)

		self.avr = record.AV_Recorder()
		self.fname = ""
		self.fe = None
		time.sleep(1)

	def get_img(self,img_path):
		img = Image.open(img_path)  # PIL solution
		img = img.resize((self.width, self.height), Image.ANTIALIAS) #The (250, 250) is (height, width)
		img = ImageTk.PhotoImage(img)
		return img

	def checkloop(self):
		global root
		global vroot
		while not stop_thread:
			try:
				if GPIO.input(18) == 0:
					print("Button on pin 18 was pushed!")
					if self.avr.is_recording():
						self.avr.stop()
						img = self.get_img("images/rec_stop.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
						logger.new_log_entry(self.fname,self.avr.ext)
						facerec.store_face_encodings(self.fe, self.fname)
						print('Video was saved as "'+self.fname + '.' + self.avr.ext +'"\n')
						time.sleep(3)
						img = self.get_img("images/first.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
					else:
						img = self.get_img("images/face_recog.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
						self.fname = str(shortuuid.uuid())
						self.fe = facerec.generate_face_encodings()
						if self.fe:
							img = self.get_img("images/please_wait.jpeg")
							self.canvas.itemconfig(self.img_on_canvas,image=img)
							self.avr.record(OUTPUT_DIR+self.fname)
							img = self.get_img("images/record3.jpeg")
							self.canvas.itemconfig(self.img_on_canvas,image=img)
						else:
							img = self.get_img("images/rec_discard.jpeg")
							self.canvas.itemconfig(self.img_on_canvas,image=img)
						time.sleep(3)

				if GPIO.input(16) == 0:
					print("Button on pin 16 was pushed!")
					if self.avr.discard():
						img = self.get_img("images/rec_discard.jpeg")
						self.canvas.itemconfig(self.img_on_canvas,image=img)
						time.sleep(3)
					else:
						time.sleep(2)
						#it will sync to server if long pressed for 2 secs
						if GPIO.input(16) == 0:
							img = self.get_img("images/syncing.jpeg")
							self.canvas.itemconfig(self.img_on_canvas,image=img)
							if not sync.sync2server():
								print('display image here for failure!')
								time.sleep(2)
							# os.execv(sys.executable, ['python3'] + sys.argv)	
					# w2 = Tk()
					# w2.mainloop()
					img = self.get_img("images/first.jpeg")
					self.canvas.itemconfig(self.img_on_canvas,image=img)


				if GPIO.input(12) == 0:
					print("Button on pin 12 was pushed!")
					img = self.get_img("images/please_look.jpeg")
					self.canvas.itemconfig(self.img_on_canvas,image=img)
					resfid = facerec.fetch_fid()
					if resfid:
						print('Match Found: ',resfid)
						qid = ""
						vpath = ""
						for ans in resfid:
							qid = ans
							break
						for ans in os.listdir(ANSWER_DIR):
							if ans.startswith(qid):
								vpath = ANSWER_DIR + ans
								break
						if vpath:
							first_time = True
							vroot = Tk.Tk()
							player = tPlayer(vroot)
							player.play(vpath)
							check_return_btn()
							if RPI:
								vroot.attributes('-fullscreen', 'true')
								vroot.focus_force()
							vroot.mainloop()
							vroot = None
					else:
						print('No Match Found')
					img = self.get_img("images/first.jpeg")
					self.canvas.itemconfig(self.img_on_canvas,image=img)
					time.sleep(3)
					

			except Exception as e:
				print(e)
				self.avr.discard()
				os.system('pkill -9 ffmpeg')
				os.execv(sys.executable, ['python3'] + sys.argv)

def updater():
	global root
	root.update()
	root.after(10,updater)

print('Program Started...')
root = Tk.Tk()

#set first image 
canvas = Tk.Canvas(root, width = width, height = height)  
canvas.pack() 
img = Image.open("images/first.jpeg")  # PIL solution
img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
img = ImageTk.PhotoImage(img) 
canvas.create_image(0, 0, anchor="nw", image=img) 

chk = check_buttons(canvas)
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
