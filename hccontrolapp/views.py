from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from datetime import datetime
from hccontrolapp.models import Categoria_Producto, Producto, Merma
from hccontrolapp.form import ProductoForm
from datetime import date


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
    return render(request, 'login.html', {'form': form})


def logout(request):
    do_logout(request)
    return redirect('login_user')


def panel_home(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, "index.html", context)
    return redirect('login_user')


def categories_productos(request):
    if request.user.is_authenticated:
        categories_products = Categoria_Producto.objects.all()
        context = {'categories_products': categories_products}
        return render(request,
                      "punto_venta/categoria_producto/categorias_productos.html",
                      context)
    return redirect('login_user')


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
                      {'categoryForm': categoryForm})
    return redirect('login_user')


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


def eliminar_categoria(request, id_cp):
    if request.user.is_authenticated:
        cp = Categoria_Producto.objects.get(id=id_cp)
        cp.delete()
        return redirect('categories_productos')
    return redirect('login_user')


#############Productos##############

def productos(request):
    products = Producto.objects.all()
    context = {'productos': products}
    return render(request, "punto_venta/producto/productos.html", context)


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


def modificar_producto(request, id_p=None):
    if request.user.is_authenticated:
        producto_custom = Producto.objects.get(id=id_p)
        update_form = ProductoForm(request.POST or None, request.FILES or None, instance=producto_custom)
        if update_form.is_valid():
            edit = update_form.save(commit=False)
            edit.save()
            messages.success(request, 'Producto modificado correctamente')
            return redirect('productos')
        context = {'producto': producto_custom, 'update_form': update_form, }
        return render(request, 'punto_venta/productos/modificar_productos.html', context)
    return redirect('login_user')


def eliminar_producto(request, id_p):
    if request.user.is_authenticated:
        p = Producto.objects.get(id=id_p)
        p.delete()
        messages.success(request, 'Producto eliminado satisfactoriamente')
        return redirect('productos')
    return redirect('login_user')


def mermas(request):
    decrease = Merma.objects.all()
    context = {'mermas': decrease}
    return render(request, "punto_venta/merma/merma.html", context)


def add_merma(request, id_p):
    if request.user.is_authenticated:
        if request.method == "POST":
            producto_custom = Producto.objects.get(id=id_p)
            count_merma = request.POST.get('count_merma')
            today = date.today()
            if Merma.objects.filter(producto=producto_custom).exists():
                if Merma.objects.filter(producto=producto_custom).filter(fecha__day=today.day).exists():
                    if_merma = Merma.objects.filter(producto=producto_custom).filter(fecha__day=today.day)[:1].get()
                    cant_existente = if_merma.cantidad_producto_merma + int(count_merma)
                    Merma.objects.filter(producto=producto_custom).filter(fecha__day=today.day) \
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

            messages.success(request, 'Producto mermado satisfactoriamente')
            return redirect('productos')
        context = {}
        return render(request, "punto_venta/producto/productos.html", context)
    return redirect('login_user')


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

            return redirect('mermas')
        context = {'merma': merma}
        return render(request, 'punto_venta/merma/merma.html', context)
    return redirect('login_user')


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
