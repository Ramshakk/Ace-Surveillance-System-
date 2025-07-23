import torch
from IPython.display import Image, clear_output  # to display images
import cv2
import matplotlib.pyplot as plt
import torch
import cv2
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import Image ,ImageTk
import pymysql
import matplotlib.pyplot as plt
import time
#from tkVideoPlayer import TkinterVideo
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
import multiprocessing
import winsound
from twilio.rest import Client

people_count_list =[]
account_sid = 'AC1b81c692e1254d17ea554f604444b636'
auth_token = '4d8875c629b6b9603e08e545047a509f'
client = Client(account_sid, auth_token)

filename = 'people_count_list.pkl'

# Load the saved people count list if the file exists
try:
    with open(filename, 'rb') as file:
        people_count_list = pickle.load(file)
except FileNotFoundError:
    people_count_list = []


def send_twilio_alert(message):
    from_phone = '+12543483055'
    to_phone = '+923367163015'
    client.messages.create(
        body='Alert: Number of people reached the total capacity',
        from_=from_phone,
        to=to_phone
    )

def queue(root):
    
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    #model = torch.load('yolov5s.pt')
    # Define the parameters and variables
    roi_x, roi_y, roi_w, roi_h = 0, 0, 1500, 800  # define the ROI as a rectangle (x, y, width, height)
    new_shape = (640, 640)
    thresh_queue = 3
    aoi_x, aoi_y, aoi_w, aoi_h = 410, 200, 1000, 400  # define the AOI as a rectangle (x, y, width, height)
    people_count_list = []  # a list to store the people count at each frame
    
    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack()

    # Open the video file
    cap = cv2.VideoCapture("FYP/q4.mp4")

    plt.switch_backend('TkAgg')

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        # Resize the frame to the desired dimensions
        #frame = cv2.resize(frame, (1000, 700), interpolation=cv2.INTER_LINEAR)

        results = model(frame)  # inference
        # Loop through the detected objects
        people_count = 0
        for detection in results.pred[0]:
            if detection[5] == 0:  # check if the object is a pedestrian (class ID 0)
                bbox = detection[0:4]  # get the bounding box coordinates
                x, y, w, h = bbox.tolist()  # convert the tensor to a list of integers
                # Check if the bounding box intersects with the AOI
                if (x + w/2 > aoi_x-50 + aoi_w*7/8) and (y + h/2 > aoi_y + aoi_h/8) and (y + h/2 < aoi_y + aoi_h*7/8):    
                    people_count += 1
                    if people_count > thresh_queue:
                      #  from Alert import Alert
                        cv2.putText(frame, f'open another counter ', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        people_count -= 1          
        if people_count > 0:
            print(f"{people_count} people in the AOI")
        
        people_count_list.append(people_count)  # append the count to the list 

        #if people_count >= thresh_queue:
            #message = 'Total threshold exceeded! Number of people: {}'.format(sum(people_count_list))
            #send_twilio_alert(message)
        #cv2.rectangle(frame, (aoi_x, aoi_y), (aoi_x + aoi_w, aoi_y + aoi_h), (0, 0, 0), 2)
        canvas.create_rectangle(aoi_x, aoi_y, aoi_x + aoi_w, aoi_y + aoi_h, outline='black', width=2)
    
        # Display the results
        #cv2.imshow('Object Detection', results.render()[0])  # show the image with bounding boxes
    
        # Display the people count
        cv2.putText(frame, f'People Count: {people_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        #cv2.imshow('Frame', frame)
        with open(filename, 'wb') as file:
            pickle.dump(people_count_list, file)
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.resize((1000, 700), Image.ANTIALIAS)

        # Convert the PIL Image to a Tkinter PhotoImage object
        tk_image = ImageTk.PhotoImage(pil_image)

        # Draw the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)    
        # Display the results
        #cv2.imshow('Object Detection', results.render()[0])  # show the image with bounding boxes
    
        # Display the people count
        #cv2.putText(frame, f'People Count: {people_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        #cv2.imshow('Frame', frame)
        
        #if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' to quit
         #   break
        root.update()
    cap.release()
    cv2.destroyAllWindows()
    
    return people_count_list
    
def display_previous_plots(current_results, root):
    with open('people_count_list.pkl', 'rb') as file:
        previous_results = pickle.load(file)
    all_results = previous_results + current_results
    with open('people_count_list.pkl', 'wb') as file:
        pickle.dump(all_results, file)   
     
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).plot(all_results)
    fig.suptitle('People Count Over Time')
    fig.axes[0].set_xlabel('Frame')
    fig.axes[0].set_ylabel('People Count')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Plot the graph of the people count over time
if __name__ == '__main__':
    root = tk.Tk()
    # Set the title of the main window
    root.title("My Application")

    people_count_list = queue(root)
    #display_plot(people_count_list,root)
    display_previous_plots(people_count_list,root)
    root.mainloop()
