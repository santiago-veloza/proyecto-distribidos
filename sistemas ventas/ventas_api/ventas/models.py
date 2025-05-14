from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto

class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.cliente.username}"

    def calcular_total(self):
        return sum(detalle.producto.precio * detalle.cantidad for detalle in self.detalles.all())

    def save(self, *args, **kwargs):
        # Guardar la venta primero si es nueva (para que tenga ID)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Si no es nueva, recalcular el total (después de que existan los detalles)
        if not is_new:
            self.total = self.calcular_total()
            super().save(update_fields=['total'])

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Detalle de Venta #{self.venta.id} - Producto: {self.producto.nombre}"
