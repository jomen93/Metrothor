import numpy as np
import matplotlib.pyplot as plt 
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import cv2
import glob

img_size = 50

imP = [cv2.imread(file,cv2.IMREAD_GRAYSCALE) for file in glob.glob("imagenes/mascota/Perro100/*.jpg")]
imPNew =np.array([cv2.resize(file,(img_size,img_size))for file in imP]).reshape(-1,img_size,img_size,1)

imPNew = imPNew/255.
model = Sequential()

model.add(Conv2D(64,(3,3),input_shape=imPNew[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Dense(1))
model.add(Activation("sigmoid"))
model.compile(loss="binary_crossentropy",
             optimizer="adam",
             metrics=["accuracy"])
