from django.urls import path
from .views import lista_productos, crear_producto

urlpatterns = [
    path('productos/', lista_productos, name='lista_productos'),
    path('producto/crear/', crear_producto, name='crear_producto'),
]