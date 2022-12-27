import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt             # Para generar gráficas a partir de los datos
import seaborn as sns                       
from scipy.spatial import distance
from scipy.spatial.distance import cdist    # Para el cálculo de distancias

#para estandarizar los datos
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

#para arbol particional Se importan las bibliotecas
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator

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
        self.matrizOriginal = []

        self.matrizEtiquetadaJerarquico = []
        self.conteoCadaClusterJerarquico = pd.DataFrame()
        self.centroidesJerarquico = pd.DataFrame()

        self.sse = []  #matriz SSE para clustering particional
        self.matrizEtiquetadaParticional = []
        self.conteoCadaClusterParticional = pd.DataFrame()
        self.centroidesParticional = pd.DataFrame()

        self.numeroObjetosMatriz = 0

    def mapaCalor(self): 
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/clustering/'+self.nombreArchivo)
        self.datosDataFrameFiltrados = pd.read_csv(directorio)
        self.matrizOriginal = self.datosDataFrameFiltrados

        self.matrizEtiquetadaJerarquico = self.matrizOriginal
        self.matrizEtiquetadaParticional = self.matrizOriginal

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

    def arbolJerarquico(self):
        #Se crean las etiquetas de los elementos en los clusters
        MJerarquico = AgglomerativeClustering(n_clusters=4, linkage='complete', affinity='euclidean')
        MJerarquico.fit_predict(self.datosEstandarizados)

        #se etiquetan los objetos según el número de clusters
        self.matrizEtiquetadaJerarquico['clusterH'] = MJerarquico.labels_

        #se guarda la matriz con los elementos resumidos en cuenta
        self.conteoCadaClusterJerarquico = self.matrizEtiquetadaJerarquico.groupby(['clusterH'])['clusterH'].count().reset_index(name='Elementos')

        #los centroides
        self.centroidesJerarquico = self.matrizEtiquetadaJerarquico.groupby(['clusterH'])['Texture', 'Area', 'Compactness', 'Symmetry', 'FractalDimension'].mean().reset_index()

        return self

    def arbolParticional(self):
        #se utiliza SSE para tener la suma de distancias de cada cluster
        SSE = []
        for i in range(2, 12):
            km = KMeans(n_clusters=i, random_state=0)
            km.fit(self.datosEstandarizados)
            SSE.append(km.inertia_)

        self.sse = SSE



        #uso de kneed
        kl = KneeLocator(range(2, 12), SSE, curve="convex", direction="decreasing")
        numeroRodilla =  kl.elbow



        #Se crean las etiquetas de los elementos en los clusters
        MParticional = KMeans(n_clusters=numeroRodilla, random_state=0).fit(self.datosEstandarizados)
        MParticional.predict(self.datosEstandarizados)

        #se agrega la columna de las etiquetas en la matriz de datos
        self.matrizEtiquetadaParticional['clusterP'] = MParticional.labels_

        #se guarda la matriz con los elementos resumidos en cuenta
        self.conteoCadaClusterParticional = self.matrizEtiquetadaParticional.groupby(['clusterP'])['clusterP'].count().reset_index(name='Elementos')

        #los centroides
        self.centroidesParticional = self.matrizEtiquetadaParticional.groupby(['clusterP'])['Texture', 'Area', 'Compactness', 'Symmetry', 'FractalDimension'].mean().reset_index()

        return self

    