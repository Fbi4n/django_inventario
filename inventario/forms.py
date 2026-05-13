from django import forms
from .models import Producto, Movimiento

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
        
        model = Movimiento
        
        fields = [
            'producto',
            'tipo',
            'cantidad'
        ]