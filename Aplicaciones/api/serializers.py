from rest_framework import serializers
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'
        read_only_fields = ('creado', 'actualizado')
        extra_kwargs = {
            'codigo': {'required': False}  
        }
    
    def validate_codigo(self, value):
        # validar solo si se proporciona código
        if value and len(value) != 6:
            raise serializers.ValidationError("El código debe tener exactamente 6 caracteres")
        return value
    
    def validate(self, data):
        # validar que código esté presente solo para creación
        request = self.context.get('request')
        if request and request.method == 'POST':
            if 'codigo' not in data:
                raise serializers.ValidationError({"codigo": "Este campo es requerido para crear una tarea"})
        
        if 'nombre' in data and len(data['nombre']) > 50:
            raise serializers.ValidationError({"nombre": "El nombre no puede tener más de 50 caracteres"})
        
        return data
    
    def create(self, validated_data):
        # para creación: código es requerido
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # para actualización: actualizar solo los campos proporcionados
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()
        return instance