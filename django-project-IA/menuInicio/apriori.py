from django.db import models

#imports de los algoritmos
import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
from apyori import apriori

import os
import json

# Create your models here.


#(support, confidence, lift, nombreArchivo)

class AprioriAlgorithm:
    def __init__(self, nombreArchivo, support, confidence, lift):
        self.nombreArchivo = nombreArchivo
        self.frecuencia = []
        self.items = []
        self.cuenta = 0

        self.support = support
        self.confidence = confidence
        self.lift = lift

        self.listaResultados = []

    def accion(self): 
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/apriori/'+self.nombreArchivo)
        DatosMovies = pd.read_csv(directorio, header=None)
        #Se incluyen todas las transacciones en una sola lista    .    Columna vertical para contabilizar mejor  7460 x 20
        Transacciones = DatosMovies.values.reshape(-1).tolist() #-1 significa 'dimensión no conocida'
        #Se crea una matriz (dataframe) usando la lista y se incluye una columna 'Frecuencia'
        ListaM = pd.DataFrame(Transacciones)
        ListaM['Frecuencia'] = 1
        #Se agrupa los elementos
        ListaM = ListaM.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
        ListaM['Porcentaje'] = (ListaM['Frecuencia'] / ListaM['Frecuencia'].sum()) #Porcentaje
        ListaM = ListaM.rename(columns={0 : 'Item'})

        frecuencia = ListaM['Frecuencia'].values.tolist()
        items = ListaM['Item'].values.tolist()

        frecuencia.reverse()
        items.reverse()

        cuenta = len(items)

        self.frecuencia = frecuencia
        self.items = items
        self.cuenta = cuenta

        return self

    
    def accionReglasAsoc(self):

        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/apriori/'+self.nombreArchivo)
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
