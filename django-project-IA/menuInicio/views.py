from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import AprioriAlgorithm

#Vistas del framework API Rest
from rest_framework.views import APIView
from rest_framework.response import Response

#import para validar numeros
import numbers

# Create your views here.

#Es necesario instalar la App menuInicio en el archivo settings del proyecto
def index(request):
    return render(request, 'index.html')

def temasPreferencia(request):
    return render(request, 'views/temasPreferencia.html')

def sitiosImportantes(request):
    return render(request, 'views/sitiosImportantes.html')

def acercaDe(request):
    return render(request, 'views/acercaDe.html')

def apriori(request):
    if request.method == 'GET':
        return render(request, 'views/associationRules.html')
    else:  
        if(request.POST["soporte"]=="" or request.POST["confianza"]=="" or request.POST["elevacion"]==""):
            return render(request, 'views/associationRules.html')
        else:
            soporte = float(request.POST["soporte"])
            confianza = float(request.POST["confianza"])
            elevacion = float(request.POST["elevacion"])
            aprioriData = AprioriAlgorithm()
            lista = aprioriData.listaResultadosApriori(soporte, confianza, elevacion)

            #lista = [1,2,3,4,5,6,7,8,9,10]
            return render(request, 'views/associationRules.html', {
                'list':lista,
                'display':'block'
            })


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



"""Uso de Rest framework para trabajar con los datos"""
class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None): 
        """data = {
            "sales": 200,
            "customers":20,
        }"""
        aprioriData = AprioriAlgorithm()
        items = aprioriData.retornaItems()
        frecuencia = aprioriData.retornaFrecuencia()
        cuenta = aprioriData.retornaCuenta()
        data = {
            "items": items,
            "frecuencia":frecuencia,
            "cuenta": cuenta,
        }
        return Response(data)
