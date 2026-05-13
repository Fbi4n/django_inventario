from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Movimiento, Categoria
from .forms import ProductoForm, MovimientoForm
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
@login_required
def lista_productos(request):

    productos_lista = Producto.objects.select_related(
        'categoria',
        'proveedor'
    )

    busqueda = request.GET.get('buscar')

    if busqueda:

        productos_lista = productos_lista.filter(

            Q(nombre__icontains=busqueda)
            |
            Q(categoria__nombre__icontains=busqueda)

        )

    paginator = Paginator(
        productos_lista,
        5
    )

    page_number = request.GET.get('page')

    productos = paginator.get_page(page_number)

    return render(
        request,
        'inventario/lista_productos.html',
        {
            'productos': productos
        }
    )
    
#--------------------------------------------------------------------#
@login_required   
def crear_producto(request):
    
    if request.method == 'POST':
        
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Producto creado correctamente'
            )
            
            return redirect('lista_productos')
        
    else:
        
        form = ProductoForm()
        
    return render(request, 'inventario/crear_producto.html',{
        'form':form
    })
    
#--------------------------------------------------------------------#
@login_required   
def editar_producto(request, id):
        
    producto = get_object_or_404(Producto, id=id)
        
    if request.method == 'POST':
        
        form = ProductoForm(request.POST, instance=producto)
        
        if form.is_valid():
            form.save()
            messages.info(
                request,
                'Producto editado correctamente'
            )
            
            return redirect('lista_productos')
        
    else:
        
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {
        'form': form
    })
    
#--------------------------------------------------------------------#
@login_required    
def eliminar_producto(request, id):
    
    producto = get_object_or_404(Producto, id=id)
    
    producto.delete()
    messages.error(
        request,
        'Producto eliminado correctamente'
        )
    
    return redirect('lista_productos')

#--------------------------------------------------------------------#
@login_required  
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
        


#--------------------------------------------------------------------#
@login_required
def dashboard(request):

    total_productos= Producto.objects.count()
    
    total_categorias = Categoria.objects.count()
    
    productos_sin_stock = Producto.objects.filter(stock__lte=0).count()
    
    total_stock = Producto.objects.aggregate(
        Sum('stock')
    )['stock__sum']
    
    ultimos_movimientos = Movimiento.objects.order_by('-fecha')[:5]
    
    context = {
        'total_productos': total_productos,
        
        'total_categorias': total_categorias,
        
        'productos_sin_stock': productos_sin_stock,
        
        'total_stock': total_stock,
        
        'ultimos_movimientos': ultimos_movimientos
    }
    
    return render(request,'inventario/dashboard.html', context)

#--------------------------------------------------------------------#
@login_required
def api_productos(request):
    
    productos = Producto.objects.all()
    
    data = []
    
    for producto in productos:
        data.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'stock': producto.stock,
            'categoria': producto.categoria.nombre,
        })
    return JsonResponse(data, safe=False)

#--------------------------------------------------------------------#
@login_required
def productos_ajax(request):
    
    return render(
        request,
        'inventario/productos_ajax.html'
    )