from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'rol')
    search_fields = ('username', 'rol')
    list_filter = ('rol',)
