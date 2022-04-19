from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from datetime import datetime
from hccontrolapp.models import Categoria_Producto, Producto, Merma, Gastos, Venta, Venta_Diaria, Entrada, \
    Establecimiento, Traslado, User, Material
from hccontrolapp.form import ProductoForm, TrasladoForm
from datetime import date
from django.db import transaction
from django.contrib.auth.decorators import login_required


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
    return render(
        request,
        'login.html',
        {'form': form}
    )


@login_required
def logout(request):
    do_logout(request)
    return redirect('login_user')


@login_required
def panel_home(request):
    if request.user.is_authenticated:
        return render(request, "index.html", {})
    return redirect('login_user')


@login_required
def usuarios(request):
    users = User.objects.exclude(is_superuser=True)
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
            print(userForm.errors)
    else:
        userForm = UserForm()
    return render(request, 'usuarios/insertar_usuarios.html',
                  {'userForm': userForm})


@login_required
def editar_usuario(request, id_user=None):
    if request.user.is_authenticated:
        user_custom = User.objects.get(id=id_user)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            carnet = request.POST.get('carnet')
            genero = request.POST.get('sexo')
            user_name = request.POST.get('user_name')
            rol_de = request.POST.get('rol_de')
            password1 = request.POST.get('password1')
            with transaction.atomic():
                user_custom.set_password(password1)
                user_custom.save()
                if rol_de == 'dependiente':
                    User.objects.filter(id=id_user).update(
                        first_name=first_name,
                        last_name=last_name,
                        carnet=carnet,
                        username=user_name,
                        is_dependiente=True,
                        is_administrador=False,
                        sexo=genero
                    )
                else:
                    User.objects.filter(id=id_user).update(
                        first_name=first_name,
                        last_name=last_name,
                        carnet=carnet,
                        username=user_name,
                        is_dependiente=False,
                        is_administrador=True,
                        sexo=genero
                    )
            messages.success(request, 'Datos de usuario actualizado satisfactoriamente')
            return redirect('usuarios')
        context = {'user': user_custom}
        return render(request, 'usuarios/editar_usuarios.html', context)
    return redirect('login_user')


@login_required
def eliminar_usuario(request, id_user):
    if request.user.is_authenticated:
        u = User.objects.get(id=id_user)
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
        users = User.objects.all()
        context = {'establecimientos': establecimiento, 'users': users}
        return render(request, "punto_venta/establecimiento/establecimientos.html", context)
    return redirect('login_user')


