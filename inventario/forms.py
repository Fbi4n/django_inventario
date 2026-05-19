from django import forms
from .models import Producto, Movimiento

# 1. Creamos un MixIn para reutilizar la lógica de Bootstrap
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Si el campo es un select (ForeignKey o ChoiceField como 'tipo')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select',
                })
            # Para inputs de texto, números, etc.
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Ingrese {field_name.replace("_", " ")}'
                })


# 2. Tus formularios heredan primero del MixIn y luego de ModelForm
class ProductoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'precio',
            'stock',
            'categoria',
            'proveedor'
        ]


class MovimientoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'producto',
            'tipo',
            'cantidad'
        ]