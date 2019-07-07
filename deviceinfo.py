import subprocess
from config import *
import tkinter as Tk
from PIL import ImageTk,Image 


def getMyIp():
	return subprocess.check_output(['hostname', '-I']).decode().strip()

def getMachineId():
	return MACHINE_ID

def getStorageLeft():
	diskinfo_raw = subprocess.Popen("df -h", shell=True,stdout=subprocess.PIPE)
	output = diskinfo_raw.communicate()[0].decode()
	mount_usage = dict((fields[5], fields[3]) for fields in [line.split() for line in output.strip().split("\n")][1:])
	if RPI:
		return mount_usage['/'] 
	else:
		return mount_usage['/home']

def get_info():
	ip = getMyIp()
	mid = getMachineId()
	ssd = getStorageLeft()
	return ip,mid,ssd

class infoPanel(Tk.Frame):
	def __init__(self,parent):
		Tk.Frame.__init__(self,parent)
		self.parent = parent
		self.ip,self.mid,self.ssd = get_info()
		self.txt1 = Tk.Label(self.parent,text = "Machine ID",font = "Times 18 bold")
		self.txt2 = Tk.Label(self.parent,text = self.mid,font = "Times 12")
		# print('got here!\n')
		img = Image.open("images/machine.png")  # PIL solution
		img = img.resize((80, 80), Image.ANTIALIAS)
		self.imgtmp = ImageTk.PhotoImage(img)
		self.img1 = Tk.Label(self.parent, image = self.imgtmp)

		self.txt3 = Tk.Label(self.parent,text = "IP Address",font = "Times 18 bold")
		self.txt4 = Tk.Label(self.parent,text = self.ip,font = "Times 14")
		img = Image.open("images/ip.png")  # PIL solution
		img = img.resize((80, 80), Image.ANTIALIAS)
		self.imgtmp2 = ImageTk.PhotoImage(img)
		self.img2 = Tk.Label(self.parent, image = self.imgtmp2)

		self.txt5 = Tk.Label(self.parent,text = "Storage Available",font = "Times 18 bold")
		self.txt6 = Tk.Label(self.parent,text = self.ssd,font = "Times 14")
		img = Image.open("images/storage.png")  # PIL solution
		img = img.resize((80, 80), Image.ANTIALIAS)
		self.imgtmp3 = ImageTk.PhotoImage(img)
		self.img3 = Tk.Label(self.parent, image = self.imgtmp3)
		self.img1.grid(row=0,column=0,rowspan = 3)
		self.txt1.grid(row=0,column=1)
		self.txt2.grid(row=1,column=1)
		self.img2.grid(row=3,column=0,rowspan = 3)
		self.txt3.grid(row=3,column=1)
		self.txt4.grid(row=4,column=1)
		self.img3.grid(row=6,column=0,rowspan = 3)
		self.txt5.grid(row=6,column=1)
		self.txt6.grid(row=7,column=1)

def check_ireturn_btn(status):
	global iroot
	if status == 1:
		iroot.quit()
		iroot.destroy()
		return
		#code to exit this window and return to normal flow
	iroot.after(5000,check_ireturn_btn,1)

iroot = Tk.Tk()
window = infoPanel(iroot)
if RPI:
	iroot.attributes('-fullscreen', 'true')
	iroot.focus_force()
check_ireturn_btn(0)
iroot.mainloop()