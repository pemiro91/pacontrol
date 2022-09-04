from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from datetime import date, datetime, timedelta
from hccontrolapp.models import Categoria_Producto, Producto, ProductoEstablecimiento, \
    Merma, Gastos, Venta, Venta_Diaria, Entrada, Ficha_Tecnica_Nombre, Ficha_Tecnica_Material, Ficha_Tecnica_Gastos, \
    Ficha_Tecnica, Establecimiento, Traslado, User, Material, Moneda, Merma_Material, Entrada_Material
from hccontrolapp.form import ProductoForm, TrasladoForm, TrasladoEstablecimientoForm, UserForm, MaterialForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.utils.text import slugify
from decimal import Decimal
from django.db.models import Q, F, Count, Sum
from django.utils import timezone


# Create your views here.

def login_user(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # messages.success(request, 'Usuario autenticado satisfactoriamente.')
                return redirect('panel')
        else:
            messages.error(request, 'Usuario o contraseña incorrecto.')
            return redirect('login_user')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {'form': form})


@login_required
def logout(request):
    do_logout(request)
    return redirect('login_user')


def allSundays(year):
    """This code was provided in the previous answer! It's not mine!"""
    d = date(year, 1, 1)  # January 1st
    d += timedelta(days=7 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days=7)


@login_required
def panel_home(request):
    if request.user.is_authenticated:
        sales_current_establishment = Venta.objects.all().values('establecimiento__nombre_establecimiento'). \
            order_by('establecimiento').filter(fecha_venta__day=datetime.now().day,
                                               fecha_venta__month=datetime.now().month,
                                               fecha_venta__year=datetime.now().year).annotate(
            venta_total=Sum('venta_total'))

        gastos_actual_establishment = Gastos.objects.all().values('establecimiento__nombre_establecimiento'). \
            order_by('establecimiento').filter(fecha_gasto__day=datetime.now().day,
                                               fecha_gasto__month=datetime.now().month,
                                               fecha_gasto__year=datetime.now().year).annotate(
            monto_gasto=Sum('monto_gasto'))

        sales_current = Venta_Diaria.objects.all().filter(fecha_venta__day=datetime.now().day,
                                                          fecha_venta__month=datetime.now().month,
                                                          fecha_venta__year=datetime.now().year).aggregate(
            venta_total=Sum('venta_total'))

        gastos_actual = Gastos.objects.all().filter(fecha_gasto__day=datetime.now().day,
                                                    fecha_gasto__month=datetime.now().month,
                                                    fecha_gasto__year=datetime.now().year).aggregate(
            monto_gasto=Sum('monto_gasto'))

        posible_venta = ProductoEstablecimiento.get_total_sales_reporter()

        gasto_final = Merma.get_total_merma() + Gastos.get_total_gasto() + Venta.get_total_sales_home()
        ganancia_bruta = Venta.get_total_sales() - Venta.get_total_sales_costo()
        ganancia_neta = ganancia_bruta - gasto_final

        for venta in sales_current_establishment:
            print(venta['venta_total'])

        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        lastWeek = Venta.objects.filter(fecha_venta__gte=monday_of_last_week,
                                        fecha_venta__lt=monday_of_this_week).aggregate(
            venta_total=Sum('venta_total'))

        currentDate = date.today()

        summaryDay = Venta.objects.filter(fecha_venta__range=(monday_of_this_week, currentDate.strftime("%Y-%m-%d"))) \
            .aggregate(venta_total=Sum('venta_total'))

        return render(request, "index.html", {'sales_current': sales_current['venta_total'],
                                              'gastos_actual': gastos_actual['monto_gasto'],
                                              'ganancia_neta': ganancia_neta,
                                              'costo_inversion': Venta.get_total_sales_costo(),
                                              'posible_venta': posible_venta, 'lastWeek': lastWeek['venta_total'],
                                              'summaryDay': summaryDay['venta_total'],
                                              'sales_current_establishment': sales_current_establishment,
                                              'gastos_actual_establishment': gastos_actual_establishment})
    return redirect('login_user')


@login_required
def usuarios(request):
    users = User.objects.exclude(is_superuser=True).order_by('pk')
    context = {'users': users}
    return render(request, "usuarios/usuarios.html", context)


@login_required
def insertar_usuario(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST or None)
        if userForm.is_valid():
            user_form = userForm.save(commit=False)
            user_form.save()
            messages.success(request, "El usuario se agregó satisfactoriamente!")
            return redirect("usuarios")
        else:
            messages.error(request, userForm.errors)
            print(userForm.errors)
            return redirect("insertar_usuario")
    else:
        userForm = UserForm()
    return render(request, 'usuarios/insertar_usuarios.html',
                  {'userForm': userForm})


@login_required
def editar_usuario(request, slug_username=None):
    if request.user.is_authenticated:
        user_custom = User.objects.get(slug=slug_username)
        update_form = UserForm(request.POST or None, instance=user_custom)
        if update_form.is_valid():
            edit = update_form.save(commit=False)
            edit.save()
            messages.success(request, 'Usuario modificado correctamente')
            return redirect('usuarios')
        context = {'user': user_custom, 'update_form': update_form, }
        return render(request, 'usuarios/editar_usuarios.html', context)
    return redirect('login_user')


@login_required
def eliminar_usuario(request, slug_username):
    if request.user.is_authenticated:
        u = User.objects.get(slug=slug_username)
        u.delete()
        messages.success(request, 'El usuario fue eliminado satisfactoriamente')
        return redirect('usuarios')
    return redirect('login_user')


@login_required
def categories_productos(request):
    if request.user.is_authenticated:
        categories_products = Categoria_Producto.objects.all()
        context = {'categories_products': categories_products}
        return render(request,
                      "punto_venta/categoria_producto/categorias_productos.html",
                      context)
    return redirect('login_user')


