from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .apriori import AprioriAlgorithm


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import resolve

#Vistas del framework API Rest
from rest_framework.views import APIView
from rest_framework.response import Response

#import para validar numeros
import numbers

#importar para archivos
import os

#importar archivos
from django.core.files.storage import FileSystemStorage

#import de apriori
from .apriori import AprioriAlgorithm

#import de metricas de distancias
from .metricasDistancia import metricasDistancia
#para renderizar el mapa de calor
import urllib
from io import BytesIO
import base64
#para manejar los datos
import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt             # Para generar gráficas a partir de los datos
import seaborn as sns                       
from scipy.spatial import distance


#import de clustering
from .clustering import clustering
#para trabajar con el árbol jerarquico
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

#para arbol particional Se importan las bibliotecas
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator


#import de los modelos de clasificacion
from .clasificacion import clasificacion
from sklearn.metrics import RocCurveDisplay




# Create your views here.


#variables globales de Apriori
variableNombreApriori = ""
objetoApriori = AprioriAlgorithm(variableNombreApriori,0,0,0)
accesoValidadoApriori = False
lista = []


#variables globales de Metricas de distancia
variableNombreMetricas = ""
objetoMetricas = metricasDistancia(variableNombreMetricas)
accesoValidadoMetricas = False
pantallaMatrices = False



#variables globales de Clustering
variableNombreClustering = ""
objetoClustering = clustering(variableNombreClustering)
accesoValidadoClustering = False
pantallaClustering = False
arbolJerarquicoGuardado = 0
graficoRodillaGuardado = 0
numeroRodilla = 0



#variables globales de Clasificacion
variableNombreClasificacion = ""
objetoClasificacion = clasificacion(variableNombreClasificacion)
accesoValidadoClasificacion = False
pantallaClasificacion = False
graficoDispersionClasificacionGuardado = 0
graficoCurvaROCGuardado = 0




#Es necesario instalar la App menuInicio en el archivo settings del proyecto
def index(request):
    return render(request, 'index.html')

def temasPreferencia(request):
    return render(request, 'views/otros/temasPreferencia.html')

def sitiosImportantes(request):
    return render(request, 'views/otros/sitiosImportantes.html')

def acercaDe(request):
    return render(request, 'views/otros/acercaDe.html')


