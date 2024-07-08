from django.db import models
from django.contrib.auth.models import AbstractUser

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        txt = "Categoria: {0} "
        return txt.format(self.nombre)
    
class Subcategoria(models.Model):
    id_subcategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)

    def __str__(self):
        txt = "{0} - Subcategoría: {1}"
        return txt.format(self.categoria, self.nombre)

class Producto(models.Model):
    sku = models.IntegerField(primary_key=True)
    precio = models.IntegerField()
    stock = models.IntegerField()
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="imagenesProducto")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(auto_now_add=True)
    disponible = models.BooleanField(default=True)

    def decrementar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            if (self.stock == 0):
                self.disponible = False
            self.save()
        else:
            raise ValueError("No hay suficiente stock para decrementar.")

    def __str__(self):
        txt = "Sku: {0} | Nombre: {1} | Stock: {2} | Precio: {3} | Disponible: {4}"
        return txt.format( self.sku, self.nombre , self.stock, self.precio, self.disponible)

class User(AbstractUser):
    NIVELES_USUARIO = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente')
    ]
    
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=12, null=False)
    direccion = models.CharField(max_length=100, null=False)
    nivel = models.CharField(max_length=10, choices=NIVELES_USUARIO, default='cliente')
    
    def __str__(self):
        txt = "{0} - [{1}]"
        return txt.format(self.username, self.nivel )

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} - {self.cantidad}"