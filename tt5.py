from tkinter import *  
from PIL import ImageTk,Image  

height=240
width=320
def Rec_start():
	root = Tk()  
	canvas = Canvas(root, width = width, height = height)  
	canvas.pack() 
	img = Image.open("images/record3.png")  # PIL solution
	img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
	img = ImageTk.PhotoImage(img) 
	#img = ImageTk.PhotoImage(Image.open("record3.png"))  
	canvas.create_image(0, 0, anchor="nw", image=img) 
	root.mainloop()  

def Rec_stop():
	root = Tk()  
	canvas = Canvas(root, width = width, height = height)  
	canvas.pack() 
	img = Image.open("images/record1.png")  # PIL solution
	img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
	img = ImageTk.PhotoImage(img) 
	#img = ImageTk.PhotoImage(Image.open("record1.png"))  
	canvas.create_image(0, 0, anchor="nw", image=img) 
	root.mainloop()  

def Rec_retry():
	root = Tk()  
	canvas = Canvas(root, width = width, height = height)  
	canvas.pack() 
	img = Image.open("images/record2.png")  # PIL solution
	img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
	img = ImageTk.PhotoImage(img) 
	#img = ImageTk.PhotoImage(Image.open("record2.png"))  
	canvas.create_image(0, 0, anchor="nw", image=img) 
	root.mainloop()  

#def quit():
	#root.destroy()

if __name__=="__main__":
	Rec_retry()
	Rec_start()
	Rec_stop()
