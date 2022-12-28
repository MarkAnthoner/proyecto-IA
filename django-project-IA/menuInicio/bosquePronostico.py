import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
          
# Para generar y almacenar los gráficos dentro del cuaderno
import yfinance as yf

class bosquePronostico:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
        self.listaResultados = []
        self.matrizInf = []
        self.datosDF = {}
        self.datosColumnas = []  #lista de las columnas
        self.datosColumnasSinClase = []

        self.datosDataFrameFiltrados = pd.DataFrame()  #data frame de la matriz de datos filtrados
        self.datosDataFrameSinClase = pd.DataFrame()
        self.agrupamientoClasificacion = pd.DataFrame()  #se tiene el groupBy

        self.diccionarioEmparejamientoClases = {}
        self.varClaseEsString = True


        self.variableClase = ""
        self.predictoras = []  #estructura que se usa para almacenar el Array de resultados predictores
        self.clase = [] #estructura que se usa para almacenar el Array de resultados Clase
        self.matrizOriginal = []
        self.scoreClasificacion = 0
        self.curvaROCRegresionLineal = 0
        self.resultadoCalculoItem = ""



        self.numeroObjetosMatriz = 0