def validacionApriori(request):

    global accesoValidadoApriori
    global variableNombreApriori
    global objetoApriori

    global lista

    if(accesoValidadoApriori == False):
        #no se ha validado el dataset, entonces se redirige a la vista de subir archivo
        if request.method == 'GET':
            accesoValidadoApriori = False
            return render(request, 'views/apriori/subirApriori.html')
            #return HttpResponseRedirect(reverse('apriori-subir'))
        else: 
            myfile = request.FILES['archivo']
            fs = FileSystemStorage()

            nombreArchivo = myfile.name
            global variableNombreApriori
            variableNombreApriori = nombreArchivo
            print(nombreArchivo)

            #se pone el directorio completo
            directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/apriori/'+nombreArchivo)
            #print(directorio) 

            #se coloca el directorio y el nombre del archivo
            filename = fs.save(directorio, myfile)
            uploaded_file_url = fs.url(filename)


            global objetoApriori
            objetoApriori = AprioriAlgorithm(variableNombreApriori,0,0,0)
            objetoApriori = objetoApriori.accion()

            accesoValidadoApriori = True

            #return apriori(request)
            return render(request, 'views/apriori/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
    else:


        if request.method == 'GET':
            return render(request, 'views/apriori/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else: 
            #if 'form-ejecucion' in request.POST:
            if request.POST["form-tipo"] == 'form-ejecucion':
                if(request.POST["soporte"]=="" or request.POST["confianza"]=="" or request.POST["elevacion"]==""):
                    return render(request, 'views/apriori/associationRules.html')
                    #return HttpResponseRedirect(reverse('apriori-algoritmo'))
                else:
                    
                    soporte = float(request.POST["soporte"])
                    confianza = float(request.POST["confianza"])
                    elevacion = float(request.POST["elevacion"])

                    
                    objetoApriori = AprioriAlgorithm(variableNombreApriori, soporte, confianza, elevacion)
                    objetoApriori = objetoApriori.accionReglasAsoc()
                    objetoApriori = objetoApriori.accion()
                    #lista = AprioriAlgorithm(variableNombreApriori, soporte, confianza, elevacion)

                    #global lista
                    lista = objetoApriori.listaResultados
                    print(request.POST["form-tipo"])

                    #lista = [1,2,3,4,5,6,7,8,9,10]
                    return render(request, 'views/apriori/associationRules.html', {
                        'list':lista,
                        'display':'block'
                    })
            #elif 'form-reporte' in request.POST:
            elif request.POST["form-tipo"] == 'form-reporte':
                """Logica de generacion de reporte"""
                print("Se genera reporte")
                #global lista
                return render(request, 'views/apriori/associationRules.html', {
                        'list':lista,
                        'display':'block',
                        'muestraReporte':'block'
                    })
                




        #se imprime el directorio actual
        #print(  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/')  )

        #se guarda el directorio actual para validar que se haya subido un archivo csv
        direccion = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/')

        #si sí se subió un csv antes, se redirije al algoritmo apriori
        if any(File.endswith(".csv") for File in os.listdir( direccion )):
            #return render(request, 'views/associationRules.html')

            accesoValidadoApriori = True
            return render(request, 'views/apriori/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else:
            #return HttpResponseRedirect(resolve('views/subirApriori.html'))
            #return HttpResponseRedirect(reverse('apriori-subir'))
            return render(request, 'views/apriori/subirApriori.html')
            #return render(request, 'views/subirApriori.html')
 
def eliminarDataSetApriori(request):
    global accesoValidadoApriori
    global lista
    if(accesoValidadoApriori == True):
        accesoValidadoApriori = False
        lista = []

        """#Falta agregar logica de eliminar archivo CSV"""
        #return render(request, 'views/subirApriori.html')
        return HttpResponseRedirect(reverse('index'))
    else:
        #si el acceso ya no es validado, se manda directamente al inicio
        accesoValidadoApriori = False
        return render(request, 'views/apriori/subirApriori.html')

"""Uso de Rest framework para trabajar con los datos de APRIORI"""
class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None): 
        """data = {
            "sales": 200,
            "customers":20,
        }"""

        global variableNombreApriori

        global objetoApriori

        #items = retornaItems(variableNombreApriori)
        items = objetoApriori.items

        #frecuencia = retornaFrecuencia(variableNombreApriori)
        frecuencia = objetoApriori.frecuencia

        #cuenta = retornaCuenta(variableNombreApriori)
        cuenta = objetoApriori.cuenta

        data = {
            "items": items,
            "frecuencia":frecuencia,
            "cuenta": cuenta,
        }
        return Response(data)



"""Metricas de distancia"""
def validacionMetricasDistancia(request):
    global accesoValidadoMetricas
    global variableNombreMetricas
    global objetoMetricas
    global pantallaMatrices

    if(accesoValidadoMetricas == False):
        #no se ha validado el dataset, entonces se redirige a la vista de subir archivo
        if request.method == 'GET':
            accesoValidadoMetricas = False
            return render(request, 'views/metricas/subirMetricas.html')
        else: 
            myfile = request.FILES['archivo-metricas']
            fs = FileSystemStorage()

            nombreArchivo = myfile.name
            global variableNombreMetricas
            variableNombreMetricas = nombreArchivo

            #se pone el directorio completo
            directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/metricas/'+nombreArchivo)

            #se coloca el directorio y el nombre del archivo
            filename = fs.save(directorio, myfile)
            uploaded_file_url = fs.url(filename)


            global objetoMetricas
            objetoMetricas = metricasDistancia(variableNombreMetricas)
            #generamos la matriz inferior
            objetoMetricas = objetoMetricas.mapaCalor()

            accesoValidadoMetricas = True

            """Poner parte de la impresion en pantalla"""
            #llamamos al metodo de este archivo que genera el grafico tomando la matriz inferior
            mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)


            return render(request, 'views/metricas/metricasDistancia.html', {
                'mapaCalor':mapaCalorGenerado,
                'listaColumnas':objetoMetricas.datosColumnas,
                'displaySeleccion':"block",
                'display':"none",
            })
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
    else:


        if request.method == 'GET':
            if pantallaMatrices == True:
                print("CUando se esté en la pantalla de subir objetos, y no se ingrese correctamente")
                #aquí se ha seleccionado alguna característica
                mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                return render(request, 'views/metricas/metricasDistancia.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoMetricas.datosColumnas,
                    'displaySeleccion':"none",
                    'display':"block",
                    'dataFrameEuclidiana':objetoMetricas.datosMatrizEuclidiana,
                    'dataFrameChevyshev':objetoMetricas.datosMatrizChevyshev,
                    'dataFrameManhattan':objetoMetricas.datosMatrizManhattan,
                    'dataFrameMinkowski':objetoMetricas.datosMatrizMinkowski,
                    'numeroObjetos': objetoMetricas.numeroObjetosMatriz,
                })

            else:
                mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                return render(request, 'views/metricas/metricasDistancia.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoMetricas.datosColumnas,
                    'displaySeleccion':"block",
                    'display':"none",
                })
                #return render(request, 'views/metricas/metricasDistancia.html')
                #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else: 
            
            if request.POST["form-tipo"] == 'form-seleccion-carac':
                """Con todo esto me di cuenta de que en el form sin seleccionar casillas, se tienen tres elementos unicamente"""
                """
                print()
                print()
                print(len(request.POST))
                print(request.POST)
                print()
                print() """

                #si no se seleccionó alguna caracteristica, se vuelve a preguntar
                if(len(request.POST) <= 3):
                    mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                    print()
                    print("Se vuelve a preguntar por las caracteristicas")
                    print()
                    return render(request, 'views/metricas/metricasDistancia.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoMetricas.datosColumnas,
                        'displaySeleccion':"block",
                        'display':"none",
                    })
                else:
                    print()
                    print("Se procesan las características")
                    print()

                    pantallaMatrices = True

                    diccionarioCaracteristicas = request.POST
                    listaCaracteristicas = []
                    tamanioDiccionario = len(request.POST)

                    for key in diccionarioCaracteristicas:
                        listaCaracteristicas.append(diccionarioCaracteristicas[key])

                    #solo se toman las características seleccionadas
                    tamanioLista = tamanioDiccionario - 2
                    listaCaracteristicas = listaCaracteristicas[1:tamanioLista]
                    print(listaCaracteristicas)
                    print()

                    #eliminar las características
                    objetoMetricas = objetoMetricas.filtrarDatos(listaCaracteristicas)

                    #obtener las matrices de distancias parciales
                    objetoMetricas = objetoMetricas.mostrarMatrizEuclidiana()
                    objetoMetricas = objetoMetricas.mostrarMatrizChevyshev()
                    objetoMetricas = objetoMetricas.mostrarMatrizManhattan()
                    objetoMetricas = objetoMetricas.mostrarMatrizMinkowski()

                    
                    #aquí se ha seleccionado alguna característica
                    mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                    return render(request, 'views/metricas/metricasDistancia.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoMetricas.datosColumnas,
                        'displaySeleccion':"none",
                        'display':"block",
                        'dataFrameEuclidiana':objetoMetricas.datosMatrizEuclidiana,
                        'dataFrameChevyshev':objetoMetricas.datosMatrizChevyshev,
                        'dataFrameManhattan':objetoMetricas.datosMatrizManhattan,
                        'dataFrameMinkowski':objetoMetricas.datosMatrizMinkowski,
                        'numeroObjetos': objetoMetricas.numeroObjetosMatriz,
                    })


            #elif 'form-reporte' in request.POST:
            elif request.POST["form-tipo"] == 'form-reporte':
                """Logica de generacion de reporte"""
                print("Se genera reporte")
                #global lista
                return render(request, 'views/associationRules.html', {
                        'list':lista,
                        'display':'block',
                        'muestraReporte':'block',
                    })

            elif request.POST["form-tipo"] == 'form-matriz-euclidiana':
                """Logica de la generacion de distancia euclidiana"""

                #se obtiene la distancia Euclidiana

                #el nombre de la variable en POST es el "name" del formulario
                valorObjeto1 = int(request.POST["name_valor1"])
                valorObjeto2 = int(request.POST["name_valor2"])
                objetoMetricas = objetoMetricas.calcularDistanciaObjetosEuclidiana(valorObjeto1, valorObjeto2)

                
                #aquí se ha seleccionado alguna característica
                mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                return render(request, 'views/metricas/metricasDistancia.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoMetricas.datosColumnas,
                    'displaySeleccion':"none",
                    'display':"block",
                    'dataFrameEuclidiana':objetoMetricas.datosMatrizEuclidiana,
                    'dataFrameChevyshev':objetoMetricas.datosMatrizChevyshev,
                    'dataFrameManhattan':objetoMetricas.datosMatrizManhattan,
                    'dataFrameMinkowski':objetoMetricas.datosMatrizMinkowski,
                    'numeroObjetos': objetoMetricas.numeroObjetosMatriz,
                    'distanciaObjetosEuclidiana': objetoMetricas.distanciaObjetosEuclidiana,
                    'objetoEu1':valorObjeto1,
                    'objetoEu2':valorObjeto2,
                    'hayDistancia':"Euclidiana",
                })

            elif request.POST["form-tipo"] == 'form-matriz-chevyshev':
                """Logica de la generacion de distancia chevyshev"""

                #el nombre de la variable en POST es el "name" del formulario
                valorObjeto1 = int(request.POST["name_valor1"])
                valorObjeto2 = int(request.POST["name_valor2"])
                objetoMetricas = objetoMetricas.calcularDistanciaObjetosChevyshev(valorObjeto1, valorObjeto2)

                
                #aquí se ha seleccionado alguna característica
                mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                return render(request, 'views/metricas/metricasDistancia.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoMetricas.datosColumnas,
                    'displaySeleccion':"none",
                    'display':"block",
                    'dataFrameEuclidiana':objetoMetricas.datosMatrizEuclidiana,
                    'dataFrameChevyshev':objetoMetricas.datosMatrizChevyshev,
                    'dataFrameManhattan':objetoMetricas.datosMatrizManhattan,
                    'dataFrameMinkowski':objetoMetricas.datosMatrizMinkowski,
                    'numeroObjetos': objetoMetricas.numeroObjetosMatriz,
                    'distanciaObjetosChevyshev': objetoMetricas.distanciaObjetosChevyshev,
                    'objetoCh1':valorObjeto1,
                    'objetoCh2':valorObjeto2,
                    'hayDistancia':"Chevyshev",
                })
            elif request.POST["form-tipo"] == 'form-matriz-manhattan':
                """Logica de la generacion de distancia manhattan"""

                #el nombre de la variable en POST es el "name" del formulario
                valorObjeto1 = int(request.POST["name_valor1"])
                valorObjeto2 = int(request.POST["name_valor2"])
                objetoMetricas = objetoMetricas.calcularDistanciaObjetosManhattan(valorObjeto1, valorObjeto2)

                
                #aquí se ha seleccionado alguna característica
                mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                return render(request, 'views/metricas/metricasDistancia.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoMetricas.datosColumnas,
                    'displaySeleccion':"none",
                    'display':"block",
                    'dataFrameEuclidiana':objetoMetricas.datosMatrizEuclidiana,
                    'dataFrameChevyshev':objetoMetricas.datosMatrizChevyshev,
                    'dataFrameManhattan':objetoMetricas.datosMatrizManhattan,
                    'dataFrameMinkowski':objetoMetricas.datosMatrizMinkowski,
                    'numeroObjetos': objetoMetricas.numeroObjetosMatriz,
                    'distanciaObjetosManhattan': objetoMetricas.distanciaObjetosManhattan,
                    'objetoMan1':valorObjeto1,
                    'objetoMan2':valorObjeto2,
                    'hayDistancia':"Manhattan",
                })
            elif request.POST["form-tipo"] == 'form-matriz-minkowski':
                """Logica de la generacion de distancia minkowski"""

                #el nombre de la variable en POST es el "name" del formulario
                valorObjeto1 = int(request.POST["name_valor1"])
                valorObjeto2 = int(request.POST["name_valor2"])
                objetoMetricas = objetoMetricas.calcularDistanciaObjetosMinkowski(valorObjeto1, valorObjeto2)

                
                #aquí se ha seleccionado alguna característica
                mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                return render(request, 'views/metricas/metricasDistancia.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoMetricas.datosColumnas,
                    'displaySeleccion':"none",
                    'display':"block",
                    'dataFrameEuclidiana':objetoMetricas.datosMatrizEuclidiana,
                    'dataFrameChevyshev':objetoMetricas.datosMatrizChevyshev,
                    'dataFrameManhattan':objetoMetricas.datosMatrizManhattan,
                    'dataFrameMinkowski':objetoMetricas.datosMatrizMinkowski,
                    'numeroObjetos': objetoMetricas.numeroObjetosMatriz,
                    'distanciaObjetosMinkowski': objetoMetricas.distanciaObjetosMinkowski,
                    'objetoMin1':valorObjeto1,
                    'objetoMin2':valorObjeto2,
                    'hayDistancia':"Minkowski",
                })
                

            return 0

