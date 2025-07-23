import cv2
import matplotlib.pyplot as plt
import numpy as np
from twilio.rest import Client
from util import get_parking_spots_bboxes, empty_or_not
#from tkVideoPlayer import TkinterVideo
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
from tkinter import *
from tkinter import messagebox
from PIL import Image ,ImageTk

account_sid = 'AC1b81c692e1254d17ea554f604444b636'
auth_token = '4d8875c629b6b9603e08e545047a509f'
client = Client(account_sid, auth_token)
twilio_phone_number = '+12543483055'
recipient_phone_number = '+923367163015'
send_alert=False

available_spots = [] 
filename = 'Available_spots.pkl'

#client = Client(account_sid, auth_token)

# Function to send SMS alert
def send_sms_alert():
    message = Client.messages.create(
        body='Alert: Number of cars reached the total capacity',
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print('Sent SMS alert with SID:', message.sid)
    
def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))

def Parking(root):
    send_alert=False
    mask = "FYP/mask1.png"
    video_path = "FYP/parking3.mp4"

    mask = cv2.imread(mask, 0)

    cap = cv2.VideoCapture(video_path)

    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack()

    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

    spots = get_parking_spots_bboxes(connected_components)

    spots_status = [None for j in spots]
    diffs = [None for j in spots]

    previous_frame = None

    frame_nmr = 0
    ret = True
    step = 30
    
    while ret:
        ret, frame = cap.read()

        if frame_nmr % step == 0 and previous_frame is not None:
            for spot_indx, spot in enumerate(spots):
                x1, y1, w, h = spot

                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

                diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y1:y1 + h, x1:x1 + w, :])

            print([diffs[j] for j in np.argsort(diffs)][::-1])

        if frame_nmr % step == 0:
            if previous_frame is None:
                arr_ = range(len(spots))
            else:
                arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
            for spot_indx in arr_:
                spot = spots[spot_indx]
                x1, y1, w, h = spot

                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

                spot_status = empty_or_not(spot_crop)

                spots_status[spot_indx] = spot_status

        if frame_nmr % step == 0:
            previous_frame = frame.copy()

        available_spots.append(sum(spots_status))

        for spot_indx, spot in enumerate(spots):
            spot_status = spots_status[spot_indx]
            x1, y1, w, h = spots[spot_indx]

            if spot_status:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)

        cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)
        cv2.putText(frame, 'Available spots: {} / {}'.format(str(sum(spots_status)), str(len(spots_status))), (100, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if send_alert:
              send_sms_alert()
              send_alert = False
         
        frame_nmr += 1
        final_frame = cv2.resize(frame, (1000, 700))
        final_frame = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(final_frame)
        photo = ImageTk.PhotoImage(img)

        with open(filename, 'wb') as file:
            pickle.dump(available_spots, file)        
        # display the image on the canvas
        canvas.create_image(0, 0, anchor='nw', image=photo)
        root.update()

    cap.release()
    cv2.destroyAllWindows()
    
    return available_spots

def plot_data(spots_available,root):
    with open('Available_spots.pkl', 'rb') as file:
        previous_results = pickle.load(file)
    all_results = previous_results + spots_available
    with open('Available_spots.pkl', 'wb') as file:
        pickle.dump(all_results, file)  

    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).plot(all_results)
    fig.suptitle('Parking Analysis')
    fig.axes[0].set_xlabel('Frame')
    fig.axes[0].set_ylabel('Available Slots')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
if __name__ == '__main__':
    root = tk.Tk()
    # Set the title of the main window
    root.title("My Application")

    # call Parking function to get processed frame
    available_spots = Parking(root)
    plot_data(available_spots,root)
    root.mainloop()
