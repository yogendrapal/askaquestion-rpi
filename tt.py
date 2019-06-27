from tkinter import *  
from PIL import ImageTk,Image  

height=240
width=320
def first():
	root = Tk()  
	canvas = Canvas(root, width = width, height = height)  
	canvas.pack() 
	img = Image.open("images/first.png")  # PIL solution
	img = img.resize((width, height), Image.ANTIALIAS) #The (250, 250) is (height, width)
	img = ImageTk.PhotoImage(img) 
	#img = ImageTk.PhotoImage(Image.open("Photo.jpg"))  
	canvas.create_image(0, 0, anchor="nw", image=img) 
	root.mainloop()  

#def quit():
	#root.destroy()

#if __name__=="__main__":
  #first()