@login_required
def agregar_categoria(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nombre_categoria = request.POST.get('nombre_categoria')
            descripcion_categoria = request.POST.get('descripcion_categoria')

            c = Categoria_Producto.objects.create(
                nombre_categoria=nombre_categoria,
                descripcion=descripcion_categoria
            )
            c.save()
            messages.success(request, 'La categoría se agregó satisfactoriamente')
            return redirect('categories_productos')
        return render(request, 'punto_venta/categoria_producto/categorias_productos.html',
                      {})
    return redirect('login_user')


@login_required
def editar_categoria(request, id_o=None):
    if request.user.is_authenticated:
        categoria = Categoria_Producto.objects.get(id=id_o)
        if request.method == 'POST':
            nombre_categoria = request.POST.get('nombre_categoria')
            descripcion_categoria = request.POST.get('descripcion_categoria')

            Categoria_Producto.objects.filter(id=id_o).update(nombre_categoria=nombre_categoria)
            Categoria_Producto.objects.filter(id=id_o).update(descripcion=descripcion_categoria)

            messages.success(request, 'La categoría fue modificada satisfactoriamente')
            return redirect('categories_productos')
        context = {'categoria': categoria}
        return render(request, 'punto_venta/categoria_producto/categorias_productos.html', context)
    return redirect('login_user')


@login_required
def eliminar_categoria(request, id_cp):
    if request.user.is_authenticated:
        cp = Categoria_Producto.objects.get(id=id_cp)
        cp.delete()
        messages.success(request, 'La categoría se eliminó satisfactoriamente')
        return redirect('categories_productos')
    return redirect('login_user')


@login_required
def establecimientos(request):
    if request.user.is_authenticated:
        establecimiento = Establecimiento.objects.all()
        users = User.objects.exclude(rol=False)
        context = {'establecimientos': establecimiento, 'users': users}
        return render(request, "punto_venta/establecimiento/establecimientos.html", context)
    return redirect('login_user')


@login_required
def agregar_establecimiento(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nombre_establecimiento = request.POST.get('nombre_establecimiento')
            descripcion_establecimiento = request.POST.get('descripcion_establecimiento')
            user_responsable = request.POST.getlist('user_responsable')

            for i in range(0, len(user_responsable)):
                user_responsable[i] = int(user_responsable[i])

            if Establecimiento.objects.filter(user__in=user_responsable):
                messages.error(request, 'Uno de los responsables seleccionado tiene asignado un establecimiento')
                return redirect('establecimientos')
            else:
                e = Establecimiento.objects.create(
                    nombre_establecimiento=nombre_establecimiento,
                    descripcion=descripcion_establecimiento
                )

                for item in user_responsable:
                    e.user.add(item)
                e.save()
                messages.success(request, 'El establecimiento se agregó satisfactoriamente')
                return redirect('establecimientos')
        return render(request, 'punto_venta/establecimiento/establecimientos.html', {})
    return redirect('login_user')


@login_required
def editar_establecimiento(request, id_e=None):
    if request.user.is_authenticated:
        establecimiento = Establecimiento.objects.get(id=id_e)
        users_rest = QuerySet
        for user_establecimiento in establecimiento.user.all():
            users_rest = User.objects.exclude(rol=False).exclude(id=user_establecimiento.id)
        if request.method == 'POST':
            nombre_establecimiento = request.POST.get('nombre_establecimiento')
            descripcion_establecimiento = request.POST.get('descripcion_establecimiento')

            Establecimiento.objects.filter(id=id_e).update(nombre_establecimiento=nombre_establecimiento)
            Establecimiento.objects.filter(id=id_e).update(descripcion=descripcion_establecimiento)

            messages.success(request, 'El establecimiento fue modificado satisfactoriamente')
            return redirect('establecimientos')
        context = {'establecimiento': establecimiento, 'users_rest': users_rest}
        return render(request, 'punto_venta/establecimiento/establecimientos.html', context)
    return redirect('login_user')


@login_required
def eliminar_establecimiento(request, id_e):
    if request.user.is_authenticated:
        e = Establecimiento.objects.get(id=id_e)
        e.delete()
        messages.success(request, 'El establecimiento fue eliminado satisfactoriamente')
        return redirect('establecimientos')
    return redirect('login_user')


@login_required
def traslado(request, store_parameter, product_parameter):
    product_origin = get_object_or_404(Producto, slug=product_parameter)
    product_establecimiento = ProductoEstablecimiento.objects. \
        filter(establecimiento__slug=store_parameter).filter(producto_id=product_origin.id)[0]
    if request.method == "POST":
        trasladoForm = TrasladoEstablecimientoForm(request.POST,
                                                   establecimiento_id=product_establecimiento.establecimiento_id)
        if trasladoForm.is_valid():
            establecimiento_id = trasladoForm.cleaned_data['establecimiento'].id
            count = trasladoForm.cleaned_data['cantidad_trasladar']
            if int(count) <= product_establecimiento.cantidad_existente:
                resta_existente = product_establecimiento.cantidad_existente - int(count)
                ProductoEstablecimiento.objects.filter(producto_id=product_origin.id). \
                    filter(establecimiento_id=product_establecimiento.establecimiento_id
                           ).update(cantidad_existente=resta_existente)

                if not ProductoEstablecimiento.objects.filter(producto_id=product_origin.id). \
                        filter(establecimiento_id=establecimiento_id):
                    newProducto = ProductoEstablecimiento(producto_id=product_origin.id,
                                                          cantidad_existente=int(count),
                                                          precio_venta=product_establecimiento.precio_venta,
                                                          establecimiento_id=establecimiento_id,
                                                          fecha=datetime.now())
                    newProducto.save()
                    move = Traslado(producto_id=product_origin.id, establecimiento_id=establecimiento_id,
                                    establecimiento_padre_id=product_establecimiento.establecimiento_id,
                                    cantidad_trasladar=int(count), user=request.user)
                    move.save()

                else:
                    product_traslado = ProductoEstablecimiento.objects.filter(producto__id=product.id) \
                        .filter(establecimiento_id=establecimiento_id)
                    agregar_existente = product_traslado[0].cantidad_existente + int(count)

                    ProductoEstablecimiento.objects.filter(producto__id=product_origin.id) \
                        .filter(establecimiento_id=establecimiento_id).update(
                        cantidad_existente=agregar_existente)

                    move = Traslado(producto_id=product_origin.id, establecimiento_id=establecimiento_id,
                                    establecimiento_padre_id=product_establecimiento.establecimiento_id,
                                    cantidad_trasladar=int(count), user=request.user)
                    move.save()

                messages.success(request, "El traslado se realizó satisfactoriamente!")
                return redirect(
                    reverse('productos_establecimientos', args=(product_establecimiento.establecimiento.slug,)))
            else:
                messages.error(request, "Cantidad insuficiente para realizar el traslado!")
                return redirect(reverse('traslado', args=(id_p,)))
    else:
        trasladoForm = TrasladoEstablecimientoForm(request.POST,
                                                   establecimiento_id=product_establecimiento.establecimiento_id)

    return render(request, 'punto_venta/traslado/insertar_traslado.html',
                  {'trasladoForm': trasladoForm})


@login_required
def traslado_general(request, product_parameter):
    product = get_object_or_404(Producto, slug=product_parameter)
    if request.method == "POST":
        trasladoForm = TrasladoForm(request.POST)
        if trasladoForm.is_valid():
            establecimiento_id = trasladoForm.cleaned_data['establecimiento'].id
            count = trasladoForm.cleaned_data['cantidad_trasladar']
            precio_venta = trasladoForm.cleaned_data['precio_venta']

            if int(count) <= product.cantidad_existente:
                resta_existente = product.cantidad_existente - int(count)
                Producto.objects.filter(id=product.id).update(cantidad_existente=resta_existente)
                if not ProductoEstablecimiento.objects.filter(producto_id=product.id). \
                        filter(establecimiento_id=establecimiento_id):
                    newProducto = ProductoEstablecimiento(producto=product,
                                                          cantidad_existente=int(count),
                                                          precio_venta=precio_venta,
                                                          establecimiento_id=establecimiento_id,
                                                          fecha=datetime.now())
                    newProducto.save()

                    move = Traslado(producto_id=product.id, establecimiento_id=establecimiento_id,
                                    establecimiento_padre=None,
                                    cantidad_trasladar=int(count), user=request.user)
                    move.save()

                else:

                    product_traslado = ProductoEstablecimiento.objects.filter(producto__id=product.id) \
                        .filter(establecimiento_id=establecimiento_id)
                    agregar_existente = product_traslado[0].cantidad_existente + int(count)

                    ProductoEstablecimiento.objects.filter(producto__id=product.id) \
                        .filter(establecimiento_id=establecimiento_id).update(
                        cantidad_existente=agregar_existente, precio_venta=precio_venta)

                    move = Traslado(producto_id=product.id, establecimiento_id=establecimiento_id,
                                    establecimiento_padre_id=None,
                                    cantidad_trasladar=int(count), user=request.user)
                    move.save()

                messages.success(request, "El traslado se realizó satisfactoriamente!")
                return redirect('productos')
            else:
                messages.error(request, "Cantidad insuficiente para realizar el traslado!")
                return redirect(reverse('traslado', args=(id_p,)))
    else:
        trasladoForm = TrasladoForm(request.POST)

    return render(request, 'punto_venta/traslado/insertar_traslado.html',
                  {'trasladoForm': trasladoForm})


@login_required
def traslados(request):
    transfers = Traslado.objects.all().order_by('id')
    context = {'traslados': transfers}
    return render(request, "punto_venta/traslado/traslados.html", context)


@login_required
def traslados_store(request, store):
    transfers = Traslado.objects.filter(establecimiento_padre__slug=store).order_by('id')
    context = {'traslados_store': transfers}
    return render(request, "punto_venta/traslado/traslados.html", context)


@login_required
def edit_traslado(request, id_t=None):
    if request.user.is_authenticated:
        move = Traslado.objects.get(id=id_t)
        if request.method == 'POST':
            count_traslado = request.POST.get('count_traslado')
            producto_custom = Producto.objects.get(id=move.producto.id)
            if int(count_traslado) != 0:
                rest_traslado = move.cantidad_trasladar - int(count_traslado)
                cant_existente = producto_custom.cantidad_existente + rest_traslado
                Traslado.objects.filter(id=id_t).update(cantidad_trasladar=int(count_traslado))
                Producto.objects.filter(id=move.producto.id).update(cantidad_existente=cant_existente)
                messages.success(request,
                                 'La cantidad trasladada de ' + move.producto.nombre_producto + ' fue modificada '
                                                                                                'satisfactoriamente')
            else:
                # messages.error(request, 'La cantidad no puede ser 0, si lo desea elimine el producto')
                cant_traslado = producto_custom.cantidad_existente + move.cantidad_trasladar
                Producto.objects.filter(id=move.producto.id).update(cantidad_existente=cant_traslado)
                move.delete()
                messages.success(request, 'Traslado eliminado satisfactoriamente')

            return redirect('traslados')
        context = {'move': move}
        return render(request, 'punto_venta/traslado/traslados.html', context)
    return redirect('login_user')


@login_required
def delete_traslado(request, id_t):
    if request.user.is_authenticated:
        t = Traslado.objects.get(id=id_t)
        producto_custom = Producto.objects.get(id=t.producto.id)

        if producto_custom.cantidad_existente == t.cantidad_trasladar:
            Producto.objects.filter(id=t.producto.id).update(cantidad_existente=0)

            producto_custom2 = Producto.objects.get(establecimiento_id=t.establecimiento_padre.id)
            cant_traslado = producto_custom2.cantidad_existente + t.cantidad_trasladar
            Producto.objects.filter(establecimiento_id=t.establecimiento_padre.id).update(
                cantidad_existente=cant_traslado)

        else:
            producto_custom2 = Producto.objects.get(id=t.producto.id)
            cant_traslado = producto_custom2.cantidad_existente + t.cantidad_trasladar
            Producto.objects.filter(id=t.producto.id).update(cantidad_existente=cant_traslado)
        t.delete()
        messages.success(request, 'Traslado eliminado satisfactoriamente')
        return redirect('traslados')
    return redirect('login_user')


############# Productos ##############
@login_required
def productos_establecimientos(request, store):
    establecimiento = Establecimiento.objects.get(slug=store)
    products = ProductoEstablecimiento.objects.filter(establecimiento__slug=store).order_by('id')
    tasa = Moneda.objects.all()[0]
    context = {'productos': products, 'store': store, 'tasa': tasa, 'establecimiento': establecimiento}
    return render(request, "punto_venta/producto/productos_establecimientos.html", context)


@login_required
def productos(request):
    products = Producto.objects.all().order_by('id')
    materials = Material.objects.all().order_by('id')
    context = {'productos': products, 'materials': materials}
    return render(request, "punto_venta/producto/productos.html", context)


@login_required
def agregar_producto(request):
    if request.method == 'POST':
        productoForm = ProductoForm(request.POST or None, request.FILES or None)
        if productoForm.is_valid():
            producto_form = productoForm.save(commit=False)
            producto_form.save()
            messages.success(request, "El producto se agregó satisfactoriamente!")
            return redirect("productos")
        else:
            print(productoForm.errors)
    else:
        productoForm = ProductoForm()
    return render(request, 'punto_venta/producto/insertar_producto.html',
                  {'productoForm': productoForm})


@login_required
def modificar_producto(request, product=None):
    if request.user.is_authenticated:
        producto_custom = Producto.objects.get(slug=product)
        update_form = ProductoForm(request.POST or None, request.FILES or None, instance=producto_custom)
        if update_form.is_valid():
            edit = update_form.save(commit=False)
            edit.save()
            messages.success(request, 'Producto modificado correctamente')
            return redirect('productos')
        context = {'producto': producto_custom, 'update_form': update_form, }
        return render(request, 'punto_venta/producto/modificar_producto.html', context)
    return redirect('login_user')


@login_required
def eliminar_producto(request, id_p):
    if request.user.is_authenticated:
        p = Producto.objects.get(id=id_p)
        p.delete()
        messages.success(request, 'Producto eliminado satisfactoriamente')
        return redirect('productos')
    return redirect('login_user')


@login_required
def edit_product_establecimiento(request, id_p):
    if request.user.is_authenticated:
        producto_custom = ProductoEstablecimiento.objects.get(id=id_p)
        if request.method == "POST":
            precio_venta = request.POST.get('precio_venta')
            ProductoEstablecimiento.objects.filter(pk=id_p).update(precio_venta=precio_venta)

            messages.success(request, 'Precio de Venta modificado satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto_custom.establecimiento.slug,)))
        context = {}
        return render(request, "punto_venta/producto/productos_establecimientos.html", context)
    return redirect('login_user')


today = date.today()


############# Entradas ##############

@login_required
def entradas(request):
    increases = Entrada.objects.all()
    tasa = Moneda.objects.all()[0]
    context = {'increases_all': increases, 'tasa': tasa}
    return render(request, "punto_venta/entrada/entrada.html", context)


@login_required
def entradas_for_store(request, store):
    increases = Entrada.objects.filter(establecimiento__slug=store)
    context = {'increases': increases}
    return render(request, "punto_venta/entrada/entrada.html", context)


@login_required
def entradas_materiales(request):
    increases = Moneda.objects.all()
    context = {'increases_all': increases}
    return render(request, "punto_venta/entrada/entrada_material.html", context)


@login_required
def add_incrementar(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = ProductoEstablecimiento.objects.get(id=id_p)
            count_incrementar = request.POST.get('count_incrementar')

            if Entrada.objects.filter(producto=producto_custom.producto).filter(
                    establecimiento_id=producto_custom.establecimiento.id):
                if Entrada.objects.filter(producto=producto_custom.producto).filter(
                        establecimiento_id=producto_custom.establecimiento.id).filter(fecha__day=today.day,
                                                                                      fecha__month=today.month,
                                                                                      fecha__year=today.year):
                    if_incrementar = Entrada.objects.filter(producto=producto_custom.producto).filter(
                        establecimiento_id=producto_custom.establecimiento.id).filter(
                        fecha__day=today.day,
                        fecha__month=today.month,
                        fecha__year=today.year)[:1].get()
                    cant_existente = if_incrementar.cantidad_producto_entrada + int(count_incrementar)
                    Entrada.objects.filter(producto=producto_custom.producto).filter(
                        establecimiento_id=producto_custom.establecimiento.id).filter(fecha__day=today.day,
                                                                                      fecha__month=today.month,
                                                                                      fecha__year=today.year) \
                        .update(cantidad_producto_entrada=int(cant_existente))
                    count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                    ProductoEstablecimiento.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)
                else:
                    c = Entrada.objects.create(producto=producto_custom.producto,
                                               establecimiento_id=producto_custom.establecimiento.id,
                                               cantidad_producto_entrada=int(count_incrementar),
                                               fecha=datetime.now())
                    c.save()
                    count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                    ProductoEstablecimiento.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)
            else:
                c = Entrada.objects.create(producto=producto_custom.producto,
                                           establecimiento_id=producto_custom.establecimiento.id,
                                           cantidad_producto_entrada=int(count_incrementar),
                                           fecha=datetime.now())
                c.save()
                count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                ProductoEstablecimiento.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)

            messages.success(request, 'Producto incrementado satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto_custom.establecimiento.slug,)))
        context = {}
        return render(request, "punto_venta/producto/productos_establecimientos.html", context)
    return redirect('login_user')


@login_required
def edit_entrada(request, id_e=None):
    if request.user.is_authenticated:
        entrada = Entrada.objects.get(id=id_e)
        if request.method == 'POST':
            count_entrada = request.POST.get('count_entrada')
            if int(count_entrada) < entrada.cantidad_producto_entrada:
                rest = entrada.cantidad_producto_entrada - int(count_entrada)
                Entrada.objects.filter(id=id_e).update(cantidad_producto_entrada=rest)

                product = ProductoEstablecimiento.objects.filter(producto_id=entrada.producto.id).filter(
                    establecimiento_id=entrada.establecimiento.id)[:1].get()
                rest_prod = product.cantidad_existente - rest
                ProductoEstablecimiento.objects.filter(producto_id=entrada.producto.id).filter(
                    establecimiento_id=entrada.establecimiento.id).update(cantidad_existente=rest_prod)
            else:
                diferencia = int(count_entrada) - entrada.cantidad_producto_entrada
                suma = entrada.cantidad_producto_entrada + diferencia
                Entrada.objects.filter(id=id_e).update(cantidad_producto_entrada=suma)
                producto_custom = ProductoEstablecimiento.objects.filter(producto_id=entrada.producto.id).filter(
                    establecimiento_id=entrada.establecimiento.id)[:1].get()
                cant_existente = producto_custom.cantidad_existente + diferencia
                ProductoEstablecimiento.objects.filter(producto_id=entrada.producto.id).filter(
                    establecimiento_id=entrada.establecimiento.id).update(cantidad_existente=cant_existente)
            messages.success(request,
                             'La cantidad incrementada de ' + entrada.producto.nombre_producto + ' fue modificada '
                                                                                                 'satisfactoriamente')

            return redirect(reverse('entradas_store', args=(entrada.establecimiento.slug,)))
        context = {'entrada': entrada}
        return render(request, 'punto_venta/entrada/entrada.html', context)
    return redirect('login_user')


@login_required
def delete_entrada(request, id_e):
    if request.user.is_authenticated:
        e = Entrada.objects.get(id=id_e)
        producto_custom = ProductoEstablecimiento.objects.filter(producto_id=e.producto.id).filter(
            establecimiento_id=e.establecimiento.id)[:1].get()
        cant_incrementar = producto_custom.cantidad_existente - e.cantidad_producto_entrada
        ProductoEstablecimiento.objects.filter(producto_id=e.producto.id).filter(
            establecimiento_id=e.establecimiento.id).update(cantidad_existente=cant_incrementar)
        e.delete()
        messages.success(request, 'Entrada eliminada satisfactoriamente')
        return redirect(reverse('entradas_store', args=(e.establecimiento.slug,)))
    return redirect('login_user')


@login_required
def add_incrementar_general(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = Producto.objects.get(id=id_p)
            count_incrementar = request.POST.get('count_incrementar')

            if Entrada.objects.filter(producto=producto_custom).filter(establecimiento_id=None):
                if Entrada.objects.filter(producto=producto_custom).filter(
                        establecimiento_id=None).filter(fecha__day=today.day, fecha__month=today.month,
                                                        fecha__year=today.year):
                    if_incrementar = Entrada.objects.filter(producto=producto_custom).filter(
                        establecimiento_id=None).filter(fecha__day=today.day, fecha__month=today.month,
                                                        fecha__year=today.year)[:1].get()
                    cant_existente = if_incrementar.cantidad_producto_entrada + int(count_incrementar)
                    Entrada.objects.filter(producto=producto_custom).filter(
                        establecimiento_id=None).filter(fecha__day=today.day, fecha__month=today.month,
                                                        fecha__year=today.year) \
                        .update(cantidad_producto_entrada=int(cant_existente))
                    count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)
                else:
                    c = Entrada.objects.create(producto=producto_custom,
                                               establecimiento_id=producto_custom.establecimiento.id,
                                               cantidad_producto_entrada=int(count_incrementar),
                                               fecha=datetime.now())
                    c.save()
                    count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)
            else:
                c = Entrada.objects.create(producto=producto_custom,
                                           establecimiento_id=None,
                                           cantidad_producto_entrada=int(count_incrementar),
                                           fecha=datetime.now())
                c.save()
                count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                Producto.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)

            messages.success(request, 'Producto incrementado satisfactoriamente')
            return redirect('productos')
        context = {}
        return render(request, "punto_venta/producto/productos.html", context)
    return redirect('login_user')


