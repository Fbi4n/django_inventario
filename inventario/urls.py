from django.urls import path
from .views import lista_productos, crear_producto, editar_producto, eliminar_producto

urlpatterns = [
    path('productos/', lista_productos, name='lista_productos'),
    path('producto/crear/', crear_producto, name='crear_producto'),
    path('productos/<int:id>/editar/', editar_producto, name='editar_producto'),
    path('productos/<int:id>/eliminar/', eliminar_producto, name='eliminar_producto')
]