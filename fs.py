import numpy as np 
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
import cv2
import math
from IPython.display import clear_output
import os
from keras.layers import GlobalAveragePooling2D, Dense
from keras.models import Model
from keras.models import load_model
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import tkinter as tk
import pickle
# from twilio.rest import Client

IMG_SIZE = 224
NUM_EPOCHS = 20
NUM_CLASSES = 3
TRAIN_BATCH_SIZE = 77
TEST_BATCH_SIZE = 1

pred_classes = []
conf_scores = []

filename = 'fire_smoke.pkl'
# Load the saved people count list if the file exists

def create_model():
    # Load the pre-trained ResNet50 model
    base_model = ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    learning_rate=0.01
    # Add your custom layers on top of the base model
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)

    # Combine the base model and custom layers into a new model
    model = Model(inputs=base_model.input, outputs=predictions)

    # Freeze the weights of the base model so that they are not updated during training
    for layer in base_model.layers:
        layer.trainable = False

    # Compile the model with the desired hyperparameters
    opt =  tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    return model

model = create_model()

def get_label_dict(model):
    class_indices = model.class_indices
    label_dict = dict((v,k) for k,v in class_indices.items())
    return label_dict

def get_labels( generator ):
    generator.reset()
    labels = []
    for i in range(len(generator)):
        labels.extend(np.array(generator[i][1]) )
    return np.argmax(labels, axis =1)

def get_pred_labels(test_generator):
    test_generator.reset()
    pred_vec=model.predict_generator(test_generator,
                                     steps=test_generator.n, #test_generator.batch_size
                                     verbose=1)
    return np.argmax( pred_vec, axis = 1), np.max(pred_vec, axis = 1)
    
def draw_prediction( frame, class_string ):
    x_start = frame.shape[1] -600
    cv2.putText(frame, class_string, (x_start, 75), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 0, 0), 2, cv2.LINE_AA)
    return frame

def prepare_image_for_prediction( img):
   
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    # The below function inserts an additional dimension at the axis position provided
    img = np.expand_dims(img, axis=0)
    # perform pre-processing that was done when resnet model was trained.
    return preprocess_input(img)


loaded_model = load_model("FYP//my_model.h5")
trained_model_l=loaded_model
trained_model=loaded_model
# label_dict_l = get_label_dict(train_generator )
train_generator=loaded_model
validation_generator=loaded_model

def get_display_string(pred_class, label_dict):
    txt = ""
    for c, confidence in pred_class:
        txt += label_dict[c]
        if c :
            txt += '['+ str(confidence) +']'
    #print("count="+str(len(pred_class)) + " txt:" + txt)
    return txt

def get_label_dict(class_indices):
    label_dict = dict((v,k) for k,v in class_indices.items())
    return label_dict

class_indices = {'default':0,'fire': 1, 'smoke': 2}
label_dict = get_label_dict(class_indices)
video_path = "FYP//t1.mp4"

def predict1(model, video_path, label_dict,root):
    # account_sid = 'AC1b81c692e1254d17ea554f604444b636'
    # auth_token = '4d8875c629b6b9603e08e545047a509f'
    # client = Client(account_sid, auth_token)
    
    vs = cv2.VideoCapture(video_path)
    fps = math.floor(vs.get(cv2.CAP_PROP_FPS))
    ret_val = True
    pred_classes = []
    conf_scores = []
    frame_number = 0
    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack()
    while True:
        ret_val, frame = vs.read()
        if not ret_val:
            break
       
        resized_frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        frame_for_pred = prepare_image_for_prediction(resized_frame)
        pred_vec = model.predict(frame_for_pred)
        
        confidence = np.round(pred_vec.max(), 2) 
        if confidence > 0.4:
            pc = pred_vec.argmax()
            pred_class = label_dict[pc]
            pred_classes.append(pred_class)
            conf_scores.append(confidence)
        else:
            pred_classes.append(None)
            conf_scores.append(None)
            
        # if pred_class in ['fire', 'smoke']:
            # Send a notification
            # message = client.messages.create(
            #     body="Fire or smoke detected . Please take necessary action.",
            #     from_="+12543483055",
            #     to="+923367163015"
            # )
        if pred_class:
            txt = get_display_string([(pc, confidence)], label_dict)       
            frame = draw_prediction(frame, txt)

        #cv2.imshow('Frame', frame)
        #cv2.waitKey(1)
        
        frame_number += 1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)    
        canvas.create_image(0, 0, anchor=tk.NW, image=frame)        
        root.update()

    vs.release()
    cv2.destroyAllWindows()
    
    # Replace None values with 'Not available'
    pred_classes = ['Not available' if x is None else x for x in pred_classes]
    conf_scores = ['Not available' if x is None else x for x in conf_scores]
    with open(filename, 'wb') as file:
        pickle.dump((pred_classes,conf_scores), file)    
    return pred_classes, conf_scores

def plot_fire(pred_classes,conf_scores,root):
    with open('fire_smoke.pkl', 'rb') as file:
        all_results = pickle.load(file)
    all_results += pred_classes + conf_scores
    with open('fire_smoke.pkl', 'wb') as file:
        pickle.dump(all_results, file)
       
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).plot(all_results)
    fig.suptitle('Fire and Smoke')
    fig.axes[0].set_xlabel('Frame')
    fig.axes[0].set_ylabel('Prediction')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)   


def mainFunc(root):
    pred_classes, conf_scores = predict1(loaded_model, video_path, label_dict, root)
    return pred_classes, conf_scores

if __name__ == '__main__':
    root = tk.Tk()
    # Set the title of the main window
    root.title("My Application")

    #pred, conf = predict1(loaded_model, video_path, label_dict, root)
    pred_classes, conf_scores = mainFunc(root)
    plot_fire(pred_classes,conf_scores,root )
    root.mainloop()