@login_required
def agregar_establecimiento(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nombre_establecimiento = request.POST.get('nombre_establecimiento')
            descripcion_establecimiento = request.POST.get('descripcion_establecimiento')
            user_responsable = request.POST.get('user_responsable')

            e = Establecimiento.objects.create(
                nombre_establecimiento=nombre_establecimiento,
                descripcion=descripcion_establecimiento,
                user_id=int(user_responsable)
            )
            e.save()
            messages.success(request, 'El establecimiento se agregó satisfactoriamente')
            return redirect('establecimientos')
        return render(request, 'punto_venta/establecimiento/establecimientos.html', {})
    return redirect('login_user')


@login_required
def editar_establecimiento(request, id_e=None):
    if request.user.is_authenticated:
        establecimiento = Establecimiento.objects.get(id=id_e)
        if request.method == 'POST':
            nombre_establecimiento = request.POST.get('nombre_establecimiento')
            descripcion_establecimiento = request.POST.get('descripcion_establecimiento')

            Establecimiento.objects.filter(id=id_e).update(nombre_establecimiento=nombre_establecimiento)
            Establecimiento.objects.filter(id=id_e).update(descripcion=descripcion_establecimiento)

            messages.success(request, 'El establecimiento fue modificado satisfactoriamente')
            return redirect('establecimientos')
        context = {'establecimiento': establecimiento}
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
def traslado(request, product_parameter):
    product = get_object_or_404(Producto, slug=product_parameter)
    if request.method == "POST":
        trasladoForm = TrasladoForm(request.POST, establecimiento_id=product.establecimiento_id)
        if trasladoForm.is_valid():
            establecimiento_id = trasladoForm.cleaned_data['establecimiento'].id
            count = trasladoForm.cleaned_data['cantidad_trasladar']
            if int(count) <= product.cantidad_existente:
                resta_existente = product.cantidad_existente - int(count)
                Producto.objects.filter(id=product.id).update(cantidad_existente=resta_existente)

                if not Producto.objects.filter(id=product.id).filter(establecimiento_id=establecimiento_id).exists():
                    newProducto = Producto(imagen=product.imagen,
                                           nombre_producto=product.nombre_producto,
                                           cantidad_existente=int(count),
                                           costo=product.costo,
                                           precio_venta=product.precio_venta,
                                           categoria_producto=product.categoria_producto,
                                           establecimiento_id=establecimiento_id,
                                           slug=product.slug)
                    newProducto.save()

                    move = Traslado(producto_id=newProducto.id, establecimiento_id=establecimiento_id,
                                    establecimiento_padre_id=product.establecimiento_id,
                                    cantidad_trasladar=int(count), user=request.user)
                    move.save()

                else:
                    product_traslado = Producto.objects.filter(id=product.id) \
                        .filter(establecimiento_id=establecimiento_id)
                    agregar_existente = product_traslado[0].cantidad_existente + int(count)

                    Producto.objects.filter(id=product.id).filter(establecimiento_id=establecimiento_id).update(
                        cantidad_existente=agregar_existente)

                    move = Traslado(producto_id=id_p, establecimiento_id=establecimiento_id,
                                    establecimiento_padre_id=product.establecimiento_id,
                                    cantidad_trasladar=int(count), user=request.user)
                    move.save()

                messages.success(request, "El traslado se realizó satisfactoriamente!")
                return redirect(reverse('productos_establecimientos', args=(product.establecimiento.slug,)))
            else:
                messages.error(request, "Cantidad insuficiente para realizar el traslado!")
                return redirect(reverse('traslado', args=(id_p,)))
    else:
        trasladoForm = TrasladoForm(request.POST, establecimiento_id=product.establecimiento_id)

    return render(request, 'punto_venta/traslado/insertar_traslado.html',
                  {'trasladoForm': trasladoForm})


@login_required
def traslados(request):
    transfers = Traslado.objects.all().order_by('id')
    context = {'traslados': transfers}
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


#############Productos##############
@login_required
def productos_establecimientos(request, store):
    products = Producto.objects.filter(establecimiento__slug=store).order_by('id')
    context = {'productos': products}
    return render(request, "punto_venta/producto/productos_establecimientos.html", context)


@login_required
def productos(request):
    products = Producto.objects.all().order_by('id')
    context = {'productos': products}
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


today = date.today()


@login_required
def entradas(request):
    increases = Entrada.objects.all()
    context = {'increases': increases}
    return render(request, "punto_venta/entrada/entrada.html", context)


@login_required
def add_incrementar(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = Producto.objects.get(id=id_p)
            count_incrementar = request.POST.get('count_incrementar')

            if Entrada.objects.filter(producto=producto_custom).exists():
                if Entrada.objects.filter(producto=producto_custom).filter(fecha__day=today.day,
                                                                           fecha__month=today.month,
                                                                           fecha__year=today.year).exists():
                    if_incrementar = Entrada.objects.filter(producto=producto_custom).filter(fecha__day=today.day,
                                                                                             fecha__month=today.month,
                                                                                             fecha__year=today.year)[
                                     :1].get()
                    cant_existente = if_incrementar.cantidad_producto_entrada + int(count_incrementar)
                    Entrada.objects.filter(producto=producto_custom).filter(fecha__day=today.day,
                                                                            fecha__month=today.month,
                                                                            fecha__year=today.year) \
                        .update(cantidad_producto_entrada=int(cant_existente))
                    count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)
                else:
                    c = Entrada.objects.create(producto=producto_custom,
                                               cantidad_producto_entrada=int(count_incrementar),
                                               fecha=datetime.now())
                    c.save()
                    count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)
            else:
                c = Entrada.objects.create(producto=producto_custom,
                                           cantidad_producto_entrada=int(count_incrementar),
                                           fecha=datetime.now())
                c.save()
                count_incrementar_prod = producto_custom.cantidad_existente + int(count_incrementar)
                Producto.objects.filter(id=id_p).update(cantidad_existente=count_incrementar_prod)

            operations_sales(request)
            messages.success(request, 'Producto incrementado satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto_custom.establecimiento.id,)))
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

            operations_sales(request)
            return redirect('entradas')
        context = {'entradas': entradas}
        return render(request, 'punto_venta/entrada/entrada.html', context)
    return redirect('login_user')


@login_required
def delete_entrada(request, id_e):
    if request.user.is_authenticated:
        e = Entrada.objects.get(id=id_e)
        producto_custom = Producto.objects.get(id=e.producto.id)
        cant_incrementar = producto_custom.cantidad_existente - e.cantidad_producto_entrada
        Producto.objects.filter(id=e.producto.id).update(cantidad_existente=cant_incrementar)
        e.delete()
        messages.success(request, 'Entrada eliminada satisfactoriamente')
        return redirect('entradas')
    return redirect('login_user')


@login_required
def mermas(request):
    decrease = Merma.objects.all()
    context = {'mermas': decrease}
    return render(request, "punto_venta/merma/merma.html", context)


@login_required
def add_merma(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = Producto.objects.get(id=id_p)
            count_merma = request.POST.get('count_merma')
            today = date.today()
            if Merma.objects.filter(producto=producto_custom).exists():
                if Merma.objects.filter(producto=producto_custom).filter(fecha__day=today.day,
                                                                         fecha__month=today.month,
                                                                         fecha__year=today.year).exists():
                    if_merma = Merma.objects.filter(producto=producto_custom).filter(fecha__day=today.day,
                                                                                     fecha__month=today.month,
                                                                                     fecha__year=today.year)[:1].get()
                    cant_existente = if_merma.cantidad_producto_merma + int(count_merma)
                    Merma.objects.filter(producto=producto_custom).filter(fecha__day=today.day,
                                                                          fecha__month=today.month,
                                                                          fecha__year=today.year) \
                        .update(cantidad_producto_merma=int(cant_existente))
                    count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)
                else:
                    c = Merma.objects.create(producto=producto_custom, cantidad_producto_merma=int(count_merma),
                                             fecha=datetime.now())
                    c.save()
                    count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                    Producto.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)
            else:
                c = Merma.objects.create(producto=producto_custom, cantidad_producto_merma=int(count_merma),
                                         fecha=datetime.now())
                c.save()
                count_merma_prod = producto_custom.cantidad_existente - int(count_merma)
                Producto.objects.filter(id=id_p).update(cantidad_existente=count_merma_prod)

            operations_sales(request)
            messages.success(request, 'Producto mermado satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto_custom.establecimiento.id,)))
        context = {}
        return render(request, "punto_venta/producto/productos.html", context)
    return redirect('login_user')


@login_required
def edit_merma(request, id_m=None):
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

            operations_sales(request)
            return redirect('mermas')
        context = {'merma': merma}
        return render(request, 'punto_venta/merma/merma.html', context)
    return redirect('login_user')


@login_required
def delete_merma(request, id_m):
    if request.user.is_authenticated:
        m = Merma.objects.get(id=id_m)
        producto_custom = Producto.objects.get(id=m.producto.id)
        cant_merma = producto_custom.cantidad_existente + m.cantidad_producto_merma
        Producto.objects.filter(id=m.producto.id).update(cantidad_existente=cant_merma)
        m.delete()
        messages.success(request, 'Merma eliminada satisfactoriamente')
        return redirect('mermas')
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
def add_spending(request):
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
def buy(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto = Producto.objects.get(id=id_p)
            payment_type = request.POST.get('payment_type')
            count_product_var = request.POST.get('count_product_var')
            deudor_name = request.POST.get('deudor_name')

            venta_monto = int(count_product_var) * producto.precio_venta
            venta_monto_costo = int(count_product_var) * producto.costo
            if deudor_name:
                Venta.objects.create(usuario=request.user, producto=producto, cantidad=int(count_product_var),
                                     tipo_pago=payment_type, venta_total=venta_monto, costo=venta_monto_costo,
                                     deudor=deudor_name, fecha_venta=datetime.now())
            else:
                Venta.objects.create(usuario=request.user, producto=producto, cantidad=int(count_product_var),
                                     tipo_pago=payment_type, venta_total=venta_monto, costo=venta_monto_costo,
                                     fecha_venta=datetime.now())

            count_venta = producto.cantidad_existente - int(count_product_var)
            Producto.objects.filter(id=producto.id).update(cantidad_existente=count_venta)

            operations_sales(request)

            messages.success(request, 'Venta registrada satisfactoriamente')
            return redirect(reverse('productos_establecimientos', args=(producto.establecimiento.id,)))

        context = {}
        return render(request, "punto_venta/producto/productos.html", context)
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
def materiales(request):
    materials = Material.objects.all().order_by('id')
    context = {'materials': materials}
    return render(request, "almacen/material/materiales.html", context)


@login_required
def agregar_material(request):
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