def eliminarDataSetMetricas(request):
    global accesoValidadoMetricas
    if(accesoValidadoMetricas == True):
        accesoValidadoMetricas = False

        """#Falta agregar logica de eliminar archivo CSV"""
        #return render(request, 'views/subirApriori.html')
        return HttpResponseRedirect(reverse('index'))
    else:
        #si el acceso ya no es validado, se manda directamente al inicio
        accesoValidadoMetricas = False
        return render(request, 'views/metricas/subirMetricas.html')

def generarMapaMetricas(matrizInferior, datosCorrelacionados):
    # Con la matriz de correlaciones, se plantea un mapa de calor para ver que hay variables muy dependientes entre sí: 
    # perímetro, area, radio, puntos concavos, concavidad
    # compactacion, puntos concavos, concavidad

    plt.figure(figsize=(14,7))
    sns.heatmap(datosCorrelacionados, cmap = 'RdBu_r', annot = True, mask = matrizInferior)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic




"""Clustering"""
def validacionClustering(request):
    global accesoValidadoClustering
    global variableNombreClustering
    global objetoClustering
    global pantallaClustering
    global arbolJerarquicoGuardado
    global graficoRodillaGuardado

    if(accesoValidadoClustering == False):
        #no se ha validado el dataset, entonces se redirige a la vista de subir archivo
        if request.method == 'GET':
            accesoValidadoClustering = False
            return render(request, 'views/clustering/subirClustering.html')
        else: 
            myfile = request.FILES['archivo-clustering']
            fs = FileSystemStorage()

            nombreArchivo = myfile.name
            global variableNombreClustering
            variableNombreClustering = nombreArchivo

            #se pone el directorio completo
            directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/clustering/'+nombreArchivo)

            #se coloca el directorio y el nombre del archivo
            filename = fs.save(directorio, myfile)
            uploaded_file_url = fs.url(filename)


            global objetoClustering
            objetoClustering = clustering(variableNombreClustering)
            #generamos la matriz inferior
            objetoClustering = objetoClustering.mapaCalor()

            accesoValidadoClustering = True

            """Poner parte de la impresion en pantalla"""
            #llamamos al metodo de este archivo que genera el grafico tomando la matriz inferior
            mapaCalorGenerado = generarMapaMetricas(objetoClustering.matrizInf, objetoClustering.datosDF)


            return render(request, 'views/clustering/clustering.html', {
                'mapaCalor':mapaCalorGenerado,
                'listaColumnas':objetoClustering.datosColumnas,
                'displaySeleccion':"block",
                'display':"none",
            })
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
    else:


        if request.method == 'GET':
            if pantallaClustering == True:
                print("Cuando ya se haya calculado algún cluster, pero se ingrese a la pantalla de Clustering desde otra vista")
                mapaCalorGenerado = generarMapaMetricas(objetoClustering.matrizInf, objetoClustering.datosDF)
                return render(request, 'views/clustering/clustering.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoClustering.datosColumnas,
                    'displaySeleccion':"none",
                    'display':"block",
                    'numeroObjetos': objetoClustering.numeroObjetosMatriz,

                    'arbolJerarquico': arbolJerarquicoGuardado,
                    'dataFrameJerarquico':objetoClustering.matrizEtiquetadaJerarquico,
                    'dataFrameConteoJerarquico':objetoClustering.conteoCadaClusterJerarquico,
                    'dataFrameCentroidesJerarquico':objetoClustering.centroidesJerarquico,

                    'arbolParticional':graficoRodillaGuardado,
                    'dataFrameParticional':objetoClustering.matrizEtiquetadaParticional,
                    'dataFrameConteoParticional':objetoClustering.conteoCadaClusterParticional,
                    'dataFrameCentroidesParticional':objetoClustering.centroidesParticional,
                })

            else:
                print("Pantalla GET cuando se regresa a la vista de Clustering, y no se haya entrada antes a calcular los clusters")
                mapaCalorGenerado = generarMapaMetricas(objetoClustering.matrizInf, objetoClustering.datosDF)
                return render(request, 'views/clustering/clustering.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoClustering.datosColumnas,
                    'displaySeleccion':"block",
                    'display':"none",
                })
                #return render(request, 'views/metricas/metricasDistancia.html')
                #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else: 
            
            if request.POST["form-tipo"] == 'form-seleccion-carac':
                """Con todo esto me di cuenta de que en el form sin seleccionar casillas, se tienen tres elementos unicamente"""
                """
                print()
                print()
                print(len(request.POST))
                print(request.POST)
                print()
                print() """

                #si no se seleccionó alguna caracteristica, se vuelve a preguntar
                if(len(request.POST) <= 3):
                    mapaCalorGenerado = generarMapaMetricas(objetoClustering.matrizInf, objetoClustering.datosDF)
                    print()
                    print("Se vuelve a preguntar por las caracteristicas")
                    print()
                    return render(request, 'views/clustering/clustering.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoClustering.datosColumnas,
                        'displaySeleccion':"block",
                        'display':"none",
                    })
                else:
                    print()
                    print("Se procesan las características")
                    print()

                    pantallaClustering = True

                    diccionarioCaracteristicas = request.POST
                    listaCaracteristicas = []
                    tamanioDiccionario = len(request.POST)

                    for key in diccionarioCaracteristicas:
                        listaCaracteristicas.append(diccionarioCaracteristicas[key])

                    #solo se toman las características seleccionadas
                    tamanioLista = tamanioDiccionario - 2
                    listaCaracteristicas = listaCaracteristicas[1:tamanioLista]
                    print(listaCaracteristicas)
                    print()

                    #eliminar las características
                    objetoClustering = objetoClustering.filtrarDatos(listaCaracteristicas)


                    """HASTA ESTE PUNTO, LO ANTERIOR ES LO MISMO QUE EN MÉTRICAS"""


                    #obtener la matriz con los clusters jerarquicos
                    objetoClustering = objetoClustering.arbolJerarquico()
                    #generar el arbol jerarquico dibujado
                    arbolJerarquico = generarArbolJerarquico(objetoClustering.datosEstandarizados)


                    #ahora el arbol particional
                    objetoClustering = objetoClustering.arbolParticional()
                    arbolParticional = generarGraficoRodilla(objetoClustering.sse)
                    
                    #aquí se ha seleccionado alguna característica
                    mapaCalorGenerado = generarMapaMetricas(objetoClustering.matrizInf, objetoClustering.datosDF)
                    return render(request, 'views/clustering/clustering.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoClustering.datosColumnas,
                        'displaySeleccion':"none",
                        'display':"block",
                        'numeroObjetos': objetoClustering.numeroObjetosMatriz,

                        'arbolJerarquico': arbolJerarquico,
                        'dataFrameJerarquico':objetoClustering.matrizEtiquetadaJerarquico,
                        'dataFrameConteoJerarquico':objetoClustering.conteoCadaClusterJerarquico,
                        'dataFrameCentroidesJerarquico':objetoClustering.centroidesJerarquico,

                        'arbolParticional':arbolParticional,
                        'dataFrameParticional':objetoClustering.matrizEtiquetadaParticional,
                        'dataFrameConteoParticional':objetoClustering.conteoCadaClusterParticional,
                        'dataFrameCentroidesParticional':objetoClustering.centroidesParticional,
                    })


            #elif 'form-reporte' in request.POST:
            elif request.POST["form-tipo"] == 'form-reporte':
                """Logica de generacion de reporte"""
                print("Se genera reporte")
                #global lista
                return render(request, 'views/associationRules.html', {
                        'list':lista,
                        'display':'block',
                        'muestraReporte':'block',
                    })
                

            return 0


