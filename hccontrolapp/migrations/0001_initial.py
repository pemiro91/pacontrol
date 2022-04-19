# Generated by Django 4.0.2 on 2022-04-19 15:48

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
                ('carnet', models.CharField(blank=True, max_length=12, null=True)),
                ('sexo', models.BooleanField(default=False)),
                ('rol', models.BooleanField(default=False)),
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
                ('nombre_establecimiento', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='material/')),
                ('nombre_material', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('costo', models.FloatField(max_length=100)),
                ('unidad_medida', models.CharField(choices=[('Centimetros', 'centimetros'), ('Unidad', 'unidad')], max_length=50)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
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
                ('precio_venta', models.FloatField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(null=True)),
                ('categoria_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.categoria_producto')),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Venta_Diaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('venta_total', models.IntegerField()),
                ('costo', models.FloatField(max_length=100)),
                ('ganancia_bruta', models.FloatField(max_length=100)),
                ('gasto', models.FloatField(max_length=100)),
                ('ganancia_neta', models.FloatField(max_length=100)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('tipo_pago', models.CharField(choices=[('En Efectivo', 'En_Efectivo'), ('Transferencia', 'Transferencia'), ('Por encargo', 'Por_Encargo'), ('Cuenta Casa', 'Cuenta_Casa')], max_length=50)),
                ('venta_total', models.FloatField(max_length=100)),
                ('costo', models.FloatField(blank=True, max_length=100, null=True)),
                ('deudor', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_venta', models.DateTimeField(verbose_name=datetime.datetime(2022, 4, 19, 11, 48, 58, 430875))),
                ('slug', models.SlugField(null=True, unique=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
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
                ('establecimiento_padre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='establecimiento_padre', to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merma_Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_material_merma', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 4, 19, 11, 48, 58, 433880))),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='Merma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto_merma', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 4, 19, 11, 48, 58, 432877))),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concepto', models.CharField(max_length=200)),
                ('monto_gasto', models.FloatField(max_length=100)),
                ('fecha_gasto', models.DateTimeField(verbose_name=datetime.datetime(2022, 4, 19, 11, 48, 58, 430875))),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entrada_Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_material_entrada', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 4, 19, 11, 48, 58, 432877))),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto_entrada', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2022, 4, 19, 11, 48, 58, 431872))),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.establecimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hccontrolapp.producto')),
            ],
        ),
    ]
