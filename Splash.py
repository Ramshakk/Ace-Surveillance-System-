from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
import pymysql
import matplotlib.pyplot as plt
import time
from tkVideoPlayer import TkinterVideo

def splash():

    w=Tk()

    #Using piece of code from old splash screen
    width_of_window = 700
    height_of_window = 250
    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
    #w.configure(bg='#ED1B76')
    w.overrideredirect(1) #for hiding titlebar

    Frame(w, width=857, height=250, bg='#000000').place(x=0,y=0)
    label1=Label(w, text='SMART SURVEILLANCE SYSTEM', fg='white', bg='#272727') #decorate it 
    label1.configure(font=("Game Of Squids", 24, "bold"))   #You need to install this font in your PC or try another one
    label1.place(x=80,y=90)

    label2=Label(w, text='Loading...', fg='white', bg='#272727') #decorate it 
    label2.configure(font=("Calibri", 11))
    label2.place(x=10,y=215)

#making animation

    image_a=ImageTk.PhotoImage(Image.open('FYP/c2.png'))
    image_b=ImageTk.PhotoImage(Image.open('FYP/c1.png'))




    for i in range(5): #5loops
        l1=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=260, y=145)
        l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=280, y=145)
        l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=300, y=145)
        l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=320, y=145)
        l5=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=340, y=145)
        l6=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=360, y=145)    
        w.update_idletasks()
        time.sleep(0.5)

        l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=260, y=145)
        l2=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=280, y=145)
        l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=300, y=145)
        l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=320, y=145)
        l5=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=340, y=145)
        l6=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=360, y=145)  
        w.update_idletasks()
        time.sleep(0.5)

        l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=260, y=145)
        l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=280, y=145)
        l3=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=300, y=145)
        l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=320, y=145)
        l5=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=340, y=145)
        l6=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=360, y=145)  
        w.update_idletasks()
        time.sleep(0.5)

        l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=260, y=145)
        l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=280, y=145)
        l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=300, y=145)
        l4=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=320, y=145)
        l5=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=340, y=145)
        l6=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=360, y=145)  
        w.update_idletasks()
        time.sleep(0.5)
    
        l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=260, y=145)
        l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=280, y=145)
        l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=300, y=145)
        l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=320, y=145)
        l5=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=340, y=145)
        l6=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=360, y=145)  
        w.update_idletasks()
        time.sleep(0.5)
    
        l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=260, y=145)
        l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=280, y=145)
        l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=300, y=145)
        l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=320, y=145)
        l5=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=340, y=145)
        l6=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=360, y=145)  
        w.update_idletasks()
        time.sleep(0.5)    
        
    w.destroy()

if __name__ == '__main__':
    splash()