def eliminarDataSetClustering(request):
    global accesoValidadoClustering
    if(accesoValidadoClustering == True):
        accesoValidadoClustering = False

        """#Falta agregar logica de eliminar archivo CSV"""
        #return render(request, 'views/subirApriori.html')
        return HttpResponseRedirect(reverse('index'))
    else:
        #si el acceso ya no es validado, se manda directamente al inicio
        accesoValidadoClustering = False
        return render(request, 'views/clustering/subirClustering.html')

def generarArbolJerarquico(matrizEstandarizada):

    global arbolJerarquicoGuardado
    
    plt.figure(figsize=(10, 7))
    plt.title("Árbol jerárquico")
    plt.xlabel('Observaciones')
    plt.ylabel('Distancia')
    shc.dendrogram(shc.linkage(matrizEstandarizada, method='complete', metric='euclidean'))

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    arbolJerarquicoGuardado = graphic

    return graphic

def generarGraficoRodilla(matrizSSE):

    global graficoRodillaGuardado
    global numeroRodilla

    kl = KneeLocator(range(2, 12), matrizSSE, curve="convex", direction="decreasing")
    
    numeroRodilla = kl.elbow

    #se localiza el mejor numero de clusters con kneed
    plt.style.use('ggplot')
    kl.plot_knee()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    graficoRodillaGuardado = graphic

    return graphic




