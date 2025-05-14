from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'precio')  # 👀 Muestra columnas en el listado
    search_fields = ('nombre',)
    list_filter = ('nombre',)
