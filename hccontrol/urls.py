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

                  path('almacen', views.productos, name="productos"),
                  path('almacen/insertar-producto', views.agregar_producto, name="insertar_producto"),
                  path('almacen/editar_producto/<slug:product>', views.modificar_producto, name="editar_producto"),
                  path('productos_establecimientos/edit_product_establecimiento/<int:id_p>',
                       views.edit_product_establecimiento,
                       name="edit_product_establecimiento"),
                  path('productos/eliminar_producto/<int:id_p>', views.eliminar_producto, name="eliminar_producto"),

                  ############# Entradas ##############
                  path('entradas', views.entradas, name="entradas"),
                  path('entradas/<slug:store>', views.entradas_for_store, name="entradas_store"),
                  path('productos_establecimientos/add_incrementar/<int:id_p>', views.add_incrementar,
                       name="add_incrementar"),
                  path('entradas/edit_entrada/<int:id_e>', views.edit_entrada, name="edit_entrada"),
                  path('entradas/delete_entrada/<int:id_e>', views.delete_entrada, name="delete_entrada"),

                  path('productos/add_incrementar_general/<int:id_p>', views.add_incrementar_general,
                       name="add_incrementar_general"),
                  path('entradas/edit_entrada_general/<int:id_e>', views.edit_entrada_general,
                       name="edit_entrada_general"),
                  path('entradas/delete_entrada_general/<int:id_e>', views.delete_entrada_general,
                       name="delete_entrada_general"),

                  ############# Mermas ##############
                  path('mermas', views.mermas, name="mermas"),
                  path('mermas/<slug:store>', views.mermas_store, name="mermas_store"),
                  path('productos_establecimientos/add_merma/<int:id_p>', views.add_merma, name="add_merma"),
                  path('mermas/edit_merma/<int:id_m>', views.edit_merma, name="edit_merma"),
                  path('mermas/delete_merma/<int:id_m>', views.delete_merma, name="delete_merma"),

                  path('productos/add_merma_general/<int:id_p>', views.add_merma_general,
                       name="add_merma_general"),
                  path('merma/edit_merma_general/<int:id_e>', views.edit_merma_general,
                       name="edit_merma_general"),
                  path('merma/delete_merma_general/<int:id_e>', views.delete_merma_general,
                       name="delete_merma_general"),

                  ############# Gastos ##############
                  path('expenses/<slug:store>', views.expenses_store, name="expenses_store"),
                  path('expenses/add_spending/<slug:store>', views.add_spending, name="add_spending"),
                  path('expenses_general', views.expenses, name="expenses"),
                  path('expenses_general/add_spending_general', views.add_spending_general,
                       name="add_spending_general"),

                  ############# Venta Diaria ##############
                  path('productos_establecimientos/buy/<int:id_p>', views.buy, name="buy"),
                  path('ventas_diaria', views.ventas_diaria, name="ventas_diaria"),
                  path('ventas_diaria/<slug:store>', views.ventas_diaria_store, name="ventas_diaria_store"),
                  path('ventas_diaria/ventas/<int:id_vd>', views.ventas, name="ventas"),
                  path('ventas_diaria/ventas/<int:id_vd>/<slug:store>', views.ventas_slug, name="ventas_slug"),

                  ############# Traslado ##############
                  path('traslados', views.traslados, name="traslados"),
                  path('traslados/<slug:store>', views.traslados_store, name="traslados_store"),
                  path('productos/traslado/<slug:product_parameter>', views.traslado_general, name="traslado_general"),
                  path('productos_establecimientos/traslado/<slug:store_parameter>/<slug:product_parameter>',
                       views.traslado, name="traslado"),
                  path('traslados/edit_traslado/<int:id_t>', views.edit_traslado, name="edit_traslado"),
                  path('mermas/delete_traslado/<int:id_t>', views.delete_traslado, name="delete_traslado"),

                  path('materiales', views.materiales, name="materiales"),
                  path('materiales/insertar_material', views.agregar_material, name="insertar_material"),
                  path('materiales/modificar_material/<slug:material>',
                       views.modificar_material, name="modificar_material"),
                  path('materiales/eliminar_material/<slug:material>', views.eliminar_material,
                       name="eliminar_material"),
                  path('materiales/add_incrementar/<slug:material>', views.add_incrementar_material,
                       name="add_incrementar_material"),
                  path('materiales/add_merma/<slug:material>', views.add_merma_material, name="add_merma_material"),
                  path('mermas_material', views.mermas_material, name="mermas_material"),
                  path('mermas_material/edit_merma/<int:id_m>', views.edit_merma_material, name="edit_merma_material"),
                  path('mermas_material/delete_merma/<int:id_m>', views.delete_merma_material,
                       name="delete_merma_material"),
                  path('entradas_materiales', views.entradas_materiales, name="entradas_materiales"),
                  path('entradas_material/edit_entrada/<int:id_e>', views.edit_entrada_material,
                       name="edit_entrada_material"),
                  path('entradas_material/delete_entrada/<int:id_e>', views.delete_entrada_material,
                       name="delete_entrada_material"),

                  path('almacen/ficha-tecnica/add_name_ficha', views.add_name_ficha, name="add_name_ficha"),
                  path('almacen/ficha-tecnica/<slug:ficha>', views.add_material, name="add_material"),
                  path('almacen/ficha-tecnica/add-count-material/<slug:ficha>/<slug:material>'
                       , views.add_count_material, name="add_count_material"),
                  path('almacen/ficha-tecnica/add_gasto_material/<slug:ficha>'
                       , views.add_gasto_material, name="add_gasto_material"),
                  path('ficha-tecnica', views.ficha_tecnica, name="ficha_tecnica"),
                  path('producir/<slug:ficha>', views.producir, name="producir"),
                  path('ficha-tecnica/edit-material/<slug:ficha>', views.edit_material, name="edit_material"),
                  path('ficha-tecnica/edit-material/edit_count_material/<slug:ficha>/<slug:material>',
                       views.edit_count_material, name="edit_count_material"),
                  path('ficha-tecnica/edit-material/edit_gasto_material/<slug:ficha>',
                       views.edit_gasto_material, name="edit_gasto_material"),

                  path('monedas', views.monedas, name="monedas"),
                  path('monedas/agregar_moneda', views.agregar_moneda, name="agregar_moneda"),
                  path('monedas/editar_moneda/<slug:moneda_slug>', views.editar_moneda, name="editar_moneda"),
                  path('monedas/eliminar_moneda/<slug:moneda>', views.eliminar_moneda,
                       name="eliminar_moneda"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
