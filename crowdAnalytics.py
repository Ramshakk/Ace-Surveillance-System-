import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from vidgear.gears import CamGear 
from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image ,ImageTk

th_crowd = 0 
th_PNO = 0
def display(th_crowd, th_Parking, th_queue, th_PNO):

    # Use the retrieved variables as needed
    print("th_crowd:", th_crowd)
    print("th_Parking:", th_Parking)
    print("th_queue:", th_queue)
    print("th_PNO:", th_PNO)
    threshold =th_crowd
    return th_crowd, th_PNO

def crowd(root,th_crowd):
    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack()
    threshold =th_crowd
    stream = CamGear(source='FYP/people.mp4', logging=True).start()
    print("this is capacity ")
    count=0
    while True:
        frame = stream.read()
        count += 1
        if count % 6 != 0:
            continue
 
        # frame=cv2.resize(frame,(1020,600))
        bbox,label,conf=cv.detect_common_objects(frame)
        frame =  draw_bbox(frame,bbox,label,conf)
        person_count = label.count('person')
        print("person_count", person_count)
        print("threshold: ", threshold)
        if person_count > int(threshold):
            cv2.putText(frame, f'capacity is full', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)     
        cv2.putText(frame,str(person_count),(50,60),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
        #cv2.imshow("FRAME",frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.resize((1000, 700), Image.ANTIALIAS)

        # Convert the PIL Image to a Tkinter PhotoImage object
        tk_image = ImageTk.PhotoImage(pil_image)

        # Draw the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)    
        root.update()

        if cv2.waitKey(1)&0xFF=='q':
            break
    stream.release()
    cv2.destroyAllWindows()