"""Clasificación"""
def validacionClasificacion(request):
    global accesoValidadoClasificacion
    global variableNombreClasificacion
    global objetoClasificacion
    global pantallaClasificacion

    if(accesoValidadoClasificacion == False):
        #no se ha validado el dataset, entonces se redirige a la vista de subir archivo
        if request.method == 'GET':
            accesoValidadoClasificacion = False
            return render(request, 'views/clasificacion/subirClasificacion.html')
        else: 
            myfile = request.FILES['archivo-clasificacion']
            fs = FileSystemStorage()

            nombreArchivo = myfile.name
            global variableNombreClasificacion
            variableNombreClasificacion = nombreArchivo

            #se pone el directorio completo
            directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/clasificacion/'+nombreArchivo)

            #se coloca el directorio y el nombre del archivo
            filename = fs.save(directorio, myfile)
            uploaded_file_url = fs.url(filename)


            global objetoClasificacion
            objetoClasificacion = clasificacion(variableNombreClasificacion)
            #generamos la matriz inferior
            objetoClasificacion = objetoClasificacion.mapaCalor()

            accesoValidadoClasificacion = True

            """Poner parte de la impresion en pantalla"""
            #llamamos al metodo de este archivo que genera el grafico tomando la matriz inferior
            mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClasificacion.datosDF)


            return render(request, 'views/clasificacion/clasificacion.html', {
                'mapaCalor':mapaCalorGenerado,
                'listaColumnas':objetoClasificacion.datosColumnas,
                'displaySeleccion':"block",
                'displayClase':"block",
                'displayPredictoras':"none",
                'display':"none",
            })
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
    else:


        if request.method == 'GET':
            if pantallaClasificacion == True:
                print("Cuando ya se haya calculado la clasificacion, pero se ingrese a la pantalla de Clasificacion desde otra vista")
                mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClustering.datosDF)
                return render(request, 'views/clasificacion/clasificacion.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoClasificacion.datosColumnas,
                    'displaySeleccion':"none",
                    'displayClase':"block",
                    'displayPredictoras':"none",
                    'display':"block",
                    'numeroObjetos': objetoClasificacion.numeroObjetosMatriz,
                
                })

            else:
                print("Pantalla GET cuando se regresa a la vista de Clasificacion, y no se haya entrada antes a calcular la clasificacion")
                mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClasificacion.datosDF)
                return render(request, 'views/clasificacion/clasificacion.html', {
                    'mapaCalor':mapaCalorGenerado,
                    'listaColumnas':objetoClasificacion.datosColumnas,
                    'displaySeleccion':"block",
                    'displayClase':"block",
                    'displayPredictoras':"none",
                    'display':"none",
                })
                #return render(request, 'views/metricas/metricasDistancia.html')
                #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else: 
            
            if request.POST["form-tipo"] == 'form-seleccion-clase':
                """Con todo esto me di cuenta de que en el form sin seleccionar casillas, se tienen tres elementos unicamente"""
                """
                print()
                print()
                print(len(request.POST))
                print(request.POST)
                print()
                print() """

                #si no se seleccionó alguna caracteristica, o si se seleccionó más de 1, se vuelve a preguntar
                if(len(request.POST) <= 3 or len(request.POST) >=5):
                    mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClasificacion.datosDF)
                    print()
                    print("Se vuelve a preguntar por las caracteristicas")
                    print()
                    return render(request, 'views/clasificacion/clasificacion.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoClasificacion.datosColumnas,
                        'displaySeleccion':"block",
                        'displayClase':"block",
                        'displayPredictoras':"none",
                        'display':"none",
                    })
                else:
                    print()
                    print("Se procesa la clase")
                    print()

                    pantallaClasificacion = False

                    diccionarioCaracteristicas = request.POST
                    listaCaracteristicas = []
                    tamanioDiccionario = len(request.POST)

                    for key in diccionarioCaracteristicas:
                        listaCaracteristicas.append(diccionarioCaracteristicas[key])

                    #solo se toman las características seleccionadas
                    tamanioLista = tamanioDiccionario - 2
                    listaCaracteristicas = listaCaracteristicas[1:tamanioLista]
                    print(listaCaracteristicas)
                    print()

                    #tomo la variable clase y se elimina de las columnas
                    objetoClasificacion = objetoClasificacion.filtrarClase(listaCaracteristicas)
                    objetoClasificacion.variableClase = listaCaracteristicas.pop(0)
                    print(objetoClasificacion.variableClase)

                    mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClasificacion.datosDF)
                    return render(request, 'views/clasificacion/clasificacion.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoClasificacion.datosColumnas,
                        'displaySeleccion':"block",
                        'displayClase':"none",
                        'displayPredictoras':"block",
                        'display':"none",
                    })


            if request.POST["form-tipo"] == 'form-seleccion-predictoras':
                """Con todo esto me di cuenta de que en el form sin seleccionar casillas, se tienen tres elementos unicamente"""
                """
                print()
                print()
                print(len(request.POST))
                print(request.POST)
                print()
                print() """

                #si no se seleccionó alguna caracteristica, se vuelve a preguntar
                if(len(request.POST) <= 3 ):
                    mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClasificacion.datosDF)
                    print()
                    print("Se vuelve a preguntar por las caracteristicas")
                    print()
                    return render(request, 'views/clasificacion/clasificacion.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoClasificacion.datosColumnas,
                        'displaySeleccion':"block",
                        'displayClase':"none",
                        'displayPredictoras':"block",
                        'display':"none",
                    })
                else:
                    print()
                    print("Se procesan las predictoras")
                    print()

                    pantallaClasificacion = True

                    diccionarioCaracteristicas = request.POST
                    listaCaracteristicas = []
                    tamanioDiccionario = len(request.POST)

                    for key in diccionarioCaracteristicas:
                        listaCaracteristicas.append(diccionarioCaracteristicas[key])

                    #solo se toman las características seleccionadas
                    tamanioLista = tamanioDiccionario - 2
                    listaCaracteristicas = listaCaracteristicas[1:tamanioLista]
                    print(listaCaracteristicas)
                    print()


                    #eliminar las características
                    objetoClasificacion = objetoClasificacion.filtrarDatos(listaCaracteristicas)


                    """HASTA ESTE PUNTO, LO ANTERIOR ES LO MISMO QUE EN MÉTRICAS y QUE EN CLUSTERING"""


                    #obtener las variables clase y predictoras
                    objetoClasificacion = objetoClasificacion.variablesClaseyPredictoras()

                    #generar el grafico de dispersion de prueba
                    grafico = graficoDispersionPrueba(objetoClasificacion.predictoras, objetoClasificacion.variableClase)


                    objetoClasificacion = objetoClasificacion.aplicacionAlgoritmoRegresionLineal()
                    
                    
                    #aquí se ha seleccionado alguna característica
                    mapaCalorGenerado = generarMapaMetricas(objetoClasificacion.matrizInf, objetoClasificacion.datosDF)
                    return render(request, 'views/clasificacion/clasificacion.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoClasificacion.datosColumnas,
                        'displaySeleccion':"none",
                        'displayClase':"none",
                        'displayPredictoras':"none",
                        'display':"block",

                        'dataFrameConteoClasificacion': objetoClasificacion.agrupamientoClasificacion,
                        'graficoDispersionPrueba':grafico,
                        'scoreRegresionLineal':objetoClasificacion.scoreClasificacion,
                        'curvaROC': objetoClasificacion.curvaROCRegresionLineal
                    })


                    

            #elif 'form-reporte' in request.POST:
            elif request.POST["form-tipo"] == 'form-reporte':
                """Logica de generacion de reporte"""
                print("Se genera reporte")
                #global lista
                return render(request, 'views/associationRules.html', {
                        'list':lista,
                        'display':'block',
                        'muestraReporte':'block',
                    })
                

            return 0