@login_required
def edit_entrada_general(request, id_e=None):
    if request.user.is_authenticated:
        entrada = Entrada.objects.get(id=id_e)
        if request.method == 'POST':
            count_entrada = request.POST.get('count_entrada')
            if int(count_entrada) < entrada.cantidad_producto_entrada:
                rest = entrada.cantidad_producto_entrada - int(count_entrada)
                Entrada.objects.filter(id=id_e).update(cantidad_producto_entrada=rest)

                product = Producto.objects.get(id=entrada.producto.id)
                rest_prod = product.cantidad_existente - rest
                Producto.objects.filter(id=entrada.producto.id).update(cantidad_existente=rest_prod)
            else:
                diferencia = int(count_entrada) - entrada.cantidad_producto_entrada
                suma = entrada.cantidad_producto_entrada + diferencia
                Entrada.objects.filter(id=id_e).update(cantidad_producto_entrada=suma)
                producto_custom = Producto.objects.get(id=entrada.producto.id)
                cant_existente = producto_custom.cantidad_existente + diferencia
                Producto.objects.filter(id=entrada.producto.id).update(cantidad_existente=cant_existente)
            messages.success(request,
                             'La cantidad incrementada de ' + entrada.producto.nombre_producto + ' fue modificada '
                                                                                                 'satisfactoriamente')

            return redirect('entradas')
        context = {'entrada': entrada}
        return render(request, 'punto_venta/entrada/entrada.html', context)
    return redirect('login_user')


