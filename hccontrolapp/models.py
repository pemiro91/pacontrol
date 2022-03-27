import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

TIPO_PAGO = (
    ('En Efectivo', 'En_Efectivo'),
    ('Transferencia', 'Transferencia'),
    ('Por encargo', 'Por_Encargo'),
    ('Cuenta Casa', 'Cuenta_Casa')
)


class User(AbstractUser):
    sexo = models.BooleanField(default=False)
    is_dependiente = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=False)


class Categoria_Producto(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(max_length=50, name='descripcion')

    def __str__(self):
        return self.nombre_categoria


class Establecimiento(models.Model):
    nombre_establecimiento = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(max_length=50, name='descripcion')

    def __str__(self):
        return self.nombre_establecimiento


class Producto(models.Model):
    imagen = models.ImageField(upload_to='producto/', null=True, blank=True)
    nombre_producto = models.CharField(max_length=100, name='nombre_producto')
    cantidad_existente = models.IntegerField()
    costo = models.FloatField(max_length=100, name='costo')
    precio_venta = models.FloatField(max_length=100, name='precio_venta')
    categoria_producto = models.ForeignKey(Categoria_Producto, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
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

    @classmethod
    def get_total_gasto(cls):
        return sum([gasto.monto_gasto for gasto in cls.objects.filter(fecha_gasto__day=date.today().day,
                                                                      fecha_gasto__month=date.today().month,
                                                                      fecha_gasto__year=date.today().year)])


class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, name='usuario')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad = models.IntegerField()
    tipo_pago = models.CharField(max_length=50, choices=TIPO_PAGO, name='tipo_pago')
    venta_total = models.FloatField(max_length=100)
    costo = models.FloatField(max_length=100, null=True, blank=True)
    deudor = models.CharField(max_length=50, name='deudor', null=True, blank=True)
    fecha_venta = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.producto)

    @classmethod
    def get_total_count(cls):
        return sum([sale.cantidad for sale in cls.objects.filter(fecha_venta__day=date.today().day,
                                                                 fecha_venta__month=date.today().month,
                                                                 fecha_venta__year=date.today().year)])

    @classmethod
    def get_total_sales(cls):
        return sum([
            sale.cantidad * sale.producto.precio_venta for sale in
            cls.objects.filter(fecha_venta__day=date.today().day,
                               fecha_venta__month=date.today().month,
                               fecha_venta__year=date.today().year).exclude(tipo_pago='home_account')
        ])

    @classmethod
    def get_total_sales_costo(cls):
        return sum([
            sale.cantidad * sale.producto.costo for sale in cls.objects.filter(fecha_venta__day=date.today().day,
                                                                               fecha_venta__month=date.today().month,
                                                                               fecha_venta__year=date.today().year)
        ])

    @classmethod
    def get_total_sales_home(cls):
        return sum([
            sale.cantidad * sale.producto.precio_venta for sale in cls.objects.filter(tipo_pago="home_account",
                                                                                      fecha_venta__day=date.today().day,
                                                                                      fecha_venta__month=date.today().month,
                                                                                      fecha_venta__year=date.today().year)
        ])


class Venta_Diaria(models.Model):
    fecha_venta = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    venta_total = models.IntegerField()
    costo = models.FloatField(max_length=100)
    ganancia_bruta = models.FloatField(max_length=100)
    gasto = models.FloatField(max_length=100)
    ganancia_neta = models.FloatField(max_length=100)

    def str(self):
        return str(self.fecha_venta)


class Entrada(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad_producto_entrada = models.IntegerField()
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.producto.nombre_producto)


class Merma(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad_producto_merma = models.IntegerField()
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.producto.nombre_producto)

    @classmethod
    def get_total_merma(cls):
        return sum([merma.cantidad_producto_merma * merma.producto.precio_venta
                    for merma in cls.objects.filter(fecha__day=date.today().day,
                                                    fecha__month=date.today().month,
                                                    fecha__year=date.today().year)])



