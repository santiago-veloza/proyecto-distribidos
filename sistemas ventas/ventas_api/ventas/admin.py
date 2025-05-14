from django.contrib import admin
from .models import Venta, DetalleVenta

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total')
    search_fields = ('cliente__username',)
    
    list_filter = ('fecha',)
    
    
    
    

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', )
    list_filter = ('producto',)