@login_required
def delete_entrada_general(request, id_e):
    if request.user.is_authenticated:
        e = Entrada.objects.get(id=id_e)
        producto_custom = Producto.objects.get(id=e.producto.id)
        cant_incrementar = producto_custom.cantidad_existente - e.cantidad_producto_entrada
        Producto.objects.filter(id=e.producto.id).update(cantidad_existente=cant_incrementar)
        e.delete()
        messages.success(request, 'Entrada eliminada satisfactoriamente')
        return redirect('entradas')
    return redirect('login_user')


############# Merma ##############


@login_required
def mermas(request):
    listMermas = []
    decrease = Merma.objects.all()
    tasa = Moneda.objects.all()[0]
    for merma in decrease:
        ratio = merma.producto.costo * tasa.tasa
        monto = ratio * merma.cantidad_producto_merma
        mermita = MermaFinal(merma.id, merma.fecha, merma.producto.nombre_producto,
                             merma.cantidad_producto_merma, ratio, monto)
        listMermas.append(mermita)
    context = {'mermas': listMermas, 'tasa': tasa}
    return render(request, "punto_venta/merma/merma.html", context)


class MermaFinal:
    def __init__(self, id, fecha, nombre_producto, cantidad_producto_merma, costo, monto):
        self.id = id
        self.fecha = fecha
        self.nombre_producto = nombre_producto
        self.cantidad_producto_merma = cantidad_producto_merma
        self.costo = costo
        self.monto = monto


@login_required
def mermas_store(request, store):
    listMermas = []
    decrease = Merma.objects.filter(establecimiento__slug=store)
    tasa = Moneda.objects.all()[0]
    for merma in decrease:
        ratio = merma.producto.costo * tasa.tasa
        mermita = MermaFinal(merma.id, merma.fecha, merma.producto.nombre_producto,
                             merma.cantidad_producto_merma, ratio, 0)
        listMermas.append(mermita)

    context = {'mermas_store': listMermas, 'tasa': tasa}
    return render(request, "punto_venta/merma/merma.html", context)


@login_required
def mermas_material(request):
    decrease = Merma_Material.objects.all()
    context = {'mermas_material': decrease}
    return render(request, "punto_venta/merma/merma_material.html", context)


@login_required
def add_merma(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = ProductoEstablecimiento.objects.get(id=id_p)
            count_merma = request.POST.get('count_merma')
            today = date.today()
            if Merma.objects.filter(producto=producto_custom.producto).filter(
                    establecimiento_id=producto_custom.establecimiento.id):
                if Merma.objects.filter(producto=producto_custom.producto).filter(
                        establecimiento_id=producto_custom.establecimiento.id).filter(fecha__day=today.day,
                                                                                      fecha__month=today.month,
                                                                                      fecha__year=today.year):
                    if_merma = Merma.objects.filter(producto=producto_custom.producto).filter(
                        establecimiento_id=producto_custom.establecimiento.id).filter(fecha__day=today.day,
                                                                                      fecha__month=today.month,
                                                                                      fecha__year=today.year)[:1].get()
                    cant_existente = if_merma.cantidad_producto_merma + int(count_merma)
                    Merma.objects.filter(producto=producto_custom.producto).filter(
                        establecimiento_id=producto_custom.establecimiento.id).filter(fecha__day=today.day,
                                                                                      fecha__month=today.month,
                                                                                      fecha__year=today.year) \
                        .update(cantidad_producto_merma=int(cant_existente))
                    count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                    ProductoEstablecimiento.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)
                else:
                    c = Merma.objects.create(producto=producto_custom.producto,
                                             cantidad_producto_merma=int(count_merma),
                                             establecimiento_id=producto_custom.establecimiento.id,
                                             fecha=datetime.now())
                    c.save()
                    count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                    ProductoEstablecimiento.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)
            else:
                c = Merma.objects.create(producto=producto_custom.producto, cantidad_producto_merma=int(count_merma),
                                         establecimiento_id=producto_custom.establecimiento.id,
                                         fecha=datetime.now())
                c.save()
                count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                ProductoEstablecimiento.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)

            operations_sales_store(request, producto_custom.establecimiento.id)
            messages.success(request, 'Producto mermado satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto_custom.establecimiento.slug,)))
        context = {}
        return render(request, "punto_venta/producto/productos_establecimientos.html", context)
    return redirect('login_user')


@login_required
def edit_merma(request, id_m=None):
    if request.user.is_authenticated:
        merma = Merma.objects.get(id=id_m)
        if request.method == 'POST':
            count_merma = request.POST.get('count_merma')
            producto_custom = ProductoEstablecimiento.objects.filter(producto_id=merma.producto.id).filter(
                establecimiento_id=merma.establecimiento.id)[:1].get()
            if int(count_merma) != 0:
                rest_merma = merma.cantidad_producto_merma - int(count_merma)
                cant_existente = producto_custom.cantidad_existente + rest_merma
                Merma.objects.filter(id=id_m).update(cantidad_producto_merma=int(count_merma))
                ProductoEstablecimiento.objects.filter(producto_id=merma.producto.id).filter(
                    establecimiento_id=merma.establecimiento.id).update(cantidad_existente=cant_existente)
                messages.success(request,
                                 'La cantidad mermada de ' + merma.producto.nombre_producto + ' fue modificada '
                                                                                              'satisfactoriamente')
            else:
                # messages.error(request, 'La cantidad no puede ser 0, si lo desea elimine el producto')
                cant_merma = producto_custom.cantidad_existente + merma.cantidad_producto_merma
                ProductoEstablecimiento.objects.filter(producto_id=merma.producto.id).filter(
                    establecimiento_id=merma.establecimiento.id).update(cantidad_existente=cant_merma)
                merma.delete()
                messages.success(request, 'Merma eliminada satisfactoriamente')

            operations_sales_store(request, m.establecimiento.id)
            return redirect(reverse('mermas_store', args=(merma.establecimiento.slug,)))
        context = {'merma': merma}
        return render(request, 'punto_venta/merma/merma.html', context)
    return redirect('login_user')


@login_required
def delete_merma(request, id_m):
    if request.user.is_authenticated:
        m = Merma.objects.get(id=id_m)
        producto_custom = ProductoEstablecimiento.objects.filter(producto_id=e.producto.id).filter(
            establecimiento_id=e.establecimiento.id)[:1].get()
        cant_merma = producto_custom.cantidad_existente + m.cantidad_producto_merma
        ProductoEstablecimiento.objects.filter(id=m.producto.id).filter(
            establecimiento_id=m.establecimiento.id).update(cantidad_existente=cant_merma)
        m.delete()
        messages.success(request, 'Merma eliminada satisfactoriamente')
        return redirect(reverse('mermas_store', args=(m.establecimiento.slug,)))
    return redirect('login_user')


@login_required
def add_merma_general(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = Producto.objects.get(id=id_p)
            count_merma = request.POST.get('count_merma')
            today = date.today()
            if Merma.objects.filter(producto=producto_custom).filter(establecimiento_id=None):
                if Merma.objects.filter(producto=producto_custom).filter(establecimiento_id=None) \
                        .filter(fecha__day=today.day,
                                fecha__month=today.month,
                                fecha__year=today.year).exists():
                    if_merma = Merma.objects.filter(producto=producto_custom).filter(establecimiento_id=None).filter(
                        fecha__day=today.day,
                        fecha__month=today.month,
                        fecha__year=today.year)[:1].get()
                    cant_existente = if_merma.cantidad_producto_merma + int(count_merma)
                    Merma.objects.filter(producto=producto_custom).filter(establecimiento_id=None).filter(
                        fecha__day=today.day,
                        fecha__month=today.month,
                        fecha__year=today.year) \
                        .update(cantidad_producto_merma=int(cant_existente))
                    count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)
                else:
                    c = Merma.objects.create(producto=producto_custom, cantidad_producto_merma=int(count_merma),
                                             establecimiento_id=None,
                                             fecha=datetime.now())
                    c.save()
                    count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)
            else:
                c = Merma.objects.create(producto=producto_custom, cantidad_producto_merma=int(count_merma),
                                         establecimiento_id=None,
                                         fecha=datetime.now())
                c.save()
                count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                Producto.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)

            operations_sales_store(request, None)
            messages.success(request, 'Producto mermado satisfactoriamente')
            return redirect('productos')
        context = {}
        return render(request, "punto_venta/producto/productos_establecimientos.html", context)
    return redirect('login_user')