def eliminarDataSetClasificacion(request):
    global accesoValidadoClasificacion
    if(accesoValidadoClasificacion == True):
        accesoValidadoClasificacion = False

        """#Falta agregar logica de eliminar archivo CSV"""
        #return render(request, 'views/subirApriori.html')
        return HttpResponseRedirect(reverse('index'))
    else:
        #si el acceso ya no es validado, se manda directamente al inicio
        accesoValidadoClasificacion = False
        return render(request, 'views/clustering/subirClasificacion.html')


def graficoDispersionPrueba(datosClase, variableClase):
    global graficoDispersionClasificacionGuardado
    global objetoClasificacion
    arrayDatosClase = np.array(datosClase)

    #se localiza el mejor numero de clusters con kneed
    plt.figure(figsize=(10, 7))
    plt.scatter(arrayDatosClase[:,0], arrayDatosClase[:,1], c = objetoClasificacion.datosDataFrameFiltrados.Diagnosis)
    plt.grid()
    plt.xlabel(objetoClasificacion.datosColumnas[0])
    plt.ylabel(objetoClasificacion.datosColumnas[1])
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    graficoDispersionClasificacionGuardado = graphic

    return graphic

def graficoCurvaROC():

    global graficoCurvaROCGuardado

    CurvaROC = RocCurveDisplay.from_estimator(ClasificacionRL, X_validation, Y_validation, name="Cáncer de mama")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    graficoCurvaROCGuardado = graphic
    return graphic

