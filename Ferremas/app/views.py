import json
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import *
from .mercadopago import *
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





#------------------------------MERCADO PAGO-------------------------------------
@csrf_exempt
@login_required
def process_payment(request):
    if request.method == "POST":
        try:
            print("Datos recibidos:", request.body)

            form_data = json.loads(request.body)
            transaction_amount = form_data.get("transaction_amount")
            items = form_data.get("items")

            print("Transaction amount:", transaction_amount)
            print("Items:", items)

            if items is None or transaction_amount is None:
                return JsonResponse(
                    {"error": "Datos incompletos en la solicitud"}, status=400
                )

            # Crear la orden
            order = Order.objects.create(
                user=request.user, total_amount=transaction_amount
            )

            print("Orden creada:", order)

            if "compras" in request.session:
                del request.session["compras"]
                request.session.modified = True

            for item in items:
                print("Procesando item:", item)
                producto = get_object_or_404(Producto, sku=item["sku"])
                print("Producto encontrado:", producto)
                OrderItem.objects.create(
                    order=order,
                    product=producto,
                    quantity=item["cantidad"],
                    price=item["precio"],
                    image=item.get("imagen"),
                )

                # Decrementar el stock del producto
                try:
                    producto.decrementar_stock(item["cantidad"])
                    print("Stock decrementado para el producto:", producto)
                except ValueError as e:
                    # Manejar el error de stock insuficiente, si es necesario
                    return JsonResponse({"error": str(e)}, status=400)

            # Actualizar estado de la orden a "procesando"
            order.status = "processing"
            order.save()
            print("Estado de la orden actualizado a procesando")

            # Redirigir a la página de pago exitoso con el ID de la orden
            return JsonResponse({"redirect_url": f"/pago_exitoso/{order.id}/"})

        except json.JSONDecodeError as json_error:
            print("Error JSON:", str(json_error))
            return JsonResponse(
                {"error": "Error al decodificar los datos JSON"}, status=400
            )
        except Exception as e:
            print("Error general:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)


@login_required
def crear_preferencia(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transaction_amount = data.get("transaction_amount")
        items = data.get("items")

        print("Datos recibidos para crear preferencia:", data)

        user = request.user
        payer_info = {
            "name": user.first_name,
            "surname": user.last_name,
            "email": user.email,
        }

        preference_items = []
        for item in items:
            preference_items.append(
                {
                    "title": item["nombre"],
                    "quantity": item["cantidad"],
                    "unit_price": item["precio"],
                    "picture_url": item.get("imagen"),
                }
            )

        preference_data = {
            "items": preference_items,
            "payer": payer_info,
            "back_urls": {
                "success": "http://127.0.0.1:8000/pago_exitoso/",
                "failure": "http://127.0.0.1:8000/pago_fallido/",
                "pending": "http://127.0.0.1:8000/pago_pendiente/",
            },
            "auto_return": "approved",
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        print("Preferencia creada:", preference)

        return JsonResponse({"preference_id": preference["id"]})


@login_required
def cargar_pago_exitoso(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {"order": order, "items": order.items.all()}
    return render(request, "editar", context)


def CargarPagofallido(request):
    return render(request, "editar")


def CargarPagopendiente(request):
    return render(request, "editar")

