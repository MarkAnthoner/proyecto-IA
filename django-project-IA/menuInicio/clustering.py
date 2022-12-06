import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt             # Para generar gráficas a partir de los datos
import seaborn as sns                       
from scipy.spatial import distance
from scipy.spatial.distance import cdist    # Para el cálculo de distancias

#para estandarizar los datos
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

import os

class clustering:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
        self.listaResultados = []
        self.matrizInf = []
        self.datosDF = {}
        self.datosColumnas = []  #lista
        self.datosDataFrameFiltrados = pd.DataFrame()  #data frame de la matriz de datos filtrados

        self.datosEstandarizados = []#no dataframe

        self.numeroObjetosMatriz = 0
        self.distanciaObjetosEuclidiana = 0
        self.distanciaObjetosChevyshev = 0
        self.distanciaObjetosManhattan = 0
        self.distanciaObjetosMinkowski = 0

    def mapaCalor(self): 
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/clustering/'+self.nombreArchivo)
        self.datosDataFrameFiltrados = pd.read_csv(directorio)
        self.numeroObjetosMatriz = len(self.datosDataFrameFiltrados)-1
        # Se otbiene la matriz de correlaciones entre variables
        self.datosDF = self.datosDataFrameFiltrados.corr()
        self.matrizInf = np.triu(self.datosDF)
        self.datosColumnas = list(self.datosDataFrameFiltrados.columns)

        return self

    def filtrarDatos(self, listaCaracteristicas):
        #List1 = ['Homer',  'Bart', 'Lisa', 'Maggie', 'Lisa']
        #List2 = ['Bart', 'Homer', 'Lisa']

        check = all(item in self.datosColumnas for item in listaCaracteristicas)
        if check is True:
            self.datosDataFrameFiltrados = self.datosDataFrameFiltrados.drop(columns=listaCaracteristicas)
            estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler o MinMaxScaler 
            MEstandarizada = estandarizar.fit_transform(self.datosDataFrameFiltrados)         # Se calculan la media y desviación y se escalan los datos
            self.datosDataFrameFiltrados = pd.DataFrame(MEstandarizada)
            self.datosEstandarizados = MEstandarizada

        self.datosColumnas = list(self.datosDataFrameFiltrados.columns)

        return self

    