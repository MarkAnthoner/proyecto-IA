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
        self.datosMatrizEuclidiana = pd.DataFrame()

    def mapaCalor(self): 
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/'+self.nombreArchivo)
        self.datosDataFrameFiltrados = pd.read_csv(directorio)
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

        self.datosColumnas = list(self.datosDataFrameFiltrados.columns)

        return self

    def mostrarMatrizEuclidiana(self):
        DstEuclidiana = cdist(self.datosDataFrameFiltrados[0:5], self.datosDataFrameFiltrados[0:5], metric='euclidean')  #ddist de la biblioteca Spatial.distance
        #dos veces la matriz para hacer el cálculo con valores diferentes de la misma matriz
        self.datosMatrizEuclidiana = pd.DataFrame(DstEuclidiana)

        return self

    
    def accionReglasAsoc(self):

        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/'+self.nombreArchivo)
        DatosMovies = pd.read_csv(directorio, header=None)
        
        #Se crea una lista de listas a partir del dataframe y se remueven los 'NaN'
        #level=0 especifica desde el primer índice
        MoviesLista = DatosMovies.stack().groupby(level=0).apply(list).tolist()
        #cada lista dentro de la gran lista, significan las vistas de cada usuario

        #se pasa MoviesLista sin Nulos
        ReglasC1 = apriori(MoviesLista, 
                    min_support=self.support, 
                    min_confidence=self.confidence, 
                    min_lift=self.lift)
        """min_support=0.01, 
                    min_confidence=0.3, 
                    min_lift=2)"""

        ResultadosC1 = list(ReglasC1)
        #listaResultados = []
        #"Regla":[],"Soporte":[],"Confianza":[], "Lift":[]};

        for item in ResultadosC1:
            #El primer índice de la lista
            Emparejar = item[0]
            items = [x for x in Emparejar]


            self.listaResultados.append( {'Regla': "Regla: " + str(item[0]), 'Soporte': "Soporte: " + str(item[1]), 'Confianza': "Confianza: " + str(item[2][0][2]), 'Lift': "Lift: " + str(item[2][0][3])} )

            #listaResultados["Regla"].append("Regla: " + str(item[0]))
            #print("Regla: " + str(item[0]))

            #El segundo índice de la lista
            #listaResultados["Soporte"].append("Soporte: " + str(item[1]))
            #print("Soporte: " + str(item[1]))

            #El tercer índice de la lista
            #listaResultados["Confianza"].append("Confianza: " + str(item[2][0][2]))
            #print("Confianza: " + str(item[2][0][2]))

            #Cuarto elemento de la lista
            #listaResultados["Lift"].append("Lift: " + str(item[2][0][3]))
            #print("Lift: " + str(item[2][0][3])) 
            #print("=====================================") 

        return self