@login_required
def edit_merma_general(request, id_m=None):
    if request.user.is_authenticated:
        merma = Merma.objects.get(id=id_m)
        if request.method == 'POST':
            count_merma = request.POST.get('count_merma')
            producto_custom = Producto.objects.get(id=merma.producto.id)
            if int(count_merma) != 0:
                rest_merma = merma.cantidad_producto_merma - int(count_merma)
                cant_existente = producto_custom.cantidad_existente + rest_merma
                Merma.objects.filter(id=id_m).update(cantidad_producto_merma=int(count_merma))
                Producto.objects.filter(id=merma.producto.id).update(cantidad_existente=cant_existente)
                messages.success(request,
                                 'La cantidad mermada de ' + merma.producto.nombre_producto + ' fue modificada '
                                                                                              'satisfactoriamente')
            else:
                # messages.error(request, 'La cantidad no puede ser 0, si lo desea elimine el producto')
                cant_merma = producto_custom.cantidad_existente + merma.cantidad_producto_merma
                Producto.objects.filter(id=merma.producto.id).update(cantidad_existente=cant_merma)
                merma.delete()
                messages.success(request, 'Merma eliminada satisfactoriamente')

            operations_sales_store(request, m.establecimiento.id)
            return redirect(reverse('mermas_store', args=(merma.establecimiento.slug,)))
        context = {'merma': merma}
        return render(request, 'punto_venta/merma/merma.html', context)
    return redirect('login_user')


@login_required
def delete_merma_general(request, id_m):
    if request.user.is_authenticated:
        m = Merma.objects.get(id=id_m)
        producto_custom = Producto.objects.get(id=m.producto.id)
        cant_merma = producto_custom.cantidad_existente + m.cantidad_producto_merma
        Producto.objects.filter(id=m.producto.id).update(cantidad_existente=cant_merma)
        m.delete()
        messages.success(request, 'Merma eliminada satisfactoriamente')
        return redirect(reverse('mermas_store', args=(m.establecimiento.slug,)))
    return redirect('login_user')


@login_required
def operations_sales(request):
    gasto_final = Merma.get_total_merma() + Gastos.get_total_gasto() + Venta.get_total_sales_home()
    ganancia_bruta = Venta.get_total_sales() - Venta.get_total_sales_costo()
    ganancia_neta = Venta.get_total_sales() - Venta.get_total_sales_costo() - gasto_final
    if Venta_Diaria.objects.filter(fecha_venta__day=date.today().day,
                                   fecha_venta__month=date.today().month,
                                   fecha_venta__year=date.today().year).exists():
        Venta_Diaria.objects.filter(fecha_venta__day=date.today().day,
                                    fecha_venta__month=date.today().month,
                                    fecha_venta__year=date.today().year).update(
            cantidad=Venta.get_total_count(),
            venta_total=Venta.get_total_sales(),
            costo=Venta.get_total_sales_costo(),
            ganancia_bruta=ganancia_bruta,
            gasto=gasto_final,
            ganancia_neta=ganancia_neta
        )
    else:
        Venta_Diaria.objects.create(fecha_venta=datetime.now(), cantidad=Venta.get_total_count(),
                                    venta_total=Venta.get_total_sales(), costo=Venta.get_total_sales_costo(),
                                    ganancia_bruta=ganancia_bruta, gasto=gasto_final, ganancia_neta=ganancia_neta)


@login_required
def operations_sales_store(request, store_id):
    gasto_final = Merma.get_total_merma() + Gastos.get_total_gasto() + Venta.get_total_sales_home()
    ganancia_bruta = Venta.get_total_sales() - Venta.get_total_sales_costo()
    ganancia_neta = Venta.get_total_sales() - Venta.get_total_sales_costo() - gasto_final
    if Venta_Diaria.objects.filter(fecha_venta__day=date.today().day,
                                   fecha_venta__month=date.today().month,
                                   fecha_venta__year=date.today().year):
        Venta_Diaria.objects.filter(fecha_venta__day=date.today().day,
                                    fecha_venta__month=date.today().month,
                                    fecha_venta__year=date.today().year).update(
            cantidad=Venta.get_total_count(),
            venta_total=Venta.get_total_sales(),
            costo=Venta.get_total_sales_costo(),
            ganancia_bruta=ganancia_bruta,
            gasto=gasto_final,
            ganancia_neta=ganancia_neta
        )
    else:
        Venta_Diaria.objects.create(fecha_venta=datetime.now(), cantidad=Venta.get_total_count(),
                                    venta_total=Venta.get_total_sales(), costo=Venta.get_total_sales_costo(),
                                    establecimiento_id=store_id,
                                    ganancia_bruta=ganancia_bruta, gasto=gasto_final, ganancia_neta=ganancia_neta)


@login_required
def add_spending(request, store):
    if request.user.is_authenticated:
        if request.method == "POST":
            concepto = request.POST.get('concepto')
            gasto_amount = request.POST.get('gasto_amount')
            establecimiento = Establecimiento.objects.get(slug=store)
            Gastos.objects.create(usuario=request.user, concepto=concepto,
                                  monto_gasto=gasto_amount, fecha_gasto=datetime.now(),
                                  establecimiento_id=establecimiento.id)
            operations_sales_store(request, establecimiento.id)

            messages.success(request, 'Gasto registrado satisfactoriamente')
            return redirect(reverse('expenses_store', args=(store,)))
        context = {}
        return render(request, "punto_venta/gasto/gastos.html", context)
    return redirect('login_user')


