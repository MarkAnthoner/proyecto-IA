from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("acercaDe/", views.acercaDe, name="acerca"),
    path("sitiosImportantes/", views.sitiosImportantes, name="sitios"),


    path("apriori/algoritmo", views.validacionApriori, name="apriori-validacion"),
    path("apriori/algoritmo-eliminar", views.eliminarDataSetApriori, name="apriori-eliminar-dataset"),


    path("metricas/algoritmo", views.validacionMetricasDistancia, name="metricas-distancia-validacion"),
    path("metricas/algoritmo-eliminar", views.eliminarDataSetMetricas, name="metricas-eliminar-dataset"),


    path("clustering/algoritmo", views.validacionClustering, name="clustering-validacion"),
    path("clustering/algoritmo-eliminar", views.eliminarDataSetClustering, name="clustering-eliminar-dataset"),


    path("clasificacion/algoritmo", views.validacionClasificacion, name="clasificacion-validacion"),
    path("clasificacion/algoritmo-eliminar", views.eliminarDataSetClasificacion, name="clasificacion-eliminar-dataset"),


    path("arbolYbosque/algoritmo", views.validacionArbolYbosque, name="arbolYbosque-validacion"),
    path("arbolYbosque/algoritmo-eliminar-arbol-pronostico", views.eliminarDataSetArbolPronostico, name="arbolYbosque-eliminar-dataset-arbol-pronostico"),
    path("arbolYbosque/algoritmo-eliminar-bosque-pronostico", views.eliminarDataSetBosquePronostico, name="arbolYbosque-eliminar-dataset-bosque-pronostico"),
    path("arbolYbosque/algoritmo-eliminar-arbol-clasificacion", views.eliminarDataSetArbolClasificacion, name="arbolYbosque-eliminar-dataset-arbol-clasificacion"),
    path("arbolYbosque/algoritmo-eliminar-bosque-clasificacion", views.eliminarDataSetBosqueClasificacion, name="arbolYbosque-eliminar-dataset-bosque-clasificacion"),



    #path("apriori/algoritmo", views.apriori, name="apriori-algoritmo"),
    #path("apriori/subir", views.subirApriori, name="apriori-subir"),


    path("api/data/", views.getData, name="api-data"),
    path("api/chart/data/", views.ChartData.as_view(), name="api-chart-data"),
    path("about/", views.about, name="about"),
]




#path("algoritmoApriori/", views.validacionApriori, name="apriori"),