import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten
#from sklearn.preprocessing import MinMAxScaler
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
for i in range(0,len(data_c)-pasos+1):
	x_train.append(data_c[i:i+7])
	y_train.append(data_c[i+8])

x_train = np.array(x_train); y_train = np.array(y_train)







