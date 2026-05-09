from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
# Create your views here.
def lista_productos(request):
    
    productos = Producto.objects.all()
    
    return render(request, 'inventario/lista_productos.html',{
        'productos': productos
    })
    
def crear_producto(request):
    
    if request.method == 'POST':
        
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('lista_productos')
        
    else:
        
        form = ProductoForm()
        
    return render(request, 'inventario/crear_producto.html',{
        'form':form
    })