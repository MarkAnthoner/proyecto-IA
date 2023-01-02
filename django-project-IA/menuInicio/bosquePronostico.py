import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
          
# Para generar y almacenar los gráficos dentro del cuaderno
import yfinance as yf

#para renderizar y guardar la gráfica de orecios de las acciones
import urllib
from io import BytesIO
import base64

import os

#aplicar el algoritmo
from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.tree import plot_tree

class bosquePronostico:
    def __init__(self, nombreEmpresa):
        self.nombreEmpresa = nombreEmpresa
        self.empresaHist = pd.DataFrame()
        self.empresaHistSinColumnas = pd.DataFrame()
        self.empresaHistDescribe = pd.DataFrame()
        self.graficaPreciosAcciones = 0
        self.graficaPronosticoAcciones = 0
        self.graficaBosque = 0

        self.empresaHistModelo = pd.DataFrame()
        self.datosColumnas = []  #lista de las columnas
        self.columnasTrasEliminar = []

        self.variableClase = ""
        self.columnasFiltradas = False

        self.predictoras = []  #estructura que se usa para almacenar el Array de resultados predictores
        self.clase = [] #estructura que se usa para almacenar el Array de resultados Clase

        self.matrizImportancia = pd.DataFrame()
        self.resultadoCalculoItem = 0
        self.scoreClasificacion = 0
        


    def mostrarDatosPrimeraVez(self):
        # Para la empresa seleccionada
        DataEmpresa = yf.Ticker(self.nombreEmpresa)
        self.empresaHist = DataEmpresa.history(start = '2018-1-1', end = '2021-1-1', interval='1d')
        self.empresaHistSinColumnas = self.empresaHist
        self.empresaHistModelo = self.empresaHist

        self.datosColumnas = list(self.empresaHist.columns)
        self.columnasTrasEliminar = self.datosColumnas

        #resumen de los datos del dataframe
        self.empresaHistDescribe = self.empresaHist.describe()

        #creacion de la grafica del precio de las acciones

        plt.figure(figsize=(20, 5))
        plt.plot(self.empresaHist['Open'], color='purple', marker='+', label='Open')
        plt.plot(self.empresaHist['High'], color='blue', marker='+', label='High')
        plt.plot(self.empresaHist['Low'], color='orange', marker='+', label='Low')
        plt.plot(self.empresaHist['Close'], color='green', marker='+', label='Close')
        plt.xlabel('Fecha')
        plt.ylabel('Precio de las acciones')
        plt.title(self.nombreEmpresa)
        plt.grid(True)
        plt.legend()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        self.graficaPreciosAcciones = graphic

        return self

    def filtrarClase(self, variableClase):
        #List1 = ['Homer',  'Bart', 'Lisa', 'Maggie', 'Lisa']
        #List2 = ['Bart', 'Homer', 'Lisa']

        check = all(item in self.datosColumnas for item in variableClase)
        if check is True:
            self.empresaHistSinColumnas = self.empresaHist
            self.empresaHistSinColumnas = self.empresaHistSinColumnas.drop(columns=variableClase)


        self.columnasTrasEliminar = list(self.empresaHistSinColumnas.columns)

        return self

    def filtrarDatos(self, listaCaracteristicas):
        #List1 = ['Homer',  'Bart', 'Lisa', 'Maggie', 'Lisa']
        #List2 = ['Bart', 'Homer', 'Lisa']

        if (self.columnasFiltradas == False):
            check = all(item in self.datosColumnas for item in listaCaracteristicas)
            if check is True:
                self.empresaHistSinColumnas = self.empresaHistSinColumnas.drop(columns=listaCaracteristicas)
                self.empresaHistModelo = self.empresaHistModelo.drop(columns=listaCaracteristicas)

            self.columnasTrasEliminar = list(self.empresaHistSinColumnas.columns)
            self.columnasFiltradas = True
        else:
            print("Ya se han filtrado las columnas")


        return self

    def variablesPredictorasYClase(self):

        # En caso de tener valores nulos
        self.empresaHistModelo = self.empresaHistModelo.dropna()

        X = np.array(self.empresaHistModelo[ self.columnasTrasEliminar ])
        self.predictoras = X.tolist()

        #Variable clase
        Y = np.array(self.empresaHistModelo[self.variableClase])
        self.clase = Y.tolist()

        return self

    def aplicacionAlgoritmoArbolPronostico(self):
        #division de los datos de entrenamiento y validacion
        arrayX = np.array(self.predictoras)
        arrayY = np.array(self.clase)
        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(arrayX, arrayY, 
                                                                    test_size = 0.2, 
                                                                    random_state = 0, 
                                                                    shuffle = True)

        #Se entrena el modelo a partir de los datos de entrada
        PronosticoBA = RandomForestRegressor(n_estimators=105, max_depth=8, min_samples_split=8, min_samples_leaf=4, random_state=0)
        PronosticoBA.fit(X_train, Y_train)

        #Se genera el pronóstico
        Y_Pronostico = PronosticoBA.predict(X_test)

        #Se calcula la exactitud promedio de la validación
        self.scoreClasificacion = r2_score(Y_test, Y_Pronostico)



        #validacion del modelo

        self.matrizImportancia = pd.DataFrame({'Variable': list(self.empresaHistModelo[self.columnasTrasEliminar]),
                            'Importancia': PronosticoBA.feature_importances_}).sort_values('Importancia', ascending=False)
                            



        #Pronostico de las acciones
        plt.figure(figsize=(20, 5))
        plt.plot(Y_test, color='red', marker='+', label='Real')
        plt.plot(Y_Pronostico, color='green', marker='+', label='Estimado')
        plt.xlabel('Fecha')
        plt.ylabel('Precio de las acciones')
        plt.title('Pronóstico de las acciones de ' + self.nombreEmpresa)
        plt.grid(True)
        plt.legend()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        self.graficaPronosticoAcciones = graphic

        #conformacion del arbol
        Estimador = PronosticoBA.estimators_[50]
        plt.figure(figsize=(16,16))  
        plot_tree(Estimador, 
                feature_names = self.columnasTrasEliminar)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        self.graficaBosque = graphic

        return self

    def calculoItemPronostico(self, itemDataframe):
        #division de los datos de entrenamiento y validacion
        arrayX = np.array(self.predictoras)
        arrayY = np.array(self.clase)
        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(arrayX, arrayY, 
                                                                    test_size = 0.2, 
                                                                    random_state = 0, 
                                                                    shuffle = True)

        #Se entrena el modelo a partir de los datos de entrada
        PronosticoBA = RandomForestRegressor(n_estimators=105, max_depth=8, min_samples_split=8, min_samples_leaf=4, random_state=0)
        PronosticoBA.fit(X_train, Y_train)

        #Se genera el pronóstico
        Y_Pronostico = PronosticoBA.predict(X_test)

        #Se calcula la exactitud promedio de la validación
        self.scoreClasificacion = r2_score(Y_test, Y_Pronostico)




        #Item a calcular para clasificar
        itemACalcular = itemDataframe


        #arroja, en numero, el pronostico
        resultadoClasificacion = float(PronosticoBA.predict(itemACalcular))
        self.resultadoCalculoItem = resultadoClasificacion

        return self
