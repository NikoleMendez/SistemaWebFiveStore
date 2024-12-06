from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Stock(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True, default='default_name')
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, default=1)  # Valor predeterminado para 'producto'

    def __str__(self):
        return self.name

class Producto(models.Model):
    cod = models.CharField(max_length=25, blank=True, null=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, default=1)



class Permiso(models.Model):
    nombre = models.CharField(max_length=25, blank=True, null=True)
    modulo_administracion = models.BooleanField(default=False)
    modulo_compra = models.BooleanField(default=False)
    modulo_venta = models.BooleanField(default=False)
    modulo_stock = models.BooleanField(default=False)
    modulo_informe = models.BooleanField(default=False)
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=25, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True, default='')
    password = models.CharField(max_length=128)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Proveedor(models.Model):
    nombre = models.CharField(max_length=25, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)

class Cliente(models.Model):
    nombre = models.CharField(max_length=25, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=25, blank=True, null=True)

class Almacen(models.Model):
    fecha = models.DateField(blank=True, null=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, default=1)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField(blank=True, null=True, default=1)
    precioc = models.IntegerField(blank=True, null=True)
    preciov = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Cambiado a DecimalField
    estado = models.BooleanField(default=True)

class Compra(models.Model):
    fecha = models.DateField(blank=True, null=True)
    proveedor = models.ForeignKey('proveedor', on_delete=models.CASCADE, default=1)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField(blank=True, null=True)
    precioc=models.IntegerField(blank=True, null=True) 
    preciov = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    total = models.IntegerField(blank=True, null=True)

class DetalleCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=True, null=True)
    precioc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Detalle de compra {self.id} para la compra {self.compra.id}"

class Venta(models.Model):
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    glosa = models.CharField(max_length=25, blank=True, null=True)
    tipo_pago = models.CharField(max_length=25, blank=True, null=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que realizó la venta

    def __str__(self):
        return f"Venta {self.id} - Cliente {self.cliente.nombre}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=True, null=True)
    preciov = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Detalle de venta {self.id} para la venta {self.venta.id}"

    

class Cotizacion(models.Model):
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    cotizacion = models.CharField(max_length=25, blank=True, null=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=True, null=True)
    preciov = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    total = models.IntegerField(blank=True, null=True)

    

