from hccontrolapp.models import Establecimiento


def puntos(request):
    puntos_venta = Establecimiento.objects.filter(user=request.user)
    return {'puntos_venta': puntos_venta}
