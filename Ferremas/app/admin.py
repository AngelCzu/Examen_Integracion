from django.contrib import admin
from . import models
admin.site.register(models.User)
admin.site.register(models.Categoria)
admin.site.register(models.Subcategoria)
admin.site.register(models.Producto)

# Register your models here.
