from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import *
import random   
# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')



#------------------------------VISTA LOGIN-------------------------------------
@csrf_exempt
def login_registro(request):
    context = {}
    if request.method == 'POST':
        if 'txtUsuIng' in request.POST and 'txtPasswordIng' in request.POST:
            usuario = request.POST.get('txtUsuIng')
            clave = request.POST.get('txtPasswordIng')
            user = authenticate(request, username=usuario, password=clave)
            if user is not None:
                login(request, user)
                return redirect('/inicio')
            else:
                context['error'] = 'Credenciales inválidas. Intente nuevamente.'

        elif ('txtNomUsuReg' in request.POST and 'txtApeUsuReg' in request.POST and
              'txtCorreoReg' in request.POST and 'txtDirecReg' in request.POST and
              'txtNumReg' in request.POST and 'txtPasswordReg' in request.POST):
            
            nombre_usuario = request.POST.get('txtNomUsuReg')
            apellido_usuario = request.POST.get('txtApeUsuReg')
            correo = request.POST.get('txtCorreoReg')
            direccion = request.POST.get('txtDirecReg')
            telefono = request.POST.get('txtNumReg')
            contraseña = request.POST.get('txtPasswordReg')

            if User.objects.filter(username=nombre_usuario).exists():
                context['error'] = 'El nombre de usuario ya está en uso. Intente con otro nombre.'
            elif User.objects.filter(email=correo).exists():
                context['error'] = 'El correo electrónico ya está en uso. Intente con otro correo.'
            else:
                user = User.objects.create_user(username=nombre_usuario, email=correo, password=contraseña)
                user.nombre = nombre_usuario
                user.apellido = apellido_usuario
                user.direccion = direccion
                user.telefono = telefono
                user.save()
                
                login(request, user)
                return redirect('/inicio')

    return render(request, 'login.html', context)

def logout_view(request):
    if request.method == 'POST':
        # Si se envía una solicitud POST con el nombre 'logout', entonces realiza el logout.
        logout(request)
        return redirect('inicio')   
    




#------------------------------VISTA AGREGAR PRODUCTO-------------------------------------
@login_required
@user_passes_test(lambda u: u.nivel == 'admin')
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('agregar_producto')
    else:
        form = ProductoForm()

    return render(request, 'agregar_producto.html', {'form': form})

@login_required
def load_subcategorias(request):
    categoria_id = request.GET.get('categoria_id')
    subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id).order_by('nombre')
    return JsonResponse(list(subcategorias.values('id_subcategoria', 'nombre')), safe=False)






#------------------------------VISTA PRODUCTOS-------------------------------------

def lista_productos(request):
    productos = Producto.objects.all()
    if request.user.is_authenticated:
        cantidad_compras = Carrito.objects.filter(usuario=request.user).aggregate(total=models.Sum('cantidad'))['total']
    else:
        cantidad_compras = 0
    return render(request, 'productos.html', {'productos': productos, 'cantidad_compras': cantidad_compras})






#------------------------------PRODUCTOS, CARRITO Y EDIT CARRITO-------------------------------------


@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    productos_usuario = carrito.select_related('producto')
    total = carrito.count()
    total_precio = sum(item.producto.precio * item.cantidad for item in carrito)
    productos_aleatorios = Producto.objects.exclude(sku__in=[item.producto.sku for item in carrito]).order_by('?')[:4]
    return render(request, 'compras.html', {
        'productos_usuario': productos_usuario,
        'total': total,
        'total_precio': total_precio,
        'productos_aleatorios': productos_aleatorios
    })

@csrf_exempt
@login_required
def sumar_producto(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        producto = Producto.objects.get(sku=sku)
        carrito = Carrito.objects.get(usuario=request.user, producto=producto)
        carrito.cantidad += 1
        carrito.save()
        
        # Obtener la cantidad total de productos en el carrito
        total_cantidad = Carrito.objects.filter(usuario=request.user).aggregate(total=models.Sum('cantidad'))['total']
        total_precio = sum(item.producto.precio * item.cantidad for item in Carrito.objects.filter(usuario=request.user))
        
        return JsonResponse({'status': 'success', 'total_cantidad': total_cantidad, 'total_precio': total_precio})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@csrf_exempt
@login_required
def restar_producto(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        producto = Producto.objects.get(sku=sku)
        carrito = Carrito.objects.get(usuario=request.user, producto=producto)
        if carrito.cantidad > 1:
            carrito.cantidad -= 1
            carrito.save()
        else:
            carrito.delete()
        
        # Obtener la cantidad total de productos en el carrito
        total_cantidad = Carrito.objects.filter(usuario=request.user).aggregate(total=models.Sum('cantidad'))['total']
        total_precio = sum(item.producto.precio * item.cantidad for item in Carrito.objects.filter(usuario=request.user))
        
        return JsonResponse({'status': 'success', 'total_cantidad': total_cantidad, 'total_precio': total_precio})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@csrf_exempt
@login_required
def comprar_producto(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        producto = Producto.objects.get(sku=sku)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
        if not created:
            carrito.cantidad += 1
            carrito.save()
        
        # Obtener la cantidad total de productos en el carrito
        total_cantidad = Carrito.objects.filter(usuario=request.user).aggregate(total=models.Sum('cantidad'))['total']
        
        return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito', 'total_cantidad': total_cantidad})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