@login_required
def add_spending_general(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concepto = request.POST.get('concepto')
            gasto_amount = request.POST.get('gasto_amount')
            Gastos.objects.create(usuario=request.user, concepto=concepto,
                                  monto_gasto=gasto_amount, fecha_gasto=datetime.now())
            operations_sales(request)

            messages.success(request, 'Gasto registrado satisfactoriamente')
            return redirect('expenses')
        context = {}
        return render(request, "punto_venta/gasto/gastos.html", context)
    return redirect('login_user')


@login_required
def expenses(request):
    if request.user.is_authenticated:
        gastos = Gastos.objects.all()
        context = {'gastos': gastos}
        return render(request, "punto_venta/gasto/gastos.html", context)
    return redirect('login_user')


@login_required
def expenses_store(request, store):
    if request.user.is_authenticated:
        gastos = Gastos.objects.filter(establecimiento__slug=store)
        establecimiento = Establecimiento.objects.get(slug=store)
        context = {'gastos_store': gastos, 'store': store, 'establecimiento': establecimiento}
        return render(request, "punto_venta/gasto/gastos.html", context)
    return redirect('login_user')


@login_required
def buy(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto = ProductoEstablecimiento.objects.get(id=id_p)
            payment_type = request.POST.get('payment_type')
            count_product_var = request.POST.get('count_product_var')
            deudor_name = request.POST.get('deudor_name')

            venta_monto = int(count_product_var) * producto.precio_venta
            tasa = Moneda.objects.all()[0]
            costo_mn = producto.producto.costo * tasa.tasa
            venta_monto_costo = int(count_product_var) * costo_mn

            if deudor_name:
                Venta.objects.create(usuario=request.user, producto=producto, cantidad=int(count_product_var),
                                     tipo_pago=payment_type, venta_total=venta_monto, costo=venta_monto_costo,
                                     deudor=deudor_name, establecimiento_id=producto.establecimiento.id,
                                     fecha_venta=datetime.now())
            else:
                Venta.objects.create(usuario=request.user, producto=producto, cantidad=int(count_product_var),
                                     tipo_pago=payment_type, venta_total=venta_monto, costo=venta_monto_costo,
                                     establecimiento_id=producto.establecimiento.id, fecha_venta=datetime.now())

            count_venta = producto.cantidad_existente - int(count_product_var)
            ProductoEstablecimiento.objects.filter(id=producto.id).update(cantidad_existente=count_venta)

            gasto_final = Merma.get_total_merma() + Gastos.get_total_gasto() + Venta.get_total_sales_home()
            ganancia_bruta = Venta.get_total_sales() - Venta.get_total_sales_costo()
            ganancia_neta = Venta.get_total_sales() - Venta.get_total_sales_costo() - gasto_final
            if Venta_Diaria.objects.filter(fecha_venta__day=date.today().day,
                                           fecha_venta__month=date.today().month,
                                           fecha_venta__year=date.today().year):
                Venta_Diaria.objects.filter(fecha_venta__day=date.today().day,
                                            fecha_venta__month=date.today().month,
                                            fecha_venta__year=date.today().year).update(
                    cantidad=Venta.get_total_count(),
                    venta_total=Venta.get_total_sales(),
                    costo=Venta.get_total_sales_costo(),
                    ganancia_bruta=ganancia_bruta,
                    gasto=gasto_final,
                    establecimiento_id=producto.establecimiento_id,
                    ganancia_neta=ganancia_neta
                )
            else:
                Venta_Diaria.objects.create(fecha_venta=datetime.now(), cantidad=Venta.get_total_count(),
                                            venta_total=Venta.get_total_sales(), costo=Venta.get_total_sales_costo(),
                                            establecimiento_id=producto.establecimiento_id,
                                            ganancia_bruta=ganancia_bruta, gasto=gasto_final,
                                            ganancia_neta=ganancia_neta)

            messages.success(request, 'Venta registrada satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto.establecimiento.slug,)))

        context = {}
        return render(request, "punto_venta/producto/productos_establecimientos.html", context)
    return redirect('login_user')


@login_required
def ventas_diaria(request):
    if request.user.is_authenticated:
        sales = Venta_Diaria.objects.all().order_by('fecha_venta')
        if request.method == "POST":
            fecha_init = request.POST.get('fecha_init')
            fecha_finish = request.POST.get('fecha_finish')

            date_time_str = str(fecha_init)
            date_time_str_finish = str(fecha_finish)
            date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y')
            date_time_obj_finish = datetime.strptime(date_time_str_finish, '%d/%m/%Y')

            formatDate2 = date_time_obj.strftime("%Y-%m-%d")
            formatDate3 = date_time_obj_finish.strftime("%Y-%m-%d")

            sales_filter = Venta_Diaria.objects.filter(fecha_venta__range=(formatDate2, formatDate3)) \
                .order_by('fecha_venta')
            context = {'sales_filter': sales_filter}
            return render(request, "punto_venta/venta/ventas_diaria.html", context)

        context = {'sales': sales}
        return render(request, "punto_venta/venta/ventas_diaria.html", context)
    return redirect('login_user')


@login_required
def ventas_diaria_store(request, store):
    if request.user.is_authenticated:
        sales_establecimiento = Venta_Diaria.objects.filter(establecimiento__slug=store).order_by('fecha_venta')
        if request.method == "POST":
            fecha_init = request.POST.get('fecha_init')
            fecha_finish = request.POST.get('fecha_finish')

            date_time_str = str(fecha_init)
            date_time_str_finish = str(fecha_finish)
            date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y')
            date_time_obj_finish = datetime.strptime(date_time_str_finish, '%d/%m/%Y')

            formatDate2 = date_time_obj.strftime("%Y-%m-%d")
            formatDate3 = date_time_obj_finish.strftime("%Y-%m-%d")

            sales_filter_store = Venta_Diaria.objects.filter(establecimiento__slug=store) \
                .filter(fecha_venta__range=(formatDate2, formatDate3)) \
                .order_by('fecha_venta')
            context = {'sales_filter_store': sales_filter_store}
            return render(request, "punto_venta/venta/ventas_diaria.html", context)

        context = {'sales_establecimiento': sales_establecimiento}
        return render(request, "punto_venta/venta/ventas_diaria.html", context)
    return redirect('login_user')


@login_required
def ventas(request, id_vd):
    if request.user.is_authenticated:
        venta = get_object_or_404(Venta_Diaria, pk=id_vd)
        sales = Venta.objects.filter(fecha_venta__day=venta.fecha_venta.day,
                                     fecha_venta__month=venta.fecha_venta.month,
                                     fecha_venta__year=venta.fecha_venta.year)
        context = {'sales': sales}
        return render(request, "punto_venta/venta/ventas.html", context)
    return redirect('login_user')


@login_required
def ventas_deudor(request):
    if request.user.is_authenticated:
        sales = Venta.objects.filter(tipo_pago='credit')
        context = {'sales': sales}
        return render(request, "punto_venta/deudores/deudores.html", context)
    return redirect('login_user')


@login_required
def ventas_slug(request, id_vd, store):
    if request.user.is_authenticated:
        venta = get_object_or_404(Venta_Diaria, pk=id_vd)
        sales = Venta.objects.filter(fecha_venta__day=venta.fecha_venta.day,
                                     fecha_venta__month=venta.fecha_venta.month,
                                     fecha_venta__year=venta.fecha_venta.year)
        context = {'sales': sales, 'slug_store': store}
        return render(request, "punto_venta/venta/ventas.html", context)
    return redirect('login_user')


def edit_credit(request, id_c=None):
    if request.user.is_authenticated:
        venta = Venta.objects.get(id=id_c)
        if request.method == 'POST':
            amount_credit = request.POST.get('amount_credit')

            Venta.objects.filter(id=id_c).update(venta_total=amount_credit)

            messages.success(request, 'El crédito de ' + venta.deudor + ' fue modificada satisfactoriamente')
            return redirect('ventas_deudor')
        context = {'venta': venta}
        return render(request, 'punto_venta/deudores/deudores.html', context)
    return redirect('login_user')


############# Materiales ##############

@login_required
def materiales(request):
    materials = Material.objects.all().order_by('id')
    context = {'materials': materials}
    return render(request, "almacen/material/materiales.html", context)


@login_required
def agregar_material(request):
    if request.method == 'POST':
        materialForm = MaterialForm(request.POST or None, request.FILES or None)
        if materialForm.is_valid():
            material_form = materialForm.save(commit=False)
            material_form.save()
            messages.success(request, "El material se agregó satisfactoriamente!")
            return redirect("materiales")
        else:
            print(materialForm.errors)
    else:
        materialForm = MaterialForm()
    return render(request, 'almacen/material/insertar_material.html',
                  {'materialForm': materialForm})


@login_required
def modificar_material(request, material=None):
    if request.user.is_authenticated:
        material_custom = Material.objects.get(slug=material)
        update_form = MaterialForm(request.POST or None, request.FILES or None, instance=material_custom)
        if update_form.is_valid():
            edit = update_form.save(commit=False)
            edit.save()
            messages.success(request, 'Material modificado correctamente')
            return redirect('materiales')
        context = {'material': material_custom, 'update_form': update_form, }
        return render(request, 'almacen/material/modificar_material.html', context)
    return redirect('login_user')


@login_required
def eliminar_material(request, material):
    if request.user.is_authenticated:
        m = Material.objects.get(slug=material)
        m.delete()
        messages.success(request, 'Material eliminado satisfactoriamente')
        return redirect('materiales')
    return redirect('login_user')


@login_required
def add_incrementar_material(request, material):
    if request.user.is_authenticated:
        if request.method == "POST":
            material_custom = Material.objects.get(slug=material)
            count_incrementar = request.POST.get('count_incrementar')

            if Moneda.objects.filter(material=material_custom).exists():
                if Moneda.objects.filter(material=material_custom).filter(fecha__day=today.day,
                                                                          fecha__month=today.month,
                                                                          fecha__year=today.year).exists():
                    if_incrementar = Moneda.objects.filter(material=material_custom).filter(
                        fecha__day=today.day,
                        fecha__month=today.month,
                        fecha__year=today.year)[
                                     :1].get()
                    cant_existente = if_incrementar.cantidad_material_entrada + int(count_incrementar)
                    Moneda.objects.filter(material=material_custom).filter(fecha__day=today.day,
                                                                           fecha__month=today.month,
                                                                           fecha__year=today.year) \
                        .update(cantidad_material_entrada=int(cant_existente))
                    count_incrementar_prod = material_custom.cantidad + int(count_incrementar)
                    Material.objects.filter(slug=material).update(cantidad=count_incrementar_prod)
                else:
                    c = Moneda.objects.create(material=material_custom,
                                              cantidad_material_entrada=int(count_incrementar),
                                              fecha=datetime.now())
                    c.save()
                    count_incrementar_prod = material_custom.cantidad + int(count_incrementar)
                    Material.objects.filter(slug=material).update(cantidad=count_incrementar_prod)
            else:
                c = Moneda.objects.create(material=material_custom,
                                          cantidad_material_entrada=int(count_incrementar),
                                          fecha=datetime.now())
                c.save()
                count_incrementar_prod = material_custom.cantidad + int(count_incrementar)
                Material.objects.filter(slug=material).update(cantidad=count_incrementar_prod)

            messages.success(request, 'Material incrementado satisfactoriamente')
            return redirect('materiales')
        context = {}
        return render(request, "almacen/material/materiales.html", context)
    return redirect('login_user')


@login_required
def add_merma_material(request, material):
    if request.user.is_authenticated:
        if request.method == "POST":
            material_custom = Material.objects.get(slug=material)
            count_merma = request.POST.get('count_merma')
            today = date.today()
            if Merma_Material.objects.filter(material=material_custom).exists():
                if Merma_Material.objects.filter(material=material_custom).filter(fecha__day=today.day,
                                                                                  fecha__month=today.month,
                                                                                  fecha__year=today.year).exists():
                    if_merma = Merma_Material.objects.filter(material=material_custom).filter(fecha__day=today.day,
                                                                                              fecha__month=today.month,
                                                                                              fecha__year=today.year)[
                               :1].get()
                    cant_existente = if_merma.cantidad_material_merma + int(count_merma)
                    Merma_Material.objects.filter(material=material_custom).filter(fecha__day=today.day,
                                                                                   fecha__month=today.month,
                                                                                   fecha__year=today.year) \
                        .update(cantidad_material_merma=int(cant_existente))
                    count_merma_prod = material_custom.cantidad - int(count_merma)
                    Material.objects.filter(slug=material).update(cantidad=count_merma_prod)
                else:
                    c = Merma_Material.objects.create(material=material_custom,
                                                      cantidad_material_merma=int(count_merma),
                                                      fecha=datetime.now())
                    c.save()
                    count_merma_prod = material_custom.cantidad - int(count_merma)
                    Material.objects.filter(slug=material).update(cantidad=count_merma_prod)
            else:
                c = Merma_Material.objects.create(material=material_custom, cantidad_material_merma=int(count_merma),
                                                  fecha=datetime.now())
                c.save()
                count_merma_prod = material_custom.cantidad - int(count_merma)
                Material.objects.filter(slug=material).update(cantidad=count_merma_prod)

            messages.success(request, 'Material mermado satisfactoriamente')
            return redirect('materiales')
        context = {}
        return render(request, "almacen/material/materiales.html", context)
    return redirect('login_user')


@login_required
def edit_merma_material(request, id_m=None):
    if request.user.is_authenticated:
        merma = Merma_Material.objects.get(id=id_m)
        if request.method == 'POST':
            count_merma = request.POST.get('count_merma')
            material_custom = Material.objects.get(id=merma.material.id)
            if int(count_merma) != 0:
                rest_merma = merma.cantidad_material_merma - int(count_merma)
                cant_existente = material_custom.cantidad + rest_merma
                Merma_Material.objects.filter(id=id_m).update(cantidad_material_merma=int(count_merma))
                Material.objects.filter(id=merma.material.id).update(cantidad=cant_existente)
                messages.success(request,
                                 'La cantidad mermada de ' + merma.material.nombre_material + ' fue modificada '
                                                                                              'satisfactoriamente')
            else:
                # messages.error(request, 'La cantidad no puede ser 0, si lo desea elimine el producto')
                cant_merma = material_custom.cantidad + merma.cantidad_material_merma
                Material.objects.filter(id=merma.material.id).update(cantidad=cant_merma)
                merma.delete()
                messages.success(request, 'Merma eliminada satisfactoriamente')
            return redirect('mermas_material')
        context = {'merma': merma}
        return render(request, 'punto_venta/merma/merma_material.html', context)
    return redirect('login_user')


@login_required
def delete_merma_material(request, id_m):
    if request.user.is_authenticated:
        m = Merma_Material.objects.get(id=id_m)
        producto_custom = Material.objects.get(id=m.material.id)
        cant_merma = producto_custom.cantidad + m.cantidad_material_merma
        Material.objects.filter(id=m.material.id).update(cantidad=cant_merma)
        m.delete()
        messages.success(request, 'Merma eliminada satisfactoriamente')
        return redirect('mermas_material')
    return redirect('login_user')


@login_required
def edit_entrada_material(request, id_e=None):
    if request.user.is_authenticated:
        entrada = Entrada_Material.objects.get(id=id_e)
        if request.method == 'POST':
            count_entrada = request.POST.get('count_entrada')
            if int(count_entrada) < entrada.cantidad_material_entrada:
                rest = entrada.cantidad_material_entrada - int(count_entrada)
                Entrada_Material.objects.filter(id=id_e).update(cantidad_material_entrada=rest)
                material = Material.objects.get(id=entrada.material.id)
                rest_material = material.cantidad - rest
                Material.objects.filter(id=entrada.material.id).update(cantidad=rest_material)
            else:
                diferencia = int(count_entrada) - entrada.cantidad_material_entrada
                suma = entrada.cantidad_material_entrada + diferencia
                Entrada_Material.objects.filter(id=id_e).update(cantidad_material_entrada=suma)
                material_custom = Material.objects.get(id=entrada.material.id)
                cant_existente = material_custom.cantidad + diferencia
                Material.objects.filter(id=entrada.material.id).update(cantidad=cant_existente)
            messages.success(request,
                             'La cantidad incrementada de ' + entrada.material.nombre_material + ' fue modificada '
                                                                                                 'satisfactoriamente')

            return redirect('entradas_materiales')
        context = {'entrada': entrada}
        return render(request, 'punto_venta/entrada/entrada_material.html', context)
    return redirect('login_user')


@login_required
def delete_entrada_material(request, id_e):
    if request.user.is_authenticated:
        e = Entrada_Material.objects.get(id=id_e)
        material_custom = Material.objects.get(id=e.material.id)
        cant_incrementar = material_custom.cantidad - e.cantidad_material_entrada
        Material.objects.filter(id=e.material.id).update(cantidad=cant_incrementar)
        e.delete()
        messages.success(request, 'Entrada eliminada satisfactoriamente')
        return redirect('entradas_materiales')
    return redirect('login_user')


@login_required
def add_name_ficha(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name_ficha = request.POST.get('name_ficha')

            c = Ficha_Tecnica_Nombre.objects.create(nombre_ficha=name_ficha)
            c.save()
            messages.success(request, 'El nombre de la ficha se agregó satisfactoriamente')
            return redirect(reverse('add_material', args=(c.slug,)))
        return render(request, 'punto_venta/producto/productos.html', {})
    return redirect('login_user')


@login_required
def add_material(request, ficha):
    materials = Material.objects.all().order_by('id')
    ficha_nombre = Ficha_Tecnica_Nombre.objects.get(slug=ficha)
    context = {'materials': materials, 'ficha': ficha, 'ficha_nombre': ficha_nombre}
    return render(request, "almacen/material/add_material.html", context)


@login_required
def add_count_material(request, ficha, material):
    if request.user.is_authenticated:
        if request.method == "POST":
            material_custom = Material.objects.get(slug=material)
            nombre_material_custom = Ficha_Tecnica_Nombre.objects.get(slug=ficha)
            count_material = request.POST.get('count_material')

            if float(count_material) != 0:
                if Ficha_Tecnica_Material.objects.filter(material__slug=material):
                    Ficha_Tecnica_Material.objects.filter(material__slug=material) \
                        .update(cantidad_material=float(count_material))
                    messages.success(request, 'Cantidad de material actualizado satisfactoriamente')
                    return redirect(reverse('add_material', args=(ficha,)))
                else:
                    c = Ficha_Tecnica_Material.objects.create(material=material_custom,
                                                              cantidad_material=float(count_material),
                                                              nombre_ficha=nombre_material_custom)
                    c.save()
                    messages.success(request, 'Cantidad de material agregado satisfactoriamente')
                    return redirect(reverse('add_material', args=(ficha,)))
            else:
                messages.error(request, 'La cantidad proporcionada no puede ser 0')
                return redirect(reverse('add_material', args=(ficha,)))

        context = {}
        return render(request, "almacen/material/add_material.html", context)
    return redirect('login_user')


@login_required
def add_gasto_material(request, ficha):
    if request.user.is_authenticated:
        if request.method == "POST":
            nombre_material_custom = Ficha_Tecnica_Nombre.objects.get(slug=ficha)
            gasto_directo_var = request.POST.get('gasto_directo_var')
            gasto_indirecto_var = request.POST.get('gasto_indirecto_var')
            impuesto = request.POST.get('impuesto')
            ficha_gasto_var = Ficha_Tecnica_Gastos.objects.create(gasto_directo=gasto_directo_var,
                                                                  gasto_indirecto=gasto_indirecto_var,
                                                                  impuesto=impuesto,
                                                                  nombre_ficha=nombre_material_custom)
            ficha_gasto_var.save()

            ficha_final = Ficha_Tecnica.objects.create(nombre_ficha=nombre_material_custom,
                                                       ficha_gasto_id=ficha_gasto_var.id)
            for item in Ficha_Tecnica_Material.objects.filter(nombre_ficha=nombre_material_custom):
                ficha_final.materiales.add(item)
            messages.success(request, 'Material agregado satisfactoriamente')
            return redirect('ficha_tecnica')
        return render(request, "almacen/material/add_material.html", context)
    return redirect('login_user')


class Ficha_Tecnica_Final:
    def __init__(self, id, nombre_ficha, ficha_slug, count_material, costo, slug):
        self.id = id
        self.nombre_ficha = nombre_ficha
        self.ficha_slug = ficha_slug
        self.count_material = count_material
        self.costo = costo
        self.slug = slug


@login_required
def ficha_tecnica(request):
    fichas = Ficha_Tecnica.objects.all()
    costo_material_final = 0.0
    fichas_final = []
    for item in fichas:
        costo_gasto = item.ficha_gasto.gasto_directo + item.ficha_gasto.gasto_indirecto + item.ficha_gasto.impuesto
        for item2 in item.materiales.all():
            costo_material = item2.material.costo * item2.cantidad_material
            costo_material_final += costo_material

        costo_final = costo_gasto + costo_material_final
        ficha = Ficha_Tecnica_Final(item.id, item.nombre_ficha.nombre_ficha, item.nombre_ficha.slug,
                                    item.materiales.count, costo_final, item.nombre_ficha.slug)
        fichas_final.append(ficha)

    context = {'fichas': fichas_final}
    return render(request, "punto_venta/ficha_tecnica/ficha_tecnica.html", context)


@login_required
def producir(request, ficha):
    if request.user.is_authenticated:
        if request.method == "POST":
            fichaTecnica = Ficha_Tecnica.objects.get(nombre_ficha__slug=ficha)

            count_prod = request.POST.get('count_prod')
            sumatoria_costo_material = 0.0
            for item in fichaTecnica.materiales.all():
                rebaja_material = item.cantidad_material * int(count_prod)
                rebaja_costo = rebaja_material * item.material.costo
                sumatoria_costo_material += rebaja_costo
                material_object = Material.objects.get(slug=item.material.slug)
                if material_object.cantidad > float(rebaja_material):
                    count_material_real = item.material.cantidad - float(rebaja_material)
                    Material.objects.filter(slug=item.material.slug).update(cantidad=count_material_real)

                else:
                    messages.error(request, 'Falta de material')
                    break

            costo_gastos = fichaTecnica.ficha_gasto.gasto_directo + fichaTecnica.ficha_gasto.gasto_indirecto + \
                           fichaTecnica.ficha_gasto.impuesto

            costo_producto = sumatoria_costo_material + costo_gastos

            if Producto.objects.filter(slug=fichaTecnica.nombre_ficha.slug):
                product = Producto.objects.get(slug=fichaTecnica.nombre_ficha.slug)
                count_update = product.cantidad_existente + int(count_prod)
                Producto.objects.filter(slug=fichaTecnica.nombre_ficha.slug).update(cantidad_existente=count_update,
                                                                                    costo=costo_producto)
            else:
                Producto.objects.create(nombre_producto=fichaTecnica.nombre_ficha.nombre_ficha,
                                        cantidad_existente=int(count_prod),
                                        costo=costo_producto)

            messages.success(request, 'Producción concluida satisfactoriamente')
            return redirect('ficha_tecnica')
        return render(request, "punto_venta/ficha_tecnica/ficha_tecnica.html", context)
    return redirect('login_user')


@login_required
def edit_material(request, ficha):
    ficha_nombre = Ficha_Tecnica_Nombre.objects.get(slug=ficha)
    fichas = Ficha_Tecnica_Material.objects.filter(nombre_ficha__slug=ficha)
    ficha_gasto = Ficha_Tecnica_Gastos.objects.get(nombre_ficha__slug=ficha)
    context = {'ficha': ficha, 'fichas': fichas, 'ficha_nombre': ficha_nombre, 'ficha_gasto': ficha_gasto}
    return render(request, "punto_venta/ficha_tecnica/edit_ficha_tecnica.html", context)


@login_required
def edit_count_material(request, ficha, material):
    if request.user.is_authenticated:
        if request.method == "POST":
            count_material = request.POST.get('count_material')

            if float(count_material) != 0:
                Ficha_Tecnica_Material.objects.filter(material__slug=material) \
                    .update(cantidad_material=float(count_material))
                messages.success(request, 'Cantidad de material actualizado satisfactoriamente')
                return redirect(reverse('edit_material', args=(ficha,)))
            else:
                messages.error(request, 'La cantidad proporcionada no puede ser 0')
                return redirect(reverse('edit_material', args=(ficha,)))

        context = {}
        return render(request, "punto_venta/ficha_tecnica/edit_ficha_tecnica.html", context)
    return redirect('login_user')


@login_required
def edit_gasto_material(request, ficha):
    if request.user.is_authenticated:
        if request.method == "POST":
            gasto_directo_var = request.POST.get('gasto_directo_var')
            gasto_indirecto_var = request.POST.get('gasto_indirecto_var')
            impuesto = request.POST.get('impuesto')
            Ficha_Tecnica_Gastos.objects.filter(nombre_ficha__slug=ficha) \
                .update(gasto_directo=float(gasto_directo_var), gasto_indirecto=float(gasto_indirecto_var),
                        impuesto=float(impuesto))

            messages.success(request, 'Ficha técnica actualizada satisfactoriamente')
            return redirect('ficha_tecnica')
        return render(request, "punto_venta/ficha_tecnica/edit_ficha_tecnica.html", context)
    return redirect('login_user')


############# Moneda ##############

@login_required
def monedas(request):
    coins = Moneda.objects.all().order_by('id')
    context = {'coins': coins}
    return render(request, "punto_venta/moneda/moneda.html", context)


@login_required
def agregar_moneda(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nombre_moneda = request.POST.get('nombre_moneda')
            tasa = request.POST.get('tasa')

            e = Moneda.objects.create(moneda=nombre_moneda, tasa=tasa)
            e.save()

            messages.success(request, 'El tipo de moneda se agregó satisfactoriamente')
            return redirect('monedas')

        return render(request, 'punto_venta/moneda/moneda.html', {})
    return redirect('login_user')


@login_required
def editar_moneda(request, moneda_slug=None):
    if request.user.is_authenticated:
        moneda = Moneda.objects.get(slug=moneda_slug)
        if request.method == 'POST':
            nombre_moneda = request.POST.get('nombre_moneda')
            tasa = request.POST.get('tasa')

            slug = slugify(nombre_moneda)
            Moneda.objects.filter(slug=moneda_slug).update(moneda=nombre_moneda)
            Moneda.objects.filter(slug=moneda_slug).update(tasa=tasa)
            Moneda.objects.filter(slug=moneda_slug).update(slug=slug)

            messages.success(request, 'La moneda fue modificada satisfactoriamente')
            return redirect('monedas')
        context = {'moneda': moneda}
        return render(request, 'punto_venta/moneda/moneda.html', context)
    return redirect('login_user')


@login_required
def eliminar_moneda(request, moneda):
    if request.user.is_authenticated:
        m = Moneda.objects.get(slug=moneda)
        m.delete()
        messages.success(request, 'La moneda fue eliminada satisfactoriamente')
        return redirect('monedas')
    return redirect('login_user')
