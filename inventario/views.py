from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Movimientos
from .forms import ProductoForm, MovimientoForm


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
  
def crear_movimiento(request):
    
    if request.method == 'POST':
        
        form = MovimientoForm(request.POST)
        
        if form.is_valid():
            
            movimiento = form.save(commit=False)
            
            producto = movimiento.producto
            
            if movimiento.tipo == 'ENTRADA':
                
                producto.stock += movimiento.cantidad
                
            elif movimiento.tipo == 'SALIDA':
                
                if producto.stock < movimiento.cantidad:
                    
                    form.add_error(
                        'cantidad',
                        'Stock insuficiente'
                    )
                    
                    return render(
                        request,
                        'inventario/crear_movimiento.html',
                        {'form': form}
                    )
                
                producto.stock -= movimiento.cantidad
            
            producto.save()
            
            movimiento.save()
            
            return redirect('lista_productos')
        
    else:
        
        form = MovimientoForm()
            
    return render(request,
                      'inventario/crear_movimiento.html',
                      {'form': form})
        
