import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv1D ,Flatten

from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMAxScaler
# Lectrua de datos
data = pd.read_excel("reporte.xlsx")

# definicion de variables auxiliares para manejo de columnas
fecha = data.columns[0]
Valor = data.columns[1]
IVA = data.columns[2]
Total = data.columns[3]

# Dado que se tienen listados en diferentes filas los gastos de un mismo dia
# se debe juntar los gastos de un solo dia para poder tener adecuadamente la
# serie de tiempo

data = data.groupby(fecha)[[Valor,IVA,Total]].sum()
# Definicion de la serie temporal
#data_c = data[[fecha,Total]]
data_c = data[Total].to_numpy()

# Se hace un plot para la visualizacion de la serie temporal tal cual datos

plot = False
if plot == True:
	plt.figure(figsize=(15,6))
	plt.plot(data[Total],"b-")
	plt.plot(data[Total],"b.")
	plt.grid(color="k", alpha=0.5, linestyle="dashed", linewidth=0.9)
	plt.title("Compras 2019")
	plt.xlabel("Fecha")
	plt.ylabel("Dinero")
	plt.savefig("Compras 2019")

# Preparacion de los datos
# Alterer el flujo del archivo de datos que contiene la columna en precios
# Se convertirá el problema en uno "supervisado" para poder alimetar la red
# neuronal y utilizar la backpropagation, para hacer esto se hace necesario
# tener una salida y entrada del modelo. Lo que ser hará será tomar los 7
# dias previos para "obtener" el octavo.

# Entradas: Serán 7 Columnas que representan las compras de los 7 dias
# anteriores

# Salida: El valor del "octavo" dia. las ventas de ese día

# Antes de todo se reorganizan los vectores de datos para facilitar el input
# en la red neuronal

Pasos = 7
x_train = []; y_train=[]
len_data = len(data_c)
for i in range(0,len(data_c)-Pasos-1):
	x_train.append(data_c[i:i+7])
	y_train.append(data_c[i+8])

x_train = np.array(x_train); y_train = np.array(y_train)

# forma para poder enviarlo a la red neuronal
#x_train = x_train.reshape(-1,1)
#y_train = y_train.reshape(-1,1)

# separacion entre conjuntos de entrenamiento y validacion
X_train, X_test, Y_train, Y_test = train_test_split(x_train,
						    y_train,
						    test_size=0.2)


X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)


model = Sequential()
model.add(Conv1D(Pasos, (2),
	  input_shape=(X_train.shape[1], 1), activation="elu"))
model.add(Dense(512, input_shape=(Pasos,1), activation="tanh"))
model.add(Flatten())
model.add(Dense(256, activation="elu"))
model.add(Dense(128, activation="tanh"))
model.add(Dense(1, activation="tanh"))

model.compile(loss=tf.keras.losses.MeanAbsolutePercentageError(),
	      optimizer="Adam",
	      metrics=[tf.keras.metrics.Accuracy()])

epochs = 40
model = model.fit(X_train, Y_train, epochs=epochs, verbose=1,
		  validation_data=(X_test, Y_test))












