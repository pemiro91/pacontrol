# Generated by Django 4.0.2 on 2022-10-21 20:27

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('carnet', models.CharField(max_length=12)),
                ('sexo', models.BooleanField(default=False)),
                ('rol', models.BooleanField(default=False)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Auditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('cellphone', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('carnet', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=250)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria_Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=50)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_establecimiento', models.CharField(default='Almacen', max_length=50)),
                ('descripcion', models.TextField(default='Almacen de productos', max_length=50)),
                ('slug', models.SlugField(default='almacen', unique=True)),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ficha_Tecnica_Nombre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ficha', models.CharField(max_length=50)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='material/')),
                ('nombre_material', models.CharField(max_length=100)),
                ('cantidad', models.FloatField(blank=True, null=True)),
                ('costo', models.FloatField(max_length=100)),
                ('unidad_medida', models.CharField(max_length=50)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda', models.CharField(blank=True, max_length=50, null=True)),
                ('tasa', models.IntegerField(blank=True, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='producto/')),
                ('nombre_producto', models.CharField(max_length=100)),
                ('cantidad_existente', models.IntegerField()),
                ('costo', models.FloatField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('categoria_producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.categoria_producto')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoEstablecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_existente', models.IntegerField()),
                ('precio_venta', models.FloatField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Venta_Diaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateField(auto_now_add=True, null=True)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('venta_total', models.IntegerField(blank=True, null=True)),
                ('costo', models.FloatField(blank=True, max_length=100, null=True)),
                ('ganancia_bruta', models.FloatField(blank=True, max_length=100, null=True)),
                ('gasto', models.FloatField(blank=True, max_length=100, null=True)),
                ('ganancia_neta', models.FloatField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('tipo_pago', models.CharField(choices=[('En Efectivo', 'En_Efectivo'), ('Transferencia', 'Transferencia'), ('Por encargo', 'Por_Encargo'), ('Cuenta Casa', 'Cuenta_Casa')], max_length=50)),
                ('venta_total', models.FloatField(blank=True, max_length=100, null=True)),
                ('costo', models.FloatField(blank=True, max_length=100, null=True)),
                ('deudor', models.CharField(blank=True, max_length=50, null=True)),
                ('restante', models.FloatField(blank=True, max_length=100, null=True)),
                ('fecha_venta', models.DateField(auto_now_add=True, null=True)),
                ('fecha_modificada', models.DateField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.productoestablecimiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Traslado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_trasladar', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='establecimiento', to='hccontrolapp.establecimiento')),
                ('establecimiento_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establecimiento_padre', to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merma_Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_material_merma', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 21, 16, 27, 16, 390682))),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='Merma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto_merma', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 21, 16, 27, 16, 390682))),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concepto', models.CharField(max_length=200)),
                ('monto_gasto', models.FloatField(max_length=100)),
                ('fecha_gasto', models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 21, 16, 27, 16, 390682))),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ficha_Tecnica_Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_material', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.material')),
                ('nombre_ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.ficha_tecnica_nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Ficha_Tecnica_Gastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gasto_directo', models.FloatField()),
                ('gasto_indirecto', models.FloatField()),
                ('impuesto', models.FloatField()),
                ('nombre_ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.ficha_tecnica_nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Ficha_Tecnica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ficha_gasto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.ficha_tecnica_gastos')),
                ('materiales', models.ManyToManyField(blank=True, to='hccontrolapp.Ficha_Tecnica_Material')),
                ('nombre_ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.ficha_tecnica_nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada_Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_material_entrada', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 21, 16, 27, 16, 390682))),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto_entrada', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 21, 16, 27, 16, 390682))),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Auditoria_Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_material', models.FloatField(blank=True, null=True)),
                ('auditoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.auditoria')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='Auditoria_Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(blank=True, max_length=250, null=True)),
                ('cantidad_producto', models.FloatField(blank=True, null=True)),
                ('fecha_entrega', models.DateField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('auditoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.auditoria')),
            ],
        ),
    ]
