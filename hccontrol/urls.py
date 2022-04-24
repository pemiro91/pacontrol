"""hccontrol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.customurls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.customurls'))
"""
from django.contrib import admin
from django.urls import path
from hccontrolapp import views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('', views.login_user, name="login_user"),
                  path('salir', views.logout, name="salir"),
                  path('panel', views.panel_home, name="panel"),

                  path('usuarios', views.usuarios, name="usuarios"),
                  path('usuarios/insertar_usuario', views.insertar_usuario, name="insertar_usuario"),
                  path('usuarios/editar_usuario/<slug:slug_username>', views.editar_usuario, name="editar_usuario"),
                  path('usuarios/eliminar_usuario/<slug:slug_username>', views.eliminar_usuario,
                       name="eliminar_usuario"),

                  path('categoria', views.categories_productos, name="categories_productos"),
                  path('categoria/agregar_categoria', views.agregar_categoria, name="agregar_categoria"),
                  path('categoria/editar_categoria/<int:id_o>', views.editar_categoria, name="editar_categoria"),
                  path('categoria/eliminar_categoria/<int:id_cp>', views.eliminar_categoria, name="eliminar_categoria"),

                  path('establecimientos', views.establecimientos, name="establecimientos"),
                  path('establecimiento/agregar_establecimiento', views.agregar_establecimiento,
                       name="agregar_establecimiento"),
                  path('establecimiento/editar_establecimiento/<int:id_e>', views.editar_establecimiento,
                       name="editar_establecimiento"),
                  path('establecimiento/eliminar_establecimiento/<int:id_e>', views.eliminar_establecimiento,
                       name="eliminar_establecimiento"),

                  path('productos_establecimientos/<slug:store>', views.productos_establecimientos,
                       name="productos_establecimientos"),

                  path('productos', views.productos, name="productos"),
                  path('productos/insertar_producto', views.agregar_producto, name="insertar_producto"),
                  path('productos/editar_producto/<slug:product>', views.modificar_producto, name="editar_producto"),
                  path('productos/eliminar_producto/<int:id_p>', views.eliminar_producto, name="eliminar_producto"),

                  path('entradas', views.entradas, name="entradas"),
                  path('entradas/<slug:store>', views.entradas_for_store, name="entradas_store"),
                  path('productos_establecimientos/add_incrementar/<int:id_p>', views.add_incrementar,
                       name="add_incrementar"),
                  path('entradas/edit_entrada/<int:id_e>', views.edit_entrada, name="edit_entrada"),
                  path('entradas/delete_entrada/<int:id_e>', views.delete_entrada, name="delete_entrada"),

                  path('mermas', views.mermas, name="mermas"),
                  path('mermas/<slug:store>', views.mermas_store, name="mermas_store"),
                  path('productos_establecimientos/add_merma/<int:id_p>', views.add_merma, name="add_merma"),
                  path('mermas/edit_merma/<int:id_m>', views.edit_merma, name="edit_merma"),
                  path('mermas/delete_merma/<int:id_m>', views.delete_merma, name="delete_merma"),

                  path('expenses', views.expenses, name="expenses"),
                  path('expenses/<slug:store>', views.expenses_store, name="expenses_store"),
                  path('expenses/add_spending', views.add_spending, name="add_spending"),
                  path('expenses/add_spending/<slug:store>', views.add_spending_store, name="add_spending_store"),

                  path('productos_establecimientos/buy/<int:id_p>', views.buy, name="buy"),
                  path('ventas_diaria', views.ventas_diaria, name="ventas_diaria"),
                  path('ventas_diaria/<slug:store>', views.ventas_diaria_store, name="ventas_diaria_store"),
                  path('ventas_diaria/ventas/<int:id_vd>', views.ventas, name="ventas"),
                  path('ventas_diaria/ventas/<int:id_vd>/<slug:store>', views.ventas_slug, name="ventas_slug"),

                  path('traslados', views.traslados, name="traslados"),
                  path('traslados/<slug:store>', views.traslados_store, name="traslados_store"),
                  path('productos_establecimientos/traslado/<slug:product_parameter>', views.traslado, name="traslado"),
                  path('traslados/edit_traslado/<int:id_t>', views.edit_traslado, name="edit_traslado"),
                  path('mermas/delete_traslado/<int:id_t>', views.delete_traslado, name="delete_traslado"),

                  path('materiales', views.materiales, name="materiales"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
