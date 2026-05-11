from django.shortcuts import render, redirect, get_object_or_404
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
    
def editar_producto(request, id):
        
    producto = get_object_or_404(Producto, id=id)
        
    if request.method == 'POST':
        
        form = ProductoForm(request.POST, instance=producto)
        
        if form.is_valid():
            form.save()
            
            return redirect('lista_productos')
        
    else:
        
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {
        'form': form
    })
    
def eliminar_producto(request, id):
    
    producto = get_object_or_404(Producto, id=id)
    
    producto.delete()
    
    return redirect('lista_productos')
  