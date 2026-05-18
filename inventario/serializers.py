from rest_framework import serializers

from .models import Producto, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categoria
        fields ='__all__'

class ProductoSerializer(serializers.ModelSerializer):
    
    categoria = CategoriaSerializer()
    valor_total = serializers.SerializerMethodField()
    
    class Meta:

        model = Producto

        fields = '__all__'
        
        read_only_fields = ['valor_total']
        
    def get_valor_total(self, obj):
        
        return obj.precio * obj.stock
    
    def validate(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "El Stock no puede ser negativo"
            )
        return value
    
    def validate(self, data):
        
        if data['precio']<=0:
            raise  serializers.ValidationError(
                "El precio debe ser mayor  a 0"
            )
        return data
    

class ProductoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = '__all__'
        
    
class ProductoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = '__all__'
