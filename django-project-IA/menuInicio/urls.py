from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("temasPreferencia/", views.temasPreferencia, name="temas"),
    path("acercaDe/", views.acercaDe, name="acerca"),
    path("sitiosImportantes/", views.sitiosImportantes, name="sitios"),


    path("apriori/algoritmo", views.validacionApriori, name="apriori-validacion"),
    path("apriori/algoritmo-eliminar", views.eliminarDataSetApriori, name="apriori-eliminar-dataset"),


    #path("apriori/algoritmo", views.apriori, name="apriori-algoritmo"),
    #path("apriori/subir", views.subirApriori, name="apriori-subir"),


    path("api/data/", views.getData, name="api-data"),
    path("api/chart/data/", views.ChartData.as_view(), name="api-chart-data"),
    path("about/", views.about, name="about"),
]




#path("algoritmoApriori/", views.validacionApriori, name="apriori"),