def getData(request):
    """data = {
        "sales": 100,
        "customers":10,
    }"""
    return 0 
    """
    JsonResponse(data)"""


def about(request):
    return HttpResponse("About")
   

"""def apriori(request):
    if request.method == 'GET':
        return render(request, 'views/associationRules.html')
        #return HttpResponseRedirect(reverse('apriori-algoritmo'))
    else:  
        if(request.POST["soporte"]=="" or request.POST["confianza"]=="" or request.POST["elevacion"]==""):
            return render(request, 'views/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else:
            global variableNombreApriori
            soporte = float(request.POST["soporte"])
            confianza = float(request.POST["confianza"])
            elevacion = float(request.POST["elevacion"])

            global objetoApriori
            objetoApriori = AprioriAlgorithm(variableNombreApriori, soporte, confianza, elevacion)
            objetoApriori = objetoApriori.accionReglasAsoc()
            objetoApriori = objetoApriori.accion()
            #lista = AprioriAlgorithm(variableNombreApriori, soporte, confianza, elevacion)
            lista = objetoApriori.listaResultados

            #lista = [1,2,3,4,5,6,7,8,9,10]
            return render(request, 'views/associationRules.html', {
                'list':lista,
                'display':'block'
            })
"""



"""

def subirApriori(request):
    if request.method == 'GET':
        return render(request, 'views/subirApriori.html')
        #return HttpResponseRedirect(reverse('apriori-subir'))
    else: 
        myfile = request.FILES['archivo']
        fs = FileSystemStorage()

        nombreArchivo = myfile.name
        global variableNombreApriori
        variableNombreApriori = nombreArchivo
        print(nombreArchivo)

        #se pone el directorio completo
        directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/'+nombreArchivo)
        print(directorio)

        #se coloca el directorio y el nombre del archivo
        filename = fs.save(directorio, myfile)
        uploaded_file_url = fs.url(filename)


        global objetoApriori
        objetoApriori = AprioriAlgorithm(variableNombreApriori,0,0,0)
        objetoApriori = objetoApriori.accion()
        #return apriori(request)
        #return render(request, 'views/associationRules.html')
        return HttpResponseRedirect(reverse('apriori-algoritmo'))

"""