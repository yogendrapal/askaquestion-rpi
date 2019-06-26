from tkinter import *
from PIL import ImageTk,Image 
import time
height=240
width=320
counter = 5
cu=0

def video_succ(label):
	global cu
	if cu<1:
		cu+=1
		label.config(text="Recording stopped...\nVideo saved successfully!!",fg = "black",font = ("Times",18))
	if cu==2:
		cu+=1
		label.after(1000,video_succ(label))
	

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
	img=Image.open("record.jpeg")
	img = img.resize((width, height), Image.ANTIALIAS)    
	img = ImageTk.PhotoImage(img)
	canvas.create_image(0, 0, anchor="nw", image=img)
	widget = Label(canvas,font=("Times",20))	
	widget.pack()	
	counter_label(widget)
	canvas.create_window(165, 25, window=widget)	       
	video_succ(widget)	
	root.mainloop()



if __name__=="__main__":
  stop()
