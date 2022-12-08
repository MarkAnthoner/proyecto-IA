from django.db import models

#imports de los algoritmos
import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt             # Para generar gráficas a partir de los datos
import seaborn as sns                       
from scipy.spatial import distance
from scipy.spatial.distance import cdist    # Para el cálculo de distancias

#para estandarizar los datos
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

import os
import json


# Create your models here.



class metricasDistancia:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
        self.listaResultados = []
        self.matrizInf = []
        self.datosDF = {}
        self.datosColumnas = []  #lista
        self.datosDataFrameFiltrados = pd.DataFrame()  #data frame de la matriz de datos filtrados

        self.datosEstandarizados = []#no dataframe

        #matrices recortadas para imprimir
        self.datosMatrizEuclidiana = pd.DataFrame()
        self.datosMatrizChevyshev = pd.DataFrame()        
        self.datosMatrizManhattan = pd.DataFrame() 
        self.datosMatrizMinkowski = pd.DataFrame()


        self.numeroObjetosMatriz = 0
        self.distanciaObjetosEuclidiana = 0
        self.distanciaObjetosChevyshev = 0
        self.distanciaObjetosManhattan = 0
        self.distanciaObjetosMinkowski = 0

    def mapaCalor(self): 
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/metricas/'+self.nombreArchivo)
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

    def mostrarMatrizEuclidiana(self):
        DstEuclidiana = cdist(self.datosEstandarizados[0:5], self.datosEstandarizados[0:5], metric='euclidean')  #ddist de la biblioteca Spatial.distance
        #dos veces la matriz para hacer el cálculo con valores diferentes de la misma matriz
        self.datosMatrizEuclidiana = pd.DataFrame(DstEuclidiana)

        return self

    def mostrarMatrizChevyshev(self):
        DstChebyshev = cdist(self.datosDataFrameFiltrados[0:5], self.datosDataFrameFiltrados[0:5], metric='chebyshev')
        self.datosMatrizChevyshev = pd.DataFrame(DstChebyshev)

        return self

    def mostrarMatrizManhattan(self):
        DstManhattan = cdist(self.datosDataFrameFiltrados[0:5], self.datosDataFrameFiltrados[0:5], metric='cityblock')
        self.datosMatrizManhattan = pd.DataFrame(DstManhattan)

        return self

    def mostrarMatrizMinkowski(self):
        DstMinkowski = cdist(self.datosDataFrameFiltrados[0:5], self.datosDataFrameFiltrados[0:5], metric='minkowski', p=1.5)
        self.datosMatrizMinkowski = pd.DataFrame(DstMinkowski)

        return self



    """CALCULO DE LAS DISTANCIAS ENTRE DOS OBJETOS"""
    def calcularDistanciaObjetosEuclidiana(self, indiceUno, indiceDos):
        Objeto1 = self.datosEstandarizados[indiceUno]
        Objeto2 = self.datosEstandarizados[indiceDos]
        self.distanciaObjetosEuclidiana = distance.euclidean(Objeto1,Objeto2)

        return self

    def calcularDistanciaObjetosChevyshev(self, indiceUno, indiceDos):
        Objeto1 = self.datosEstandarizados[indiceUno]
        Objeto2 = self.datosEstandarizados[indiceDos]
        self.distanciaObjetosChevyshev = distance.chebyshev(Objeto1,Objeto2)

        return self

    def calcularDistanciaObjetosManhattan(self, indiceUno, indiceDos):
        Objeto1 = self.datosEstandarizados[indiceUno]
        Objeto2 = self.datosEstandarizados[indiceDos]
        self.distanciaObjetosManhattan = distance.cityblock(Objeto1,Objeto2)

        return self

    def calcularDistanciaObjetosMinkowski(self, indiceUno, indiceDos):
        Objeto1 = self.datosEstandarizados[indiceUno]
        Objeto2 = self.datosEstandarizados[indiceDos]
        self.distanciaObjetosMinkowski = distance.minkowski(Objeto1,Objeto2, p=1.5)

        return self


