import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    sexo = models.BooleanField(default=False)
    is_dependiente = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=False)


class Categoria_Producto(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(max_length=50, name='descripcion')

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    imagen = models.ImageField(upload_to='producto/', null=True, blank=True)
    nombre_producto = models.CharField(max_length=100, name='nombre_producto')
    cantidad_existente = models.IntegerField()
    costo = models.FloatField(max_length=100, name='costo')
    precio_venta = models.FloatField(max_length=100, name='precio_venta')
    inversion = models.FloatField(max_length=100, name='inversion')
    cantidad_vendida = models.IntegerField()
    ganancia = models.FloatField(max_length=100, name='ganancia')
    cantidad_a_vender = models.IntegerField()
    categoria_producto = models.ForeignKey(Categoria_Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return self.nombre_producto


class Gastos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, name='usuario')
    concepto = models.CharField(max_length=200)
    monto_gasto = models.FloatField(max_length=100)
    fecha_gasto = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.concepto)


class Reporte_Ampliado(models.Model):
    nombre = models.CharField(max_length=200)
    cantidad_existente = models.IntegerField()
    costo_produccion = models.FloatField(max_length=100)
    precio_venta = models.FloatField(max_length=100)
    inversion = models.FloatField(max_length=100)
    cantidad_vendido = models.FloatField(max_length=100)
    ganancia = models.FloatField(max_length=100)

    def str(self):
        return str(self.nombre)


class Venta_Diaria(models.Model):
    fecha_venta = models.DateTimeField(datetime.datetime.now())
    cantidad = models.IntegerField()
    venta_total = models.IntegerField()
    a_cobrar = models.IntegerField()
    inversion = models.FloatField(max_length=100)
    ganancia = models.FloatField(max_length=100)
    gasto = models.FloatField(max_length=100)
    ganancia_real = models.FloatField(max_length=100)

    def str(self):
        return str(self.fecha_venta)


class Merma(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad_producto_merma = models.IntegerField()
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.producto.nombre_producto)
