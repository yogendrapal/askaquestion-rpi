from tkinter import *
from PIL import ImageTk,Image 
import time
height=240
width=320

counter = 5 

def video_succ(label):
	label.config(text="Video saved successfully!!",fg = "black",font = ("Times",18))

def counter_label(label):
  
  def count():
    global counter
    counter -= 1
    label.config(text="Please wait for "+str(counter)+"  secs")
    if counter>0:
      label.after(1000, count)
    else:
      label.config(text="Now you can sync your videos!!",fg = "black",font = ("Times",18))
  if counter>0:
    count()


def stop():

	root=Tk() 
	canvas = Canvas(width=width, height=height)   
	canvas.pack(expand="yes", fill="both")    
	img=Image.open("images/record.jpeg")
	img = img.resize((width, height), Image.ANTIALIAS)    
	img = ImageTk.PhotoImage(img)
	canvas.create_image(0, 0, anchor="nw", image=img)
	widget = Label(canvas,font=("Times",20))
	#video_succ(widget)	
	widget.pack()	
	counter_label(widget)
	canvas.create_window(165, 20, window=widget)
	video_succ(widget)       
	root.mainloop()

#def quit():
	#root.destroy()

if __name__=="__main__":
  stop()
