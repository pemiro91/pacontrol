import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils.text import slugify


# Create your models here.

TIPO_PAGO = (
    ('En Efectivo', 'En_Efectivo'),
    ('Transferencia', 'Transferencia'),
    ('Por encargo', 'Por_Encargo'),
    ('Cuenta Casa', 'Cuenta_Casa')
)

UM = (
    ('Centimetros', 'centimetros'),
    ('Unidad', 'unidad')
)

# CHOICES_ROL = (
#     ('dependiente', 'Dependiente'),
#     ('administrador', 'Administrador')
# )
#
# CHOICES_SEXO = (
#     ('masculino', 'Masculino'),
#     ('femenino', 'Femenino')
# )


def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):

    from django.template.defaultfilters import slugify
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    import re
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


class User(AbstractUser):
    carnet = models.CharField(max_length=12)
    sexo = models.BooleanField(default=False)
    rol = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name


class Categoria_Producto(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(max_length=50, name='descripcion')
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_categoria)
        super(Categoria_Producto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_categoria


class Establecimiento(models.Model):
    nombre_establecimiento = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=50, name='descripcion')
    user = models.ManyToManyField(User)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_establecimiento)
        super(Establecimiento, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_establecimiento

    def get_absolute_url(self):
        return reverse("productos_establecimientos", kwargs={"slug": self.slug})


class Producto(models.Model):
    imagen = models.ImageField(upload_to='producto/', null=True, blank=True)
    nombre_producto = models.CharField(max_length=100, name='nombre_producto')
    cantidad_existente = models.IntegerField()
    costo = models.FloatField(max_length=100, name='costo')
    precio_venta = models.FloatField(max_length=100, name='precio_venta')
    categoria_producto = models.ForeignKey(Categoria_Producto, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        slug_str = "%s %s" % (self.nombre_producto, self.establecimiento.nombre_establecimiento)
        unique_slugify(self, slug_str)
        super(Producto, self).save(**kwargs)

    def __str__(self):
        return self.nombre_producto


class Traslado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, related_name='establecimiento')
    establecimiento_padre = models.ForeignKey(Establecimiento,
                                              on_delete=models.CASCADE, related_name='establecimiento_padre')
    cantidad_trasladar = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return self.establecimiento.nombre_establecimiento


class Gastos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, name='usuario')
    concepto = models.CharField(max_length=200)
    monto_gasto = models.FloatField(max_length=100)
    fecha_gasto = models.DateTimeField(datetime.datetime.now())
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)

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
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fecha_venta)
        super(Venta, self).save(*args, **kwargs)

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
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fecha_venta)
        super(Venta_Diaria, self).save(*args, **kwargs)

    def str(self):
        return str(self.fecha_venta)


class Entrada(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad_producto_entrada = models.IntegerField()
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.producto.nombre_producto)


class Merma(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad_producto_merma = models.IntegerField()
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.producto.nombre_producto)

    @classmethod
    def get_total_merma(cls):
        return sum([merma.cantidad_producto_merma * merma.producto.precio_venta
                    for merma in cls.objects.filter(fecha__day=date.today().day,
                                                    fecha__month=date.today().month,
                                                    fecha__year=date.today().year)])


class Material(models.Model):
    imagen = models.ImageField(upload_to='material/', null=True, blank=True)
    nombre_material = models.CharField(max_length=100, name='nombre_material')
    cantidad = models.IntegerField()
    costo = models.FloatField(max_length=100, name='costo')
    unidad_medida = models.CharField(max_length=50, choices=UM, name='unidad_medida')
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_material)
        super(Material, self).save(*args, **kwargs)


class Entrada_Material(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, name='material')
    cantidad_material_entrada = models.IntegerField()
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.material.nombre_material)


class Merma_Material(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, name='material')
    cantidad_material_merma = models.IntegerField()
    fecha = models.DateTimeField(datetime.datetime.now())

    def str(self):
        return str(self.material.nombre_material)

    @classmethod
    def get_total_merma(cls):
        return sum([merma.cantidad_material_merma * merma.producto.costo
                    for merma in cls.objects.filter(fecha__day=date.today().day,
                                                    fecha__month=date.today().month,
                                                    fecha__year=date.today().year)])
