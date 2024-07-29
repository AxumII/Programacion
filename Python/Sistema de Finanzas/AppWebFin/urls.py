from django.urls import path
from . import views

urlpatterns = [
    path('', views.tablaProductos, name='prueba'),
    path('guardado/', views.guardarProductos, name="guardado"), 
    # Otras URLS de tu aplicación, si las tienes.
]