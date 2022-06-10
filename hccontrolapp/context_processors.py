from django.shortcuts import render, redirect
from hccontrolapp.models import Establecimiento
from django.db.models.query import QuerySet


def puntos(request):
    puntos_venta = None
    puntos_venta_all = None
    if request.user.is_authenticated:
        try:
            puntos_venta = Establecimiento.objects.filter(user__in=[request.user])
            puntos_venta_all = Establecimiento.objects.exclude(slug='almacen')

        except DoesNotExist:
            pass

    if puntos_venta or puntos_venta_all:
        points_ok = Establecimiento.objects.filter(user__in=[request.user])
        points_all_ok = Establecimiento.objects.exclude(slug='almacen')
    else:
        points_ok = []
        points_all_ok = []

    return {'puntos_venta': points_ok, 'puntos_venta_all': points_all_ok}
