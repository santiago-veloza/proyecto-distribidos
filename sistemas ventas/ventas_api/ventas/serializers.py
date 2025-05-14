from rest_framework import serializers
from .models import Venta, DetalleVenta
from productos.models import Producto

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        exclude = ['venta']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, write_only=True)
    detalles_creados = DetalleVentaSerializer(source='detalles', many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'fecha', 'total', 'detalles', 'detalles_creados']
        read_only_fields = ['id', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        if not detalles_data:
            raise serializers.ValidationError("❌ Debe agregar al menos un producto en la venta.")

        venta = Venta.objects.create(**validated_data)

        for detalle in detalles_data:
            producto = detalle['producto']
            cantidad = detalle['cantidad']

            if producto.stock < cantidad:
                raise serializers.ValidationError(
                    f"❌ Stock insuficiente para '{producto.nombre}'. Solo hay {producto.stock} disponibles."
                )

            producto.stock -= cantidad
            producto.save()
            DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad)

        venta.total = venta.calcular_total()
        venta.save(update_fields=['total'])

        return venta
