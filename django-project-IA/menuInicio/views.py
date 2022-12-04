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
            directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/'+nombreArchivo)
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
            directorio = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datos/'+nombreArchivo)

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

                    diccionarioCaracteristicas = request.POST
                    listaCaracteristicas = []
                    tamanioDiccionario = len(request.POST)

                    for key in diccionarioCaracteristicas:
                        listaCaracteristicas.append(diccionarioCaracteristicas[key])

                    tamanioLista = tamanioDiccionario - 2
                    listaCaracteristicas = listaCaracteristicas[1:tamanioLista]
                    print(listaCaracteristicas)
                    print()

                    #eliminar las características
                    objetoMetricas = objetoMetricas.filtrarDatos(listaCaracteristicas)
                    objetoMetricas = objetoMetricas.mostrarMatrizEuclidiana()
                    
                    #aquí se ha seleccionado alguna característica
                    mapaCalorGenerado = generarMapaMetricas(objetoMetricas.matrizInf, objetoMetricas.datosDF)
                    return render(request, 'views/metricas/metricasDistancia.html', {
                        'mapaCalor':mapaCalorGenerado,
                        'listaColumnas':objetoMetricas.datosColumnas,
                        'displaySeleccion':"none",
                        'display':"block",
                        'dataFrame':objetoMetricas.datosMatrizEuclidiana,
                    })



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
                    return render(request, 'views/associationRules.html', {
                        'list':lista,
                        'display':'block'
                    })
            #elif 'form-reporte' in request.POST:
            elif request.POST["form-tipo"] == 'form-reporte':
                """Logica de generacion de reporte"""
                print("Se genera reporte")
                #global lista
                return render(request, 'views/associationRules.html', {
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
            return render(request, 'views/metricasDistancia.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else:
            #return HttpResponseRedirect(resolve('views/subirApriori.html'))
            #return HttpResponseRedirect(reverse('apriori-subir'))
            return render(request, 'views/subirMetricas.html')
    return render(request, 'index.html')

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