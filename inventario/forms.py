from django import forms
from .models import Producto, Movimientos

class ProductoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        
        fields = [
            'nombre',
            'precio',
            'stock',
            'categoria',
            'proveedor'
        ]
class MovimientoForm(forms.ModelForm):
    
    class Meta:
        
        model = Movimientos
        
        fields = [
            'producto',
            'tipo',
            'cantidad'
        ]