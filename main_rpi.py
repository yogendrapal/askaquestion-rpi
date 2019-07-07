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
frames=[]
no_of_frames=31
vroot= None
iroot = None
home = True
homeidx = 0
homecnt = 0
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

def enableHome():
	global home
	global homeidx
	global homecnt
	homeidx = 0
	homecnt = 0
	home = True

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
	global root
	global no_of_frames
	global canvas	

	def __init__(self):
		global height
		global width
		Thread.__init__(self)
		self.height=height
		self.width=width
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
		global frames
		global vroot
		global iroot
		global home
		global canvas
		while not stop_thread:
			try:
				if GPIO.input(18) == 0:
					print("Button on pin 18 was pushed!")
					home = False
					if self.avr.is_recording():
						self.avr.stop()
						img = self.get_img("images/rec_stop.jpeg")
						canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
						logger.new_log_entry(self.fname,self.avr.ext)
						facerec.store_face_encodings(self.fe, self.fname)
						print('Video was saved as "'+self.fname + '.' + self.avr.ext +'"\n')
						time.sleep(2)
						enableHome()
					else:
						img = self.get_img("images/face_recog.jpeg")
						canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
						self.fname = str(shortuuid.uuid())
						self.fe = facerec.generate_face_encodings()
						if self.fe:
							img = self.get_img("images/please_wait.jpeg")
							canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
							self.avr.record(OUTPUT_DIR+self.fname)
							img = self.get_img("images/record3.jpeg")
							canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
							time.sleep(2)
						else:
							img = self.get_img("images/rec_discard.jpeg")
							canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
							time.sleep(2)
							enableHome()

				if GPIO.input(16) == 0:
					print("Button on pin 16 was pushed!")
					if self.avr.discard():
						home = False
						img = self.get_img("images/rec_discard.jpeg")
						canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
						time.sleep(3)
					else:
						time.sleep(2)
						#it will sync to server if long pressed for 2 secs
						if GPIO.input(16) == 0:
							os.system("python3 deviceinfo.py")
							time.sleep(5)
						else:
							home = False
							img = self.get_img("images/syncing.jpeg")
							canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
							if not sync.sync2server():
								print('display image here for failure!')
							time.sleep(2)
					enableHome()

				if GPIO.input(12) == 0:
					print("Button on pin 12 was pushed!")
					if not self.avr.is_recording():
						home = False
						img = self.get_img("images/please_look.jpeg")
						canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=img),image=img)
						resfid = facerec.fetch_fid()
						if resfid:
							print('Match Found: ',resfid)
							vpath = ""
							for ans in os.listdir(ANSWER_DIR):
								for qid in resfid:
									if ans.startswith(qid):
										vpath = ANSWER_DIR + ans
										break
								if vpath:
									break
							if vpath:
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
						enableHome()
						time.sleep(2)
					
			except Exception as e:
				print(e)
				self.avr.discard()
				os.system('pkill -9 ffmpeg')
				os.execv(sys.executable, ['python3'] + sys.argv)
			

def updater():
	global root
	global frames
	global canvas
	global homeidx
	global home
	global homecnt
	global no_of_frames
	if home:
		if homeidx>=no_of_frames:
			homeidx=0
		frame = frames[homeidx]
		if homeidx == 0:
			if homecnt == 0:
				canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=frame),image=frame)
			homecnt += 1
			if(homecnt == 200):
				homecnt = 0
				homeidx += 1
		elif homeidx in [10,20,30]:
			if homecnt == 0:
				canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=frame),image=frame)
			homecnt += 1
			if(homecnt == 100):
				homecnt = 0
				homeidx += 1
		else:
			canvas.itemconfig(canvas.create_image(0, 0, anchor="nw", image=frame),image=frame)
			homeidx += 1
	root.update()
	root.after(40,updater)

print('Program Started...')

root = Tk.Tk()

#set first image 
canvas = Tk.Canvas(root, width = width, height = height)  
canvas.pack() 

frames = [Tk.PhotoImage(file='images/first.gif',format = 'gif -index %i' %(i)) for i in range(no_of_frames)] 

chk = check_buttons()
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
