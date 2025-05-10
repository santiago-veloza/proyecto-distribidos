from django.db import models
from usuarios.models import Usuario
from productos.models import Producto

class Venta(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.cliente.username}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Venta #{self.venta.id} - Producto: {self.producto.nombre}"

class Factura(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Factura de Venta #{self.venta.id}"

