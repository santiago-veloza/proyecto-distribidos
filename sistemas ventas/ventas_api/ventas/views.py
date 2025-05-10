from django.shortcuts import render
from rest_framework import viewsets
from .models import Venta, DetalleVenta, Factura, Producto
from rest_framework.exceptions import ValidationError
from .serializers import VentaSerializer, DetalleVentaSerializer, FacturaSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    @swagger_auto_schema(tags=["Ventas"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Ventas"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Ventas"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "mensaje": "✅ Venta registrada exitosamente.",
            "venta": {
                "id": serializer.data["id"],
                "fecha": serializer.data["fecha"],
                "usuario": serializer.data["usuario"]
            }
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Ventas"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Ventas"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Ventas"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

# DetalleVenta
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

    @swagger_auto_schema(tags=["Detalle de Venta"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Detalle de Venta"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Detalle de Venta"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Detalle de Venta"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Detalle de Venta"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Detalle de Venta"])
    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('producto')
        cantidad = int(request.data.get('cantidad', 0))

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise ValidationError("❌ Producto no encontrado.")

        if producto.stock < cantidad:
            raise ValidationError(f"❌ Stock insuficiente. Solo hay {producto.stock} unidades disponibles.")

        producto.stock -= cantidad
        producto.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "mensaje": "🧾 Detalle de venta creado exitosamente.",
            "detalle": {
                "id": serializer.data["id"],
                "venta": serializer.data["venta"],
                "producto": serializer.data["producto"],
                "cantidad": serializer.data["cantidad"],
            }
        }, status=status.HTTP_201_CREATED)


# Facturas
class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    @swagger_auto_schema(tags=["Facturas"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Facturas"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Facturas"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Facturas"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Facturas"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Facturas"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "mensaje": "📄 Factura emitida correctamente.",
            "factura": {
                "id": serializer.data["id"],
                "venta": serializer.data["venta"],
                "fecha_emision": serializer.data["fecha_emision"],
                "total": serializer.data["total"]
            }
        }, status=status.HTTP_201_CREATED)