from .models import *

def carrito_total(request):
    if request.user.is_authenticated:
        total_cantidad = Carrito.objects.filter(usuario=request.user).aggregate(total=models.Sum('cantidad'))['total']
        if total_cantidad is None:
            total_cantidad = 0
    else:
        total_cantidad = 0
    return {'cantidad_compras': total_cantidad}
