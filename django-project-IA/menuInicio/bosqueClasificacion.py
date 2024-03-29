import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib


from sklearn.metrics import RocCurveDisplay
from sklearn import metrics

#para renderizar el ROC
import urllib
from io import BytesIO
import base64

import os

#modelos
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

#bosque
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import RocCurveDisplay
from sklearn import metrics

class bosqueClasificacion:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
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
        self.curvaROC = 0
        self.resultadoCalculoItem = ""

        self.matrizImportancia = pd.DataFrame()
        self.matrizValidacion = pd.DataFrame()
        self.graficaArbol = 0



        self.numeroObjetosMatriz = 0

    def mapaCalor(self): 
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/arbolYbosque/bosque/'+self.nombreArchivo)
        self.datosDataFrameFiltrados = pd.read_csv(directorio)
        self.matrizOriginal = self.datosDataFrameFiltrados


        self.numeroObjetosMatriz = len(self.datosDataFrameFiltrados)-1
        # Se otbiene la matriz de correlaciones entre variables
        self.datosDF = self.datosDataFrameFiltrados.corr()
        self.matrizInf = np.triu(self.datosDF)
        self.datosColumnas = list(self.datosDataFrameFiltrados.columns)

        return self
    
    def filtrarClase(self, variableClase):
        #List1 = ['Homer',  'Bart', 'Lisa', 'Maggie', 'Lisa']
        #List2 = ['Bart', 'Homer', 'Lisa']

        check = all(item in self.datosColumnas for item in variableClase)
        if check is True:
            self.datosDataFrameSinClase = self.datosDataFrameFiltrados
            self.datosDataFrameSinClase = self.datosDataFrameSinClase.drop(columns=variableClase)


        #se corrobora si la variable clase es string o numero
        prueba = isinstance(variableClase[0], str)
        if (prueba): #si es cadena
            self.varClaseEsString = True
        else:
            self.varClaseEsString = False

        self.datosColumnas = list(self.datosDataFrameSinClase.columns)
        self.datosColumnasSinClase = self.datosColumnas

        return self 

    def filtrarDatos(self, listaCaracteristicas):
        #List1 = ['Homer',  'Bart', 'Lisa', 'Maggie', 'Lisa']
        #List2 = ['Bart', 'Homer', 'Lisa']

        check = all(item in self.datosColumnas for item in listaCaracteristicas)
        if check is True:
            self.datosDataFrameSinClase = self.datosDataFrameSinClase.drop(columns=listaCaracteristicas)

        self.datosColumnas = list(self.datosDataFrameSinClase.columns)


        return self

    def variablesClaseyPredictoras(self):

        #Se agrupan los elementos de la variable clase
        #clase = 'Diagnosis'
        self.agrupamientoClasificacion = self.datosDataFrameFiltrados.groupby([self.variableClase])[self.variableClase].count().reset_index(name='Elementos')
        
        #se pregunta si la variable clase es cadena o numero
        if(self.varClaseEsString == True):
            
            """Proceso de conversionn de clase en letras a numeros"""
            #cada agrupamiento de la variable clase se convierte en un elemento de lista
            #lista de lista con los 
            lista = self.agrupamientoClasificacion[[self.variableClase]].values.tolist()

            #se convierte la lista de listas en una lista plana
            listaPlana = [elemento for sublista in lista for elemento in sublista]

            #con esto se emparejan las clases que estaban en letra, en valores numericos
            i = 0
            listaCombinada = []
            combinacion = []
            for x in listaPlana:
                combinacion.append(x)
                combinacion.append(i)
                listaCombinada.append(combinacion)
                
                combinacion = []
                i = i + 1

            #se convierte la lista de listas con el emparejamiento en un diccionario
            diccionarioReemplazo = {}

            for sublista in listaCombinada:
                diccionarioReemplazo[sublista[0]] = sublista[1]
                
            self.diccionarioEmparejamientoClases = diccionarioReemplazo


            #ahora sí se aplica el reemplazo
            self.datosDataFrameFiltrados = self.datosDataFrameFiltrados.replace(self.diccionarioEmparejamientoClases)
            

        #Variables predictoras
        X = np.array(self.datosDataFrameFiltrados[ self.datosColumnas ])
        self.predictoras = X.tolist()
        
        #Variable clase
        Y = np.array(self.datosDataFrameFiltrados[[self.variableClase]])
        self.clase = Y.tolist()
        #pd.DataFrame(Y)

        return self

    def aplicacionAlgoritmo(self):
        #division de los datos de entrenamiento y validacion
        arrayX = np.array(self.predictoras)
        arrayY = np.array(self.clase)

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(arrayX, arrayY, 
                                                                                test_size = 0.2, 
                                                                                random_state = 0,
                                                                                shuffle = True)

        ClasificacionBA = RandomForestClassifier(n_estimators=105,
                                         max_depth=7, 
                                         min_samples_split=4, 
                                         min_samples_leaf=2, 
                                         random_state=1234)
        ClasificacionBA.fit(X_train, Y_train)

        #Clasificación final 
        Y_ClasificacionBA = ClasificacionBA.predict(X_validation)

        #Se calcula la exactitud promedio de la validación
        self.scoreClasificacion = accuracy_score(Y_validation, Y_ClasificacionBA)



        #validacion del modelo
        #Matriz de clasificación

        #Matriz de clasificación
        ModeloClasificacion1 = ClasificacionBA.predict(X_validation)
        self.matrizValidacion = pd.crosstab(Y_validation.ravel(), 
                                        ModeloClasificacion1, 
                                        rownames=['Reales'], 
                                        colnames=['Clasificación']) 

        fig, ax = plt.subplots()
        CurvaROC = metrics.RocCurveDisplay.from_estimator(ClasificacionBA,
                                                X_validation,
                                                Y_validation,
                                                ax = ax)
    
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        self.curvaROC = graphic



        #matriz importancia
        self.matrizImportancia = pd.DataFrame({'Variable': list(self.datosDataFrameFiltrados[ self.datosColumnas ]),
                            'Importancia': ClasificacionBA.feature_importances_}).sort_values('Importancia', ascending=False)


        return self

    def calculoItemClasificacion(self, itemDataframe):
        #division de los datos de entrenamiento y validacion
        arrayX = np.array(self.predictoras)
        arrayY = np.array(self.clase)

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(arrayX, arrayY, 
                                                                                test_size = 0.2, 
                                                                                random_state = 0,
                                                                                shuffle = True)

        ClasificacionBA = RandomForestClassifier(n_estimators=105,
                                         max_depth=7, 
                                         min_samples_split=4, 
                                         min_samples_leaf=2, 
                                         random_state=1234)
        ClasificacionBA.fit(X_train, Y_train)

        #Clasificación final 
        Y_ClasificacionBA = ClasificacionBA.predict(X_validation)

        #Se calcula la exactitud promedio de la validación
        self.scoreClasificacion = accuracy_score(Y_validation, Y_ClasificacionBA)


        #Item a calcular para clasificar
        itemACalcular = itemDataframe

        #arroja, en numero, la clasificacion
        resultadoClasificacion = int(ClasificacionBA.predict(itemACalcular))

        #si se tuvo una variable clase en string
        if(self.varClaseEsString == True):

            #lista claves y valores por separado del diccionario
            key_list = list(self.diccionarioEmparejamientoClases.keys())
            val_list = list(self.diccionarioEmparejamientoClases.values())
            #se obtiene la llave correspondiente al valor numerico de la clasificacion
            position = val_list.index(int(resultadoClasificacion))
            
            #se guarda la clasificacion resultante
            self.resultadoCalculoItem = key_list[position]
        else:
            #simplememte se asigna el resultado de la clasificacion, que es numerico
            self.resultadoCalculoItem = resultadoClasificacion

        return self