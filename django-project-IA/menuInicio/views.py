from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .apriori import AprioriAlgorithm


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import resolve

#import de apriori
from .apriori import AprioriAlgorithm


#Vistas del framework API Rest
from rest_framework.views import APIView
from rest_framework.response import Response

#import para validar numeros
import numbers

#importar para archivos
import os

#importar archivos
from django.core.files.storage import FileSystemStorage

# Create your views here.



variableNombreApriori = ""
objetoApriori = AprioriAlgorithm(variableNombreApriori,0,0,0)

accesoValidado = False
lista = []



#Es necesario instalar la App menuInicio en el archivo settings del proyecto
def index(request):
    return render(request, 'index.html')

def temasPreferencia(request):
    return render(request, 'views/temasPreferencia.html')

def sitiosImportantes(request):
    return render(request, 'views/sitiosImportantes.html')

def acercaDe(request):
    return render(request, 'views/acercaDe.html')


def validacionApriori(request):

    global accesoValidado
    global variableNombreApriori
    global objetoApriori

    global lista

    if(accesoValidado == False):
        #no se ha validado el dataset, entonces se redirige a la vista de subir archivo
        if request.method == 'GET':
            accesoValidado = False
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
            #print(directorio)

            #se coloca el directorio y el nombre del archivo
            filename = fs.save(directorio, myfile)
            uploaded_file_url = fs.url(filename)


            global objetoApriori
            objetoApriori = AprioriAlgorithm(variableNombreApriori,0,0,0)
            objetoApriori = objetoApriori.accion()

            accesoValidado = True

            #return apriori(request)
            return render(request, 'views/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
    else:


        if request.method == 'GET':
            return render(request, 'views/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else: 
            #if 'form-ejecucion' in request.POST:
            if request.POST["form-tipo"] == 'form-ejecucion':
                if(request.POST["soporte"]=="" or request.POST["confianza"]=="" or request.POST["elevacion"]==""):
                    return render(request, 'views/associationRules.html')
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

            accesoValidado = True
            return render(request, 'views/associationRules.html')
            #return HttpResponseRedirect(reverse('apriori-algoritmo'))
        else:
            #return HttpResponseRedirect(resolve('views/subirApriori.html'))
            #return HttpResponseRedirect(reverse('apriori-subir'))
            return render(request, 'views/subirApriori.html')
            #return render(request, 'views/subirApriori.html')
 


def eliminarDataSetApriori(request):
    global accesoValidado
    global lista
    if(accesoValidado == True):
        accesoValidado = False
        lista = []

        """#Falta agregar logica de eliminar archivo CSV"""
        #return render(request, 'views/subirApriori.html')
        return HttpResponseRedirect(reverse('index'))
    else:
        #si el acceso ya no es validado, se manda directamente al inicio
        accesoValidado = False
        return render(request, 'views/subirApriori.html')



"""Uso de Rest framework para trabajar con los datos"""
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