import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from keras.models import load_model
import cvlib as cv
from cvlib.object_detection import draw_bbox
from vidgear.gears import CamGear
import threading
import numpy as np
import cv2
import imutils
import datetime
import time
import matplotlib.pyplot as plt
import os
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from twilio.rest import Client
import pandas as pd 
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils import class_weight
from tensorflow.python.keras import optimizers
import tensorflow as tf
from tensorflow import keras
import math
from IPython.display import clear_output
from keras.layers import GlobalAveragePooling2D, Dense
from keras.models import Model
from keras.models import load_model
import pickle

gun_cascade = cv2.CascadeClassifier('FYP/cascade.xml')

def detect_and_predict_video(model_path, video_path, class_indices,root):
    IMG_SIZE = 224

    def create_model():
        base_model = ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        learning_rate = 0.01
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(NUM_CLASSES, activation='softmax')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        for layer in base_model.layers:
            layer.trainable = False
        opt = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def draw_prediction(frame, class_string):
        if class_string == "default":
            return frame

        x_start = frame.shape[1] - 600
        cv2.putText(frame, class_string, (x_start, 75), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 0, 0), 2, cv2.LINE_AA)
        return frame


    def prepare_image_for_prediction(img):
        img = np.expand_dims(img, axis=0)
        return preprocess_input(img)

    def get_display_string(pred_class, label_dict):
        txt = ""
        for c, confidence in pred_class:
            txt += label_dict[c]
            if c:
                txt += '[' + str(confidence) + ']'
        return txt

    def get_label_dict(class_indices):
        label_dict = dict((v, k) for k, v in class_indices.items())
        return label_dict

    loaded_model = load_model(model_path)
    label_dict = get_label_dict(class_indices)

    stream = CamGear(source=video_path, logging=True).start()

    count = 0
    ctr = 0
    pred_classes = []
    conf_scores = []
    firstFrame = None
    gun_exist = False
    gun_count = 0
    detected_frames = []
    previous_frame = 0
    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack()    
    while True:
        frame = stream.read()
        count += 1
        if count % 6 != 0:
            continue

        frame = cv2.resize(frame, (1020, 600))
        bbox, label, conf = cv.detect_common_objects(frame)

        filtered_bbox = []
        filtered_label = []
        for bb, lbl in zip(bbox, label):
            if lbl == "person":
                filtered_bbox.append(bb)
                filtered_label.append(lbl)

        frame = draw_bbox(frame, filtered_bbox, filtered_label, conf)
        person_count = len(filtered_bbox)
        cv2.putText(frame, str(person_count), (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        resized_frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        frame_for_pred = prepare_image_for_prediction(resized_frame)
        pred_vec = loaded_model.predict(frame_for_pred)
        confidence = np.round(pred_vec.max(), 2)

        if confidence > 0.4:
            pc = pred_vec.argmax()
            pred_class = label_dict[pc]
            pred_classes.append(pred_class)
            conf_scores.append(confidence)
        else:
            pred_classes.append(None)
            conf_scores.append(None)

        if pred_class:
            txt = get_display_string([(pc, confidence)], label_dict)
            frame = draw_prediction(frame, txt)


        # frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ctr+=1 
        if ctr > 450:
            gun = gun_cascade.detectMultiScale(gray,
                                       1.3, 5,
                                       minSize=(160, 160))
            print("this is gun:" ,len(gun), "::",ctr )
            if len(gun) > previous_frame:
                gun_exist = True
                cv2.putText(frame, "Gun Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                gun_count += 1
                # Call send_sms_alert() function to send the notification
                #send_sms_alert()
            if firstFrame is None:
                firstFrame = gray
                continue
   
            # Draw the timestamp on the frame
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"),
                     (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)

            key = cv2.waitKey(1) & 0xFF
      
            if key == ord('q'):
                break
            if gun_exist:
                detected_frames.append((datetime.datetime.now(), gun_count))

            # Reset the gun counter and flag
            gun_count = 0
            gun_exist = False


        #cv2.imshow("FRAME", frame)
        if cv2.waitKey(1) & 0xFF == 'q':
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.resize((1000, 700), Image.ANTIALIAS)

        # Convert the PIL Image to a Tkinter PhotoImage object
        tk_image = ImageTk.PhotoImage(pil_image)

        # Draw the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        
        root.update()

    stream.release()
    cv2.destroyAllWindows()

    pred_classes = ['Not available' if x is None else x for x in pred_classes]
    conf_scores = ['Not available' if x is None else x for x in conf_scores]


model_path = "FYP/my_model.h5"
video_path = "FYP/Sur3.mp4"
class_indices = {'default': 0, 'fire': 1, 'smoke': 2}


def mainFunc(root):
    detect_and_predict_video(model_path, video_path, class_indices, root)

if __name__ == '__main__':
    root = tk.Tk()
    # Set the title of the main window
    root.title("My Application")

    #pred, conf = predict1(loaded_model, video_path, label_dict, root)
    mainFunc(root)
    #plot_fire(pred_classes,conf_scores,root )
    root.mainloop()