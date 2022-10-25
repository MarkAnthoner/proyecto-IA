from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("temasPreferencia/", views.temasPreferencia, name="temas"),
    path("acercaDe/", views.acercaDe, name="acerca"),
    path("sitiosImportantes/", views.sitiosImportantes, name="sitios"),
    path("algoritmoApriori/", views.apriori, name="apriori"),
    path("api/data/", views.getData, name="api-data"),
    path("api/chart/data/", views.ChartData.as_view(), name="api-chart-data"),
    path("about/", views.about, name="about"),
]