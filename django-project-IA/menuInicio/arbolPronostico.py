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

class arbolPronostico:
    def __init__(self, nombreEmpresa):
        self.nombreEmpresa = nombreEmpresa
        self.empresaHist = pd.DataFrame()
        self.empresaHistSinColumnas = pd.DataFrame()
        self.empresaHistDescribe = pd.DataFrame()
        self.graficaPreciosAcciones = 0
        
        self.datosColumnas = []  #lista de las columnas
        self.columnasTrasEliminar = []

        self.variableClase = ""
        
        
        self.listaResultados = []
        self.matrizInf = []
        self.datosDF = {}
        
        self.datosColumnasSinClase = []

        self.datosDataFrameFiltrados = pd.DataFrame()  #data frame de la matriz de datos filtrados
        self.datosDataFrameSinClase = pd.DataFrame()
        self.agrupamientoClasificacion = pd.DataFrame()  #se tiene el groupBy

        self.diccionarioEmparejamientoClases = {}
        self.varClaseEsString = True


        
        self.predictoras = []  #estructura que se usa para almacenar el Array de resultados predictores
        self.clase = [] #estructura que se usa para almacenar el Array de resultados Clase
        self.matrizOriginal = []
        self.scoreClasificacion = 0
        self.curvaROCRegresionLineal = 0
        self.resultadoCalculoItem = ""



        self.numeroObjetosMatriz = 0

    def mostrarDatosPrimeraVez(self):
        # Para la empresa seleccionada
        DataEmpresa = yf.Ticker(self.nombreEmpresa)
        self.empresaHist = DataEmpresa.history(start = '2018-1-1', end = '2021-1-1', interval='1d')
        self.empresaHistSinColumnas = self.empresaHist

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

        check = all(item in self.datosColumnas for item in listaCaracteristicas)
        if check is True:
            self.empresaHistSinColumnas = self.empresaHistSinColumnas.drop(columns=listaCaracteristicas)

        self.columnasTrasEliminar = list(self.empresaHistSinColumnas.columns)


        return self