import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


# Load the video
def Heatmap(root): 
    cap = cv2.VideoCapture("FYP/crowd.mp4")
     # Create a canvas widget
    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack()
    # Define the HOG descriptor and set the SVM detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    ret, frame = cap.read()
    # Define the heatmap accumulator
    heatmap = np.zeros((frame.shape[0],frame.shape[1]))
    
    # Loop through the frames of the video
    while True:
        # Read the frame
        ret, frame = cap.read()

        # If there are no more frames, break out of the loop
        if not ret:
            break
            
        # Detect people in the frame using the HOG descriptor
        rects, _ = hog.detectMultiScale(frame)
        #heatmap = np.zeros((frame.shape[0], frame.shape[1]))
        # Update the heatmap accumulator for each person detected
        for x, y, w, h in rects:
            heatmap[y:y+h, x:x+w] += 1

        # Normalize the heatmap values to the range [0, 255]
        heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)

        # Apply a color map to the normalized heatmap
        heatmap_color = cv2.applyColorMap(heatmap_norm.astype(np.uint8), cv2.COLORMAP_JET)
        heatmap_color_resized = cv2.resize(heatmap_color, (frame.shape[1], frame.shape[0]))
        # Overlay the heatmap on the original video frame
        overlay = cv2.addWeighted(frame, 0.5, heatmap_color_resized, 0.5, 0)

        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(overlay)

        # Create a PhotoImage object after the root window is initialized
        img = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, image=img, anchor=tk.NW)
        
        #if cv2.waitKey(1) == ord('q'):
         #   break
        root.update()         
        # Display the overlay
        #cv2.imshow('Overlay', overlay)

        # Wait for a key press
        #if cv2.waitKey(1) == ord('q'):
         #   break
    
    cap.release()
    cv2.destroyAllWindows()
    root.mainloop()   
    return heatmap_color  
if __name__ == '__main__':
    root = tk.Tk()
    # Set the title of the main window
    root.title("My Application")

    heat = Heatmap(root)
    #display_plot(,root)
    root.mainloop()
