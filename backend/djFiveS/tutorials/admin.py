from django.contrib import admin
from tutorials.models import Stock
from tutorials.models import Producto

# Register your models here.
admin.site.register(Producto)
admin.site.register(Stock)