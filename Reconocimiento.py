import numpy as np
import matplotlib.pyplot as plt 
import cv2
import glob
from keras import models

img_size = 50

imP = [cv2.imread(file,cv2.IMREAD_GRAYSCALE) for file in glob.glob("imagenes/mascota/Perro100/*.jpg")]
imG = [cv2.imread(file,cv2.IMREAD_GRAYSCALE) for file in glob.glob("imagenes/mascota/Gato100/*.jpg")]
#yimP = np.zeros(imP)
#imG = np.ones(imG)


#X_train, Ytrain = imP[:0.8*len(imP)],yimP[]


plt.imshow(imG[10],cmap = "gray")
plt.show()