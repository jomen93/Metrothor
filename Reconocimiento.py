import numpy as np
import matplotlib.pyplot as plt 
import cv2
import glob
from keras import models

img_size = 50

imP = [cv2.imread(file,cv2.IMREAD_GRAYSCALE) for file in glob.glob("imagenes/mascota/Perro100/*.jpg")]
imG = [cv2.imread(file,cv2.IMREAD_GRAYSCALE) for file in glob.glob("imagenes/mascota/Gato100/*.jpg")]

yimP = np.zeros(len(imP))
yimG = np.ones(len(imG))


X_train, Ytrain = np.array([imP[:int(0.8*len(imP))],yimP[:int(0.8*len(imP))]])
X_test, Ytest   = np.array([imP[int(0.8*len(imP)):len(imP)],yimP[int(0.8*len(imP)):len(imP)]])



X_train = X_train.reshape(len(X_train),img_size,img_size,1)
X_test = X_test.reshape(len(X_test),img_size,img_size,1)

print ("Done!")